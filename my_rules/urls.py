from django.urls import path

from . import views


app_name = 'my_rules'

urlpatterns = [
    path('', views.MyRulesView.as_view(), name='my_rules')
]
