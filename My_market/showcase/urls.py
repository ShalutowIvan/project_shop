from django.urls import path, re_path
from showcase.views import *

# app_name = 'showcase' #если прописать название приложения, то в шаблонах придется его везде дописать через двоеточие для каждоый ссылки функции. Возможно это будет понятнее если в проекте много приложений.

urlpatterns = [#тут подключаем все ссылки которые будут идти после корневой ссылки из файла urls.py из папки с проектом
	path('', GoodsHome.as_view(), name='start'),
    path('basket/', basket_view, name='basket_view'),
    path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    path('login/', LoginUser.as_view(), name='login'),

    path('register/', RegisterUser.as_view(), name='register'),
    #урл регистрации с подтвержлением почты
    # path('register/', signup, name='register'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),


    path('logout/', logout_user, name='logout'),
    path('baskets/<int:product_id>/', add_in_basket, name='add_in_basket'),#в шаблоне буде прописана название ссылки и цифра id продукта просто через пробел и будет срабатывать как ссылка
    path('admin/', adminka, name='adminka'),
    path('baskets/clear_basket/<int:basket_id>/', clear_basket, name='clear_basket'),
    path('contacts/', Get_contacts.as_view(), name='contacts'),    
    path('checkout/', checkout, name='checkout'),
    path('checkout_list/', checkout_list, name='checkout_list'),
    # path('confirm_email/', confirm_email, name='confirm_email'),

    # path('group/<str:name_product>/', add_in_basket, name='add_in_basket'),
    # path('product/<slug:product_slug>/', show_product, name='product')
    ]