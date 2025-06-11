import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Yüklə .env faylını
load_dotenv()

# API açarlarını götür
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini API açarını konfiqurasiya et
genai.configure(api_key=GOOGLE_API_KEY)

# Model obyektini yarat
model = genai.GenerativeModel("gemini-1.5-flash")

# Start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Mən Gemini ilə işləyən bir Telegram botuyam. Mənə sual ver!")

# Mesajlara cavab
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Gemini xətası: {e}")
        await update.message.reply_text("Üzr istəyirəm, cavab alarkən xəta baş verdi.")

# Botu işə sal
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot başladıldı...")
    app.run_polling()

if __name__ == "__main__":
    main()
