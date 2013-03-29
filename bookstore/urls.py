#bookstore/urls.py
#Rolph Recto

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from bookstore.models import Book, Author, Review
from bookstore.views import *

urlpatterns = patterns('bookstore.views',
    #index/homepage
    url(r'^$',
        TemplateView.as_view(template_name='bookstore/index.html'),
        name='index'),
    url(r'^index/?$',
        TemplateView.as_view(template_name='bookstore/index.html'),
        name='index'),

    #login user
    url(r'^login/?$',
        LoginView.as_view(),
        name='login'),

    #login success
    url(r'^login/success/?$',
        TemplateView.as_view(template_name='bookstore/login_success.html'),
        name='login_success'),

    #login user
    url(r'^logout/?$',
        LogoutView.as_view(),
        name='logout'),

    #list of reviews for a certain book
    url(r'^book/(?P<book_id>[0-9]+?)/?$',
        BookReviewListView.as_view(),
        name='book_review_list'
    ),

    #list of reviews for a certain user
    url(r'^user/(?P<user_id>[0-9]+?)/?$',
        UserReviewListView.as_view(),
        name='user_review_list'
    ),
    url(r'^user/(?P<username>.+?)/?$',
        UserReviewListView.as_view(),
        name='user_review_list'
    ),

    #list of books, sorted
    url(r'^books?/?$',
        BookListView.as_view(),
        name='book_list'
    ),
)