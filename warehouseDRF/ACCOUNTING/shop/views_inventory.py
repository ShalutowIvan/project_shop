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


#кнопка открыть
# <a href="{% url 'receipt_document_open' j.id %}"><button class="open_receipt">Открыть документ</button></a>
#кнопка удалить
# <a href="{% url 'receipt_document_delete' j.id %}"><button class="delete_receipt">Удалить документ</button></a>
#кнопка создать
# <a href="{% url 'receipt_document_create' %}"><h1>Добавить документ</h1></a>


def inventory_create(request, number_group):
	if request.method == 'POST':
		form = Inventory_number_form(data=request.POST)
		if form.is_valid():
			invent = form.save(commit=False)
			invent.save()

			return redirect('inventory_open', invent.id)

	else:
		form = Inventory_number_form()

	context = {'form': form}

	return render(request, 'shop/inventory_create.html', context=context)



def inventory_open(request, number):
	return


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