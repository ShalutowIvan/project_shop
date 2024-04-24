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
    path('synchronization_order/', synchronization, name='synchronization'),
    path('order_list/', Order_list.as_view(), name='order_list'),
    path('order_list/open/<int:order_number>/', order_list_open, name='order_list_open'),
    path('order_list/open/activate/<int:order_activate>/', order_list_activate, name='order_list_activate'),
    path('order_list/open/deactivate/<int:order_deactivate>/', order_list_deactivate, name='order_list_deactivate'),


    
    path('good_list/', Goods_list.as_view(), name='goods_list'),
    path('good_list/add/', Goods_add.as_view(), name='goods_add'),
    path('good_list/add_group/', Group_add.as_view(), name='group_add'),
    path('receipt/list/view/', receipt_list, name='receipt_list'),
    path('receipt/list/view/create/', receipt_document_create, name='receipt_document_create'),
    path('receipt/list/view/delete/<int:number_delete_receipt>/', receipt_document_delete, name='receipt_document_delete'),
    path('receipt/list/view/open/<int:open_receipt>/', receipt_document_open, name='receipt_document_open'),
    path('receipt/list/view/open/add_goods/<int:number_doc>/', receipt_add_goods, name='receipt_add_goods'),
    path('receipt/list/view/open/delete_goods/<int:number_delete_good>/', receipt_delete_goods, name='receipt_delete_goods'),
    path('receipt/list/view/open/activate/<int:receipt_activate>/', receipt_document_activate, name='receipt_document_activate'),
    path('receipt/list/view/open/deactivate/<int:receipt_deactivate>/', receipt_document_deactivate, name='receipt_document_deactivate'),
    
    # path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    # path('order/list/', Order_list_view.as_view(), name='order_list'),
    # path('order/list/<int:pk>', Order_list_view.as_view(), name='order_list_c'),

    path('api/get_good/', Get_good.as_view(), name='get_good'),
    path('api/get_group/', Get_group.as_view(), name='get_group'),
    path('api/get_order/', Get_order.as_view(), name='get_order'),

    ]