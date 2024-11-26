from flask import Flask, request
import requests

app = Flask(__name__)

API_TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"
CHAT_ID = "6471494609"

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    message = data.get("message", "پیامی از سمت ChatGPT دریافت شد")
    
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
