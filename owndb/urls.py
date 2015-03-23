from django.conf.urls import patterns, include, url
from django.contrib import admin


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^store/', include('store.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       )
