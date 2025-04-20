import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"

logging.basicConfig(level=logging.INFO)

async def yl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        parts = text.split(" -n ")
        if len(parts) != 2:
            await update.message.reply_text("Invalid format. Use: /yl <url> -n <title> -t <thumbnail>")
            return

        shadowlink = parts[0].split(" ")[1]
        title_thumb = parts[1].split(" -t ")
        title = title_thumb[0]
        thumbnail = title_thumb[1]

        response = requests.get(shadowlink)
        if response.status_code != 200:
            await update.message.reply_text("Failed to fetch link.")
            return

        final_url = response.url
        if not final_url.endswith(".mkv"):
            final_url = final_url.split("?")[0] + ".mkv"

        keyboard = [
            [InlineKeyboardButton("Download Now", url=final_url)],
            [InlineKeyboardButton("Copy Link", switch_inline_query=final_url)],
            [InlineKeyboardButton("Leech", url=final_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(
            photo=thumbnail,
            caption=f"<b>{title}</b>\n\n<a href='{final_url}'>Download Link</a>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Something went wrong!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("yl", yl))
    app.run_polling()
