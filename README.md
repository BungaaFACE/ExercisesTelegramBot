# Exercises Telegram Bot
## Описание
Данный бот автоматически парсит задачи с ресурса codeforces.com и выводит задачи по вашим фильтрам. 
Периодичность парсера можно настроить.  
## Стэк
 - Async
 - Telethon
 - SQL Alchemy
 - aiohttp
 - API
 - ООП
## Возможности бота
 - Настройка периодичности парсинга задач  
 - Подборка задач по тегам и сложности
 - Если задач по критериям тега и сложности более 10 - вывод рандомных задач
 - Поиск задачи по названию
 - Вывод условий задачи и данных о количестве решений и т.п.
## Установка и запуск
1. Клонирование репозитория:
`git clone https://github.com/BungaaFACE/ExercisesTelegramBot`
2. Войти в папку проекта:
`cd ExercisesTelegramBot`
3. Установить зависимости:
`pip install -r requirements.txt`
4. Переименовать файл .env.tpl --> .env
5. Ввести свои данные аккаунта разработчика Telegram, бота и БД.  
Примечание: если у вас есть данных БД знаки @, : и т.п. возспользуйтесь URL encoder для перевода символов в формат URL. Например @ == %40.  
6. Запустить файл main.py.