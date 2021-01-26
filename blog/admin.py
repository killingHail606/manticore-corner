from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Post, Lexicon, Quote, AboutBlog


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_pub', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_pub'
    ordering = ('status', 'date_pub')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


@admin.register(Lexicon)
class LexiconAdmin(admin.ModelAdmin):
    list_display = ('word', 'description')
    search_fields = ('word', 'description')


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'body')
    search_fields = ('author', 'body')


@admin.register(AboutBlog)
class AboutBlogAdmin(admin.ModelAdmin):
    list_display = ('title',)

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
