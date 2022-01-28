from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView

import homepage
from driver.models import Driver
from .models import Ride, Vehicle
from .forms import RideForm


# def ride_create(request):
#     if request.method == "POST":
#         ride_form = RideForm(data=request.post)
#         if ride_form.is_valid():
#             new_ride = ride_form.save(commit=False)
#             new_ride.requester = User.objects.get(id=1)
#             new_ride.save()
#             return render(request, 'ride/dashboard.html')


class ride_create(LoginRequiredMixin, CreateView):
    template_name = 'ride/request_create.html'
    form_class = RideForm
    queryset = Ride.objects.all()

    def form_valid(self, form):
        form.instance.ownerName = self.request.user.username
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
                vehicle = Vehicle.objects.get(driver=user_object)
                return {"CONFIRMED": True, "OPEN": False, "COMPLETE": False}
            except ObjectDoesNotExist:
                return {"OPEN": True, "CONFIRMED": True, "COMPLETE": False}
        else:
            ret = {}
            for k in ['CONFIRMED', 'OPEN', 'COMPLETE']:
                ret[k] = True if k in request.GET else False
            return ret

    return render(request, 'ride/dashboard.html')


def requestPage(request):
    return render(request, 'ride/requestPage.html')
    # if request.method == 'GET':
    #     if request.user.is_authenticated:
    #         try:
    #             driver = Driver.objects.get(user_id=request.user.id)
    #             return render(request, 'login/edit_info.html', {'driver': driver, 'user': request.user})
    #         except ObjectDoesNotExist:
    #             return render(request, 'login/edit_info.html', {'user': request.user})
    #     else:
    #         return redirect(homepage.views.homepage)
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         try:
    #             driver = Driver.objects.get(user_id=request.user.id)
    #             driver.license = request.POST.get("license")
    #             driver.type = request.POST.get("type")
    #             driver.passenger_number = request.POST.get("passengerNumber")
    #             driver.special_info = request.POST.get("specialInfo")
    #             driver.save()
    #         except ObjectDoesNotExist:
    #             pass
    #         user = User.objects.get(username=request.user.username)
    #         user.first_name = request.POST.get("firstName")
    #         user.last_name = request.POST.get("lastName")
    #         user.email = request.POST.get("email")
    #         user.save()
    #     return redirect(homepage.views.homepage)

def sharingPage(request):
    return redirect(homepage.views.homepage)