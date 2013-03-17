#bookstore/urls.py
#Rolph Recto

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('bookstore',
    url(r'^$',
        TemplateView.as_view(template_name='bookstore/index.html'),
        name='index'),
)