from django.urls import path, re_path
from shop.views import *

# app_name = 'showcase' #если прописать название приложения, то в шаблонах придется его везде дописать через двоеточие для каждоый ссылки функции. Возможно это будет понятнее если в проекте много приложений.

urlpatterns = [
	# path('', GoodsHome.as_view(), name='start'),
    # path('basket/', basket_view, name='basket_view'),
    # path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    # path('baskets/<int:product_id>/', add_in_basket, name='add_in_basket'),
    # path('admin/', adminka, name='adminka'),
    # path('baskets/clear_basket/<int:basket_id>/', clear_basket, name='clear_basket'),
    # path('contacts/', Get_contacts.as_view(), name='contacts'),    
    # path('checkout/', checkout, name='checkout'),
    # path('checkout_list/', checkout_list, name='checkout_list'),
    # path('search/', SearchGood.as_view(), name='search'),
    

    # path('group/<str:name_product>/', add_in_basket, name='add_in_basket'),
    # path('product/<slug:product_slug>/', show_product, name='product')
    path('', Home.as_view(), name='start'),
    path('order_list/', Order_list.as_view(), name='order_list'),
    path('synchronization_order/', synchronization, name='synchronization'),
    path('good_list/', Goods_list.as_view(), name='goods_list'),
    path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    # path('order/list/', Order_list_view.as_view(), name='order_list'),
    # path('order/list/<int:pk>', Order_list_view.as_view(), name='order_list_c'),

    path('api/get_good/', Get_good.as_view(), name='get_good'),
    # path('api/get_good2/', get_good, name='get_good2'),
    ]