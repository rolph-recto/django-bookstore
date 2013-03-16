#bookstore/admin.py

from django.contrib import admin
from bookstore.models import Author, Book, Review

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)