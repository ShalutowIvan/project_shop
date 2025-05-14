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
from rest_framework.decorators import api_view
from rest_framework import status


###########################################################################
# РАСХОДНЫЙ документ - начало

# отображение списка документов
class Get_expense_list(APIView):

    def get(self, request):
        expense_list = Expense_number.objects.all()

        return Response(Expense_number_serializer(instance=expense_list, many=True).data)


# создание документа списания
class Expense_document_create_api(APIView):
    
    def post(self, request, *args, **kwargs):
        
        serializer = Expense_number_serializer(data=request.data)

        if serializer.is_valid():            
            # serializer.validated_data["user"] = self.request.user# юзера потом тянуть из токена, когда запилю авторизацию. 
            serializer.save()
            
            return Response({"success": True, })
        else:

            return Response({"error": serializer.errors}, status=400)


# удаление документа
@api_view(['GET'])
def api_expense_document_delete(request, number_delete_expense):
    try:
        expense = Expense_number.objects.get(id=number_delete_expense)
        good_list_delete = Expense_list.objects.filter(number_act=number_delete_expense)

        expense.delete()
        good_list_delete.delete()
        print("Расходный документ удален.")
        return Response({"success": True}, status=status.HTTP_200_OK)    
    except Exception as ex:
        print("Ошибка при удалении документа:", ex)
        return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)


#открытие документа
class Expense_document_open_api(APIView):

    def get(self, request, number_expense):
        goods_in_expense = Expense_list.objects.filter(number_act=number_expense)#тут список, queryset

        return Response(Expense_list_serializer(instance=goods_in_expense, many=True).data)


#получение позиции из таблицы с номерами документов. Роут относится к открытию дока. Номер и этот роут используется в открытом доке. Запрашивается только 1 номер. 
class Expense_number_open_api(APIView):

    def get(self, request, number_expense):
        number_expense = Expense_number.objects.get(id=number_expense)

        return Response(Expense_number_serializer(instance=number_expense, many=False).data)


class Expense_add_goods_api(APIView):

    def post(self, request, number_doc):
        serializer = Expense_add_good_serializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(id=1)            
            good = Goods.objects.get(name_product=serializer.validated_data["newGood"])            
            good_in_expense = Expense_list.objects.filter(product=good) & Expense_list.objects.filter(number_act=number_doc)

            if not good_in_expense:#проверка есть ли такой товар уже в списке
                new_good_in_expense = Expense_list(product=good, number_act=number_doc, quantity=1, user=user)
                new_good_in_expense.save()            
                return Response(Expense_list_serializer(instance=new_good_in_expense, many=False).data)

            return Response({"answer": "empty"})
        else:
            return Response({"error": serializer.errors}, status=400)



#проведение документа
@api_view(['GET'])
def api_expense_list_activate(request, expense_activate):
    doc = Expense_number.objects.get(id=expense_activate)

    data = {'state_expense': doc.state}

    if doc.state == False:
        list_goods_to_subtract = Expense_list.objects.filter(number_act=expense_activate)
        gen_list = [i.product.id for i in list_goods_to_subtract]

        #список товаров из таблицы товары, которые содержатся в документе
        list_good = Goods.objects.filter(pk__in=gen_list)#не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

        list_good = list(list_good)

        #перебираем сгенерированный лист товаров и отнимаем остаток по документу к каждому товару
        for i in range(len(gen_list)):
            list_good[i].stock -= list_goods_to_subtract[i].quantity        

        #пишем товары в базу
        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])
        #меняем состояние на тру - проведен и кидаем в базу
        doc.state = True
        doc.save()
        data = {'state_expense': doc.state}

    return Response(data, status=status.HTTP_200_OK)


#отмена проведения документа
@api_view(['GET'])
def api_expense_list_deactivate(request, expense_deactivate):
    doc = Expense_number.objects.get(id=expense_deactivate)
    data = {'state_expense': doc.state}

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
        data = {'state_expense': doc.state}

    return Response(data, status=status.HTTP_200_OK)


#удаление позиции из акта
@api_view(['DELETE'])
def api_expense_delete_goods(request, id_delete_good):
    try:
        list_delete = Expense_list.objects.get(id=id_delete_good)
        list_delete.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)    
    except Exception as ex:
        print("Ошибка при удалении товара:", ex)
        return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)


class Expense_save_api(APIView):

    def patch(self, request):
        serializer = Expense_save_good_serializer(data=request.data)

        if serializer.is_valid():
            # print(serializer.data['items'])#тут я получаю данные с колвом и ИД позиций в накладной. Нужно найти соответствуюзщие позиции в таблице в джанго и в них перезаписать колво.
            #получаю списки и сортирую их по возрастанию id, потому что там порядок рандом...            
            data = serializer.data['items']
            data = sorted(data, key=lambda x: x["id"])
            list_id = [ i["id"] for i in serializer.data['items']]            
            list_good = Expense_list.objects.filter(pk__in=list_id)            
            list_good = sorted(list(list_good), key=lambda x: x.id)

            for j in range(len(list_id)):
                list_good[j].quantity = data[j]["quantity"]
                

            goods = Expense_list.objects.bulk_update(objs=list_good, fields=["quantity"])
            
            return Response({"Все": "Супер"})
        else:
            return Response({"error": serializer.errors}, status=400)







