import asyncio
import os
import signal
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# پیکربندی Flask
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

# ایجاد برنامه تلگرام
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

# اجرای همزمان Flask و Telegram
async def main():
    # اجرای Flask به صورت async
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5000"]

    flask_task = asyncio.create_task(serve(app, config))
    telegram_task = asyncio.create_task(app_telegram.run_polling())

    await asyncio.gather(flask_task, telegram_task)

if __name__ == '__main__':
    # حذف Signal Handling برای جلوگیری از خطای set_wakeup_fd
    if os.name != "nt":
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda: None)
            except NotImplementedError:
                pass

    asyncio.run(main())
