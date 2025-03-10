from flask import Flask, request, jsonify
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

TOKEN = "8065946631:AAHXYAFUdyGCtUl6jIh_0cMV-RRVBU3ssO0"

# Initialize Firebase
cred = credentials.Certificate("xvisaibot-firebase-adminsdk-fbsvc-1d0c5f7d49")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text("Welcome! Type 'doctor' to book an appointment.")

def handle_message(update, context):
    text = update.message.text.lower()
    
    if "doctor" in text:
        update.message.reply_text("Do you want a chat or call consultation? Choose an option:\n1. Chat\n2. Call")

    elif "chat" in text:
        chat_id = str(uuid.uuid4())
        db.collection("chats").document(chat_id).set({"status": "open"})
        update.message.reply_text(f"Chat booked. Chat ID: {chat_id}")

    elif "call" in text:
        call_link = f"https://meet.jit.si/{uuid.uuid4().hex}"
        update.message.reply_text(f"Join your call here: {call_link}")

    else:
        update.message.reply_text("I didn't understand that.")

# Telegram Bot Setup
app_telegram = Application.builder().token(TOKEN).build()

app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(), bot)
    app_telegram.update_queue.put(update)
    return "OK"



if __name__ == "__main__":
    app.run(port=5000)
