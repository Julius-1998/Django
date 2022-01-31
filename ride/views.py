from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, ListView
from django.db.models import Q

import homepage
from driver.models import Driver

from ride.models import Ride, ShareInfo
from ride.forms import RideForm, JoinRequestForm


class ride_create(LoginRequiredMixin, CreateView):
    template_name = 'ride/request_create.html'
    form_class = RideForm
    queryset = Ride.objects.all()

    def form_valid(self, form):
        form.instance.requester = self.request.user.username
        form.save()
        # return super().form_valid(form)
        return redirect(homepage.views.homepage)


def get_user(request):
    return request.user.id


def dashboard(request):
    user = get_user(request)
    user_object = User.objects.get(id=user)

    def infer_allowed_statuses(request):
        if len(request.GET) == 0:
            try:
                driver = Driver.objects.get(driver=user_object)
                return {"CONFIRMED": True, "OPEN": False, "COMPLETE": False}
            except ObjectDoesNotExist:
                return {"OPEN": True, "CONFIRMED": True, "COMPLETE": False}
        else:
            ret = {}
            for k in ['CONFIRMED', 'OPEN', 'COMPLETE']:
                ret[k] = True if k in request.GET else False
            return ret

    return render(request, 'ride/dashboard.html')


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

    def get_queryset(self):
        return Ride.objects.filter((Q(requester=self.request.user.username) | Q(sharers=self.request.user.username))
                                   & (Q(status='confirmed') | Q(status='non-confirmed')))

