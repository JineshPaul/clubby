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


def index(request):
    """
    :param request:
    :return:
    """
    return render(request, 'base/index.html')


class Movie(APIView):
    """
    Add Movie and Get Movie information
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        """
        :param request:
        :return:
        """

    def post(self,request):
        """
        :param request:
        :return:
        """
        serializer = serializers.MovieSerializer(data=request.data)
        if serializer.is_valid():
            try:
                movie = models.Movie.objects.get(user=request.user,pk=request.data.get("movie_id"))
                movie.movie = request.FILES.get("movie",None)
                movie.title = serializer.validated_data.get("title")
                movie.category = serializer.validated_data.get("category")
                movie.description = serializer.validated_data.get("description")
                movie.save()
                return api_utils.response({"message": constants.SUCCESS})
            except:
                movie = models.Movie.objects.create(user=request.user,
                                            title = serializer.validated_data.get("title"),
                                            category = serializer.validated_data.get("category"),
                                            description = serializer.validated_data.get("description")
                                            )
                movie.movie = request.FILES.get("movie",None)
                movie.save()

                return api_utils.response({"message": constants.SUCCESS})
        return api_utils.response({}, status.HTTP_400_BAD_REQUEST, api_utils.generate_error_message(serializer.errors))


class DeleteMovie(APIView):
    """
    Delete Movie
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        """
        param: movie id
        """
        try:
             movie = models.Movie.objects.get(pk=request.data.get("movie_id"))
             movie.delete()
             return api_utils.response({"message": constants.SUCCESS})
        except:
            return api_utils.response({}, status.HTTP_400_BAD_REQUEST, "Movie Not found in server")