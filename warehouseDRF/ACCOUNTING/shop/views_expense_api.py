from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

import string
import random
from transliterate import translit

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers_expense import *



###########################################################################
# РАСХОДНЫЙ документ - начало - открытие
# @login_required
# def expense_list(request):
#     expense_list = Expense_number.objects.all()

#     context = {"expense_list_view": expense_list}

#     org = Organization.objects.all()
#     if org:
#         context['org'] = org[0]

#     return render(request, "shop/expense_list.html", context=context)


class Get_expense_list(APIView):

    def get(self, request):
        expense_list = Expense_number.objects.all()

        return Response(Expense_number_serializer(instance=expense_list, many=True).data)



# создание акта списания - добавить документ с добавлением коммента. После создания документа он сразу открывается - редирект на урл receipt_document_open
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


# приходный документ - открытие
@login_required
def expense_document_open(request, open_expense):
    expense_open = Expense_number.objects.get(id=open_expense)
    expense_good_list = Expense_list.objects.filter(number_act=open_expense)  # поиск по номеру акта
    context = {"number": open_expense, 'expense_good_list': expense_good_list, "expense_doc": expense_open}

    org = Organization.objects.all()

    if org:
        context['org'] = org[0]

    return render(request, "shop/expense_open.html", context=context)


# проведение документа - это функция после которой меняется статус документа и добавляется товар на остаток на основании документа
@login_required
def expense_document_activate(request, expense_activate):
    doc = Expense_number.objects.get(id=expense_activate)
    if doc.state == False:
        list_goods_to_subtract = Expense_list.objects.filter(number_act=expense_activate)
        gen_list = [i.product.id for i in list_goods_to_subtract]

        list_good = Goods.objects.filter(
            pk__in=gen_list)  # не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

        list_good = list(list_good)

        for i in range(len(gen_list)):
            list_good[i].stock -= list_goods_to_subtract[i].quantity

        # print(list_good[i].stock)

        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

        doc.state = True
        doc.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# отмена проведения документа
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

        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

        doc.state = False
        doc.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# приходный документ - удаление, удаляется и таблица с номером документа и товары с этим же номером документа
@login_required
def expense_document_delete(request, number_delete_expense):
    rec = Expense_number.objects.get(id=number_delete_expense)
    good_list_delete = Expense_list.objects.filter(number_act=number_delete_expense)

    rec.delete()
    good_list_delete.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# добавление товара - в открытом документе. number_doc берется из номера открытого документа, который мы открыли функцией receipt_document_open он прокидывается в html.
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


# удаление товара из накладной
@login_required
def expense_delete_goods(request, number_delete_good):
    list_delete = Expense_list.objects.get(id=number_delete_good)
    list_delete.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])