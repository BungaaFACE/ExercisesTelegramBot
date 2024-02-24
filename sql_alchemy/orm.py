from sql_alchemy.models import TagsOrm, ProblemsOrm
from sql_alchemy.database import async_session_factory
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from sqlalchemy import distinct
from sqlalchemy.sql.expression import func
import logging


class BaseAsyncORM: 
        
    async def __aenter__(self):
        self._session = async_session_factory()
        return self

    async def _get_or_create_or_update(self, model, filter_by='name', session_add=True, update=False, **kwargs):
        """

        Args:
            model (_type_): ORM model
            filter_by (str, optional): search by that parameter. Defaults to 'name'. __all__ search all field in kwargs.
            session_add (bool, optional): add created model to session or not. Defaults to True.
            update (bool, optional): if row exists do it need update. Defaults to False.

        Returns:
            instanse: model instance
            is_created: if model instance was created
        """
        # choose model
        query = select(model)
        # filter by all kwargs or only selected in filter_by
        if filter_by == '__all__':
            query = query.filter_by(**kwargs)
        else:
            query = query.filter_by(**{filter_by: kwargs[filter_by]})
            
        instance = (await self._session.execute(query)).first()
        if instance:
            instance = instance[0]
            # if update param is True then updating all changed instance parameters
            if update:
                for parameter, value in kwargs.items():
                    if getattr(instance, parameter) != value:
                        instance.__setattr__(parameter, value)
                        
            return instance, False
        else:
            # create instance if not exist
            instance = model(**kwargs)
            # add created model to session if session_add param is True
            if session_add:
                self._session.add(instance)
            return instance, True

    async def _get_model_rows(self, 
                              model, 
                              filter_by: dict = None, 
                              filter_: list = None,
                              join=None, 
                              join_filter_by: dict  = None, 
                              columns: list=None, 
                              order_by: list = None,
                              limit: int=None):
        
        get_all_query = select(model)
        if filter_by:
            get_all_query = get_all_query.filter_by(**filter_by)
        if filter_:
            get_all_query = get_all_query.filter(*filter_)
        if join:
            get_all_query = get_all_query.join(join)
        if join_filter_by:
            get_all_query = get_all_query.filter_by(**join_filter_by)
        if columns:
            get_all_query = get_all_query.options(load_only(*columns))
        if order_by:
            get_all_query = get_all_query.order_by(*order_by)
        if limit:
            get_all_query = get_all_query.limit(limit)
        return (await self._session.execute(get_all_query)).scalars().all()
    

class InsertAsyncORM(BaseAsyncORM):
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(exc_type)
            logging.error(exc_val)
            logging.error(exc_tb)
            await self._session.rollback()
            raise exc_type(exc_val)
        else:
            await self._session.flush()
            await self._session.commit()
    
    async def __str_to_orm_tags(self, tags_list: list[str]):
        tags = []
        for tag_name in tags_list:
            tag, _ = await self._get_or_create_or_update(TagsOrm, name=tag_name)
            tags.append(tag)
        return tags
    
    async def add_problems(self, problems_list: list[dict]):
        problem_instances = []
        for problem_ind in range(len(problems_list)):
            tags_str_list = problems_list[problem_ind].pop('tags')
            tag_instances = await self.__str_to_orm_tags(tags_str_list)
            problem_instance, is_created = await self._get_or_create_or_update(ProblemsOrm, session_add=False, update=True, **problems_list[problem_ind])
            if is_created:
                problem_instance.problem_tags.extend(tag_instances)
                problem_instances.append(problem_instance)
        self._session.add_all(problem_instances)
    
class SelectAsyncORM(BaseAsyncORM):
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(exc_type)
            logging.error(exc_val)
            logging.error(exc_tb)
            raise exc_type(exc_val)
        else:
            await self._session.close()
    
    async def get_tag_names_list(self):
        return await self._get_model_rows(distinct(TagsOrm.name))
    
    async def get_difficulty_list(self):
        return await self._get_model_rows(distinct(ProblemsOrm.rating))
    
    async def get_problems_list(self, tag_name, difficulty):
        filter_by = {
            'rating': difficulty,
        }
        join_filter_by = {
            'name': tag_name
        }
        if filter_by['rating'] == 'Задачи без сложности':
            filter_by['rating'] = None
        elif filter_by['rating'] == 'Любая сложность':
            del filter_by['rating']
            
        return await self._get_model_rows(ProblemsOrm, 
                                          filter_by=filter_by, 
                                          join=ProblemsOrm.problem_tags, 
                                          join_filter_by=join_filter_by, 
                                          order_by=[func.random()],
                                          limit=10)
    
    async def get_problem_by_id(self, problem_id):
        return (await self._get_model_rows(ProblemsOrm, filter_by={'id': problem_id}))[0]
    
    async def get_problem_by_name(self, problem_name):
        return await self._get_model_rows(ProblemsOrm, 
                                          filter_=[ProblemsOrm.name.ilike(f'%{problem_name}%')], 
                                          limit=10)


if __name__ == "__main__":
    import asyncio
    async def test():
        async with SelectAsyncORM() as sql_select:
            problem = await sql_select.get_problem_by_name(problem_name='1285')
            print(problem)
        
    asyncio.run(test())
