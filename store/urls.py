from django.conf.urls import patterns, include, url
from store.views import ProjectList
from store.views import ProjectAdd
from store.views import ProjectDelete
from store.views import ProjectEdit
from store.views import FormList
from store.views import FormAdd
from store.views import FormDelete
from store.views import FormEdit
from store.views import FormInstanceAdd
from store.views import FormInstanceList
from store.views import FormInstanceDetail

urlpatterns = patterns('',
    url(r'^p(?P<page>[0-9]+)/$', ProjectList.as_view(), name='project-list'),
    url(r'^add/?$', ProjectAdd.as_view(), name='project-add'),
    url(r'^/?$', ProjectList.as_view(), name='project-list'),
    url(r'^(?P<project>[\w\-\_]+)/p(?P<page>[0-9]+)/$', FormList.as_view(), name='form-list'),
    url(r'^(?P<project>[\w\-\_]+)/edit/?$', ProjectEdit.as_view(), name='project-edit'),
    url(r'^(?P<project>[\w\-\_]+)/delete/?$', ProjectDelete.as_view(), name='project-delete'),
    url(r'^(?P<project>[\w\-\_]+)/add/?$', FormAdd.as_view(), name='form-add'),
    url(r'^(?P<project>[\w\-\_]+)/?$', FormList.as_view(), name='form-list'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/p(?P<page>[0-9]+)/$', FormInstanceList.as_view(), name='forminstance-list'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/edit/?$', FormEdit.as_view(), name='form-edit'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/delete/?$', FormDelete.as_view(), name='form-delete'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/add/?$', FormInstanceAdd.as_view(), name='forminstance-add'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/?$', FormInstanceList.as_view(), name='forminstance-list'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/(?P<forminstance>[\w\-\_]+)/p(?P<page>[0-9]+)/$', FormInstanceDetail.as_view(), name='forminstance-detail'),
    url(r'^(?P<project>[\w\-\_]+)/(?P<form>[\w\-\_]+)/(?P<forminstance>[\w\-\_]+)/?$', FormInstanceDetail.as_view(), name='forminstance-detail'),
)
