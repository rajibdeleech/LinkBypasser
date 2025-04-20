import os
import requests
from flask import Flask
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send /yl <shadowlink> -n <title> -t <thumbnail>")

@bot.message_handler(commands=['yl'])
def yl(message):
    try:
        text = message.text
        if "-n" in text and "-t" in text:
            parts = text.split("-n")
            link_part = parts[0].replace("/yl", "").strip()
            name_thumb = parts[1].split("-t")
            name = name_thumb[0].strip()
            thumb = name_thumb[1].strip()

            res = requests.get(link_part)
            json_data = res.json()

            video_url = json_data.get("url", "").replace("source", "preview") + ".mkv"

            caption = f"<b>{name}</b>\n\n<a href='{video_url}'>Download Link</a>"
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("Download", url=video_url),
                InlineKeyboardButton("Leech", url=f"https://t.me/yourleechbot?start={video_url}")
            )

            bot.send_photo(
                chat_id=message.chat.id,
                photo=thumb,
                caption=caption,
                parse_mode='HTML',
                reply_markup=markup
            )
        else:
            bot.reply_to(message, "Please use the correct format:\n/yl <shadowlink> -n <title> -t <thumbnail>")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
