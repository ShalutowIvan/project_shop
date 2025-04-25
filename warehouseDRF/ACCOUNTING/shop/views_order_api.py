from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from rest_framework import generics, viewsets, mixins
from .models import *
from .serializers_orders import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Subquery, OuterRef

from django.forms import model_to_dict

from .forms import *
from django.core.exceptions import ObjectDoesNotExist

import random
import string
import os
import requests
import pandas as pd
from transliterate import translit
from .utils import handle_uploaded_file
from PIL import Image


#получение списка заказов
class Get_order(APIView):

	def get(self, request):		
		#та же самая сортировка только для postgresql
		# order = Order_list_bought.objects.order_by('order_number').distinct('order_number')

		#для любой БД. Сортировка с записей с уникальными номерами заказа. Нужно только номера и дата
		subquery = Order_list_bought.objects.filter(order_number=OuterRef('order_number')).values('id')[:1]
		unique_orders = Order_list_bought.objects.filter(id__in=Subquery(subquery))

		return Response(Order_number_Serializer(instance=unique_orders, many=True).data)


#открыть заказ
class Get_order_open(APIView):

	def get(self, request, order_number):	
		goods_in_order = Order_list_bought.objects.filter(order_number=order_number)#тут список, queryset

		return Response(Order_open_Serializer(instance=goods_in_order, many=True).data)



#фильтры заказов тут сделать. Можно просто функции, 3 кнопки, проведенные, не проведенные, все. Сделал их в отдельном блоке в html. 

#проведенные
class Get_order_completed(APIView):

	def get(self, request):

		subquery = Order_list_bought.objects.filter(order_number=OuterRef('order_number')).values('id')[:1]
		unique_orders = Order_list_bought.objects.filter(id__in=Subquery(subquery), state_order=True)


		return Response(Order_number_Serializer(instance=unique_orders, many=True).data)

#непроведенные
class Get_order_not_completed(APIView):

	def get(self, request):

		subquery = Order_list_bought.objects.filter(order_number=OuterRef('order_number')).values('id')[:1]
		unique_orders = Order_list_bought.objects.filter(id__in=Subquery(subquery), state_order=False)


		return Response(Order_number_Serializer(instance=unique_orders, many=True).data)


#функция проведения заказа
@api_view(['GET'])
def api_order_list_activate(request, order_activate):
	order = Order_list_bought.objects.filter(order_number=order_activate)#запросили список товаров из заказа по номеру заказа
	data = {None: None}

	if order[0].state_order == False:
		
		gen_list = [i.product_id.id for i in order]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock -= order[i].quantity			
			order[i].state_order = True
			order[i].save()

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])
		
		data = {'state_order': order[0].state_order}

	return Response(data, status=status.HTTP_200_OK)


#отмена проведения заказа
@api_view(['GET'])
def api_order_list_deactivate(request, order_deactivate):
	order = Order_list_bought.objects.filter(order_number=order_deactivate)#запросили список товаров из заказа по номеру заказа
	data = {None: None}

	if order[0].state_order == True:
		
		gen_list = [i.product_id.id for i in order]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock += order[i].quantity	
			order[i].state_order = False
			order[i].save()

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])			

		data = {'state_order': order[0].state_order}

	return Response(data, status=status.HTTP_200_OK)




