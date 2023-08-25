from django.urls import path, re_path
from showcase.views import *


urlpatterns = [#тут подключаем все ссылки которые будут идти после корневой ссылки из файла urls.py из папки с проектом
	path('', GoodsHome.as_view(), name='start'),
    path('basket/', basket, name='basket'),
    path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    # path('group/<str:name_product>/', add_in_basket, name='add_in_basket'),
    # path('product/<slug:product_slug>/', show_product, name='product')
    #для групп сделать

]