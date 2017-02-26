"""cinema_clubby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from oauth2_provider import models as oauth_models
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from oauth2_provider import models as oauth_models
from django.conf.urls.static import static
from django.views.generic import TemplateView
import api
from core import views
from profiles import views as profile_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('', include('django.contrib.auth.urls')),
    url(r"^social/", include('social.apps.django_app.urls', namespace='social')),
    url(r"^auth/", include('rest_framework_social_oauth2.urls')),
    url(r"^v1.0/", include('api.urls', namespace='api_urls')),
    url(r"^$", views.index, name='index'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        profile_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', profile_views.password_reset_complete, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.unregister(oauth_models.AccessToken)
admin.site.unregister(oauth_models.Grant)
admin.site.unregister(oauth_models.RefreshToken)
admin.site.unregister(oauth_models.Application)
