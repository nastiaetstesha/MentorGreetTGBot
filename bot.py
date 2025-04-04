import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from api_client import (
    fetch_mentors,
    fetch_postcards,
    APIConnectionError,
    set_api_base_url,
)
from utils import (
    start,
    show_mentors,
    process_user_message,
    confirm_card_selection,
    cancel_card_selection,
)


def main():
    load_dotenv()

    token = os.getenv("TG_TOKEN")
    api_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8080")
    set_api_base_url(api_url)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    try:
        mentors = fetch_mentors()
        postcards = fetch_postcards()

        dp.bot_data["mentors"] = mentors
        dp.bot_data["cards"] = postcards
    except APIConnectionError:
        logger.error("Ошибка при получении данных с сервера 001")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text("📜 Список менторов"),
                                  show_mentors))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                  process_user_message))
    dp.add_handler(CallbackQueryHandler(confirm_card_selection,
                                        pattern="confirm_card"))
    dp.add_handler(CallbackQueryHandler(cancel_card_selection,
                                        pattern="cancel_card"))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
