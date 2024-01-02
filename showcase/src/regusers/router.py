from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status, Cookie, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from sqlalchemy import insert, select
from pydantic import BaseModel, Field, EmailStr, validator, UUID4

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings import templates, EXPIRE_TIME, KEY, KEY2, ALG, EXPIRE_TIME_REFRESH

from .models import *
from src.showcase.models import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# OAuth2PasswordRequestForm - это форма для авторизации из фастапи

from .schemas import *

from .secure import pwd_context, create_access_token, create_refresh_token, update_tokens

import uuid

from jose import JWTError, jwt

from datetime import datetime, timedelta

from jose.exceptions import ExpiredSignatureError




#мой роутер
router_reg = APIRouter(
    prefix="/regusers",
    tags=["Regusers"]
)



#роутеры для реги


@router_reg.get("/registration")
async def registration_get(request: Request, session: AsyncSession = Depends(get_async_session)):

    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    response = templates.TemplateResponse("regusers/register.html", context)
    return response

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


    return RedirectResponse("/regusers/auth", status_code=303)


#аннотейтед это такие аннотации с типом данных и значениями. В доке по фастапи есть инфа в питоне 3,8 как в метанит, а в питон 3,9 появились Annotated 




# https://www.youtube.com/watch?v=RHWqTpNvJQw&list=PL2nrINOQYLiX6U8ArGi6Kvs_iItdWCYUi&index=1&ab_channel=%D0%93%D0%BB%D0%B5%D0%B1%D0%A2%D1%83%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2




@router_reg.get("/auth", response_model=None, response_class=HTMLResponse)
async def auth_get(request: Request, session: AsyncSession = Depends(get_async_session)):
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    response = templates.TemplateResponse("regusers/login.html", context)
    return response

#пока сделал проверку пользователя по вводу логина и пароля и если все верно то создается токен в БД, в токене есть юзер ид пользователя
@router_reg.post("/auth", response_model=None, response_class=HTMLResponse)
async def auth_user(response: Response, request: Request, session: AsyncSession = Depends(get_async_session), email: EmailStr = Form(), password: str = Form()):

    user: User = await session.scalar(select(User).where(User.email == email))#ищем пользователя по емейл
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not pwd_context.verify(password, user.hashed_password):#сверка пароля с БД
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    
    refresh_token: Token = await session.scalar(select(Token).where(Token.user_id == user.id))
    
    #тут проверка истек ли рефреш токен
    try:
        payload = jwt.decode(refresh_token.refresh_token, KEY2, algorithms=[ALG])        

    except Exception as ex:#если истек рефреш то его просто удаляем, и нужно заново логиниться
        print("РЕФРЕШ ТОКЕН ИСТЕК")
        print(ex)
        if type(ex) == ExpiredSignatureError:            
            await session.delete(refresh_token)
            await session.commit()
            refresh_token = None


    if not refresh_token:
        #рефреш токен
        refresh_token_expires = timedelta(minutes=int(EXPIRE_TIME_REFRESH))        
        refresh_token_jwt = create_refresh_token(data={"sub": str(user.id), "iss": user.email}, expires_delta=refresh_token_expires)

        #аксес токен
        access_token_expires = timedelta(minutes=int(EXPIRE_TIME))        
        access_token_jwt = create_access_token(data={"sub": str(user.id), "iss": "showcase"}, expires_delta=access_token_expires)
        

        token: Token = Token(user_id=user.id, refresh_token=refresh_token_jwt)
        session.add(token)       
        await session.commit()
        await session.refresh(token)
        refresh_token: Token = await session.scalar(select(Token).where(Token.user_id == user.id))
    else:
        access_token_expires = timedelta(minutes=int(EXPIRE_TIME))
        access_token_jwt = create_access_token(data={"sub": str(user.id), "iss": "showcase"}, expires_delta=access_token_expires)


    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }
    
    response = templates.TemplateResponse("regusers/login.html", context)    
    response.set_cookie(key="RT", value=refresh_token.refresh_token)
    response.set_cookie(key="Authorization", value=access_token_jwt)
   
    return response
    


@router_reg.get("/logout")
async def logout_user(request: Request, response: Response, Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):
    
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    response = templates.TemplateResponse("regusers/login.html", context)
    
    if RT != None:
        us_token: Token = await session.scalar(select(Token).where(Token.refresh_token == RT))
        if us_token:
            await session.delete(us_token)
            await session.commit()
        response.delete_cookie("RT")
        response.delete_cookie("Authorization")

    return response
    

#функция проверки токена.
async def access_token_verify(acces_token):#проверка аксес токена из куки  
    
    try:
        payload = jwt.decode(acces_token, KEY, algorithms=[ALG])#в acces_token передается просто строка
        
        user_id = payload.get("sub")#у меня тут user_id, а не юзернейм
        if user_id is None:
            print("нет такого user_id")
            return False, None
            
    
    except Exception as ex:
                
        if type(ex) == ExpiredSignatureError:#если время действия токена истекло, то вывод принта. Можно тут написать логику что будет если аксес токен истекает
            
            print("ОШИБКА АКСЕС ТУТ")
            print(ex)
            return ex, None

       
        return False, None
        

    return (True, user_id)





# #функция проверки токена из кук. Пока роуты без схем, нужно сделать со схемами пайдентика
@router_reg.get("/self", response_model=None)
async def test_token(request: Request, RT: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):
    
    response = templates.TemplateResponse("regusers/test2.html", {"request": request})
    
    return response
    

    
    




################################################################################
#просто ссылки для перехода на страницу тестовой авторизации. Потом удалить.
# @router_reg.get("/registration")
# async def url_reg(request: Request):
#     pass
#     # return RedirectResponse("/auth", status_code=303)


# @router_reg.get("/auth")
# async def url_auth(request: Request):
#     pass
    # return RedirectResponse("", status_code=303)
################################################################################


# <a href="{{ url_for('url_reg') }}"><h1>РЕГА</h1></a>
#     <br>    
#     <a href="{{ url_for('url_auth') }}"><h1>АУТХ</h1></a>
#     <br>
#     <a href="{{ url_for('test_token') }}"><h1>Проверка токена</h1></a>


