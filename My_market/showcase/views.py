from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .models import *
from .forms import *



def start(request):
    # gr = Group.objects.all()
    org = Organization.objects.all()
    gd = Goods.objects.all()

    form = AddGoodForm()

    # tovar = Goods.objects.filter(name_product=name_product)
    # t_basket = Goods_in_basket.objects.create(name_product=tovar.name_product, price=tovar.price, quantity=1, group=tovar.group)
    # g_basket.save()
    # print(tovar.name_product)
    

    dat = {
    # "gr": gr,
    "org": org[0],
    "gd": gd,
    "form": form,
    }


    return render(request, "showcase/start.html", context=dat)






def show_group(request, group_slug): 
    groups = Group.objects.filter(slug=group_slug)
    goods = Goods.objects.filter(group_id=groups[0].id)
    # gr = Group.objects.all()
    # print(groups)
    data = {
    'goods': goods,    
    # 'gr': gr,
    'title': 'Товары',
    }
   

    return render(request, "showcase/good.html", context=data)

   

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
    return render(request, "showcase/basket.html")

#разобраться с добавлением товара в корзину
