from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .Form import UploadFileForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .som_model import load_data, print_attribute, Som
from bson.objectid import ObjectId
from .models import dataframe
import time
import json


class QueryUserInfo(APIView):

    def post(self, request):
        # print('keydict')
        for key in request.POST:
            keydict = eval(key)
            # print(keydict)
            data_id = ObjectId(str(keydict["data_id"]))
            current_object = dataframe.objects.get(_id=data_id)
            df = load_data(current_object.data)
            models = Som()
            models.read_data(df)
            # print(models.data)
            try:
                x = int(keydict["x"])
                models.x = x
            except:
                x = 1
                models.x = x
            try:
                y = int(keydict["y"])
                models.y = y
            except:
                y = 1
                models.y = y
            try:
                length = int(keydict["len"])
                models.input_len = length
            except:
                models.load_length()
            try:
                sigmas = float(keydict["sigmas"])
                models.sigma = sigmas
            except:
                pass
            try:
                lr = float(keydict["lr"])
                models.lr = lr
            except:
                pass
            try:
                iteration = int(keydict["iteration"])
            except:
                iteration = 100
            neighbour = str(keydict["neighbour"])
            models.neighborhood_function = neighbour
            topology = str(keydict["topology"])
            models.topology = topology
            activation = str(keydict["activation"])
            models.activation_distance = activation
            try:
                randoms = float(keydict["random"])
                models.random_seed = randoms
            except:
                pass
            models.model()
            models.fit(iteration)
            results = models.process_map()
        return JsonResponse(results, safe=False)

    #@csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(QueryUserInfo, self).dispatch(*args, **kwargs)


def som_model(request):
    if request.method == "GET":
        content = {'name': 'file not uploaded', "attribute": "no attribute detected", "size": "empty_size"}
        return render(request, 'visualization0.1.html', content)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            saved_data = form.save()
            f_name = str(request.FILES['data'])
            data_info = print_attribute(saved_data.data)
            content = {"name": f_name, "attribute": data_info[0], "size": data_info[1], "data_id": str(saved_data._id)}
            # request.session["data_id"] = str(saved_data._id)

            return render(request, 'visualization0.1.html', content)
        else:
            return render(request, 'visualization0.1.html', {"upload_msg": "not valid file"})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})











