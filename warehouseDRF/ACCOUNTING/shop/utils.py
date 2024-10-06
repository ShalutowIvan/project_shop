from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import *


class DataMixin:
    def get_user_context(self, **kwargs):
    	pass
        # context = kwargs
        # cats = Category.objects.annotate(Count('women'))

        # user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(1)

        # context['menu'] = user_menu

        # context['cats'] = cats
        # if 'cat_selected' not in context:
        #     context['cat_selected'] = 0
        # return context



def handle_uploaded_file(file_name, path):
    with open(f"{path}{file_name.name}", "wb+") as destination:
        for chunk in file_name.chunks():
            destination.write(chunk)

