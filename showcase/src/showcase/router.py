from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from .models import *
from src.settings import templates
from src.regusers.router import get_current_user_from_token
from src.regusers.secure import update_tokens
from jose.exceptions import ExpiredSignatureError





router_showcase = APIRouter(
    prefix="",
    tags=["Showcase"]
)



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

    check = await get_current_user_from_token(acces_token=Authorization)
    
    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": gr.scalars(),
    "gd": gd.scalars(),
    "check": check
    }


    #нужно переделать модель чтобы через поле группы в таблице товаров можно было обращаться к названию группы, а не только к ИД группы. Иначе лишние sql запросы будут

    response = templates.TemplateResponse("showcase/start.html", context)
    if type(check) == ExpiredSignatureError:        
        tokens = await update_tokens(RT=RT, db=session)
        refresh = tokens[0]
        access = tokens[1]
        response.set_cookie(key="RT", value=refresh)
        response.set_cookie(key="Authorization", value=access)


    return response



@router_showcase.get("/{slug}")
async def show_group(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)):
    # параметр должен подтянуться из базы групп из поля слаг. В теле функции нужно по слагу фильтровать товары через запрос из бд и выводить их html в отдельный шаблон с контекстом. 

    query = select(Goods).options(joinedload(Goods.group))
    # .options(joinedload(Goods.group)).group_by(Goods.group.slug == slug)
    # good_gr = await session.execute(query.filter_by(Goods.group.slug == slug))

        
    good_gr = await session.scalars(query)
    # good_gr = good_gr.where(Goods.group.slug == slug)
    good_gr = list(filter(lambda x: x.group.slug == slug, good_gr))

    gr = await session.execute(select(Group))

    # print(good_gr)
    #.where(Goods.group.slug == slug)
    # .where()
    # print("мы тут --------------------")
    # for i in good_gr:
    #     print(i.group.slug)

    # sl = await session.scalar(select(Group).where(Group.slug == slug))

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
async def add_in_basket(request: Request, good_id: int, session: AsyncSession = Depends(get_async_session)):
    
    # product = await session.get(Goods, good_id)
    basket = await session.execute(select(Basket).where(Basket.product_id == good_id))
    basket = basket.scalars().all()
    if basket == []:#если в корзине нет такого товара, то добавляет товар в корзину
        product = Basket(product_id=good_id, quantity=1, user_id=1)#пользователю нужно подтянуть из БД или из запроса как то или из токена
        session.add(product)
        await session.commit()
        # await session.refresh()
    else:
        basket[0].quantity += 1
        await session.commit()
        # await session.refresh()

    # response = templates.TemplateResponse("showcase/start.html", context)
    print("ТУТ КОРЗИНААААААААААААААААААААААААА")
    # print(basket.scalars())
    http_referer = request.headers.get('referer')
    return RedirectResponse(http_referer)
    # return RedirectResponse(f"/basket/{good_id}", status_code=303)
   


# пример запроса из роутера авторизации
    # await session.scalar(select(User).where(User.email == email))



@router_showcase.get("/goods/basket", response_class=HTMLResponse)
async def basket_view(request: Request, session: AsyncSession = Depends(get_async_session)):

    basket = await session.execute(select(Basket))
    org = await session.execute(select(Organization))    
    gr = await session.execute(select(Group))



    context = {
    "request": request,
    "basket": basket.scalars().all(),
    "org": org.scalars().first(),
    "group": gr.scalars().all(),

    }

    return templates.TemplateResponse("showcase/basket.html", context)

# <p>Итоговое количество= {{ basket.total_quantity }}</p>
# <h4>Итоговая сумма= {{ basket.total_sum }}</h4>

# {% if not i.photo %}
# <p><img class="product-img" src="{{i.photo.url}}"></p>
# {% endif %}

# <a href="{% url 'clear_basket' i.id %}"><p>Удалить</p></a>
# <a href="{{ url_for('contacts') }}"><h1>Оформить заказ</h1></a>




@router_showcase.get("/checkout_list", response_class=HTMLResponse)
async def checkout_list(request: Request, session: AsyncSession = Depends(get_async_session)):
    order_list = await session.execute(select(Order_list))
    kont = await session.execute(select(Contacts))

    context = {
    "request": request,
    "order_list": order_list.all(),
    "contacts": kont.all()
    }

    return templates.TemplateResponse("showcase/basket.html", context)



# @router_showcase.get("/checkout_list", response_class=HTMLResponse)
# async def contacts(request: Request, session: AsyncSession = Depends(get_async_session)):
#     pass


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




