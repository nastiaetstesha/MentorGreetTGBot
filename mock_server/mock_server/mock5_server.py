import jj
import asyncio
import json

from jj.mock import mocked


async def run_mock_server():
    matcher_mentors = jj.match("GET", "/mentors")
    response_mentors = jj.Response(
        status=200,
        body=json.dumps({
            "mentors": [
                {"id": 1, "name": {}, "tg_username": "@eugene_dev", "tg_chat_id": 41878799, "bday": "1991-02-23"},
                {"id": 2, "name": {"first": "Ильмир", "second": "Devman"}, "tg_username": "@ilmir_dev", "tg_chat_id": 6467718221},
                {"id": 3, "name": {"first": "Нурбек", "second": "Devman"}, "tg_username": "@nurbek_dev", "tg_chat_id": 335075762, "bday": "1991-02-23"},
                {"id": 4, "name": {"first": "Катя", "second": "Иванова"}, "tg_username": "@katie", "tg_chat_id": 335000000},
                {"id": 5, "name": {"first": "Иван", "second": "Петряков"}, "tg_username": "@i_petr", "tg_chat_id": 335000001, "bday": "1991-02-23"},
                {"id": 6, "name": {"first": "Амир", "second": "Амиров"}, "tg_username": "@aarr", "tg_chat_id": 335000002, "bday": "1995-09-01"},

            ], "count": 2
        }, ensure_ascii=False)
    )

    matcher_postcards = jj.match("GET", "/postcards")
    response_postcards = jj.Response(
        status=200,
        body=json.dumps({
            "postcards": [
                {"id": 1, "holidayId": "01.01", "name_ru": "Новый год", "body": "🎉✨С Новым годом! Пусть этот год принесёт вам счастье, здоровье и успех!"},
                {"id": 2, "holidayId": "01.01", "name_ru": "Новый год", "body": "🚀Новый год — это начало новой главы! Пусть она будет написана счастьем!"},
                {"id": 3, "holidayId": "01.01", "name_ru": "Новый год", "body": "С Новым годом! Пусть всё задуманное сбудется! 🎉"},
                {"id": 4, "holidayId": "01.01", "name_ru": "Новый год", "body": "Пусть Новый год принесет удачу и радость! 🎇"},
                {"id": 5, "holidayId": "01.01", "name_ru": "Новый год", "body": "Новогодние чудеса уже начались! 🌟"},
                {"id": 6, "holidayId": "birthday", "name_ru": "День рождения", "body": "🎂🎉 #name, С Днём рождения! Пусть этот год будет наполнен радостью и любовью!"},
                {"id": 7, "holidayId": "birthday", "name_ru": "День рождения", "body": "🎁🎈 #name, С Днём рождения! Пусть все ваши желания исполняются!"},
                {"id": 8, "holidayId": "birthday", "name_ru": "День рождения", "body": "С Днём рождения! Пусть каждый день дарит радость! 🎂"},
                {"id": 9, "holidayId": "birthday", "name_ru": "День рождения", "body": "Поздравляю с Днём рождения! Пусть мечты сбываются! 🌈"},
                {"id": 10, "holidayId": "birthday", "name_ru": "День рождения", "body": "С днём рождения! Всего самого наилучшего! 🎁"}
            ]
        }, ensure_ascii=False)
    )

    # Создаем persistent mocks
    mock_mentors = await mocked(matcher_mentors, response_mentors)
    mock_postcards = await mocked(matcher_postcards, response_postcards)

    print("Mock сервер запущен на http://localhost:8080")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n Сервер остановлен.")


async def fetch_mock_history():
    matcher_mentors = jj.match("GET", "/mentors")
    response_mentors = jj.Response(status=200, json={})

    mock = await mocked(matcher_mentors, response_mentors)
    history = await mock.fetch_history()
    print("\n📜 История запросов к /mentors:", history)

if __name__ == "__main__":
    try:
        asyncio.run(run_mock_server())
    except KeyboardInterrupt:
        pass
