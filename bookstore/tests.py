#bookstore/tests.py
#Rolph Recto

import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from bookstore.models import Author, Book, Review
from django.core.exceptions import ValidationError

class BookstoreModelsTest(TestCase):
    """Test suite for Bookstore models"""

    def testAuthorString(self):
        """Test whether string representation of Author is correct"""

        a = Author(first_name='Ernest', last_name='Hemingway')
        self.assertEqual(str(a), 'Ernest Hemingway')


    def testAuthorNullFields(self):
        """Test whether Author with Null fields is invalidated"""
        #last name is Null
        a1 = Author(first_name='Ernest')
        self.assertRaises(ValidationError, a1.full_clean)

        #first name is Null
        a2 = Author(last_name='Hemingway')
        self.assertRaises(ValidationError, a2.full_clean)


    def testBookString(self):
        """Test whether string representation of Book is correct"""

        b = Book(
            title='A Farewell to Arms',
            author=Author(first_name='Ernest', last_name='Hemingway'),
            publication_year=1929
        )

        self.assertEqual(str(b), 'A Farewell to Arms')


    def testBookNullFields(self):
        """Test whether Book with Null fields is invalidated"""
        #title is Null
        b1 = Book(author=Author(first_name='Ernest', last_name='Hemingway'))
        self.assertRaises(ValidationError, b1.full_clean)

        #author is Null
        b2 = Book(title='A Farewell to Arms')
        self.assertRaises(ValidationError, b2.full_clean)

        #no need to test for publication year, as it is optional


    def testBookNegativePublicationYear(self):
        """Test whether a Book with a negative pub year is invalidated"""

        b = Book(
            title='A Farewell to Arms',
            author=Author(first_name='Ernest', last_name='Hemingway'),
            publication_year=-10
        )

        self.assertRaises(ValidationError, b.full_clean)


    def testReviewString(self):
        """Test whether string representation of Review is correct"""

        r = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            review_message='',
            rating=1
        )

        self.assertEqual(str(r), 'guy : A Farewell to Arms')


    def testReviewNullFields(self):
        """Test whether Book with Null fields is invalidated"""

        #user is Null
        r1 = Review(
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            review_message='',
            rating=1
        )
        self.assertRaises(ValidationError, r1.full_clean)

        #book is Null
        r2 = Review(
            user=User(username='guy'),
            timestamp=datetime.datetime.now(),
            review_message='',
            rating=1
        )
        self.assertRaises(ValidationError, r2.full_clean)

        #timestamp is Null
        r3 = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            review_message='',
            rating=1
        )
        self.assertRaises(ValidationError, r3.full_clean)

        #review_message is Null
        r4 = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            rating=1
        )
        self.assertRaises(ValidationError, r4.full_clean)

        #rating is Null
        r5 = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            review_message='',
        )
        self.assertRaises(ValidationError, r5.full_clean)


    def testReviewInvalidRating(self):
        """Test whether a review with an invalid rating
        (ie. not 1-5) is invalid"""

        #rating is less than 1
        r1 = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            review_message='',
            rating=0
        )
        self.assertRaises(ValidationError, r1.full_clean)

        #rating is greater than 5
        r2 = Review(
            user=User(username='guy'),
            book=Book(title='A Farewell to Arms'),
            timestamp=datetime.datetime.now(),
            review_message='',
            rating=6
        )
        self.assertRaises(ValidationError, r2.full_clean)


class BookstoreViewsTest(TestCase):
    """Test suite for Bookstore views"""

    def testSimple(self):
        self.assertEqual(1, 1)


