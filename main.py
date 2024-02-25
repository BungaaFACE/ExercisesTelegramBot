import asyncio
from dotenv import load_dotenv
from codeforces_api.codeforces_api import sync_exercises_task
from config import settings
from telethon import TelegramClient
from telegram_bot.handlers import problem_detail, search_problem_by_name, start_message, search_tag_and_difficulty

load_dotenv(dotenv_path='.env')




async def main():
    # Cоздаем бота
    bot_client = await TelegramClient('bot_session', settings.API_ID, settings.API_HASH).start(bot_token=settings.TELEGRAM_BOT_TOKEN)
    bot_client.add_event_handler(start_message)
    bot_client.add_event_handler(search_tag_and_difficulty)
    bot_client.add_event_handler(problem_detail)
    bot_client.add_event_handler(search_problem_by_name)
    
    # Добавляем периодическую задачу для парсинга задач
    await sync_exercises_task(settings.TIME_PERIOD)
    # Поскольку бот telethon запускается при выполнении команды bot.start, нам не нужно выполнять run_until_disconnected() и т.п.
    # В синхронизации задач и так стоит бесконечный цикл


if __name__ == '__main__':
    asyncio.run(main())
    