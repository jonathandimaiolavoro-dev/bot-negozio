from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
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

# MENU PRINCIPALE
def menu():
    keyboard = [
        [InlineKeyboardButton("🛒 Fai ordine", callback_data="ordine")],
        [InlineKeyboardButton("📦 Vedi ordini", callback_data="ordini")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Benvenuto in {SHOP_NAME} 🤖\nScegli un'opzione:",
        reply_markup=menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user.username or "utente"

    if query.data == "ordine":
        salva_ordine(user, "ordine generico")
        await query.edit_message_text("🛒 Ordine registrato!")
    
    elif query.data == "ordini":
        dati = leggi_ordini()
        testo = "📦 Ordini:\n" + "".join(dati) if dati else "Nessun ordine"
        await query.edit_message_text(testo)
    
    elif query.data == "info":
        await query.edit_message_text(
            f"ℹ️ {SHOP_NAME}\nBot per gestione ordini automatica"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
