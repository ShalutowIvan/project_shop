import pytest
from conftest import client, async_session_maker_test, override_get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from src.regusers.models import *
# from sqlalchemy import insert, select

from src.regusers.secure import send_email_verify, send_email_restore_password


from httpx import AsyncClient
from contextlib import nullcontext as not_raise
# async def test_
#райс из smtplib
from smtplib import SMTPRecipientsRefused

from src.settings import KEY4





#функция тестирования авторизации, для отправки данных формы нужно писать data вместо json. пока синхронная
# def test_reg():
# 	response = client.post("/regusers/registration", data={
# 		"name": "Василий Петрович",
# 		"email": "почта яндекса",
# 		"password1": "Qwer1234",
# 		"password2": "Qwer1234"
# 		})

# 	assert response.status_code == 200

#асинхронный вариант функции регистрации
# @pytest.mark.parametrize(
#     "name, email, password1, password2, status_code", [
#     ("Василий Петрович", "ivanshalutov@yandex.ru", "Qwer1234", "Qwer1234", 303),
#     ("Василий Петрович", "asd@asd", "Qwer1234", "Qwer1234", 422),#валидация идет с пайдантиком, и он выдает такой статус код 422. Надо подумать на счет валидации почты. Причем если убрать валидаци пайдантика, то регается с кривой почтой
#     ("", "", "", "", 200),
#     ("Василий Петрович", "asd", "Qwer1234", "Qwer1234", 422),
#     ])
# async def test_registration(name, email, password1, password2, status_code, ac: AsyncClient):
#     response = await ac.post("/regusers/registration", data={
#         "name": name,
# 		"email": email,
# 		"password1": password1,
# 		"password2": password2
#     })

#     assert response.status_code == status_code


#косячный тест функции для кнопки забыли пароль
# @pytest.mark.parametrize(
#     "email, error", [
#     ("ivanshalutov@yandex.ru", not_raise()),
#     ("asd", pytest.raises(SMTPRecipientsRefused)),
#     # ("", "", "", "", 200),
#     ])
# async def test_forgot_pass(email, error, ac: AsyncClient):
#     # response = await ac.post("/regusers/registration", data={
# 	# 	"email": email
#     # })
#     with error:
#         await ac.post("/regusers/forgot_password/", data={
#             "email": email
#         })


#тест функции для кнопки забыли пароль для отправки ссылки для смены пароля
# @pytest.mark.parametrize(
#     "email, status_code", [
#     ("ivanshalutov@yandex.ru", 303),
#     ("asd", 422),
#     ("asd@asd", 422),    
#     ])
# async def test_forgot_pass(email, status_code, ac: AsyncClient):
#     response = await ac.post("/regusers/forgot_password/", data={
# 		"email": email
#     })
#     assert response.status_code == status_code


#второй вариант функции для забыли пароль
@pytest.mark.parametrize(
    "email, status_code", [
    ("ivanshalutov@yandex.ru", 303),
    ("asd", 422),
    ("asd@asd", 422),    
    ])
async def test_forgot_pass(email, status_code, ac: AsyncClient):
    response = await ac.post("/regusers/forgot_password/", data={
      "email": email
    })
    assert response.status_code == status_code

    user = await session.scalar(select(User).where(User.email == email))
    # content = await send_email_restore_password(user=user)
    
    assert user != None


#тест сссылки из письма
@pytest.mark.parametrize(
    "password1, password2, token, status_code", [
    ("Qwer1234", "Qwer1234", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.D-PUbaFp3o2DYcFpPBVX67syyOoRjKZFAeskKOh5hog", 200),
    ("Qwer123", "Qwer1234", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.D-PUbaFp3o2DYcFpPBVX67syyOoRjKZFAeskKOh5hog", 200),
    ("Qwer1234", "Qwer1234", "asd", 200),
    ])
async def test_forgot_pass2(password1, password2, token, status_code, ac: AsyncClient, session: AsyncSession = Depends(override_get_async_session)):
    response = await ac.post("/regusers/restore/password_user/", data={
		"password1": password1,
        "password2": password2,
        "token": token,
    })

    user = await session.scalar(select(User).where(User.email == email))
    # content = await send_email_restore_password(user=user)
    assert user != None

    assert response.status_code == status_code

#если все хорошо код 303
#не смог пока сделать сквозной тест. 

# http://127.0.0.1:8000/regusers/restore/password_user/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIn0.YHdgGr55E24SsH4YsaAmOos6VDhIrL3mYF6LQ_SFGMM




# там разные урл и нужно сначала на одну потом на другую прыгнуть

#при некорректном емейл не отправляется почта
# {"detail":[{"type":"value_error","loc":["body","email"],"msg":"value is not a valid email address: The email address is not valid. It must have exactly one @-sign.","input":"qwe","ctx":{"reason":"The email address is not valid. It must have exactly one @-sign."}}]}


# придумать тест-кейсы для реги, авторизации и функционала витрины
#рега
# 1. регистрация пользака - сделал
# 2. активация пользака - не нужно
# 3. забыли пароль - отправка письма - сделал
# 4. забыли пароль - переход по ссылке из письма и ввод нового пароля - тут скорее всего нужен сквозной тест через несколько роутеров, так как не указывается в это роутере пользак для смены пароля, и он указывается в другом роутере
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


