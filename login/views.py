from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def loginpage(request):
    return render(request, "login.html", locals())


@require_POST
def userin(request):
    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        check = True
    else:
        check = False
    return JsonResponse({"check": check})


@require_POST
def adduser(request):
    username = request.POST['login']
    password = request.POST['password']
    password_rep = request.POST['password_rep']
    fails = ""
    flag = True
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        flag = False

    if flag:
        fails += "Этот логин уже используется<br>"
    if len(username) < 3:
        fails += "Логин минимум - 3 символа<br>"
    if len(password) < 5:
        fails += "Пароль минимум - 5 символов<br>"
    if password != password_rep:
        fails += "Пароли не совпадают<br>"

    if fails == "":
        user2 = User.objects.create_user(username=username, password=password)
        user2.save()
        fails = True

    return JsonResponse({"fails": fails})


@login_required
def userout(request):
    logout(request)
    return redirect('/')
