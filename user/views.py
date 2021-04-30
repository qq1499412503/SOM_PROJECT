from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from .models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
from som.models import dataframe
from bson.objectid import ObjectId
import json
# Create your views here.




class UpdateUser(APIView):

    def post(self, request):
        print(request.POST)
        for key in request.POST:
            keydict = eval(key)
            uid = keydict["user_id"]
            username = keydict["username"]
            email = keydict["email"]
            phone_number = keydict["phone_number"]
            DOB = datetime.strptime(keydict["DOB"], '%Y-%m-%d').replace(tzinfo=timezone.utc)
            user = User.objects.get(pk=uid)
            user.username = username
            user.email = email
            user.save()
            user_ob = User.objects.get(pk=uid)
            current_user = UserInfo.objects.get(user=user_ob)
            current_user.phone_number = phone_number
            current_user.DOB = DOB
            current_user.save()
            return JsonResponse({"code": "200", "msg": "success"}, safe=False)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UpdateUser, self).dispatch(*args, **kwargs)

class UpdatePasswd(APIView):

    def post(self, request):
        for key in request.POST:
            keydict = eval(key)
            uid = keydict["user_id"]
            p1 = str(keydict["passwd1"])
            p2 = str(keydict["passwd2"])
            if p1 == p2 and p1 != '' and p2 != '' and p1 is not None and p2 is not None:
                user = User.objects.get(pk=uid)
                user.set_password(p1)
                user.save()
                return JsonResponse({"code": "200", "msg": "password successful changed, please login again"}, safe=False)
            else:
                return JsonResponse({"code": "211", "msg": "password can not be none or different"}, safe=False)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UpdatePasswd, self).dispatch(*args, **kwargs)

def get_user(email):
    try:
        user = User.objects.get(email=email)
        print(user.username)
        return user.username
    except User.DoesNotExist:
        return None


def check_error_register(username, email, password):
    if username != '' and username is not None:
        try:
            user = User.objects.get(username=username)
            return {"code": "111", "msg": "username existed"}
        except User.DoesNotExist:
            pass
    else:
        return {"code": "222", "msg": "username error or username existed"}
    if email != '' and email is not None:
        try:
            user = User.objects.get(email=email)
            return {"code": "333", "msg": "email existed"}
        except User.DoesNotExist:
            pass
    else:
        return {"code": "444", "msg": "email error or email existed"}
    if password != '' and password is not None and len(password) >= 8:
        pass
    else:
        return {"code": "555", "msg": "password error"}
    return {"code": "200", "msg": "all correct"}


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = get_user(request.POST['email'])
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('yes')
            login(request, user)

            return redirect('/som/')
        else:
            content = {"code":"164" ,"msg": "username or password incorrect"}
            return render(request, 'login.html', content)


def register_view(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        verify = check_error_register(username, email, password)
        if verify["code"] == "200":
            user = User.objects.create_user(username, email, password)
            user.save()
            user_info = UserInfo(user=user,DOB=datetime.now())
            user_info.save()
            return redirect('/som/')
        else:
            return render(request, 'register.html', verify)


def profile_view(request):
    if request.user.is_authenticated:
        uid = request.user.id
        user_ob = User.objects.get(pk=uid)
        current_user = UserInfo.objects.get(user=user_ob)
    else:
        raise Http404
    if request.method == "GET":
        data = dataframe.objects.filter(uid=uid).order_by('-time')[:5]
        # for a in data:
            # print(a._id,a.file_name,a.author,a.description)
        content = {"UID": uid, "username": request.user.username, "mail_address": request.user.email, "phone_number": current_user.phone_number , "DOB":current_user.DOB.strftime('%Y-%m-%d'), "data":data}
        return render(request, 'profile.html', content)
    if request.method == "POST":
        data_id = ObjectId(str(request.POST['did']))
        current_object = dataframe.objects.get(_id=data_id)
        file_name = current_object.file_name
        author = current_object.author
        time = current_object.time
        description = current_object.description
        publish = current_object.publish
        data_name = str(current_object.data).split('/')[-1]
        map = json.dumps(dict(current_object.map))
        x = current_object.x
        y = current_object.y
        content = {'did':data_id, 'name':file_name, 'Author':author, 'Date':time, 'Description':description, 'Publish':publish, 'map':map, 'Data_file':data_name, 'x':x,'y':y }
        return render(request, 'view.html', content)


def logout_view(request):
    logout(request)
    return render(request, 'login.html')
