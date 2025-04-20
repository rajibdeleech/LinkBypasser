import logging
import requests
import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Dispatcher,
)

BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"
WEBHOOK_URL = "https://linkbypasser-pro.onrender.com"

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /yl <shadowlink> -n <title> -t <thumbnail>")

async def yl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        parts = text.split(" -n ")
        url = parts[0].replace("/yl ", "").strip()
        title_part = parts[1].split(" -t ")
        title = title_part[0].strip()
        thumb = title_part[1].strip()

        response = requests.get(url)
        video_data = response.json()
        download_url = video_data.get("data", {}).get("download")

        if not download_url:
            await update.message.reply_text("Failed to get download link.")
            return

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Leech", url=download_url)],
            [InlineKeyboardButton("Copy Link", url=download_url)]
        ])

        await update.message.reply_photo(
            photo=thumb,
            caption=f"<b><a href='{download_url}'>{title}</a></b>",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Error parsing command or fetching download link.")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is live!"

if __name__ == "__main__":
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("yl", yl))

    # Set dispatcher for incoming updates
    app.dispatcher = app_telegram.dispatcher

    # Set webhook
    bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
