from django.test import TestCase

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APISimpleTestCase
from . import views,models
from django.conf import settings

# Create your tests here.


class RegisterTest(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.Register.as_view()
        data={"email":"test4@email.com","password":"password@1234","phone_number":"9000000004"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:profiles_urls:register-user'),data=data)
        #force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)


class UserInfoTest(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.UserInfo.as_view()
        data={}
        user = models.User.objects.get(email='test@email.com')
        request = factory.get(settings.BASE_URL+reverse('api_urls:profiles_urls:user-info'),data=data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)


class LoginTest(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.Login.as_view()
        data={"username":"test@email.com","password":"password@1234"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:profiles_urls:login-user'),data=data)
        #force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)