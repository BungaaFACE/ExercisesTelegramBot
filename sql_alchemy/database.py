from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from config import settings

db_url = settings.DATABASE_URL_psycopg
if settings.TEST:
    db_url = settings.TEST_SQLITE_SYNC

sync_engine = create_engine(
    url=db_url,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_db_url = settings.DATABASE_URL_asyncpg
if settings.TEST:
    async_db_url = settings.TEST_SQLITE_ASYNC

async_engine = create_async_engine(
    url=async_db_url,
    echo=True,
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    repr_cols_num = 2
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"