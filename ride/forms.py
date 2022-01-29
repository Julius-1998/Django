from django import forms
from .models import Ride
from datetime import datetime, timedelta
from django.utils import timezone


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            'pick_up_location',
            'destination',
            'arrive_time',
            'passenger_number',
            'vehicle_type',
            'is_sharable',
            'special_request'
        ]


class JoinRequestForm(forms.Form):
    pick_up_location = forms.CharField()
    destination = forms.CharField()
    min_arrive_time = forms.DateTimeField(label='minimum arrive time', initial=timezone.now, required=False)
    # max_arrive_time = forms.DateTimeField(label='max arrive time', initial=hour_from_now, required=False)
    passenger_num = forms.DecimalField(max_value=4, min_value=1, label='PassengersNum', initial=1)


class DriverSearchRequestForm(forms.Form):
    pick_up_location = forms.CharField()
    destination = forms.CharField()
    min_arrive_time = forms.DateTimeField(label='minimum arrive time', initial=timezone.now, required=False)
    # max_arrive_time = forms.DateTimeField(label='max arrive time', initial=hour_from_now, required=False)
