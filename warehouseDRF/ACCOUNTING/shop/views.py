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
@login_required
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

#список заказов
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
				res[i.order_number] = [i.fio, i.phone, i.time_create, i.state_order]
			
		context["order_list"] = res

		org = Organization.objects.all()
		if org:
			context['org'] = org[0]

		return context


#фильтры заказов тут сделать. Можно просто функции, 3 кнопки, проведенные, не проведенные, все. Сделал их в отдельном блоке в html. 
def order_completed(request):
	db_order = Order_list_bought.objects.filter(state_order=True)

	context = {}
	res = {}
	for i in db_order:
		if res.get(i.order_number) == None:
			res[i.order_number] = [i.fio, i.phone, i.time_create, i.state_order]
			
	context["order_list"] = res

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/order_list_completed.html", context=context)


def order_not_completed(request):
	db_order = Order_list_bought.objects.filter(state_order=False)

	context = {}
	res = {}
	for i in db_order:
		if res.get(i.order_number) == None:
			res[i.order_number] = [i.fio, i.phone, i.time_create, i.state_order]
			
	context["order_list"] = res

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/order_list_completed.html", context=context)



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


@login_required
def group_show(request, group_slug):

	goods_in_group = Goods.objects.filter(group__slug=group_slug)
	groups = Group.objects.all()

	context = {"goods_in_group": goods_in_group, "groups": groups}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/good_group.html", context=context)



#для получения списка товаров в витрине это для апи
# @login_required
class Get_good(APIView):

	def get(self, request):
		good = Goods.objects.all()

		return Response(GoodsSerializer(instance=good, many=True).data)


# для получения списка групп в витрине для апи
# @login_required
class Get_group(APIView):

	def get(self, request):
		group = Group.objects.all()

		return Response(GroupSerializer(instance=group, many=True).data)
		

# @login_required
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

import os
import pandas as pd
from transliterate import translit

#загрузка файла с товарами
def goods_load_file(request):	

	if request.method == 'POST':		
		p = request.POST
		f = request.FILES
		file = request.FILES['load_file']
		
		db_goods = pd.read_excel(file)
		# context = {"goods_in_file": db_goods}#тут объект <class 'pandas.core.frame.DataFrame'>


		# print(type(db_goods))#тип <class 'pandas.core.frame.DataFrame'>
		# keys - для извлечения ключей
		# values - для извлечения значений
		# items - для извленичения ключей и значений
		# далее в доку если нужно что-то еще для DataFrame из pandas

		groups_query = Group.objects.all()
		groups = [i.name_group.lower() for i in groups_query]
		goods = []

		for i in db_goods.values:
			if i[4].lower() in groups:				
				goods.append(
				Goods(
				name_product=i[0], 
				slug=translit(i[0], language_code='ru', reversed=True), 
				vendor_code=i[1], 
				price=i[2],
				stock=i[3],
				group=Group.objects.get(name_group=i[4].title()),
				user=request.user
				) )
			else:
				group_obj = Group(name_group=i[4].title(), slug=translit(i[4], language_code='ru', reversed=True))
				# иначе создаем новую группу
				group_obj.save()
				goods.append(
				Goods(
				name_product=i[0], 
				slug=translit(i[0], language_code='ru', reversed=True), 
				vendor_code=i[1], 
				price=i[2],
				stock=i[3],
				group=group_obj,
				user=request.user
				) )

		goods_create = Goods.objects.bulk_create(goods)
		# return redirect('goods_pars_file', fields)
		# return render(request, 'goods_pars_file', context=context)
		return redirect('goods_list')
	
	# context = {'form': form}
	context = {}

	return render(request, 'shop/good_load_file.html', context=context)    


def create_empty_excel(columns: list, filename: str, sheet_name: str = 'Sheet1'):
    df = pd.DataFrame(columns=columns)

    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', filename)
    excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()

    return filepath


def url_from_load_pattern(request):
	filepath = create_empty_excel(columns=["Название", "Артикул", "Цена", "Остаток", "Группа"], filename="Шаблон для загрузки товаров.xlsx")

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


# ВИДЕО по скачиванию файла
# https://www.youtube.com/watch?v=JMNq4sDKkTc

# https://www.youtube.com/watch?v=xPRA4jixCX8
# https://www.youtube.com/watch?v=tquWqkgU1X0


# https://ru.stackoverflow.com/questions/1203933/django-python-%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5-%D1%81%D0%BA%D0%B0%D1%87%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2



#код для загрузки файла
# https://stackoverflow.com/questions/36392510/django-download-a-file/36394206#36394206

# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404

# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404






#урл для парсинга файла с товарами и записи товаров в базу
# def goods_pars_file(request):#как сюда передать датафрейм или лист не знаю, в джанго урл надо это прописать хз как. Нужно закинуть в контекст фрейм

# 	#вариант с формой
# 	if request.method == 'POST':
# 		# form = Parse_file(data=request.POST)
		
			



# 		return redirect('goods_list')

# 	# else:
# 	# 	form = Parse_file()

# 	# , "goods": goods
# 	# 'form': form,
# 	context = {}

# 	return render(request, 'shop/good_parse_file.html', context=context)    

	


#список накладных просто вывод
@login_required
def receipt_list(request):
	rec_list = Receipt_number.objects.all()
	
	context = {"receipt_list_view": rec_list}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/receipt_list.html", context=context)


#загузка файла накладной.




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
	receipt_open = Receipt_number.objects.get(id=int(open_receipt))
	receipt_good_list = Receipt_list.objects.filter(number_receipt=int(open_receipt))
	context = {"number": open_receipt, 'receipt_good_list': receipt_good_list, "receipt_doc": receipt_open}

	org = Organization.objects.all()
        
	if org:
		context['org'] = org[0]

	return render(request, "shop/receipt_open.html", context=context)


#редактирование позиции в накладной
def receipt_document_edit(request, number_edit_good):

	if request.method == 'POST':
		form = Receipt_edit_goods_form(data=request.POST)
		if form.is_valid():			
			
			quantity = form.cleaned_data.get("quantity")
			good_edit = Receipt_list.objects.get(id=number_edit_good)
			good_edit.quantity = quantity
			
			good_edit.save()

			# print(type(number_edit_good))

			return redirect('receipt_document_open', good_edit.number_receipt)

	else:
		form = Receipt_edit_goods_form()

	context = {'form': form, "number_edit_good": number_edit_good}
	

	return render(request, "shop/receipt_goods_edit.html", context=context)




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


#отчеты!!!!!!!!!!
#просто страница с отчетами
def reports(request):
	context = {}
	org = Organization.objects.all()
	if org:
		context['org'] = org[0]
	return render(request, "shop/reports.html", context=context)


# <p><input type="date" label class="form-label" for="{{ form.date_by.id_for_label }}">Дата по: </label>{{ form.date_by }}</p>
#отчет по приходу
@login_required
def income_report(request):
	
	if request.method == 'POST':
		form = Date_report_income(data=request.POST)
		if form.is_valid():			
			d_from = form.cleaned_data.get("date_from")
			d_by = form.cleaned_data.get("date_by")

			rec_list = Receipt_number.objects.filter(time_create__gte=d_from, time_create__lte=d_by)#тут сделать запрос

			context = {"receipt_list_view": rec_list}
			org = Organization.objects.all()
			if org:
				context['org'] = org[0]
			
			return render(request, "shop/report_list_income.html", context=context)

	else:
		form = Date_report_income()

	context = {'form': form}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/reports_income.html", context=context)


#отчет по расходу
def expense_report(request):

	if request.method == 'POST':
		form = Date_report_income(data=request.POST)
		if form.is_valid():			
			d_from = form.cleaned_data.get("date_from")
			d_by = form.cleaned_data.get("date_by")

			rec_list = Expense_number.objects.filter(time_create__gte=d_from, time_create__lte=d_by)

			context = {"receipt_list_view": rec_list}
			org = Organization.objects.all()
			if org:
				context['org'] = org[0]
			
			return render(request, "shop/report_list_expense.html", context=context)

	else:
		form = Date_report_income()

	context = {'form': form}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/reports_expense.html", context=context)
	


# <a href="{% url 'order_list_open' i %}"><button class="open_order">Открыть заказ</button></a> тут ошибка
#отчет по продажам
def sales_report(request):

	if request.method == 'POST':
		form = Date_report_income(data=request.POST)
		if form.is_valid():			
			d_from = form.cleaned_data.get("date_from")
			d_by = form.cleaned_data.get("date_by")
			
			order_list = Order_list_bought.objects.filter(time_create__gte=d_from, time_create__lte=d_by)#тут сделать запрос другой, подумать
			print("!!!!!!!!!!!!!!!!!!!!")
			print(order_list)

			context = {"order_list": order_list}
			org = Organization.objects.all()
			if org:
				context['org'] = org[0]
			
			return render(request, "shop/report_sales_list.html", context=context)

	else:
		form = Date_report_income()

	context = {'form': form}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/reports_sales.html", context=context)


#тут товар и сколько всего продано этого товара за период
def sales_report_summary(request):

	if request.method == 'POST':
		form = Date_report_income(data=request.POST)
		if form.is_valid():			
			d_from = form.cleaned_data.get("date_from")
			d_by = form.cleaned_data.get("date_by")

			order_list = Order_list_bought.objects.filter(time_create__gte=d_from, time_create__lte=d_by)
			
			
			report_quantity = {}
			for i in order_list:
				if i.state_order == True:
					if report_quantity.get(i.product_id) == None:
						report_quantity[i.product_id] = i.quantity
					else:
						report_quantity[i.product_id] += i.quantity

			
			context = {"report_quantity": report_quantity}


			org = Organization.objects.all()
			if org:
				context['org'] = org[0]
			
			return render(request, "shop/report_sales_summary_list.html", context=context)

	else:
		form = Date_report_income()

	context = {'form': form}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/reports_sales_summary.html", context=context)



# class GoodsViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
# 	pass



