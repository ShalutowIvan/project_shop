from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User


#функция для отправки письма со ссылкой для активации пользователя
def send_email_verify(request, user, use_https=False):

    current_site = get_current_site(request)
    context = {
    'user': user,
    'domain': current_site.domain,
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "token": token_generator.make_token(user),
    'protocol': 'https' if use_https else 'http',    
    }

    html_body = render_to_string('regusers/user_active.html', context=context,)
    msg = EmailMultiAlternatives(subject='Активация', to=[user.email,],)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    

#функция для дешифрования зашифрованного id юзера, который регался при заполнении формы на регистрацию. Возращается сам объет то есть строка из базы того юзера, который регался, поиск идет по его id.
def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


#функция для отправки письма при сбросе пароля
def send_email_restore_password(request, user, use_https=False):
    current_site = get_current_site(request)

    context = {
    'user': user,
    'domain': current_site.domain,
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "token": token_generator.make_token(user),
    'protocol': 'https' if use_https else 'http',
    }

    html_body = render_to_string('regusers/restore_password.html', context=context,)
    msg = EmailMultiAlternatives(subject='Восстановление пароля', to=[user.email,],)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    


