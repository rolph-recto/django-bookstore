#bookstore/tests.py
#Rolph Recto

import datetime

from django.test import TestCase
from django.contrib.auth.models import User, UserManager
from bookstore.models import Author, Book, Review
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch

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

    def setUp(self):
        self.user = User(username='user', password='password', email='u@ex.com')
        self.user.save()

        self.author = Author(first_name='Ernest', last_name='Hemingway')
        self.author.save()

        self.book = Book(title='A Farewell to Arms', author=self.author,
            publication_year=1929)
        self.book.save()

        self.book2 = Book(title='The Sun Also Rises', author=self.author,
            publication_year=1926)
        self.book2.save()

        self.book3 = Book(title='For Whom The Bell Tolls', author=self.author,
            publication_year=1940)
        self.book3.save()

        self.review = Review(
            user=self.user,
            book=self.book,
            timestamp=datetime.datetime.now(),
            review_message='Good Book',
            rating=5
        )

    def testIndex(self):
        """Test bookstore index view"""
        response = self.client.get(reverse('bookstore:index'))
        #Just make sure the page loads, that's all
        self.assertEqual(response.status_code, 200)

    def testBookReviewList(self):
        """Test books review list view"""
        #if no book id was specified, it should return an error
        self.assertRaises(
            NoReverseMatch,
            lambda: self.client.get(reverse('bookstore:book_review_list'))
        )

        #if the book id is invalid, it should return an error
        response = self.client.get(reverse(
            'bookstore:book_review_list',
            kwargs = {'book_id':0}
        ))
        self.assertEqual(response.status_code, 404)

        #if the book id is valid, it should give the right book
        response = self.client.get(reverse(
            'bookstore:book_review_list',
            kwargs = {'book_id':1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book'].title, 'A Farewell to Arms')

    def testUserReviewList(self):
        """Test user review list view"""
        #if no user id was specified, it should return an error
        self.assertRaises(
            NoReverseMatch,
            lambda: self.client.get(reverse('bookstore:user_review_list'))
        )

        #if the user id is invalid, it should return an error
        response = self.client.get(reverse(
            'bookstore:user_review_list',
            kwargs = {'user_id':0}
        ))
        self.assertEqual(response.status_code, 404)

        #if the username is invalid, it should return an error
        response = self.client.get(reverse(
            'bookstore:user_review_list',
            kwargs = {'username':'nobody'}
        ))
        self.assertEqual(response.status_code, 404)

        #if the user id is valid, it should give the right book
        response = self.client.get(reverse(
            'bookstore:user_review_list',
            kwargs = {'user_id':1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['queried_user'].username, 'user')
        self.assertEqual(response.context['queried_user'].pk, 1)

        #if the username is valid, it should give the right book
        response = self.client.get(reverse(
            'bookstore:user_review_list',
            kwargs = {'username':'user'}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['queried_user'].username, 'user')
        self.assertEqual(response.context['queried_user'].pk, 1)

    def testBookList(self):
        """Test book list view"""
        #make sure the context has a list of books, in alphabetical order
        response = self.client.get((reverse('bookstore:book_list')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book_list'][0].title,
            'A Farewell to Arms')
        self.assertEqual(response.context['book_list'][1].title,
            'For Whom The Bell Tolls')
        self.assertEqual(response.context['book_list'][2].title,
            'The Sun Also Rises')


