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
	path('activate_user/<uidb64>/<token>/', Activate_user.as_view(), name='activate_user'),
	
	path('invalid_verify/', invalid_verify, name='invalid_verify'),

]

