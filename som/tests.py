from django.test import TestCase
from .models import dataframe
from .som_model import Som
from django.test import Client
from django.urls import reverse, resolve



class SomTestCase(TestCase):
    def setUp(self):
       self.client = Client()

    def test_pages_test_case(self):
        url = '/som/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualization0.1.html')

# class ApiTestCase(TestCase):
#     def setUp(self):
#         self.code = 'api'
#
#     def test_sample_api_test_case(self):
#         url = '/som/user_query_info/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 405)
#         data = response.json()
#         self.assertEqual(data['test'], 'test')

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

    def test_logout_get(self):
        response = self.client.get('/som/test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visual.html')

class TT_test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logout_get(self):
        response = self.client.get('/som/tt')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test.html')










