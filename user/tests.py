from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import UserInfo
from django.core.exceptions import ValidationError
from django.http import QueryDict
from som.models import dataframe
from bson.objectid import ObjectId
import datetime
# Create your tests here.




class Pagetest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_log_in_page(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        username = "test1"
        email = "test1@email.com"
        password = "test11234"
        response2 = self.client.post('/user/login/', {"username": username, "email": email , "password": password})
        try:
            user = User.objects.get(username=username)
            self.assertEqual(user.username, username)
            self.assertEqual(user.email, email)
            print(user.id)
        except User.DoesNotExist:
            self.assertRaises(ValidationError)
        self.assertEqual(response2.status_code, 200)



    def test_register_page(self):
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        username = "test"
        email = "test@email.com"
        password = "test1234"
        response2 = self.client.post('/user/register/',
                                     {"username": username, "email": email, "password": password})
        try:
            user = User.objects.get(username=username)
            self.assertEqual(user.username, username)
            self.assertEqual(user.email, email)
            print(user.id)
        except User.DoesNotExist:
            self.assertRaises(ValidationError)
        self.assertRedirects(response2, '/som/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class ApiTestCase(TestCase):
    def setUp(self):
        self.code = 'api'

    def test_sample_api_test_case(self):
        url = '/user/update_user/'
        try:
            username1 = "test1"
            email1 = "test1@email.com"
            password1 = "test1234"
            User.objects.create_user(username1, email1, password1)
            user = User.objects.get(username="test1")
            uid = user.id
            #print(uid)
            username = "test2"
            email = "test2@email.com"
            phone_number = "0426276721"
            DOB = str(datetime.datetime.now().date())
            user_info = UserInfo(user=user, DOB=datetime.datetime.now())
            user_info.save()
            dic = {"user_id": uid, "username": username, "email": email, "phone_number": phone_number, "DOB": DOB}
            qdic = QueryDict.dict({str(dic):""})
            # for key in qdic:
            #     print(key)
            #     print(eval(key))
            # print(qdic)
            response2 = self.client.post(url,qdic)
            data = response2.json()
            self.assertEqual(data['code'], '200')
            #confirm update
            user = User.objects.get(pk = uid)
            currentuser = UserInfo.objects.get(user=user)

            uname = user.username
            umail = user.email
            uphone = currentuser.phone_number
            uDOB = currentuser.DOB.date()
            self.assertEqual(uname, username)
            self.assertEqual(umail, email)
            self.assertEqual(uphone, phone_number)
            self.assertEqual(str(uDOB), DOB)
            self.assertEqual(response2.status_code, 200)
        except User.DoesNotExist:
            self.assertRaises(ValidationError)

class Login_Test(TestCase):

    def setUp(self):
        User.objects.create_user('admin','admin@email.com', 'admin123456')
        self.client = Client()

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@email.com")

    def test_login_action_username_password_null(self):
        test_data = {'username':'','password':'','email':'admin@email.com'}
        response = self.client.post('/user/login/', data = test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "164")

    def test_login_action_username_password_error(self):
        test_data = {'username':'spike', 'password':'123', 'email':'admin@email.com'}
        response = self.client.post('/user/login/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "164")

    def test_login_action_success(self):
        test_data ={'username':'admin', 'password':'admin123456', 'email':'admin@email.com'}
        response = self.client.post('/user/login/', test_data)
        self.assertEqual(response.status_code, 302)

class Register_Test(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@email.com', 'admin123456')
        self.client = Client()

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@email.com")

    def test_register_username_existed(self):
        test_data = {'username': 'admin','password': 'admin123456', 'email': 'username_existed@email.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "111")

    def test_register_username_error(self):
        test_data = {'username': '', 'password': 'admin123456', 'email': 'username_error@email.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "222")

    def test_register_email_existed(self):
        test_data = {'username': '123', 'password': 'admin123456', 'email': 'admin@email.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "333")

    def test_register_email_error(self):
        test_data = {'username': '123', 'password':'admin123456', 'email': ''}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "444")

    def test_register_password_error(self):
        test_data = {'username': '123', 'password': '', 'email': 'password_error@email.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["code"], "555")

    def test_register_success(self):
        test_data = {'username': 'test', 'password': 'admin123456', 'email': 'test@email.com'}
        response = self.client.post('/user/register/', data=test_data)
        self.assertEqual(response.status_code, 302)


class Profile_view_test(TestCase):

    def setUp(self):
        user = User.objects.create_user('admin', 'admin@email.com', 'admin123456')
        user.save()
        user_info = UserInfo(user=user, DOB=datetime.datetime.now())
        user_info.save()
        self.client = Client()

    def test_profile_view_get(self):
        response_login = self.client.post('/user/login/',{'email':"admin@email.com",'password':"admin123456"})
        response = self.client.get('/user/profile/')
        uid = User.objects.get(email = "admin@email.com").id
        data = dataframe.objects.filter(uid=uid).order_by('-time')[:5]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(list(data),list(response.context['data']))

    def test_profile_post_did(self):
        response_login = self.client.post('/user/login/',
                                          {'email': "admin@email.com", 'password': "admin123456"})
        dataframe.objects.create(file_name="som_1")
        data_id = ObjectId(dataframe.objects.get(file_name="som_1")._id)
        current_object = dataframe.objects.get(_id=data_id)
        file_name = current_object.file_name
        dic = {'did':data_id, 'name':file_name}
        response = self.client.post('/user/profile/',dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')
        self.assertIn('som_1'.encode('UTF-8'), response.content)

    def test_profile_post_pagen(self):
        response_login = self.client.post('/user/login/',
                                          {'email': "admin@email.com", 'password': "admin123456"})
        page = 0
        username = "test1"
        email = "test1@email.com"
        password = "test1234"
        User.objects.create_user(username, email, password)
        user = User.objects.get(username="test1")
        uid = user.id
        test_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
        for i in range(len(test_list)):
            author = "spike"+test_list[i]
            vis_name = "som_project1"+test_list[i]
            description = "this is a test"+test_list[i]
            dataframe.objects.create(file_name="som_1"+test_list[i])
            data_id = ObjectId(dataframe.objects.get(file_name="som_1"+test_list[i])._id)
            dic = {"user_id": uid, "data_id": data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})
            response2 = self.client.post('/som/save_map', qdic)

        #when len(data)>0
        data = dataframe.objects.filter(publish=False).order_by('-time')[(1 + page) * 5:(2 + page) * 5]

        dic = {"page_n":page,"data":data}
        response = self.client.post('/user/profile/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(list(data), list(response.context['data']))
        self.assertEqual(list(str(page+1)), list(response.context['page']))


    def test_profile_post_pagel(self):
        response_login = self.client.post('/user/login/',
                                          {'email': "admin@email.com", 'password': "admin123456"})
        page = 1
        username = "test1"
        email = "test1@email.com"
        password = "test1234"
        User.objects.create_user(username, email, password)
        user = User.objects.get(username="test1")
        uid = user.id
        test_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
        for i in range(len(test_list)):
            author = "spike"+test_list[i]
            vis_name = "som_project1"+test_list[i]
            description = "this is a test"+test_list[i]
            dataframe.objects.create(file_name="som_1"+test_list[i])
            data_id = ObjectId(dataframe.objects.get(file_name="som_1"+test_list[i])._id)
            dic = {"user_id": uid, "data_id": data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})
            response2 = self.client.post('/som/save_map', qdic)

        #when len(data)>0
        data = dataframe.objects.filter(publish=False).order_by('-time')[(page - 1) * 5:page * 5]

        dic = {"page_l":page,"data":data}
        response = self.client.post('/user/profile/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(list(str(page-1)), list(response.context['page']))

    # def test_profile_post_pagen_data_zero(self):
    #     page = 1
    #     data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
    #     dic = {"page_l": page, "data": data}
    #     response = self.client.post('/publish/list/', dic)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'publish.html')
    #     self.assertEqual(list(data), list(response.context['data']))
    #     self.assertEqual(list(str(page)), list(response.context['page']))

class Logout_test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logout_get(self):
        response = self.client.get('/user/logout')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')












