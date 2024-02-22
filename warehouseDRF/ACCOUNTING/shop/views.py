from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, viewsets, mixins
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from django.forms import model_to_dict

from .forms import *

import requests


# class GoodsViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
# 	pass


# спланировать какой будет функционал в учетной системе и как все будет выглядеть
# сделать список заказов

class Order_list_view(APIView):

	def get(self, request):
		pass


	def post(self, request):
		pass



def test_view(request):
	rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
	res = rq.text
	print(res)
	return HttpResponse(res)

#в таком виде сейчас возвращается
# {"1":[["Хлеб",1.0,"2024-02-16T02:13:59.166505",44.0,"домой","Вася","89998887766"]],"2":[["Хлеб",2.0,"2024-02-16T02:19:42.964451",44.0,"домой","Jhon","89998887766"]]}
#ключ словаря это номер заказа, далее в значении ключа инфа о заказе