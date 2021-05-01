from django.test import TestCase, Client
from som.models import dataframe



class Publish_Test(TestCase):

    def setUp(self):
        self.client = Client()
        dataframe.objects.create(file_name="som_project", uid=1, description="this is a test", x=6, y=8)

    def test_publish_get(self):
        response = self.client.get('/publish/list/')
        data = dataframe.objects.filter(publish=True).order_by('-time')[:5]

        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'publish.html')
        # self.assertIn(b'som_project', response.content)
        # self.assertIn(b'this is a test', response.content)
        #self.assertIn('empty_size'.encode('UTF-8'), response.content)

    def test_publish_post(self):
        data = {'file_name':"som_project", 'uid':1, 'description':"this is a test", 'x':6, 'y':8}
        response = self.client.post('/publish/list/',data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')