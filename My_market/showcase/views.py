from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.

def index(request):
    data = {'группа 1': 'товар 1'}

    return render(request, "showcase/home.html", {"data": 1111})

def basket(request):
    return render(request, "showcase/basket.html")
