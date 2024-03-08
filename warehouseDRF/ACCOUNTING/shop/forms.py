from django import forms
from django.core.exceptions import ValidationError

from .models import *


class Goods_add_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Goods
        fields = ['name_product', 'slug', 'vendor_code', 'price', 'photo', 'stock', 'group', ]


    def clean_title(self):
        fio = self.cleaned_data['fio']
        if len(fio) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return fio


# class Url_form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     class Meta:
#         model = Url_list
#         fields = ['url', ]


