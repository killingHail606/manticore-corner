from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Rules


@admin.register(Rules)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
