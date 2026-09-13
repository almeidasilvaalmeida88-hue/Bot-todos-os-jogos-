import os, time, threading, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = set()

def get_todos_jogos():
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"
        r = requests.get(url, timeout=10).json()
        jogos = []
        for ev in r['events']:
            comp = ev['competitions'][0]
            home = comp['competitors'][0]
            away = comp['competitors'][1]
            status = comp['status']['type']['state']
            minuto = comp['status']['type']['shortDetail']
            liga = ev['league']['name']
            txt = f"{liga}: {home['team']['shortDisplayName']} {home.get('score','0')} x {away.get('score','0')} {away['team']['shortDisplayName']} - {minuto}"
            jogos.append({'id': ev['id'], 'texto': txt, 'status': status})
        return jogos
    except: return []

async def todos(update, context):
    jogos = get_todos_jogos()
    msg = "📋 TODOS OS JOGOS\n\n" + "\n".join([j['texto'] for j in jogos[:15]])
    await update.message.reply_text(msg)

async def auto(update, context):
    CHAT_IDS.add(update.effective_chat.id)
    await update.message.reply_text("✅ AUTO ATIVADO! Agora vou mandar gol de TODOS os jogos!")

async def parar(update, context):
    CHAT_IDS.discard(update.effective_chat.id)
    await update.message.reply_text("🛑 Parado")

def loop(app):
    ult = {}
    while True:
        time.sleep(60)
        try:
            for j in get_todos_jogos():
                if j['id'] in ult and ult[j['id']]!=j['texto'] and j['status']=='in':
                    for cid in list(CHAT_IDS):
                        try: app.bot.send_message(cid, f"⚽ GOL!\n{j['texto']}")
                        except: pass
                ult[j['id']] = j['texto']
        except: pass

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("todos", todos))
app.add_handler(CommandHandler("auto", auto))
app.add_handler(CommandHandler("parar", parar))
threading.Thread(target=loop, args=(app,), daemon=True).start()
app.run_polling()
