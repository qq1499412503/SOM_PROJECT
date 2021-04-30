from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404




# Create your views here.
def redirect_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/publish/list')
        else:
            return redirect('/user/login')
