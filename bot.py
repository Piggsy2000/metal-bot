from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = ""
ADMIN_ID =  


user_state = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🎸 Предложить группу", callback_data="band")],
        [InlineKeyboardButton("📢 Жалоба", callback_data="complaint")],
        [InlineKeyboardButton("🔗 Перейти к навигации", url="https://t.me/metalgrindcollection/10294")]
    ]
    if update.message:
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "band":
        user_state[user_id] = "waiting_for_band"
        await query.edit_message_text("Напишите название группы, которую хотите предложить:")
    elif query.data == "complaint":
        user_state[user_id] = "waiting_for_complaint"
        await query.edit_message_text("Опишите, на что хотите пожаловаться:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    text = update.message.text
    state = user_state.get(user_id)

    username = f"@{user.username}" if user.username else "без username"
    name = f"{user.first_name} {user.last_name or ''}".strip()

    if state == "waiting_for_band":
        await update.message.reply_text("Спасибо! Мы рассмотрим вашу группу.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🎸 Предложение группы:\n"
                 f"👤 От: {name} ({username})\n"
                 f"🆔 ID: {user_id}\n\n"
                 f"{text}"
        )
        user_state[user_id] = None

    elif state == "waiting_for_complaint":
        await update.message.reply_text("Спасибо за жалобу. Мы рассмотрим её.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📢 Жалоба:\n"
                 f"👤 От: {name} ({username})\n"
                 f"🆔 ID: {user_id}\n\n"
                 f"{text}"
        )
        user_state[user_id] = None

    else:
        await update.message.reply_text("Нажмите /start и выберите действие.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤘 Бот активен. Напиши /start в Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()
