import nest_asyncio
nest_asyncio.apply()

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

# تنظیمات تلگرام
TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"
CHAT_ID = 6471494609
bot = Bot(token=TOKEN)

# دستورات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"سلام {update.effective_user.first_name}! این ربات Railway هست.")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Chat ID شما: {chat_id}")

app_telegram = ApplicationBuilder().token(TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("chatid", get_chat_id))

# اعلان‌ها (Webhook)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message", "پیامی ارسال نشده است.")
    bot.send_message(chat_id=CHAT_ID, text=message)
    return "پیام ارسال شد!", 200

if __name__ == '__main__':
    # اجرای Flask و ربات تلگرام به صورت جداگانه
    from threading import Thread
    import asyncio

    def run_flask():
        app.run(host="0.0.0.0", port=5000)

    def run_telegram():
        asyncio.run(app_telegram.run_polling())

    Thread(target=run_flask).start()
    Thread(target=run_telegram).start()
