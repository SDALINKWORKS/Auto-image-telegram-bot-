import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import TOKEN, CHANNEL_USERNAME, PLAY_URL, OFFER_URL, SUPPORT_URL

logging.basicConfig(level=logging.INFO)

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")]
    ]

    text = (
        "Welcome 👋\n"
        "Get access to exclusive drops + winner alerts.\n\n"
        "Step 1/2: Join our channel to unlock."
    )

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# CHECK MEMBERSHIP
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:
            keyboard = [
                [InlineKeyboardButton("🎰 Play Now", url=PLAY_URL)],
                [InlineKeyboardButton("🎁 Today’s Offer", url=OFFER_URL)],
                [InlineKeyboardButton("💬 Support", url=SUPPORT_URL)]
            ]

            text = "Unlocked 🎉\n\nStep 2/2: Continue to the site."

            await query.answer()
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            raise Exception("Not joined")

    except:
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")]
        ]

        text = (
            "❌ Not subscribed yet.\n\n"
            "Join to unlock access:\n"
            "• Exclusive drops\n"
            "• Winner alerts\n"
            "• Daily opportunities"
        )

        await query.answer()
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# MAIN FUNCTION
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
