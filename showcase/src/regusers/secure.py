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










# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



