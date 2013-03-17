#bookstore/views.py
#Rolph Recto

from django.contrib.auth.models import User
from bookstore.models import Author, Book, Review
from django.views.generic.list import ListView
from django.db.models import Avg
from django.shortcuts import get_object_or_404

class BookReviewListView(ListView):
    """View for a list of reviews for a book"""
    model = Review
    template_name = 'bookstore/book_review_list.html'

    def get_queryset(self):
        self.book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        return Review.objects.filter(book=self.book)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookReviewListView, self).get_context_data(**kwargs)
        # Add in the book
        context['book'] = self.book
        agg_list = self.get_queryset().aggregate(Avg('rating'))
        context['average_rating'] = agg_list['rating__avg']
        return context


class UserReviewListView(ListView):
    """View for a list of reviews for a user"""
    model = Review
    template_name = 'bookstore/user_review_list.html'

    def get_queryset(self):
        #URLconf captured user id
        if 'user_id' in self.kwargs:
            self.user = get_object_or_404(User, pk=self.kwargs['user_id'])
        #URLconf captured username
        else:
            self.user = get_object_or_404(User, username=self.kwargs['username'])

        return Review.objects.filter(user=self.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserReviewListView, self).get_context_data(**kwargs)
        # Add in the book
        context['user'] = self.user
        agg_list = self.get_queryset().aggregate(Avg('rating'))
        context['average_rating'] = agg_list['rating__avg']
        return context
