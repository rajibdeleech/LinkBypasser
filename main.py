import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your actual bot token
BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_command(text):
    parts = text.split()
    shadowlink = parts[1] if len(parts) > 1 else None
    title, thumb = "", ""

    if "-n" in parts:
        idx = parts.index("-n") + 1
        if idx < len(parts): title = parts[idx]

    if "-t" in parts:
        idx = parts.index("-t") + 1
        if idx < len(parts): thumb = parts[idx]

    return shadowlink, title, thumb

async def yl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        shadowlink, title, thumb = parse_command(text)

        if not shadowlink or not shadowlink.startswith("http"):
            await update.message.reply_text("Invalid Shadowlink URL.")
            return

        # Call Shadowlink API
        res = requests.get(shadowlink)
        if res.status_code != 200 or "url" not in res.json():
            await update.message.reply_text("Failed to fetch link.")
            return

        mkv_link = res.json()["url"]
        if not mkv_link.endswith(".mkv"):
            mkv_link += ".mkv"  # Optional: force mkv if needed

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶ Download MKV", url=mkv_link)],
            [InlineKeyboardButton("⬆ Leech/Upload", url=mkv_link)]
        ])

        if thumb:
            await update.message.reply_photo(
                photo=thumb,
                caption=f"**{title or 'Download Ready!'}**",
                reply_markup=buttons,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"**{title or 'Download Ready!'}**\n{mkv_link}",
                reply_markup=buttons,
                parse_mode="Markdown"
            )

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error processing request.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("yl", yl))
    app.run_polling()
