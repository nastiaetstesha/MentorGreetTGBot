import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import CallbackContext
from api_client import (
    fetch_mentors,
    APIConnectionError,
    APIHTTPError,
    APIParsingError,
    APIValidationError,
    APIClientError
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_server_error(update: Update, context: CallbackContext):
    """Сообщает пользователю об ошибке на сервере."""
    update.message.reply_text("🚨 Произошла ошибка на сервере. Попробуйте позже.")


def handle_role_selection(update: Update, context: CallbackContext):
    """Определяет роль пользователя после выбора кнопки 'Я Ментор' или 'Я Ученик'."""
    user = update.message.from_user
    selected_role = update.message.text

    try:
        mentors = context.bot_data.get("mentors", [])
        
        if selected_role == "Я Ментор":
            for mentor in mentors:
                if mentor.get("tg_username") == f"@{user.username}":
                    context.user_data["role"] = "mentor"
                    update.message.reply_text("Вы ментор. Теперь вы можете получать поздравления!", 
                                              reply_markup=ReplyKeyboardRemove())
                    return

            update.message.reply_text("Вы не зарегистрированы как ментор.",
                                      reply_markup=ReplyKeyboardRemove())
            return

        elif selected_role == "Я Ученик":
            context.user_data["role"] = "student"
            show_mentors(update, context)

    except Exception as e:
        logger.error(f"Ошибка при проверке роли: {e}")
        handle_server_error(update, context)


def start(update: Update, context: CallbackContext):
    """Стартовый диалог с выбором роли."""
    context.user_data.pop("role", None)
    keyboard = [["Я Ментор"], ["Я Ученик"]]
    update.message.reply_text(
        "Привет! Выберите вашу роль:",
        reply_markup=ReplyKeyboardMarkup(keyboard,
                                         resize_keyboard=True,
                                         one_time_keyboard=True)
    )


def show_mentors(update: Update, context: CallbackContext):
    """Отправляет пользователю список менторов."""
    try:
        mentors = fetch_mentors()
        context.bot_data["mentors"] = mentors

        if not mentors:
            update.message.reply_text("Список менторов пуст. Попробуйте позже.")
        else:
            update.message.reply_text("Выбери ментора из списка:",
                                      reply_markup=get_unique_mentor_display(mentors))
    
    except APIValidationError:
        handle_server_error(update, context)
    except (APIConnectionError, APIHTTPError, APIParsingError, APIClientError):
        handle_server_error(update, context)


def get_unique_mentor_display(mentors):
    """Создаёт клавиатуру с именами менторов."""
    name_counts = {}
    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_counts[full_name] = name_counts.get(full_name, 0) + 1

    keyboard = []
    for mentor in mentors:
        full_name = get_mentor_full_name(mentor)
        name_part = shorten_name(full_name)
        display_name = name_part if name_counts[full_name] == 1 else f"{name_part} ({mentor['tg_username']})"
        keyboard.append([display_name])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                               one_time_keyboard=True)


def get_mentor_full_name(mentor):
    """Возвращает полное имя ментора."""
    return f'{mentor["name"]["first"]} {mentor["name"]["second"]}'


def shorten_name(name):
    """Сокращает имя для удобства отображения."""
    words = name.split()
    if len(words) > 2:
        return f"{words[1]} {words[-1]}..."
    return name


def process_user_message(update: Update, context: CallbackContext):
    """Определяет, какая функция должна быть вызвана после получения сообщения."""
    try:
        if "role" not in context.user_data:
            handle_role_selection(update, context)
            return

        if context.user_data.get("role") == "mentor":
            update.message.reply_text("Вы ментор и принимаете открытки, а не выбираете их.")
            return

        if context.user_data.get("state") == "choosing_card":
            select_card(update, context)
        else:
            select_mentor(update, context)

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        handle_server_error(update, context)


def get_cards_keyboard(cards):
    keyboard = []
    for card in cards:
        display = f"{card['name_ru']} #{card['id']}"
        keyboard.append([display])
    return ReplyKeyboardMarkup(keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=True)


def select_mentor(update: Update, context: CallbackContext):
    """Позволяет ученику выбрать ментора."""
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
        update.message.reply_text(f"Ты выбрал {get_mentor_full_name(selected_mentor)}.")
        context.user_data["state"] = "choosing_card"
        select_card(update, context)
    else:
        update.message.reply_text("Выбери ментора из списка.")


def confirm_card_selection(update: Update, context: CallbackContext):
    """Обрабатывает подтверждение открытки перед отправкой."""
    query = update.callback_query
    query.answer()

    selected_mentor = context.user_data.get("selected_mentor")
    selected_card = context.user_data.get("selected_card")

    if selected_card and selected_mentor:
        body = selected_card["body"].replace("#name", selected_mentor)
        query.message.reply_text(
            f"Ты отправил открытку '{selected_card['name_ru']}' для {selected_mentor}!\n\n{body}",
            reply_markup=ReplyKeyboardRemove()
        )

        context.user_data.pop("selected_mentor", None)
        context.user_data.pop("selected_card", None)
        context.user_data.pop("state", None)
    else:
        query.message.reply_text("Произошла ошибка. Попробуйте снова.")


def cancel_card_selection(update: Update, context: CallbackContext):
    """Отменяет выбор открытки и возвращает к списку открыток."""
    query = update.callback_query
    query.answer()

    query.message.reply_text("Выбери другую открытку:",
                             reply_markup=get_cards_keyboard(
                                 context.bot_data.get("cards", [])
                                 ))


def select_card(update: Update, context: CallbackContext):
    """Позволяет пользователю выбрать открытку, но перед отправкой показывает текст."""
    try:
        if context.user_data.get("state") != "choosing_card":
            select_mentor(update, context)
            return

        cards = context.bot_data.get("cards", [])

        if not cards:
            update.message.reply_text("Список открыток пуст. Попробуйте позже.",
                                      reply_markup=ReplyKeyboardRemove())
            context.user_data.pop("selected_mentor", None)
            context.user_data.pop("state", None)
            return

        selected_mentor = context.user_data.get("selected_mentor")
        selected_text = update.message.text.strip()

        selected_id = int(selected_text.split("#")[-1]) if "#" in selected_text else None

        selected_card = next((card for card in cards if card["id"] == selected_id), None)

        if selected_card:
            body = selected_card["body"].replace("#name", selected_mentor)
            context.user_data["selected_card"] = selected_card

            keyboard = [
                [InlineKeyboardButton(" Отправить", callback_data="confirm_card")],
                [InlineKeyboardButton(" Выбрать другую", callback_data="cancel_card")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                f"Ты выбрал открытку '{selected_card['name_ru']}'. Вот её текст:\n\n{body}\n\nОтправить её?",
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text("Выбери открытку из списка:",
                                      reply_markup=get_cards_keyboard(cards))

    except APIValidationError:
        handle_server_error(update, context)
    except (APIConnectionError, APIHTTPError, APIParsingError, APIClientError):
        handle_server_error(update, context)
