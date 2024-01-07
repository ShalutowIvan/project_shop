import uuid
from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_400_BAD_REQUEST

from .models import User, Token
from .schemas import UserCreate, MailBody

from fastapi.security import APIKeyHeader, APIKeyCookie, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.settings import KEY, KEY2, ALG, EXPIRE_TIME, EXPIRE_TIME_REFRESH, KEY3
from datetime import datetime, timedelta
from jose.exceptions import ExpiredSignatureError

#импорты для отправки почты
from src.settings import PORT, HOST, HOST_USER, HOST_PASSWORD, DEFAULT_EMAIL
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# apikey_scheme = APIKeyCookie(name="Authorization")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")#это проверка токена на валидность


#статья про jwt на хабре
# https://habr.com/ru/articles/340146/
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:#если задано время истекания токена, то к текущему времени мы добавляем время истекания
        expire = datetime.utcnow() + expires_delta
    #expires_delta это если делать какую-то
    else:#иначе задаем время истекания также 30 мин
        expire = datetime.utcnow() + timedelta(minutes=int(EXPIRE_TIME))#протестить длительность токена с 0 минут
    to_encode.update({"exp": expire})#тут мы добавили элемент в словарь который скопировали выше элемент с ключом "exp" и значением времени, которое сделали строкой выше. 
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALG)#тут мы кодируем наш токен.
    return encoded_jwt



def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:#если задано время истекания токена, то к текущему времени мы добавляем время истекания
        expire = datetime.utcnow() + expires_delta
    #expires_delta это если делать какую-то
    else:#иначе задаем время истекания также 30 мин
        expire = datetime.utcnow() + timedelta(minutes=int(EXPIRE_TIME_REFRESH))#протестить длительность токена с 0 минут
    to_encode.update({"exp": expire})#тут мы добавили элемент в словарь который скопировали выше элемент с ключом "exp" и значением времени, которое сделали строкой выше. 
    encoded_jwt = jwt.encode(to_encode, KEY2, algorithm=ALG)#тут мы кодируем наш токен.
    return encoded_jwt



async def update_tokens(RT, db):#передаем сюда рефреш токен и сессию с ДБ
	#расшифровка рефреш токена
	try:
		payload = jwt.decode(RT, KEY2, algorithms=[ALG])
		pl_id = payload.get("sub")
		pl_email = payload.get("iss")

	except Exception as ex:#если истек рефреш то его просто удаляем, и нужно заново логиниться
		print("ОШИБКА ОБНОВЛЕНИЯ ТУТ!!!!!!!!!")
		print(ex)
		if type(ex) == ExpiredSignatureError:
			us_token: Token = await db.scalar(select(Token).where(Token.refresh_token == RT))
			if us_token:
				await db.delete(us_token)
				await db.commit()
		
		return False, False

    #создаем новый рефреш и аксес. Данные для создания токенов берем из декодированного токена из пейлоада
        
    #проверка совпадает ли токен из кук с базой для безопасности, в случае если злоумышленник обновил уже токен, а мы нет, то все токены должны удалиться
	RT_in_db: Token = await db.scalar(select(Token).where(Token.refresh_token == RT))#ищем рефреш в ДБ по токену из кук
	if not RT_in_db:
		tk: Token = await db.scalar(select(Token).where(Token.user_id == int(pl_id)))#ищем токен по пользаку и удаляем его
		await db.delete(tk)
		await db.commit()
		await db.refresh(tk)
		print("Токен не совпадает с базой!!!!!!!")
		return False, False

	#рефреш токен
	refresh_token_expires = timedelta(minutes=int(EXPIRE_TIME_REFRESH))    
	refresh_token_jwt = create_refresh_token(data={"sub": str(pl_id), "iss": pl_email}, expires_delta=refresh_token_expires)

	#аксес токен
	access_token_expires = timedelta(minutes=int(EXPIRE_TIME))
	access_token_jwt = create_access_token(data={"sub": pl_id, "iss": "showcase"}, expires_delta=access_token_expires)

	#обновляем рефреш в базе	
	new_RT: Token = Token(user_id=int(pl_id), refresh_token=refresh_token_jwt)#для создания объекта нужен Ид пользака

	await db.delete(RT_in_db)
	db.add(new_RT)
	await db.commit()
	await db.refresh(new_RT)

	return [refresh_token_jwt, access_token_jwt]








import smtplib
from email.message import EmailMessage
from celery import Celery


#функция из джанго. Скорее всего нужно стандартную функцию юзать для почты smtplib. Возможно отправку почты сделать через селери, это как бы фоновая задача, отдельный процесс от фастапи, как бы второе приложение. И есть фловер, это еще один процесс.
# async def send_email_verify(data: dict|None=None, use_https=False):
# 	msg = MailBody(**data)
#     message = MIMEText(msg.body, "html")
#     message["From"] = USERNAME
#     message["To"] = ",".join(msg.to)
#     message["Subject"] = msg.subject

#     ctx = create_default_context()

#     try:
#         with SMTP(HOST, PORT) as server:
#             server.ehlo()
#             server.starttls(context=ctx)
#             server.ehlo()
#             server.login(USERNAME, PASSWORD)
#             server.send_message(message)
#             server.quit()
#         return {"status": 200, "errors": None}
#     except Exception as e:
#         return {"status": 500, "errors": e}


async def send_email_verify(user, use_https=False):
	email = EmailMessage()
	email['Subject'] = 'Подтверждение регистрации в интернет магазине'
	email['From'] = HOST_USER
	email['To'] = user.email

	http = "http" if use_https == False else "https"	 

	token = jwt.encode({"sub": str(user.id)}, KEY3, algorithm=ALG)
	# to_encode = str(user.id)
	# token = pwd_context.hash(to_encode)

	#параметры из ссылки пойдут при запуске функции activate_user
	email.set_content(f"<a href={http}://127.0.0.1:8000/regusers/verification/check_user/{token}><h1>ССЫЛКА</h1></a>" , subtype='html')
    
    #в token передается параметр через слеш и считается второй ссылкой и не работает


    #в этой функции нужно зашифровать пользака и потом дешифровать. Все это прокинуть в ссылке. В джанго там еще шифруется что-то. Можно подсмотреть там
    

	with smtplib.SMTP_SSL(HOST, PORT) as server:
		server.login(HOST_USER, HOST_PASSWORD)
		server.send_message(email)

    # return email



# '<h1>Здравствуйте</h1><h5>Перейдите по ссылке чтобы закончить регистрацию</h5>'
# f"<a href="{{ protocol }}://{{ domain }}{% url 'regusers:activate_user' uidb64=uid token=token %}"><h1>ССЫЛКА</h1></a>"
# f"<a href="{{ protocol }}://127.0.0.1:8000/{{ urlfor 'activate_user' }}"><h1>ССЫЛКА</h1></a>"
# протокол прокинем через условие
# домен как сделать в ссылке?
# в урл не понятно зачем пишется uid и token



    
    # current_site = get_current_site(request)
    # context = {
    # 'user': user,
    # 'domain': current_site.domain,
    # "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    # "token": token_generator.make_token(user),
    # 'protocol': 'https' if use_https else 'http',
    # }

    # html_body = render_to_string('regusers/user_active.html', context=context,)
    # msg = EmailMultiAlternatives(subject='Активация', to=[user.email,],)
    # msg.attach_alternative(html_body, "text/html")
    # msg.send()


#########################
# email = EmailMessage()
#     email['Subject'] = 'Натрейдил Отчет Дашборд'
#     email['From'] = SMTP_USER
#     email['To'] = SMTP_USER

#     email.set_content(
#         '<div>'
#         f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊</h1>'
#         '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
#         '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
#         '-mobile-free-vector.jpg" width="600">'
#         '</div>',
#         subtype='html'
#     )
#     return email


# @celery.task
# def send_email_report_dashboard(username: str):
#     email = get_email_template_dashboard(username)
#     with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.send_message(email)





#понять где писать функцию отправки почты и что в нее передавать контекст html и тд
# background_tasks - фоновая задача, сам объект фоновой задачи принимает в себя функцию и параметры для нее. Выполняется в фоне