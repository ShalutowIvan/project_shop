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



class Home(ListView):
    # paginate_by = 11
    # model = Goods
	template_name = 'shop/start.html'
	context_object_name = 'home'

	def get_queryset(self):
		return
        
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)		       		
		org = Organization.objects.all()
		if org:
			context['org'] = org[0]

		return context


class Order_list(ListView):
    # paginate_by = 11
    # model = Goods
	template_name = 'shop/order_list.html'
	context_object_name = 'order'

	def get_queryset(self):
		return
        
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		db_order = Order_list_bought.objects.all()
        		
		res = {}
		for i in db_order:
			if res.get(i.order_number) == None:
				res[i.order_number] = [i.fio, i.phone, i.time_create, i.delivery_address, [[i.product_id, i.quantity], ] ]
			else:
				res[i.order_number][4] += [[i.product_id, i.quantity], ]
		
		
		context["order_list"] = res

		org = Organization.objects.all()
		if org:
			context['org'] = org[0]

		return context

#получение списка заказов
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


# class Order_list_view(APIView):

# 	def get(self, request):
# 		db_order = Order_list_bought.objects.all()

# 		return render(request, "shop/checkout_list.html", context=db_order)


# 	def post(self, request):
# 		pass



class Goods_list(ListView):
    paginate_by = 11
    model = Goods
    template_name = 'shop/good.html'
    context_object_name = 'gd'


    def get_queryset(self):#этот get_queryset для поиска товаров, товар ищется по названию всегда во всем каталоге, даже если зайти в группу то поиск будет также по всему каталогу. Потом доделать
        return Goods.objects.filter(name_product__icontains=self.request.GET.get('q', ''))
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Organization.objects.all()
        
        if org:
            context['org'] = org[0]
        

        
        return context


#для получения списка товаров в витрине
class Get_good(APIView):

	def get(self, request):
		good = Goods.objects.all()
		# good = Goods.objects.all().values()
		# return Response({"good": list(good)})
		# return Response({"good": GoodsSerializer(good, many=True).data})
		
		return Response(GoodsSerializer(instance=good, many=True).data)



# def get_good(request):
# 	good = Goods.objects.all().values()
# 	return Response({"request": request, "good": list(good)})




class GroupShow(ListView):
    paginate_by = 10
    model = Goods
    template_name = 'showcase/good.html'
    context_object_name = 'goods'
    allow_empty = True

    def get_queryset(self):
        # q_set = Goods.objects.filter(group__slug=self.kwargs['group_slug'])
        # if q_set == []:
        #     return ["Пусто"]
        # else:
        return Goods.objects.filter(group__slug=self.kwargs['group_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if len(context['goods']) == 0:
            context['title'] = 'Группа - ' + "Пусто"
        else:
            context['title'] = 'Группа - ' + str(context['goods'][0].group)

        org = Organization.objects.all()
        if org:
            context['org'] = org[0]
        context['form'] = AddGoodForm()

        return context




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