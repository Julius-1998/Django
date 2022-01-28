from django import forms
from .models import Ride, Vehicle
from datetime import datetime, timedelta
from django.utils import timezone


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            'Pick_Up_Location',
            'Destination',
            'Arrive_Time',
            'PassengersNum',
            'vehicleType',
            'WantShare',
            'Special_Request'
        ]


class JoinRequestForm(forms.Form):
    Pick_Up_Location = forms.CharField()
    Destination = forms.CharField()
    min_arrive_time = forms.DateTimeField(label='minimum arrive time', initial=timezone.now, required=False)
    # max_arrive_time = forms.DateTimeField(label='max arrive time', initial=hour_from_now, required=False)
    PassengersNum = forms.DecimalField(max_value=4, min_value=1, label='PassengersNum', initial=1)


class DriverSearchRequestForm(forms.Form):
    Pick_Up_Location = forms.CharField()
    Destination = forms.CharField()
    min_arrive_time = forms.DateTimeField(label='minimum arrive time', initial=timezone.now, required=False)
    # max_arrive_time = forms.DateTimeField(label='max arrive time', initial=hour_from_now, required=False)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'license_plate_number',
            'Capacity',
            'Special_Features',
            'driverName'
        ]
