import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def shorten_name(name):
    words = name.split()
    return " ".join(words[:2]) + "..." if len(words) > 2 else name


def get_mentors_keyboard(mentors):
    keyboard = [[shorten_name(mentor["name"])] for mentor in mentors]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_cards_keyboard(cards):
    keyboard = [[card["name"]] for card in cards]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start(update: Update, context: CallbackContext):
    keyboard = [["📜 Список менторов"]]
    update.message.reply_text("Привет! Нажми кнопку, чтобы увидеть список менторов.",
                              reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True))


def show_mentors(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])
    if not mentors:
        update.message.reply_text("Список менторов пуст. Пожалуйста, загрузите данные.")
    else:
        update.message.reply_text("Выбери ментора из списка:", reply_markup=get_mentors_keyboard(mentors))


def select_mentor(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])
    if update.message.text in [m["name"] for m in mentors]:
        context.user_data["selected_mentor"] = update.message.text
        update.message.reply_text(f"Ты выбрал {update.message.text}. Теперь выбери открытку:",
                                  reply_markup=get_cards_keyboard(context.bot_data.get("cards", [])))
    else:
        update.message.reply_text("Выбери ментора из списка.")


def select_card(update: Update, context: CallbackContext):
    cards = context.bot_data.get("cards", [])
    selected_mentor = context.user_data.get("selected_mentor")
    if update.message.text in [c["name"] for c in cards] and selected_mentor:
        selected_card = next(c for c in cards if c["name"] == update.message.text)
        update.message.reply_text(f"Ты выбрал открытку '{selected_card['name']}' для {selected_mentor}! {selected_card['body']}",
                                  reply_markup=ReplyKeyboardRemove())
        context.user_data.pop("selected_mentor", None)  # Удаляем данные о выбранном менторе
    else:
        update.message.reply_text("Выбери открытку из списка.")
