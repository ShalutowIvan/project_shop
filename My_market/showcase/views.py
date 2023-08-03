from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .models import *
# Create your views here.



def index(request):
    data = Group.objects.all()
    print(data)
    return render(request, "showcase/start.html", {"data": data})

def basket(request):
    return render(request, "showcase/basket.html")
