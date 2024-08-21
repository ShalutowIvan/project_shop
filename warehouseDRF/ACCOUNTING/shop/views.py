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



#получение списка заказов с сайта витрины, поиск идет по артикулу, то есть в номере заказа идет артикул. Если ID совпадать в базах не будут ничего страшного, главное чтобы совпадали артикулы.
def synchronization(request):
	try:
		rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
		res = rq.json()
		db_order = Order_list_bought.objects.all()
		order_number_list = list(i.order_number for i in db_order)		

		for i in res:
			if i["order_number"] not in order_number_list:
				# vendor = i['product_id']
				# i['product_id'] = Goods.objects.get(vendor_code=vendor).id
				#сделать проверку на state, если фолз, то пропускаем или что то еще
				if i["state"] == False:
					continue

				serializer = OrderSerializer(data=i)
				serializer.is_valid(raise_exception=True)
				serializer.save()

		return HttpResponseRedirect(request.META['HTTP_REFERER'])

	except Exception as ex:
		context = {"error": ex}
		org = Organization.objects.all()
		if org:
			context['org'] = org[0]

		return render(request, "shop/synchro_error.html", context=context )


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
		# for i in db_order:
		# 	if res.get(i.order_number) == None:
		# 		res[i.order_number] = [i.fio, i.phone, i.time_create, i.delivery_address, [[i.product_id, i.quantity], ] ]
		# 	else:
		# 		res[i.order_number][4] += [[i.product_id, i.quantity], ]

		for i in db_order:
			if res.get(i.order_number) == None:
				res[i.order_number] = [i.fio, i.phone, i.time_create, i.state_order]
			
		context["order_list"] = res

		org = Organization.objects.all()
		if org:
			context['org'] = org[0]

		return context


#функция открыть заказ. 
@login_required
def order_list_open(request, order_number):	

	goods_in_order = Order_list_bought.objects.filter(order_number=order_number)#тут список, queryset
	
	context = {"goods_in_order": goods_in_order, "order_number": order_number}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/order_list_open.html", context=context)
	
# Нужно еще сделать оповещение на сайте витрины на странице заказов


#функция проведения заказа
@login_required
def order_list_activate(request, order_activate):
	order = Order_list_bought.objects.filter(order_number=order_activate)#запросили список товаров из заказа по номеру заказа


	if order[0].state_order == False:
		
		gen_list = [i.product_id.id for i in order]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock -= order[i].quantity			
			order[i].state_order = True
			order[i].save()

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])
			

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#отмена проведения заказа
@login_required
def order_list_deactivate(request, order_deactivate):
	order = Order_list_bought.objects.filter(order_number=order_deactivate)#запросили список товаров из заказа по номеру заказа


	if order[0].state_order == True:
		
		gen_list = [i.product_id.id for i in order]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock += order[i].quantity	
			order[i].state_order = False
			order[i].save()

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])
			

	return HttpResponseRedirect(request.META['HTTP_REFERER'])



#отображение списка товаров
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
        groups = Group.objects.all()
        context["groups"] = groups
        if org:
            context['org'] = org[0]

        # context['form'] = AddGoodForm()#форма для поиска не нужна
        
        return context


# class Group_show(ListView):
#     paginate_by = 10
#     model = Goods
#     template_name = 'shop/good_group.html'
#     context_object_name = 'gd'
#     allow_empty = True

#     def get_queryset(self):        
#         return Goods.objects.filter(group__slug=self.kwargs['group_slug'])

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # if len(context['goods']) == 0:
#         #     context['title'] = 'Группа - ' + "Пусто"
#         # else:
#         #     context['title'] = 'Группа - ' + str(context['goods'][0].group)

#         # context["goods"] = Goods.objects.filter(group.slug)




#         org = Organization.objects.all()
#         if org:
#             context['org'] = org[0]
        

#         return context


def group_show(request, group_slug):

	goods_in_group = Goods.objects.filter(group__slug=group_slug)
	groups = Group.objects.all()

	context = {"goods_in_group": goods_in_group, "groups": groups}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/good_group.html", context=context)








#для получения списка товаров в витрине это для апи
class Get_good(APIView):

	def get(self, request):
		good = Goods.objects.all()

		return Response(GoodsSerializer(instance=good, many=True).data)


# для получения списка групп в витрине для апи
class Get_group(APIView):

	def get(self, request):
		group = Group.objects.all()

		return Response(GroupSerializer(instance=group, many=True).data)
		


class Get_order(APIView):

	def get(self, request):
		order = Order_list_bought.objects.all()

		return Response(Order_get_Serializer(instance=order, many=True).data)
		




#добавление группы товаров
class Group_add(CreateView):
    form_class = Group_add_form
    template_name = 'shop/group_add.html'
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
	context = {"number": open_receipt, 'receipt_good_list': receipt_good_list, "receipt_doc": receipt_open}

	org = Organization.objects.all()
        
	if org:
		context['org'] = org[0]

	return render(request, "shop/receipt_open.html", context=context)


#проведение документа - то функция после которой меняется статус документа и добавляется товар на остаток на основании документа
@login_required
def receipt_document_activate(request, receipt_activate):
	doc = Receipt_number.objects.get(id=receipt_activate)
	if doc.state == False:
		list_goods_to_add = Receipt_list.objects.filter(number_receipt=receipt_activate)
		gen_list = [i.product.id for i in list_goods_to_add]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock += list_goods_to_add[i].quantity
			
			# print(list_good[i].stock)

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])

		doc.state = True
		doc.save()		

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#отмена проведения документа
@login_required
def receipt_document_deactivate(request, receipt_deactivate):
	doc = Receipt_number.objects.get(id=receipt_deactivate)

	if doc.state == True:
		list_goods_to_add = Receipt_list.objects.filter(number_receipt=receipt_deactivate)
		gen_list = [i.product.id for i in list_goods_to_add]

		list_good = Goods.objects.filter(pk__in=gen_list)

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock -= list_goods_to_add[i].quantity			

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])

		doc.state = False
		doc.save()	

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#приходный документ - удаление, удаляется и таблица с номером документа и товары с этим же номером документа
@login_required
def receipt_document_delete(request, number_delete_receipt):
	rec = Receipt_number.objects.get(id=number_delete_receipt)
	good_list_delete = Receipt_list.objects.filter(number_receipt=number_delete_receipt)
	
	rec.delete()
	good_list_delete.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#добавление товара - в открытом документе. number_doc берется из номера открытого документа, который мы открыли функцией receipt_document_open он прокидывается в html.
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

	return render(request, "shop/receipt_goods_add.html", context=context)


#удаление товара из накладной
@login_required
def receipt_delete_goods(request, number_delete_good):
	list_delete = Receipt_list.objects.get(id=number_delete_good)
	list_delete.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


###########################################################################
#РАСХОДНЫЙ документ - начало - открытие
@login_required
def expense_list(request):
	expense_list = Expense_number.objects.all()
	
	context = {"expense_list_view": expense_list}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/expense_list.html", context=context)



#создание акта списания - добавить документ с добавлением коммента. После создания документа он сразу открывается - редирект на урл receipt_document_open
@login_required
def expense_document_create(request):
	if request.method == 'POST':
		form = Expense_number_form(data=request.POST)
		if form.is_valid():
			comm = form.save(commit=False)
			comm.save()

			return redirect('expense_document_open', comm.id)

	else:
		form = Expense_number_form()

	context = {'form': form}

	return render(request, 'shop/expense_create.html', context=context)    

	

#приходный документ - открытие
@login_required
def expense_document_open(request, open_expense):
	expense_open = Expense_number.objects.get(id=open_expense)
	expense_good_list = Expense_list.objects.filter(number_act=open_expense)#поиск по номеру акта
	context = {"number": open_expense, 'expense_good_list': expense_good_list, "expense_doc": expense_open}

	org = Organization.objects.all()
        
	if org:
		context['org'] = org[0]

	return render(request, "shop/expense_open.html", context=context)


#проведение документа - это функция после которой меняется статус документа и добавляется товар на остаток на основании документа
@login_required
def expense_document_activate(request, expense_activate):
	doc = Expense_number.objects.get(id=expense_activate)
	if doc.state == False:
		list_goods_to_subtract = Expense_list.objects.filter(number_act=expense_activate)
		gen_list = [i.product.id for i in list_goods_to_subtract]

		list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock -= list_goods_to_subtract[i].quantity
			
			# print(list_good[i].stock)

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])

		doc.state = True
		doc.save()		

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#отмена проведения документа
@login_required
def expense_document_deactivate(request, expense_deactivate):
	doc = Expense_number.objects.get(id=expense_deactivate)

	if doc.state == True:
		list_goods_to_subtract = Expense_list.objects.filter(number_act=expense_deactivate)
		gen_list = [i.product.id for i in list_goods_to_subtract]

		list_good = Goods.objects.filter(pk__in=gen_list)

		list_good = list(list_good)
		
		for i in range(len(gen_list)):
			
			list_good[i].stock += list_goods_to_subtract[i].quantity			

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock",])

		doc.state = False
		doc.save()	

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#приходный документ - удаление, удаляется и таблица с номером документа и товары с этим же номером документа
@login_required
def expense_document_delete(request, number_delete_expense):
	rec = Expense_number.objects.get(id=number_delete_expense)
	good_list_delete = Expense_list.objects.filter(number_act=number_delete_expense)
	
	rec.delete()
	good_list_delete.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#добавление товара - в открытом документе. number_doc берется из номера открытого документа, который мы открыли функцией receipt_document_open он прокидывается в html.
@login_required
def expense_add_goods(request, number_doc):
	if request.method == 'POST':
		form = Expense_add_goods_form(data=request.POST)
		if form.is_valid():
			good = form.save(commit=False)
			good.number_act = number_doc
			good.user = request.user
			good.save()

			return redirect('expense_document_open', number_doc)

	else:
		form = Expense_add_goods_form()

	context = {'form': form, "number_doc": number_doc}

	return render(request, "shop/expense_goods_add.html", context=context)


#удаление товара из накладной
@login_required
def expense_delete_goods(request, number_delete_good):
	list_delete = Expense_list.objects.get(id=number_delete_good)
	list_delete.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])



#####################################################################################



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


