from django.urls import path, re_path
from regusers.views import *

app_name = 'regusers'


urlpatterns = [
	# path('login/', LoginUser.as_view(), name='log_in'),
	# path('register/', RegisterUser.as_view(), name='register'),
	
	#урл регистрации с подтвержлением почты
	path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),

    path('logout/', logout_user, name='logout'),
    

	path('confirm_email/', confirm_email, name='confirm_email'),
	path('activate_user/<uidb64>/<token>/', activate_user, name='activate_user'),#тут должна быть функция, а не класс. Тут формируется урл с параметрами, мы их в шаблоне пишем при указании самой урл и потом далее параметры просто через пробел. Первый параметр <uidb64> (он кодируется через функцию кодировщик из джанго), второй параметр <token> (генерируется генератором токена из джанго). 
	
	path('invalid_verify/', invalid_verify, name='invalid_verify'),

	path('forgot_password/', forgot_password, name='forgot_password'),

	path('go_to_restore_password/', go_to_restore_password, name='go_to_restore_password'),

	path('restore_password_url/<uidb64>/<token>/', restore_password_url, name='restore_password_url'),
	path('restore_password_form/', restore_password_form, name='restore_password_form'),

]

