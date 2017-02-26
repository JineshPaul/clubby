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
    Store the Movie information
    """
    CATEGORY_CHOICES = (
        ('D', 'Drama'),
        ('A', 'Action'),
        ('T', 'Thriller'),
        ('F', 'Fantacy'),
        ('C' , 'Animation')
         )

    user = models.ForeignKey(profile_models.User)
    movie = models.FileField(upload_to="movies/", max_length=700, blank=True, null=True)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, blank=True, null=True)
    title = models.CharField(_('Title '), max_length=254, blank=False, null=False)
    description = models.TextField(_("Description"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.title)


class Review(TimeStampedModel):
    """
    Store the portfolio information
    """
    user = models.ForeignKey(profile_models.User)
    movie = models.ForeignKey(Movie,null=True, blank=True, default=None)
    review = models.TextField(_("Review"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.movie) + str(self.id)


class Rating(TimeStampedModel):
    """
    Store the portfolio information
    """
    user = models.ForeignKey(profile_models.User)
    movie = models.ForeignKey(Movie,null=True, blank=True, default=None)
    rating = models.FloatField(_("Rating"), null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return str(self.movie) + str(self.id)


class Cast(models.Model):
    movie = models.ForeignKey(Movie)
    role_name = models.CharField(_('Cast Name '), max_length=254, blank=False, null=False)
    real_name = models.CharField(_('Real name '), max_length=254, blank=False, null=False)

    def __str__(self):
        return str(self.movie) + str(self.real_name)





