def get_chat_id(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Chat ID شما: {chat_id}")
