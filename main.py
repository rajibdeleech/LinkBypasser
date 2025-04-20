from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"

def yl_handler(update: Update, context: CallbackContext):
    try:
        args = update.message.text.split()
        if "-n" not in args or "-t" not in args:
            update.message.reply_text("Missing -n or -t flags. Use:\n/yl <link> -n <title> -t <thumbnail>")
            return

        link_index = 1
        n_index = args.index("-n")
        t_index = args.index("-t")

        shadowlink = args[link_index]
        title = " ".join(args[n_index + 1:t_index])
        thumbnail = " ".join(args[t_index + 1:])

        # Call your deployed bypasser API
        bypass_url = f"https://linkbypasser-nwlt.onrender.com/bypass?url={shadowlink}"
        response = requests.get(bypass_url)
        final_link = response.text.strip()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Leech", url=final_link)],
            [InlineKeyboardButton("Download", url=final_link)]
        ])

        caption = f"<b>{title}</b>\n\n<a href='{final_link}'>Download Link</a>"

        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=thumbnail,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("yl", yl_handler))
    updater.start_polling()
    updater.idle()from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

BOT_TOKEN = "8115696441:AAHm-CyGqu628dTpxv2edBb_9YbRx8QtV0Y"

def yl_handler(update: Update, context: CallbackContext):
    try:
        args = update.message.text.split()
        if "-n" not in args or "-t" not in args:
            update.message.reply_text("Missing -n or -t flags. Use:\n/yl <link> -n <title> -t <thumbnail>")
            return

        link_index = 1
        n_index = args.index("-n")
        t_index = args.index("-t")

        shadowlink = args[link_index]
        title = " ".join(args[n_index + 1:t_index])
        thumbnail = " ".join(args[t_index + 1:])

        # Call your deployed bypasser API
        bypass_url = f"https://linkbypasser-nwlt.onrender.com/bypass?url={shadowlink}"
        response = requests.get(bypass_url)
        final_link = response.text.strip()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Leech", url=final_link)],
            [InlineKeyboardButton("Download", url=final_link)]
        ])

        caption = f"<b>{title}</b>\n\n<a href='{final_link}'>Download Link</a>"

        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=thumbnail,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("yl", yl_handler))
    updater.start_polling()
    updater.idle()
