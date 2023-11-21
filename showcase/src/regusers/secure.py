import uuid
from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_400_BAD_REQUEST

from .models import User, Token
from .schemas import UserCreate



from fastapi.security import APIKeyHeader, APIKeyCookie, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.settings import KEY, KEY2, ALG, EXPIRE_TIME, EXPIRE_TIME_REFRESH
from datetime import datetime, timedelta
from jose.exceptions import ExpiredSignatureError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# apikey_scheme = APIKeyHeader(name="Authorization")
#пока через хедер сделаю, потом переделать на куки. Хедер даже не юзаю пока

apikey_scheme = APIKeyCookie(name="Authorization")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")#это проверка токена на валидность



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
	
	try:
		payload = jwt.decode(RT, KEY2, algorithms=[ALG])
		pl = payload.get("sub")

	except Exception as ex:#если истек рефреш то его просто удаляем, и нужно заново логиниться
		
		if type(ex) == ExpiredSignatureError:
			us_token: Token = await db.scalar(select(Token).where(Token.refresh_token == RT))
			if us_token:
				await db.delete(us_token)
				await db.commit()
		
		return False, False

    #создаем новый рефреш и аксес. Данные для создания токенов берем из декодированного токена из пейлоада
    # user: User =  await session.scalar(select(User).where(User.email == email))
    #рефреш токен
	refresh_token_expires = timedelta(minutes=int(EXPIRE_TIME_REFRESH))    
	refresh_token_jwt = create_refresh_token(data={"sub": pl, "iss": "showcase"}, expires_delta=refresh_token_expires)

	#аксес токен
	access_token_expires = timedelta(minutes=int(EXPIRE_TIME))
	access_token_jwt = create_access_token(data={"sub": pl[1], "iss": "showcase"}, expires_delta=access_token_expires)

	#обновляем рефреш в базе
	us_token: Token = await db.scalar(select(Token).where(Token.refresh_token == RT))
	new_RT: Token = Token(user_id=pl[0], refresh_token=refresh_token_jwt)#для создания объекта нужен Ид пользака
	await db.delete(us_token)
	db.add(new_RT)
	await db.commit()
	await db.refresh(new_RT)

	return [refresh_token_jwt, access_token_jwt]











# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



