from flask import Flask
import threading, os, time, requests, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- TRUQUE PRA RENDER NÃO DAR ERRO DE PORTA ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online - Todos os Jogos!"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()
# -----------------------------------------------

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = set()

def get_todos_jogos():
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/misc/scoreboard"
        r = requests.get(url, timeout=10).json()
        jogos = []
        for ev in r.get('events', []):
            comp = ev['competitions'][0]
            home = comp['competitors'][0]
            away = comp['competitors'][1]
            # inverte se home não for casa
            if home['homeAway']!= 'home':
                home, away = away, home
            status = comp['status']['type']['description']
            liga = ev['leagues'][0]['name'] if 'leagues' in ev else ev.get('league',{}).get('name','Jogo')
            txt = f"{liga}: {home['team']['displayName']} {home.get('score','')} x {away.get('score','')} {away['team']['displayName']} - {status}"
            jogos.append(txt)
        return "\n".join(jogos) if jogos else "Nenhum jogo ao vivo agora."
    except Exception as e:
        return f"Erro ao buscar jogos: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.effective_chat.id)
    await update.message.reply_text("Bot ON! Vou mandar todos os jogos. Use /jogos")

async def jogos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_todos_jogos())

async def main_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jogos", jogos_cmd))
    print("Bot rodando...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main_bot())
