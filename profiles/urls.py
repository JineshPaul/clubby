from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^info/$", views.UserInfo.as_view(), name='user-info'),
    url(r"^register/$", views.Register.as_view(), name='register-user'),
    url(r"^login/$", views.Login.as_view(), name='login-user'),
    #url(r'^profile/completeness/', views.ProfileCompleteness.as_view(), name='profile-completeness'),

    ]
