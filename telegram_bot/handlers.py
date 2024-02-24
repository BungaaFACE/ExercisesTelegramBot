from telegram_bot import keyboards as kb
from telethon import events
from pprint import pprint
from telegram_bot.services import get_problem_text, wait_for_response
from sql_alchemy.orm import SelectAsyncORM


@events.register(events.NewMessage(pattern='/start'))
async def start_message(event):
    await event.respond('Добро пожаловать в бота по подборке задач с codeforces!', buttons=kb.start_kb)


@events.register(events.CallbackQuery(data=b'tag_and_diff'))
async def search_tag_and_difficulty(event):
    
    response_event = await wait_for_response(event, 'Выберите тему', keyboard=await kb.get_tags_reply_kb())
    
    if response_event:
        tag_name = response_event.text
        if tag_name == 'Отмена':
            await event.respond('Главное меню', buttons=kb.start_kb)
            return

    response_event = await wait_for_response(event, 'Выберите минимальную сложность:', keyboard=await kb.get_difficulty_reply_kb())
    
    if response_event:
        difficulty = response_event.text
        if tag_name == 'Отмена':
            await event.respond('Главное меню', buttons=kb.start_kb)
            return
    
    problems_count, keyboard = await kb.get_problems_set_kb(tag_name=tag_name, difficulty=difficulty)
    if not problems_count:
        await event.respond('По заданным критериям задач нет.')
    else:
        await event.respond(f'Вот подборка из {problems_count} задач по заданным критериям:', buttons=keyboard)
    

@events.register(events.CallbackQuery(data=b'name_or_id'))
async def search_problem_by_name(event):
    
    response_event = await wait_for_response(event, 'Введите часть названия/id задачи:')
    
    if response_event:
        problem_name = response_event.text
        
        problems_count, keyboard = await kb.get_problems_set_kb(problem_name=problem_name)
        
        if not problems_count:
            await event.respond('По заданным критериям задач нет.')
        else:
            await event.respond(f'Вот подборка из {problems_count} задач по заданным критериям:', buttons=keyboard)


@events.register(events.CallbackQuery())
async def problem_detail(event):
    callback_text = event.data.decode()
    # callback для задачи
    if callback_text.startswith('problem'):
        _, problem_id = callback_text.split('_')
        message = await get_problem_text(problem_id)
        await event.respond(message)

