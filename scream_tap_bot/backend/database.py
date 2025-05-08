import json
import os

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {'users': [], 'referrals': []} # Return empty dicts for empty file
        else:
            return {'users': [], 'referrals': []}

    def save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_user(self, user_id):
        for user in self.data['users']:
            if user['user_id'] == user_id:
                return user
        return None

    def get_all_users(self):
        return self.data['users']

    def create_user(self, user_id, username):
        referral_code = self.generate_referral_code()
        new_user = {
            'user_id': user_id,
            'username': username,
            'balance': 0,
            'level': 1,
            'clicks': 0,
            'referral_code': referral_code,
            'language': 'ru'
        }
        self.data['users'].append(new_user)
        self.save_data()
        return True

    def update_balance(self, user_id, amount):
        user = self.get_user(user_id)
        if user:
            user['balance'] += amount
            self.save_data()

    def update_clicks(self, user_id, clicks):
        user = self.get_user(user_id)
        if user:
            user['clicks'] = clicks
            self.save_data()

    def update_level(self, user_id, level):
        user = self.get_user(user_id)
        if user:
            user['level'] = level
            self.save_data()

    def get_top_players(self, limit=10):
        sorted_users = sorted(self.data['users'], key=lambda x: x['balance'], reverse=True)
        return sorted_users[:limit]

    def add_referral(self, referrer_id, referral_id):
        # Check if referral already exists
        for ref in self.data['referrals']:
            if ref['referrer_id'] == referrer_id and ref['referral_id'] == referral_id:
                return False

        new_referral = {
            'referrer_id': referrer_id,
            'referral_id': referral_id
        }
        self.data['referrals'].append(new_referral)
        self.save_data()
        return True

    def get_user_by_referral_code(self, referral_code):
        for user in self.data['users']:
            if user['referral_code'] == referral_code:
                return user
        return None

    def update_nickname(self, user_id, nickname):
        user = self.get_user(user_id)
        if user:
            user['username'] = nickname
            self.save_data()

    def update_language(self, user_id, language):
        user = self.get_user(user_id)
        if user:
            user['language'] = language
            self.save_data()

    def generate_referral_code(self):
        import uuid
        return str(uuid.uuid4())[:8]

# Пример использования (в app.py):
# db = Database("scream_tap_bot.json")
# user = db.get_user(123)
