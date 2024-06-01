import pytest
from src.showcase.schemas import *
from src.showcase.models import *

# from src.db_t.database import Session as session
# from tests.conftest import engine_test
from sqlalchemy.orm import Session
from datetime import datetime

# from contextlib import nullcontext as does_not_raise#nullcontext означет что нет ошибки исключения с контекстом
from tests.conftest import client, async_session_maker_test


@pytest.fixture
def goods():
    
    goods = [
        Goods(name_product="Хлеб", vendor_code="qwe-123", stock=10, price=30, slug="hleb", photo="tut", availability=True, group_id=1),
        Goods(name_product="Масло", vendor_code="asd-123", stock=11, price=150, slug="maslo", photo="tut2", availability=True, group_id=2),
        Goods(name_product="Молоко", vendor_code="zxc-123", stock=12, price=55, slug="milk", photo="tut3", availability=True, group_id=2)
    ]
    return goods


@pytest.fixture
def group():
    group = [
    Group(name_group="Хлеб", slug="hleb"),
    Group(name_group="Молоко", slug="milk")
    ]
    return group



# @pytest.mark.usefixtures("empty_goods")
# class TestGoods:

	# def test_count_goods(self, goods):
    #     for i in goods:
    #         CandiesService.add(candy)#тут должен быть класс товаров

    #     assert CandiesService.count() == 3

    # @pytest.mark.usefixtures("group")
    # def test_add_group(self, group):
    #     with Session(autoflush=False, bind=engine_test) as db:
    #         for i in group:
    #             db.add(i)

    #         db.commit()


    # @pytest.mark.usefixtures("goods")
    # def test_list_goods(self, goods):
        
    #     with Session(autoflush=False, bind=engine_test) as db:
    #         for i in goods:
    #             db.add(i)

    #         db.commit()




        #поменял вместо pydentic модели обычную орм модель, сработало, то есть передаю без валидации
        
    

#
#
# @pytest.mark.usefixtures("group")
# async def test_add_group(group):
#     async with async_session_maker_test() as session:
#         for i in group:
#             session.add(i)
#
#         await session.commit()
#
#
# @pytest.mark.usefixtures("goods")
# async def test_list_goods(goods):
#
#     async with async_session_maker_test() as session:
#         for i in goods:
#             session.add(i)
#
#         await session.commit()
#
#
#



        