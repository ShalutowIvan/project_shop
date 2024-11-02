import pytest
from src.showcase.schemas import *
from src.showcase.models import *
from tests.conftest import async_session_maker_test
# from src.db_t.database import Session as session

from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import insert, select
# from contextlib import nullcontext as does_not_raise#nullcontext означет что нет ошибки исключения с контекстом

from httpx import AsyncClient

# @pytest.fixture
# def goods():
#
#     goods = [
#         Goods(name_product="Хлеб", vendor_code="qwe-123", stock=10, price=30, slug="hleb", photo="tut", availability=True, group_id=1),
#         Goods(name_product="Масло", vendor_code="asd-123", stock=11, price=150, slug="maslo", photo="tut2", availability=True, group_id=2),
#         Goods(name_product="Молоко", vendor_code="zxc-123", stock=12, price=55, slug="milk", photo="tut3", availability=True, group_id=2)
#     ]
#     return goods
#
#
# @pytest.fixture
# def group():
#     group = [
#     Group(name_group="Хлеб", slug="hleb"),
#     Group(name_group="Молоко", slug="milk")
#     ]
#     return group


#тест кнопки добавления товара в корзину
@pytest.mark.parametrize(
                        "good_id, status_code",
                         [
                             (1, 200),
                             (555, 200),
                             ("qwe", 200)
                         ])
async def test_add_in_basket(good_id, status_code, ac: AsyncClient):
    response = await ac.get(f"/basket/{good_id}")
    assert response.status_code == status_code


#тест кнопки удаления товара из корзины
# @pytest.mark.parametrize(
#     "basket_id, status_code",
#     [
#         (1, 200),
#         (5, 200),
#         (77777, 200),
#         ("qwe", 200)
#     ]
# )
# async def test_delete_in_basket(basket_id, status_code, ac: AsyncClient):
#     response = await ac.get(f"/basket/{basket_id}")
#     assert response.status_code == status_code


#тест формы запроса контактов
# @pytest.mark.parametrize(
#     "fio, phone, delivery_address, pay, status_code",
#     [
#         ("Петров Иван", 89996667777, "домой", 1, 200),#тут все ок
#         ("Сидоров Петр", "asd", "домой", 1, 200),#вместо телефона строка
#         ("Глеб Вачовски", 89996667777, "домой", "asd", 200),#вместо способа оплаты строка
#         ("Анастасия Заворотнюк", 89996667777, "домой", 555, 200)#неверный код способа оплаты
#     ]
# )
# async def test_contacts_form(fio, phone, delivery_address, pay, status_code, ac: AsyncClient):
#     response = await ac.post("/basket/contacts/",
#                              data={
#                                      "fio": fio,
#                              		"phone": phone,
#                              		"delivery_address": delivery_address,
#                              		"pay": pay
#                                  }
#                              )
#     assert response.status_code == status_code











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


# витрина
# 1. Проверить, что на главной отображаются все товары из каталога - скорее всего не надо
# 2. проверить что при нажатии на группу выводятся товары из этой группы
# 3. Проверить добавление товара в корзину, что товар добавился. - проверил что товар просто добавляется. заморочка с авторизацией, не могу прокинуть токен
# 4. Проверить что корзина отображается по нужному пользаку
# 5. Проверить удаление из корзины - сделал
# 6. Проверить пост запрос для оформления заказа - сделал
# 7. Проверить что список заказов отображается по нужному пользаку
# 8. Проверить роутер для получения заказов это гет запрос
# 9. Проверить получения товаров из учетной системы
# 10. Проверить получения групп товаров из учетной системы
# 11. Проверить смену статуса заказов при синхронизации с учетной системой




