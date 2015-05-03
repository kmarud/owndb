from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import ProfileDetail

urlpatterns = patterns('',
   url(r'^', include('pages.urls')),	
   url(r'^admin/', include(admin.site.urls)),
   url(r'^store/', include('store.urls')),
   url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),
   url(r'^accounts/', include('allauth.urls')),
   url(r'^accounts/profile$', ProfileDetail.as_view(), name='profile-detail')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

