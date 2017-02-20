from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models as internal_models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from . import models
from django.http import HttpResponse
import os
from rangefilter.filter import DateRangeFilter

# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    """
    to achieve:
    1. Changing User Phone number or email id
    2. To add remarks against a user
    3. Be able to trigger a email id verification from admin panel
    4. Showing total online users at a time
    """
    formfield_overrides = {
        internal_models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        internal_models.EmailField: {'widget': TextInput(attrs={'size': '17'})},
        internal_models.TextField: {'widget': Textarea(attrs={'rows': '2', 'cols': '40'})},
    }
    search_fields = ['title']
    list_display = ['id', 'user', 'title','description','created_at']
    list_editable = ['title']
    empty_value_display = 'unknown'


class ReviewAdmin(admin.ModelAdmin):
    """
    to achieve:
    1. Changing User Phone number or email id
    2. To add remarks against a user
    3. Be able to trigger a email id verification from admin panel
    4. Showing total online users at a time
    """
    formfield_overrides = {
        internal_models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        internal_models.EmailField: {'widget': TextInput(attrs={'size': '17'})},
        internal_models.TextField: {'widget': Textarea(attrs={'rows': '2', 'cols': '40'})},
    }
    search_fields = ['user','movie']
    list_display = ['id', 'user', 'movie','review','created_at']
    list_editable = ['review']
    empty_value_display = 'unknown'


class RatingAdmin(admin.ModelAdmin):
    """
    to achieve:
    1. Changing User Phone number or email id
    2. To add remarks against a user
    3. Be able to trigger a email id verification from admin panel
    4. Showing total online users at a time
    """
    formfield_overrides = {
        internal_models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        internal_models.EmailField: {'widget': TextInput(attrs={'size': '17'})},
        internal_models.TextField: {'widget': Textarea(attrs={'rows': '2', 'cols': '40'})},
    }
    search_fields = ['user','movie']
    list_display = ['id', 'user', 'movie','rating','created_at']
    list_editable = ['rating']
    empty_value_display = 'unknown'



admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Rating, RatingAdmin)
