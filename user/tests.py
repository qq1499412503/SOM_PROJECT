from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, resolve
# Create your tests here.


class Pagetest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_log_in_page(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_page(self):
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

class Login_Test(TestCase):

    def setUp(self):
        User.objects.create_user('admin','admin@email.com', 'admin123456')

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@email.com")

    def test_login_action_username_password_null(self):
        test_data = {'username':'','password':'','email':''}
        response = self.client.post('/user/login/', data = test_data)
        self.assertEqual(response.status_code, 200)

    def test_login_action_username_password_error(self):
        test_data = {'username':'abc', 'password':'123', 'email':'123@163.com'}
        response = self.client.post('/user/login/', data=test_data)
        self.assertEqual(response.status_code, 200)

    def test_login_action_success(self):
        test_data ={'username':'admin', 'password':'admin123456', 'email':'admin@email.com'}
        response = self.client.post('/user/login/', data = test_data)
        self.assertEqual(response.status_code, 302)


class Register_Test(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@email.com', 'admin123456')

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@email.com")

    def test_register_action_username_password_null(self):
        test_data = {'username': '', 'password': '', 'email': ''}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response)

    def test_register_action_username_password_error(self):
        test_data = {'username': 'abc', 'password': '123', 'email': '123@163.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response)
        self.assertNotIn('abc'.encode('UTF-8'), response.content)

    def test_register_action_success(self):
        test_data = {'username': 'admin', 'password': 'admin123456', 'email': 'admin@email.com'}
        response = self.client.post(path = '/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response)
#
# class userupdate(TestCase):
#
#     def sutUp:





