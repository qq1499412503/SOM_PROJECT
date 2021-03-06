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
import os
from som.Form import UploadFileForm
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from minisom import MiniSom
from .ecsom import *
from numpy.linalg import norm
from numpy.testing import assert_almost_equal, assert_array_almost_equal
from numpy.testing import assert_array_equal


class SomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        username = "testt"
        email = "test1@email.com"
        password = "test1234"
        users = User.objects.create_user(username, email, password)
        users.save()
        logged_in = self.client.login(username=username, password=password)

    def test_pages_test_case(self):
        url = '/som/model'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualization0.1.html')

class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.code = 'api'
        username = "testt"
        email = "test1@email.com"
        password = "test1234"
        users = User.objects.create_user(username, email, password)
        users.save()
        logged_in = self.client.login(username=username, password=password)

    def test_userqueryinfo(self):
        url = reverse('som:som_model')
        response = self.client.get(url)
        csrf_token = response.cookies['csrftoken'].value
        fp = open('./som/animal.txt', "rb")

        myBytesIO = io.BytesIO(fp.read())
        myBytesIO.seek(0)
        txt = InMemoryUploadedFile(
            myBytesIO, None, 'random-name.txt', 'txt', len(myBytesIO.getvalue()), None
        )

        response1 = self.client.post(url, data={"csrfmiddlewaretoken": csrf_token, "data": txt})
        self.assertEqual(response1.status_code, 200)
        data_id = response1.context["data_id"]

        x = 5
        y = 5
        length = 100
        sigmas = 0.2
        lr = 0.01
        iteration = 200
        neighbour = "gaussian"
        topology = "rectangular"
        activation = "euclidean"
        randoms = 0.2
        dic = {"data_id":data_id,"x":x,"y":y,"length":length,"sigmas":sigmas,"lr":lr,"iteration":iteration,
               "topology":topology,"neighbour":neighbour,"activation":activation,"randoms":randoms}
        qdic = QueryDict.dict({str(dic):""})

        response2 = self.client.post('/som/user_query_info/', qdic)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("weight".encode('UTF-8'), response2.content)
        self.assertIn("label".encode('UTF-8'), response2.content)

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
                   "vis_name": vis_name, "description": description,"min_color":"white","max_color":"blue"}
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
                   "description": description,"min_color":"white","max_color":"blue"}
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
        username = "testt"
        email = "test1@email.com"
        password = "test1234"
        users = User.objects.create_user(username, email, password)
        users.save()
        logged_in = self.client.login(username=username, password=password)
        self.url = reverse('som:som_model')

    def test_views_som_model_get(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIn('file not uploaded'.encode('UTF-8'), response.content)
        self.assertIn('no attribute detected'.encode('UTF-8'), response.content)
        self.assertIn('empty_size'.encode('UTF-8'), response.content)

    def test_views_som_model_post(self):
        response1 = self.client.get(self.url)
        csrf_token = response1.cookies['csrftoken'].value
        fp = open('./som/animal.txt', "rb")

        myBytesIO = io.BytesIO(fp.read())
        myBytesIO.seek(0)
        txt = InMemoryUploadedFile(
            myBytesIO, None, 'random-name.txt', 'txt', len(myBytesIO.getvalue()), None
        )

        response = self.client.post(self.url, data={"csrfmiddlewaretoken": csrf_token, "data": txt})
        self.assertEqual(response.status_code, 200)
        try:
            data_id = response.context["data_id"]
            output_result = True
        except TypeError:
            print("fail to initialize data")
            output_result = False
        self.assertEqual(output_result, True)
        self.assertTemplateUsed(response, 'visualization0.1.html')


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


class TestSom(TestCase):
    def setUp(self):
        self.som = Mm(5, 5, 1)
        for i in range(5):
            for j in range(5):
                # checking weights normalization
                assert_almost_equal(1.0, norm(self.som._weights[i, j]))
        self.som._weights = np.zeros((5, 5, 1))  # fake weights
        self.som._weights[2, 3] = 5.0
        self.som._weights[1, 1] = 2.0

    def test_u_matrix(self):
        som = Mm(2, 2, 2, topology='hexagonal', random_seed=1)
        som._weights = np.array([[[1.,  0.], [0., 1.]], [[1., 0.], [0., 1.]]])
        # print(som.distance_map())
        arrays= np.array([[0. , 1. , 0. , 1.],[0. , 1. , 0. , 1.],[0. , 1. , 0. , 1.],[0. , 1. , 0. , 1.]])
        assert_array_equal(som.distance_map(), arrays)

    def test_u_matrix_with_avg_node(self):
        som = Mm(2, 2, 2, topology='hexagonal', random_seed=1)
        som._weights = np.array([[[1.,  0.], [0., 1.]], [[1., 0.], [0., 1.]]])
        distance_maps =  som.distance_map()
        u_matrix = som.avg_distance(distance_maps)
        # print(u_matrix)
        arrays= np.array([[4/6 , 1. , 4/6 , 1.],[0. , 1. , 0. , 1.],[4/6 , 1. , 4/6 , 1.],[0. , 1. , 0. , 1.]])
        assert_array_equal(u_matrix, arrays)



