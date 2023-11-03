from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from sqlalchemy import insert, select

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings import templates

from .models import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# OAuth2PasswordRequestForm - это форма для авторизации из фастапи

from .schemas import *

from .secure import pwd_context

import uuid

#мой роутер
router_reg = APIRouter(
    prefix="",
    tags=["Regusers"]
)

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)



#роутеры для реги


@router_reg.get("/registration")
async def registration_get(request: Request):
    return templates.TemplateResponse("regusers/test.html", {"request": request})

# username: str = Form(...), password: str = Form(...)

#функция из видоса. 
# def reg(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):


# , response_model=UserCreate
@router_reg.post("/registration", status_code=201)#response_model это валидация для запроса
async def registration_post(request: Request, session: AsyncSession = Depends(get_async_session), name: str = Form(), email: str = Form(), password: str = Form()):
    # stmt = await session.execute(select(users))

    user = User(name=name, email=email, hashed_password=pwd_context.hash(password))

    # stmt = insert(users).values(email=email, name=name, password=password)
    # user = stmt.users(email=email, name=name, password=password)
    
    session.add(user)
    await session.commit()


    return RedirectResponse("/auth", status_code=303)

# сделать перезапись пароля в захешированный пароль. То есть берем пароль из формы и юзера создаем, потом хешируем и перезаписываем пароль в базу захешированным. 
#аннотейтед это такие аннотации с типом данных и значениями. В доке по фастапи есть инфа в питоне 3,8 как в метанит, а в питон 3,9 появились Annotated 




@router_reg.get("/auth")
async def auth_get(request: Request):
    return templates.TemplateResponse("regusers/test2.html", {"request": request})

#пока сделал проверку пользователя по вводу логина и пароля и если все верно то создается токен в БД, в токене есть юзер ид пользователя
@router_reg.post("/auth")
async def auth_user(request: Request, session: AsyncSession = Depends(get_async_session), email: str = Form(), password: str = Form()):
    user: User = await session.scalar(select(User).where(User.email == email))#ищем пользователя по емейл
    if not user:#если юзер не нашелся, то генерим исключение
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    if not pwd_context.verify(password, user.hashed_password):#сверка пароля с БД
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    

    token: Token = Token(user_id=user.id, acces_token=str(uuid.uuid4()))
    session.add(token)
    await session.commit()
    # return {"acces_token": token.acces_token}
    return RedirectResponse("/", status_code=303)



###########################################################
#функция поиска записи в таблице токенов по токену. Находится запись по токену, в ней есть инфа о пользователе которому принадлежит токен и возвращаем юзера владеющего токеном или иначе исключение. Обратиться в пользователю мы можем из-за того что есть relationship в модели, то есть ссылка на юзера, очень удобно. Скорее всего это надо сделать роутером или как то юзать в html-ках для првоерки авторизации. Также нужно сделать jwt токен вместо обычного uuid, и сделать ему время жизни
def get_user_by_token(acces_token: str, session: AsyncSession = Depends(get_async_session)):
    token = session.scalar(select(Token).where(Token.access_token == acces_token))
    if token:
        # return { "id": token.user.id, "email": token.user.email }
        return True
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
############################################################








################################################################################
#просто ссылки для перехода на страницу тестовой авторизации. Потом удалить.
@router_reg.get("/registration")
async def url_reg(request: Request):
    pass
    # return RedirectResponse("/auth", status_code=303)


@router_reg.get("/auth")
async def url_auth(request: Request):
    pass
    # return RedirectResponse("", status_code=303)
################################################################################
