import json
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_mentors_keyboard(mentors):
    keyboard = [[mentor["name"]] for mentor in mentors]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    keyboard = [["📜 Список менторов"]]
    update.message.reply_text("Привет! Нажми кнопку, чтобы увидеть список менторов.",
                              reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


def show_mentors(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])  # Используем bot_data
    if not mentors:
        update.message.reply_text("Список менторов пуст. Пожалуйста, загрузите данные.")
    else:
        update.message.reply_text("Выбери ментора из списка:", reply_markup=get_mentors_keyboard(mentors))


def select_mentor(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])  # Используем bot_data
    if update.message.text in [m["name"] for m in mentors]:
        update.message.reply_text(f"Ты выбрал {update.message.text}. Теперь можешь отправить ему открытку (функция в разработке).")
    else:
        update.message.reply_text("Выбери ментора из списка.")