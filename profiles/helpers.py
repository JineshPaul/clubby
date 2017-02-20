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