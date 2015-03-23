from django.conf.urls import patterns, include, url
from accounts.views import RegistrationView


urlpatterns = patterns('',
                       url(r'^/?$', RegistrationView.as_view(), name='registraionview-list'),
                       url(r'^login$', 'django.contrib.auth.views.login', {'next_page': '/store'}),
                       url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/'}),
                       )