from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.contrib.auth import logout, login

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






# def add_in_basket(request, name_product):
#     # if request.method == 'POST':
#     #     form = AddPostForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         #print(form.cleaned_data)
#     #         form.save()
#     #         return redirect('home')
#     # else:
#     #     form = AddPostForm()

# #сделать через форму в каждом товаре
#     tovar = Goods.objects.filter(name_product=name_product)
#     t_basket = Goods_in_basket.objects.create(name_product=tovar.name_product, price=tovar.price, quantity=1, group=tovar.group)
#     # g_basket.save()
#     print(tovar.name_product)
#     return render(request, "showcase/start.html", {"tovar": tovar, 't_basket': t_basket})    

# {% url 'add_in_basket' %}
# <form action="{% url 'add_in_basket' %}" method="post">
# {% csrf_token %}
# </form>

# def show_product(request, product):
#     return HttpResponse(f"<h1>Вася {product}</h1>")




def basket(request):
    context = request.session.items()
    print(context)
    return render(request, "showcase/basket.html")

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


#начал пилить корзину. Добавил приложение корзины.
# ссылка на видяху с корзиной, ост 20 мин:
# https://www.youtube.com/watch?v=XjkP2dSPv7g&t=352s&ab_channel=EngineerSpock-IT%26%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5

