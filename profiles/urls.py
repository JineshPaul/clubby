from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^info/$", views.UserInfo.as_view(), name='user-info'),
    url(r"^register/$", views.Register.as_view(), name='register-user'),
    url(r"^login/$", views.Login.as_view(), name='login-user'),
    url(r"^change/password/$", views.ChangePassword.as_view(), name='change-password'),
    url(r"^reset/password/$", views.ResetPassword.as_view(), name='reset-password'),
    url(r"^verify/confirm/(?P<token>[A-Z0-9]{50})/$", views.CheckEmailCode.as_view(), name='check-email-code'),
    url(r"^resend/verify/email/$", views.ResendVerifyEmail.as_view(), name='resend-verify-email'),
    url(r"^additional/info/add/$", views.AdditionalInfo.as_view(), name='additional-info-add'),
    url(r"^additional/info/get/$", views.AdditionalInfo.as_view(), name='additional-info-get'),




    #url(r'^profile/completeness/', views.ProfileCompleteness.as_view(), name='profile-completeness'),

    ]
