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
        data={"email":"jineshpaul89@gmail.com","password":"password@1234","phone_number":"9999999999"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:profiles_urls:register-user'),data=data,format='json')
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

class PasswordChangeTest(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.ChangePassword.as_view()
        user = models.User.objects.get(email='test@email.com')
        data={"old_password":"password@123","new_password":"password@1234"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:profiles_urls:change-password'),data=data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

class PasswordResetTest(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.ResetPassword.as_view()
        data={"email":"jineshpaul89@gmail.com"}
        request = factory.post(settings.BASE_URL+reverse('api_urls:profiles_urls:reset-password'),data=data)
        #force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

class PasswordResetConfirm_Test(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.password_reset_confirm.as_view()
        data = {}
        request = factory.post(settings.BASE_URL + reverse('api_urls:profiles_urls:reset-password'), data=data)


class AdditionalInfoAdd_Test(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.AdditionalInfo.as_view()
        user = models.User.objects.get(email='jineshpaul89@gmail.com')
        data = {'dob':'1989-09-14','gender':'M','marital_status':'M','address':{'pincode':'574234','address1':'BTM 2nd stage','address2':'',
                'city':'bangalore','district':'bangalore','state':'Karnataka','country':'India'}}
        request = factory.post(settings.BASE_URL + reverse('api_urls:profiles_urls:additional-info-add'), data=data,format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)


class AdditionalInfoGet_Test(APISimpleTestCase):
    allow_database_queries = True
    def test(self):
        factory = APIRequestFactory()
        view = views.AdditionalInfo.as_view()
        user = models.User.objects.get(email='jineshpaul89@gmail.com')
        request = factory.get(settings.BASE_URL + reverse('api_urls:profiles_urls:additional-info-get'))
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
