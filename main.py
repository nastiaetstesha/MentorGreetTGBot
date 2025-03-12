import logging
import os
import requests

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from utils import load_json, start, show_mentors, fetch_data, process_user_message


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("TG_TOKEN")
    bot = Bot(token=token)
    '''   
    MENTORS_FILE = "mentors.json"
    POSTCARDS_FILE = "postcards.json"
    
    mentors = load_json(MENTORS_FILE)
    postcards = load_json(POSTCARDS_FILE)
    '''
    logging.basicConfig(level=logging.INFO)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    mentors = fetch_data("mentors")
    postcards = fetch_data("postcards")

    dp.bot_data["mentors"] = mentors
    dp.bot_data["cards"] = postcards


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text("📜 Список менторов"), show_mentors))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_user_message))
    
    updater.start_polling()
    updater.idle()
