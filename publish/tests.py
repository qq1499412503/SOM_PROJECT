from django.test import TestCase, Client
from bson.objectid import ObjectId
from som.models import dataframe




class Publish_Test(TestCase):

    def setUp(self):
        self.client = Client()
        dataframe.objects.create(file_name="som_project",
                                 uid=1, description="this is a test", x=6, y=8)

    def test_publish_get(self):
        response = self.client.get('/publish/list/')
        data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')
        self.assertEqual(list(data), list(response.context['data']))

    def test_publish_post(self):
        dataframe.objects.create(file_name="som_1")
        data_id = ObjectId(dataframe.objects.create(file_name="som_1")._id)
        current_object = dataframe.objects.get(_id=data_id)
        file_name = current_object.file_name
        dic = {'did': data_id, 'name': file_name}
        response = self.client.post('/publish/list/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')
        self.assertIn('som_1'.encode('UTF-8'), response.content)


# try
        # except userdoesnotexsited