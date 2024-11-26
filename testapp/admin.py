from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn')
    search_fields = ('title', 'author', 'isbn')
    
    class Media:
        css = {
            'all': ('admin_autocomplete/css/autocomplete.css',)
        }
        js = ('admin_autocomplete/js/autocomplete.js',)
