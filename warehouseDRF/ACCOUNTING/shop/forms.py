from django import forms
from django.core.exceptions import ValidationError

from .models import *

from datetime import datetime, date

class Goods_add_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Goods
        fields = ['name_product', 'vendor_code', 'price', 'photo', 'stock', 'group',]


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

#форма для даты при формировании отчета по продажам
class Date_report_income(forms.Form):    
    
    date_from = forms.DateTimeField()
    date_by = forms.DateTimeField()
    


class Receipt_edit_goods_form(forms.Form):
    
    quantity = forms.FloatField()


#для инвентаризации
class Inventory_number_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Inventory_number
        fields = ['comment',]


class Inventory_group_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Inventory_group
        fields = ['group',]


class Inventiry_open_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Inventory_list
        fields = ['quantity_new',]
    #уточнить модел.форм нужна или обычная или вообще джанго форма не нужна