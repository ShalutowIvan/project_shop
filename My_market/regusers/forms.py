from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import *




class RegisterUserForm(UserCreationForm):#делаем класс для формы на базе UserCreationForm, его также нужно импортировать.
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите вашу почту'}))



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
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))
# placeholder - это надпись в строке ввода
    class Meta:
        model = User#взяли пользователя из джанго. К нему можно и дополнительные поля приделать через класс модели. То есть в файле models можно прописать класс и сделать класс из джанго как родитель и дописать к нему доп поля
        fields = ('username', 'password')


class Forgot_passwordForm(PasswordResetForm):    
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите вашу почту'}))

    class Meta:
        model = User
        fields = ('email', )




class Restore_passwordForm(SetPasswordForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('password1', 'password2')

    