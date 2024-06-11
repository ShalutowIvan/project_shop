import pytest
from fastapi import Depends
from conftest import client, async_session_maker_test
from sqlalchemy.ext.asyncio import AsyncSession


from src.regusers.models import *
from sqlalchemy import insert, select

from src.regusers.secure import send_email_verify, send_email_restore_password


from httpx import AsyncClient
from contextlib import nullcontext as not_raise

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
# @pytest.mark.parametrize(
#     "email, status_code", [
#     ("ivanshalutov@yandex.ru", 303),
#     ("asd", 422),
#     ("asd@asd", 422),    
#     ])
# async def test_forgot_pass(email, status_code, ac: AsyncClient):
#     response = await ac.post("/regusers/forgot_password/", data={
#       "email": email
#     })
#     assert response.status_code == status_code

#     user = await session.scalar(select(User).where(User.email == email))
#     # content = await send_email_restore_password(user=user)
    
#     assert user != None


#тест сссылки из письма. Проверяются ошибки при вводе пароля и зарегался ли юзер
# @pytest.mark.parametrize(
#     "password1, password2, email, status_code", [
#     ("Qwer1234", "Qwer1234", "ivanshalutov@yandex.ru", 303),
#     ("Qwer123", "Qwer1234", "ivanshalutov@yandex.ru", 200),
#     ("Qwer", "Qwer", "ivanshalutov@yandex.ru", 200),
#     ])
# async def test_forgot_pass2(password1, password2, email, status_code, ac: AsyncClient, ):
#     async with async_session_maker_test() as session:
#
#         user = await session.scalar(select(User).where(User.email == email))
#         # user = await session.execute(select(User).where(User.email == email))
#
#         content = await send_email_restore_password(user=user)
#         begin = content.find("password_user/")
#         end = content.find("><h1>")
#         slice_token = content[begin + 14:end]
#
#         # payload = jwt.decode(slice_token, KEY4, algorithms=[ALG])
#         # assert payload.get("sub") == user.id
#
#         response = await ac.post("/regusers/restore/password_user/", data={
#             "password1": password1,
#             "password2": password2,
#             "token": slice_token,
#         })
#
#         assert user != None
#         assert response.status_code == status_code

#Depends в тестах не работают, приходится просто открывать соединение

#тест авторизации. Неверный пароль, верный пароль, неверно введена почта, незареганная почта
# @pytest.mark.parametrize(
#     "email, password, status_code",
#     [
#         ("ivanshalutov@yandex.ru", "Qwer1234", 200),
#         ("ivanshalutov@yandex.ru", "Qwer1234444", 200),
#         ("ivanshalutov@yandex", "Qwer1234", 422),
#         ("asd@yandex.ru", "Qwer1234", 200)
#     ]
# )
# async def test_auth(email, password, status_code, ac: AsyncClient):
#     response = await ac.post("/regusers/auth", data={
#         "email": email,
#         "password": password,
#     })
#
#     assert response.status_code == status_code


# # @pytest.mark.parametrize(
# #     "status_code",
# #     (200,),
# #     (200,),
# # )
# async def test_exit(ac: AsyncClient):
#     response = await ac.get("/regusers/logout")
#
#     assert response.status_code == 200






# придумать тест-кейсы для реги, авторизации и функционала витрины
#рега
# 1. регистрация пользака - сделал
# 2. активация пользака - не нужно
# 3. забыли пароль - отправка письма - сделал
# 4. забыли пароль - сделал
# 5. авторизация пост запрос - сделал
# 6. кнопка выход - сделал



# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/operations", params={
#         "operation_type": "Выплата купонов",
#     })

#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1


