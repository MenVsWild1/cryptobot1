from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from database import Database
from game_logic import calculate_click_reward, apply_boost, handle_level_up, generate_referral_code
import config

app = Flask(__name__)
CORS(app)

db = Database(config.DATABASE_FILE)
db.load_data() # Load the data when the app starts

# Helper function to get user data safely
def get_safe_user_data(user_data):
    if user_data:
        return {
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'balance': user_data['balance'],
            'level': user_data['level'],
            'clicks': user_data['clicks'],
            'referral_code': user_data['referral_code'],
            'language': user_data['language']
        }
    else:
        return None

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user_data = db.get_user(user_id)
    safe_user_data = get_safe_user_data(user_data)
    if safe_user_data:
        return jsonify(safe_user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/click/<int:user_id>', methods=['POST'])
def handle_click(user_id):
    user_data = db.get_user(user_id)
    safe_user_data = get_safe_user_data(user_data)
    if not safe_user_data:
        return jsonify({'error': 'User not found'}), 404

    boost_type = request.args.get('boost', None) # Get boost type from query parameters
    boost_multiplier = apply_boost(boost_type, safe_user_data['balance'])

    reward = calculate_click_reward(safe_user_data['clicks'] + 1) * boost_multiplier
    db.update_clicks(user_id, safe_user_data['clicks'] + 1)
    db.update_balance(user_id, reward)

    # Level up check
    updated_user_data = db.get_user(user_id)
    safe_updated_user_data = get_safe_user_data(updated_user_data)
    level = safe_updated_user_data['level']
    clicks = safe_updated_user_data['clicks']
    if clicks >= level * 100:
      new_level = level + 1
      rewards = handle_level_up(user_id, new_level, db) # Pass database object
      db.update_level(user_id, new_level)
    else:
      new_level = level

    return jsonify({
        'balance': safe_updated_user_data['balance'],
        'clicks': safe_updated_user_data['clicks'],
        'reward': reward,
        'level': new_level
    })

@app.route('/api/top-players', methods=['GET'])
def get_top_players():
    top_users = db.get_top_players(limit=10)
    players = []
    for user in top_users:
        players.append({
            'user_id': user['user_id'],
            'username': user['username'],
            'balance': user['balance']
        })
    return jsonify(players)

@app.route('/api/daily-reward/<int:user_id>', methods=['POST'])
def get_daily_reward(user_id):
    user_data = db.get_user(user_id)
    safe_user_data = get_safe_user_data(user_data)
    if not safe_user_data:
        return jsonify({'error': 'User not found'}), 404

    reward = 100  # Example reward
    db.update_balance(user_id, reward)
    updated_user_data = db.get_user(user_id)
    safe_updated_user_data = get_safe_user_data(updated_user_data)
    return jsonify({
        'balance': safe_updated_user_data['balance']
    })

@app.route('/api/settings/<int:user_id>', methods=['POST'])
def save_settings(user_id):
    user_data = db.get_user(user_id)
    safe_user_data = get_safe_user_data(user_data)
    if not safe_user_data:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    nickname = data.get('nickname')
    language = data.get('language')

    db.update_nickname(user_id, nickname)
    db.update_language(user_id, language)

    return jsonify({'status': 'Settings saved'})

@app.route('/api/referral/<string:referral_code>/<int:user_id>', methods=['POST'])
def apply_referral(referral_code, user_id):
    referrer_data = db.get_user_by_referral_code(referral_code)
    if not referrer_data:
        return jsonify({'error': 'Invalid referral code'}), 400

    if referrer_data['user_id'] == user_id:
        return jsonify({'error': 'Cannot refer yourself'}), 400

    if db.add_referral(referrer_data['user_id'], user_id):
        db.update_balance(referrer_data['user_id'], 100)
        return jsonify({'message': 'Referral applied successfully'}), 200
    else:
        return jsonify({'error': 'Referral already applied'}), 409

# Event routes
@app.route('/api/event/market-crash', methods=['POST'])
def market_crash_event():
    users = db.get_all_users()
    for user in users:
        balance = user['balance']
        new_balance = int(balance * 0.7)  # -30%
        db.update_balance(user['user_id'], new_balance - balance)  # Update balance by the difference

    return jsonify({'message': 'Market crash event triggered'}), 200

@app.route('/api/event/airdrop', methods=['POST'])
def airdrop_event():
    users = db.get_all_users()
    if not users:
        return jsonify({'message': 'No users to airdrop to'}), 204

    lucky_user = random.choice(users)
    db.update_balance(lucky_user['user_id'], 1000)
    return jsonify({'message': f'Airdrop sent to user {lucky_user["user_id"]}'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
