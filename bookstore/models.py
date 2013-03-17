#bookstore/models.py
#Rolph Recto

from django.contrib.auth.models import User
from django.db import models

from django.core.exceptions import ValidationError

from bookstore import util


class Author(models.Model):
    """Model class for authors"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    """Model class for books"""

    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author)
    #we're assuming that no book is published before 0 A.D.
    publication_year = models.IntegerField(null=True,
        validators=[util.not_negative])

    def __unicode__(self):
        return self.title


class Review(models.Model):
    """Model class for user reviews of books"""

    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    timestamp = models.DateTimeField()
    #what the user had to say about the book
    review_message = models.TextField()
    #ratings go from 1-5
    rating = models.IntegerField(
        choices=(
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        )
    )

    def __unicode__(self):
        return self.user.username + " : " + self.book.title