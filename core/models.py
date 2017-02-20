# -*- coding: utf-8 -*-
from enum import IntEnum
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Max, Sum, Q

from django.contrib.postgres.fields import HStoreField, ArrayField
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from djutil.models import TimeStampedModel
from django.db.models import F

from profiles import models as profile_models

# Create your models here.


class Movie(TimeStampedModel):
    """
    Store the portfolio information
    """
    user = models.ForeignKey(profile_models.User)
    title = models.CharField(_('Title '), max_length=254, blank=False, null=False)
    description = models.TextField(_("Description"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.user) + str(self.id)


class Review(TimeStampedModel):
    """
    Store the portfolio information
    """
    user = models.ForeignKey(profile_models.User)
    movie = models.ForeignKey(Movie,null=True, blank=True, default=None)
    review = models.TextField(_("Review"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.user) + str(self.id)


class Rating(TimeStampedModel):
    """
    Store the portfolio information
    """
    user = models.ForeignKey(profile_models.User)
    movie = models.ForeignKey(Movie,null=True, blank=True, default=None)
    rating = models.FloatField(_("Rating"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.user) + str(self.id)




