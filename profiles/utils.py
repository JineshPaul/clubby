from django.conf import settings
from django.db.models import Sum, F
from . import models as profile_models


def check_existing_user(**kwargs):
    """
       this method check the whether user exist or not in database
       email, password, phone
    """
    email = kwargs['email']
    phone = kwargs['phone_number']


    try:
        user = profile_models.User.objects.get(email__iexact=email)
        result = 1
    except profile_models.User.DoesNotExist:
        try:
            user = profile_models.User.objects.get(phone_number = phone)
            result = 2
        except profile_models.User.DoesNotExist:
            user = None
            result = 3
    return result



