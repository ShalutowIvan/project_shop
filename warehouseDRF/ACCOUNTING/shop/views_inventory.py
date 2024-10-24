from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import pandas as pd
import string
import random
from transliterate import translit


###################################################################################
#инвентаризация - начало
# в инвенту закидываются все товары из группы с остатком из базы, остаток из базы закидывается в колонку колва "было"
	#колонка стало нужно заполнять, она пустая либо можно что туда закинуть, после проведения инвенты колво прибавляется либо отнимается при отмене проведения, то есть именно сложение либо вычитание

def inventory_list(request):
	inv_list = Inventory_number.objects.all()

	context = {"inventory_list_view": inv_list}

	org = Organization.objects.all()
	if org:
		context['org'] = org[0]

	return render(request, "shop/inventory_list.html", context=context)


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
	invent_group = Inventory_group.objects.filter(number_inventory=inv_number)

	invent.delete()
	invent_list_delete.delete()
	invent_group.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

#тут остановился!!!!!!!!!!!
def inventory_open(request, inv_number):

	if request.method == 'POST':
		form = Inventiry_open_form(data=request.POST)#форму поменять
		if form.is_valid():
			invent = form.save(commit=False)
			invent.save()

			return redirect('inventory_open', invent.id)#нужно решить куда будет редирект

	else:
		form = Inventiry_open_form()
	
	inv_number_obj = Inventory_number.objects.get(id=int(inv_number))
	inv_good_list = Inventory_list.objects.filter(number_inventory=int(inv_number))
	inv_buffer = Inventory_buffer.objects.filter(number_inventory=int(inv_number))
	context = {'form': form, "number_inv": inv_number, 'inv_good_list': inv_good_list, "inv_number_obj": inv_number_obj, "inv_buffer": inv_buffer}

	#тут доделать, много логики еще. Должна быть форма с товарами из добавленных групп, поле для заполнения это колво в колонке стало
	org = Organization.objects.all()

	if org:
		context['org'] = org[0]
	
	return render(request, "shop/inventory_open.html", context=context)

#загрузка файла из html
# {% if receipt_doc.state == False %}
# <a href="{% url 'receipt_load_file' number %}"><button>Загрузить файл накладной</button></a>
# {% endif %}

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


def inventory_add_group(request, inv_number):
	if request.method == 'POST':
		form = Inventory_group_form(data=request.POST)
		if form.is_valid():
			group = form.save(commit=False)
			group.number_inventory = inv_number
			group.save()

			return redirect('inventory_open', inv_number)

	else:
		form = Inventory_group_form()

	context = {'form': form, "inv_number": inv_number}

	return render(request, "shop/inventory_add_group.html", context=context)



def inventory_save(request, number):
	return


def inventory_activate(request, number):
	return


def inventory_deactivate(request, number):
	return


def inventory_load_file(request, number):
	return


def inventory_result(request, number):#подсчет недостачи и излишков
	return





#####################################################################################