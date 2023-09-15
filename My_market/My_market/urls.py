"""
URL configuration for My_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from showcase.views import *
from regusers.views import *
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include('showcase.urls')),#тут указали стартовую страницу от которой будут идти все другие ссылки приложения
    path('', include('regusers.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#тут нужно будет дописать ссылки на корзину. так как корзина отдельное приложение

if settings.DEBUG:#в случае включенного режима дебага то есть DEBUG=True мы к маршрутам urlpatterns которые мы указали выше добавляем маршрут для статических данных графических файлов и указываем наш добавленный урл и корневую папку где будут храниться файлы, скорее всего static это функция такая. Делается это только в отладочном режиме, на реальных серверах это уже настроено, но у нас не настроено. static надо импортировать из django.conf.urls.static. DEBUG должен быть True. Теперь тестовый сервер может их брать по адресу media и отображать на html странице
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)