from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, Form

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


from sqlalchemy import insert, select, text
from sqlalchemy.orm import joinedload

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from .models import *
from src.regusers.models import User
from src.settings import templates
from src.regusers.secure import test_token_expire, access_token_decode

from jose.exceptions import ExpiredSignatureError

import requests



router_showcase = APIRouter(
    prefix="",
    tags=["Showcase"]
)



#функция для формирования контекста страницы
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




@router_showcase.get("/", response_class=HTMLResponse)
async def home(request: Request, Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):    

    check = await access_token_decode(acces_token=Authorization)    
    
    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True
    
    context = await base_requisites(db=session, check=check, request=request)
    good = await session.execute(select(Goods))
    context["good"] = good.scalars()

    response = templates.TemplateResponse("showcase/start.html", context)
    #если флаг, то надо куки новые закинуть
    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response


@router_showcase.get("/{slug}", response_class=HTMLResponse)
async def show_group(request: Request, slug: str, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):    

    #нужно сделать валидацию для параметра slug, а то он тянет любое значение лиш бы было str
    check = await access_token_decode(acces_token=Authorization)

    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True    

    query = select(Goods).options(joinedload(Goods.group))
    good_gr = await session.scalars(query)
    good_gr = list(filter(lambda x: x.group.slug == slug, good_gr))

    context = await base_requisites(db=session, check=check, request=request)
    context["good"] = good_gr

    response = templates.TemplateResponse("showcase/good.html", context)

    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response
      

# <a href="{{ i.slug }}">{{ i.name_group }}</a>


#это форма для поиска товаров
# <form action="{% url 'start' %}" method="get">

#     <input type="search" type="text" name='q' placeholder="Введите название товара">

#     <button type="submit">Найти</button>
# </form>

# {% if g.photo %}
# <p><img class="product-img" src="{{g.photo.url}}"></p>
# {% endif %}
# , response_class=HTMLResponse


@router_showcase.get("/basket/{good_id}")
async def add_in_basket(request: Request, good_id: int, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None)):
    #подтянул ид пользака из токена
    check = await access_token_decode(acces_token=Authorization)
    
    if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
        context = await base_requisites(db=session, check=check, request=request)

        return templates.TemplateResponse("showcase/if_not_auth.html", context)


    query = select(Basket).where(Basket.product_id == good_id, Basket.user_id == int(check[1]))

    basket = await session.scalars(query)
    basket = basket.all()
    

    if basket == []:#если в корзине нет такого товара, то добавляет товар в корзину        
        product = Basket(product_id=good_id, quantity=1, user_id=int(check[1]))
        session.add(product)
        await session.commit()
    else:        
        basket[0].quantity += 1
        await session.commit()
        
    
    http_referer = request.headers.get('referer')
    return RedirectResponse(http_referer)
    
   

@router_showcase.get("/basket/goods/", response_class=HTMLResponse)
async def basket_view(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):

    check = await access_token_decode(acces_token=Authorization)
    
    if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
        context = await base_requisites(db=session, check=check, request=request)

        return templates.TemplateResponse("showcase/if_not_auth.html", context)


    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True    

    
    query = select(Basket).options(joinedload(Basket.product)).where(Basket.user_id == int(check[1]))    
    basket = await session.scalars(query)    

    context = await base_requisites(db=session, check=check, request=request)
    context["basket"] = basket

    response = templates.TemplateResponse("showcase/basket.html", context)

    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response


#удаление товара по коду товара то есть id
@router_showcase.get("/basket/goods/{basket_id}")
async def delete_in_basket(request: Request, basket_id: int, session: AsyncSession = Depends(get_async_session)):    
    
    basket = await session.get(Basket, basket_id)
    await session.delete(basket)
    await session.commit()    
    
    return RedirectResponse("/basket/goods/")
    



# <p>Итоговое количество= {{ basket.total_quantity }}</p>
# <h4>Итоговая сумма= {{ basket.total_sum }}</h4>

# {% if not i.photo %}
# <p><img class="product-img" src="{{i.photo.url}}"></p>
# {% endif %}

# <a href="{% url 'clear_basket' i.id %}"><p>Удалить</p></a>
# <a href="{{ url_for('contacts') }}"><h1>Оформить заказ</h1></a>

# <input name="basketID" type="number" value="{{ i.quantity }}" min="0">

# <h1> Название товара: {{i.product.name_product}}</h1>
# <p>Цена: {{ i.product.price }}</p>
# <p>Сумма цена * количество: {{ i.product.price }}</p>


# @router_showcase.get("/checkout_list", response_class=HTMLResponse)
# async def contacts(request: Request, session: AsyncSession = Depends(get_async_session)):
#     pass

#роутер для прогрузки страницы с формой запроса контактов
@router_showcase.get("/basket/contacts/")
async def contacts(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):
    
    check = await access_token_decode(acces_token=Authorization)
    
    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True

    context = await base_requisites(db=session, check=check, request=request)

    pay_goods = await session.scalars(select(Basket).where(Basket.user_id == int(check[1])))

    if pay_goods.all() == []:
        context["empty_basket"] = "Корзина пуста!"
        response = templates.TemplateResponse("showcase/basket.html", context)
        if flag:
            response.set_cookie(key="RT", value=tokens[0])
            response.set_cookie(key="Authorization", value=tokens[1])
        return response    

    response = templates.TemplateResponse("showcase/contacts.html", context)

    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response

# import uuid
#заготовка для формы запроса контактов из формы регистрации, переделать под запрос контактов
@router_showcase.post("/basket/contacts/", response_model=None, status_code=201)#response_model это валидация для запроса
async def contacts_form(request: Request, session: AsyncSession = Depends(get_async_session), fio: str = Form(), phone: str = Form(), delivery_address: str = Form(), pay: int = Form(), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):
    #дешифровка jwt аксес
    check = await access_token_decode(acces_token=Authorization)
    
    #проверка на истечение токена, в случае если истек обновляем
    flag = False
    if type(check[0]) == ExpiredSignatureError:
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True    
    
    #создаем объект в таблице контактов
    # kontakt = Contacts(fio=fio, phone=phone, delivery_address=delivery_address, pay_id=pay, user_id=int(check[1]))
    order_counter = Order_counter(user_id=int(check[1]))

    session.add(order_counter)
    await session.commit()
    await session.refresh(order_counter)

    #делаем запрос в таблице корзина с фильтром по пользаку
    pay_goods = await session.scalars(select(Basket).where(Basket.user_id == int(check[1])))
    #запрос в таблице контактов по пользаку
    order_number = await session.scalars(select(Order_counter).where(Order_counter.user_id == int(check[1])))
    id_order_number = order_number.all()[-1].id#берем последний в списке номер, это будет номер заказа, таблицу контактов запрашиваю для указания номера заказа
    #формируем генератор списка товаров из корзины
    res = [Order_list(order_number=id_order_number, fio=fio, delivery_address=delivery_address, phone=phone, product_id=i.product_id, quantity=i.quantity, user_id=int(check[1])) for i in pay_goods.all()]
            
    session.add_all(res)

    #удаление всех записей в корзине с фильтром по пользаку
    await session.execute(text(f"DELETE FROM basket WHERE user_id = {check[1]};"))  
    # await session.execute(text(f"DELETE FROM contacts WHERE user_id = {check[1]};"))  

    await session.commit()

    context = await base_requisites(db=session, check=check, request=request)
    context["order_number"] = id_order_number
    response = templates.TemplateResponse("showcase/order_done.html", context)

    if flag:        
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])
        

    # return RedirectResponse("/basket/contacts/checkout/", status_code=303)
    # return RedirectResponse("/", status_code=303)#после оформления переходим на стартовую
    return response

#роутер для кнопки оформления заказа после ввода контактов. Он оказался не нужен
# @router_showcase.get("/basket/contacts/checkout/", response_class=HTMLResponse)
# async def checkout(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None)):
    
#     check = await access_token_decode(acces_token=Authorization)
#     #фильтруем корзину по юзеру

#     # query = select(Basket).options(joinedload(Basket.product)).where(Basket.user_id == int(check_id[1]))    
#     # basket = await session.scalars(query)

#     pay_goods = await session.scalars(select(Basket).where(Basket.user_id == int(check[1])))
#     contacts = await session.scalars(select(Contacts).where(Contacts.user_id == int(check[1])))
#     id_contact = contacts.all()[-1].id

#     res = [Order_list(product_id=i.product_id, quantity=i.quantity, order_number=id_contact, user_id=int(check[1])) for i in pay_goods.all()]
    
#     session.add_all(res)

#     #удаление всех записей в корзине с фильтром по пользаку
#     await session.execute(text(f"DELETE FROM basket WHERE user_id = {check[1]};"))    
        
#     await session.commit()

#     return RedirectResponse("/", status_code=303)





@router_showcase.get("/checkout_list/orders/", response_class=HTMLResponse)
async def checkout_list(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):
    
    check = await access_token_decode(acces_token=Authorization)

    if check[1] == None:#если нет токена то есть пользак вообще не вводил логин пас, то отображаем страницу следующую
        context = await base_requisites(db=session, check=check, request=request)
        return templates.TemplateResponse("showcase/if_not_auth.html", context)

    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True
    
    query = select(Order_list).options(joinedload(Order_list.product)).where(Order_list.user_id == int(check[1]))    
    order_list = await session.scalars(query)
    
    kount = await session.scalars(select(Order_counter).where(Order_counter.user_id == int(check[1])))
    #таблица контактов будет постоянно пополняться и со временем станет огромной и жестко тупить при заказах, так как она пополняется от всех пользаков при каждом заказе. надо что-то придумать. 
    
    context = await base_requisites(db=session, check=check, request=request)
    context["order_list"] = order_list.all()
    context["count_order"] = kount.all()

    #решить что делать с таблицей контактов и с таблицей заказов, они будут очень сильно разрастаться и тормозить потом

    response = templates.TemplateResponse("showcase/checkout_list.html", context)

    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response


#ТУТ РОУТЕРЫ для API с учетной системой

#это роутер для того чтобы учетная система обратилась по ссылке и получила заказы
@router_showcase.get("/checkout_list/orders/all/")
async def synchronization(request: Request, session: AsyncSession = Depends(get_async_session)):    
    
    query = select(Order_list).options(joinedload(Order_list.product))#для обращения к связанному полю товара сделал связанный select, и потом обратился к артикулу и его выгружаем.
    order_list = await session.scalars(query)    
    
    context = order_list.all()
        
    res = ({"fio": i.fio, "phone": i.phone, "product_id": i.product.vendor_code, "quantity": i.quantity, "order_number": i.order_number, "time_create": i.time_create, "delivery_address": i.delivery_address} for i in context)
    #product_id - это артикул тут, потом я по нему ищу товары, пока так. id товаров не совпадают.
    return res




#получение списка товаров из учетной системы, это кнопка в самом проекте фастапи
@router_showcase.get("/query_api/get/good/")
async def get_good(request: Request, session: AsyncSession = Depends(get_async_session)):
    rq = requests.get("http://127.0.0.1:9999/api/get_good/")
    res = rq.json()
    
    
    # [{'name_product': 'Зубная паста', 'slug': 'zubnaya-pasta', 'vendor_code': '_', 'price': '111.00', 'photo': 'photos/2024/02/29/400.jpg', 'stock': 4.0, 'availability': True, 'group_id': 2}, {'name_product': 'Хлеб', 'slug': 'hleb', 'vendor_code': 'qwe123', 'price': '22.00', 'photo': 'photos/2024/02/29/хлеб.png', 'stock': 22.0, 'availability': True, 'group_id': 1}, {'name_product': 'Молоко', 'slug': 'milk', 'vendor_code': 'asd123', 'price': '55.00', 'photo': 'photos/2024/02/29/молоко.jpg', 'stock': 32.0, 'availability': True, 'group_id': 1}]    - это возвращается из запроса из апи дрф
    query_good = await session.scalars(select(Goods))
    good_list = query_good.all()#тут список объектов из таблицы товаров
    # print("тут гуд лист!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(good_list)
    # [<src.showcase.models.Goods object at 0x0000015E9DFF7FD0>, <src.showcase.models.Goods object at 0x0000015E9DFF7E80>, <src.showcase.models.Goods object at 0x0000015E9DFF7E50>, <src.showcase.models.Goods object at 0x0000015E9DFF7E20>, <src.showcase.models.Goods object at 0x0000015E9DFF7DF0>]

    # print("тут из рес!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(res[0]['vendor_code'])
    vendors = {i.vendor_code: i for i in good_list}
    res_with_keys = {i["vendor_code"]: i for i in res}
    # {'123zzzzzzzzzz': {'name_product': 'Булочка', 'slug': 'bulochka', 'vendor_code': '123zzzzzzzzzz', 'price': '22.00', 'photo': 'photos/2024/03/03/images.jpg', 'stock': 4.0, 'availability': True, 'group_id': 1}, '_': {'name_product': 'Зубная паста', 'slug': 'zubnaya-pasta', 'vendor_code': '_', 'price': '111.00', 'photo': 'photos/2024/02/29/400.jpg', 'stock': 6.0, 'availability': True, 'group_id': 2}, '000000000': {'name_product': 'Унитаз', 'slug': 'unitaz', 'vendor_code': '000000000', 'price': '3333.00', 'photo': 'photos/2024/03/03/унитаз_XB8d3Z5.jpg', 'stock': 11.0, 'availability': True, 'group_id': 2}, 'qwe123': {'name_product': 'Хлеб', 'slug': 'hleb', 'vendor_code': 'qwe123', 'price': '22.00', 'photo': 'photos/2024/02/29/хлеб.png', 'stock': 25.0, 'availability': True, 'group_id': 1}, 'asd123': {'name_product': 'Молоко', 'slug': 'milk', 'vendor_code': 'asd123', 'price': '55.00', 'photo': 'photos/2024/02/29/молоко.jpg', 'stock': 29.0, 'availability': True, 'group_id': 1}}


    # print("req!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(res_with_keys)
    # print(vendors["_"].name_product)
    # {'123zzzzzzzzzz': <src.showcase.models.Goods object at 0x0000015E9DFF7FD0>, 'asd123': <src.showcase.models.Goods object at 0x0000015E9DFF7E80>, 'qwe123': <src.showcase.models.Goods object at 0x0000015E9DFF7E50>, '_': <src.showcase.models.Goods object at 0x0000015E9DFF7E20>, '000000000': <src.showcase.models.Goods object at 0x0000015E9DFF7DF0>}

    if good_list == []:
        for k in res:
            product = Goods(name_product=k["name_product"], price=float(k["price"]), vendor_code=k["vendor_code"], stock=float(k["stock"]), slug=k["slug"], photo=k["photo"], availability=True, group_id=int(k["group_id"]))
            session.add(product)
            # await session.commit()
    
    elif good_list != []:        
        for j in res:
            if j["vendor_code"] in vendors:
                if vendors[j["vendor_code"]].stock == j["stock"]:
                    continue
                else:
                    vendors[j["vendor_code"]].stock = j["stock"]
                    session.add(vendors[j["vendor_code"]])
                    # await session.commit()
            else:
                product = Goods(name_product=j["name_product"], price=float(j["price"]), vendor_code=j["vendor_code"], stock=float(j["stock"]), slug=j["slug"], photo=j["photo"], availability=True, group_id=int(j["group_id"]))
                session.add(product)
                # await session.commit()

    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(good_list[-1].name_product)



    for i in good_list:
        if res_with_keys.get(i.vendor_code):
            continue
        else:
            # good_list.remove(i)
            await session.delete(i)
    

    await session.commit()    


    # session.add_all(good_list)
    # await session.commit()


    # print(good_list[-1].name_product)


    # сделать удаление элемента, желательно чтобы было все в одном цикле, но пока не получается.

    return RedirectResponse("/")

#####################################################################################



# from fastapi import UploadFile, File
# import shutil


# @router_showcase.get("/load_files/file/", response_class=HTMLResponse)
# async def file_get(request: Request):
#     context = {"request": request}

#     response = templates.TemplateResponse("showcase/upload_file.html", context)

#     return response


#загрузка фото в базу товаров, это чтобы как то проверить как работать с фото
# @router_showcase.post("/load_files/file/", response_class=HTMLResponse)
# async def file_post(request: Request, foto: UploadFile = File()):

#     # check = await access_token_decode(acces_token=Authorization)

#     # flag = False
#     # if type(check[0]) == ExpiredSignatureError:   
#     #     tokens = await test_token_expire(RT=RT, db=session)        
#     #     check = tokens[2]
#     #     flag = True

#     # foto: UploadFile = File(...) - это параметр в функции для загрузки файла



#     with open(f'fotos/{foto.filename}', 'wb') as buffer:#открываем тестовый файл как буфер и загружаем в него файл
#         shutil.copyfileobj(foto.file, buffer)#тут будет создан файл который запишется на диск


#     # context = {"request": request}
#     # context = await base_requisites(db=session, check=check, request=request)
#     # response = templates.TemplateResponse("showcase/upload_file.html", context)

#     # if flag:
#     #     response.set_cookie(key="RT", value=tokens[0])
#     #     response.set_cookie(key="Authorization", value=tokens[1])

#     # return response
#     return RedirectResponse("/")

#видос про загрузку файлов
# https://www.youtube.com/watch?v=kANFWfgTZT8&ab_channel=FastAPIChannel


# <!-- пагинация начало -->
# {% if page_obj.has_other_pages %}
# <nav class="list-pages">
#     <ul>
# {% if page_obj.has_previous %}
# <li class="page-num">
# <a href="?page={{ page_obj.previous_page_number }}">&lt;</a>
# </li>
# {% endif %}

# {% for i in paginator.page_range %}

# {% if page_obj.number == i %}
# <li class="page_selected">{{ i }}</li>

# {% elif i >= page_obj.number|add:-2 and i <= page_obj.number|add:2  %}


# <li class="page-num">
#     <a href="?page={{ i }}">{{ i }}</a>
# </li>
# {% endif %}

# {% endfor %}


# {% if page_obj.has_next %}
# <li class="page-num">
# <a href="?page={{ page_obj.next_page_number }}">&gt;</a>
# </li>
# {% endif %}
# </ul>
# </nav>
# {% endif %}

# <!-- пагинация конец -->


# <!--Форма для поиска товара -->
# <form action="{% url 'start' %}" method="get">

#     <input type="search" type="text" name='q' placeholder="Введите название товара">

#     <button type="submit">Найти</button>
# </form>
# <!--конец Форма для поиска товара -->



# <!--    {% # if request.user.is_authenticated %}   -->

# <!--  {% # else %}  -->

# <!--                {% # endif %} -->



# <!--форма для добавления корзины -->
#     {% if request.user.is_authenticated %}
# <a href="{% url 'add_in_basket' j.id %}"><button class="add_basket">Добавить в корзину</button></a>

#     <br><br>


#     {% endif %}
# <!--конец форма -->






