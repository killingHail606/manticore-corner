from django.urls import path

from . import views

app_name = 'authorization'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('user_page/', views.UserPageView.as_view(), name='user_page'),
]
