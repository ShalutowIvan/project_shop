from django.contrib import admin
from .models import *
# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_product', 'price', 'stock', 'availability')#это для отображения ссылок для перехода на нужные поля сайта
	list_display_links = ('id', 'name_product')#это для отображения ссылок для перехода на нужные поля сайта
	search_fields = ('name_product', )#это инфа по каким полям будет идти поиск. Далее идем в файл models.py для уазания названия полей на русском языке. 
	list_editable = ('availability',)#это чтобы через админку можно было редачить этот параметр
	list_filter = ('group', )#для фильтра по этим параметрам в админке
	prepopulated_fields = {"slug": ("name_product",)}


admin.site.register(Goods, GoodsAdmin)#можно регать и декоратором. Декоратор можно юзать к классу


class GroupAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_group')
	list_display_links = ('id', 'name_group')
	search_fields = ('name_group',)#обязательно нужно передавать кортеж, а не просто строку в скобках
	prepopulated_fields = {"slug": ("name_group", )}

admin.site.register(Group, GroupAdmin)


class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_org', 'inn_kpp', 'ogrn', 'working_mode', 'adres', 'phone', 'email_name', 'telegram', 'whatsApp')
	list_display_links = ('id', 'name_org')#это для отображения ссылок для перехода на нужные поля сайта
	search_fields = ('name_org', 'about')#это инфа по каким полям будет идти поиск. Далее идем в файл models.py для уазания названия полей на русском языке.         
	# prepopulated_fields = {"slug": ("name_org",)}


admin.site.register(Organization, OrganizationAdmin)


# class Order_list_want_byAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name_product', 'price', 'quantity', 'availability')
# 	list_display_links = ('id', 'name_product')
# 	search_fields = ('name_product', )
# 	list_filter = ('group', )
#
#
# admin.site.register(Order_list_want_by, Order_list_want_byAdmin)


class Order_list_boughtAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_product', 'price', 'quantity',)
	list_display_links = ('id', 'name_product')
	search_fields = ('name_product', )
	list_filter = ('group', )


admin.site.register(Order_list_bought, Order_list_boughtAdmin)


class BasketsAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'product', 'price', 'quantity', 'availability')
	list_display_links = ('id', 'product')
	search_fields = ('user', 'product' )


admin.site.register(Baskets, BasketsAdmin)


# class OrderAdmin(admin.ModelAdmin):
# 	list_display = ('fio', 'phone', 'e_mail', 'delivery_address', 'pay')
# 	list_display_links = ('fio',)
# 	search_fields = ('user', 'fio')

# admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
	list_display = ('payment',)
	list_display_links = ('payment',)

admin.site.register(Payment, PaymentAdmin)





