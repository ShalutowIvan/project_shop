import pytest
from conftest import client, async_session_maker_test

from src.regusers.models import *
# from sqlalchemy import insert, select

from httpx import AsyncClient
from contextlib import nullcontext as not_raise
# async def test_



#функция тестирования авторизации, для отправки данных формы нужно писать data вместо json. пока синхронная
# def test_reg():
# 	response = client.post("/regusers/registration", data={
# 		"name": "Василий Петрович",
# 		"email": "ivanshalutov@yandex.ru",
# 		"password1": "Qwer1234",
# 		"password2": "Qwer1234"
# 		})

# 	assert response.status_code == 200

# #асинхронный вариант функции
@pytest.mark.parametrize(
    "name, email, password1, password2, error", [
    ("Василий Петрович", "почта яндекса", "Qwer1234", "Qwer1234", not_raise),
    ("Василий Петрович", "asd@asd", "Qwer1234", "Qwer1234", value_error),#проверка на точку в домене после собаки
    ("", "", "", "", missing),
    ("Василий Петрович", "asd", "Qwer1234", "Qwer1234", value_error),
    ()
    ])
async def test_reg_async(name, email, password1, password2, error, ac: AsyncClient):
    response = await ac.post("/regusers/registration", data={
        "name": "Василий Петрович",
		"email": "почта яндекса",
		"password1": "Qwer1234",
		"password2": "Qwer1234"
    })
    with expectation:
        assert тут доделать!!!!!!!!!!!!!!!!!!

    # assert response.status_code == 303

#при некорректном емейл не отправляется почта
# {"detail":[{"type":"value_error","loc":["body","email"],"msg":"value is not a valid email address: The email address is not valid. It must have exactly one @-sign.","input":"qwe","ctx":{"reason":"The email address is not valid. It must have exactly one @-sign."}}]}


# придумать тест-кейсы для реги, авторизации и функционала витрины
#рега
# 1. регистрация пользака
# 2. активация пользака
# 3. забыли пароль - отправка письма
# 4. забыли пароль - переход по ссылке из письма и ввод нового пароля
# 5. авторизация пост запрос
# 6. кнопка выход

# витрина
# 1. Проверить, что на главной отображаются все товары из каталога
# 2. проверить что при нажатии на группу выводятся товары из этой группы
# 3. Проверить добавление товара в корзину, что товар добавился. Тут есть связь с пользаком, заморочка
# 4. Проверить что корзина отображается по нужному пользаку
# 5. Проверить удаление из корзины
# 6. Проверить пост запрос для оформления заказа
# 7. Проверить что список заказов отображается по нужному пользаку
# 8. Проверить роутер для получения заказов это гет запрос
# 9. Проверить получения товаров из учетной системы
# 10. Проверить получения групп товаров из учетной системы
# 11. Проверить смену статуса заказов при синхронизации с учетной системой



# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/operations", params={
#         "operation_type": "Выплата купонов",
#     })

#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1


