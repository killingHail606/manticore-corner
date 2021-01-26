from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BooksView.as_view(), name='books'),
    path('<slug:slug>/', views.BooksSectionView.as_view(), name='books_section'),
    path('<slug:slug_section>/<slug:slug_genre>', views.BooksGenreView.as_view(), name='books_genre'),
    path('<slug:slug>', views.BookDetailView.as_view(), name='book_detail'),
]
