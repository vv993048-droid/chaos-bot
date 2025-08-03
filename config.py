# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env (если есть)
load_dotenv()

# === BOT_TOKEN ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN or not BOT_TOKEN.strip():
    raise ValueError("❌ Не задан BOT_TOKEN в переменных окружения. Убедись, что он добавлен в Render Environment.")
BOT_TOKEN = BOT_TOKEN.strip()

# === GROUP_CHAT_ID ===
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if not GROUP_CHAT_ID or not GROUP_CHAT_ID.strip():
    raise ValueError("❌ Не задан GROUP_CHAT_ID в переменных окружения. Добавь его в Render (например: -1001234567890).")
GROUP_CHAT_ID = GROUP_CHAT_ID.strip()

# Попробуем преобразовать в int
try:
    GROUP_CHAT_ID = int(GROUP_CHAT_ID)
except ValueError:
    raise ValueError(
        f"❌ GROUP_CHAT_ID не является числом: '{GROUP_CHAT_ID}'\n"
        "Он должен быть целым числом, например: -1001234567890\n"
        "Проверь, что в Render Environment нет кавычек, пробелов или опечаток."
    )

# === OPENAI_API_KEY ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
    raise ValueError("❌ Не задан OPENAI_API_KEY в переменных окружения. Получи его на: https://platform.openai.com/api-keys")
OPENAI_API_KEY = OPENAI_API_KEY.strip()

# ✅ Все переменные загружены
print("✅ config.py: Все переменные окружения загружены успешно.")