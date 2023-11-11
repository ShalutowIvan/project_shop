import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_400_BAD_REQUEST

from .models import User, Token
from .schemas import UserCreate



from fastapi.security import APIKeyHeader, APIKeyCookie
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.settings import KEY, KEY2, ALG, EXPIRE_TIME
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# apikey_scheme = APIKeyHeader(name="Authorization")
#пока через хедер сделаю, потом переделать на куки. Хедер даже не юзаю пока

apikey_scheme = APIKeyCookie(name="Authorization")



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:#если задано время истекания токена, то к текущему времени мы добавляем время истекания
        expire = datetime.utcnow() + expires_delta
    #expires_delta это если делать какую-то
    else:#иначе задаем время истекания 15 мин
        expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)
    to_encode.update({"exp": expire})#тут мы добавили элемент в словарь который скопировали выше элемент с ключом "exp" и значением времени, которое сделали строкой выше. 
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALG)#тут мы кодируем наш токен.
    return encoded_jwt



# #функция для проверки существования пользователя и присвоением пароля
# def register(db: Session, user_data: UserCreate):
#     if db.scalar(select(User).where(User.email == user_data.email)):
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists!"
#         )
#     user = User(email=user_data.email)
#     user.hashed_password = pwd_context.hash(user_data.password)#тут пароль мы хешируем и сохраняем
#     db.add(user)
#     db.commit()
#     return {
#         "id": user.id,
#         "email": user.email,
#     }




# def create_token(db: Session, user_data: UserCreate):
#     user: User = db.scalar(select(User).where(User.email == user_data.email))
#     if not user:
#         raise HTTPException(
#             status_code=HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )

#     if not pwd_context.verify(user_data.password, user.hashed_password):#функция для сверки пароля с захешированным паролем. скорее всего хеширует и сверяет. 
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     token: Token = Token(user_id=user.id, acces_token=str(uuid.uuid4()))
#     db.add(token)
#     db.commit()
#     return {"acces_token": token.acces_token}




