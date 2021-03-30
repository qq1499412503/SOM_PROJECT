from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


def som_model(request):
    if request.method == "GET":
        content = {'msg': 'yes'}
        return render(request, 'som_model.html', content)



class sample_api(APIView):
    def get(self, request, *args, **kwargs):
        # request.query_params.get('code', ',')
        return Response({
            'msg': 'test'
        })


