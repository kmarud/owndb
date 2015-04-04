from django.conf.urls import patterns, include, url
from django.contrib import admin


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
					   url(r'^$', include('pages.urls')),	
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^store/', include('store.urls')),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),
                       url(r'^accounts/', include('allauth.urls')),
                       )
