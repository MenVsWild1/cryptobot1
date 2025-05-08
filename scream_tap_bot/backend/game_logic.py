 
import random
import time

def calculate_click_reward(clicks):
    """Вычисляет награду за клик, включая комбо и критические клики."""
    reward = 1
    if clicks % 10 == 0:
        reward += 5  # Комбо
    if random.randint(1, 50) == 1:
        reward += 50  # Критический клик
    return reward

def apply_boost(boost_type, balance):
    """Применяет буст или анти-буст."""
    if boost_type == "грустный_шиба":
        return max(1, int(balance * 0.5))  # -50% баланса, минимум 1
    elif boost_type == "кричащий_сатоши":
        return 2  # Множитель x2
    elif boost_type == "призрак_луна":
        return 1.5 # 50% автокликер бонус
    return 1  # Нет буста

def handle_level_up(user_id, new_level, db):
    """Обрабатывает повышение уровня и выдает награды (NFT, бусты, роли)."""
    rewards = {
        'nft': f"NFT Level {new_level}",  # Заглушка
        'boost': '2x на 10 секунд',  # Заглушка
        'role': f"Degenerate Level {new_level}",  # Заглушка
        'coins': new_level * 50 # Пример награды в коинах
    }

    # You can add more complex logic here, such as saving the NFT to the user's profile.
    db.update_balance(user_id, rewards['coins']) # give the coins
    return rewards

def generate_referral_code():
    """Генерирует случайный реферальный код."""
    import uuid
    return str(uuid.uuid4())[:8]

