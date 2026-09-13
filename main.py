
import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler
import requests

TOKEN = os.getenv("TOKEN")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot online!"

def get_jogos():
    # aqui fica sua logica de jogos
    return "Carregando jogos de hoje..."

async def start(update, context):
    await update.message.reply_text("Bot online! Use /jogos")

async def jogos(update, context):
    jogos_text = get_jogos()
    await update.message.reply_text(jogos_text)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jogos", jogos))
    application.run_polling()

if __name__ == "__main__":
    # roda o bot em segundo plano
    threading.Thread(target=run_bot, daemon=True).start()
    # roda o flask na porta do Render
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
