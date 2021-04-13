from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .Form import UploadFileForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# Create your views here.


def som_model(request):
    if request.method == "GET":
        content = {'msg': 'yes'}
        return render(request, 'visualization0.1.html', content)



class sample_api(APIView):
    def get(self, request, *args, **kwargs):
        # request.query_params.get('code', ',')
        return Response({
            'msg': 'test'
        })


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            #return HttpResponseRedirect('/som')
        else:
            print(request.FILES)
            return HttpResponse('true')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    print(f.chunks())
    with open('test1.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            print('true write')

def vis(request):
    if request.method == "GET":
        return render(request, 'vis.html')