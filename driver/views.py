from django.shortcuts import render, redirect

# Create your views here.
import homepage
from driver.models import Driver
from django.contrib.auth.models import Group, Permission


def register_view(request):
    if request.method == 'GET':
        return render(request, 'driver/register.html')
    if request.method == 'POST':
        driver = Driver()
        driver.license = request.POST.get("license")
        driver.type = request.POST.get("type")
        driver.passenger_number = request.POST.get("passengerNumber")
        driver.special_info = request.POST.get("specialInfo")
        driver.user = request.user
        driver.save()
        group, create = Group.objects.get_or_create(name='driver')
        if create:
            can_view_driver = Permission.objects.get(name='Can view driver')
            group.permissions.add(can_view_driver)

        driver.user.groups.add(group)
        return redirect(homepage.views.homepage)

