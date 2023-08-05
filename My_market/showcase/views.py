from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .models import *
# Create your views here.



def all_group(request):
    data = Group.objects.all()
    # print(data)
    return render(request, "showcase/start.html", {"data": data})


#сделать чтобы при переходе по урл выходила список товаров, урл должна тенуться по группе

def show_group(request, group_slug): 
    groups = Group.objects.filter(slug=group_slug)
    goods = Goods.objects.filter(group_id=groups[0].id)
    print(groups)
    data = {
    'goods': goods,
    'groups': groups,
    'title': 'Товары',
    'gr_selected': groups[0].id,

    }
    # if len(goods) == 0:
    #     raise Http404()


    return render(request, "showcase/good.html", context=data)

    # return render(request, 'showcase/good.html', context=context)

# def show_product(request, product):
#     return HttpResponse(f"<h1>Вася {product}</h1>")




def basket(request):
    return render(request, "showcase/basket.html")
