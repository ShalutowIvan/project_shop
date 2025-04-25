from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .models import *
from .forms import *
import pandas as pd
import string
import random
import os
from transliterate import translit
# from openpyxl import load_workbook

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers_inventory import *







###################################################################################
#инвентаризация - начало
# в инвенту закидываются все товары из группы с остатком из базы, остаток из базы закидывается в колонку колва "было"
	#колонка стало нужно заполнять, она пустая либо можно что туда закинуть, после проведения инвенты колво прибавляется либо отнимается при отмене проведения, то есть именно сложение либо вычитание

# def inventory_list(request):
# 	inv_list = Inventory_number.objects.all()

# 	context = {"inventory_list_view": inv_list}

# 	org = Organization.objects.all()
# 	if org:
# 		context['org'] = org[0]

# 	return render(request, "shop/inventory_list.html", context=context)


class Get_inventory_list(APIView):

    def get(self, request):
        inventory_list = Inventory_number.objects.all()

        return Response(Inventory_number_serializer(instance=inventory_list, many=True).data)





def inventory_create(request):
	if request.method == 'POST':
		form = Inventory_number_form(data=request.POST)
		if form.is_valid():
			invent = form.save(commit=False)
			invent.save()

			return redirect('inventory_open', invent.id)

	else:
		form = Inventory_number_form()

	context = {'form': form}
	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, 'shop/inventory_create.html', context=context)


def inventory_delete(request, inv_number):
	invent = Inventory_number.objects.get(id=inv_number)
	invent_list_delete = Inventory_list.objects.filter(number_inventory=inv_number)
	# invent_group = Inventory_group.objects.filter(number_inventory=inv_number)

	invent.delete()
	invent_list_delete.delete()
	# invent_group.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])



def inventory_open(request, inv_number):
	inv_number_obj = Inventory_number.objects.get(id=int(inv_number))
	inv_good_list = Inventory_list.objects.filter(number_inventory=int(inv_number))
	inv_buffer = Inventory_buffer.objects.filter(number_inventory=int(inv_number))

	if request.method == 'POST':
		try:			
			for i in inv_good_list:
				i.quantity_new = float(request.POST[str(i.id)].replace(",", "."))#ид работает как имя из формы

			list_good = inv_good_list#возможно нужно будет тип поменять на list			
			goods = Inventory_list.objects.bulk_update(objs=list_good, fields=["quantity_new",])
			return redirect('inventory_open', inv_number)#остаемся на этой же странице, но тянем все из БД. 

		except Exception as ex:
			context = {"error": ex, "inv_number": inv_number}
			return render(request, 'shop/error_with_inventory.html', context=context)
	
	context = {"number_inv": inv_number, 'inv_good_list': inv_good_list, "inv_number_obj": inv_number_obj, "inv_buffer": inv_buffer}
	
	org = Organization.objects.all()

	if org:
		context['org'] = org[0]
	
	return render(request, "shop/inventory_open.html", context=context)


def inventory_add_group(request, inv_number):
	groups_query = Group.objects.all()

	if request.method == 'POST':
		# form = Inventory_group_form(data=request.POST)
		# if form.is_valid():
			# group = form.save(commit=False)
		group = Group.objects.get(id=int(request.POST["group_inv"]))#просто группа без модели
			# group.number_inventory = inv_number

		goods = Goods.objects.filter(group__slug=group.slug)
		query_list_inventory = Inventory_list.objects.filter(number_inventory=inv_number)
		list_goods_name_inventory = [i.product.name_product for i in query_list_inventory]
		good_list_from_inventory = []
		for i in goods:
			if i.name_product in list_goods_name_inventory:
				continue
			else:
				good_list_from_inventory.append(
					Inventory_list(
							product=i,
							number_inventory=inv_number,
							quantity_old=i.stock,
							quantity_new=0,
							user=request.user
							))

		if good_list_from_inventory != []:
			inventory_create = Inventory_list.objects.bulk_create(good_list_from_inventory)
			# group.save()
		return redirect('inventory_open', inv_number)
	# else:
	# 	form = Inventory_group_form()

	context = {"groups_query": groups_query, "inv_number": inv_number}

	return render(request, "shop/inventory_add_group.html", context=context)


#при проведении инвенты остаток либо отнимается либо прибивляется на разницу
def inventory_activate(request, inv_number):
	invent_number = Inventory_number.objects.get(id=inv_number)
	buffer = list(Inventory_buffer.objects.filter(number_inventory=inv_number))

	if invent_number.state == False:
		if buffer != []:#ТУТ НЕ РАБОТАЕТ УСЛОВИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			context = {"number_inv": inv_number, "undistributed_goods": "Есть не распределенные товары"}
			return render(request, "shop/error_with_inventory_buffer.html", context=context)
			# return redirect('inventory_open', inv_number)

		list_goods_in_inventory = Inventory_list.objects.filter(number_inventory=inv_number)

		gen_list = [i.product.id for i in list_goods_in_inventory]
		list_good = Goods.objects.filter(pk__in=gen_list)

		list_good = list(list_good)


		for i in range(len(gen_list)):
			if list_goods_in_inventory[i].quantity_old >= list_goods_in_inventory[i].quantity_new:
				list_good[i].stock -= list_goods_in_inventory[i].quantity_old - list_goods_in_inventory[i].quantity_new
			elif list_goods_in_inventory[i].quantity_old <= list_goods_in_inventory[i].quantity_new:
				list_good[i].stock += list_goods_in_inventory[i].quantity_new - list_goods_in_inventory[i].quantity_old

		goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

		invent_number.state = True
		invent_number.save()

	
	return redirect('inventory_open', inv_number)
	# return redirect('inventory_list')


def inventory_deactivate(request, inv_number):
	invent_number = Inventory_number.objects.get(id=inv_number)
	if invent_number.state == True:
		list_goods_in_inventory = Inventory_list.objects.filter(number_inventory=inv_number)

		gen_list = [i.product.id for i in list_goods_in_inventory]
		list_good = Goods.objects.filter(pk__in=gen_list)

		list_good = list(list_good)

		for i in range(len(gen_list)):
			if list_goods_in_inventory[i].quantity_old >= list_goods_in_inventory[i].quantity_new:
				list_good[i].stock += list_goods_in_inventory[i].quantity_old - list_goods_in_inventory[i].quantity_new
			elif list_goods_in_inventory[i].quantity_old <= list_goods_in_inventory[i].quantity_new:
				list_good[i].stock -= list_goods_in_inventory[i].quantity_new - list_goods_in_inventory[i].quantity_old

	goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

	invent_number.state = False
	invent_number.save()

	return redirect('inventory_open', inv_number)


#загрузка файла
def inventory_load_file(request, inv_number):
	if request.method == 'POST':		
		file = request.FILES['load_file']  # тут имя файла

		list_inventory = []#список объектов инвенты
		buffer_inventory = []#список объектов для буфера инвенты, то есть товаров которых нет в базе

		try:
			file_inventory = pd.read_excel(file)#прочитали файл excel, тут есть датафрейм, в нем есть таблица
			
			list_good_in_file = [i[0] for i in file_inventory.values]#взяли список названий товаров из файла
			#file_inventory.values - выцепляет строки, каждая строка из файла это список из значений столбцов. Берем первый столбец, это название товар в генераторе. Получается список названий товара из файла.

			query_objects_in_base = Goods.objects.filter(name_product__in=list_good_in_file)#фильтр товаров из базы по списку товаров из файла. То есть берем товары из базы которые есть в списке товаров из файла. 
			
			#ниже отсортировал объекты товаров из базы, чтобы порядок был такой же как из файла. Элементы с пустым списком это значит что товара нет в базе. То есть если j.name_product == i не найдет товар, то запишется элемент пустой список - [].
			list_goods = [
			tuple((j for j in query_objects_in_base if j.name_product == i))
			for i in list_good_in_file
			]
			
			#запрашиваем товары из текущей инвентаризации, чтобы потом их можно было проверить. 
			query_goods_in_invent = list(Inventory_list.objects.filter(number_inventory=inv_number))
			goods_in_invent = [i.product.name_product for i in query_goods_in_invent]#делаем список из названий товара текущей инвентаризации
			objs_in_invent = []#это будет список объектов товаров из текущей инвенты, в которых нужно обновить колво из загружаемого файла. 

			#это для тоже самое что и выше, но для обновления колва в буффере инвентаризации, то в списке товаров, которых еще нет в общем каталоге товаров. 
			query_goods_in_invent_buffer = list(Inventory_buffer.objects.filter(number_inventory=inv_number))
			goods_in_invent_buffer = [i.product for i in query_goods_in_invent_buffer]
			objs_in_invent_buffer = []

			for i in range(len(list_good_in_file)):
				if list_goods[i] != ():#если товар в базе есть такой, то объект этого товара добавляем в инвенту
					if list_good_in_file[i] in goods_in_invent:
						obj_invent = query_goods_in_invent[goods_in_invent.index(list_good_in_file[i])]
						obj_invent.quantity_new = file_inventory.values[i][1]						
						objs_in_invent.append(obj_invent)
						continue#тут колво обновляться у существующего товара

					list_inventory.append(
                        Inventory_list(
                            product=list_goods[i][0],
                            number_inventory=inv_number,                            
                            quantity_old=list_goods[i][0].stock,
                            quantity_new=file_inventory.values[i][1],
                            user=request.user
                        ))
				else:#иначе есть товара нет, то добавляем его в буфер, и в название пишем название из файла
					if list_good_in_file[i] in goods_in_invent_buffer:
						obj_invent_buffer = query_goods_in_invent_buffer[goods_in_invent_buffer.index(list_good_in_file[i])]
						obj_invent_buffer.quantity_new = file_inventory.values[i][1]
						objs_in_invent_buffer.append(obj_invent_buffer)
						continue

					buffer_inventory.append(Inventory_buffer(
                        product=file_inventory.values[i][0],
                        number_inventory=inv_number,
                        quantity_old=0,
                        quantity_new=file_inventory.values[i][1],
                        user=request.user
                    ))

			if list_inventory != []:
				inventory_create = Inventory_list.objects.bulk_create(list_inventory)
			if buffer_inventory != []:
				buffer_inventory = Inventory_buffer.objects.bulk_create(buffer_inventory)				
			if objs_in_invent != []:
				invent_update_file = Inventory_list.objects.bulk_update(objs=objs_in_invent, fields=["quantity_new",])
			if objs_in_invent_buffer != []:
				invent_update_file_buffer = Inventory_buffer.objects.bulk_update(objs=objs_in_invent_buffer, fields=["quantity_new",])

			
			#запись файлов которых нет в базе в файл xlsx. Его можно потом скачать. Берется из буфера инвентаризации
			name = [i.product for i in buffer_inventory]
			quantity = [i.quantity_new for i in buffer_inventory]
			data = {"Название": name, "Количество": quantity}
			df = pd.DataFrame(data)
			df.to_excel('xls/error.xlsx', index=False)
			########################################################################

			return redirect('inventory_open', inv_number)

		except Exception as ex:
			context = {"error": ex}

			return render(request, 'shop/error_with_loadfile_receipt.html', context=context)

	context = {"inv_number": inv_number}

	return render(request, 'shop/inventory_load_file.html', context=context)


#добавить все товары из буфера в инвентаризацию если их нет
def inventory_add_all_buffer(request, number_inv):
	good_in_buffer = Inventory_buffer.objects.filter(number_inventory=number_inv)
	letters = string.ascii_lowercase
	no_group = Group.objects.get(name_group="Без группы")
	list_inventory = []
	list_goods = []

	for i in good_in_buffer:
		goods_from_buffer = Goods(
        	name_product=i.product,
        	slug=translit(i.product, language_code='ru', reversed=True),
        	vendor_code=''.join(random.choice(letters) for i in range(15)),
        	price=0,
        	stock=0,
        	group=no_group,
        	photo="_",
        	user=request.user
    		)
		list_goods.append(goods_from_buffer)

		#ост тут
		list_inventory.append(
			Inventory_list(
			product=goods_from_buffer,
			number_inventory=number_inv,                            
			quantity_old=0,
			quantity_new=i.quantity_new,
			user=request.user
            ))

	if list_goods != []:
		goods_create = Goods.objects.bulk_create(list_goods)
	if list_inventory != []:
		inventory_create = Inventory_list.objects.bulk_create(list_inventory)

	good_in_buffer.delete()


	return redirect('inventory_open', number_inv)



#урл для скачивания файла шаблона инвентаризации
def url_from_load_template_inv(request):
	# filepath = create_empty_excel(columns=["Название", "Артикул", "Цена", "Остаток", "Группа"], filename="Шаблон для загрузки товаров.xlsx")
	path = os.path.abspath(r"shop\static\shop\xls\template_inv.xlsx")
	response = FileResponse(open(path, 'rb'))
	#подумать что сделать со ссылкой на файл шаблона, он у меня берется по абсолютной ссылке, и на другом пк не будет работать
	return response


#урл для скачивания файла с ошибками
def url_from_load_error_inv(request):
	# filepath = create_empty_excel(columns=["Название", "Артикул", "Цена", "Остаток", "Группа"], filename="Шаблон для загрузки товаров.xlsx")
	path = os.path.abspath(r"xls\error.xlsx")
	response = FileResponse(open(path, 'rb'))
	#подумать что сделать со ссылкой на файл шаблона, он у меня берется по абсолютной ссылке, и на другом пк не будет работать
	return response


#добавить товар если нет в БД
def inventory_add_if_not_in_base(request, number_good):
    good_in_buffer = Inventory_buffer.objects.get(id=number_good)
    letters = string.ascii_lowercase  # это создания артикула, будет случайная последовательность символов

    good_in_base = Goods(
        name_product=good_in_buffer.product,
        slug=translit(good_in_buffer.product, language_code='ru', reversed=True),
        vendor_code=''.join(random.choice(letters) for i in range(15)),
        price=0,
        stock=0,
        group=Group.objects.get(name_group="Без группы"),
        photo="_",
        user=request.user
    )
    good_in_base.save()

    good_in_inventory = Inventory_list(
        product=good_in_base,
        number_inventory=good_in_buffer.number_inventory,
		quantity_old=0,
        quantity_new=good_in_buffer.quantity_new,
        user=request.user
    )
    good_in_inventory.save()

    good_in_buffer.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])



# заменить товар на другой если нет в бд. Возможно лучше еще сделать кнопку для отдельного добавления товара в инвенту
def inventory_change_if_not_in_base(request, number_good):
	good_in_buffer = Inventory_buffer.objects.get(id=number_good)
	number_inv = good_in_buffer.number_inventory
	if request.method == 'POST':
		form = Inventory_add_goods_form(data=request.POST)
		if form.is_valid():
			good_in_form = form.cleaned_data.get("product")
			good_in_invent = Inventory_list.objects.filter(product=good_in_form)
			if good_in_invent:#при добавлении товара который уже есть в инвенте, обновится колво в товаре инвенты
				good_in_invent.quantity_new = good_in_buffer.quantity_new
				good_in_invent.save()
			else:
				good_in_inv = form.save(commit=False)
				good_in_inv.number_inventory = number_inv
				good_in_inv.quantity_old = good_in_form.stock
				good_in_inv.quantity_new = good_in_buffer.quantity_new
				good_in_inv.user = request.user
				good_in_inv.save()
			good_in_buffer.delete()

			return redirect('inventory_open', number_inv)
	else:
		form = Inventory_add_goods_form()

	context = {'form': form, "number_good": number_good}

	return render(request, "shop/inventory_goods_add.html", context=context)



# def inventory_add_goods(request, number_inv):
#
# 	if request.method == 'POST':
# 		form = Inventory_add_goods_form(data=request.POST)
# 		if form.is_valid():
# 			good_in_inv = form.save(commit=False)
# 			good_in_inv.number_inventory = number_inv
# 			# good_in_inv.quantity_old = form.cleaned_data.get("quantity_old")#тут может быть ошибка
# 			good_in_inv.quantity_old = 0
# 			good_in_inv.user = request.user
# 			good_in_inv.save()
# 			# good_in_buffer.delete()
#
# 			return redirect('inventory_open', number_inv)
#
# 	else:
# 		form = Receipt_add_goods_form()
#
# 	context = {'form': form, "number_doc": number_inv}
#
# 	return render(request, "shop/receipt_goods_add.html", context=context)


def inventory_delete_position_if_not_in_base(request, id_good):
	invent_good_delete = Inventory_buffer.objects.get(id=id_good)
	# inv_number = invent_good_delete.number_inventory
	invent_good_delete.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	# return redirect('inventory_open', inv_number)



def inventory_update_quantity(request, number_inv):
	query_goods_in_invent = Inventory_list.objects.filter(number_inventory=number_inv)
	for i in query_goods_in_invent:
		i.quantity_old = i.product.stock

	goods = Inventory_list.objects.bulk_update(objs=query_goods_in_invent, fields=["quantity_old",])

	return redirect('inventory_open', number_inv)


def inventory_print(request, inv_number):#ост тут
	list_inventory = Inventory_list.objects.filter(number_inventory=inv_number)

	name = [i.product for i in list_inventory]
	quantity_old = [i.quantity_old for i in list_inventory]
	quantity_new = [i.quantity_new for i in list_inventory]
	data = {"Название": name, "Количество было": quantity_old, "Количество стало": quantity_new}
	df = pd.DataFrame(data)
	df.to_excel('shop/static/shop/xls/print_inventory.xlsx', index=False)
	
	path = os.path.abspath(r"shop\static\shop\xls\print_inventory.xlsx")
	response = FileResponse(open(path, 'rb'))
	#подумать что сделать со ссылкой на файл шаблона, он у меня берется по абсолютной ссылке, и на другом пк не будет работать
	return response



def inventory_result(request, inv_number):#подсчет недостачи и излишков
	return






#####################################################################################




# def inventory_delete_position(request, id_good_in_inventory):
# 	invent_good_delete = Inventory_list.objects.get(id=id_good_in_inventory)
# 	# inv_number = invent_good_delete.number_inventory
# 	invent_good_delete.delete()
# 	return HttpResponseRedirect(request.META['HTTP_REFERER'])
# 	# return redirect('inventory_open', inv_number)

# <a href="{% url 'inventory_delete_position' i.id %}"><button class="delete_position">Удалить</button></a>
#удаление в цикле из формы не работает


# <!--проведение и деактивация и сохранение документа ниже-->
# {% if inv_number_obj.state == False %}
# <a href="{% url '' number_inv %}"><h3>Добавить группу товара</h3></a>
#
# <a href="{% url '' number_inv %}"><button class="activate_inv">Провести документ</button></a>
#
# <a href="{% url '' number_inv %}"><button class="activate_inv">Сохранить документ</button></a>
#
# {% else %}
#
# <a href="{% url '' number_inv %}"><button class="deactivate_receipt">Отмена проведения документа</button></a>
#
# {% endif %}


#ссылка на статью хабра про загрузку файлов xls
# https://habr.com/ru/articles/824050/

# def url_from_load_template_inv(request, sheet_name: str = 'Sheet1'):
# 	# columns = {'Имя': ['Анна', 'Петр', 'Мария'],
#     #     'Возраст': [25, 30, 35],
#     #     'Город': ['Москва', 'Санкт-Петербург', 'Киев']}
# 	# filename = "Excel"
# 	# df = pd.DataFrame(columns)
#
# 	# if not os.path.exists('excel_files'):
# 	# 	os.makedirs('excel_files')
#
# 	# filepath = os.path.join('excel_files', filename)
# 	# excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
# 	# df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
# 	# excel_writer._save()
# 	df.to_excel('данные.xlsx', index=False)
#
# 	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	# return filepath