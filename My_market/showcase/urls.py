from django.urls import path, re_path
from showcase.views import *


urlpatterns = [#тут подключаем все ссылки которые будут идти после корневой ссылки из файла urls.py из папки с проектом
	path('', all_group, name='all_group'),
    path('basket/', basket, name='basket'),
    path('group/<slug:group_slug>/', show_group, name='group')
    # path('product/<slug:product_slug>/', show_product, name='product')
    #для групп сделать

]