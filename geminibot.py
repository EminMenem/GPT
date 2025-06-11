import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Birbaşa daxil edilmiş API açarları
TELEGRAM_BOT_TOKEN = "7641401806:AAEiRUN5ZmUtJ2RXuFvXPDJg00uvlGoRWNA"
GOOGLE_API_KEY = "AIzaSyDfMJbYZTVXB8AbENSGEnch8uQZw0EOuvg"

# Gemini API açarını konfiqurasiya et
genai.configure(api_key=GOOGLE_API_KEY)

# Model obyektini yarat
model = genai.GenerativeModel("gemini-1.5-flash")

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Mən Gemini ilə işləyən bir Telegram botuyam. Mənə sual ver!")

# İstifadəçi mesajlarına cavab
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Gemini xətası: {e}")
        await update.message.reply_text("Üzr istəyirəm, cavab alarkən xəta baş verdi.")

# Botun əsas funksiyası
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot başladıldı...")
    app.run_polling()

if __name__ == "__main__":
    main()
