#1. Django REST Framework - что это такое | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!
#drf это дополнение для джанго. нужно чтобы можно было делать запросы с других серверов к приложению на drf.
#rest это архитектурный стиль взаимодействия между клиентом и сервером. описание способа взаимодействия между клиентом и сервером
#на стороне сервеа создается программный интерфейс API.
#DRF это интрумент для создания апи нашего сайта.
#например стороннее приложение делает get запрос к сайту на DRF у какому то урл этого сайта то есть по ссылке. Сайт создает данные по этому апи запросу и отдает ответ клиенту обычно в виде JSON формате. То есть приложение отправило запрос по ссылке, и получило ответ в виде сырых данных в формате JSON. Потом приложение обрабатывает данные и отображает то что ему нужно. 
#в DRF есть CRUD, валидация, авторизация и регистрация юзеров, права доступа к данным через апи.
# схема работы
#приходит апи запрос то есть ссылка из браузера это запрос --- далее маршрутизатор отправляет в обработку этот запрос тому представлению, которое связано с этим запросом, представления обрабатывают запросы и отправляют результат пользователю в виде страницы или просто сырые данные в зависимости от потребности --- далее запрос идет к сериализаторам, они обрабатывают данные, например берут данные из бд и отправляют пользаку в виде JSON например, или сериализатор может удалить или изменить данные.

#2. Установка Django Rest Framework | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!!

#команда установки такая же как в обычном джанго
#pip install django
#команда старт проекта такая же как в обычном джанго
# django-admin startproject ACCOUNTING
#запуск сервера такой же
#миграции
#python manage.py migrate
#создание приложения
#python manage.py startapp название приложения
#в сеттинг нужно подключить приложение в списке INSTALLED_APPS
#модели частино скопировал
#создание миграций!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#python manage.py makemigrations
#сама миграция!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# python manage.py migrate
# создание суперпользователя
# python manage.py createsuperuser
#я создал пользака root пароль 1234
# суперюзера надо зарегать
# перейти в файл admin.py приложения
#там прописать все наши модели, чтобы они закинулись в админку
#установка DRF!!!!!!!!!!!!!!!!!
# pip install djangorestframework
#потом нужно зарегать приложение DRF 
#в файле settings.py в списке INSTALLED_APPS добавить приложение с названием rest_framework
# импортируем ветку generics, в ней много базовых классов для представлений для DRF. Далее в файле views продолжаем


#3. Базовый класс APIView для представлений | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!
#при создании апи нужны 3 составляющие:
# 1. Создание представления - views
# 2. Создание сериализатора - для валидации данных как я понял
# 3. Маршрутизация - urls.py
# Рассмотрим представления
# есть класс в DRF класс APIView - этот класс стоит во главе иерархии всех классов представления DRF. То есть другие классы представления наследуются от него. Он представляет собой базовый класс представлений в рамках DRF, базовый имеется ввиду самые базовые функции без лишних конструкций. В доукментации есть описания классов которые наследуются от APIView, их можно потом юзать.
# Сначала определим метод get в этом классе. ОН будет отвечать за get запросы, они будут через него автоматом работать. 
#программа которая отправляет какие либо запросы в API - это постман, самая распространенная программа для запросов. Можно отправлять какие-либо get или post запросы. 
#нужно установить postman
#создаем там новую вкладку new_tab
#там можно выбрать запрос get и в урл скопировать нашу ссылку для представления http://127.0.0.1:8000/api/v1/goodlist/
# Вернется наш словарик, который мы там возвращаем в функции get
#если выбрать сейчас post запрос, то выйдет ошибка, метод post не разрешен. 
# {
#     "detail": "Метод \"POST\" не разрешен."
# }
#такой ответ генерирует базовый класс APIView из DRF. Такой ответ был выдан из-за того что не был определен метод post
#чтобы ошибки такой не было, нужно определить метод post, его нужно так и назвать def post
#теперь в постмане будет возвращаться то, что мы возвращаем в нашей функции post
#теперь попробуем сделать запрос в БД. Сделаем запрос товаров из БД. Они все отобразятся в браузере.
# Также так как мы определили метод post, то в браузере автоматом будет форма для добавления товаров, ее сгенерировал DRF автоматом. Без сериализатора она не работает, но отображается. Если нужно можно сделать сериализатор, тогда будет работать. 
#Аналогично будет и postman
# Если отрправить get запрос, то вернутся значения из БД, те же самые что и в браузере
#в Postman есть вкладка pretty, там данные упорядочены в удобном виде разбитые по строкам. Есть еще вкладка Raw, там сырые данные из запроса, просто сплошным текстом. Preview - это примерно то же самое что и Raw. 
#теперь модифицируем post запрос, чтобы он добавлял новые данные в БД. 
#теперь метод пост добавляет новую запись в БД и возвращает то что было добавлено. 
#теперь можно через программу postman отправить post запрос для добавления строки в БД. Как это сделать. Нужно в программе postman с той же самой ссылкой выбрать post запрос, потом перейти на вкладку body, там пишется тело запроса. Там нужно выбрать raw, это сырой запрос. В этой вкладке нужно прописать словарик с нужными данными для добавления строки в БД. 
#данные нужно написать те, которые мы берем из request в функции post нашей вью в виде словаря. Также по умолчанию в postman выбран заголовок запроса HTTP - Text, а нам нужно выбрать JSON. 
# Также немало важно. Если есть поля с вторичным ключом, то в названия нужно дописывать _id, например не просто group, а group_id и функции post и в JSON, иначе будет ошибка при добавлении записи в БД. 
# {
#     "name_product": "Зубная паста",
#     "slug": "tooth_paste",
#     "price": 110,
#     "photo": "photos/2024/01/26/400.jpg",
#     "stock": 11,
#     "group_id": 3
# }
#в случае если будет что-то не так, то возвращается не json в postman, а html ошибка из джанго. Джанго сам ее формирует. В postman эту же html страницу можно посмотреть на вкладке Preview внизу, и в Pretty будет только код html
#у меня почему-то выходила ошибка 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
#но запись в базу при этом добавлялась. Из-за чего выходит ошибка, непонятно, вроде сделал все верно. 
#в джанго встроенные html страницы для отображения ошибок. 
#когда на сервер приходит HTTP запрос от клиента в наш API, маршрутизатор передает этот запрос фреймворку, и DRF вызывает нужный метод из класса представления для нужного типа запроса get, post, delete и тд. Получется класс APIView связывает запрос с соответствующим методом из класса который мы пропишем. 

#4. Введение в сериализацию. Класс Serializer | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!
# При обмене данными через API чаще всего используют форматы JSON и XML. JSON чаще. Иногда разрабатывают свой собственный формат для обмена, но редко. 
# Сериализатор - это конвертатор объектов языка python в JSON формат. Это его основная функция. Также он конвертирует модели джанго и наборы queryset. Также и наоборот из JSON в объекты питона. 
#перейдем в файл serializers.py там пропишем класс, который будет преобразовывать в JSON формат, как бы имитировать нашу модель. 

# Как я понял в качестве сериализатора в FastApi используется pydentic. С ним надо тоже разобраться!!!!!!!!!!!!


#5. Методы save(), create() и update() класса Serializer | Уроки по Django REST Framework!!!!!!!!!!!!!!!!
# наш класс сертиализатор только преобразует данные в формат json и обратно. Но сериализаторы должны сохранять и изменять данные в БД и удалять. У нас пока это делает GoodsAPIView с базовым классом APIView
# для этого можно в классе GoodsSerializer переопределить 2 метода create и update
# create(self, validated_data) - для добавления (создания) записи (данных)
# update(self, instance, validated_data) - для изменения данных (записи)


#6. Класс ModelSerializer и представление ListCreateAPIView | Уроки по Django REST Framework!!!!!!!!!!!!!
# ранее у нас был сериализатор связанный с моделью БД. Мы использовали класс Serializer, который связываться с моделью БД. МОжно удалять, добавлить, изменять, получать данные из БД. 
# Для этой схемы есть специальный класс сериализатор serializers.ModelSerializer. Он значительно упрощает работу с сериализатором. С ним не нужно прописывать типы полей вручную в самом классе. В основном там нужен только класс Meta.
#также есть специальные вью классы для упрощения работы. Перейдем во воью создадим класс и наследуем его от ListCreateAPIView. Импортировать их нужно из ветки generics
# Ссылка на документацию с классами представлений:
# https://www.django-rest-framework.org/api-guide/generic-views/

#7. Представления UpdateAPIView и RetrieveUpdateDestroyAPIView | Уроки по Django REST Framework!!!!!!!!!!!!!!!!
# ListCreateAPIView - это для post и get запросов. А UpdateAPIView для изменения в БД, то есть put и putch запросов. В это классе UpdateAPIView есть классы миксины в которых описана логика для видов запроса put и putch. Другие виды запросов там не прописаны и постман будет писать ошибку запрос не разрешен. 
# Но часто в проектах требуется применять все виды запросов CRUD. Для этого есть класс RetrieveUpdateDestroyAPIView, в нем можно делать все виды запросов. В нем есть все нужные миксины, то есть он наследуется от всех нужных миксинов для операций CRUD. Пропишем клас с наследованием от RetrieveUpdateDestroyAPIView. Если сделать класс с этим классом, то в браузере можно будет посмотреть, изменить и удалить и джанго также сразу отобразит фронтовую часть для всех этих действий. Можно изменить, удалить и посмотреть. Если удалить и потом через постман посмотреть, то постман напишет страница не найдена. 
#Также весь фронтенд который идет из джанго можно отключить, чтобы потом в других приложениях при апи запросах не тянулся фронт из джанго, а только нужные данные. 
# Чтобы фронт из джанго отключился нужно в файле settings.py прописать следующее:
# REST_FRAMEWORK = {
# 	'DEFAULT_RENDERER_CLASSES': [
# 	'rest_framework.renderers.JSONRenderer',
# 	#'rest_framework.renderers.BrowsableAPIRenderer', #эту строку можно закоментировать, она отвечает за отрисовку рест страниц при апи запросах. Без нее будут просто json возвращаться. Пока пилим проект ее можно оставить, но потом закоментировать. 
# 	]
# }

# также есть и много других настроек, их можно гуглить. 

#8. Viewsets и ModelViewSet | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!!!!
#Мы сделали несколько классов вью с однотипным кодом. В DRF их можно объединять, есть специальный функционал Viewsets. Ссылка на док-цию: https://www.django-rest-framework.org/api-guide/viewsets/
# Мы воспользуемся классом ModelViewSet, он поддерживает работу с моделями. Прописал этот класс во вьюшках. Он по сути заменяет все те предыдущие классы. 

#внутри те же самые параметры. Перейдем теперь в urls.py, там теперь в урл можно писать еще и параметры с видами запросов и названиями методов для их обработки, все это прописывается в виде словарей, ключ это название запроса, значение это название метода. Прочитать про название методов для запросов можно в док-ции. И также все виды запросов работают через браузер или постман.

#Мы в urls.py пишем 2 урл для пост и гет запроса, урл для гет без параметра, а урл для пост put delete с параметром.
# Но также в джанго чтобы на писать по 2 строки УРЛ с одинаковымы адресами для пост и гет запроса, есть специальный функционал для роутеров. Есть SimpleRouter и DefaultRouter. Импортировать их и прописывать нужно в urls.py, импорт такой: from rest_framework import routers. Потом нужно создать объект роутера. Потом нужно в этом объекте зарегать объект вьюсета. 
# router = routers.SimpleRouter()#SimpleRouter это класс роутера
# router.register(r'good', GoodsViewSet)#GoodsViewSet - это клас вьюсета. 
#теперь его нужно прописать в маршрутах. Там мы прописываем весь набор маршрутов, который был сгенерирован роутером. 
# path('api/v1/', include(router.urls))#так прописали путь
#теперь в браузере если перейти по ссылке http://127.0.0.1:8000/api/v1/good/, то отобразится наши данные из БД и можно сделать гет и пост запрос, то есть посмотреть и добавить данные. Также если прописать параметр в маршруте http://127.0.0.1:8000/api/v1/good/11, то то можно будет делать delete и put запросы. 
#То есть тут будет присутствовать весь функционал для работы с БД CRUD. То есть 1 класс и 2 строки кода в нем дает все это, но и роутер зарегать надо. 
#Также можно и юзать другие урезанные классы, в случае если нам не нужен лишний функционал. Например класс ReadOnlyModelViewSet позволяет тольк читать инфу, то есть только гет запрос. Параметр тоже можно добавлять, но доступен также только просмотр. 
#Там внутри таких классов подключены нужные миксины с нужными видами запросов. То есть по факту мы можем точно также юзать нужные нам миксины из базовых классов DRF. Будет все то же самое. 

#9. Роутеры: SimpleRouter и DefaultRouter | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!
# Ссылка на док-цию про использование роутеров: https://www.django-rest-framework.org/api-guide/routers/
#так выглядит список урл default: 
# [<URLPattern '^good/$' [name='goods-list']>,
#  <URLPattern '^good\.(?P<format>[a-z0-9]+)/?$' [name='goods-list']>,
#  <URLPattern '^good/(?P<pk>[^/.]+)/$' [name='goods-detail']>, 
# <URLPattern '^good/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='goods-detail']>, 
# <URLPattern '^$' [name='api-root']>, 
# <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>]
#в нем есть 3 группы маршрутов. 
# Первые 2 строки выше отвечают за получение списка позиций, то есть когда запрос идет без параметра в УРЛ, также есть и все операции CRUD, если они прописаны в классе представления
# 3 и 4 строки отвечают за получение какой одной строки, то есть когда запрос идет с параметров для фильтрации, аналогично есть нужные операции CRUD если они прописаны
# 5 и 6 строки они присутствуют только в default router, эти маршруты присутствуют только в самом роутере. То есть маршрут без префикса из роутера.  
#если перейти по маршрут из default то есть по 5 или 6 строке, то там будет словарь (возможно json) по ссылкой на маршрут из 1 и 2 пункта, то есть ссылка на обычнный маршрут без параметров. 
# {
#     "good": "http://127.0.0.1:8000/api/v1/good/"
# }
#если юзать SimpleRouter то default маршрута (http://127.0.0.1:8000/api/v1/) не будет, и если по нему перейти, будет отображаться НОС. 
# Также в списке выше есть поле [name='goods-list'], тут прописывается имя маршрута. Это имя можно юзать на фронте в html например как понял в jinja. Имена там формируются автоматом. 
# Эти имена формируются из названия модели с маленькой буквы потом "-" потом слово "list" в случае если это список или слово "detail" в случае если есть параметр в урл для фильтрации. Префикс в роутере не влияет на имя маршрута, только на путь самого маршрута. Но имя можно указать самим прописать еще один параметр basename="имя урл".
#  Например так: basename="tovar"
# теперь имена урл будут выглядеть так: [name='tovar-list']
#причем этот параметр basename обязателен если не указывать во вью классе атрибут queryset. Если не указать ни queryset ни basename то роутер не сможет подставить имя модели при формировании имен маршрута. 

# Предположим если стандартных маршуртов не достаточно и нужно определить свой. Для этого есть специальный декоратор @action() для определения новых маршрутов. Новые маршруты можно прописать в классе вью в отдельных УРЛ. Например выведем список групп, а не список товаров. Перейдем в файл views.py приложения. 

# Также иногда нужно не просто возвращать все записи из таблицы, а какие то сложные условия делать с группировкой объекдинением таблиц и тд. 
# Для этого можно переопределить метод get_queryset в классе вью. Там можно прописать нужный нам срез или нужную фильтрацию. Атрибут queryset можно теперь убрать. НО обязательно тогда прописать параметр basename='название модели с маленькой буквы'. Без него не будет ссылки на модель и вью работать не будет. 

# Еще можно создавать свои классы роутеров. Их лучше делать в отдельном файле routers.py и потом подключать в urls.py. На данный момент для демонстрации класс роутера создадим в файл urls.py


#10. Ограничения доступа (permissions) | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!
# Добавим в таблицу товаров еще одно поле user. 
# user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")		
# models.CASCADE - означает что при удалении пользака будут удалены все записи связанные с этим пользаком. 
# модель User имортируем из джанго. from django.contrib.auth.models import User. 
#теперь в таблице товаров у каждого товара будет поле юзер. ТО есть тот кто товар добавил. 
# сделаем отдельные новые вью. 

#пропишем маршруты для текущих вьюшек. И теперь любой пользак может что-либо делать с данными с нашего сайта. Это означает что безопасности нет вообще. 
# Для этого в джанго используются permissions - ограничения прав доступа. 
# AllowAny – полный доступ;
# IsAuthenticated – только для авторизованных пользователей;
# IsAdminUser – только для администраторов;
# IsAuthenticatedOrReadOnly – только для авторизованных или всем, но для чтения.
# Ссылка на док-цию: https://www.django-rest-framework.org/api-guide/permissions/
# Сделаем так чтобы можно было добавлять записи только если авторизован пользак. Можно воспользоваться классом IsAuthenticatedOrReadOnly.
#во воьшке сделали permissions свои вручную в отдельном файле permissions.py

#Еще можно делать глобальные ограничения доступа в рамках DRF. Делать их нужно в файле settings.py проекта. 
# Для этого в словарь REST_FRAMEWORK нужно добавить еще один элемент:
# 'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]
#Так как там есть строка IsAuthenticated, то доступ к данным будет предоставлен только авторизованным пользакам. Этот пермишн срабатывает по умолчанию если нет какиих либо других пермишн. Если есть в классе другие пермишн, то срабатывают они. Если пермишн нет, то срабатывает глобальный пермишн. 
#Изначально в DRF пермишн указан такой AllowAny. Но мы его теперь переопределили.

#11. Авторизация и аутентификация. Session-based authentication | Уроки по Django REST Framework!!!!!!!!!!!!!!!!
#Сделаем авторизацию и аутентификацию через api запросы.
# Среди встроенных в DRF:
# Session based authentication - аутентификация на основе сессий и cookies
# Token-based authentication - авторизация на основе токенов
# Или через сторонние сервисы:
# JSON Web Token (JWT) authentication - аутентификация на основе JWT-токенов
# Django REST framework OAuth - авторизация через социальные сети
# Ссылка на док-цию: https://www.django-rest-framework.org/api-guide/authentication/
# ЧТобы не потеряться какой способ авторизации выбрать нужно понимать их принцип работы, свойства и сильные и слабые стороны и когда какой способ применяется. 

#Один из первых способов авторизации основывается на куки браузера и сессиях сервера. 
# В DRF она встроена
# Перейдем в urls.py и пропишем там маршурт для авторизации. 
# path('api/v1/drf-auth/', include('rest_framework.urls'))
# в нем дополнительно есть 2 маршрата login и logout. Их можно прописать после api/v1/drf-auth/
# после авторизации идет переадресация в profile. Но стандартного маршрута туда нет. 
#на странице DRF стандартных вьюшек, есть кнопка для выхода - logout. 


#12. Аутентификация по токенам. Пакет Djoser | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!
# В Django REST Framework популярны два подхода при реализации токенов:
#
# стандартная аутентификация токенами (библиотека Djoser);
# JWT-токены (библиотека Simple JWT).
#В DRF есть встроенный функционал реализации авторизации по токенам. Сторонние библиотеки можно не юзать.
# Ссылка на док-цию: https://www.django-rest-framework.org/api-guide/authentication/
# Там многое самим делать нужно будет. Но можно юзать библиотеку djoser, в ней уже много реализовано. И можно все брать и использовать.
#авторизация по токенам.
#Логика авторизации по токенам:
#Пользак в форме вводит логи и пароль. Сервер сверяет их с БД, если такие логин и пароль есть, то создает токен и связывает с ID пользака и записывает его в БД. Потом отдает этот токен пользователю, пользак его сохраняет в локальное хранилище. Потом когда пользак будет заходить на защищеный ресурс сайта, то он в запросе в заголовке http передает свой токен. Сервер сверяет токен с БД и понимает что это за пользователь, и дает доступ пользаку. Токен может отправлять любой клиент, то есть с любого устройства или приложения, в разных приложениях клиентом может выступать разные приложения другие. Обычно время жизни больше у таких токенов. При выходе из системы токен удаляет из БД. 1 токен может использоваться разными устройствами.
# Док-ция к Djoser: https://djoser.readthedocs.io/en/latest/
# Подключение djoser!!!!!!!
# В файле settings.py в коллекции INSTALLED_APPS добавить djoser. Мы также и добавим стандартную аутентификацию 'rest_framework.authtoken'
# INSTALLED_APPS = [
#     ...
#
#     'rest_framework.authtoken',
#     'djoser',
# ]
#Потом нужно сделать миграции, можно сразу python manage.py migrate написать, без makemigrations.
#Далее в urls.py нужно прописать 2 строки:
# path('api/v1/auth/', include('djoser.urls')),          # new
# re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
# re_path нужно импортировать также
#также нужно дописать словарь в коллекции REST_FRAMEWORK в файле settings.py
# REST_FRAMEWORK = {
#     ...
# 'DEFAULT_AUTHENTICATION_CLASSES': [
#     'rest_framework.authentication.TokenAuthentication',
#     'rest_framework.authentication.BasicAuthentication',
#     'rest_framework.authentication.SessionAuthentication',
# ]
# }
#По умолчанию DRF юзает аутентификацию по сессиям.
#перейдем по ссылке: http://127.0.0.1:8000/api/v1/auth/
# Там будет ссылка список пользователей которые зареганы в системе.
# "http://127.0.0.1:8000/api/v1/auth/users/"
# С помощью djoser можно регать, изменять, удалять пользаков. В нем много функционала.
# В док-ции есть инфа по базовым эндпоинтам base endpoints.
#Например для регистрации пользака нужно отправить пост запрос по ссылке: http://127.0.0.1:8000/api/v1/auth/users/
# Можно это сделать через postman. Возьмем эту ссылку, и сделаем пост запрос, передав в body данные формы, на вкладке form-data.
#заполним эти поля ключи
# username
# password
# email
# и соответственно значения к ним
# seconduser
# JxtymCkj;ysqGfhjkm777
# seconduser@mail.ru
#Остальные действия также можно выполнять. В док-ции есть ссылки которые можно юзать в этой библиотеке. Через постман можно по ним переходить и что-то делать.
#эти маршруты прописаны в этой строке:
# re_path(r'^auth/', include('djoser.urls.authtoken')),
#то есть auth/ и далее подключен пакет djoser.urls.authtoken, в нем много разных маршрутов.
#в док-ции есть раздел для авторизации: Token Endpoints
# https://djoser.readthedocs.io/en/latest/token_endpoints.html
# Там можно посмотреть ссылку для авторизации
# http://127.0.0.1:8000/auth/token/login/
# Отправляем через постман на нее пост запрос. Также переходим на вкладку body и заполняем форму form-data
# username - seconduser
# password - JxtymCkj;ysqGfhjkm777
# После отправки будет djoser возвращает токен: {"auth_token":"efd502ddc04a1c8fd6768f666ee1fcf65e840ffc"}
# с помощью него можно будет пройти аутентификацию пользака
# Пропишем в GoodsAPIUpdate пермишн IsAuthenticated. Это значит изменять может только аутентифицированный пользак. Без авторизации не будет отображаться позиции.
# Чтобы в постмане можно было просмотреть с авторизацией, нужно зайти на вкладку Headers (заголовки), и там прописать название токена в колонку Key Authorization, и в колонку Value нужно написать: Token efd502ddc04a1c8fd6768f666ee1fcf65e840ffc. То есть слово Token и наш токен который нам был возвращен ранее когда мы через постман ввели логин и пароль. 
# Authorization: Token efd502ddc04a1c8fd6768f666ee1fcf65e840ffc
# Теперь если сделать гет запрос с этими данными, то получим нужную запись, так как будет считаться что мы авторизованы. Как будто зашли через браузер с заголовком Authorization: Token efd502ddc04a1c8fd6768f666ee1fcf65e840ffc.
# Чтобы сделать выход из системы, нужно сделать пост запрос в постмане по ссылке: http://127.0.0.1:8000/auth/token/logout/
# И также нужно передать заголовок Authorization: Token efd502ddc04a1c8fd6768f666ee1fcf65e840ffc. Это нужно для того чтобы сервер понимал какой пользователь выходит из системы. Будет возвращен пустой ответ. Если он пустой и нет ошибок, значит все хорошо прошло. 
# Если после выхода по токену зайти по этому же токену, то будет ошибка в виде ответа: 
# {
#     "detail": "Недопустимый токен."
# }
# Это означает что мы вышли из системы, скорее всего наш токен просто удален из базы, поэтому ошибка. 

# Также в классах представлений можно указываь способ аутентификации пользака. 
# Например в классе можно прописать атрибут: authentication_classes = (TokenAuthentication, )
# Это будет означать что тут аутентификацию идет только по токенам. По сессиям уже нельзя. 
# На данный момент путь path('api/v1/drf-auth/', include('rest_framework.urls')), это авторизация по сессиям. Она в DRF по умолчанию реализована. Если сейчас авторизуемся как ранее мы это делали, то уже срабатывать GoodsAPIUpdate не будет, так как там прописали authentication_classes = (TokenAuthentication, )
# Перейдем по ссылке: http://127.0.0.1:8000/api/v1/good/1/
# и будет возвращен json:
# {
#     "detail": "Учетные данные не были предоставлены."
# }
# Если закоментировать строку: authentication_classes = (TokenAuthentication, )
# то ошибка в браузере сразу пропадет. И наша аутентификация сразу сработает. 


#13. Идея авторизации по JWT-токенам | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!!!!!!
# пример JWT-токена:
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4NjgxOTAzLCJqdGkiOiJlNzM2N2MxZTY4YTc0ZTI2YjA5ZDkwZDQyZjc2MDBkZSIsInVzZXJfaWQiOjV9.a-OlrfisMAEB5VKyoarOI_eWQFwN6KOy2Bvg7iQ9uDs
# Есть в нем 3 раздела:
# header – заголовка;
# payload – полезные данные;
# signature – подпись.
# Они разделены точками в токене. 
# Фрагменты header и payload – это обычные JSON-строки, закодированные алгоритмом base64 в последовательность ASCII-букв и цифр. А signature – это фрагмент шифрования строки «header.payload», например, с помощью алгоритма HS256 с использованием секретного ключа:
# header = base64urlEncode(b'') - {"alg": "HS256", "typ": "JWT"}
# alg - алгоритм шифрования.
# typ - тип токена.
# payload = base64urlEncode(b'') - {"userid": 1, "exp": 1000, "email": "user@mail.ru"}
# userid - ид пользака
# exp - время жизни токена
# email - почта пользака
# в payload можно записывать и другие данные. Но желательно нечувствительные. 
# Эти json строки кодируются с помощью алгоритма base64. То есть не зашифрованы, а просто закодированы, то есть представлены в другом виде. Их можно обратно раскодировать без ключей. То есть данные в JWT не защинены от просмотра. Но изменить данные нельзя в них, так как есть третья составляющая signature.

# signature = HMAC-SHA256(header.payload, SECRET_KEY)
# тут в signature берется header и payload объединяются в единую строку через точку скорее всего, и затем шифруется с использованием алогоритма шифрования который указали в header, алгоритм HS256 шифрует с использование SECRET_KEY, который мы также укажем в коде. 
# Также сервер потом может проверять подпись, сервер шифрует хедер и пейлоад из полученного токена и зашифрованную строку сверяет с подписью из БД, если они сходятся, то значит данные не изменены. 
# С помощью такого способа мы можем защитить данные от изменения

# Затем, полученные три фрагмента объединяются через точку и получается JWT-токен:
# jwt_token = header.payload.signature

# Алгоритмы авторизации могут отличаться. 
# Общая идея JWT токенов
# Это нужно для авторизации в связанных между собой сервисах. Например гугл, ютуб, гмаил и тд.
# Если бы не было jwt, то во всех таких сайтах пришлось бы дублровать функционал по запросам к единой дб, а это затратно и сложно. 

# Теперь, когда мы познакомились со структурой JWT-токенов, посмотрим, на процесс авторизации и аутентификации с их помощью. Но сразу отмечу, что конкретные алгоритмы авторизации могут несколько отличаться, поэтому я расскажу общую идею JWT-токенов.

# Первый вопрос здесь, зачем вообще понадобилось изобретать новый тип токенов? Разве не хватало прежних? Не хватало. Например, когда единая учетная запись используется множеством независимых сервисов, как это сделано в компании Google. Нам достаточно один раз авторизоваться (ввести логин/пароль) и мы получаем доступ ко всему его инструментарию. Реализовать это на уровне обычных токенов было бы неудобно, так как каждый сервис должен был бы получать доступ к БД с токенами пользователя, добавлять и удалять их. То есть, сервисы уже не были бы полностью независимыми, им пришлось бы дублировать некоторый функционал, а это источник многих потенциальных ошибок и проблем.

# В связи с этим и была придумана несколько иная схема авторизации пользователей. Вначале клиент, естественно, должен пройти процедуру авторизации. Для этого сервис перенаправляет его запрос на сервер авторизации, который функционирует в рамках всего инструментария компании. Если учетные данные пользователя оказались корректными, то сервер возвращает пользователю два JWT-токена, которые мы обозначим, как access_token и refresh_token. Дополнительно refresh_token сохраняется в БД сервера авторизации, а на стороне клиента оба: access_token и refresh_token.

# Зачем нужны два токена, вы сейчас поймете. Для доступа к сервисам используется первый access_token, который имеет короткое время действия, например, 5 минут. Так как access_token содержит в себе информацию о пользователе, а также цифровую подпись, то сервис «понимает» какой пользователь запрашивает доступ и, кроме того, имеет возможность проверить корректность токена по его подписи, так как все сервисы «знают» секретный ключ, которым были закодированы данные пользователя. То есть, прямая подмена данных в access_token со стороны злоумышленника очень непростая задача.

# Хорошо, но если access_token достаточно, чтобы пройти аутентификацию на сервисах, то почему его время действия так ограничено? Давайте пользоваться им постоянно и не усложнять алгоритм авторизации? Так можно было бы сделать, если бы не было злоумышленников, которые могут украсть access_token и получить постоянный доступ к сервисам. И, так как гарантированно защититься от кражи невозможно, то разработчики решили, просто ограничить время жизни access_token.

# Ладно, хорошо, но тогда по истечении 5 минут пользователю снова придется вводить логин/пароль для авторизации в сервисах, чтобы получить новый access_token на следующие 5 минут? Согласитесь, перспектива не очень приятная? Поэтому и существует второй refresh_token, который имеет заметно большее время жизни от суток и более. Когда время действия access_token заканчивается на сервер авторизации отправляется refresh_token и пользователю назначаются новые access_token и refresh_token. Обратите внимание, refresh_token тоже меняется при запросе нового access_token. Соответственно в БД и локальном хранилище на стороне клиента эти токены обновляются. Так происходит защита сервисов при краже access_token.

# Конечно, злоумышленник и за несколько минут может наделать делов в наших профайлах, но так мы имеем хоть какую-то защиту от взлома. Согласитесь, это лучше, чем если бы третьи лица получали доступ на гораздо больший срок. Ну а абсолютной гарантии от взлома все равно ни одна система не может обеспечить. Поэтому, соблюдайте цифровую гигиену и защищайте свои данные от хакерских атак. Включайте двойную авторизацию по логину/паролю и СМС на критических сервисах, например, банковских, госуслугах, брокерских счетах и т.п. Другого человечество еще не придумало.

# Но внимательный зритель может заметить, что злоумышленник также может украсть и refresh_token. Тогда он получает постоянный доступ в сервисы под нашими учетными данными! Да, и это самый неприятный момент в этом алгоритме. Злоумышленник сможет использовать refresh_token, пока честный пользователь явно не разлогиниться (выйдет из системы). В этом случае, все refresh_token этого пользователя помечаются как недействительные и злоумышленник не сможет продлить access_token. Ему придется уже вводить логин/пароль, которые он, скорее всего, не будет знать.

# Вот общая схема работы JWT-токенов. Опять же, конкретная реализация алгоритмов авторизации/аутентификации может отличаться. Здесь по разному можно организовывать БД для хранения refresh_token, а иногда и access_token. По разному сохранять их на стороне клиента, защищая дополнительно refresh_token от кражи. И так далее. То есть, конкретные реализации в разных системах могут заметно отличаться.

# Ну, и, конечно же, открытый вопрос, нужно ли именно вам в ваших проектах использовать JWT-токены? На мой взгляд, на простых сайтах, которые лишь взаимодействуют с большим числом различных клиентов (браузеров, смартфонов, носимой электроники и т.п.), достаточно применять обычные токены. И на практике именно так и делают. Большинство сайтов при реализации API используют простую авторизацию и аутентификацию по токенам и этого вполне достаточно. JWT-токены имеют несколько специфические приложения. Конечно, для крупных компаний со множеством независимых сервисов, это один из вариантов авторизации. Но и в небольших проектах им тоже есть место. Например, на файлообменниках можно организовать временный доступ к скачиваемому файлу, как раз, через JWT-токен. При этом refresh_token можно совсем отбросить и не использовать. Возможны и другие частные приложения. Хотя, я не стану выступать в роли оракула и наперед предсказывать ограниченность применения этой новой идеи авторизации. Кто знает, возможно, через некоторое время она станет доминирующей при реализации алгоритмов авторизации во многих сервисах? Но пока она имеет свою небольшую нишу, где и применяется.

# Теория есть также тут: https://proproprogs.ru/django/drf-ideya-avtorizacii-po-jwt-tokenam


#14. Делаем авторизацию по JWT-токенам | Уроки по Django REST Framework!!!!!!!!!!!!!!!!!!!!!
# Теория тут: https://proproprogs.ru/django/drf-delaem-avtorizaciyu-po-jwt-tokenam
# Ссылка на док-цию в DRF: https://www.django-rest-framework.org/api-guide/authentication/#third-party-packages
# Можно юзать библиотеку Simlpe JWT. Она также работает в связке с Djoser. Работает она для DRF.
# Ссылка на док-цию по Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
# Установка:
# pip install djangorestframework-simplejwt
# Затем, в файле settings.py в словаре REST_FRAMEWORK прописать возможность авторизации через JWT-токены:

# REST_FRAMEWORK = {
#     ...
 
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         ...
#     ]
# }
# строку 'rest_framework.authentication.TokenAuthentication', коментируем. Так как мы переходим на JWT. 
# Далее, в коллекцию urlpatterns в файле urls.py проекта добавим три маршрута (берем из документации):

# urlpatterns = [
#     ...
#     path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# ]
# Потом из док-ции по ссылке: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
# Нужно скопировать словарь SIMPLE_JWT и импортировать from datetime import timedelta, записать это в файл settings.py
#поправить там нужно SEVRET_KEY. Его можно прописать в отдельном файле с использованием .env файла. 

# ост 5 мин















