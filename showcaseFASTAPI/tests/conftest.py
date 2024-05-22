import pytest
from src.db_t import Base, engine
from src.showcase.models_t import *
from src.regusers.models_t import *
from src.db_t.database import Session as session
from src.settings_t import *


#общая фикстура будет запускаться перед запуском всех тестов и в конце
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # print(f"{settings.DB_NAME=}")
    assert MODE == "TEST"
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


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


