from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import auth_logout

from . import views

app_name = 'authorization'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('user_page/', views.UserPageView.as_view(), name='user_page'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', auth_logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]