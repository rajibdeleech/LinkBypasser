from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
import requests
import os

TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# /yl command handler
def yl(update, context):
    args = context.args
    if not args:
        update.message.reply_text("Usage: /yl <shadowlink> -n <title> -t <thumbnail>")
        return

    try:
        url = args[0]
        name = ""
        thumb = ""

        if "-n" in args:
            name = args[args.index("-n") + 1]
        if "-t" in args:
            thumb = args[args.index("-t") + 1]

        r = requests.get(url)
        real_url = r.url

        caption = f"📥 [{name}]({real_url})\n\n✅ Tap the button below to download or copy the link."

        keyboard = [
            [telegram.InlineKeyboardButton("⚡ Download Now", url=real_url)],
            [telegram.InlineKeyboardButton("📋 Copy Link", switch_inline_query=real_url)]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)

        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=thumb,
            caption=caption,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return 'Bot is running!'

# Setup dispatcher
from telegram.ext import CallbackContext
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("yl", yl))

# Set webhook on startup
@app.before_first_request
def init_webhook():
    webhook_url = f"https://linkbypasser.onrender.com/{TOKEN}"  # Make sure this matches your Render URL
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    app.run(port=10000)
