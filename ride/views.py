from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q
from django.core.mail import send_mail

import homepage
import ride.views
from driver.models import Driver

from ride.models import Ride,ShareInfo
from ride.forms import RideForm, JoinRequestForm


class ride_create(LoginRequiredMixin, CreateView):
    template_name = 'ride/request_create.html'
    form_class = RideForm
    queryset = Ride.objects.all()

    def form_valid(self, form):
        form.instance.ownerName = self.request.user.username
        form.save()
        # return super().form_valid(form)
        return redirect(homepage.views.homepage)


def get_user(request):
    return request.user.username


def dashboard(request):
    user = get_user(request)
    user_object = User.objects.get(username=user)

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


def driver_ride_list(request):
    driver = Driver.objects.get(user=request.user.id)
    passenger_number = driver.passenger_number
    car_type = driver.type
    special_request = driver.special_info
    print(special_request)
    rides = Ride.objects.filter(Q(status='non-confirmed')&
                               (Q(special_request=special_request)|Q(special_request=''))&
                                Q(passenger_number__lte=passenger_number)&
                                (Q(vehicle_type=car_type)|Q(vehicle_type=''))
    )
    return render(request, 'ride/driver_ride_list.html', {'rides': rides})


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
            return render(request, 'ride/share.html', {'form': form, 'rides': rides,'num': passenger_num})
        # if not valid do something else
        return render(request, 'ride/share.html', {'form': form})


def join_ride(request, ride_id, passenger_num):
    ride = Ride.objects.get(id=ride_id)
    # add the sharer's passenger num to the ride
    ride.passenger_number += passenger_num
    ride.is_share_found = True
    user = User.objects.get(id=request.user.id)
    ride.sharers = user.username
    ride.save()
    messages.success(request, 'Changes successfully saved.')
    return redirect(homepage.views.homepage)


def confirm_ride(request,ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 'confirmed'
    ride.driver = get_user(request)
    ride.save()
    messages.success(request, 'Ride successfully confirmed.')
    # send emails to owner and other sharer
    requester_mail = User.objects.get(username=ride.requester).email
    sharer_mail = User.objects.get(username=ride.sharers).email
    send_mail(
        'Message from Uber',
        'Your ride is confirmed.',
        'sjzhou5292@gmail.com',
        [requester_mail, sharer_mail],
        fail_silently=True,
    )
    return redirect(homepage.views.homepage)


class ride_view(LoginRequiredMixin, ListView):
    template_name = 'ride/ride_list.html'

    def get(self, request, *args, **kwargs):
        rides = Ride.objects.filter((Q(requester=self.request.user.username) | Q(sharers=self.request.user.username))
                                   & (Q(status='confirmed') | Q(status='non-confirmed')))
        return render(request, self.template_name, {'rides': rides})


class ride_update(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'ride/request_update.html'
    form_class = RideForm
    queryset = Ride.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ride, id=id_)

    def form_valid(self, form):
        form.instance.ownerName = self.request.user.username
        form.save()
        return redirect(ride.views.ride_view)

    def test_func(self):
        post = self.get_object()
        if self.request.user.username == post.ownerName:
            return True
        return False
