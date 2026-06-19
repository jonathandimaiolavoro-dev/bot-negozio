from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os
from datetime import datetime

TOKEN = "8910320426:AAGFpBuSkVh4UyB1ZABhGUhhk-NyEYtHJC4"

FILE = "ordini.txt"

# stato utenti (multi-cliente vero)
user_state = {}

# ----------------- DATABASE SEMPLICE -----------------

def salva_ordine(user_id, username, testo):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {user_id} | {username} | {testo}\n")

def leggi_ordini():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return f.readlines()

# ----------------- MENU -----------------

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Nuovo ordine", callback_data="ordine")],
        [InlineKeyboardButton("📦 Ordini", callback_data="ordini")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")]
    ])

# ----------------- START -----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛍️ Benvenuto nel sistema ordini PRO\nScegli un'opzione:",
        reply_markup=menu()
    )

# ----------------- BOTTONI -----------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "ordine":
        user_state[user_id] = "ordine"
        await query.message.reply_text("✍️ Scrivi il tuo ordine (es: pizza margherita)")
    
    elif query.data == "ordini":
        dati = leggi_ordini()
        testo = "📦 ORDINI:\n" + "".join(dati) if dati else "Nessun ordine ancora"
        await query.message.reply_text(testo)
    
    elif query.data == "info":
        await query.message.reply_text(
            "ℹ️ Sistema ordini PRO\n"
            "✔ clienti separati\n"
            "✔ gestione automatica\n"
            "✔ pronto per negozi"
        )

# ----------------- MESSAGGI -----------------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "utente"
    testo = update.message.text

    if user_state.get(user_id) == "ordine":
        salva_ordine(user_id, username, testo)
        await update.message.reply_text(
            f"✅ Ordine salvato!\n📦 {testo}"
        )
        user_state[user_id] = None
    else:
        await update.message.reply_text("👉 Usa /start per aprire il menu")

# ----------------- MAIN -----------------

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
