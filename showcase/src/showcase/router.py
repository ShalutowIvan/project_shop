from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, Form

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from .models import *
from src.regusers.models import User
from src.settings import templates
from src.regusers.router import access_token_verify
from src.regusers.secure import update_tokens
from jose.exceptions import ExpiredSignatureError





router_showcase = APIRouter(
    prefix="",
    tags=["Showcase"]
)

# router_showgroup = APIRouter(
#     prefix="",
#     tags=["Showgroup"]
# )




##################################################################################
#памятка как делать sql запрос с асинхронным подключением к сессии БД!!!!!!!!!!!!
#этот код нужно писать в асинхронной функции
# org = select(organization)#создали запрос на таблицу организаций. organization это модель БД, которую мы ранее сами сделали. select это функция из sql алхимии. 
# res = await session.execute(org)#запросили ее из сессии, всю таблицу. session - это параметр функции вьюшки, execute это метод для подключения. В скобках пишем переменную которую написали выше.
# print(f"Название {res.all()[0]}")#тут мы сделали sql запрос всей таблицы, возвращается список кортежей по каждой строке в таблице, 1 строка 1 кортеж. Тут к предыдущей переменной можно юзать функции из sql алхимии. 
##################################################################################




##################################################################################
#памятка как работает Depends
#сначала срабатывает функция которую передали в Depends. Потом срабатывает функция в которой указан depends.
#Если в Depends есть оператор yield с сессией БД, то он еще завершает потом работу БД.
#то есть получается функция которую передали в Depends вызывается перед запуском той функции в которой указали Depends. 
#также можно и передавать в Depends класс. В классе должен быть инициализатор с нужными параметрами. Можно указать параметры в инициализаторе такие как в функции и это будет тоже самое. 
#примеры
# class Paginator:
#     def __init__(self, limit: int = 10, skip: int = 0):
#         self.limit = limit
#         self.skip = skip


# def page(limit: int = 10, skip: int = 0):#эту функцию можно юзать как Depends и класс выше, и эффект будет один и тот же. В функции представления будут также передаваться доп параметры те же самые. Скорее всего потому что объект класса Paginator это как бы тоже словарь, и тут в функции возвращается тоже словарь
#     return {"limit": limit, "skip": skip}


# @app.get("/subject_class")
# async def get_subject_class(pagination_params: Paginator = Depends(Paginator)):#название класса в скобках можно не прописывать, либо название класса в качестве аннотации типа можено не прописывать.
#     return pagination_params
#еще можно делать вызываемые объект как функции с методом __call__
# в методе __call__ можно прописать условие, в котором в случае невыполнения условия будет вызываться исключение - ошибка. И в случае вызова исключения функция в которой мы укажем эту зависимость не будет выполняться. В случае если зависимость отработает без вызова исключений, то основная функция сработает. 
# Пример:
# class Authguard:
#     def __init__(self, name: str):
#         self.name = name


#     def __call__(self, request: Request):
#         if "super_cookie" not in request.cookies:#cookies это dict , то есть словарь, тут идет проверка есть ли такой ключ в словаре
#             raise HTTPException(status_code=403, detail="Запрещено")
#         return True

# auth_guard_payments = AuthGuard("payments")


# @app.get("/subject_class")
# async def get_subject_class(auth_guard_payments: AuthGuard = Depends(auth_guard_payments)):
#     return "my payments..."

#еще можно писать зависимости в декораторе в виде списка зависимостей
# @app.get("/subject_class", dependencies=[Depends(auth_guard_payments)])
# async def get_subject_class():#а в фукнции уже не нужно будет писать зависимости. При запуске весь список зависимостей также будет прогоняться. 
#     return "my payments..."
#cookies это dict , то есть словарь, тут идет проверка есть ли такой ключ в словаре. 
#!!!!!!!!! Также список dependencies=[Depends(auth_guard_payments)] можно прописать при создании объекта роутера, тогда ко всем роутерам будут добавляться эти зависимости, и во всех роутерах будет или какая-то проверка или доп параметр. Очень крутая штука


##################################################################################


@router_showcase.get("/", response_class=HTMLResponse)
async def home(request: Request, Authorization: str | None = Cookie(default=None), RT: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):    
    
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))
    gd = await session.execute(select(Goods))

    check = await access_token_verify(acces_token=Authorization)
    
    if check[1] != None:
        query = select(User).where(User.id == int(check[1]))    
        user = await session.scalars(query)
        user_name = user.all()[0].name
    else:
        user_name = ""



    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": gr.scalars(),
    "gd": gd.scalars(),
    "check": check[0],
    "user_name": user_name,
    }

    response = templates.TemplateResponse("showcase/start.html", context)    
    # print("ОШИБКА ТУТ!!!!!!!!!!!!!!")
    # print(check[0])# тут фолз если нет токена вообще. Во втором элементе None

    if type(check[0]) == ExpiredSignatureError:    
        tokens = await update_tokens(RT=RT, db=session)
        refresh = tokens[0]
        access = tokens[1]
        response.set_cookie(key="RT", value=refresh)
        response.set_cookie(key="Authorization", value=access)


    return response



@router_showcase.get("/{slug}", response_class=HTMLResponse)
async def show_group(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)):
    # параметр должен подтянуться из базы групп из поля слаг. В теле функции нужно по слагу фильтровать товары через запрос из бд и выводить их html в отдельный шаблон с контекстом. 

    #нужно сделать валидацию для параметра slug, а то он тянет любое значение лиш бы было str
    query = select(Goods).options(joinedload(Goods.group))
    good_gr = await session.scalars(query)    
    good_gr = list(filter(lambda x: x.group.slug == slug, good_gr))

    gr = await session.execute(select(Group))

    # good_gr = await session.execute(select(Goods))
    # good_gr = await session.scalars(select(Goods).where(Goods.group_id == sl.id))
    org = await session.execute(select(Organization))


    context = {
    "request": request,
    "good_gr": good_gr,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    response = templates.TemplateResponse("showcase/good.html", context)

    return response
    # return RedirectResponse(f"/{slug}")    

# <a href="{{ i.slug }}">{{ i.name_group }}</a>


#кнопка для добавления товара в корзину. Пока убрал
# <a href="{% url 'add_in_basket' g.id %}"><button>Добавить в корзину</button></a>

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
    check_id = await access_token_verify(acces_token=Authorization)


    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))
    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": gr.scalars().all(),

    }
    if check_id[1] == None:#если нет токена, то отображаем страницу следующую
        return templates.TemplateResponse("showcase/if_not_auth.html", context)


    query = select(Basket).where(Basket.product_id == good_id, Basket.user_id == int(check_id[1]))

    basket = await session.scalars(query)
    basket = basket.all()
    

    if basket == []:#если в корзине нет такого товара, то добавляет товар в корзину
        check_id = await access_token_verify(acces_token=Authorization)
        product = Basket(product_id=good_id, quantity=1, user_id=int(check_id[1]))
        session.add(product)
        await session.commit()
    else:
        check_id = await access_token_verify(acces_token=Authorization)
        basket[0].quantity += 1
        await session.commit()
        
    
    http_referer = request.headers.get('referer')
    return RedirectResponse(http_referer)
    
   




@router_showcase.get("/basket/goods/", response_class=HTMLResponse)
async def basket_view(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None)):

    check_id = await access_token_verify(acces_token=Authorization)
    
    query = select(Basket).options(joinedload(Basket.product)).where(Basket.user_id == int(check_id[1]))    
    basket = await session.scalars(query)
    # basket = basket.all()
    # basket = list(filter(lambda x: x.user_id == check_id[1], basket))

    # basket = basket.filter(Basket.user_id == check_id[1])
    # разобраться с фильтрами
    # print("КОРЗИНАААААААААААААААА")
    # print(basket)
    # print(check_id[1])
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "basket": basket,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    "check": check_id[0],
    }

    return templates.TemplateResponse("showcase/basket.html", context)


#тестовый переход на функцию basket_view (не маршрут, а именно функцию). Пока ничего не получилось, делаю переход по маршруту
# @router_showcase.get("/")
# async def redir(request: Request):
#     return basket_view






#удаление товара по коду товара то есть id
@router_showcase.get("/basket/goods/{basket_id}")
async def delete_in_basket(request: Request, basket_id: int, session: AsyncSession = Depends(get_async_session)):    
    
    basket = await session.get(Basket, basket_id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(basket)
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
async def contacts(request: Request, session: AsyncSession = Depends(get_async_session)):
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))

    context = {
    "request": request,
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    response = templates.TemplateResponse("showcase/contacts.html", context)
    return response


#заготовка для формы запроса контактов из формы регистрации, переделать под запрос контактов
@router_showcase.post("/basket/contacts/", response_model=None, status_code=201)#response_model это валидация для запроса
async def contacts_form(request: Request, session: AsyncSession = Depends(get_async_session), fio: str = Form(), phone: int = Form(), delivery_address: str = Form(), pay: int = Form(), Authorization: str | None = Cookie(default=None)):
    # по куки Authorization найти ид пользака
    check_id = await access_token_verify(acces_token=Authorization)
    kontakt = Contacts(fio=fio, phone=phone, delivery_address=delivery_address, pay_id=pay, user_id=int(check_id[1]))
        
    session.add(kontakt)
    await session.commit()

    return RedirectResponse("/basket/contacts/checkout/", status_code=303)


#роутер для кнопки оформления заказа после ввода контактов
@router_showcase.get("/basket/contacts/checkout/", response_class=HTMLResponse)
async def checkout(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None)):
    
    check_id = await access_token_verify(acces_token=Authorization)
    #фильтруем корзину по юзеру

    # query = select(Basket).options(joinedload(Basket.product)).where(Basket.user_id == int(check_id[1]))    
    # basket = await session.scalars(query)

    pay_goods = await session.scalars(select(Basket).where(Basket.user_id == int(check_id[1])))
    contacts = await session.scalars(select(Contacts).where(Contacts.user_id == int(check_id[1])))
    id_contact = contacts.all()[-1].id

    res = [Order_list(product_id=i.product_id, quantity=i.quantity, order_number=id_contact, user_id=int(check_id[1])) for i in pay_goods.all()]
    
    session.add_all(res)

    # for i in pay_goods.all():  
    #     print("!!!!!!!!!!!!!!!!!!!")
    #     print(i)

    #     await session.delete(i)

    
    
        # delete(pay_goods#все элементы корзины. Удаление не работает
    await session.commit()

    print(contacts)

    return RedirectResponse("/", status_code=303)




 # взять из модели корзины все товары по юзеру
    # взять контакт по юзеру


@router_showcase.get("/checkout_list/orders/", response_class=HTMLResponse)
async def checkout_list(request: Request, session: AsyncSession = Depends(get_async_session), Authorization: str | None = Cookie(default=None)):

    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))


    check_id = await access_token_verify(acces_token=Authorization)

    query = select(Order_list).options(joinedload(Order_list.product)).where(Order_list.user_id == int(check_id[1]))    
    order_list = await session.scalars(query)
    
    kont = await session.scalars(select(Contacts).where(Contacts.user_id == int(check_id[1])))
    #таблица контактов будет постоянно пополняться и со временем станет огромной и жестко тупить при заказах, так как она пополняется от всех пользаков при каждом заказе. надо что-то придумать. 
    
    context = {
    "request": request,
    "order_list": order_list.all(),
    "contacts": kont.all(),
    "org": org.scalars().first(),
    "group": gr.scalars().all(),
    }

    return templates.TemplateResponse("showcase/checkout_list.html", context)


#заказы не филтруются. Но формируется таблицы с заказами. И товары из корзины не удаляются после формирования заказа. 

     






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





