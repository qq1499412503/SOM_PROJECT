from django.shortcuts import render

# Create your views here.


def publish_view(request):
    if request.method == "GET":
        return render(request, 'publish.html')


def view_view(request):
    if request.method == "GET":
        return render(request, 'view.html')