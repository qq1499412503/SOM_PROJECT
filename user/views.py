from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.


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
            return {"code": "222", "msg": "username existed"}
        except User.DoesNotExist:
            pass
    else:
        return {"code": "111", "msg": "username error or username existed"}
    if email != '' and email is not None and email.includes('@') and email.includes('.'):
        try:
            user = User.objects.get(email=email)
            return {"code": "222", "msg": "email existed"}
        except User.DoesNotExist:
            pass
    else:
        return {"code": "111", "msg": "email error or email existed"}
    if password != '' and password is not None and len(password) >= 8:
        pass
    else:
        return {"code": "111", "msg": "password error"}
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
            login(request, user)
            return redirect('/som/')
        else:
            content = {"msg": "username or password incorrect"}
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
            return render(request, 'visualization0.1.html')
        else:
            return render(request, 'register.html', verify)
