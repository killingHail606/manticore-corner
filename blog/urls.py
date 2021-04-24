from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_blog'),
    path('articles/', views.Articles.as_view(), name='articles'),
    path('articles/category/<slug:slug>', views.Articles.as_view(), name='articles_categories'),
    path('articles/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('about_blog/', views.AboutBlogView.as_view(), name='about_blog'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('like/', views.post_like, name='post_like'),
    path('comment/', views.post_comment, name='post_comment'),
    path('search/', views.SearchView.as_view(), name='search'),
]
