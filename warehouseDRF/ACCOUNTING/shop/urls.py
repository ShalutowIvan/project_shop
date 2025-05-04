from django.urls import path, re_path
from shop.views import *
from shop.views_receipt import *
from shop.views_expense import *
from shop.views_inventory import *


from shop.views_order_api import *
from shop.views_goods_api import *
from shop.views_receipt_api import *
from shop.views_expense_api import *
from shop.views_inventory_api import *
from shop.views_report_api import *

# app_name = 'showcase' #если прописать название приложения, то в шаблонах придется его везде дописать через двоеточие для каждоый ссылки функции. Возможно это будет понятнее если в проекте много приложений.

urlpatterns = [

    path('', Home.as_view(), name='start'),
    #заказы
    path('synchronization_order/', synchronization, name='synchronization'),
    path('order_list/', Order_list.as_view(), name='order_list'),
    path('order_list/completed/', order_completed, name='order_completed'),
    path('order_list/not_completed/', order_not_completed, name='order_not_completed'),

    path('order_list/open/<int:order_number>/', order_list_open, name='order_list_open'),
    path('order_list/open/activate/<int:order_activate>/', order_list_activate, name='order_list_activate'),
    path('order_list/open/deactivate/<int:order_deactivate>/', order_list_deactivate, name='order_list_deactivate'),
    #товары
    path('good_list/', Goods_list.as_view(), name='goods_list'),
    path('good_list/group_show/<slug:group_slug>/', group_show, name='group_show'),
    path('good_list/add/', Goods_add.as_view(), name='goods_add'),
    path('good_list/add_group/', Group_add.as_view(), name='group_add'),
    path('good_list/goods_modify/<int:good_id>/', goods_modify, name='goods_modify'),
    path('good_list/goods_delete/<int:good_id>/', goods_delete, name='goods_delete'),
    path('good_list/group_delete/', group_delete, name='group_delete'),
    path('good_list/select_group_to_transfer/<int:group_id>/', select_group_to_transfer, name='select_group_to_transfer'),
    
    path('good_list/load_file/', goods_load_file, name='goods_load_file'),
    path('good_list/load_file/url_from_load_template/', url_from_load_template, name='url_from_load_template'),


    #приходный документ
    path('receipt/list/view/', receipt_list, name='receipt_list'),
    path('receipt/list/view/create/', receipt_document_create, name='receipt_document_create'),
    path('receipt/list/view/delete/<int:number_delete_receipt>/', receipt_document_delete, name='receipt_document_delete'),
    path('receipt/list/view/open/<int:open_receipt>/', receipt_document_open, name='receipt_document_open'),
    path('receipt/list/view/open/add_goods/<int:number_doc>/', receipt_add_goods, name='receipt_add_goods'),
    path('receipt/list/view/open/delete_goods/<int:number_delete_good>/', receipt_delete_goods, name='receipt_delete_goods'),
    path('receipt/list/view/open/edit_goods/<int:number_edit_good>/', receipt_document_edit, name='receipt_document_edit'),
    path('receipt/list/view/open/activate/<int:receipt_activate>/', receipt_document_activate, name='receipt_document_activate'),
    path('receipt/list/view/open/deactivate/<int:receipt_deactivate>/', receipt_document_deactivate, name='receipt_document_deactivate'),
    path('receipt/list/receipt_load_file/<int:number_doc>/', receipt_load_file, name='receipt_load_file'),
    path('receipt/list/receipt_add_if_not_in_base/<int:number_good>/', receipt_add_if_not_in_base, name='receipt_add_if_not_in_base'),
    path('receipt/list/receipt_change_if_not_in_base/<int:number_good>/', receipt_change_if_not_in_base, name='receipt_change_if_not_in_base'),

    #расходный документ
    path('expense/list/view/', expense_list, name='expense_list'),
    path('expense/list/view/create/', expense_document_create, name='expense_document_create'),
    path('expense/list/view/delete/<int:number_delete_expense>/', expense_document_delete, name='expense_document_delete'),
    path('expense/list/view/open/<int:open_expense>/', expense_document_open, name='expense_document_open'),
    path('expense/list/view/open/add_goods/<int:number_doc>/', expense_add_goods, name='expense_add_goods'),
    path('expense/list/view/open/delete_goods/<int:number_delete_good>/', expense_delete_goods, name='expense_delete_goods'),
    path('expense/list/view/open/activate/<int:expense_activate>/', expense_document_activate, name='expense_document_activate'),
    path('expense/list/view/open/deactivate/<int:expense_deactivate>/', expense_document_deactivate, name='expense_document_deactivate'),
    #отчеты
    path('reports/', reports, name='reports'),
    path('reports/income_report/', income_report, name='income_report'),
    path('reports/expense_report/', expense_report, name='expense_report'),
    path('reports/sales_report/', sales_report, name='sales_report'),
    path('reports/sales_report_summary/', sales_report_summary, name='sales_report_summary'),

    #инвентаризация
    path('inventory/list/view/', inventory_list, name='inventory_list'),
    path('inventory/list/view/create/', inventory_create, name='inventory_create'),
    path('inventory/list/view/open/<int:inv_number>/', inventory_open, name='inventory_open'),
    path('inventory/list/view/delete/<int:inv_number>/', inventory_delete, name='inventory_delete'),
    path('inventory/list/view/add_group/<int:inv_number>/', inventory_add_group, name='inventory_add_group'),
    path('inventory/list/view/activate/<int:inv_number>/', inventory_activate, name='inventory_activate'),
    path('inventory/list/view/deactivate/<int:inv_number>/', inventory_deactivate, name='inventory_deactivate'),
    path('inventory/list/view/receipt_load_file/<int:inv_number>/', inventory_load_file, name='inventory_load_file'),
    # path('inventory/list/view/delete_position/<int:id_good_in_inventory>/', inventory_delete_position, name='inventory_delete_position'),
    path('inventory/list/url_from_load_template_inv/', url_from_load_template_inv, name='url_from_load_template_inv'),
    path('inventory/list/url_from_load_error_inv/', url_from_load_error_inv, name='url_from_load_error_inv'),
    path('inventory/list/url_from_load_inventory/<int:inv_number>/', inventory_print, name='inventory_print'),
    path('inventory/list/delete_position_if_not_in_base/<int:id_good>/', inventory_delete_position_if_not_in_base, name='inventory_delete_position_if_not_in_base'),
    path('inventory/list/inventory_add_if_not_in_base/<int:number_good>/', inventory_add_if_not_in_base, name='inventory_add_if_not_in_base'),
    path('inventory/list/inventory_change_if_not_in_base/<int:number_good>/', inventory_change_if_not_in_base, name='inventory_change_if_not_in_base'),
    path('inventory/list/view/update_quantity/<int:number_inv>/', inventory_update_quantity, name='inventory_update_quantity'),
    path('inventory/list/view/add_all_buffer/<int:number_inv>/', inventory_add_all_buffer, name='inventory_add_all_buffer'),

    # path('group/<slug:group_slug>/', GroupShow.as_view(), name='group'),
    # path('order/list/', Order_list_view.as_view(), name='order_list'),
    # path('order/list/<int:pk>', Order_list_view.as_view(), name='order_list_c'),
    #тут будут апишные функции
    #заказы
    path('api/get_order/', Get_order.as_view(), name='get_order'),
    path('api/get_order/<int:order_number>/', Get_order_open.as_view(), name='get_order_open'),
    path('api/get_order_completed/', Get_order_completed.as_view(), name='get_order_completed'),
    path('api/get_order_not_completed/', Get_order_not_completed.as_view(), name='get_order_not_completed'),
    path('api/order_list/open/activate/<int:order_activate>/', api_order_list_activate, name='api_order_list_activate'),
    path('api/order_list/open/deactivate/<int:order_deactivate>/', api_order_list_deactivate, name='api_order_list_deactivate'),



    #товары
    path('api/get_good/', Get_good.as_view(), name='get_good'),
    path('api/get_group/', Get_group.as_view(), name='get_group'),    
    path('api/get_good_in_group/<slug:group_slug>/', Get_good_in_group.as_view(), name='get_good_in_group'),
    path('api/add_group/', Group_add_api.as_view(), name='add_group'),    
    path('api/add_good/', Goods_add_api.as_view()),    
    path('api/add_good/load_file/', Goods_load_file_api.as_view()),    
    path('api/add_good/url_from_load_template/', url_from_load_template_api),    
    path('api/upload-images/', BulkImageUploadView.as_view(), name='bulk-image-upload'),
    path('api/clean-unused-files/', CleanUnusedFilesView.as_view(), name='clean-unused-files'),
    path('api/delete_group/', Group_delete_api.as_view(), name='delete_group'),
    path('api/select_group_to_transfer/<int:group_id>', Select_group_to_transfer_api.as_view(), name='select_group_to_transfer'),
    path('api/group_without_delete/<int:group_id>', group_without_delete, name='group_without_delete'),
    path('api/goods_modify/<int:good_id>', Goods_modify_api.as_view(), name='goods_modify'),
    path('api/load_good_to_modify/<int:good_id>', load_good_to_modify, name='load_good_to_modify'),
    path('api/goods_delete/<int:good_id>', goods_delete, name='goods_delete'),
    path('api/products_find/', ProductListAPIView.as_view(), name='products_find'),
    



    #приходные документы
    path('api/receipt_list_view/', Get_receipt_list.as_view(), name='receipt_list_view'),
    #расходные документы
    path('api/expense_list_view/', Get_expense_list.as_view(), name='expense_list_view'),
    #инвентаризация
    path('api/inventory_list_view/', Get_inventory_list.as_view(), name='inventory_list_view'),
    #отчеты



    ]