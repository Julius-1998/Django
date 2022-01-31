from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Q

import homepage
from driver.models import Driver

from ride.models import Ride, ShareInfo
from ride.forms import RideForm, JoinRequestForm, DriverSearchRequestForm


def ride_create(request):
    form = RideForm
    if request.method == 'POST':
        form = RideForm(request.POST)
        form.instance.requester = request.user.username
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'ride/ride_create.html', {'form': form})


def ride_update(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    form = RideForm(instance=ride)
    if request.method == 'POST':
        form = RideForm(request.POST, instance=ride)
        form.instance.requester = request.user.username
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes successfully saved.')
            return redirect('/')

    return render(request, 'ride/ride_create.html', {'form': form})


def get_user(request):
    return request.user.id


def dashboard(request):
    user = get_user(request)
    User.objects.get(id=user)

    return render(request, 'ride/dashboard.html')


def driver_ride_list(request):
    if request.method == 'GET':
        form = DriverSearchRequestForm
        return render(request, 'ride/driver_ride_list.html', {'form': form})
    if request.method == 'POST':
        form = DriverSearchRequestForm(request.POST)
        if form.is_valid():
            special_request = form.cleaned_data['special_request']
            driver = Driver.objects.get(user=request.user.id)
            passenger_number = driver.passenger_number
            car_type = driver.type
            if special_request == "":
                rides = Ride.objects.filter(status='non-confirmed',
                                            passenger_number__lte=passenger_number,
                                            vehicle_type=car_type)
            else:
                rides = Ride.objects.filter(status='non-confirmed',
                                            special_request=special_request,
                                            passenger_number__lte=passenger_number,
                                            vehicle_type=car_type)
        return render(request, 'ride/driver_ride_list.html', {'form': form, 'rides': rides})


def sharing_page(request):
    if request.method == 'GET':
        form = JoinRequestForm
        return render(request, 'ride/share.html', {'form': form})
    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            min_arrive_time = form.cleaned_data['min_arrive_time']
            max_arrive_time = form.cleaned_data['max_arrive_time']
            passenger_num = form.cleaned_data['passenger_num']
            rides = Ride.objects.filter(status='non-confirmed',
                                        is_sharable=True,
                                        is_share_found=False,
                                        destination=destination,
                                        arrive_time__range=(min_arrive_time, max_arrive_time)
                                        )
            return render(request, 'ride/share.html', {'form': form, 'rides': rides, 'num': passenger_num})
        # if not valid do something else
        return render(request, 'ride/share.html', {'form': form})


def join_ride(request, ride_id, passenger_num):
    message = 'Ride joined'
    ride = Ride.objects.get(id=ride_id)
    # add the sharer's passenger num to the ride
    ride.passenger_number += passenger_num
    ride.is_share_found = True
    ride.save()
    user = User.objects.get(id=request.user.id)
    share = ShareInfo()
    share.ride = ride
    share.sharer = user
    share.save()
    messages.success(request, 'Changes successfully saved.')
    return redirect(homepage.views.homepage)


class ride_view(LoginRequiredMixin, ListView):
    template_name = 'ride/ride_list.html'

    def get(self, request, *args, **kwargs):
        rides = Ride.objects.filter((Q(requester=self.request.user.username) | Q(sharers=self.request.user.username))
                                   & (Q(status='confirmed') | Q(status='non-confirmed')))
        return render(request, self.template_name, {'rides': rides})



