import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_FILE = os.getenv("DATABASE_FILE", "scream_tap_bot.json")  # JSON file path
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))
MARKET_CRASH_INTERVAL = int(os.getenv("MARKET_CRASH_INTERVAL", 10800))
AIRDROP_INTERVAL = int(os.getenv("AIRDROP_INTERVAL", 3600))
