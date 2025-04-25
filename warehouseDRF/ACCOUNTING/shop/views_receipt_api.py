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



# создание документа - добавить документ с добавлением коммента. После создания документа он сразу открывается - редирект на урл receipt_document_open
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


# приходный документ - открытие
@login_required
def receipt_document_open(request, open_receipt):
    receipt_open = Receipt_number.objects.get(id=int(open_receipt))
    receipt_good_list = Receipt_list.objects.filter(number_receipt=int(open_receipt))
    receipt_buffer = Buffer_receipt.objects.filter(number_receipt=int(open_receipt))
    context = {"number": open_receipt, 'receipt_good_list': receipt_good_list, "receipt_doc": receipt_open,
               "receipt_buffer": receipt_buffer}

    org = Organization.objects.all()

    if org:
        context['org'] = org[0]

    return render(request, "shop/receipt_open.html", context=context)


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


# проведение документа - то функция после которой меняется статус документа и добавляется товар на остаток на основании документа
@login_required
def receipt_document_activate(request, receipt_activate):
    doc = Receipt_number.objects.get(id=receipt_activate)
    if doc.state == False:
        list_goods_to_add = Receipt_list.objects.filter(number_receipt=receipt_activate)
        gen_list = [i.product.id for i in list_goods_to_add]

        list_good = Goods.objects.filter(
            pk__in=gen_list)  # не понятно почему, но тут список объектов получается неизменяемый, у них нельзя записать новые значения. Сделал queryset типом list, и все норм. Теперь значения полей объектов стали меняться.

        list_good = list(list_good)

        for i in range(len(gen_list)):
            list_good[i].stock += list_goods_to_add[i].quantity

        # print(list_good[i].stock)

        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

        doc.state = True
        doc.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# отмена проведения документа
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

        goods = Goods.objects.bulk_update(objs=list_good, fields=["stock", ])

        doc.state = False
        doc.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# приходный документ - удаление, удаляется и таблица с номером документа и товары с этим же номером документа
@login_required
def receipt_document_delete(request, number_delete_receipt):
    rec = Receipt_number.objects.get(id=number_delete_receipt)
    good_list_delete = Receipt_list.objects.filter(number_receipt=number_delete_receipt)

    rec.delete()
    good_list_delete.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# добавление товара - в открытом документе. number_doc берется из номера открытого документа, который мы открыли функцией receipt_document_open он прокидывается в html.
@login_required
def receipt_add_goods(request, number_doc):
    if request.method == 'POST':
        form = Receipt_add_goods_form(data=request.POST)
        if form.is_valid():
            good_in_form = form.cleaned_data.get("product")
            good_in_receipt = Receipt_list.objects.filter(product=good_in_form) & Receipt_list.objects.filter(number_receipt=number_doc)             
            if not good_in_receipt:                
                good = form.save(commit=False)
                good.number_receipt = number_doc
                good.user = request.user
                good.save()

            return redirect('receipt_document_open', number_doc)

    else:
        form = Receipt_add_goods_form()

    context = {'form': form, "number_doc": number_doc}

    return render(request, "shop/receipt_goods_add.html", context=context)


# удаление товара из накладной
@login_required
def receipt_delete_goods(request, number_delete_good):
    list_delete = Receipt_list.objects.get(id=number_delete_good)
    list_delete.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


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