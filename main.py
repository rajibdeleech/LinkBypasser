import os
import requests
from flask import Flask
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Updater

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def start(update, context):
    update.message.reply_text("Send /yl <shadowlink> -n <title> -t <thumbnail_url>")

def yl(update, context):
    try:
        text = update.message.text
        parts = text.split()
        shadowlink = parts[1]
        name = text.split("-n", 1)[1].split("-t")[0].strip()
        thumb = text.split("-t", 1)[1].strip()

        # Request to Shadowlink API
        res = requests.get(shadowlink)
        json_data = res.json()

        # Extract and ensure it's an MKV link
        dl_url = json_data.get('url')
        if not dl_url.endswith(".mkv"):
            dl_url += ".mkv"

        caption = f"<b><a href='{dl_url}'>{name}</a></b>\n\nHigh-speed MKV download link ready!"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Leech", url=dl_url)],
            [InlineKeyboardButton("Copy Link", switch_inline_query=dl_url)]
        ])

        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=thumb,
            caption=caption,
            parse_mode='HTML',
            reply_markup=buttons
        )

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yl", yl))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    run_bot()
