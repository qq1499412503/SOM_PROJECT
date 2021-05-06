from django.test import TestCase
from django.contrib.auth.models import User
from user.models import UserInfo
import datetime
from django.test import Client
# Create your tests here.
class Redirect_test(TestCase):

    def setUp(self):
        user = User.objects.create_user('admin', 'admin@email.com', 'admin123456')
        user.save()
        user_info = UserInfo(user=user, DOB=datetime.datetime.now())
        user_info.save()
        self.client = Client()

    def test_redirect(self):
        response_login = self.client.post('/user/login/', {'email': "admin@email.com", 'password': "admin123456"})
        response = self.client.get('/publish/list')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')

    # def test_redirect_failed(self):
    #     response = self.client.get('/publish/list')
    #     self.assertEqual(response.status_code, 301)
    #     self.assertTemplateUsed(response, 'login.html')
