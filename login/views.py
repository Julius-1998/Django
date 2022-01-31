from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User
from django.http import Http404
from django.contrib import messages

import homepage.views
from driver.models import Driver


def login_view(request):
    # if method is get, return templates login webpage
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
            messages.warning(request, "Wrong username or password! Please try again")
            return redirect(homepage.views.homepage)


def logout_view(request):
    logout(request)
    return redirect(homepage.views.homepage)


def register_view(request):
    # if the method is get, return templates register webpage
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


def edit_info_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                driver = Driver.objects.get(user_id=request.user.id)
                return render(request, 'login/edit_info.html', {'driver': driver, 'user': request.user})
            except ObjectDoesNotExist:
                return render(request, 'login/edit_info.html', {'user': request.user})
        else:
            return redirect(homepage.views.homepage)
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                driver = Driver.objects.get(user_id=request.user.id)
                driver.license = request.POST.get("license")
                driver.type = request.POST.get("type")
                driver.passenger_number = request.POST.get("passengerNumber")
                driver.special_info = request.POST.get("specialInfo")
                driver.save()
            except ObjectDoesNotExist:
                pass
            user = User.objects.get(username=request.user.username)
            user.first_name = request.POST.get("firstName")
            user.last_name = request.POST.get("lastName")
            user.email = request.POST.get("email")
            user.save()
        return redirect(homepage.views.homepage)

