from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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

class RegisterUserForm(UserCreationForm):#делаем класс для формы на базе UserCreationForm, его также нужно импортировать.
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))



    class Meta:
        model = User#пишем модель. Ее также нужно импортировать из джанго
        fields = ('username', 'email', 'password1', 'password2')#указали поля для нашей формы.
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }#виджеты для назначение классов для полей, то есть стили добавлеяем через эти классы. Имена полей можно посмотреть через панель разработчика в браузере через просмотреть код на нужном нам элементе. Там есть input поля и прописаны имена полей. Они также берутся из джанго. Также можно посмотреть и имена полей для других полей, не только username и пароли. Делаем мы так, потому что мы делаем свою форму вместо стандартной. В другом фреймворке наверно можно и свои поля для своей формы указать. Далее перейдем в файл views.py и перепишем наш класс. 
        #стили для стандартных полей почему-то не работают. Поэтому нам придется переопределить эти поля и к ним дописать также виджеты со стилями. Переопределить их нужно до класса Meta. Теперь стили будут работать. Перейдем далее в шаблон и перепишем там шаблон. Добавим еще поле email в нашу форму. Теперь можно регать новых пользователей. Выглядит совсем все стандартно.  


class LoginUserForm(AuthenticationForm):#название сами придумали, базовый класс нужно также импортировать дополинетльно. 
    #ниже мы определели поля для ввода логина и пароля и прописали к ним виджеты для стилей css. 
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))



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




