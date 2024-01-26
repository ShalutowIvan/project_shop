from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Goods


class GoodsModel:#имитация модели. У нас будут объекты этого класса
    def __init__(self, name_product, slug):
        self.name_product = name_product
        self.slug = slug


# class GoodsSerializer(serializers.ModelSerializer):#пишем сериализатор для проверки данных при выдаче их пользаку. Проверяем таблицу Goods
    
#     class Meta:
#         model = Goods
#         fields = ('name_product', 'group')


class GoodsSerializer(serializers.Serializer):#этот клас будет преобразовывать модель GoodsModel в JSON формат. Наследуется от класса Serializer
    #класс Meta напрямую работает с моделями. А теперь напрямую с моделями мы не можем работать так как испоьзуем класс Serializer как базовый. Определить нужно здесь 2 атрибута
    name_product = serializers.CharField(max_length=255)#сериализация первого поля в строковый тип. То есть теперь при поступлении данных у них будет проверяться длинна и преобразовываться. 
    slug = serializers.CharField(max_length=255)#тут аналогично. Если в скобках ничего не прописать, то проверка будет только на тип данных.


#чтобы посмотреть как работает сериализатор, сделем обычную функцию.
def encode():
    model = GoodsModel('Товар', 'tovar')
    model_sr = GoodsSerializer(model)#тут объект сериализации, а не байтовая json строка. Ниже сделаем Json строку
    print(model_sr.data, type(model_sr.data), sep='\n')#тут мы смотрим что у нас будет выведено. 
    json = JSONRenderer().render(model_sr.data)#JSONRenderer нужно импортировать. JSONRenderer преобразует объект сериализации в байтовую JSON строку. 
    print(json)

#функцию encode можно проверить только через оболочку shell через файл проекта manage.py. Так как просто так файл serializers.py не запускается. И функцию просто так нельзя запускать. Чтобы зайти в оболочку нужно в cmd прописать python manage.py shell. Потом импортировать там функцию encode и потом ее можно запускать там же в оболочке. 
# наша функция вернут следующее:
# {'name_product': 'Товар', 'slug': 'tovar'}#здесь преобразован объект в обычный словарь
# <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
# b'{"name_product":"\xd0\xa2\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80","slug":"tovar"}'#тут приобразован словарь в json строку. Кирилица странно преобразовалась. 

# Как все работает!!!!!!!!!!!
#в сериализаторе мы прописываем названия атрибутов класса то есть переменных с такими же названия как названия полей в модели, это обязательно и важно. 
# когда создается объект GoodsSerializer и передается в него объект модели, то там отрабатывает определенный мета класс, котрый определен для сериализаторов, и этот мета класс вместо атрибутов в классе сериализаторе (в нашем случае в классе GoodsSerializer есть 2 атрибута name_product и slug), создает словарь data состоящий из значений объекта модели (в нашем случае модель это класс GoodsModel) и представляет их в виде словаря data. Далее словарь преобразуется в Json строку (Как это делается не совсем понятно.)
#далее модели джанго уже также будет преобразовываться по такому же принципу
# ост 9 мин



