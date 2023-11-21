from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status, Cookie, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from sqlalchemy import insert, select
from pydantic import BaseModel, Field, EmailStr, validator, UUID4

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings import templates, EXPIRE_TIME, KEY, KEY2, ALG, EXPIRE_TIME_REFRESH

from .models import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# OAuth2PasswordRequestForm - это форма для авторизации из фастапи

from .schemas import *

from .secure import pwd_context, create_access_token, apikey_scheme, create_refresh_token, update_tokens

import uuid

from jose import JWTError, jwt

from datetime import datetime, timedelta

from jose.exceptions import ExpiredSignatureError

from pydantic import EmailStr


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




# https://www.youtube.com/watch?v=RHWqTpNvJQw&list=PL2nrINOQYLiX6U8ArGi6Kvs_iItdWCYUi&index=1&ab_channel=%D0%93%D0%BB%D0%B5%D0%B1%D0%A2%D1%83%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2




@router_reg.get("/auth", response_model=None, response_class=HTMLResponse)
async def auth_get(request: Request):
    return templates.TemplateResponse("regusers/test2.html", {"request": request})

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
    

    if not refresh_token:
        #рефреш токен
        refresh_token_expires = timedelta(minutes=int(EXPIRE_TIME_REFRESH))
        # user_str = str(user.id)
        refresh_token_jwt = create_refresh_token(data={"sub": [user.id, user.email], "iss": "showcase"}, expires_delta=refresh_token_expires)

        #аксес токен
        access_token_expires = timedelta(minutes=int(EXPIRE_TIME))
        # user_str = str(user.id)
        access_token_jwt = create_access_token(data={"sub": user.email, "iss": "showcase"}, expires_delta=access_token_expires)

        #тут нужно прокинуть хедер Sec-Ch-Ua: в нем инфа о браузере через который зашли

        # access_token_expires = timedelta(minutes=int(EXPIRE_TIME))
        # access_token_jwt = create_access_token(data={"sub": user.email, "iss": "showcase"}, expires_delta=access_token_expires)

        token: Token = Token(user_id=user.id, refresh_token=refresh_token_jwt)
        session.add(token)       
        await session.commit()
        await session.refresh(token)
        refresh_token: Token = await session.scalar(select(Token).where(Token.user_id == user.id))
    # elif 

    
    
    #тут где то наверно сделать рефреш токена
    
    response = templates.TemplateResponse("regusers/test2.html", {"request": request})
    # response = JSONResponse(content={"message": "куки установлены"})
    response.set_cookie(key="RT", value=refresh_token.refresh_token)
    response.set_cookie(key="Authorization", value=access_token_jwt)
   
    return response
    # return {"access_token": access_token_jwt, "token_type": "bearer"}#возвращаем токен, и тип токена. Так нужно, чтобы можно было обращаться к токену



@router_reg.get("/logout")
async def logout_user(request: Request, response: Response, Authorization: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):
    response = templates.TemplateResponse("regusers/test2.html", {"request": request})
    
    if Authorization != None:
        us_token: Token = await session.scalar(select(Token).where(Token.refresh_token == Authorization))
        await session.delete(us_token)
        await session.commit()

    # response = templates.TemplateResponse("login.html", {"request": request, "title": "Login", "current_user": AnonymousUser()})
    # response.set_cookie(key="Authorization",
    #     value="",
    #     )
    response.delete_cookie("Authorization")


    # print(response)
    # return {"message": "Hello METANIT.COM"}
    return response
    # return RedirectResponse("", status_code=303)
    # return {"Authorization": "1", "token_type": "bearer"}
 



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name=apikey_scheme)


#функция проверки токена. Проверить эту функцию до конца, првоерить сессию...
# async def get_current_user_from_token(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_async_session)):

async def get_current_user_from_token(acces_token):#проверка аксес токена из куки  
    
    try:
        payload = jwt.decode(acces_token, KEY, algorithms=[ALG])#в acces_token передается просто строка
        
        email = payload.get("sub")#у меня тут почта, а не юзернейм
        if email is None:
            print("нет такого email")
            return False
            # raise credentials_exception
    # except JWTError:
    except Exception as ex:
        # us_token: Token = await db.scalar(select(Token).where(Token.acces_token == acces_token))
        
        if type(ex) == ExpiredSignatureError:#если время действия токена истекло, то вывод принта. Можно тут написать логику что будет если аксес токен истекает
            # us_token: Token = await db.scalar(select(Token).where(Token.refresh_token == acces_token))
            # if us_token:
            #     await db.delete(us_token)
            #     await db.commit()#удаляем из ДБ чтобы при создании нового не было дублей токенов
            # return
            # tokens = update_tokens(RT=RT, db=db)#тут возвращается кортеж из двух токенов
            print("ОШИБКА ТУТ")
            print(ex)
            return ex

        # тут нужно сделать обновление, юзнуть нашу функцию 



        return False
        # raise credentials_exception
    # token: Token = await db.scalar(select(Token).where(Token.email == email))#тут поиск пользователя по его почте - логину. Проверка что в токене не левая почта. тут нуэна другая проверка, на какой нибудь хедер
    # if token is None:
    #     print("нет пользака")
    #     return False
    #     # raise credentials_exception

    return True









# https://habr.com/ru/companies/doubletapp/articles/764424/

#сделал, работает и время само по себе валидируется, если срок истекает, то пишет ошибку. !!!!!!!!!!!!!
#нужно еще сделать обновление токена в базе. А то он там не удаляется и постоянно висит если уже один раз вошли. И получается jwt не обновляется. Нужно чтобы обновлялся токен в базе. 



# ###########################################################
# #функция поиска записи юзера в таблице токенов по токену. Находится запись по токену, в ней есть инфа о пользователе которому принадлежит токен и возвращаем юзера владеющего токеном или иначе исключение. Обратиться в пользователю мы можем из-за того что есть relationship в модели, то есть ссылка на юзера, очень удобно. Скорее всего это надо сделать роутером или как то юзать в html-ках для првоерки авторизации. Также нужно сделать jwt токен вместо обычного uuid, и сделать ему время жизни
# async def get_user_by_token(acces_token: str, session: AsyncSession = Depends(get_async_session)):
#     token = await session.scalar(select(Token).where(Token.acces_token == acces_token))
#     if token:
#         return { "id": token.user.id, "email": token.user.email }
#         # return True
#     else:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="UNAUTHORIZED"
#         )
# ############################################################





# #функция проверки токена из кук. Пока роуты без схем, нужно сделать со схемами пайдентика
@router_reg.get("/self", response_model=None)
async def test_token(RT: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):
    
    # Authorization: str | None = Cookie(default=None), 
    # check = await get_current_user_from_token(acces_token=Authorization, db=session)
    return RT
    


#Нужно юзать в шаблоне функцию не test_token, а get_current_user_from_token, и прокидывать результат этой функции в контекст.


# @router_reg.get("/self", response_model=None)
# async def test_token(Authorization = Cookie()):
#     return  Authorization

# str | None = Cookie(default=None)


# пользак у меня уже регается, и записывается в базу. Потом когда авторизуется, ему я кидаю токен в куки и записываю в базу этот же токен. Есть кнопка "выйти", она уда










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
