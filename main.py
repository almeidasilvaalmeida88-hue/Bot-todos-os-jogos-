
import os, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "ok"
TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("⚽ Analise ao vivo luz ON! Use /palpite")

async def palpite(update, context):
    await update.message.reply_text("Palpite teste OK! Agora vou colocar a ESPN de novo")

def run_bot():
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("palpite", palpite))
    bot.run_polling(drop_pending_updates=True)

threading.Thread(target=run_bot,daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
