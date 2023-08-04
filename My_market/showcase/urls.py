from django.urls import path, re_path
from showcase.views import *


urlpatterns = [#тут подключаем все ссылки которые будут идти после корневой ссылки из файла urls.py из папки с проектом
	path('', product, name='start'),
    path('basket/', basket, name='basket'),


]