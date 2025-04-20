import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"

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
        original_url = video_data.get("data", {}).get("download")

        if not original_url:
            await update.message.reply_text("Failed to get download link.")
            return

        # Force MKV format if available
        if not original_url.endswith(".mkv"):
            if ".mp4" in original_url:
                mkv_url = original_url.replace(".mp4", ".mkv")
            else:
                mkv_url = original_url + ".mkv"
        else:
            mkv_url = original_url

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Leech", url=mkv_url)],
            [InlineKeyboardButton("Copy Link", url=mkv_url)]
        ])

        await update.message.reply_photo(
            photo=thumb,
            caption=f"<b><a href='{mkv_url}'>{title}</a></b>",
            parse_mode="HTML",
            reply_markup=keyboard
        )

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Error parsing command or fetching download link.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yl", yl))
    print("Bot running...")
    app.run_polling()
