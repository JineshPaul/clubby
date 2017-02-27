from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^movie/add/$", views.Movie.as_view(), name='movie-add'),
    url(r"^movie/get/$", views.Movie.as_view(), name='movie-get'),
    url(r"^movie/delete/$", views.DeleteMovie.as_view(), name='movie-delete'),
    url(r"^cast/add/$", views.Cast.as_view(), name='cast-add'),
    url(r"^cast/get/$", views.Cast.as_view(), name='cast-get'),
   ]