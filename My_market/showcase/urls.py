from django.urls import path, re_path
from showcase.views import *

urlpatterns = [
	path('', index),
    path('basket/', basket),


]