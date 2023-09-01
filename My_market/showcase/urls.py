from django.urls import path, re_path
from showcase.views import *

# app_name = 'showcase' #если прописать название приложения, то в шаблонах придется его везде дописать через двоеточие для каждоый ссылки функции. Возможно это будет понятнее если в проекте много приложений.

urlpatterns = [#тут подключаем все ссылки которые будут идти после корневой ссылки из файла urls.py из папки с проектом
	path('', GoodsHome.as_view(), name='start'),
    path('basket/', basket, name='basket'),
    path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('baskets/<int:product_id>/', add_in_basket, name='add_in_basket'),#в шаблоне буде прописана название ссылки и цифра id продукта просто через пробел и будет срабатывать как ссылка
    path('admin/', adminka, name='adminka'),
    path('clear_basket/', clear_basket, name='clear_basket'),
    # path('group/<str:name_product>/', add_in_basket, name='add_in_basket'),
    # path('product/<slug:product_slug>/', show_product, name='product')
    ]