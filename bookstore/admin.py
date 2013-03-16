#bookstore/admin.py

from django.contrib import admin
from bookstore.models import Author, Book, Review


class AuthorAdmin(admin.ModelAdmin):
    """ModelAdmin class for Author model"""
    list_display = ('last_name', 'first_name', )
    search_fields = ('first_name', 'last_name',)


class BookAdmin(admin.ModelAdmin):
    """ModelAdmin class for Book model"""
    list_display = ('title', 'author', 'publication_year',)
    search_fields = ('title',)
    ordering = ('publication_year', 'title',)


class ReviewAdmin(admin.ModelAdmin):
    """"ModelAdmin class for Review model"""
    list_display = ('user', 'book', 'rating', 'timestamp')
    date_hierarchy = 'timestamp'
    ordering = ('timestamp',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)