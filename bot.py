from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os
from datetime import datetime

TOKEN = "8910320426:AAGFpBuSkVh4UyB1ZABhGUhhk-NyEYtHJC4"

FILE = "ordini.txt"
SHOP_NAME = "Bot Negozio"

# stato temporaneo utenti (per prendere input ordine)
user_state = {}

def salva_ordine(user, testo):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {user} | {testo}\n")

def leggi_ordini():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return f.readlines()

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Fai ordine", callback_data="ordine")],
        [InlineKeyboardButton("📦 Vedi ordini", callback_data="ordini")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Benvenuto in {SHOP_NAME} 🤖\nScegli cosa fare:",
        reply_markup=menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = query.from_user.username or "utente"

    if query.data == "ordine":
        user_state[user_id] = "ordine"
        await query.message.reply_text("✍️ Scrivi ora il tuo ordine (es: pizza margherita)")
    
    elif query.data == "ordini":
        dati = leggi_ordini()
        testo = "📦 Ordini:\n" + "".join(dati) if dati else "Nessun ordine"
        await query.message.reply_text(testo)
    
    elif query.data == "info":
        await query.message.reply_text(
            f"ℹ️ {SHOP_NAME}\nSistema ordini automatico per negozi"
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = update.message.from_user.username or "utente"
    testo = update.message.text

    if user_id in user_state and user_state[user_id] == "ordine":
        salva_ordine(user, testo)
        await update.message.reply_text(f"✅ Ordine ricevuto: {testo}")
        user_state[user_id] = None
    else:
        await update.message.reply_text("👉 Usa /start per aprire il menu")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
