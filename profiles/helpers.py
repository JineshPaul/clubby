"""
To make structure of code more organised. We are keeping all those functions that don't involve model queries here

"""
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

import requests
from requests.auth import HTTPBasicAuth
import logging
import copy
from django.db.models import Sum
import datetime
from oauth2_provider.models import AccessToken
from django.conf import settings


def get_access_token(user, password,is_web=True):
    """
    :return: The json formatted data to be returned along with access_token
    """
    data = {'grant_type': 'password', 'username': user.username, 'password': password}
    auth = HTTPBasicAuth(settings.CLIENT_ID, settings.CLIENT_SECRET)
    response = requests.post(settings.BASE_URL + '/o/token/', auth=auth, data=data)
    responseJSON = response.json()
    if not responseJSON.get('access_token'):
        #logger = logging.getLogger('django.error')
        #logger.error("Profiles: access_token: Access token failed for user with id: " + user.id)
        print("access error no token ")

    return responseJSON


def send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    logger = logging.getLogger('django.debug')

    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    if email_template_name is not None:
        body = loader.render_to_string(email_template_name, context)
    else:
        body = ''
    if isinstance(to_email, list):
        email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    else:
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
        logger.debug("send_email: to: " + to_email + " template: " + html_email_template_name)

    email_message.send()


def send_reset_email(user, domain_override=None,
                     subject_template_name='registration/password_reset_request_subject.txt',
                     email_template_name=None, use_https=False,
                     token_generator=default_token_generator, from_email=None, request=None,
                     html_email_template_name='registration/password_reset_email.html', extra_email_context=None):
    """
    Generates a one-use only link for resetting password and sends to the
    user.
    """
    if user.first_name != "":
        user_name = user.first_name.title()
    else:
        user_name = user.email

    context = {
        'email': user.email,
        'user_name': user_name,
        'domain': settings.BASE_URL,
        'site_name': "Clubby",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }
    send_mail(subject_template_name, email_template_name, context, from_email, user.email,
              html_email_template_name=html_email_template_name)


def send_verify_email(user, code, domain_override=None,
                      subject_template_name='verify_email/verify_email_subject.txt',
                      email_template_name=None, use_https=False,
                      token_generator=default_token_generator, from_email=None, request=None,
                      html_email_template_name='verify_email/verify_email.html', extra_email_context=None):
    """

    :param user: user whose email is to be verified
    :param code: an alphanumeric code of length 50
    :param domain_override:
    :param subject_template_name: file containing subject of email
    :param email_template_name: file containing body of email
    :param use_https: boolean to whether use https or not
    :param token_generator:
    :param from_email:
    :param request:
    :param html_email_template_name:
    :param extra_email_context:
    :return:
    """
    if user.first_name != "":
        user_name = user.first_name.title()
    else:
        user_name = user.email

    context = {
        'user_name': user_name,
        'email': user.email,
        'domain': settings.BASE_URL,
        'site_name': "Clubby",
        'user': user,
        'token': code,
        'protocol': 'https' if use_https else 'http',
    }
    send_mail(subject_template_name, email_template_name, context, from_email, user.email,
              html_email_template_name=html_email_template_name)
