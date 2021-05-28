from django.test import TestCase, Client
from bson.objectid import ObjectId
from som.models import dataframe
from django.contrib.auth.models import User
from django.http import QueryDict
from bson.objectid import ObjectId






class Publish_Test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_publish_get(self):
        #insert one data
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
        dic = {"user_id": uid, "data_id": data_id, "author": author,
               "vis_name": vis_name, "description": description}
        qdic = QueryDict.dict({str(dic): ""})
        response2 = self.client.post('/som/save_and_publish', qdic)

        data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
        response = self.client.get('/publish/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')
        self.assertEqual(list(data), list(response.context['data']))

    def test_publish_post_did(self):
        dataframe.objects.create(file_name="som_1")
        data_id = ObjectId(dataframe.objects.get(file_name="som_1")._id)
        current_object = dataframe.objects.get(_id=data_id)
        file_name = current_object.file_name
        dic = {'did': data_id, 'name': file_name}
        response = self.client.post('/publish/list/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html.bak')
        self.assertIn('som_1'.encode('UTF-8'), response.content)

    def test_publish_post_pagen(self):
        page = 0
        username = "test1"
        email = "test1@email.com"
        password = "test1234"
        User.objects.create_user(username, email, password)
        user = User.objects.get(username="test1")
        uid = user.id
        test_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]
        for i in range(len(test_list)):
            author = "spike"+test_list[i]
            vis_name = "som_project1"+test_list[i]
            description = "this is a test"+test_list[i]
            dataframe.objects.create(file_name="som_1"+test_list[i])
            data_id = ObjectId(dataframe.objects.get(file_name="som_1"+test_list[i])._id)
            dic = {"user_id": uid, "data_id": data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})
            response2 = self.client.post('/som/save_and_publish', qdic)

        #when len(data)>0
        data = dataframe.objects.filter(publish=True).order_by('-time')[(1 + page) * 5:(2 + page) * 5]

        dic = {"page_n":page,"data":data}
        response = self.client.post('/publish/list/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')
        self.assertEqual(list(data), list(response.context['data']))
        self.assertEqual(list(str(page+1)), list(response.context['page']))


    def test_publish_post_pagel(self):
        page = 1
        username = "test1"
        email = "test1@email.com"
        password = "test1234"
        User.objects.create_user(username, email, password)
        user = User.objects.get(username="test1")
        uid = user.id
        test_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
                     "19", "20","21"]
        for i in range(len(test_list)):
            author = "spike" + test_list[i]
            vis_name = "som_project1" + test_list[i]
            description = "this is a test" + test_list[i]
            dataframe.objects.create(file_name="som_1" + test_list[i])
            data_id = ObjectId(dataframe.objects.get(file_name="som_1" + test_list[i])._id)
            dic = {"user_id": uid, "data_id": data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})
            response2 = self.client.post('/som/save_and_publish', qdic)

        # when len(data)>0
        data = dataframe.objects.filter(publish=True).order_by('-time')[(page-1)*5:page*5]

        dic = {"page_l": page, "data": data}
        response = self.client.post('/publish/list/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')
        self.assertEqual(list(data), list(response.context['data']))
        self.assertEqual(list(str(page - 1)), list(response.context['page']))

    def test_pagen_data_equal_to_zero(self):
        page = 4
        username = "test1"
        email = "test1@email.com"
        password = "test1234"
        User.objects.create_user(username, email, password)
        user = User.objects.get(username="test1")
        uid = user.id
        test_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
                     "19", "20","21"]
        for i in range(len(test_list)):
            author = "spike" + test_list[i]
            vis_name = "som_project1" + test_list[i]
            description = "this is a test" + test_list[i]
            dataframe.objects.create(file_name="som_1" + test_list[i])
            data_id = ObjectId(dataframe.objects.get(file_name="som_1" + test_list[i])._id)
            dic = {"user_id": uid, "data_id": data_id, "author": author,
                   "vis_name": vis_name, "description": description}
            qdic = QueryDict.dict({str(dic): ""})
            response2 = self.client.post('/som/save_and_publish', qdic)

        # when len(data)>0
        data = dataframe.objects.filter(publish=True).order_by('-time')[page * 5:(1 + page) * 5]

        dic = {"page_n": page, "data": data}
        response = self.client.post('/publish/list/', dic)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish.html')
        self.assertEqual(list(data), list(response.context['data']))
        self.assertEqual(list(str(page)), list(response.context['page']))

    # def test_pagel_data_equal_to_zero(self):
    #     page = 0
    #     data = dataframe.objects.filter(publish=True).order_by('-time')[:5]
    #     dic = {"page_l": page, "data": data}
    #     response = self.client.post('/publish/list/', dic)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'publish.html')
    #     self.assertEqual(list(data), list(response.context['data']))
    #     self.assertEqual(list(str(page)), list(response.context['page']))
