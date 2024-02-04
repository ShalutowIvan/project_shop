"""
URL configuration for ACCOUNTING project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from shop.views import *
from regusers.views import *
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
#для jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


# class MyCustomRouter(routers.SimpleRouter):#наследуемся от симплроутера и прописываем свои параметры
#     #сначала определяем атрибут routes, это список из маршрутов. Каждый элемент списка это объект класса Route. Каждый класс определяет 1 отдельный маршрут. 
#     # url - это шаблон маршрута, там используются регулярные выражения. В нашем случае адреса определены без обратного слеша в конце ссылки. Если дописать обратный слеш, то в нашем случае будет ошибка в браузере. Браузер обратный слеш сам дописывает часто в конце. Можно пробовать еще в постмане открывать ссылки.
#     # mapping - связывается тип запроса с соответствующим методом вьюсета и указывает сам тип запроса
#     # name - определяет название маршрута
#     # detail - указывает на то что это будет список или отдельная запись. То есть будет возвращать список из БД или одну запись. 
#     # initkwargs - это доп аргументы для коллекции kwargs, которые передаются конкретному определению при срабатывании маршрута. 
#     routes = [
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get': 'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'List'}),
#         routers.Route(url=r'^{prefix}/{lookup}$',
#                       mapping={'get': 'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix': 'Detail'})
#     ]

# #далее чтобы подключить роутер нужно прописать его ниже. Вместо DefaultRouter пишем MyCustomRouter. И далее его также регистрируем и добавляем в список урл через include в path



# # router = routers.SimpleRouter()
# # router = routers.DefaultRouter()
# router2 = MyCustomRouter()
# # router.register(r'good', GoodsViewSet, basename="tovar")
# # router.register(r'good', GoodsViewSet, basename='goods')
# router2.register(r'good', GoodsViewSet, basename='goods')
# print(router2.urls)#коллекция урл



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/goodlist/', GoodsAPIList.as_view()),
    # path('api/v1/goodlist/<int:pk>/', GoodsAPIUpdate.as_view()),
    # path('api/v1/gooddetail/<int:pk>/', GoodsAPIDetail.as_view()),
    # path('api/v1/goodlist/', GoodsViewSet.as_view({'get': 'list'})),
    # path('api/v1/goodlist/<int:pk>/', GoodsViewSet.as_view({'put': 'update'})),
    # path('api/v1/', include(router.urls)), #http://127.0.0.1:8000/api/v1/good/# то есть в конце урл дописывается строка (префикс) из роутера, то есть api/v1/ + good. urls - это набор маршрутов (коллекция) из вью сета. 
    # path('api/v1/', include(router2.urls)),
    # path('api/v1/drf-auth/', include('rest_framework.urls')),
    # path('api/v1/good/', GoodsAPIList.as_view()),
    # path('api/v1/good/<int:pk>/', GoodsAPIUpdate.as_view()),
    # path('api/v1/gooddelete/<int:pk>/', GoodsAPIDestroy.as_view()),
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    # #авторизация jwt
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('shop.urls')),#тут указали стартовую страницу от которой будут идти все другие ссылки приложения
    path('', include('regusers.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)