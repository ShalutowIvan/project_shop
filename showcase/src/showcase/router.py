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


#заготовка для формы запроса контактов из формы регистрации, переделать под запрос контактов
@router_showcase.post("/basket/contacts/", response_model=None, status_code=201)#response_model это валидация для запроса
async def contacts_form(request: Request, session: AsyncSession = Depends(get_async_session), fio: str = Form(), phone: int = Form(), delivery_address: str = Form(), pay: int = Form(), Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None)):
    # по куки Authorization найти ид пользака
    check = await access_token_decode(acces_token=Authorization)
    
    flag = False
    if type(check[0]) == ExpiredSignatureError:   
        tokens = await test_token_expire(RT=RT, db=session)        
        check = tokens[2]
        flag = True

    # if type(check[0]) == ExpiredSignatureError:
    #     context = await base_requisites(db=session, check=check, request=request)

    #     return templates.TemplateResponse("showcase/if_not_auth_in_order.html", context)

    kontakt = Contacts(fio=fio, phone=phone, delivery_address=delivery_address, pay_id=pay, user_id=int(check[1]))
        
    session.add(kontakt)
    await session.commit()
    await session.refresh(kontakt)

    pay_goods = await session.scalars(select(Basket).where(Basket.user_id == int(check[1])))
    contacts = await session.scalars(select(Contacts).where(Contacts.user_id == int(check[1])))
    id_contact = contacts.all()[-1].id#это будет номер заказа, таблицу контактов запрашиваю для указания номера заказа

    res = [Order_list(product_id=i.product_id, quantity=i.quantity, order_number=id_contact, user_id=int(check[1])) for i in pay_goods.all()]
    
    session.add_all(res)

    #удаление всех записей в корзине с фильтром по пользаку
    await session.execute(text(f"DELETE FROM basket WHERE user_id = {check[1]};"))  
    # await session.execute(text(f"DELETE FROM contacts WHERE user_id = {check[1]};"))  

    await session.commit()    

    context = await base_requisites(db=session, check=check, request=request)
    context["order_number"] = id_contact
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
    
    kont = await session.scalars(select(Contacts).where(Contacts.user_id == int(check[1])))
    #таблица контактов будет постоянно пополняться и со временем станет огромной и жестко тупить при заказах, так как она пополняется от всех пользаков при каждом заказе. надо что-то придумать. 
    
    context = await base_requisites(db=session, check=check, request=request)
    context["order_list"] = order_list.all()
    context["contacts"] = kont.all()

    #решить что делать с таблицей контактов и с таблицей заказов, они будут очень сильно разрастаться и тормозить потом

    response = templates.TemplateResponse("showcase/checkout_list.html", context)

    if flag:
        response.set_cookie(key="RT", value=tokens[0])
        response.set_cookie(key="Authorization", value=tokens[1])

    return response



from fastapi import UploadFile, File
import shutil


@router_showcase.get("/load_files/file/", response_class=HTMLResponse)
async def file_get(request: Request):
    context = {"request": request}

    response = templates.TemplateResponse("showcase/upload_file.html", context)

    return response


#загрузка фото в базу товаров, это чтобы как то проверить как работать с фото
@router_showcase.post("/load_files/file/", response_class=HTMLResponse)
async def file_post(request: Request, foto: UploadFile = File(...)):

    # check = await access_token_decode(acces_token=Authorization)

    # flag = False
    # if type(check[0]) == ExpiredSignatureError:   
    #     tokens = await test_token_expire(RT=RT, db=session)        
    #     check = tokens[2]
    #     flag = True

    # foto: UploadFile = File(...) - это параметр в функции для загрузки файла



    with open(f'{foto.filename}', 'wb') as buffer:#открываем тестовый файл как буфер и загружаем в него файл
        shutil.copyfileobj(foto.file, buffer)#тут будет создан файл который запишется на диск


    context = {"request": request}
    # context = await base_requisites(db=session, check=check, request=request)
    response = templates.TemplateResponse("showcase/upload_file.html", context)

    # if flag:
    #     response.set_cookie(key="RT", value=tokens[0])
    #     response.set_cookie(key="Authorization", value=tokens[1])

    return response

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





