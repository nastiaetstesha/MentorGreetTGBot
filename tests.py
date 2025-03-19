import json
import os
import requests

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext



# API_BASE_URL = "https://my-json-server.typicode.com/devmanorg/congrats-mentor"
# https://my-json-server.typicode.com/devmanorg/congrats-mentor/mentors
API_BASE_URL = "http://127.0.0.1:8080"


def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            return data
    return []


def process_user_message(update: Update, context: CallbackContext):
    """Определяет, какую функцию запустить в зависимости от состояния диалога."""
    
    # Если в контексте есть состояние "выбор открытки", передаём сообщение в select_card
    if context.user_data.get("state") == "choosing_card":
        select_card(update, context)
    else:
        select_mentor(update, context)


def select_mentor(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])
    selected_text = update.message.text

    selected_mentor = None
    name_counts = {}
    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_counts[full_name] = name_counts.get(full_name, 0) + 1

    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_part = shorten_name(full_name)
        if name_counts[full_name] == 1:
            display_name = name_part
        else:
            display_name = f"{name_part} ({mentor['tg_username']})"

        if selected_text == display_name:
            selected_mentor = mentor
            break

    if selected_mentor:
        context.user_data["selected_mentor"] = get_mentor_full_name(selected_mentor)
        cards = fetch_data("postcards")
        context.bot_data["cards"] = cards

        update.message.reply_text(
            f"Ты выбрал {get_mentor_full_name(selected_mentor)}. Теперь выбери открытку:",
            reply_markup=get_cards_keyboard(cards)
        )

        # ✅ После выбора ментора переключаем состояние на "выбор открытки"
        context.user_data["state"] = "choosing_card"

    else:
        update.message.reply_text("Выбери ментора из списка.")


def select_card(update: Update, context: CallbackContext):
    """Обрабатывает выбор открытки"""
    
    # ✅ Если состояние не "выбор открытки", значит, что-то пошло не так → возвращаем в select_mentor
    if context.user_data.get("state") != "choosing_card":
        select_mentor(update, context)
        return

    cards = context.bot_data.get("cards", [])
    selected_mentor = context.user_data.get("selected_mentor")
    selected_text = update.message.text

    selected_card = next((c for c in cards if c["name_ru"] == selected_text), None)

    if selected_card:
        body = selected_card["body"].replace("#name", selected_mentor)
        update.message.reply_text(
            f"Ты выбрал открытку '{selected_card['name_ru']}' для {selected_mentor}!\n\n{body}",
            reply_markup=ReplyKeyboardRemove()
        )

        # ✅ Сбрасываем состояние, так как выбор завершён
        context.user_data.pop("selected_mentor", None)
        context.user_data.pop("state", None)
    else:
        update.message.reply_text("Выбери открытку из списка.")

a = fetch_data("mentors")

for m in a:
    print(m.split())
# print(fetch_data("postcards"))