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
from matplotlib import cm, colorbar
import matplotlib


class QueryUserInfo(APIView):

    def post(self, request):
        # print('keydict')
        for key in request.POST:
            keydict = eval(key)
            # print(keydict)
            data_id = ObjectId(str(keydict["data_id"]))
            current_object = dataframe.objects.get(_id=data_id)
            df, lb = load_data(current_object.data)
            models = Som()
            models.read_data(df)
            models.read_label(lb)
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
            current_object.map = results
            current_object.x = x
            current_object.y = y
            current_object.save()
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



def test(request):
    if request.method == "GET":
        return render(request, 'visual.html')


def tt(request):
    if request.method == "GET":
        return render(request, 'test.html')




class SaveMap(APIView):

    def post(self, request):
        for key in request.POST:
            keydict = eval(key)
            uid = str(keydict["user_id"])
            data_id = ObjectId(str(keydict["data_id"]))
            author = str(keydict["author"])
            vis_name = str(keydict["vis_name"])
            description = str(keydict["description"])
            current_object = dataframe.objects.get(_id=data_id)
            current_object.uid = uid
            current_object.author = author
            current_object.description = description
            current_object.file_name = vis_name
            current_object.save()
            results = {"code":"200","msg":"successful"}
        return JsonResponse(results, safe=False)

    #@csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SaveMap, self).dispatch(*args, **kwargs)

class SaveAndPublish(APIView):

    def post(self, request):
        for key in request.POST:
            keydict = eval(key)
            uid = str(keydict["user_id"])
            data_id = ObjectId(str(keydict["data_id"]))
            author = str(keydict["author"])
            vis_name = str(keydict["vis_name"])
            description = str(keydict["description"])
            current_object = dataframe.objects.get(_id=data_id)
            current_object.uid = uid
            current_object.author = author
            current_object.description = description
            current_object.file_name = vis_name
            current_object.publish = True
            current_object.save()
            results = {"code":"200","msg":"successful"}
        return JsonResponse(results, safe=False)

    #@csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SaveAndPublish, self).dispatch(*args, **kwargs)

class ChangeColor(APIView):

    def post(self, request):
        for key in request.POST:
            keydict = eval(key)
            # print(request.POST['color'])
            print(len(keydict['nodes'][0]))
            color = []
            for i in range(len(keydict['nodes'])):
                sub_color = []
                for j in range(len(keydict['nodes'][0])):
                    if i % 2 == 0 and j % 2 == 0:
                        sub_color.append('#B8B8B8')
                    else:
                        if keydict['color'] == 'blue':
                            nc = cm.Blues(keydict['color_value'][i][j])
                        elif keydict['color'] == 'red':
                            nc = cm.Reds(keydict['color_value'][i][j])
                        elif keydict['color'] == 'green':
                            nc = cm.Greens(keydict['color_value'][i][j])
                        elif keydict['color'] == 'blue to red':
                            if keydict['color_value'][i][j] >= 0.5:
                                new_val = (keydict['color_value'][i][j]-0.5)/0.5
                                nc = cm.Reds(new_val)
                            else:
                                new_val = (0.5-keydict['color_value'][i][j])/0.5
                                nc = cm.Blues(new_val)

                        new_color = matplotlib.colors.rgb2hex(nc)
                        sub_color.append(new_color)

                color.append(sub_color)
            keydict['nodes'] = color

        return JsonResponse(keydict, safe=False)

    # @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ChangeColor, self).dispatch(*args, **kwargs)