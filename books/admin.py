from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Book, BooksGenre, BooksSection


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'date_pub', 'genre')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title', 'author')}
    date_hierarchy = 'date_pub'
    ordering = ('date_pub',)

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


@admin.register(BooksGenre)
class BooksGenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'list')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BooksSection)
class BooksSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
