
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djutil.models import TimeStampedModel
from dateutil.relativedelta import relativedelta
from . import manager
from enum import Enum
from enum import IntEnum
from datetime import date
import os
from api import utils as api_utils

# Create your models here.



class User(AbstractBaseUser, TimeStampedModel):

    id = models.CharField(_('user id'), max_length=20, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=254, blank=True, default="")
    middle_name = models.CharField(_('middle name'), max_length=254, blank=True, default="")
    last_name = models.CharField(_('last name'), max_length=254, blank=True, default="")
    username = models.CharField(_('username'), max_length=254, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    phone_regex = RegexValidator(regex='[0-9]{10,12}',
                                 message=_("Phone number must be entered in the format:"
                                           " '9999999999'. Up to 12 digits allowed."))
    phone_number = models.CharField(_('phone_number'), validators=[phone_regex], max_length=12, blank=False, null=False,
                                    unique=True)
    dob = models.DateField(_('dob'), blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect it instead of deleting accounts.'))

    USERNAME_FIELD = 'email'

    objects = manager.CustomUserManager()

    # class Meta:
    #     """
    #
    #     """
    #     app_label = 'profiles'

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = api_utils.gen_hash(api_utils.expires())

        self.clean()

        super(User, self).save(*args, **kwargs)

    def clean(self):
        super(User, self).clean()
        if self.email:
            self.username = self.email

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(x for x in parts if x)

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name.strip()