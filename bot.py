from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from datetime import datetime

TOKEN = "8910320426:AAGFpBuSkVh4UyB1ZABhGUhhk-NyEYtHJC4"

FILE = "ordini.txt"
SHOP_NAME = "Bot Negozio"

def salva_ordine(user, testo):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {user} | {testo}\n")

def leggi_ordini():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return f.readlines()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🛒 Benvenuto in {SHOP_NAME}\n\n"
        "Comandi disponibili:\n"
        "/ordine prodotto\n"
        "/ordini\n"
        "/info"
    )

async def ordine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or "utente"
    testo = " ".join(context.args)

    if testo:
        salva_ordine(user, testo)
        await update.message.reply_text(
            f"✅ Ordine ricevuto!\nProdotto: {testo}"
        )
    else:
        await update.message.reply_text("⚠️ Scrivi un prodotto dopo /ordine")

async def ordini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = leggi_ordini()

    if not dati:
        await update.message.reply_text("📭 Nessun ordine ancora")
    else:
        await update.message.reply_text("📦 Ordini:\n" + "".join(dati))

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"ℹ️ {SHOP_NAME}\n"
        "Sistema ordini automatico Telegram\n"
        "Risposte rapide + gestione clienti"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ordine", ordine))
    app.add_handler(CommandHandler("ordini", ordini))
    app.add_handler(CommandHandler("info", info))

    app.run_polling()

if __name__ == "__main__":
    main()
