from django import forms
from ride.models import Ride
from datetime import datetime, timedelta
from django.utils import timezone
from ride.widget import DateTimePickerInput


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
    destination = forms.CharField(required=True)
    min_arrive_time = forms.DateTimeField(widget=DateTimePickerInput,label='minArriveTime', initial=timezone.now, required=False)
    max_arrive_time = forms.DateTimeField(widget=DateTimePickerInput,label='maxArriveTime', initial=timezone.now, required=False)
    passenger_num = forms.DecimalField(max_value=4, min_value=1, label='PassengersNum', initial=1)


class DriverSearchRequestForm(forms.Form):
    special_request = forms.CharField(required=False)