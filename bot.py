from flask import Flask, request
import logging
import telegram

# تنظیمات اصلی
TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"  # توکن ربات تلگرام خود را اینجا قرار دهید
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# فعال کردن لاگ‌ها
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot server is running!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # دریافت داده‌های وبهوک از تلگرام
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        logger.info(f"Received update: {update}")

        # پردازش پیام‌ها (به عنوان نمونه)
        if update.message:
            chat_id = update.message.chat_id
            text = update.message.text
            bot.send_message(chat_id=chat_id, text=f"Echo: {text}")

        return "Webhook received!", 200

    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    # پردازش پیام و ارسال پاسخ
    return jsonify({'status': 'success', 'message': 'پیام ارسال شد!'})
