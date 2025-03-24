import jsonschema
import logging
import os
import requests

from dotenv import load_dotenv
from jsonschema import validate


load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

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


class APIClientError(Exception):
    """Базовое исключение клиента API"""
    pass


class APIConnectionError(APIClientError):
    """Ошибка подключения к серверу"""
    pass


class APIHTTPError(APIClientError):
    """Сервер вернул ошибку HTTP"""
    pass


class APIParsingError(APIClientError):
    """Ошибка парсинга JSON"""
    pass


class APIValidationError(APIClientError):
    """Ошибка валидации полученного JSON по схеме"""
    pass


def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Ошибка подключения при запросе {url}: {e}")
        raise APIConnectionError("Не удалось подключиться к серверу") from e

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP {response.status_code} при запросе {url}: {e}")
        raise APIHTTPError(f"Сервер вернул ошибку: {response.status_code}") from e

    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Ошибка разбора JSON при запросе {url}: {e}")
        raise APIParsingError("Ошибка разбора JSON-ответа") from e

    except requests.exceptions.RequestException as e:
        logger.error(f"Сетевая ошибка при запросе {url}: {e}")
        raise APIClientError("Общая ошибка API-клиента") from e


def fetch_mentors():
    """Запрашивает список менторов с сервера и валидирует данные."""
    try:
        data = fetch_data("mentors")
        validate_json(data, mentors_schema)
        return data.get("mentors", [])
    except APIClientError as e:
        logger.error(f"Ошибка при загрузке менторов: {e}")
        return []


def fetch_postcards():
    """Запрашивает список открыток с сервера и валидирует данные."""
    try:
        data = fetch_data("postcards")
        validate_json(data, postcards_schema)
        return data.get("postcards", [])
    except APIClientError as e:
        logger.error(f"Ошибка при загрузке открыток: {e}")
        return []


def validate_json(response_json, schema):
    """
    Валидирует JSON-ответ по схеме API.
    Выбрасывает исключение `ServerError`, если валидация не пройдена.
    """
    try:
        validate(instance=response_json, schema=schema)
        logger.info("JSON успешно прошёл валидацию по схеме.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise APIValidationError("Данные не соответствуют схеме API") from e

