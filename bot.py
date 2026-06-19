from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = "8910320426:AAGFpBuSkVh4UyB1ZABhGUhhk-NyEYtHJC4"

FILE = "ordini.txt"

def salva_ordine(testo):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(testo + "\n")

def leggi_ordini():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return f.readlines()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Bot negozio online pronto!")

async def ordine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = " ".join(context.args)

    if testo:
        salva_ordine(testo)
        await update.message.reply_text(f"Ordine ricevuto 👍: {testo}")
    else:
        await update.message.reply_text("Scrivi un prodotto dopo /ordine")

async def ordini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = leggi_ordini()

    if not dati:
        await update.message.reply_text("Nessun ordine")
    else:
        await update.message.reply_text("📦 Ordini:\n" + "".join(dati))

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ordine", ordine))
    app.add_handler(CommandHandler("ordini", ordini))

    print("Bot online...")

    app.run_polling()

if __name__ == "__main__":
    main()