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
from django.utils import timezone
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


def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        return HttpResponse("valid link")
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                request.session['email'] = user.email
                user.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        return HttpResponse("Invalid link")
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)
    context.update({'email': request.session['email']})
    request.session['email'] = None
    return TemplateResponse(request, template_name, context)


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
            user.first_name = serializer.validated_data.get("first_name","")
            user.last_name = serializer.validated_data.get("last_name","")
            user.occupation = serializer.validated_data.get("occupation", None)
            user.save()
            user_response = dict(serializer.data)

            code = api_utils.code_generator(50)
            models.EmailCode.objects.update_or_create(
                user=user, defaults={'code': code, 'expires_at': datetime.now() + timedelta(hours=24)})

            helpers.send_verify_email(user, code, use_https=settings.USE_HTTPS)

            access_token = helpers.get_access_token(user, password)
            bearer_token = access_token['access_token']
            headers = {"Authorization": "Bearer " + bearer_token}
            print(api_utils.response({"user": user_response
                                       }, headers=headers))
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


class ChangePassword(APIView):
    """
    Change password api which essentailly just check if its a email of a valid user who is active and change password
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        :param request:
        Changes password to newer password set
        """
        user = request.user
        if request.data.get("old_password") and request.data.get("new_password"):
            if user.is_active:
                if user.check_password(request.data.get("old_password")):
                    user.set_password(request.data.get("new_password"))
                    user.save()
                    return api_utils.response({"message": constants.PASSWORD_CHANGED})
                else:
                    return api_utils.response({"message": constants.INCORRECT_OLD_PASSWORD}, status.HTTP_404_NOT_FOUND,
                                              constants.INCORRECT_OLD_PASSWORD)
            else:
                return api_utils.response({"message": constants.NON_ACTIVE_USER_ERROR}, status.HTTP_404_NOT_FOUND,
                                          constants.NON_ACTIVE_USER_ERROR)
        else:
            return api_utils.response({"message": constants.MALFORMED_REQUEST}, status.HTTP_404_NOT_FOUND,
                                      constants.MALFORMED_REQUEST)


class ResetPassword(APIView):
    """
    Reset password api which essentally just check if its a email of a valid user who is active and sends a resset
    passsword link to them
    """

    def post(self, request, *args, **kwargs):
        """
        :param request:
        Changes password to newer password set
        """
        email = request.data.get('email')
        # TODO: Check if this is valid email using soe tech
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return api_utils.response({"message": constants.INCORRECT_EMAIL}, status.HTTP_404_NOT_FOUND,
                                      constants.INCORRECT_EMAIL)
        if user.is_active:
                helpers.send_reset_email(user=user)
                return api_utils.response({"message": constants.RESET_EMAIL_SENT, "case": 1})
        else:
            return api_utils.response({"message": constants.UNABLE_TO_RESET}, status.HTTP_404_NOT_FOUND,
                                      constants.NON_ACTIVE_USER_ERROR)


class CheckEmailCode(APIView):
    """
    Checks if the code sent by user is same as one stored
    """

    def get(self, request, token):
        """
        :param request:
        :param token:an alphanumeric token of length 50.
        :return:
        """
        try:
            code_entry = models.EmailCode.objects.select_related("user").get(code=token)
        except models.EmailCode.DoesNotExist:
            return render(request, 'verify_email/email_verified.html', {'user': None, 'verification_allowed': 0})

        user = code_entry.user
        if code_entry.expires_at >= timezone.now():
            user.email_verified = True
            user.save()
            code_entry.delete()
            return render(request, 'verify_email/email_verified.html', {'user': user, 'verification_allowed': 1})
        else:
            return render(request, 'verify_email/email_verified.html', {'user': user, 'verification_allowed': 0})

class ResendVerifyEmail(APIView):
    """
    Send a verification email to user given email address
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        :param request:
        :return:
        """
        flag_data = {}

        user = request.user
        if user.is_active:
            code = api_utils.code_generator(50)
            models.EmailCode.objects.update_or_create(
                user=user, defaults={'code': code, 'expires_at': datetime.now() + timedelta(hours=24)})

            helpers.send_verify_email(user=user, applicant_name=applicant_name, code=code, use_https=settings.USE_HTTPS)
            return api_utils.response({"message": constants.VERIFY_EMAIL_SENT})
        else:
            return api_utils.response({"message": constants.NON_ACTIVE_USER_ERROR}, status.HTTP_404_NOT_FOUND,
                                      constants.NON_ACTIVE_USER_ERROR)


class AdditionalInfo(APIView):
    """
    Add additional information about user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        """
        :param request:
        :return:
        """
        return_data = {}
        try:
            contact = models.Address.objects.get(user=request.user)
        except models.Address.DoesNotExist:
            address = {'pincode':'',
                       'address1':'',
                       'address2':'',
                       'city':'',
                       'district':'',
                       'state':'',
                       'country':''
                       }
            return_data["address"]= address
            return_data["dob"] = request.user.dob if request.user.dob else ""
            return_data["gender"] = request.user.gender if request.user.gender else ""
            return_data["marital_status"] = request.user.marital_status if request.user.marital_status else ""
            return api_utils.response(return_data)
        serializer = serializers.AddressSerializer(contact)
        if serializer.is_valid:
            return_data["address"] = serializer.data
            return_data["dob"] = request.user.dob if request.user.dob else ""
            return_data["gender"] = request.user.gender if request.user.gender else ""
            return_data["marital_status"] = request.user.marital_status if request.user.marital_status else ""
            return api_utils.response(return_data)
        return api_utils.response({}, status.HTTP_400_BAD_REQUEST, generate_error_message(serializer.errors))


    def post(self,request):
        """
        :param request:
        :return:
        """
        additional_serializer = serializers.AdditionalInfoSerializer(data=request.data)
        if additional_serializer.is_valid():
            user = request.user
            user.dob = additional_serializer.validated_data.get("dob")
            user.gender = additional_serializer.validated_data.get("gender")
            user.marital_status = additional_serializer.validated_data.get("marital_status")
            user.save()
        else:
            return api_utils.response({}, status.HTTP_400_BAD_REQUEST, api_utils.generate_error_message(additional_serializer.errors))

        serializer = serializers.AddressSerializer(data=request.data.get("address",""))
        if serializer.is_valid():
            models.Address.objects.update_or_create(user=request.user, defaults=serializer.data)
            return api_utils.response({"message": constants.SUCCESS})
        else:
            return api_utils.response({}, status.HTTP_400_BAD_REQUEST, api_utils.generate_error_message(serializer.errors))



