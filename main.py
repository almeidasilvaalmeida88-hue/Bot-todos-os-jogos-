import os, asyncio, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
threading.Thread(target=run_flask, daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN")

def get_todos_jogos():
    try:
        r = requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard", timeout=15).json()
        jogos=[]
        for ev in r.get('events',[])[:20]:
            try:
                comp=ev['competitions'][0]
                h=comp['competitors'][0]; a=comp['competitors'][1]
                if h['homeAway']!='home': h,a=a,h
                liga=ev['leagues'][0]['name'] if ev.get('leagues') else "Jogo"
                jogos.append(f"{liga}: {h['team']['displayName']} x {a['team']['displayName']}")
            except: continue
        return "\n".join(jogos) if jogos else "Nenhum jogo agora."
    except Exception as e: return f"Erro: {e}"

async def start(update, context): await update.message.reply_text("Bot ON! Use /jogos")
async def jogos_cmd(update, context): await update.message.reply_text(get_todos_jogos())

async def main_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jogos", jogos_cmd))
    print("Bot rodando...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main_bot())
