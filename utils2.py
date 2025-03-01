import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext


def get_unique_mentor_display(mentors):
    name_counts = {}
    for mentor in mentors:
        name_counts[mentor["name"]] = name_counts.get(mentor["name"], 0) + 1
    
    keyboard = []
    for mentor in mentors:
        display_name = mentor["name"] if name_counts[mentor["name"]] == 1 else f"{mentor['name']} ({mentor['tgid']})"
        keyboard.append([display_name])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def show_mentors2(update: Update, context: CallbackContext):
    mentors = context.bot_data.get("mentors", [])
    if not mentors:
        update.message.reply_text("Список менторов пуст. Пожалуйста, загрузите данные.")
    else:
        update.message.reply_text("Выбери ментора из списка:", reply_markup=get_unique_mentor_display(mentors))

