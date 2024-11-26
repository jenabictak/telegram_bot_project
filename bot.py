import asyncio
from flask import Flask, request
from threading import Thread
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تنظیمات تلگرام
TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"
CHAT_ID = 6471494609

# ایجاد Flask اپلیکیشن
app = Flask(__name__)

# ایجاد ربات تلگرام
bot = Bot(token=TOKEN)
app_telegram = ApplicationBuilder().token(TOKEN).build()

# دستورات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"سلام {update.effective_user.first_name}! این ربات Railway هست.")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Chat ID شما: {chat_id}")

# افزودن دستورها به اپلیکیشن تلگرام
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("chatid", get_chat_id))

# مسیر ارسال پیام از طریق Flask
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message", "پیامی ارسال نشده است.")
    bot.send_message(chat_id=CHAT_ID, text=message)
    return "پیام ارسال شد!", 200

# اجرای Flask و ربات تلگرام
def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def run_telegram():
    await app_telegram.run_polling()

if __name__ == '__main__':
    # اجرای Flask در یک ترد جداگانه
    Thread(target=run_flask).start()

    # اجرای اپلیکیشن تلگرام در حلقه اصلی asyncio
    asyncio.run(run_telegram())
