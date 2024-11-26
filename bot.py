
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"سلام {update.effective_user.first_name}! این ربات Railway هست.")

if __name__ == "__main__":
    # توکن ربات تلگرام
    TOKEN = "8187523450:AAGE1Ard4no0HPZdBdl6kitl41vld-I62PM"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("ربات شروع به کار کرد...")
    app.run_polling()
def get_chat_id(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Chat ID شما: {chat_id}")

dp.add_handler(CommandHandler("chatid", get_chat_id))
