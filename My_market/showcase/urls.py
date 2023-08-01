from django.urls import path, re_path
from showcase.views import *

urlpatterns = [
	path('', index, name='start'),
    path('basket/', basket, name='basket'),


]