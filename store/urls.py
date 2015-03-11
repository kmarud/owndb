from django.conf.urls import patterns, include, url
from store.views import CategoryList
from store.views import FormList
from store.views import FormInstanceList
from store.views import FormInstanceDetail

urlpatterns = patterns('',
                       url(r'^/(?P<page>[0-9]+)/$', CategoryList.as_view(), name='category-list'),
                       url(r'^/?$', CategoryList.as_view(), name='category-list'),
                       url(r'^(?P<category>[\w\-\_]+)/(?P<page>[0-9]+)/$', FormList.as_view(), name='form-list'),
                       url(r'^(?P<category>[\w\-\_]+)$', FormList.as_view(), name='form-list'),
                       url(r'^(?P<category>[\w\-\_]+)/(?P<form>[\w\-\_]+)/(?P<page>[0-9]+)/$', FormInstanceList.as_view(), name='forminstance-list'),
                       url(r'^(?P<category>[\w\-\_]+)/(?P<form>[\w\-\_]+)$', FormInstanceList.as_view(), name='forminstance-list'),
                       url(r'^(?P<category>[\w\-\_]+)/(?P<form>[\w\-\_]+)/(?P<forminstance>[\w\-\_]+)/(?P<page>[0-9]+)/$', FormInstanceDetail.as_view(), name='forminstance-detail'),
                       url(r'^(?P<category>[\w\-\_]+)/(?P<form>[\w\-\_]+)/(?P<forminstance>[\w\-\_]+)$', FormInstanceDetail.as_view(), name='forminstance-detail'),
                       )