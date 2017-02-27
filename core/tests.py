from django.test import TestCase

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APISimpleTestCase
from . import views,models
from django.conf import settings
from profiles import models as profile_model

# Create your tests here.

class MovieAdd_Test(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.Movie.as_view()
        user = profile_model.User.objects.get(email='jineshpaul89@gmail.com')
        data={"title":"Da Vinchi Code","movie_id":"2"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:core_urls:movie-add'),data=data,format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)


class CastAdd_Test(APISimpleTestCase):
    allow_database_queries = True

    def test(self):
        factory = APIRequestFactory()
        view = views.Cast.as_view()
        user = profile_model.User.objects.get(email='jineshpaul89@gmail.com')
        data = {'cast':[{'real_name':'Jack Paul','role_name':'J Paul','email':'jackui@gmail.com','phone_number':'9986729888'}],'movie':'2','cast_id':'2'}
        request = factory.post(settings.BASE_URL + reverse('api_urls:core_urls:cast-add'), data=data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

class CastGet_Test(APISimpleTestCase):
    allow_database_queries = True

    def test(self):
        factory = APIRequestFactory()
        view = views.Cast.as_view()
        user = profile_model.User.objects.get(email='jineshpaul89@gmail.com')
        data = {'movie':'2'}
        request = factory.get(settings.BASE_URL + reverse('api_urls:core_urls:cast-get'), data=data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

