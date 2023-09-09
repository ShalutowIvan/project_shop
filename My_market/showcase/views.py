from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.contrib.auth.decorators import login_required#это чтобы в случае когда пользователь не авторизован контроллер не срабатывал


from django.core.paginator import Paginator

from django.contrib.auth import logout, login
from django.contrib.auth.models import User

from .models import *
from .forms import *
from .utils import *


class GoodsHome(ListView):
    paginate_by = 1
    model = Goods
    template_name = 'showcase/start.html'
    context_object_name = 'gd'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Organization.objects.all()
        if org:
            context['org'] = org[0]
        context['form'] = AddGoodForm()

        
        return context



class GroupShow(ListView):
    paginate_by = 1
    model = Goods
    template_name = 'showcase/good.html'
    context_object_name = 'goods'
    allow_empty = False

    def get_queryset(self):
        return Goods.objects.filter(group__slug=self.kwargs['group_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Группа - ' + str(context['goods'][0].group)
        org = Organization.objects.all()
        context['org'] = org[0]
        context['form'] = AddGoodForm()

        return context


# {% if request.user.is_authenticated %}
# {% endif %}

#контроллер для кнопки добавления товара в корзину
@login_required#декторатор который перекидывает на страницу авторизации при срабатывании текущей функции. Страница авторизации должна быть прописана в файле settings.py в переменной LOGIN_URL. Декоратор под нее настроен.
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

# <p> Количество: {{ i.quantity }}</p>

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



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'showcase/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = "Регистрация"
        return context



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'showcase/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        # c_def = self.get_user_context(title="Авторизация")
        # return dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('start')

@login_required
def logout_user(request):#функция для выхода, чтобы выйти из аккаунта
    logout(request)#эта функция вызывает стандартную функцию джанго для выхода пользователя.
    return redirect('login')


def adminka(request):
    return redirect('adminka')



class Checkout(CreateView):
    form_class = Order_form
    template_name = 'showcase/checkout.html'
    success_url = reverse_lazy('start')
    login_url = reverse_lazy('start')
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pay_goods = Baskets.objects.filter(user=self.request.user)
        # pay = pay_goods
        
        print(context)
        print()
        # print(dict(list(pay_goods)))
        # dict(list(context)+list(pay_goods))
        # context = (list(context.items()) + list(pay_goods))
        context['pay_goods'] = pay_goods
        return context

# возможно сделать кнопку подтвердить это будут занесены в БД данные формы. потом кнопка оформить заказ, это для занесения данных из формы и из корзины в таблицу заказы

# def check_out(request):
    
#     return 

# доделать checkout. Тут скорее всего во вьюшке чекаут должна заполняться таблица модели Order_list_bought с вводом полей для заказа, и остальные поля тянутся из таблицы корзина и таблица корзина должна очиститься после заказа и заказ нужно будет на отдельной вкладке отобразить с данными. 





def view_checkout(request):
    pay_goods = Baskets.objects.filter(user=request.user)

    return render(request, "showcase/checkout_list.html", {'pay_goods': pay_goods})


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

