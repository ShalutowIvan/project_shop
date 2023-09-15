from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddGoodForm(forms.ModelForm):
    # quantity = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class': 'form-input'}))
    # availability = forms.BooleanField(initial=True)


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cat'].empty_label = "Категория не выбрана"
        



    #     tovar = Goods.objects.filter(name_product=name_product)
    #     t_basket = Goods_in_basket.objects.create(name_product=tovar.name_product, price=tovar.price, quantity=1, group=tovar.group)

    #нужно через сессии делать. по другому будет все криво



    class Meta:
        model = Baskets
        fields = ['quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'form-input'}),
            # 'quantity': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 200:
    #         raise ValidationError('Длина превышает 200 символов')

    #     return title



class Contacts_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contacts
        fields = ['fio', 'phone', 'delivery_address', 'pay']


    def clean_title(self):
        fio = self.cleaned_data['fio']
        if len(fio) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return fio




