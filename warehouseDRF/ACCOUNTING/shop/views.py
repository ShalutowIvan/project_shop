from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView

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

from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView

from django.forms import model_to_dict

from .forms import *

import requests


class ShopHome(ListView):
    # paginate_by = 11
    # model = Goods
    template_name = 'shop/start.html'
    context_object_name = 'done'

    def get_queryset(self):
    	return
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        db_order = Order_list_bought.objects.all()
        # db_order2 = db_order
        # for i in db_order:
        # 	for j in db_order2:
        # 		if i.order_number == j.order_number:
        # 			if type(i.product_id) != list:
		# 				i.product_id = [i.product_id, ]
		# 			else:
		# 				i.product_id.append(j.product_id)
				# додумать алгоритм, не знаю как вывести номер заказа и список товаров к нему	


        context["order_list"] = db_order

        return context


def synchronization(request):
	rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
	res = rq.json()
	db_order = Order_list_bought.objects.all()
	order_number_list = (i.order_number for i in db_order)
	
	for i in res:
		if i["order_number"] not in order_number_list:			
			serializer = OrderSerializer(data=i)
			serializer.is_valid(raise_exception=True)
			serializer.save()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


class Order_list_view(APIView):

	def get(self, request):
		db_order = Order_list_bought.objects.all()

		return render(request, "shop/checkout_list.html", context=db_order)


	def post(self, request):
		pass




# class Asd(RetrieveUpdateDestroyAPIView):
# 	def get(self, request):
# 		rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
# 		res = rq.text
		
# 		return HttpResponse(res)



# class Synchronization(APIView):

# 	def get(self, request):
# 		rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
# 		res = rq.text
		
# 		return HttpResponse(res)


# 	def post(self, request):
# 		# for i 
# 		pass


class GoodsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
	pass


# спланировать какой будет функционал в учетной системе и как все будет выглядеть
# сделать список заказов









#в таком виде сейчас возвращается
# {"1":[["Хлеб",1.0,"2024-02-16T02:13:59.166505",44.0,"домой","Вася","89998887766"]],"2":[["Хлеб",2.0,"2024-02-16T02:19:42.964451",44.0,"домой","Jhon","89998887766"]]}
#ключ словаря это номер заказа, далее в значении ключа инфа о заказе