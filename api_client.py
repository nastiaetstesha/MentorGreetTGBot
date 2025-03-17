import requests
import logging
import jsonschema
from jsonschema import validate

# Базовый URL для API
API_BASE_URL = "http://127.0.0.1:8080"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


class ServerError(Exception):
    """Ошибка сервера при получении и валидации данных API"""
    pass


def fetch_data(endpoint):
    """
    Получает данные с сервера по `endpoint`.
    Возвращает JSON-ответ или выбрасывает исключение.
    """
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети при запросе {url}: {e}")
        raise ServerError(f"Ошибка соединения с сервером") from e
    except requests.exceptions.HTTPError as e:
        logger.error(f"Ошибка HTTP {response.status_code} при запросе {url}")
        raise ServerError(f"Ошибка на сервере: статус {response.status_code}") from e
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON при запросе {url}")
        raise ServerError("Некорректный JSON-ответ") from e


def fetch_mentors():
    """Запрашивает список менторов с сервера и валидирует данные."""
    try:
        data = fetch_data("mentors")
        validate_json(data, mentors_schema) 
        return data.get("mentors", [])
    except ServerError as e:
        logger.error(f"Ошибка при загрузке менторов: {e}")
        return []


def fetch_postcards():
    """Запрашивает список открыток с сервера и валидирует данные."""
    try:
        data = fetch_data("postcards")
        validate_json(data, postcards_schema)
        return data.get("postcards", [])
    except ServerError as e:
        logger.error(f"Ошибка при загрузке открыток: {e}")
        return []


def validate_json(response_json, schema):
    """
    Валидирует JSON-ответ по схеме API.
    Выбрасывает исключение `ServerError`, если валидация не пройдена.
    """
    try:
        validate(instance=response_json, schema=schema)
        logger.info("JSON успешно прошёл валидацию")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Ошибка валидации JSON: {e}")
        raise ServerError("Ошибка валидации данных от сервера") from e
