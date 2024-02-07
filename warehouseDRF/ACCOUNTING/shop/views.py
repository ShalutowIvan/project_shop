from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, viewsets, mixins
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from django.forms import model_to_dict

from .forms import *





# def test_view(request):
#     if request.method == "POST":
#         form = Url_form(data=request.POST)#передали какие-то данные из пост запроса. request.POST это словарь, из него можно по ключам брать данные и что-то с ними делать.
#         if form.is_valid():#проверяем валидка ли форма. Для проверки используем встроенную функцию для форм в джанго. Там все проверки прописаны уже. 
#             url = request.POST['url']
#             # rq = requests.get(f"{url}")
#             rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")

#             return {"res": rq.text}
# 			# return HttpResponseRedirect(reverse_lazy('start'))

#     else:
#         form = Url_form()#когда пользователь только входит на страницу, то срабатывает этот код, так как изначально срабатывает get запрос. Далее в контекст заносится форма, и передается через render функцию в html-ку. Кстати код в html form.as_p означает вывести всю форму через теги p параграфы просто подряд. Можно выводить через другие теги. 
    
#     context = {'form': form}
#     return render(request, "shop/test.html", context=context)



import requests

def test_view(request):
	rq = requests.get("http://127.0.0.1:8000/checkout_list/orders/all/")
	res = rq.text
	print(res)
	return HttpResponse(res)

#в таком виде сейчас возвращается
# {"51":[["Хлеб",4.0,"2024-02-04T02:55:37.047965",22]],"49":[["Хлеб",1.0,"2024-02-04T01:05:37.596731",22],["Молоко",1.0,"2024-02-04T01:05:37.596731",22]],"50":[["Молоко",5.0,"2024-02-04T01:50:17.124023",22]]}
