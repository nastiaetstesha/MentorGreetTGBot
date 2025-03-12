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
                {"id": 1, "name": {"first": "Гений", "second": "Devman"}, "tg_username": "@eugene_dev", "tg_chat_id": 41878799, "bday": "1991-02-23"},
                {"id": 2, "name": {"first": "Ильмир", "second": "Devman"}, "tg_username": "@ilmir_dev", "tg_chat_id": 6467718221},
                {"id": 3, "name": {"first": "Ильмир", "second": "Devman"}, "tg_username": "@nurbek_dev", "tg_chat_id": 335075762, "bday": "1991-02-23"},
                {"id": 4, "name": {"first": "Катя", "second": "Иванова"}, "tg_username": "@katie", "tg_chat_id": 335000000},
                {"id": 5, "name": {"first": "Иван", "second": "Петряков"}, "tg_username": "@i_petr", "tg_chat_id": 335000001, "bday": "1991-02-23"},
                {"id": 6, "name": {"first": "Амир", "second": "Амиров"}, "tg_username": "@aarr", "tg_chat_id": 335000002, "bday": "1995-09-01"},
                {"id": 7, "name": {"first": "Анна", "second": "Мельникова"}, "tg_username": "@anna_ml", "tg_chat_id": 335000003, "bday": "1988-06-15"},
                {"id": 8, "name": {"first": "Александр", "second": "Сидоров"}, "tg_username": "@sasha_sid", "tg_chat_id": 335000004},
                {"id": 9, "name": {"first": "Михаил", "second": "Романов"}, "tg_username": "@mike_rom", "tg_chat_id": 335000005, "bday": "1989-12-04"},
                {"id": 10, "name": {"first": "Ольга", "second": "Смирнова"}, "tg_username": "@olga_sm", "tg_chat_id": 335000006},
                {"id": 11, "name": {"first": "Владимир", "second": "Кузнецов"}, "tg_username": "@v_kuz", "tg_chat_id": 335000007, "bday": "1987-05-11"},
                {"id": 12, "name": {"first": "Светлана", "second": "Орлова"}, "tg_username": "@sveta_orlova", "tg_chat_id": 335000008},
                {"id": 13, "name": {"first": "Дмитрий", "second": "Федоров"}, "tg_username": "@dmitry_fed", "tg_chat_id": 335000009, "bday": "1993-09-21"},
                {"id": 14, "name": {"first": "Юлия", "second": "Зайцева"}, "tg_username": "@yulia_z", "tg_chat_id": 335000010},
                {"id": 15, "name": {"first": "Георгий", "second": "Беляев"}, "tg_username": "@george_b", "tg_chat_id": 335000011, "bday": "1990-02-14"},
                {"id": 16, "name": {"first": "Анастасия", "second": "Лебедева"}, "tg_username": "@nasty_lebed", "tg_chat_id": 335000012},
                {"id": 17, "name": {"first": "Максим", "second": "Иванов"}, "tg_username": "@max_ivan", "tg_chat_id": 335000013, "bday": "1994-07-30"},
                {"id": 18, "name": {"first": "Наталья", "second": "Кравцова"}, "tg_username": "@nat_krav", "tg_chat_id": 335000014},
                {"id": 19, "name": {"first": "Виктор", "second": "Григорьев"}, "tg_username": "@viktor_g", "tg_chat_id": 335000015, "bday": "1996-04-18"},
                {"id": 20, "name": {"first": "Мария", "second": "Котова"}, "tg_username": "@masha_kot", "tg_chat_id": 335000016},
                {"id": 21, "name": {"first": "Андрей", "second": "Павлов"}, "tg_username": "@and_pav", "tg_chat_id": 335000017, "bday": "1992-08-10"},
                {"id": 22, "name": {"first": "Елизавета", "second": "Соколова"}, "tg_username": "@liz_sokol", "tg_chat_id": 335000018},
                {"id": 23, "name": {"first": "Сергей", "second": "Тихонов"}, "tg_username": "@sergey_t", "tg_chat_id": 335000019, "bday": "1985-01-05"},
                {"id": 24, "name": {"first": "Ксения", "second": "Фомина"}, "tg_username": "@ksenia_f", "tg_chat_id": 335000020},
                {"id": 25, "name": {"first": "Роман", "second": "Морозов"}, "tg_username": "@roman_m", "tg_chat_id": 335000021, "bday": "1998-11-12"},
                {"id": 26, "name": {"first": "Дарья", "second": "Алексеева"}, "tg_username": "@dasha_alex", "tg_chat_id": 335000022},
                {"id": 27, "name": {"first": "Вячеслав", "second": "Борисов"}, "tg_username": "@slava_b", "tg_chat_id": 335000023, "bday": "1991-06-03"},
                {"id": 28, "name": {"first": "Татьяна", "second": "Гончарова"}, "tg_username": "@tanya_g", "tg_chat_id": 335000024},
                {"id": 29, "name": {"first": "Константин", "second": "Михайлов"}, "tg_username": "@kostya_m", "tg_chat_id": 335000025, "bday": "1997-03-29"},
                {"id": 30, "name": {"first": "Оксана", "second": "Петрова"}, "tg_username": "@oksana_p", "tg_chat_id": 335000026},
                {"id": 31, "name": {"first": "Артур", "second": "Николаев"}, "tg_username": "@art_nik", "tg_chat_id": 335000027, "bday": "1995-05-20"},
                {"id": 32, "name": {"first": "Людмила", "second": "Гаврилова"}, "tg_username": "@luda_g", "tg_chat_id": 335000028},
                {"id": 33, "name": {"first": "Григорий", "second": "Кириллов"}, "tg_username": "@grig_k", "tg_chat_id": 335000029, "bday": "1986-10-07"},
                {"id": 34, "name": {"first": "Екатерина", "second": "Мартынова"}, "tg_username": "@katya_m", "tg_chat_id": 335000030},
                {"id": 35, "name": {"first": "Валерий", "second": "Прохоров"}, "tg_username": "@val_pro", "tg_chat_id": 335000031, "bday": "1993-07-25"},
                {"id": 36, "name": {"first": "Станислав", "second": "Логинов"}, "tg_username": "@stan_log", "tg_chat_id": 335000032}
                
            ]
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
