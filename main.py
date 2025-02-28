import logging
import os
from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from utils import load_json, start, show_mentors, select_mentor


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("TG_TOKEN")
    bot = Bot(token=token)
    MENTORS_FILE = "mentors.json"

    mentors = load_json(MENTORS_FILE)

    logging.basicConfig(level=logging.INFO)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Передача списка менторов в user_data
    dp.bot_data["mentors"] = mentors

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text("📜 Список менторов"), show_mentors))
    dp.add_handler(MessageHandler(Filters.text, select_mentor))

    updater.start_polling()
    updater.idle()