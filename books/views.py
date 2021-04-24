from django.views import View
from django.views.generic.base import TemplateResponseMixin

from .models import BooksSection, BooksGenre, Book
from blog.functions import lexicon, quote, SearchForm


class BooksView(TemplateResponseMixin, View):
    books_sections = BooksSection.objects.all()
    template_name = 'books/books.html'

    def get(self, *args, **kwargs):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        ctx = {'section': 'books',
               'books_sections': self.books_sections,
               } | base_ctx
        return self.render_to_response(ctx)


class BooksSectionView(TemplateResponseMixin, View):
    template_name = 'books/books_section.html'

    def get(self, *args, **kwargs):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        book_section = BooksSection.objects.get(slug=kwargs['slug'])
        return self.render_to_response({'book_section': book_section} | base_ctx)


class BooksGenreView(TemplateResponseMixin, View):
    template_name = 'books/books_genre.html'

    def get(self, *args, **kwargs):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        book_section = BooksSection.objects.get(slug=kwargs['slug_section'])
        book_genre = BooksGenre.objects.get(slug=kwargs['slug_genre'])
        books = Book.objects.filter(genre=book_genre)

        return self.render_to_response({'book_section': book_section,
                                        'book_genre': book_genre,
                                        'books': books,
                                        } | base_ctx)


class BookDetailView(TemplateResponseMixin, View):
    template_name = 'books/book_detail.html'

    def get(self, *args, **kwargs):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        book = Book.objects.get(slug=kwargs['slug'])
        genre_of_book = (str(book.genre).split(' - ')[1])

        ctx = {'book': book,
               'genre_of_book': genre_of_book,
               } | base_ctx
        return self.render_to_response(ctx)
