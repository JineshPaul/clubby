from django.shortcuts import render
from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.core.files.base import ContentFile
import urllib.request as urllib2

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from copy import deepcopy
import functools
import logging
import warnings
import logging
import threading
import re
import base64

from . import models, utils,serializers,helpers,constants
from api import utils as api_utils

# Create your views here.


class UserInfo(APIView):
    """
    Retrieve, update or delete a profile instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        GET user data
        """
        serializer = serializers.UserSerializer(request.user)
        if serializer.is_valid:
            print(serializer.data)
        return api_utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST, constants.PROFILE_GET_ERROR)


class Register(APIView):
    """
    Register views
    """
    def post(self, request, format=None):
        """
        Api to register user
        We are setting the email given as username too.
        """
        # TODO: make things atomic
        flag = False
        user = None
        serializer = serializers.UserRegisterSerializer(data=request.data)
        email = serializer.initial_data.get("email")
        password = serializer.initial_data.get("password")
        phone = serializer.initial_data.get("phone_number")
        kwargs = {'email': email, 'phone_number': phone, 'password': password}
        result = utils.check_existing_user(**kwargs)
        if result == 1:
            return api_utils.response({"message": constants.SIGNUP_ERROR, "signup_error": result},
                                      status.HTTP_404_NOT_FOUND,
                                      "email already exist")
        elif result == 2:
            return api_utils.response({"message": constants.SIGNUP_ERROR, "signup_error": result},
                                      status.HTTP_404_NOT_FOUND,
                                      "phone already exist")
        if serializer.is_valid():
            username = serializer.validated_data.get("email")
            user = models.User.objects.create_user(email=email, username=username, password=password,
                                                       phone_number=phone)
            user.image = request.FILES.get("image", None)
            user.save()
            user_response = dict(serializer.data)
            access_token = helpers.get_access_token(user, password)
            bearer_token = access_token['access_token']
            headers = {"Authorization": "Bearer " + bearer_token}
            return api_utils.response({"user": user_response
                                       }, headers=headers)
        else:
            return api_utils.response({}, status.HTTP_404_NOT_FOUND, api_utils.generate_error_message(serializer.errors))


class Login(APIView):
    """
    Login user api
    """

    def post(self, request, *args, **kwargs):
        """
        The login_error cases:
        0 - user serializer errors
        1 - user with the given email or phone does not exist.
        2 - both email and phone not verified hence not able to login.
        3 - phone_number is not verified.
        4 - email is not verified.
        5 - incorrect password entered.
        6 - non-active user.

        :param request:
        An internal call to /o/token/ is sent to get access token which is then returned as response
        """
        login_error = constants.LOGIN_ERROR_0  # login_error holds the type of error generated.
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = None
        email_id = None
        try:
            if '@' in username:
                email_id = username
                user = models.User.objects.get(email__iexact=username)
            else:
                phone_number = username
                user = models.User.objects.get(phone_number=username)
        except models.User.DoesNotExist:
            login_error = constants.LOGIN_ERROR_1
            return api_utils.response({"message": constants.UNABLE_TO_LOGIN, "login_error": login_error},
                                      status.HTTP_404_NOT_FOUND,
                                      constants.NON_EXISTENT_USER_ERROR)

        serializer = serializers.UserRegisterSerializer(user)
        if serializer.is_valid:
            if user.is_active:
                if user.check_password(password):
                    access_token = helpers.get_access_token(user, password)
                    bearer_token = access_token['access_token']
                    headers = {"Authorization": "Bearer " + bearer_token}
                    return api_utils.response({"user": serializer.data},headers=headers)
                else:
                    login_error = constants.LOGIN_ERROR_5
                    return api_utils.response({"message": constants.UNABLE_TO_LOGIN, "login_error": login_error},
                                              status.HTTP_404_NOT_FOUND,
                                              constants.LOGIN_ERROR)
            else:
                login_error = constants.LOGIN_ERROR_6
                return api_utils.response({"message": constants.UNABLE_TO_LOGIN, "login_error": login_error},
                                          status.HTTP_404_NOT_FOUND,
                                          constants.NON_ACTIVE_USER_ERROR)
        else:
            login_error = constants.LOGIN_ERROR_0
            return api_utils.response({"message": constants.UNABLE_TO_LOGIN, "login_error": login_error},
                                      status.HTTP_404_NOT_FOUND, api_utils.generate_error_message(serializer.errors))



