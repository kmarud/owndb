from django.conf.urls import patterns, include, url
from accounts.views import RegistrationView
from accounts.views import login_user


urlpatterns = patterns('',
                       url(r'^/?$', RegistrationView.as_view(), name='registraionview-list'),
                       url(r'^login$', login_user, name='login'),
                       url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/'}),
                       )