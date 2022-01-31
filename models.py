import copy
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ride(models.Model):
    VehicleTypes = (
        ('Poor', 'Poor'),
        ('XL', 'XL'),
        ('PetAccept', 'PetAccept'),
        ('Black', 'Black'),
    )

    SpecialRequests = (
        ('Quiet', 'Quiet'),
        ('Sanitized', 'Sanitized'),
    )

    RideStatus = (
        ('non-confirmed', 'non-confirmed'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )

    # users
    requester = models.CharField(max_length=50)
    driver = models.CharField(max_length=50, default='')
    sharers = models.CharField(max_length=500, default='')
    passenger_number = models.IntegerField(default=1)

    # locations
    pick_up_location = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)

    created = models.DateTimeField(default=timezone.now)
    arrive_time = models.DateTimeField(default=timezone.now)
    special_request = models.CharField(max_length=200, blank=True, choices=SpecialRequests)

    vehicle_type = models.CharField(max_length=200, null=True, choices=VehicleTypes)
    is_sharable = models.BooleanField(null=True)
    is_share_found = models.BooleanField(default=False, null=True)
    status = models.CharField(null=True, max_length=120, choices=RideStatus, default='non-confirmed')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.destination


class ShareInfo(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
