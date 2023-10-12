from typing import AsyncGenerator

from fastapi import Depends

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
# from regusers.models import User

from sqlalchemy.pool import NullPool
# from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import MetaData, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


#ссылка для подключения БД постгре
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#асинхронный движок create_async_engine
engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

# metadata = MetaData()

#это асинхронная сессия БД
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# autoflush=False,

# , poolclass=NullPool


# __all__ = ['Base']

#остановился тут. Я скопировал это из базового класса SQLAlchemyBaseUserTable(Generic[ID]). Тут надо дальше все импортировать и тд
#https://www.youtube.com/watch?v=nfueh3ei8HU&t=789s

#я решил делать чере бд и куки, а не просто jwt стратегия.
# class User(SQLAlchemyBaseUserTableUUID, Base):
#     email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
#     hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

#мы юзаем алембик, это нам не надо
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
#


#это функция для асинхронного запуска. Как к ней делать запросы пока не знаю. 
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)






