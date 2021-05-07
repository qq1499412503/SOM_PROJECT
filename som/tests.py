from django.test import TestCase
from .models import dataframe
from .som_model import Som, load_data
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import QueryDict
from bson.objectid import ObjectId
import numpy as np




class SomTestCase(TestCase):
    def setUp(self):
       self.client = Client()

    def test_pages_test_case(self):
        url = '/som/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualization0.1.html')

class ApiTestCase(TestCase):
    def setUp(self):
        self.code = 'api'


        # data1 = [[0.80, 0.55, 0.22, 0.03],
        #         [0.82, 0.50, 0.23, 0.03],
        #         [0.80, 0.54, 0.22, 0.03],
        #         [0.80, 0.53, 0.26, 0.03],
        #         [0.79, 0.56, 0.22, 0.03],
        #         [0.75, 0.60, 0.25, 0.03],
        #         [0.77, 0.59, 0.22, 0.03],
        #         [0.1, 0.2, 0.3, 0.01]]
        # data = np.array(data1)
    # def test_sample_api_test_case(self):
    #     url = '/som/user_query_info'
    #     with open('som_model.py') as fp:
    #         response = self.client.post(url, { 'df': fp})
    #         self.assertEqual(response.status_code,200)

        # x = 5
        # y = 5
        # length = 100
        # sigmas = 0.2
        # lr = 0.01
        # iteration = 200
        # neighbour = "gaussian"
        # topology = "rectangular"
        # activation = "euclidean"
        # randoms = 0.2
        #
        # dic = {"data_id": data_id, "x": x, "y": y, "length": length,
        #        "sigmas": sigmas, "lr": lr,"iteration":iteration, "neighbour": neighbour,
        #        "topology":topology, "activation":activation , "randoms":randoms , "data":df}
        # qdic = QueryDict.dict({str(dic): ""})
        #
        # response = self.client.post(url, qdic)
        # data = response.json()
        # self.assertEqual(data['code'], '200')
        # self.assertEqual(data['msg'], 'successful')

    def test_save_map(self):
        url = '/som/save_map'
        try:
            username = "test1"
            email = "test1@email.com"
            password = "test1234"
            User.objects.create_user(username, email, password)
            user = User.objects.get(username="test1")
            uid = user.id

            dataframe.objects.create(file_name="som_1")
            data_id = ObjectId(dataframe.objects.get(file_name="som_1")._id)
            author = "spike"
            vis_name = "som_project1"
            description = "this is a test"
            dic = {"user_id": uid,"data_id":data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})

            response = self.client.post(url, qdic)
            data = response.json()
            self.assertEqual(data['code'], '200')
            self.assertEqual(data['msg'], 'successful')
            # confirm update
            user = User.objects.get(pk=uid)
            current_object = dataframe.objects.get(_id=data_id)

            user_id = user.id
            uauthor = current_object.author
            uvis_name = current_object.file_name
            udescription = current_object.description

            self.assertEqual(user_id, uid)
            self.assertEqual(uauthor, author)
            self.assertEqual(uvis_name, vis_name)
            self.assertEqual(udescription, description)
            self.assertEqual(response.status_code, 200)
        except User.DoesNotExist:
            self.assertRaises(ValidationError)

    def test_save_and_publish(self):
        url = '/som/save_and_publish'
        try:
            username = "test1"
            email = "test1@email.com"
            password = "test1234"
            User.objects.create_user(username, email, password)
            user = User.objects.get(username="test1")
            uid = user.id

            dataframe.objects.create(file_name="som_1")
            data_id = ObjectId(dataframe.objects.get(file_name="som_1")._id)

            author = "spike"
            vis_name = "som_project1"
            description = "this is a test"
            dic = {"user_id": uid, "data_id": data_id,
                   "author": author, "vis_name": vis_name,
                   "description": description}
            qdic = QueryDict.dict({str(dic): ""})

            response = self.client.post(url, qdic)
            data = response.json()
            self.assertEqual(data['code'], '200')
            self.assertEqual(data['msg'], 'successful')

            # confirm update
            user = User.objects.get(pk=uid)
            current_object = dataframe.objects.get(_id=data_id)

            user_id = user.id
            uauthor = current_object.author
            uvis_name = current_object.file_name
            udescription = current_object.description

            response2 = self.client.get('/publish/list/')
            self.assertIn('spike'.encode('UTF-8'), response2.content)
            self.assertIn('som_project1'.encode('UTF-8'), response2.content)
            self.assertIn('this is a test'.encode('UTF-8'),response2.content)

            self.assertEqual(user_id, uid)
            self.assertEqual(uauthor, author)
            self.assertEqual(uvis_name, vis_name)
            self.assertEqual(udescription, description)
            self.assertEqual(response.status_code, 200)
        except User.DoesNotExist:
            self.assertRaises(ValidationError)


class ProjectTest(TestCase):
    def setUp(self) -> None:
        dataframe.objects.create(file_name="som_project")

    def test_create(self):
        dataframe.objects.create(file_name="som_1", author = "spike", uid = 2, description= "this is a test",x = 5, y= 8)
        d = dataframe.objects.get(file_name="som_1")
        self.assertEqual(d.file_name, "som_1")
        self.assertEqual(d.author, "spike")
        self.assertEqual(d.uid, 2)
        self.assertEqual(d.description, "this is a test")
        self.assertEqual(d.x, 5)
        self.assertEqual(d.y, 8)

    def test_delete(self):
        d = dataframe.objects.get(file_name="som_project")
        d.delete()
        result = dataframe.objects.filter(file_name="som_project")
        self.assertEqual(len(result),0)

    def test_updata(self):
        d = dataframe.objects.get(file_name="som_project")
        d.file_name = "som_update"
        d.save()
        result = dataframe.objects.get(file_name="som_update")
        self.assertEqual(result.file_name, "som_update")

class Views_som_model_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('som:som_model')

    def test_views_som_model_get(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIn('file not uploaded'.encode('UTF-8'), response.content)
        self.assertIn('no attribute detected'.encode('UTF-8'), response.content)
        self.assertIn('empty_size'.encode('UTF-8'), response.content)

    def test_views_som_model_post(self):
        test_data = {'name': 'somtest1', "attribute": "100", "size": "2000"}
        response = self.client.post(self.url, data = test_data)
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'upload.html')

class Test_test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get('/som/test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visual.html')

class TT_test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get('/som/tt')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test.html')










