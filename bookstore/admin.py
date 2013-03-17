#bookstore/admin.py
#by Rolph Recto

from django.contrib import admin
from bookstore.models import Author, Book, Review


class AuthorAdmin(admin.ModelAdmin):
    """ModelAdmin class for Author model"""
    list_display = ('pk', 'last_name', 'first_name', )
    search_fields = ('pk', 'first_name', 'last_name',)


class BookAdmin(admin.ModelAdmin):
    """ModelAdmin class for Book model"""
    list_display = ('pk', 'title', 'author', 'publication_year',)
    search_fields = ('title',)
    ordering = ('publication_year', 'title',)


class ReviewAdmin(admin.ModelAdmin):
    """"ModelAdmin class for Review model"""
    list_display = ('pk', 'user', 'book', 'rating', 'timestamp')
    date_hierarchy = 'timestamp'
    ordering = ('timestamp',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)