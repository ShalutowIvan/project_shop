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

def send_email_for_verify(request, user, use_https=False):
    
    current_site = get_current_site(request)
    context = {
    'user': user,
    'domain': current_site.domain,
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "token": token_generator.make_token(user),
    'protocol': 'https' if use_https else 'http',
    
    }

    message = render_to_string('showcase/check_email.html', context=context,)
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email],
        )
    email.send()
    




