from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from src.settings_t.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
# settings,
#ссылка для подключения БД постгре
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# DATABASE_URL = settings.DB_URL
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass






#это функция для асинхронного запуска. Как к ней делать запросы пока не знаю. 
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#         # await session.close()





