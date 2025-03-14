import json
import os
import requests

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext

import jsonschema
from jsonschema import validate

# API_BASE_URL = "https://my-json-server.typicode.com/devmanorg/congrats-mentor"
API_BASE_URL = "http://127.0.0.1:8080"


# Самописное исключение ServerError
class ServerError(Exception):
    """Ошибка сервера при получении и валидации данных API"""
    pass


mentors_schema = {
    "type": "object",
    "properties": {
        "mentors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {
                        "type": "object",
                        "properties": {
                            "first": {"type": "string"},
                            "second": {"type": "string"}
                        },
                        "required": ["first", "second"]
                    },
                    "tg_username": {"type": "string"},
                    "tg_chat_id": {"type": "integer"},
                    "bday": {"type": "string", "format": "date"}
                },
                "required": ["id", "name", "tg_username", "tg_chat_id"]
            }
        }
    },
    "required": ["mentors"]
}

postcards_schema = {
    "type": "object",
    "properties": {
        "postcards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "holidayId": {"type": "string"},
                    "name_ru": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["id", "holidayId", "name_ru", "body"]
            }
        }
    },
    "required": ["postcards"]
}


def check_role(update: Update, context: CallbackContext):
    """Определяет роль пользователя."""
    user = update.message.from_user
    selected_role = update.message.text
    mentors = context.bot_data.get("mentors", [])

    if selected_role == "Я Ментор":
        # Проверяем, есть ли этот пользователь в списке менторов
        for mentor in mentors:
            if mentor.get("tg_username") == f"@{user.username}":
                context.user_data["role"] = "mentor"
                update.message.reply_text("Вы ментор. Теперь вы можете получать поздравления!", 
                                          reply_markup=ReplyKeyboardRemove())
                return

        # Если никнейм не найден среди менторов
        update.message.reply_text("Вы не зарегистрированы как ментор.", reply_markup=ReplyKeyboardRemove())
        return

    elif selected_role == "Я Ученик":
        context.user_data["role"] = "student"
        show_mentors(update, context)


def validate_json(response_json, schema):
    try:
        validate(instance=response_json, schema=schema)
        print("JSON соответствует схеме API")
    except jsonschema.exceptions.ValidationError as e:
        raise ServerError("Ошибка валидации ответа от сервера") from e


def fetch_and_validate(endpoint, schema, update: Update = None, context: CallbackContext = None):
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise ServerError(f"Ошибка сервера: статус {response.status_code}")
        
        response_json = response.json()
        validate_json(response_json, schema)
        
        return response_json

    except ServerError as e:
        print(f"Ошибка сервера: {e}")
        if update and context:
            handle_server_error(update, context)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        if update and context:
            handle_server_error(update, context)
        return None
    except json.JSONDecodeError:
        print("Ошибка парсинга JSON")
        if update and context:
            handle_server_error(update, context)
        return None


def handle_server_error(update: Update, context: CallbackContext):
    update.message.reply_text("🚨 Произошла ошибка на сервере. Попробуйте позже.")


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
    return words[1] + " " + words[-1] + "..." if len(words) > 2 else name


def get_cards_keyboard(cards):
    keyboard = [[card["name_ru"]] for card in cards]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start(update: Update, context: CallbackContext):
    keyboard = [["Я Ментор"], ["Я Ученик"]]
    update.message.reply_text(
        "Привет! Выберите вашу роль:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )


def show_mentors(update: Update, context: CallbackContext):
    mentors = fetch_data("mentors") # ["mentors"]

    if not isinstance(mentors, list) or not all(isinstance(m, dict) for m in mentors) or isinstance(mentors, list) and not mentors[0]:
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


def process_user_message(update: Update, context: CallbackContext):    
    # Если роль еще не выбрана, вызываем check_role
    if "role" not in context.user_data:
        check_role(update, context)
        return

    # Если роль — "mentor", значит, он не должен выбирать открытки
    if context.user_data.get("role") == "mentor":
        update.message.reply_text("Вы ментор и принимаете открытки, а не выбираете их.")
        return

    # Если состояние — выбор открытки, запускаем select_card
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

        # После выбора ментора переключаем состояние на "выбор открытки"
        context.user_data["state"] = "choosing_card"

    else:
        update.message.reply_text("Выбери ментора из списка.")


def select_card(update: Update, context: CallbackContext):
    
    # Если состояние не "выбор открытки", значит, что-то пошло не так → возвращаем в select_mentor
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

        # Сбрасываем состояние, так как выбор завершён
        context.user_data.pop("selected_mentor", None)
        context.user_data.pop("state", None)
    else:
        update.message.reply_text("Выбери открытку из списка.")


