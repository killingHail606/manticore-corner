from django.urls import path

from . import views


app_name = 'wall_of_heroes'

urlpatterns = [
    path('', views.WallOfHeroesView.as_view(), name='heroes'),
    path('<slug:slug>', views.HeroDetailView.as_view(), name='hero_detail'),
]