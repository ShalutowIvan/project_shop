from django import forms
from django.core.exceptions import ValidationError

from .models import *


class Goods_add_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Goods
        fields = ['name_product', 'slug', 'vendor_code', 'price', 'photo', 'stock', 'group', ]


    # def clean_title(self):
    #     fio = self.cleaned_data['fio']
    #     if len(fio) > 200:
    #         raise ValidationError('Длина превышает 200 символов')

    #     return fio


# class Receipt_document_form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     class Meta:
#         model = Receipt_list
#         fields = ['product', 'quantity', ]


class Receipt_number_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Receipt_number
        fields = ['comment',]


class Receipt_add_goods_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Receipt_list
        fields = ['product', 'quantity', ]
