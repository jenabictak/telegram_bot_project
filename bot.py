import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# توکن ربات تلگرام خود را اینجا وارد کنید
BOT_TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# تنظیمات لاگ
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET"])
def home():
    """صفحه اصلی برای تست سرور"""
    return "Bot server is running!"

@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        data = request.json
        chat_id = data.get("chat_id")
        text = data.get("text")

        if not chat_id or not text:
            return jsonify({"error": "chat_id and text are required"}), 400

        # ارسال پیام به تلگرام
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
        return jsonify(response.json()), response.status_code

    except Exception as e:
        logger.exception("خطا در ارسال پیام")
        return jsonify({"error": str(e)}), 500

@app.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    try:
        data = request.json
        logger.debug(f"داده دریافتی از تلگرام: {data}")

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            # پاسخ به پیام کاربر
            response_text = f"شما این پیام را ارسال کردید: {text}"
            requests.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json={"chat_id": chat_id, "text": response_text},
            )

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.exception("خطا در پردازش پیام تلگرام")
        return jsonify({"error": str(e)}), 500
        
@app.route("/notify", methods=["POST"])
def send_from_chatgpt():
    """دریافت پیام از ChatGPT و ارسال به تلگرام"""
    try:
        data = request.json
        chat_id = data.get("chat_id")
        text = data.get("text")

        if not chat_id or not text:
            return jsonify({"error": "chat_id and text are required"}), 400

        # ارسال پیام به تلگرام
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
        return jsonify(response.json()), response.status_code

@app.route("/send_from_chatgpt", methods=["POST"])
def send_from_chatgpt():
    """دریافت پیام از ChatGPT و ارسال به تلگرام"""
    try:
        data = request.json
        chat_id = data.get("chat_id")
        text = data.get("text")

        if not chat_id or not text:
            return jsonify({"error": "chat_id and text are required"}), 400

        # ارسال پیام به تلگرام
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
        return jsonify(response.json()), response.status_code

    except Exception as e:
        logger.exception("خطا در ارسال پیام از ChatGPT")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
