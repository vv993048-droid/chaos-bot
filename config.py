# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Не задан BOT_TOKEN в .env файле")

GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if not GROUP_CHAT_ID:
    raise ValueError("❌ Не задан GROUP_CHAT_ID в .env файле")
try:
    GROUP_CHAT_ID = int(GROUP_CHAT_ID)
except ValueError:
    raise ValueError("❌ GROUP_CHAT_ID должен быть числом (например: -1001234567890)")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не задан OPENAI_API_KEY в .env файле")