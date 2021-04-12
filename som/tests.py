from django.test import TestCase
from django.test import Client


class SomTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_test_case(self):
        url = '/som/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # data = response.context['msg']
        # self.assertEqual(data,'yes')


# class ApiTestCase(TestCase):
#     def setUp(self):
#         self.code = 'api'
#
#     def test_sample_api_test_case(self):
#         url = '/som/user_query_info'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data['msg'], 'test')
