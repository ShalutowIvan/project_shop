from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, Form, Body, Header, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from sqlalchemy import insert, select, text
from sqlalchemy.orm import joinedload

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .schemas import *
from src.regusers.models import User
from src.regusers.secure import test_token_expire, access_token_decode

from jose.exceptions import ExpiredSignatureError

import requests

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
from src.settings import templates, EXPIRE_TIME, KEY, KEY2, ALG, EXPIRE_TIME_REFRESH, KEY3, KEY4


router_showcase_api = APIRouter(
    prefix="/api",
    tags=["Showcase_api"]
)



async def base_requisites(db, request, check=[False, None, " "]):#db - сессия, check - результат дешифровки аксес токена, request - Request
    org = await db.execute(select(Organization))  
    group = await db.execute(select(Group))    

    if check[1] != None and check[1] != False:       
        # query = select(User).where(User.id == int(check[1]))   
        # user = await db.scalars(query)                
        # user_name = user.all()[0].name
        user_name = check[2]
    else:
        user_name = ""

    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": group.scalars(),    
    "check": check[0],
    "user_name": user_name,
    }

    return context



@router_showcase_api.get("/groups_all/", response_model=list[GroupShema])
async def groups_all(request: Request, session: AsyncSession = Depends(get_async_session)) -> GroupShema:
    query = select(Group)
    group = await session.scalars(query)
    
    # group = await session.execute(select(Group))
    
    # context = group.scalars()

    return group






#главное сделать response_model=list[GoodsShema] в декораторе, тогда ответ из дб будет конвертироваться в JSON и приниматься на фронте
@router_showcase_api.get("/goods_all/", response_model=list[GoodsShema])
async def goods_all(request: Request, session: AsyncSession = Depends(get_async_session)) -> GoodsShema:
	
	good = await session.execute(select(Goods))
	
	context = good.scalars()
	return context



@router_showcase_api.get("/goods_in_group/{slug}", response_model=list[GoodsShema])
async def goods_in_group(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)) -> GoodsShema:	
    
    query = select(Goods).options(joinedload(Goods.group))
    good_gr = await session.scalars(query)
    if slug == "0":
        good_gr = list(good_gr)
    else:
        good_gr = list(filter(lambda x: x.group.slug == slug, good_gr))


    return good_gr




# ост тут, решил делать фронт для витрины

@router_showcase_api.get("/basket/{good_id}")
async def api_add_in_basket(request: Request, good_id: int, session: AsyncSession = Depends(get_async_session)):
    #подтянул ид пользака из токена
    # check = await access_token_decode(acces_token=Authorization)
    
    # if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
    #     context = await base_requisites(db=session, check=check, request=request)

    #     return templates.TemplateResponse("showcase/if_not_auth.html", context)

    # try:
    #     good_id = int(good_id)
    # except Exception as ex:
    #     context = await base_requisites(db=session, check=check, request=request)
    #     return templates.TemplateResponse("showcase/if_goods_none.html", context)

    fake_user_id = 1
    good_id = int(good_id)

    good = await session.get(Goods, good_id)
    # if good is None:
    #     context = await base_requisites(db=session, check=check, request=request)
    #     return templates.TemplateResponse("showcase/if_goods_none.html", context)

    query = select(Basket).where(Basket.product_id == good_id, Basket.user_id == fake_user_id)

    basket = await session.scalars(query)
    basket = basket.all()

    if basket == []:#если в корзине нет такого товара, то добавляет товар в корзину
        product = Basket(product_id=good_id, quantity=1, user_id=fake_user_id)
        session.add(product)
        await session.commit()
    else:
        basket[0].quantity += 1
        await session.commit()

    return {"Все": "Супер"}


# Authorization: Annotated[str | None, Header()] = None
from typing import Annotated


# def get_header_value(request: Request) -> str:
#     header_value = request.headers.get("Authorization")
#     if header_value is None:
#         raise HTTPException(status_code=400, detail="Header not found")
#     return header_value

# Authorization: str = Depends(get_header_value), 

######################################### тут решение по ответу GPT
from jose import JWTError, jwt

from src.regusers.schemas import UserSheme


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/regusers/auth")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALG])
        user_id = payload.get("sub")
        # user_name: str = payload.get("user_name")
        
        if user_id is None:
            print("!!!!!!!!!!!!!!!!!!")    
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
    # except JWTError:
    except Exception as ex:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(ex)
        # Not enough segments тут такая ошибка
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(user_id)
    return user_id

 # = Depends(oauth2_scheme)
# Зависимость для получения текущего пользователя
async def get_current_user(session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    # user = fake_users_db.get(username)
    user = await session.scalar(select(User).where(User.id == int(user_id)))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(user)
    if user is None:
        print("!!!!!!!!!!!!!!!!!!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return UserSheme(**user)



########################################
# current_user: User = Depends(get_current_user)

# UserSheme = Depends(get_current_user),
# Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None),
@router_showcase_api.get("/basket/goods/", response_model=list[BasketShema])
async def api_basket_view(request: Request, current_user: UserSheme = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):

    # check = await access_token_decode(acces_token=request.headers.Authorization)
    
    # if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
    #     # context = await base_requisites(db=session, check=check, request=request)
        # return templates.TemplateResponse("showcase/if_not_auth.html", context)
        # return {"Все плохо": "Нет авторизации"}

    # flag = False
    # if type(check[0]) == ExpiredSignatureError:   
    #     tokens = await test_token_expire(RT=RT, db=session)        
    #     check = tokens[2]
    #     flag = True
    # user_id = await decode_token(token=Authorization)
    # # user = get_current_user(db=session, token=Authorization)
    # user = await session.scalar(select(User).where(User.id == user_id))
    # fake_user_id = check[1]
    # user = user.first()
    print("!!!!!!!!!!!!!!!!!!!!!!!")
    print(current_user)
    fake_user_id = current_user.id


    query = select(Basket).options(joinedload(Basket.product)).where(Basket.user_id == fake_user_id)
    basket = await session.scalars(query)    
    #тут в basket выгружается запрос со связанным полем. в Pydentic схеме просто сделал валидацию, что поле product соответствует GoodsShema, и все норм сериализуется в React, и там можно спокойно обращаться к связанному полю.



    # context = await base_requisites(db=session, check=check, request=request)
    # context["basket"] = basket

    # response = templates.TemplateResponse("showcase/basket.html", context)

    # if flag:
    #     response.set_cookie(key="RT", value=tokens[0])
    #     response.set_cookie(key="Authorization", value=tokens[1])

    # return response
    return basket



@router_showcase_api.get("/basket/goods/delete/{basket_id}")
async def api_delete_in_basket(request: Request, basket_id: int, session: AsyncSession = Depends(get_async_session)):
    
    
    # if not basket_id.isdigit():#решил сделать так вместо анотации типа в роутере
    #     context = await base_requisites(db=session, request=request)
    #     return templates.TemplateResponse("showcase/if_goods_none.html", context)

    # good = await session.get(Goods, basket_id)#basket_id не совпадает с id из списка товаров
    # if good is None:
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!")
    #     context = await base_requisites(db=session, request=request)
    #     return templates.TemplateResponse("showcase/if_goods_none.html", context)


    basket = await session.get(Basket, basket_id)

    # if basket is None:
    #     context = await base_requisites(db=session, request=request)
    #     return templates.TemplateResponse("showcase/if_goods_none.html", context)

    await session.delete(basket)
    await session.commit()    
    
    # return RedirectResponse("/basket/goods/")
    return {"Все": "Супер"}



# @router_showcase_api.post("/basket/contacts/", response_model=None)#response_model это валидация для запроса
# async def api_contacts_form(request: Request, session: AsyncSession = Depends(get_async_session), fio: str = Form(), phone: str = Form(), delivery_address: str = Form(), pay: str = Form()):
    
#     # try:  # тут передалать так, чтобы в html формы выводились ошибки, то есть прокидывался контекст с ошибкой в форму, как это сделано в реге. Пока просто кидаю ошибку в html форме
#     #     tel = int(phone)
#     #     p = int(pay)
#     #     if p not in (1, 2):
#     #         raise Exception("Неверный способ оплаты")
#     # except Exception as ex:

#         # context = await base_requisites(db=session, check=check, request=request)
#         # context["error"] = ex
#         # response = templates.TemplateResponse("showcase/contacts.html", context)
#         # if flag:
#         #     response.set_cookie(key="RT", value=tokens[0])
#         #     response.set_cookie(key="Authorization", value=tokens[1])
#         # return response


#     fake_user_id = 1

#     #создаем объект в таблице счетчика заказов
#     order_counter = Order_counter(user_id=fake_user_id)

#     session.add(order_counter)
#     await session.commit()
#     await session.refresh(order_counter)

#     #делаем запрос в таблице корзина с фильтром по пользаку
#     pay_goods = await session.scalars(select(Basket).where(Basket.user_id == fake_user_id))
#     #запрос в таблице счетчика заказов по пользаку
#     order_number = await session.scalars(select(Order_counter).where(Order_counter.user_id == fake_user_id))
#     id_order_number = order_number.all()[-1].id#берем последний в списке номер, это будет номер заказа, таблицу контактов запрашиваю для указания номера заказа
#     #формируем генератор списка товаров из корзины
#     res = [Order_list(order_number=id_order_number, fio=fio, delivery_address=delivery_address, phone=phone, product_id=i.product_id, quantity=i.quantity, user_id=fake_user_id, state_order="not_received") for i in pay_goods.all()]
            
#     session.add_all(res)

#     #удаление всех записей в корзине с фильтром по пользаку
#     await session.execute(text(f"DELETE FROM basket WHERE user_id = {fake_user_id};"))  
    
#     await session.commit()

#     # context = await base_requisites(db=session, check=check, request=request)

#     # context["order_number"] = id_order_number
#     # response = templates.TemplateResponse("showcase/order_done.html", context)

#     # if flag:        
#     #     response.set_cookie(key="RT", value=tokens[0])
#     #     response.set_cookie(key="Authorization", value=tokens[1])
        

#     # return RedirectResponse("/basket/contacts/checkout/", status_code=303)
#     # return RedirectResponse("/", status_code=303)#после оформления переходим на стартовую
#     # return response

#     return {"Все": "Супер"}


#роутер для оформления заказа
@router_showcase_api.post("/basket/contacts/")
async def api_contacts_form(request: Request, formData: Order_list_form_Shema, session: AsyncSession = Depends(get_async_session)):
    
    fake_user_id = 1

    #создаем объект в таблице счетчика заказов
    order_counter = Order_counter(user_id=fake_user_id)

    session.add(order_counter)
    await session.commit()
    await session.refresh(order_counter)

    #делаем запрос в таблице корзина с фильтром по пользаку
    pay_goods = await session.scalars(select(Basket).where(Basket.user_id == fake_user_id))
    #запрос в таблице счетчика заказов по пользаку
    order_number = await session.scalars(select(Order_counter).where(Order_counter.user_id == fake_user_id))
    id_order_number = order_number.all()[-1].id#берем последний в списке номер, это будет номер заказа, таблицу контактов запрашиваю для указания номера заказа
    #формируем генератор списка товаров из корзины
    res = [Order_list(order_number=id_order_number, fio=formData.fio, delivery_address=formData.delivery_address, phone=formData.phone, product_id=i.product_id, quantity=i.quantity, user_id=fake_user_id, state_order="not_received") for i in pay_goods.all()]

            
    session.add_all(res)

    #удаление всех записей в корзине с фильтром по пользаку
    await session.execute(text(f"DELETE FROM basket WHERE user_id = {fake_user_id};"))  
    
    await session.commit()
      
    return {"Все": "Супер"}


#для отображения списка покупок (заказов созданных покупателем)
@router_showcase_api.get("/checkout_list/orders/", response_model=list[Order_counterShema])
async def checkout_number_view(request: Request, session: AsyncSession = Depends(get_async_session)):
    # сделать не списком с номером и списков покупок, а список заказов по номерам, и возможность открыть каждый заказ.
    # check = await access_token_decode(acces_token=Authorization)

    # if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
    #     context = await base_requisites(db=session, check=check, request=request)
    #     return templates.TemplateResponse("showcase/if_not_auth.html", context)

    # flag = False
    # if type(check[0]) == ExpiredSignatureError:   
    #     tokens = await test_token_expire(RT=RT, db=session)        
    #     check = tokens[2]
    #     flag = True
    
    fake_user_id = 1

    # query = select(Order_list).options(joinedload(Order_list.product)).where(Order_list.user_id == int(fake_user_id))    

    # order_list = await session.scalars(query)
    
    kount = await session.scalars(select(Order_counter).where(Order_counter.user_id == int(fake_user_id)))
    #таблица контактов будет постоянно пополняться и со временем станет огромной и жестко тупить при заказах, так как она пополняется от всех пользаков при каждом заказе. надо что-то придумать. 
    
    # context = await base_requisites(db=session, check=check, request=request)
    # context = {}

    # context["order_list"] = order_list.all()
    # context["count_order"] = kount.all()
    
    context = kount.all()

    # res = [ {i: j for j in context["order_list"] if i.id == j.order_number}
    # for i in context["count_order"]
    # ]

    
    #решить что делать с таблицей контактов и с таблицей заказов, они будут очень сильно разрастаться и тормозить потом

    # response = templates.TemplateResponse("showcase/checkout_list.html", context)

    # if flag:
    #     response.set_cookie(key="RT", value=tokens[0])
    #     response.set_cookie(key="Authorization", value=tokens[1])

    # return response
    return context


# id это номер заказа. Это функция для открытия заказа для просмотра
@router_showcase_api.get("/checkout_list/orders/{id}", response_model=list[Order_list_boughtShema])
async def checkout_list_view(request: Request, id: int, session: AsyncSession = Depends(get_async_session)):

    fake_user_id = 1

    query = select(Order_list).options(joinedload(Order_list.product)).where(Order_list.user_id == fake_user_id, Order_list.order_number == id)
    

    order_list = await session.scalars(query)
        
    context = order_list.all()
    # context = await base_requisites(db=session, check=check, request=request)
    # context["order_list"] = order_list.all()
    

    return context






