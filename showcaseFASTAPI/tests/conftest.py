import pytest
import asyncio
from typing import AsyncGenerator

from src.db import Base
# from src.showcase.models_t import *
# from src.regusers.models_t import *
from src.showcase.models import *
from src.regusers.models import *

# from src.db_t.database import Session as session
# from src.settings_t import *

from src.db.database import get_async_session

from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
#тестовые креды для ДБ
from tests.settings import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST, MODE
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool
# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

# DATABASE_URL_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, echo=True)
# engine_test = create_engine(DATABASE_URL_TEST, echo=True)
async_session_maker_test = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

# metadata.bind = engine_test

#надо сделать асинк движок БД, чтобы протестить БД асинхронно, типа пользаки асинхронно заходят регаются и как будет себя база вести при асинхронном подключении как на боевом подключении. 

#это функция для зависимости для тестов по аналогии в функцией зависимости Depends в роутерах. сешмейкре юзаем тестовый, который создали выше
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session

#добавили зависимость к приложению
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)#удаляются таблицы   ошибка тут не добавляется товары потому что база удалена
        await conn.run_sync(Base.metadata.create_all)#создаются таблицы
    yield#отдается доступ фастапи
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)#создаются таблицы
        

#также в файле toml сделали автоматический режим распознавания асинхронных функций. Но можно и самим писать pytest_asyncio в декораторе фикстуры



# # SETUP - зачем она нужна не понятно, но нужно ее создавать для асинхронных сессий
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


#создаем клиента. С ним можно юхзать post get запросы и тд. это синхронный клиент
client = TestClient(app)

#асинхронный клиент
@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:#тут мы как бы открываем сессию с клиентом 
        yield ac#ac.get или ac.post для пост и гет запросов



#общая фикстура будет запускаться перед запуском всех тестов и в конце. эта фикстура синхронная. Выше сделал асинхронные фикстуры
# @pytest.fixture(scope="session", autouse=True)
# def setup_db():
#     # print(f"{settings.DB_NAME=}")
#     assert MODE == "TEST"
#     # Base.metadata.drop_all(bind=engine_test)
#     Base.metadata.create_all(bind=engine_test)




# Base.metadata.create_all(bind=engine)


# @pytest.fixture(scope="function")
# def empty_goods():
#     CandiesService.delete_all()#клас товаро тут




# cnt = 0

# @pytest.fixture(scope="function", autouse=True)
# def cleanfile():
#     global cnt
#     with open("tests/file.txt", "w"):#открытие файла на чтение чистит весь файл при открытии, то есть все удаляет
#         pass
#     print(cnt)
#     cnt += 1


