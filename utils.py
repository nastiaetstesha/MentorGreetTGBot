import json
import os
import requests

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext

# API_BASE_URL = "https://my-json-server.typicode.com/devmanorg/congrats-mentor"
API_BASE_URL = "http://127.0.0.1:8000"


def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if endpoint == "postcards":
            return data.get("postcards", [])
        if endpoint == "mentors":
            return data.get("mentors", [])
    return []


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_mentor_full_name(mentor):
    return f'{mentor["name"]["first"]} {mentor["name"]["second"]}'


def get_unique_mentor_display(mentors):
    name_counts = {}
    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_counts[full_name] = name_counts.get(full_name, 0) + 1

    keyboard = []
    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_part = shorten_name(full_name)
        if name_counts[full_name] == 1:
            display_name = name_part
        else:
            display_name = f"{name_part} ({mentor['tg_username']})"
        keyboard.append([display_name])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def shorten_name(name):
    words = name.split()
    return " ".join(words[:2]) + "..." if len(words) > 2 else name


def get_cards_keyboard(cards):
    keyboard = [[card["name_ru"]] for card in cards]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start(update: Update, context: CallbackContext):
    keyboard = [["📜 Список менторов"]]
    update.message.reply_text("Привет! Нажми кнопку, чтобы увидеть список менторов.",
                              reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True))


def show_mentors(update: Update, context: CallbackContext):
    mentors = fetch_data("mentors") # ["mentors"]

    if not isinstance(mentors, list) or not all(isinstance(m, dict) for m in mentors):
        update.message.reply_text("Ошибка загрузки данных. Попробуйте позже.")
        return

    if not mentors:
        update.message.reply_text("Список менторов пуст. Пожалуйста, попробуйте позже.")
    else:
        context.bot_data["mentors"] = mentors
        update.message.reply_text(
            "Выбери ментора из списка:",
            reply_markup=get_unique_mentor_display(mentors)
        )


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
    else:
        update.message.reply_text("Выбери ментора из списка.")


def select_card(update: Update, context: CallbackContext):
    if "selected_mentor" not in context.user_data:
        update.message.reply_text("Сначала выбери ментора.")
        return

    cards = context.bot_data.get("cards", [])
    selected_mentor = context.user_data["selected_mentor"]
    selected_text = update.message.text

    selected_card = next((c for c in cards if c["name_ru"] == selected_text), None)

    if selected_card:
        body = selected_card["body"].replace("#name", selected_mentor)
        update.message.reply_text(
            f"Ты выбрал открытку '{selected_card['name_ru']}' для {selected_mentor}!\n\n{body}",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.pop("selected_mentor", None)
    else:
        update.message.reply_text("Выбери открытку из списка.")




'''
def select_card(update: Update, context: CallbackContext):
    cards = context.bot_data.get("cards", [])
    selected_mentor = context.user_data.get("selected_mentor")

    if not selected_mentor:
        update.message.reply_text("Сначала выбери ментора.")
        return

    selected_text = update.message.text
    selected_card = next((c for c in cards if c["name_ru"] == selected_text), None)

    if selected_card:
        body = selected_card["body"].replace("#name", selected_mentor)
        update.message.reply_text(
            f"Ты выбрал открытку '{selected_card['name_ru']}' для {selected_mentor}!\n\n{body}",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.pop("selected_mentor", None)
    else:
        update.message.reply_text("Выбери открытку из списка.")
'''
