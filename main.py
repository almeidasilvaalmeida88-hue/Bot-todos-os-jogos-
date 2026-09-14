import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot no ar!"

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Bot-todos-os-jogos ON!\nUse /palpite para Bahia x Remo hoje 20h")

async def palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """⚽ *BAHIA x REMO - HOJE 20H*

🏆 Brasileirão - Fonte Nova
Bahia 5º (43pts) x Remo 19º (23pts)

🔥 CONTEXTO:
Bahia 3 vitórias seguidas, 10 jogos invicto
Remo 8 jogos sem vencer, pior ataque
⚠️ Em 2026: 3 jogos, 3 vitórias do Remo - revanche!

✅ PRINCIPAL: Bahia vence @1.39
💎 VALOR: Bahia + Over 1.5 @1.85
🔮 Placar: 2-0 Bahia

Jogo pra pressão alta do Ceni!"""
    await update.message.reply_text(msg, parse_mode='Markdown')

def run_bot():
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("palpite", palpite))
    bot.run_polling(drop_pending_updates=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
