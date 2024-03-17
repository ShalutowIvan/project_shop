from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

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
    paginate_by = 10
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


#для получения списка товаров в витрине это для апи
class Get_good(APIView):

	def get(self, request):
		good = Goods.objects.all()

		return Response(GoodsSerializer(instance=good, many=True).data)


#добавление товара
class Goods_add(CreateView):
    form_class = Goods_add_form
    template_name = 'shop/good_add.html'
    success_url = reverse_lazy('goods_list')
    login_url = reverse_lazy('start')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Organization.objects.all()
        
        if org:
            context['org'] = org[0]
        
        return context

    #передача юзера в форму автоматом от залогининного пользователя. В самой форме юзер не заполняется
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user        
        self.object.save()
        # возвращаем form_valid предка
        return super().form_valid(form)


#список накладных просто вывод
@login_required
def receipt_list(request):
	rec_list = Receipt_number.objects.all()
	
	context = {"receipt_list_view": rec_list}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/receipt_list.html", context=context)


#создание документа - добавить документ с добавлением коммента. После создания документа он сразу открывается - редирект на урл receipt_document_open
@login_required
def receipt_document_create(request):
	if request.method == 'POST':
		form = Receipt_number_form(data=request.POST)
		if form.is_valid():
			comm = form.save(commit=False)
			comm.save()

			return redirect('receipt_document_open', comm.id)

	else:
		form = Receipt_number_form()

	context = {'form': form}

	return render(request, 'shop/receipt_create.html', context=context)    

	

#приходный документ - открытие
@login_required
def receipt_document_open(request, open_receipt):
	receipt_open = Receipt_number.objects.get(id=open_receipt)
	receipt_good_list = Receipt_list.objects.filter(number_receipt=open_receipt)
	context = {"number": open_receipt, 'receipt_good_list': receipt_good_list, "date": receipt_open.time_create}

	org = Organization.objects.all()
        
	if org:
		context['org'] = org[0]

	return render(request, "shop/receipt_open.html", context=context)


#добавление товара - в открытом документе. number_doc берется из номера открытого документа, который мы открыли функцией receipt_document_open он прокидывается в html.
#тут ошибка, что-то не так
@login_required
def receipt_add_goods(request, number_doc):
	if request.method == 'POST':
		form = Receipt_add_goods_form(data=request.POST)
		if form.is_valid():
			good = form.save(commit=False)
			good.number_receipt = number_doc
			good.user = request.user
			good.save()

			return redirect('receipt_document_open', number_doc)

	else:
		form = Receipt_add_goods_form()

	context = {'form': form, "number_doc": number_doc}



	return render(request, "receipt_goods_add.html", context=context)









# def activate_document(request, activate):#Есть мысль, сделать сохранение обязательным перед проведением, и потом кнопка проведение будет просто менять статус накладной state на True. В случае если нужно отредачить документ, нужно сделать возможность редактирования
# 	doc = Receipt_list.objects.get(id=activate)
# 	goods = Goods.objects.get(id=doc.product.id)

# 	if doc.state != True:
# 		goods.stock += doc.quantity
# 		goods.save()
# 	print(doc.state)
# 	doc.state = True
# 	doc.save()


# 	return redirect('receipt_list')
	# тут остановился

# <a href="{% url 'activate_document' j.id %}"><button class="add_rec">Провести документ</button></a>


#список накладных



# class Receipt_list(ListView):
# 	template_name = 'shop/receipt_list.html'
# 	paginate_by = 10
# 	model = Receipt_list 
# 	context_object_name = 'receipt_list_view'

# 	def get_queryset(self):
# 		return
        
# 	def get_context_data(self, *, object_list=None, **kwargs):
# 		context = super().get_context_data(**kwargs)		       		
# 		org = Organization.objects.all()
# 		if org:
# 			context['org'] = org[0]

# 		return context






# def get_good(request):
# 	good = Goods.objects.all().values()
# 	return Response({"request": request, "good": list(good)})




# class GroupShow(ListView):
#     paginate_by = 10
#     model = Goods
#     # template_name = 'shop/good.html'
#     context_object_name = 'goods'
#     allow_empty = True

#     def get_queryset(self):
#         # q_set = Goods.objects.filter(group__slug=self.kwargs['group_slug'])
#         # if q_set == []:
#         #     return ["Пусто"]
#         # else:
#         return Goods.objects.filter(group__slug=self.kwargs['group_slug'])

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         if len(context['goods']) == 0:
#             context['title'] = 'Группа - ' + "Пусто"
#         else:
#             context['title'] = 'Группа - ' + str(context['goods'][0].group)

#         org = Organization.objects.all()
#         if org:
#             context['org'] = org[0]
#         context['form'] = AddGoodForm()

#         return context




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


# class GoodsViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
# 	pass


# спланировать какой будет функционал в учетной системе и как все будет выглядеть
# сделать список заказов









#в таком виде сейчас возвращается
# {"1":[["Хлеб",1.0,"2024-02-16T02:13:59.166505",44.0,"домой","Вася","89998887766"]],"2":[["Хлеб",2.0,"2024-02-16T02:19:42.964451",44.0,"домой","Jhon","89998887766"]]}
#ключ словаря это номер заказа, далее в значении ключа инфа о заказе