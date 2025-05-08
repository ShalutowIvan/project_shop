from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

#список накладных просто вывод
# @login_required
# def receipt_list(request):
#     rec_list = Receipt_number.objects.all()

#     context = {"receipt_list_view": rec_list}

#     org = Organization.objects.all()
#     if org:
#         context['org'] = org[0]

#     return render(request, "shop/receipt_list.html", context=context)


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


#получение позиции из таблицы с номерами документов. Роут относится к открытию дока
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

        if serializer.is_valid():#тут допилить логику, чтобы одинаковые позиции повторно не добавлялись
            user = User.objects.get(id=1)            
            good = Goods.objects.get(name_product=serializer.validated_data["newGood"])
            new_good_in_receipt = Receipt_list(product=good, number_receipt=number_doc, quantity=1, user=user)
            new_good_in_receipt.save()            
            return Response(Receipt_list_serializer(instance=new_good_in_receipt, many=False).data)
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



class Receipt_save_api(APIView):

    def put(self, request):
        serializer = Receipt_save_good_serializer(data=request.data)


        if serializer.is_valid():
            print(serializer.data['items'])#тут я получаю данные с колвом и ИД позиций в накладной. Нужно найти соответствуюзщие позиции в таблице в джанго и в них перезаписать колво. Осталось только логику тут в питоне допилить. 




            # user = User.objects.get(id=1)            
            # good = Goods.objects.get(name_product=serializer.validated_data["newGood"])
            # new_good_in_receipt = Receipt_list(product=good, number_receipt=number_doc, quantity=1, user=user)
            # new_good_in_receipt.save()            
            # return Response(Receipt_list_serializer(instance=new_good_in_receipt, many=False).data)
            return Response({"Все": "Супер"})
        else:
            return Response({"error": serializer.errors}, status=400)






#редактирование позиции в накладной
class Receipt_document_edit_api(APIView):

    def patch(self, request):
        pass



# редактирование позиции в накладной
def receipt_document_edit(request, number_edit_good):
    if request.method == 'POST':
        form = Receipt_edit_goods_form(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            good_edit = Receipt_list.objects.get(id=number_edit_good)
            good_edit.quantity = quantity

            good_edit.save()

            return redirect('receipt_document_open', good_edit.number_receipt)

    else:
        form = Receipt_edit_goods_form()

    context = {'form': form, "number_edit_good": number_edit_good}

    return render(request, "shop/receipt_goods_edit.html", context=context)







# загрузка файла накладной
def receipt_load_file(request, number_doc):
    if request.method == 'POST':
        p = request.POST
        f = request.FILES  # тут мультивалуедикт
        file = request.FILES['load_file']  # тут имя файла

        receipts = []
        buffer_goods = []

        try:
            file_receipt = pd.read_excel(file)

            list_good_in_file = [i[0] for i in file_receipt.values]

            query_objects_in_base = Goods.objects.filter(name_product__in=list_good_in_file)
            goods_name_in_base = [i.name_product for i in query_objects_in_base]
            

            # list_goods = [
            # tuple((j for j in query_objects_in_base if j.name_product == i))
            # for i in list_good_in_file
            # ]
            
            #алкгоритм аналогичен как в инвентаризации, только здесь каждый элемент это не список, а объект, либо если нет объекта, то 0 добавляем, а не пустую коллекцию. 
            list_goods = []
            for i in list_good_in_file:
                if i not in goods_name_in_base:
                    list_goods.append(0)
                    continue
                for j in query_objects_in_base:
                    if j.name_product == i:
                        list_goods.append(j)

            # print(list_goods)

            # for i in file_receipt.values:
            #     try:
            #         receipts.append(
            #             Receipt_list(
            #                 product=Goods.objects.get(name_product=i[0]),
            #                 number_receipt=number_doc,
            #                 quantity=i[1],
            #                 user=request.user
            #             ))
            #     except ObjectDoesNotExist:
            #         buffer_goods.append(Buffer_receipt(
            #             product=i[0],
            #             number_receipt=number_doc,
            #             quantity=i[1],
            #             user=request.user
            #         ))

            query_goods_in_receipt = list(Receipt_list.objects.filter(number_receipt=number_doc))
            goods_in_receipt = [i.product.name_product for i in query_goods_in_receipt]#делаем список из названий товара текущей накладной
            objs_in_receipt = []#это будет список объектов товаров из текущей накладной, в которых нужно обновить колво из загружаемого файла. 

            #это для тоже самое что и выше, но для обновления колва в буффере накладной, то есть в списке товаров, которых еще нет в общем каталоге товаров. 
            query_goods_in_receipt_buffer = list(Buffer_receipt.objects.filter(number_receipt=number_doc))
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
                            number_receipt=number_doc,                                                        
                            quantity=file_receipt.values[i][1],
                            user=request.user
                        ))
                else:
                    if list_good_in_file[i] in goods_in_receipt_buffer:
                        obj_receipt_buffer = query_goods_in_receipt_buffer[goods_in_receipt_buffer.index(list_good_in_file[i])]
                        obj_receipt_buffer.quantity = file_receipt.values[i][1]
                        objs_in_receipt_buffer.append(obj_receipt_buffer)
                        continue

                    buffer_goods.append(Buffer_receipt(
                        product=file_receipt.values[i][0],
                        number_receipt=number_doc,                        
                        quantity=file_receipt.values[i][1],
                        user=request.user
                    ))

            if receipts != []:
                receipts_create = Receipt_list.objects.bulk_create(receipts)
            if buffer_goods != []:
                buffer_create = Buffer_receipt.objects.bulk_create(buffer_goods)
            if objs_in_receipt != []:
                receipt_update_file = Receipt_list.objects.bulk_update(objs=objs_in_receipt, fields=["quantity",])
            if objs_in_receipt_buffer != []:
                receipt_update_file_buffer = Buffer_receipt.objects.bulk_update(objs=objs_in_receipt_buffer, fields=["quantity",])

            return redirect('receipt_document_open', number_doc)

        except Exception as ex:
            context = {"error": ex}

            return render(request, 'shop/error_with_loadfile_receipt.html', context=context)

    context = {"number_doc": number_doc}

    return render(request, 'shop/receipt_load_file.html', context=context)


# добавить если нет в бд
def receipt_add_if_not_in_base(request, number_good):
    good_in_buffer = Buffer_receipt.objects.get(id=number_good)
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

    good_in_receipt = Receipt_list(
        product=good_in_base,
        number_receipt=good_in_buffer.number_receipt,
        quantity=good_in_buffer.quantity,
        user=request.user
    )
    good_in_receipt.save()

    good_in_buffer.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# заменить на другой если нет в бд 
def receipt_change_if_not_in_base(request, number_good):
    good_in_buffer = Buffer_receipt.objects.get(id=number_good)
    number_doc = good_in_buffer.number_receipt
    if request.method == 'POST':
        form = Receipt_add_goods_form_if_not_in_base(data=request.POST)
        if form.is_valid():
            good_in_form = form.cleaned_data.get("product")
            good_in_receipt = Receipt_list.objects.filter(product=good_in_form) & Receipt_list.objects.filter(number_receipt=number_doc)             
            if good_in_receipt:#при добавлении товара который уже есть в документе, обновится колво в товаре
                good_in_receipt[0].quantity = good_in_buffer.quantity
                good_in_receipt[0].save()
            else:
                good = form.save(commit=False)
                good.number_receipt = number_doc
                good.quantity = good_in_buffer.quantity
                good.user = request.user
                good.save()            
            good_in_buffer.delete()
            return redirect('receipt_document_open', number_doc)
    else:        
        form = Receipt_add_goods_form_if_not_in_base()

    context = {'form': form, "number_good": number_good}

    return render(request, "shop/receipt_goods_add_if_not_in_base.html", context=context)