from django.db.models import Count

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
