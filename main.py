import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "BOT LIVE - Bahia x Remo 20h"

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ON! Manda /palpite")

async def palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ *BAHIA x REMO - HOJE 20H*\n\n✅ PRINCIPAL: Bahia vence @1.39\n💎 VALOR: Bahia + Over 1.5 @1.85\n🔮 2-0 Bahia", parse_mode='Markdown')

def bot_thread():
    print("Iniciando bot Telegram...")
    Application.builder().token(TOKEN).build().add_handler(CommandHandler("start", start))
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("palpite", palpite))
    print("Bot rodando!")
    app_bot.run_polling(drop_pending_updates=True)

threading.Thread(target=bot_thread, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
