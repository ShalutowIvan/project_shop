"""
URL configuration for ACCOUNTING project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop.views import *
from rest_framework import routers

# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# router.register(r'good', GoodsViewSet, basename="tovar")
router.register(r'good', GoodsViewSet)
print(router.urls)#коллекция урл



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/goodlist/', GoodsAPIList.as_view()),
    # path('api/v1/goodlist/<int:pk>/', GoodsAPIUpdate.as_view()),
    # path('api/v1/gooddetail/<int:pk>/', GoodsAPIDetail.as_view()),
    # path('api/v1/goodlist/', GoodsViewSet.as_view({'get': 'list'})),
    # path('api/v1/goodlist/<int:pk>/', GoodsViewSet.as_view({'put': 'update'})),
    path('api/v1/', include(router.urls)), #http://127.0.0.1:8000/api/v1/good/# то есть в конце урл дописывается строка (префикс) из роутера, то есть api/v1/ + good. urls - это набор маршрутов (коллекция) из вью сета. 
]
