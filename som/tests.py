from django.test import TestCase
from .models import dataframe
from django.test import Client
from django.urls import reverse, resolve


class SomTestCase(TestCase):
    def setUp(self):
       self.client = Client()

    def test_pages_test_case(self):
        url = '/som/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def views_som_model_test(self):
    #     response = self.client.get(reverse('som:som_model'))
    #     self.assertEqual(response.status_code,200)
    #
    # def models_som_model_test(self):
    #     response = self.client.get('/som/user_query_info/')
    #     self.assertEqual(response.status_code, 405)



# class ApiTestCase(TestCase):
#     def setUp(self):
#         self.code = 'api'
#
#     def test_sample_api_test_case(self):
#         url = '/som/user_query_info/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data['msg'], 'test')

class ProjectTest(TestCase):
    def setUp(self) -> None:
        dataframe.objects.create(file_name="som_project")

    def test_create(self):
        dataframe.objects.create(file_name="som_1")
        d = dataframe.objects.get(file_name="som_1")
        self.assertEqual(d.file_name, "som_1")

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

class visualPagetest(TestCase):

    def test_visual_page_template(self):
        response = self.client.get('/som/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualization0.1.html')

class unknowntest(TestCase):
    def setUp(self) -> None:
        dataframe.objects.create(file_name="som_project")

    def test_create(self):
        dataframe.objects.create(file_name="som_1")
        d = dataframe.objects.get(file_name="som_1")
        self.assertEqual(d.file_name, "som_1")

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

class viewstest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_views_som_model(self):
        url = reverse('som:som_model')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

class sommodeltest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_models_som_model(self):
        url = '/som/user_query_info/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)


class sommodelviewtest(TestCase):
    def setUp(self) -> None:
        dataframe.objects.create(file_name="som_project")

    def test_create(self):
        dataframe.objects.create(file_name="som_1")
        d = dataframe.objects.get(file_name="som_1")
        self.assertEqual(d.file_name, "som_1")

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

class som_modelapitest(TestCase):
    def setUp(self) -> None:
        dataframe.objects.create(file_name="som_project")

    def test_create(self):
        dataframe.objects.create(file_name="som_1")
        d = dataframe.objects.get(file_name="som_1")
        self.assertEqual(d.file_name, "som_1")

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










