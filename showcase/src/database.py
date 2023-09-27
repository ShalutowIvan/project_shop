from typing import AsyncGenerator

from fastapi import Depends

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase



from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from sqlalchemy.ext.declarative import declarative_base
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER



DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#для асинхронности добавить после postgresql
# +asyncpg

# Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
#асинхронный движок create_async_engine

# , poolclass=NullPool
metadata = MetaData()


# engine = create_async_engine(DATABASE_URL)

#это асинхронная сессия БД
async_session_maker = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

# async_session_maker = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)


# db = async_session_maker()


#это функция для асинхронного запуска. Как к ней делать запросы пока не знаю. 
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session










# class Base(DeclarativeBase):
#     pass


# class User(SQLAlchemyBaseUserTable[int], Base):
#     pass


# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)