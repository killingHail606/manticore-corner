from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Hero


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_pub')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_pub'

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
