from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

from django.contrib.auth.decorators import login_required

from django.contrib.auth.tokens import default_token_generator as token_generator

# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import logout, login, get_user_model, authenticate
# from django.contrib import auth
from django.contrib.auth.models import User
from .forms import *
from .utils import send_email_verify, get_user, send_email_restore_password




#класс для авторизации из джанго
# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'regusers/login.html'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Авторизация"
#         # c_def = self.get_user_context(title="Авторизация")
#         # return dict(list(context.items()) + list(c_def.items()))
#         return context

#     def get_success_url(self):
#         return reverse_lazy('start')

# @login_required
# def logout_user(request):#функция для выхода, чтобы выйти из аккаунта
#     auth.logout(request)#эта функция вызывает стандартную функцию джанго для выхода пользователя.
#     return redirect('login')


# #регистрация через класс без верификации почты, класс из джанго
# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'regusers/register.html'
#     success_url = reverse_lazy('login')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context['title'] = "Регистрация"
#         return context

#регистрация через класс c верификацией почты, не доделал, не работает. Решил через функцию. 
# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'showcase/register.html'
#     success_url = reverse_lazy('login')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Регистрация"
#         return context


#     def form_valid(self, form):
#         user = form.save()
#         user.is_active = False
#         message =
#         send_mail('код подтверждения', message, settings.EMAIL_HOST_USER, ['test@mail.ru'], fail_silently=False)
#         
#         # login(self.request, user)
#         return redirect('login')







#_________________________________________________________НИЖЕ ИДЕТ РЕГИСТРАЦИЯ/АВТОРИЗАЦИЯ ЧЕРЕЗ ФУНКЦИИ БЕЗ КЛАССОВ ДЖАНГО__________________________________




#авторизация через функцию
def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(data=request.POST)#передали какие-то данные из пост запроса. request.POST это словарь, из него можно по ключам брать данные и что-то с ними делать.
        if form.is_valid():#проверяем валидка ли форма. Для проверки используем встроенную функцию для форм в джанго. Там все проверки прописаны уже. 
            username = request.POST['username']
            password = request.POST['password']#взяли из пост запроса юзера и пароль
            user = authenticate(username=username, password=password)#аутенитифировали пользователя с данными из пост запроса, это нужно для проверки. Далее проверим пользователя. user это объект класса User, у которого есть поля из таблицы user, и есть тут поле is_active

            if user:#если пользователья есть в базе его авторизуем

                login(request, user)
                return HttpResponseRedirect(reverse_lazy('start'))

    else:
        form = LoginUserForm()#когда пользователь только входит на страницу, то срабатывает этот код, так как изначально срабатывает get запрос. Далее в контекст заносится форма, и передается через render функцию в html-ку. Кстати код в html form.as_p означает вывести всю форму через теги p параграфы просто подряд. Можно выводить через другие теги. 
    
    context = {'form': form}
    return render(request, 'regusers/login.html', context=context)




#регистрация через функцию с верификацией почты, ниже будет несколько функций представления. Разобраться с https потом. Этот параметр есть в функции send_email_verify
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)#это словарь, в него можно данные записывать какие нам нужно после проверки валидации
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()    


            send_email_verify(request, user)#функция для отправки письма пользователю для активации пользователя. В ней есть еще параметр use_https, по умолчанию он False

            return HttpResponseRedirect(reverse_lazy('regusers:confirm_email'))#редирект на страницу с текстом чтобы перешли по ссылке и активировали почту

    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'regusers/register.html', context=context)    



def confirm_email(request):
    t = "Перейдите в вашу почту и перейдите по ссылке из письма для подтверждения адреса почты"

    return render(request, 'regusers/check_email.html', {"t": t})
    


#функция для активации пользователя. Передаем в нее зашифрованный uidb64 и token. При удачной проверке, логинится пользователь. Если что-то не так, то redirect на некорректная ссылка 
def activate_user(request, uidb64, token):
    user = get_user(uidb64)

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('start')

    return redirect('regusers:invalid_verify')



def invalid_verify(request):
    return redirect('regusers:invalid_verify')


#фукнция для кнопки забыли пароль
def forgot_password(request):
    if request.method == "POST":
        form = Forgot_passwordForm(data=request.POST)#передали какие-то данные из пост запроса. request.POST это словарь, из него можно по ключам брать данные и что-то с ними делать.
        if form.is_valid():#проверяем валидка ли форма. Для проверки используем встроенную функцию для форм в джанго. Там все проверки прописаны уже. 
            # email = form.save()
            # user = User.objects.filter(email=email.email)
            user = list(form.get_users(request.POST['email']))[0]
            print(user.email)

            send_email_restore_password(request, user)
            # if user:#если пользователья есть в базе его авторизуем

            #     login(request, user)
            return HttpResponseRedirect(reverse_lazy('regusers:go_to_restore_password'))

    else:
        form = Forgot_passwordForm()#когда пользователь только входит на страницу, то срабатывает этот код, так как изначально срабатывает get запрос. Далее в контекст заносится форма, и передается через render функцию в html-ку. Кстати код в html form.as_p означает вывести всю форму через теги p параграфы просто подряд. Можно выводить через другие теги. 
    
    context = {'form': form}
    return render(request, 'regusers/forgot_password.html', context=context)
    

def restore_password(request, uidb64, token):
    
    user = get_user(uidb64)

    if user is not None and token_generator.check_token(user, token):

        if request.method == "POST":
                    # , user=user
            form = Restore_passwordForm(data=request.POST, user=user)
            if form.is_valid():
                form.save()
                
                return HttpResponseRedirect(reverse_lazy('regusers:login'))
        else:
            form = Restore_passwordForm(user=user)

        context = {'form': form}
        return render(request, 'regusers/new_password.html', context=context)

    else:
        return redirect('regusers:invalid_verify')

    





def go_to_restore_password(request):
    s = "На вашу почту выслали письмо для восстановления пароля. Перейдите в вашу почту для восстановления пароля"

    return render(request, 'regusers/go_to_restore_password.html', {"s": s})



# class Activate_user(View):

#     def get(self, request, uidb64, token):
#         user = self.get_user(uidb64)

#         if user is not None and token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             login(request, user)
#             return redirect('start')
#         return redirect('regusers:invalid_verify')

#     @staticmethod
#     def get_user(uidb64):
#         try:
#             # urlsafe_base64_decode() decodes to bytestring
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError,
#                 User.DoesNotExist, ValidationError):
#             user = None
#         return user

# def register_user(request):
    
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             # save form in the memory not in database
#             user = form.save()
#             user.is_active = False
#             user.save()
#             # to get the domain of the current site
#             # current_site = get_current_site(request)
#             # mail_subject = 'Activation link has been sent to your email id / Ссылка активации была отправлена на ваш адрес электронной почты'
#             # message = render_to_string('showcase/acc_active_email.html', {
#             #     'user': user,
#             #     'domain': current_site.domain,
#             #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             #     'token': token_generator.make_token(user),
#             # })
#             message = token_generator.make_token(user)
#             send_mail('код подтверждения', message,
#                           settings.EMAIL_HOST_USER,
#                           ['test@mail.ru'],
#                           fail_silently=False)


#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return render(request, 'registration/register.html', {'form': form})
#     else:
#             form = RegisterUserForm()
#     return render(request, 'showcase/register.html', {'form': form, 'title': "Регистрация"})







# https: // docs.djangoproject.com / en / 4.2 / topics / email /  это ссылка на документацию по функции по отправке писем в джанго. Нужно дописать отправку письма со ссылкой зашифрованной, сделать дешифровку при активации. Или просто код отправлять и чтобы пользователь ввел код из письма для активации. Когда пользователь нективаен, то параметр is_active у него фолз, и мы его изначально таким делаем при реге. А когда он перейдет по ссылке, то он становится тру.


@login_required
def logout_user(request):#функция для выхода, чтобы выйти из аккаунта
    logout(request)#эта функция вызывает стандартную функцию джанго для выхода пользователя.
    return redirect('regusers:login')



