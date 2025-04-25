import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *


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


class Expense_number_serializer(serializers.ModelSerializer):
    class Meta:
        model = Expense_number

        fields = "__all__"




