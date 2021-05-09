from django.test import TestCase
from django.contrib.auth.models import User
from user.models import UserInfo
import datetime
from django.test import Client
from django.urls import reverse, resolve
from . import views
# Create your tests here.
class Redirect_test(TestCase):

    def setUp(self):
        user = User.objects.create_user('admin', 'admin@email.com', 'admin123456')
        user.save()
        user_info = UserInfo(user=user, DOB=datetime.datetime.now())
        user_info.save()
        self.client = Client()

    def test_redirect_return_to_publish(self):
        response_login = self.client.post('/user/login/', {'email': "admin@email.com", 'password': "admin123456"})
        url = reverse('redirect:redirect')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/publish/list')

    def test_redirect_return_to_login(self):
        url = reverse('redirect:redirect')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login')
