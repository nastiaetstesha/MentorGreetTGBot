# Mock Server для Mentors и Postcards API

Этот мок-сервер реализует эмуляцию API для получения списка менторов (`/mentors`) и открыток (`/postcards`).

## Запуск сервера

### Требования
- Python 3.7+
- Установленный пакет `jj`
- Установленный `asyncio` и `json` (входят в стандартную библиотеку Python)

### Установка зависимостей
```sh
pip install jj
```

### Запуск сервера

Для запуска сервера выполните команду:
```sh
jj --port 8080
```

```sh
python mock_server.py
```

Сервер запустится на `http://localhost:8080`.

## Использование API

### Получение списка менторов
**Запрос:**
```http
GET /mentors
```

**Ответ:**
```json
{
    "mentors": [
        {}
    ]
}
```

### Получение списка открыток
**Запрос:**
```http
GET /postcards
```

**Ответ:**
```json
{
    "postcards": [
        {"id": 1, "holidayId": "01.01", "name_ru": "FFFFНовый год", "body": "🎉✨С Новым годом! Пусть этот год принесёт вам счастье, здоровье и успех!"},
        {"id": 2, "holidayId": "01.01", "name_ru": "UНовый год", "body": "🚀Новый год — это начало новой главы! Пусть она будет написана счастьем!"}
    ]
}
```

## Остановка сервера
Сервер можно остановить с помощью сочетания клавиш:
```
CTRL + C
```

## Получение истории запросов

Вы можете получить историю запросов, вызвав `fetch_mock_history()` в коде или запустив соответствующую функцию.

Пример вызова в коде:
```python
asyncio.run(fetch_mock_history())
```

## Кейсы для тестирования

| Файл | Описание |
|-------|-----------|
| `mock_server.py` | 30+ менторов |
| `mock2_server.py` | два ментора с идентичным именем |
| `mock3_server.py` | список менторов пуст |
| `mock4_server.py` | имя ментора состоит из 15 слов |

Этот мок-сервер полезен для тестирования взаимодействий с API, отладки кода и моделирования различных сценариев.




