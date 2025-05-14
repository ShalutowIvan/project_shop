from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .models import *
from .forms import *
import pandas as pd
import string
import random
from transliterate import translit
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers_receipt import *
from .serializers_goods import *
from rest_framework.decorators import api_view
from rest_framework import status
import os


#список накладных просто вывод
class Get_receipt_list(APIView):

    def get(self, request):
        rec_list = Receipt_number.objects.all()

        return Response(Receipt_number_serializer(instance=rec_list, many=True).data)


#создание документа
class Receipt_document_create_api(APIView):
    
    def post(self, request, *args, **kwargs):
        
        serializer = Receipt_number_serializer(data=request.data)

        if serializer.is_valid():            
            # serializer.validated_data["user"] = self.request.user# юзера потом тянуть из токена, когда запилю авторизацию. 
            serializer.save()
            
            return Response({"success": True, })
        else:

            return Response({"error": serializer.errors}, status=400)


#открытие документа
class Receipt_document_open_api(APIView):

    def get(self, request, number_receipt):
        goods_in_receipt = Receipt_list.objects.filter(number_receipt=number_receipt)#тут список, queryset

        return Response(Receipt_list_serializer(instance=goods_in_receipt, many=True).data)


#получение позиции из таблицы с номерами документов. Роут относится к открытию дока. Номери этот роут используется в открытом доке
class Receipt_number_open_api(APIView):

    def get(self, request, number_receipt):
        number_receipt = Receipt_number.objects.get(id=number_receipt)

        return Response(Receipt_number_serializer(instance=number_receipt, many=False).data)


#проведение документа
@api_view(['GET'])
def api_receipt_list_activate(request, receipt_activate):
    doc = Receipt_number.objects.get(id=receipt_activate)

    data = {'state_receipt': doc.state}

    if doc.state == False:
        list_goods_to_add = Receipt_list.objects.filter(number_receipt=receipt_activate)
        gen_list = [i.product.id for i in list_goods_to_add]

        #список товаров из таблицы товары, которые содержатся в документе
        list_good = Goods.objects.filter(
            pk__in=gen_list)# не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

        list_good = list(list_good)

        #перебираем сгенерированный лист товаров и добавляем остаток по документу к каждому товару
        for i in range(len(gen_list)):
            list_good[i].stock += list_goods_to_add[i].quantity        

        #пишем товары в базу
        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])
        #меняем состояние на тру - проведен и кидаем в базу
        doc.state = True
        doc.save()
        data = {'state_receipt': doc.state}

    return Response(data, status=status.HTTP_200_OK)


#отмена проведения документа
@api_view(['GET'])
def api_receipt_list_deactivate(request, receipt_deactivate):
    doc = Receipt_number.objects.get(id=receipt_deactivate)
    data = {'state_receipt': doc.state}

    if doc.state == True:
        list_goods_to_add = Receipt_list.objects.filter(number_receipt=receipt_deactivate)
        gen_list = [i.product.id for i in list_goods_to_add]

        list_good = Goods.objects.filter(pk__in=gen_list)

        list_good = list(list_good)

        for i in range(len(gen_list)):
            list_good[i].stock -= list_goods_to_add[i].quantity

        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

        doc.state = False
        doc.save()
        data = {'state_receipt': doc.state}

    return Response(data, status=status.HTTP_200_OK)


# приходный документ - удаление, удаляется и таблица с номером документа и товары с этим же номером документа
@api_view(['GET'])
def api_receipt_document_delete(request, number_delete_receipt):
    try:
        rec = Receipt_number.objects.get(id=number_delete_receipt)
        good_list_delete = Receipt_list.objects.filter(number_receipt=number_delete_receipt)

        rec.delete()
        good_list_delete.delete()
        print("Приходный документ удален.")
        return Response({"success": True}, status=status.HTTP_200_OK)    
    except Exception as ex:
        print("Ошибка при удалении документа:", ex)
        return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)


#добавление товара в накладную. Это будет постоянно открытая форма
class Receipt_add_goods_api(APIView):


    def post(self, request, number_doc):
        serializer = Receipt_add_good_serializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(id=1)            
            good = Goods.objects.get(name_product=serializer.validated_data["newGood"])            
            good_in_receipt = Receipt_list.objects.filter(product=good) & Receipt_list.objects.filter(number_receipt=number_doc)

            if not good_in_receipt:#проверка есть ли такой товар уже в списке
                new_good_in_receipt = Receipt_list(product=good, number_receipt=number_doc, quantity=1, user=user)
                new_good_in_receipt.save()            
                return Response(Receipt_list_serializer(instance=new_good_in_receipt, many=False).data)

            return Response({"answer": "empty"})
        else:
            return Response({"error": serializer.errors}, status=400)


#удаление позиции
@api_view(['DELETE'])
def api_receipt_delete_goods(request, id_delete_good):
    try:
        list_delete = Receipt_list.objects.get(id=id_delete_good)
        list_delete.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)    
    except Exception as ex:
        print("Ошибка при удалении товара:", ex)
        return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)


#роут для сохранения накладной после изменения колва
class Receipt_save_api(APIView):

    def patch(self, request):
        serializer = Receipt_save_good_serializer(data=request.data)

        if serializer.is_valid():
            # print(serializer.data['items'])#тут я получаю данные с колвом и ИД позиций в накладной. Нужно найти соответствуюзщие позиции в таблице в джанго и в них перезаписать колво.
            #получаю списки и сортирую их по возрастанию id, потому что там порядок рандом...            
            data = serializer.data['items']
            data = sorted(data, key=lambda x: x["id"])
            list_id = [ i["id"] for i in serializer.data['items']]            
            list_good = Receipt_list.objects.filter(pk__in=list_id)            
            list_good = sorted(list(list_good), key=lambda x: x.id)  

            products_to_update = []

            for j in range(len(list_id)):
                print(data[j]["customPrice"])

                list_good[j].quantity = data[j]["quantity"]
                if data[j]["customPrice"] != 0:
                    list_good[j].product.price = float(data[j]["customPrice"])
                    
                    products_to_update.append(list_good[j].product)

            goods = Receipt_list.objects.bulk_update(objs=list_good, fields=["quantity"])

            if products_to_update != []:
                Goods.objects.bulk_update(objs=products_to_update, fields=["price"])


            
            return Response({"Все": "Супер"})
        else:
            return Response({"error": serializer.errors}, status=400)



#скачивание файла шаблона для загрузки наклданой
@api_view(['GET'])
def url_from_load_template_receipt_api(request):    
    path = os.path.abspath(r"shop\static\shop\xls\template_receipt.xlsx")
    response = FileResponse(open(path, 'rb'))
    
    return response


#загрузка файла накладной
class Receipt_load_file_api(APIView):

    def post(self, request, number_receipt, *args, **kwargs):       
        
        fake_user = User.objects.get(id=1)        
        file = request.FILES['load_file']  # тут имя файла

        receipts = []
        buffer_goods = []
        try:
            file_receipt = pd.read_excel(file)

            list_good_in_file = [i[0] for i in file_receipt.values]

            query_objects_in_base = Goods.objects.filter(name_product__in=list_good_in_file)
            goods_name_in_base = [i.name_product for i in query_objects_in_base]
                        
            #алгоритм аналогичен как в инвентаризации, только здесь каждый элемент это не список, а объект, либо если нет объекта, то 0 добавляем, а не пустую коллекцию. 
            list_goods = []
            for i in list_good_in_file:
                if i not in goods_name_in_base:
                    list_goods.append(0)
                    continue
                for j in query_objects_in_base:
                    if j.name_product == i:
                        list_goods.append(j)            

            query_goods_in_receipt = list(Receipt_list.objects.filter(number_receipt=number_receipt))
            goods_in_receipt = [i.product.name_product for i in query_goods_in_receipt]#делаем список из названий товара текущей накладной
            objs_in_receipt = []#это будет список объектов товаров из текущей накладной, в которых нужно обновить колво из загружаемого файла. 

            #это для тоже самое что и выше, но для обновления колва в буффере накладной, то есть в списке товаров, которых еще нет в общем каталоге товаров. 
            query_goods_in_receipt_buffer = list(Buffer_receipt.objects.filter(number_receipt=number_receipt))
            goods_in_receipt_buffer = [i.product for i in query_goods_in_receipt_buffer]
            objs_in_receipt_buffer = []        

            for i in range(len(list_good_in_file)):
                if list_goods[i] != 0:#0 означает что товара нет в базе, и если не 0, значит товар есть в базе и его добавляем в накладную
                    if list_good_in_file[i] in goods_in_receipt:#тут колво обновляться у существующего товара в накладной
                        obj_receipt = query_goods_in_receipt[goods_in_receipt.index(list_good_in_file[i])]
                        obj_receipt.quantity = file_receipt.values[i][1]                       
                        objs_in_receipt.append(obj_receipt)
                        continue

                    receipts.append(
                        Receipt_list(
                            product=list_goods[i],
                            number_receipt=number_receipt,                                                        
                            quantity=file_receipt.values[i][1],
                            user=fake_user
                        ))
                else:
                    if list_good_in_file[i] in goods_in_receipt_buffer:
                        obj_receipt_buffer = query_goods_in_receipt_buffer[goods_in_receipt_buffer.index(list_good_in_file[i])]
                        obj_receipt_buffer.quantity = file_receipt.values[i][1]
                        objs_in_receipt_buffer.append(obj_receipt_buffer)
                        continue

                    buffer_goods.append(Buffer_receipt(
                        product=file_receipt.values[i][0],
                        number_receipt=number_receipt,                        
                        quantity=file_receipt.values[i][1],
                        user=fake_user
                    ))

            if receipts != []:
                receipts_create = Receipt_list.objects.bulk_create(receipts)
            if buffer_goods != []:
                buffer_create = Buffer_receipt.objects.bulk_create(buffer_goods)
            if objs_in_receipt != []:
                receipt_update_file = Receipt_list.objects.bulk_update(objs=objs_in_receipt, fields=["quantity",])
            if objs_in_receipt_buffer != []:
                receipt_update_file_buffer = Buffer_receipt.objects.bulk_update(objs=objs_in_receipt_buffer, fields=["quantity",])
            

            return Response({
                'message': 'File processed successfully',
                # 'data': data,
                # 'rows_count': len(data)
            }, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            return Response(
                {'error': str(ex)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


#загрузка товаров из буфера после загрузки файла
class Receipt_load_buffer(APIView):
    
    def get(self, request, number_receipt):
        goods_in_receipt = Buffer_receipt.objects.filter(number_receipt=number_receipt)#тут список, queryset

        return Response(Receipt_list_buffer_serializer(instance=goods_in_receipt, many=True).data)


#удаление из буфера
@api_view(['DELETE'])
def api_receipt_delete_goods_buffer(request, id_delete_good):
    try:
        list_delete = Buffer_receipt.objects.get(id=id_delete_good)
        list_delete.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)    
    except Exception as ex:
        print("Ошибка при удалении товара:", ex)
        return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)


# добавить если нет в бд
class Receipt_add_if_not_in_base_api(APIView):

    def post(self, request, number_receipt):
        try:
            fake_user = User.objects.get(id=1)
            good_in_buffer = Buffer_receipt.objects.get(number_receipt=number_receipt)
            letters = string.ascii_lowercase  # это создания артикула, будет случайная последовательность символов

            good_in_base = Goods(
                name_product=good_in_buffer.product,
                slug=translit(good_in_buffer.product, language_code='ru', reversed=True),
                vendor_code=''.join(random.choice(letters) for i in range(15)),
                price=0,
                stock=0,
                group=Group.objects.get(name_group="Без группы"),
                photo="_",
                user=fake_user
            )
            good_in_base.save()

            good_in_receipt = Receipt_list(
                product=good_in_base,
                number_receipt=number_receipt,
                quantity=good_in_buffer.quantity,
                user=fake_user
            )
            good_in_receipt.save()

            good_in_buffer.delete()
            return Response(Receipt_list_serializer(instance=good_in_receipt, many=False).data)
        except Exception as ex:
            print("Ошибка при удалении товара:", ex)
            return Response({"success": True}, status=status.HTTP_400_BAD_REQUEST)



