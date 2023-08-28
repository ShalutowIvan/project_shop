from decimal import Decimal
from django.conf import settings
from showcase.models import *


class Basket:

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session#создали свойство объекта, и добавили в него коллекцию сессии. Скорее всего словарь
        basket = self.session.get(settings.BASKET_SESSION_ID)#присваиваем в переменную корзину, которая возможно есть в сессии
        if not basket:#если корзина пуста, то в сессию мы записываем элемент корзины.
            # save an empty cart in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket#и теперь в свойство объекта записываем корзину, которую подтнянули из сессии. 


    def add(self, good, quantity=1, update_quantity=False):#good это объект Good для добавления или обновления корзины, quantity - количество товара по умолчанию это 1, Это логическое значение, которое указывает, требуется ли обновление количества с заданным количеством (True), или же новое количество должно быть добавлено к существующему количеству (False).
    """
    Добавить продукт в корзину или обновить его количество.
    """
        good_id = str(good.id)#id используется как ключ в словаре содержимого корзины. преобразовали id в строку, чтобы передать в JSON для сериализации в джанго, джанго использует json для сериилизации и json работает со строками. id продукта — это ключ, а значение, которое мы сохраняем, — словарь с количеством и ценой для продукта.
        if good_id not in self.basket:
            self.basket[good_id] = {'quantity': 0, 'price': str(good.price)}#создали пустой словарь, типа пустой шаблон с нулевым колвом. Цена преобразуется также в строку
        if update_quantity:
            self.basket[good_id]['quantity'] = quantity#если есть разрешение на апдейт, тогда мы присваиваем в элемент словаря с ключом quantity нужную нам цифру колво
        else:
            self.basket[good_id]['quantity'] += quantity#иначе добавляем колво
        self.save()


    def save(self):
    # Обновление сессии basket
        self.session[settings.BASKET_SESSION_ID] = self.basket
    # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True


    def remove(self, good):#метод удаляет элемент из корзины. Корзина это словарь, удаляем элемент словаря корзины если он там есть. И сохраняем изменения
        """
        Удаление товара из корзины.
        """
        good_id = str(good.id)
        if good_id in self.basket:
            del self.basket[good_id]
            self.save()


    def __iter__(self):
    
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        good_ids = self.basket.keys()
        # получение объектов product и добавление их в корзину
        goods = Goods.objects.filter(id__in=good_ids)
        for good in goods:
            self.basket[str(good.id)]['good'] = good

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.basket.values())


    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True
