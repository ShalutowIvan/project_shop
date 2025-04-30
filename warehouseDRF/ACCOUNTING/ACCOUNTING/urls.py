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
from django.urls import path, include, re_path
from shop.views import *
from regusers.views import *
from shop.views_goods_api import *
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
#для jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter




# router = routers.SimpleRouter()
# router.register(r'goods', GoodsViewSet)
# router = DefaultRouter()
# router.register(r'api/app_goods', ProductViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('shop.urls')),#тут указали стартовую страницу от которой будут идти все другие ссылки приложения
    path('', include('regusers.urls')),
    # path('api/v1/', include(router.urls)),
    # path('', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)