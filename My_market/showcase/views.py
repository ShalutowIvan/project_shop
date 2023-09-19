from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy


from django.views.generic import ListView, DetailView, CreateView

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.contrib.auth.models import User


from .models import *
from .forms import *
from .utils import *


class GoodsHome(ListView):
    paginate_by = 1
    model = Goods
    template_name = 'showcase/start.html'
    context_object_name = 'gd'


    def get_queryset(self):#этот get_queryset для поиска товаров, товар ищется по названию всегда во всем каталоге, даже если зайти в группу то поиск будет также по всему каталогу. Потом доделать
        return Goods.objects.filter(name_product__icontains=self.request.GET.get('q', ''))
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Organization.objects.all()
        if org:
            context['org'] = org[0]
        context['form'] = AddGoodForm()

        
        return context



class GroupShow(ListView):
    paginate_by = 10
    model = Goods
    template_name = 'showcase/good.html'
    context_object_name = 'goods'
    allow_empty = True

    def get_queryset(self):
        # q_set = Goods.objects.filter(group__slug=self.kwargs['group_slug'])
        # if q_set == []:
        #     return ["Пусто"]
        # else:
        return Goods.objects.filter(group__slug=self.kwargs['group_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if len(context['goods']) == 0:
            context['title'] = 'Группа - ' + "Пусто"
        else:
            context['title'] = 'Группа - ' + str(context['goods'][0].group)
        


        org = Organization.objects.all()
        if org:
            context['org'] = org[0]
        context['form'] = AddGoodForm()

        return context




#контроллер для кнопки добавления товара в корзину
@login_required
def add_in_basket(request, product_id):
    product = Goods.objects.get(id=product_id)#тут мы получили объект товара по его id
    baskets = Baskets.objects.filter(user=request.user, product=product)#делаем переменную с фильтром из корзины по пользователю и по ID продукта. В модели корзины есть параметр product мы его сравниваем с переменной product, которую указали выше, то есть фильтр он сравнивает и филтрует по тем полям которые мы прописали. Далее будет добавлять элементы в корзину. Тут возвращается только один товар. Для каждого товара тут будет создаваться отдельный объект

    if not baskets.exists():#если корзина с определенным товаром пустая, то добавляем продукт. Если есть уже такой товар, то к нему добавляет колво 1
        Baskets.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        #добавили элемент и сохранили в дб корзины. Теперь нужно чтобы мы оставались на той же страницы где и вызвали текущий контроллер. 
    return HttpResponseRedirect(request.META['HTTP_REFERER'])#это перенаправление на ту же страницу где мы и были. ТО есть получается нажали добавить в корзину и там же и остались, и корзина пополнилась.


@login_required
def basket_view(request):
    basket = Baskets.objects.filter(user=request.user)#фильтрация по юзеру тут идет. То есть для каждого пользователя будет своя корзина
    # total_sum = sum(i.sum() for i in basket )
    # total_quantity = sum(i.quantity for i in basket)
    #логику всю лучше прописывать в классах модели, а не в контроллерах. Сделаем это.
    # total_sum = 0
    # total_quantity = 0
    # for i in basket:
    #     total_sum += i.sum()
    #     total_quantity += i.quantity
    # 'total_sum': total_sum, 'total_quantity': total_quantity 
    # context = {'basket': basket }


    return render(request, "showcase/basket.html", {'basket': basket})


@login_required
def clear_basket(request, basket_id):
    # Baskets.objects.all().delete()
    del_basket = Baskets.objects.get(id=basket_id)
    del_basket.delete()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def adminka(request):
    return redirect('adminka')



class Get_contacts(CreateView):
    form_class = Contacts_form
    template_name = 'showcase/contacts.html'
    success_url = reverse_lazy('checkout')
    login_url = reverse_lazy('start')    


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # pay_goods = Baskets.objects.filter(user=self.request.user)
        # pay = pay_goods
        # self.form_class.user = self.request.user    
        # print(context)
        # print()
        # # print(dict(list(pay_goods)))
        # dict(list(context)+list(pay_goods))
        # context = (list(context.items()) + list(pay_goods))
        # context['pay_goods'] = pay_goods
        return context
    
    #передача юзера в форму автоматом от залогининного пользователя. В самой форме юзер не заполняется
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # возвращаем form_valid предка
        return super().form_valid(form)





#функция занесения данных в таблицу заказов
def checkout(request):
    pay_goods = Baskets.objects.filter(user=request.user)
    id_contact = Contacts.objects.all().last().id

    for i in pay_goods:
        Order_list_bought.objects.create(user=i.user, name_product=i.product, quantity=i.quantity, order_number=id_contact)
    pay_goods.delete()

    return redirect('start')



def checkout_list(request):
    order_list = Order_list_bought.objects.filter(user=request.user)

    contact = list(Contacts.objects.filter(user=request.user))
    contact = [i.id for i in contact]

    itog = {
        'order_list': order_list,
        'contact': contact,
    }
    #
    # itog = {  }

    return render(request, "showcase/checkout_list.html", context=itog)




# def checkout_view(request):
#     order = Baskets.objects.filter(user=request.user)
#     contact = list(Contacts.objects.all())[-1]
#     # final_order = Order_list_bought.objects.all()
#
#     context = {
#     'contact': contact,
#     'order': order,
#     # 'final_order': final_order,
#     }
#
#     return render(request, "showcase/checkout.html", context=context)




# def add_in_basket(request, product_id):
#     product = Goods.objects.get(id=product_id)#тут мы получили объект товара по его id
#     baskets = Baskets.objects.filter(user=request.user, product=product)#делаем переменную с фильтром из корзины по пользователю и по ID продукта. В модели корзины есть параметр product мы его сравниваем с переменной product, которую указали выше, то есть фильтр он сравнивает и филтрует по тем полям которые мы прописали. Далее будет добавлять элементы в корзину. Тут возвращается только один товар. Для каждого товара тут будет создаваться отдельный объект

#     if not baskets.exists():#если корзина с определенным товаром пустая, то добавляем продукт. Если есть уже такой товар, то к нему добавляет колво 1
#         Baskets.objects.create(user=request.user, product=product, quantity=1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#         #добавили элемент и сохранили в дб корзины. Теперь нужно чтобы мы оставались на той же страницы где и вызвали текущий контроллер. 
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])






