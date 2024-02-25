from sql_alchemy.orm import InsertAsyncORM, SelectAsyncORM, TagsOrm, ProblemsOrm
import pytest
from copy import deepcopy

@pytest.mark.asyncio_cooperative
async def test_columns_prints_problem_instance():

    async with SelectAsyncORM() as sql_select:
        problem = await sql_select.get_problem_by_name(problem_name='1285')
        assert problem is not None


@pytest.mark.asyncio_cooperative
async def test_async_db_classes():
    

    test_problems = [
        {'name': '!TEST! 1931 G Одномерный пазл',
        'rating': 2000,
        'solved_count': 1554,
        'tags': ['combinatorics', 'math', 'number theory']},
        {'name': '!TEST! 1931 F Скриншоты чата',
        'rating': 1700,
        'solved_count': 4858,
        'tags': ['combinatorics',
                'dfs and similar',
                'graphs',
                'greedy',
                'implementation']},
        {'name': '!TEST! 1931 E Аня и подарок на День святого Валентина',
        'rating': 1400,
        'solved_count': 9642,
        'tags': ['games', 'greedy', 'math', 'sortings']},
        {'name': '!TEST! 1931 D Делимые пары',
        'rating': 1300,
        'solved_count': 11707,
        'tags': ['combinatorics', 'math', 'number theory']}
    ]
    
    test_problems_copy = deepcopy(test_problems)

    async with InsertAsyncORM() as sql_insert:
        await sql_insert.add_problems(test_problems_copy)

    async with SelectAsyncORM() as sql_select:
        tags = await sql_select._get_model_rows(TagsOrm)
        # skip this assert because DB already filled with data
        # assert len(tags) == 9
        assert tags is not None
        problems = await sql_select.get_problem_by_name(problem_name='!TEST! ')
        assert len(problems) == len(test_problems)
        for problem_ind in range(len(test_problems)):
            assert problems[problem_ind].name == test_problems[problem_ind]['name']
            assert problems[problem_ind].tag is not None
        
        assert repr(problems[0]).endswith(', name=!TEST! 1931 G Одномерный пазл>')