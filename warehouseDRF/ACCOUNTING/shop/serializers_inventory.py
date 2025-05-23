import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from .serializers_goods import GoodsSerializer


# class Order_number_Serializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     fio = serializers.CharField(max_length=255)        
#     order_number = serializers.IntegerField()
#     time_create = serializers.DateTimeField()#время создания заказа покупателем    
#     state_order = serializers.BooleanField()


# class Order_open_Serializer(serializers.ModelSerializer):
#     product_id = GoodsSerializer(many=False, read_only=True)

#     # user = serializers.HiddenField(default=serializers.CurrentUserDefault())#это чтобы поле с пользаком скрывалось при добавлении через форму в урлке от джанго, которое мы делаем через форму вьюшки. Мы тут создаем скрытое поле, и там по умолчанию прописываем текущего пользака. 
#     class Meta:
#         model = Order_list_bought#тут пишем модель с которой будем работать
#         # fields = ("name_product", "slug", "vendor_code", "price", "stock",  "group" )#тут пишем какие поля будем возвращать обратно клиенту. Причем тут поля с внешним ключем не нужно прописывать с _id. Пользак будет видеть число, а не группу из поля group. Также сразу доступны все виды запросов пост, гет и тд. Затрагиваться будут те поля, которые мы пропишем в запросах. 
#         #если нужно указать все поля в сериализаторе, то вручную их можно не писать.
#         # fields = "__all__"#вот если прописать, то в сериализатор будут попадать все поля. 
#         #сериализация с фото не работает почему то
#         fields = ('fio', 'phone', 'quantity', 'order_number', 'time_create', 'delivery_address', 'product_id')#product_id не стал записывать с ним проблема, так как он не совпадает с id товаров из фастапи


class Inventory_number_serializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_number

        fields = "__all__"


class Goods_in_group_add_Serializer(serializers.ModelSerializer):    

    class Meta:
        model = Group
        
        fields = ("name_group",)


class Inventory_list_serializer(serializers.ModelSerializer):    
    product = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = Inventory_list

        fields = "__all__"

        
#2 сериализатора ниже относятся к редактированию колва. Сюда возможно добавится цена...
class Inventory_update_good_serializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity_new = serializers.IntegerField(min_value=0)
    # customPrice = serializers.FloatField(min_value=0)#это поле для получения цены ее потом записываем в связанное поле из таблицы товара - цена


class Inventory_save_good_serializer(serializers.Serializer):
    items = Inventory_update_good_serializer(many=True)




class Inventory_list_buffer_serializer(serializers.ModelSerializer):    

    class Meta:
        model = Inventory_buffer

        fields = "__all__"


#для поиска товара для замены товара из буфера
class Inventory_change_good_serializer(serializers.Serializer):
    good_name = serializers.CharField(max_length=255)   