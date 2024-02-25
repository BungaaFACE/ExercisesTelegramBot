import asyncio
from codeforces_api.codeforces_api import get_exercise_description
from sql_alchemy.models import ProblemsOrm
from sql_alchemy.orm import SelectAsyncORM


async def wait_for_response(event, message, keyboard=None):
    print(message, keyboard)
    client = event.client
    chat_id = event.chat.id
    async with client.conversation(chat_id) as conv:

        # Сообщение и кнопка отмены
        await conv.send_message(message, buttons=keyboard)

        # Ожидание ответа
        tasks = [conv.get_response()]
        done, pendind = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        event = done.pop().result()
        return event

async def get_problem_text(problem_id):
    text = ''
    
    async with SelectAsyncORM() as db:
        problem: ProblemsOrm = await db.get_problem_by_id(problem_id)
    
    text += f'Название: {problem.name}\n'\
        f'Количество решений задачи: {problem.solved_count}\n'\
        f'Сложность: {problem.rating}\n'\
        f'Темы: {", ".join([tag.name for tag in problem.problem_tags])}\n\n'
    
    text += f'**{await get_exercise_description(problem.name)}**'
    
    return text