import os, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "ok"

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Analise ao vivo luz ON!\nUse /palpite")

async def palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard",timeout=10).json()
        ev=r['events'][0]
        c=ev['competitions'][0]
        h=c['competitors'][0]
        a=c['competitors'][1]
        txt=f"⚽ {h['team']['displayName']} {h.get('score','0')}x{a.get('score','0')} {a['team']['displayName']} - AO VIVO\n\nTendência: time que perde se expõe, espaço pra transição."
        await update.message.reply_text(txt)
    except:
        await update.message.reply_text("Sem jogos ao vivo agora.")

def bot():
    b=Application.builder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("palpite", palpite))
    b.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    threading.Thread(target=bot,daemon=True).start()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
