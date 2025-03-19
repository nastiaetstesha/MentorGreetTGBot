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
                {"id": 1, "name": {"first": "Мир", "second": "Devman"}, "tg_username": "@eugene_dev", "tg_chat_id": 41878799, "bday": "1991-02-23"},
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
                {"id": 11, "holidayId": "wedding", "name_ru": "Свадьба", "body": "💍 Поздравляем #name с этим счастливым днем! Пусть ваш союз будет крепким!"},
                {"id": 12, "holidayId": "wedding", "name_ru": "Свадьба", "body": "👰🤵 #name, желаем любви, счастья и гармонии в вашей семье!"},
                {"id": 13, "holidayId": "8march", "name_ru": "8 марта", "body": "🌸💐 #name, с 8 марта! Пусть этот день принесет радость и весеннее настроение!"},
                {"id": 14, "holidayId": "8march", "name_ru": "8 марта", "body": "🌺 Пусть женская красота, доброта и мудрость наполняют этот мир! #name, с праздником!"},
                {"id": 15, "holidayId": "23feb", "name_ru": "23 февраля", "body": "🛡️ #name, с Днём защитника Отечества! Пусть мужество и сила ведут вас вперед!"},
                {"id": 16, "holidayId": "23feb", "name_ru": "23 февраля", "body": "⚔️ #name, желаем стойкости, успехов и надёжных товарищей рядом!"},
                {"id": 17, "holidayId": "child_day", "name_ru": "День защиты детей", "body": "👶 Пусть дети всегда улыбаются! #name, поздравляем с праздником!"},
                {"id": 18, "holidayId": "child_day", "name_ru": "День защиты детей", "body": "🎠 Пусть каждый ребёнок будет счастлив и окружен заботой!"},
                {"id": 19, "holidayId": "teacher_day", "name_ru": "День учителя", "body": "📚 #name, спасибо за знания, мудрость и терпение!"},
                {"id": 20, "holidayId": "teacher_day", "name_ru": "День учителя", "body": "🏫 Пусть ваши ученики всегда вас радуют!"},
                {"id": 21, "holidayId": "valentine", "name_ru": "День Святого Валентина", "body": "💖 #name, пусть ваша любовь будет вечной и взаимной!"},
                {"id": 22, "holidayId": "valentine", "name_ru": "День Святого Валентина", "body": "❤️ Пусть сердца влюбленных бьются в унисон!"},
                {"id": 23, "holidayId": "new_baby", "name_ru": "Рождение ребёнка", "body": "👣 #name, поздравляем с появлением маленького чуда в вашей семье!"},
                {"id": 24, "holidayId": "new_baby", "name_ru": "Рождение ребёнка", "body": "🎀 Пусть малыш растет здоровым и счастливым!"},
                {"id": 25, "holidayId": "promotion", "name_ru": "Повышение", "body": "📈 Поздравляем #name с новой ступенью в карьере!"},
                {"id": 26, "holidayId": "promotion", "name_ru": "Повышение", "body": "🎊 Пусть успех сопровождает вас на новом пути!"},
                {"id": 27, "holidayId": "good_luck", "name_ru": "Желаем удачи", "body": "🍀 #name, пусть удача всегда будет на вашей стороне!"},
                {"id": 28, "holidayId": "good_luck", "name_ru": "Желаем удачи", "body": "✨ Желаем исполнения всех ваших желаний!"},
                {"id": 29, "holidayId": "just_because", "name_ru": "Просто так", "body": "🌟 #name, пусть ваш день будет радостным и ярким!"},
                {"id": 30, "holidayId": "just_because", "name_ru": "Просто так", "body": "😊 Без причины, просто хотим пожелать вам хорошего дня!"},
                {"id": 31, "holidayId": "motivation", "name_ru": "Мотивация", "body": "🔥 #name, не останавливайтесь, двигайтесь к своей цели!"},
                {"id": 32, "holidayId": "motivation", "name_ru": "Мотивация", "body": "🚀 Пусть каждый день приближает вас к мечте!"},
                {"id": 33, "holidayId": "travel", "name_ru": "Путешествие", "body": "🧳 #name, пусть ваш отпуск будет незабываемым!"},
                {"id": 34, "holidayId": "travel", "name_ru": "Путешествие", "body": "✈️ Желаем ярких эмоций и новых открытий!"},
                {"id": 35, "holidayId": "retirement", "name_ru": "Выход на пенсию", "body": "🎉 #name, пусть новый этап жизни будет радостным!"},
                {"id": 36, "holidayId": "retirement", "name_ru": "Выход на пенсию", "body": "🏡 Время для отдыха и новых увлечений!"},
                {"id": 37, "holidayId": "new_home", "name_ru": "Новоселье", "body": "🏠 Поздравляем #name с новым уютным домом!"},
                {"id": 38, "holidayId": "new_home", "name_ru": "Новоселье", "body": "🎁 Пусть в вашем доме всегда будет тепло и радость!"},
                {"id": 39, "holidayId": "health", "name_ru": "Желаем здоровья", "body": "💪 #name, желаем вам крепкого здоровья!"},
                {"id": 40, "holidayId": "health", "name_ru": "Желаем здоровья", "body": "🌿 Пусть каждый день приносит вам энергию и силы!"},
                {"id": 41, "holidayId": "baby_shower", "name_ru": "Рождение ребёнка", "body": "👶 #name, поздравляем с появлением малыша! Пусть он растет здоровым и счастливым!"},
                {"id": 42, "holidayId": "baby_shower", "name_ru": "Рождение ребёнка", "body": "🎀 Пусть ваш ребёнок приносит радость и вдохновение!"},
                {"id": 43, "holidayId": "engagement", "name_ru": "Помолвка", "body": "💍 #name, поздравляем с помолвкой! Пусть любовь ведёт вас вперёд!"},
                {"id": 44, "holidayId": "engagement", "name_ru": "Помолвка", "body": "💖 Пусть ваш союз будет крепким и счастливым!"},
                {"id": 45, "holidayId": "retirement", "name_ru": "Выход на пенсию", "body": "🏡 #name, желаем наслаждаться заслуженным отдыхом!"},
                {"id": 46, "holidayId": "retirement", "name_ru": "Выход на пенсию", "body": "🎉 Поздравляем! Теперь у вас больше времени для себя!"},
                {"id": 47, "holidayId": "travel", "name_ru": "Путешествие", "body": "✈️ #name, пусть ваше путешествие будет полным приключений!"},
                {"id": 48, "holidayId": "travel", "name_ru": "Путешествие", "body": "🌍 Желаем вам незабываемых впечатлений и новых открытий!"},
                {"id": 49, "holidayId": "recovery", "name_ru": "Скорейшего выздоровления", "body": "🏥 #name, желаем вам быстрого выздоровления!"},
                {"id": 50, "holidayId": "recovery", "name_ru": "Скорейшего выздоровления", "body": "💪 Пусть здоровье вернётся как можно скорее!"},
                {"id": 51, "holidayId": "good_luck", "name_ru": "Желаем удачи", "body": "🍀 #name, пусть удача всегда будет на вашей стороне!"},
                {"id": 52, "holidayId": "good_luck", "name_ru": "Желаем удачи", "body": "✨ Желаем исполнения всех ваших желаний!"},
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
