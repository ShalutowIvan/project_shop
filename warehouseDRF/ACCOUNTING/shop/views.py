from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict

# class TestApi(generics.ListAPIView):
# 	queryset = Goods.objects.all()#делаем просто запрос таблицы
# 	serializer_class = GoodsSerializer#это класс сериализатор. Его нужно импортировать из файла serializers.py. В нем будут все сериализаторы. Перейдем в этот файл и сделаем этот класс
# 	#пропишем также текущее представление в urls.py в файле проекта. Текущий класс просто возвращает json для, чтобы потом какое-то другое приложение его обработало

class GoodsAPIView(APIView):
	def get(self, request):#request - содержит все параметры входящего get запроса
		lst = Goods.objects.all().values()
		return Response({'goods': list(lst)})#теперь по ссылке будет возвращаиться просто json ответ. Пока возвращается просто строка без использования сериализатора

	
	def post(self, request):
		post_new = Goods.objects.create(
			name_product = request.data['name_product'],
			slug = request.data['slug'],
			price = request.data['price'],
			photo = request.data['photo'],
			stock = request.data['stock'],
			group_id = request.data['group_id']
		)

		return Response({'post': model_to_dict(post_new)})

# model_to_dict - это стандартная функция из обычного джанго для преобразования модели джанго класса Goods в словарь

    	
    		





