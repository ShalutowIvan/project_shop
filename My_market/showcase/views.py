from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .models import *




def start(request):
    # gr = Group.objects.all()
    org = Organization.objects.all()
    gd = Goods.objects.all()

    dat = {
    # "gr": gr,
    "org": org[0],
    "gd": gd,
    }

    # print(data)
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

   

# def show_product(request, product):
#     return HttpResponse(f"<h1>Вася {product}</h1>")




def basket(request):
    return render(request, "showcase/basket.html")

#разобраться с добавлением товара в корзину
