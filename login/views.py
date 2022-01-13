from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages

import homepage.views


def login_view(request):
    # if method is get, return static login webpage
    # if method is post, login the user, raise exception if the password is incorrect or user does not exist
    if request.method == 'GET':
        return render(request, 'login/login.html')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(homepage.views.homepage)
        else:
            # TODO: Instead of returning Http404, should pop out a warning instead
            raise Http404(username, password, "User does not exist or Password is wrong")


def logout_view(request):
    logout(request)
    return redirect(homepage.views.homepage)


def register_view(request):
    # if the method is get, return static register webpage
    # if the method is post, the user info is posted in the form, register it
    if request.method == 'GET':
        return render(request, 'login/register.html')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already in use')
            return render(request, 'login/register.html')
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        # login the user after register
        login(request, user)
        return redirect(homepage.views.homepage)

