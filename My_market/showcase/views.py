from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.

def index(request):
    return render(request, "showcase/home.html")

def basket(request):
    return render(request, "showcase/basket.html")
