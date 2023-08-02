from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.

def index(request):
    dat = {'группа 1': 'товар 1', 'группа 1': 'товар 2', 'группа 1': 'товар 3', 'группа 1': 'товар 4'}
    # data = [1, 2, 3, 4]
    return render(request, "showcase/home.html", {"data": dat})

def basket(request):
    return render(request, "showcase/basket.html")
