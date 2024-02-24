from telethon import Button
from telethon.types import KeyboardButtonCallback
from sql_alchemy.orm import SelectAsyncORM


start_kb = [
    [KeyboardButtonCallback('Поиск по теме+сложности', data='tag_and_diff')],
    [KeyboardButtonCallback('Поиск по названию/id', data='name_or_id')]
]


async def get_tags_reply_kb():
    async with SelectAsyncORM() as db:
        tag_list = await db.get_tag_names_list()
    
    kb = []
    for tag in tag_list:
        kb.append([Button.text(tag, resize=True)])
        
    kb.append([Button.text('Отмена', resize=True)])
    
    return kb


async def get_difficulty_reply_kb():
    async with SelectAsyncORM() as db:
        diff_list: list[str] = await db.get_difficulty_list()
        
    if None in diff_list:
        diff_list.remove(None)
    diff_list.sort()
    diff_list.insert(0, 'Задачи без сложности')
    diff_list.insert(0, 'Любая сложность')
        
    
    kb = []
    for diff in diff_list:
        kb.append([Button.text(str(diff), resize=True)])
        
    kb.append([Button.text('Отмена', resize=True)])
    
    return kb


async def get_problems_set_kb(problem_name=None, tag_name=None, difficulty=None):
    async with SelectAsyncORM() as db:
        if problem_name:
            problems = await db.get_problem_by_name(problem_name=problem_name)
        elif tag_name and difficulty:
            problems = await db.get_problems_list(tag_name=tag_name, difficulty=int(difficulty))
    
    kb = []
    for problem in problems:
        tags_str = ", ".join([tag.name for tag in problem.problem_tags])
        problem_id, problem_letter, *_ = problem.name.split(' ')
        kb.append([KeyboardButtonCallback(
            f'{problem.name} Теги: {tags_str}', 
            data=f'problem_{problem.id}'
            )]
        )

    return len(problems), kb


