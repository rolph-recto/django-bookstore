#bookstore/views.py
#Rolph Recto

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout

from bookstore.models import Author, Book, Review
from bookstore.forms import LoginForm


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

        # Add in the user
        context['queried_user'] = self.user

        agg_list = self.get_queryset().aggregate(Avg('rating'))
        context['average_rating'] = agg_list['rating__avg']

        return context


class BookListView(ListView):
    """View for a list of books"""
    model = Book
    template_name = 'bookstore/book_list.html'

    def get_queryset(self):
        return (Book.objects.all()
            .annotate(Avg('review__rating'))
            .order_by('title'))


class LoginView(FormView):
    """View for the login page"""
    template_name = 'bookstore/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('bookstore:login_success')

    def form_valid(self, form):
        #try to log the user in
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        #no need to check user because we already authenticated it in the form
        login(self.request, user)

        return super(LoginView, self).form_valid(form)


class LogoutView(TemplateView):
    """View for the logout page"""
    template_name = 'bookstore/logout.html'

    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)

        #log user out
        print self.request.user
        if self.request.user.is_authenticated():
            logout(self.request)
            context['logout_success'] = True
        #user wasn't logged in
        else:
            context['logout_success'] = False

        return context




