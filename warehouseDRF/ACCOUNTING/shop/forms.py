from django import forms
from django.core.exceptions import ValidationError

from .models import *

from datetime import datetime, date

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

#форма для даты при формировании отчета по продажам
class Date_report_income(forms.Form):    
    
    date_from = forms.DateTimeField()
    date_by = forms.DateTimeField()
    


class Receipt_edit_goods_form(forms.Form):
    
    quantity = forms.FloatField()

#для редактирования товара
class Goods_modify(forms.Form):
    # name_product = forms.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, default="_", unique=True, db_index=True, verbose_name="URL")
    # vendor_code = forms.CharField(max_length=255)
    # price = forms.DecimalField(max_digits=19, decimal_places=2)
    photo = forms.ImageField()
    # upload_to="photos/%Y/%m/%d/"
    # stock = models.FloatField(default=0, verbose_name="Остаток")
    # availability = models.BooleanField(default=True, verbose_name="Доступность")#если товар не доступен, он должен исчезнуть на витрине
    # group = forms.ModelChoiceField(queryset=Group.objects.all())#выбор группы
    




