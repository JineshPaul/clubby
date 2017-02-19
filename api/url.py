from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include
import profiles

urlpatterns = [
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    #url(r"^user/", include('profiles.url', namespace='profiles_urls')),
    #url(r"^core/", include('core.url', namespace='core_urls')),
    #url(r"^open/", include('external_api.url', namespace='external_api_urls'))
]