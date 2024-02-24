import asyncio
import aiohttp
import html2text
from bs4 import BeautifulSoup
from sql_alchemy.orm import InsertAsyncORM


PARAMETERS = {
    'lang': 'ru',
}


async def sync_exercises_task(time_period):
    while True:
        await sync_exercises()
        await asyncio.sleep(time_period)

async def sync_exercises():
    URL = 'https://codeforces.com/api/problemset.problems'

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=PARAMETERS) as response:
            
            if response.status == 200:
                result = (await response.json())['result']
                problems_statistics = result['problemStatistics']
                problems = result['problems']
                
                problems_list = list(map(lambda problem_ind: 
                    {'name': f'{problems_statistics[problem_ind]["contestId"]} {problems_statistics[problem_ind]["index"]} {problems[problem_ind]["name"]}', 
                    'solved_count': int(problems_statistics[problem_ind]['solvedCount']),
                    'rating': problems[problem_ind].get('rating'), 
                    # get only unique tags keeping order
                    'tags': sorted(set(problems[problem_ind]['tags']), key=problems[problem_ind]['tags'].index)}, 
                    
                    range(len(problems))))
                async with InsertAsyncORM() as sql_insert:
                    await sql_insert.add_problems(problems_list)

async def get_exercise_description(problem_name: str):
    exercise_number, exercise_letter, *_ = problem_name.split(' ')
    url = f'https://codeforces.com/problemset/problem/{exercise_number}/{exercise_letter}'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=PARAMETERS) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), features='html.parser')

                html = str(soup.find('div', {'class' : 'problem-statement'}))
                html = html.replace('<pre>', '').replace('</pre>', '')
                html = html.replace('\gt', '>')
                html = html.replace('\ge', '>=')
                html = html.replace('\lt', '<')
                html = html.replace('\le', '<=')
                html = html.replace('\n', '<br>')
                html = html.replace('\dots', '....')

                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = True
                text = text_maker.handle(html)
                text = text.replace('$$$', '')
                
                text += f'\n\nСсылка: {url}'
                return text
            else:
                return f'Не удалось получить детали задачи.\nИспользуйте ссылку: {url}'


if __name__ == "__main__":
    # asyncio.run(sync_exercises())
    async def test():
        print(await get_exercise_description('1285 B awd awdwa'))
    
    asyncio.run(test())
    
'''
    result: {
        problemStatistics: [
            {'contestId': 1928, 'index': 'F', 'solvedCount': 41},
            ...
        ],
        problems: [
            {'contestId': 1928,
            'index': 'F',
            'name': 'Цифровые узоры',
            'points': 2750.0,
            'tags': ['combinatorics', 'data structures', 'math'],
            'type': 'PROGRAMMING'},
            ...
        ]
    },
    status: 'OK'

'''