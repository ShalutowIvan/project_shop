import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from .serializers_goods import GoodsSerializer

# class GoodsModel:#имитация модели. У нас будут объекты этого класса
#     def __init__(self, name_product, slug):
#         self.name_product = name_product
#         self.slug = slug


# class GoodsSerializer(serializers.ModelSerializer):#пишем сериализатор для проверки данных при выдаче их пользаку. Проверяем таблицу Goods
    
#     class Meta:
#         model = Goods
#         fields = ('name_product', 'group')


# class GoodsSerializer(serializers.Serializer):#этот клас будет преобразовывать модель GoodsModel в JSON формат. Наследуется от класса Serializer
#     #класс Meta напрямую работает с моделями. А теперь напрямую с моделями мы не можем работать так как испоьзуем класс Serializer как базовый. Определить нужно здесь 2 атрибута
#     name_product = serializers.CharField(max_length=255)#сериализация первого поля в строковый тип. То есть теперь при поступлении данных у них будет проверяться длинна и преобразовываться. 
#     slug = serializers.CharField(max_length=255)#тут аналогично. Если в скобках ничего не прописать, то проверка будет только на тип данных.


#чтобы посмотреть как работает сериализатор, сделем обычную функцию для преобразования модели в json
# def encode():
#     model = GoodsModel('Товар', 'tovar')
#     model_sr = GoodsSerializer(model)#тут объект сериализации, а не байтовая json строка. Ниже сделаем Json строку
#     print(model_sr.data, type(model_sr.data), sep='\n')#тут мы смотрим что у нас будет выведено. 
#     json = JSONRenderer().render(model_sr.data)#JSONRenderer нужно импортировать. JSONRenderer преобразует объект сериализации в байтовую JSON строку. 
#     print(json)

#функцию encode можно проверить только через оболочку shell через файл проекта manage.py. Так как просто так файл serializers.py не запускается. И функцию просто так нельзя запускать. Чтобы зайти в оболочку нужно в cmd прописать python manage.py shell. Потом импортировать там функцию encode и потом ее можно запускать там же в оболочке. 
# наша функция вернут следующее:
# {'name_product': 'Товар', 'slug': 'tovar'}#здесь преобразован объект в обычный словарь
# <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
# b'{"name_product":"\xd0\xa2\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80","slug":"tovar"}'#тут приобразован словарь в json строку. Кирилица странно преобразовалась. 

# Как все работает!!!!!!!!!!!
#в сериализаторе мы прописываем названия атрибутов класса то есть переменных с такими же названия как названия полей в модели, это обязательно и важно. 
# когда создается объект GoodsSerializer и передается в него объект модели, то там отрабатывает определенный мета класс, котрый определен для сериализаторов, и этот мета класс вместо атрибутов в классе сериализаторе (в нашем случае в классе GoodsSerializer есть 2 атрибута name_product и slug), создает словарь data состоящий из значений объекта модели (в нашем случае модель это класс GoodsModel) и представляет их в виде словаря data. Далее словарь преобразуется в Json строку (Как это делается не совсем понятно.)
#далее модели джанго уже также будет преобразовываться по такому же принципу


# функция для преобразования json обратно в объект модели!!!!!!!!!!!!!!
# def decode():
#     stream = io.BytesIO(b'{"name_product":"\xd0\xa2\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80","slug":"tovar"}')#тут мы как бы имитируем запрос от клиента как будто пришел json от клиента. io имортировать надо из стандартного пакета питона
#     data = JSONParser().parse(stream)#создали объект класса JSONParser, и вызвали метод parse и передали в него json строку
#     serializer = GoodsSerializer(data=data)#передаем данные в сериализатор
#     serializer.is_valid()#проверяем данные на корректность
#     print(serializer.validated_data)#после того как отработает метод is_valid появляется коллекция validated_data, это и будет результат декодирования json строки.
#     #работу функции можно проверить в оболочке shell. Запускать через файл manage.py в cmd. Более подробно о кодировании и декодировании есть в документации по сериализации

#теперь поработаем с нашей БД.

# class GoodsSerializer(serializers.Serializer):#типы полей по названию вроде такие же как в модели  
#     name_product = serializers.CharField(max_length=255)
#     slug = serializers.CharField(max_length=255)
#     vendor_code = serializers.CharField(max_length=255, read_only=True)
#     price = serializers.DecimalField(max_digits=19, decimal_places=2)
#     photo = serializers.CharField()
#     stock = serializers.FloatField()
#     availability = serializers.BooleanField(default=True)
#     group_id = serializers.IntegerField()

#     def create(self, validated_data):
#         return Goods.objects.create(**validated_data)#словарь validated_data состоит из всех проверенных данных которые пришли из пост запроса, то есть уже валидны тут. 


#     def update(self, instance, validated_data):#instance - это ссылка на объект класса Goods, validated_data это словарь из проверенных данных, которые нужно изменить в бд. 
#         instance.name_product = validated_data.get('name_product', instance.name_product)#записали новое имя в позицию из БД и новое значение взяли из полученного словаря. В случае если не найдется в переданном словаре новое значение для названия товара, то вернется старое значение из модели таблицы. Для других полей нужно прописать тоже самое. 
#         instance.slug = validated_data.get('slug', instance.slug)
#         instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
#         instance.price = validated_data.get('price', instance.price)
#         instance.photo = validated_data.get('photo', instance.photo)
#         instance.stock = validated_data.get('stock', instance.stock)
#         instance.availability = validated_data.get('availability', instance.availability)
#         instance.group_id = validated_data.get('group_id', instance.group_id)
#         instance.save()#сохраняем данные в бд
#         return instance#instance обязательно нужно возвращать. так как сделали метод для изменения, то в классе views нужно прописать метод put
#далее перейдем в вью файл



#сериализатор для получения списка товаров витриной, но не для добавления товаров


class Order_get_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    fio = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)   
    product_id_id = serializers.IntegerField()#тут связанное поле, там индекс типа инт
    quantity = serializers.FloatField()  
    order_number = serializers.IntegerField()
    # time_create = serializers.DateTimeField()#время создания заказа покупателем
    delivery_address = serializers.CharField(max_length=255)
    state_order = serializers.BooleanField()


class Order_number_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    fio = serializers.CharField(max_length=255)        
    order_number = serializers.IntegerField()
    time_create = serializers.DateTimeField()#время создания заказа покупателем    
    state_order = serializers.BooleanField()



class Order_open_Serializer(serializers.ModelSerializer):
    product_id = GoodsSerializer(many=False, read_only=True)

    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())#это чтобы поле с пользаком скрывалось при добавлении через форму в урлке от джанго, которое мы делаем через форму вьюшки. Мы тут создаем скрытое поле, и там по умолчанию прописываем текущего пользака. 
    class Meta:
        model = Order_list_bought#тут пишем модель с которой будем работать
        # fields = ("name_product", "slug", "vendor_code", "price", "stock",  "group" )#тут пишем какие поля будем возвращать обратно клиенту. Причем тут поля с внешним ключем не нужно прописывать с _id. Пользак будет видеть число, а не группу из поля group. Также сразу доступны все виды запросов пост, гет и тд. Затрагиваться будут те поля, которые мы пропишем в запросах. 
        #если нужно указать все поля в сериализаторе, то вручную их можно не писать.
        # fields = "__all__"#вот если прописать, то в сериализатор будут попадать все поля. 
        #сериализация с фото не работает почему то
        fields = ('fio', 'phone', 'quantity', 'order_number', 'time_create', 'delivery_address', 'product_id', 'state_order')



