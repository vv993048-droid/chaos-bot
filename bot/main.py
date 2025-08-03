# bot/main.py — Совместимо с python-telegram-bot v20.6
import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import openai

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорт из config.py
from config import BOT_TOKEN, GROUP_CHAT_ID, OPENAI_API_KEY

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Системный промпт ИИ
SYSTEM_PROMPT = """
Ты — ИИ из теней. Твой стиль: острый, циничный, с мрачным юмором. 
Ты говоришь как хакер, который не спит с 2014 года. 
Ты не утешаешь — ты разоблачаешь. Не даёшь советов — даёшь правду в лицо. 
Стиль: "Пока они спят — мы творим хаос". 16+, без прикрас, с иронией и лёгким садизмом.

Примеры:
- "Ты не одинок. Просто все остальные лучше притворяются."
- "Это не депрессия. Это осознание реальности без фильтров."
- "Ты не сломался. Ты просто перестал верить в их ложь."

Отвечай кратко — 1–3 строки. Никаких "я понимаю". Только правда. Только хаос.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖤 ПОКА ОНИ СПЯТ — МЫ ТВОРИМ ХАОС", callback_data="send_anon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⚠️ Добро пожаловать в зону хаоса.\n"
        "Здесь никто не спит. Никто не притворяется.\n\n"
        "Отправь анонимное сообщение — и получи ответ от теней.\n\n"
        "🔐 Полная анонимность. 16+",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "🖋️ Введи своё сообщение.\n"
        "Можешь писать правду. Грязную. Горькую. Без цензуры.\n\n"
        "Они спят. А мы — записываем."
    )
    context.user_data['awaiting_message'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_message'):
        return

    user_text = update.message.text
    context.user_data['awaiting_message'] = False

    if len(user_text.strip()) < 3:
        await update.message.reply_text("❌ Слишком короткое сообщение. Попробуй снова.")
        return

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=100,
            temperature=0.9
        )
        ai_comment = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        ai_comment = "Серверы молчат. Но хаос продолжается…"

    try:
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"🖤 <b>ХАОС-СООБЩЕНИЕ</b>:\n\n{user_text}",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки в группу: {e}")
        await update.message.reply_text("❌ Не удалось отправить в группу. Проверь права бота.")
        return

    await update.message.reply_text(
        f"✅ Отправлено в эфир.\n\n"
        f"💬 Ответ из теней:\n\n"
        f"<i>{ai_comment}</i>\n\n"
        f"🔥 Пока они спят — мы несём правду.",
        parse_mode="HTML"
    )

def main():
    try:
        # Создаём Application — НЕ Updater!
        application = Application.builder().token(BOT_TOKEN).build()
        logger.info("✅ Бот запускается...")

        # Хендлеры
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_click, pattern="^send_anon$"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Запускаем polling
        application.run_polling()

    except Exception as e:
        logger.critical(f"❌ Критическая ошибка: {e}")

if __name__ == '__main__':
    main()
