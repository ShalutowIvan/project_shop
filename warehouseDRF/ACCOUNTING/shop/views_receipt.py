from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import pandas as pd
import string
import random
from transliterate import translit
from django.core.exceptions import ObjectDoesNotExist


#список накладных просто вывод
@login_required
def receipt_list(request):
    rec_list = Receipt_number.objects.all()

    context = {"receipt_list_view": rec_list}

    org = Organization.objects.all()
    if org:
        context['org'] = org[0]

    return render(request, "shop/receipt_list.html", context=context)



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
            for i in file_receipt.values:
                try:
                    receipts.append(
                        Receipt_list(
                            product=Goods.objects.get(name_product=i[0]),
                            number_receipt=number_doc,
                            quantity=i[1],
                            user=request.user
                        ))
                except ObjectDoesNotExist:
                    buffer_goods.append(Buffer_receipt(
                        product=i[0],
                        number_receipt=number_doc,
                        quantity=i[1],
                        user=request.user
                    ))

            if receipts != []:
                receipts_create = Receipt_list.objects.bulk_create(receipts)
            if buffer_goods != []:
                buffer_create = Buffer_receipt.objects.bulk_create(buffer_goods)

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


# заменить если нет в бд
def receipt_change_if_not_in_base(request, number_good):
    good_in_buffer = Buffer_receipt.objects.get(id=number_good)
    number_doc = good_in_buffer.number_receipt
    # if request.method == 'POST':
    #     form = Receipt_add_goods_form(data=request.POST)
    #     if form.is_valid():
    #         good = form.save(commit=False)
    #         good.number_receipt = number_doc
    #         good.user = request.user
    #         good.save()
    #         # good_in_buffer.delete()#не удаляется товар - потому что используется другой пост запрос. фотка товара не удаляется если она не существует, переделать
    #
    #         return redirect('receipt_document_open', number_doc)

    # else:
    #тут пост запрос идет через другую УРЛ - receipt_add_goods
    form = Receipt_add_goods_form()
    good_in_buffer.delete()
    context = {'form': form, "number_doc": number_doc}

    return render(request, "shop/receipt_goods_add.html", context=context)