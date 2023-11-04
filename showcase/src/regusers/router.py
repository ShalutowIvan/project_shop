from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status, Cookie, Header
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

from .secure import pwd_context, encode_jwt, apikey_scheme

import uuid

from datetime import datetime



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
@router_reg.post("/registration", response_model=None, status_code=201)#response_model это валидация для запроса
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









@router_reg.get("/auth", response_model=None)
async def auth_get(request: Request):
    return templates.TemplateResponse("regusers/test2.html", {"request": request})

#пока сделал проверку пользователя по вводу логина и пароля и если все верно то создается токен в БД, в токене есть юзер ид пользователя
@router_reg.post("/auth", response_model=None)
async def auth_user(request: Request, session: AsyncSession = Depends(get_async_session), email: str = Form(), password: str = Form()):
    user: User = await session.scalar(select(User).where(User.email == email))#ищем пользователя по емейл
    if not user:#если юзер не нашелся, то генерим исключение
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    if not pwd_context.verify(password, user.hashed_password):#сверка пароля с БД
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    
    us_token: Token = await session.scalar(select(Token).where(Token.user_id == user.id))
    if not us_token:
        uid = str(uuid.uuid4())
        token: Token = Token(user_id=user.id, acces_token=uid)
        session.add(token)        
        await session.commit()
        # response = JSONResponse(content={"message": "куки установлены"})
        # response.set_cookie(key="Authorization", value=us_token.acces_token)
        # # return RedirectResponse("/", status_code=303)
        # return response
    
    response = JSONResponse(content={"message": "куки установлены"})
    response.set_cookie(key="Authorization", value=us_token.acces_token)
    
    # return response
    return RedirectResponse("/", status_code=303)
    
    
# async def exit(response: Response,):
@router_reg.get("/logout")
async def exit(request: Request):
    
    response = JSONResponse(content={"message": "куки установлены"})
    # print(response.__dict__)
    # response.set_cookie(key="Authorization", value="")
    response.delete_cookie(key="Authorization")
    # print(response)
    # return {"message": "Hello METANIT.COM"}
    # return RedirectResponse("/")
    return RedirectResponse("/auth", status_code=303)

# def root(secret_code: str | None = Header(default=None)):
#     return {"Secret-Code": secret_code}


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @router.get("/logout")
# async def logout(request: Request, response: Response, current_user: User = Depends(get_current_active_user)):
#     # Also tried following two comment lines
#     # response.set_cookie(key="access_token", value="", max_age=1)
#     # response.delete_cookie("access_token", domain="localhost")
#     response = templates.TemplateResponse("login.html", {"request": request, "title": "Login", "current_user": AnonymousUser()})
#     response.delete_cookie("access_token")
#     return response


# @router_reg.get("/auth/cookie/")
# async def set_cookie(response: Response, user):
#     key = await session.scalar(select(Token).where(User.id == user.id))
#     response.set_cookie(key="Authorization", value=now)

#     # session.coc = "847597ad-ddad-4172-b15a-b62e4fbc3135"
#     return {"message": "куки установлены"}





###########################################################
#функция поиска записи юзера в таблице токенов по токену. Находится запись по токену, в ней есть инфа о пользователе которому принадлежит токен и возвращаем юзера владеющего токеном или иначе исключение. Обратиться в пользователю мы можем из-за того что есть relationship в модели, то есть ссылка на юзера, очень удобно. Скорее всего это надо сделать роутером или как то юзать в html-ках для првоерки авторизации. Также нужно сделать jwt токен вместо обычного uuid, и сделать ему время жизни
async def get_user_by_token(acces_token: str, session: AsyncSession = Depends(get_async_session)):
    token = await session.scalar(select(Token).where(Token.acces_token == acces_token))
    if token:
        return { "id": token.user.id, "email": token.user.email }
        # return True
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
############################################################


#функция проверки токена из кук. Пока роуты без схем, нужно сделать со схемами пайдентика
@router_reg.get("/self", response_model=None)
async def get_user_by_id(acces_token: Annotated[str, Depends(apikey_scheme)], session: AsyncSession = Depends(get_async_session)):
    return await get_user_by_token(acces_token=acces_token, session=session)



















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
