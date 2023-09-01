from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.contrib.auth import logout, login
from django.contrib.auth.models import User

from .models import *
from .forms import *
from .utils import *


# def start(request):
#     # gr = Group.objects.all()
#     org = Organization.objects.all()
#     gd = Goods.objects.all()

#     form = AddGoodForm()

#     # tovar = Goods.objects.filter(name_product=name_product)
#     # t_basket = Goods_in_basket.objects.create(name_product=tovar.name_product, price=tovar.price, quantity=1, group=tovar.group)
#     # g_basket.save()
#     # print(tovar.name_product)
    

#     dat = {
#     # "gr": gr,
#     "org": org[0],
#     "gd": gd,
#     "form": form,
#     }


#     return render(request, "showcase/start.html", context=dat)


class GoodsHome(ListView):
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



# def show_group(request, group_slug): 
#     groups = Group.objects.filter(slug=group_slug)
#     goods = Goods.objects.filter(group_id=groups[0].id)
#     # gr = Group.objects.all()
#     # print(groups)
#     data = {
#     'goods': goods,    
#     # 'gr': gr,
#     'title': 'Товары',
#     }
   

#     return render(request, "showcase/good.html", context=data)


class GroupShow(ListView):
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





#контроллер для кнопки добавления товара в корзину
def add_in_basket(request, product_id):
    product = Goods.objects.get(id=product_id)#тут мы получили объект товара по его id
    baskets = Baskets.objects.filter(user=request.user, product=product)#делаем переменную с фильтром из корзины по пользователю и по ID продукта. В модели корзины есть параметр product мы его сравниваем с переменной product, которую указали выше, то есть фильтр он сравнивает и филтрует по тем полям которые мы прописали. Далее будет добавлять элементы в корзину. Тут возвращается только один товар.

    if not baskets.exists():#если корзина пустая, то добавляем продукт
        Baskets.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        #добавили элемент и сохранили в дб корзины. Теперь нужно чтобы мы оставались на той же страницы где и вызвали текущий контроллер. 
    return HttpResponseRedirect(request.META['HTTP_REFERER'])#это перенаправление на ту же страницу где мы и были. ТО есть получается нажали добавить в корзину и там же и остались, и корзина пополнилась.


def clear_basket(request):
    Baskets.objects.all().delete()
    # Baskets.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




    # < form
    # action = "{% url 'start' %}"
    # method = "post" >
    # { % csrf_token %}
    # < div
    #
    # class ="form-group" >
    #
    # < p > < label
    #
    # class ="form-label" for ="{{ form.quantity.id_for_label }}" > {{form.quantity.label}}: <
    #
    #     / label > {{form.quantity}} < / p >



    # if request.method == 'POST':
    #     form = AddPostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         #print(form.cleaned_data)
    #         form.save()
    #         return redirect('home')
    # else:
    #     form = AddPostForm()

#сделать через форму в каждом товаре
    # tovar = Goods.objects.filter(name_product=name_product)
    # t_basket = Goods_in_basket.objects.create(name_product=tovar.name_product, price=tovar.price, quantity=1, group=tovar.group)
    # # g_basket.save()
    # print(tovar.name_product)
    # return render(request, "showcase/start.html", {"tovar": tovar, 't_basket': t_basket})

# сделать контроллер обработчик событий для добавления в корзину для кнопки. То есть будет возвращаться в функции определенное действие. Импортируем модель юзера


# {% url 'add_in_basket' %}
# <form action="{% url 'add_in_basket' %}" method="post">
# {% csrf_token %}
# </form>

# def show_product(request, product):
#     return HttpResponse(f"<h1>Вася {product}</h1>")




def basket(request):
    context = Baskets.objects.all()
    # print(context)
    return render(request, "showcase/basket.html", {'product_in_basket': context})

#разобраться с добавлением товара в корзину



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'showcase/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title="Регистрация")
        # return dict(list(context.items()) + list(c_def.items()))
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

def logout_user(request):#функция для выхода, чтобы выйти из аккаунта
    logout(request)#эта функция вызывает стандартную функцию джанго для выхода пользователя.
    return redirect('login')

# {% url 'showcase:add_in_basket' j.id %}
#начал пилить корзину. Добавил приложение корзины.
# ссылка на видяху с корзиной, ост 20 мин:
# https://www.youtube.com/watch?v=XjkP2dSPv7g&t=352s&ab_channel=EngineerSpock-IT%26%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5



def adminka(request):
    return redirect('adminka')






