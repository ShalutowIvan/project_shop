from django import forms
from django.core.exceptions import ValidationError

from .models import *


class Goods_add_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Goods
        fields = ['name_product', 'slug', 'vendor_code', 'price', 'photo', 'stock', 'group', ]


class Group_add_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Group
        fields = ['name_group', 'slug']
 


#для приходного документа
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


#для расходного документа
class Expense_number_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Expense_number
        fields = ['comment',]


class Expense_add_goods_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Expense_list
        fields = ['product', 'quantity', ]


