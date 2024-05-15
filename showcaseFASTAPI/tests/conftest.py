import pytest
from src.db_t import Base, engine
from src.showcase.models_t import *

from src.settings_t import *


#общая фикстура будет запускаться перед запуском всех тестов и в конце
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    print(f"{settings.DB_NAME=}")
    assert settings.MODE == "TEST"
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)





# @pytest.fixture(scope="function")
# def empty_goods():
#     CandiesService.delete_all()#клас товаро тут








