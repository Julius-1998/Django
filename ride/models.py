import copy
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ride(models.Model):
    vehicleTypes = (
        ('Poor', 'Poor'),
        ('XL', 'XL'),
        ('PetAccept', 'PetAccept'),
        ('Black', 'Black'),
    )

    SpecialRequests = (
        ('Quiet', 'Quiet'),
        ('Sanitized', 'Sanitized'),
    )

    rideStatus = (
        ('non-confirmed', 'non-confirmed'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )

    # users
    requester = models.CharField(max_length=50)
    driver = models.CharField(max_length=50, default='')
    sharers = models.CharField(max_length=500, default='')
    PassengersNum = models.IntegerField(default=1)

    # locations
    Pick_Up_Location = models.CharField(max_length=500)
    Destination = models.CharField(max_length=500)

    created = models.DateTimeField(default=timezone.now)
    Arrive_Time = models.DateTimeField('expected arrival date and time')
    Special_Request = models.CharField(max_length=200, blank=True)

    vehicleType = models.CharField(max_length=200, null=True, choices=vehicleTypes)
    WantShare = models.BooleanField(null=True)
    shareFound = models.BooleanField(default=False, null=True)
    status = models.CharField(null=True, max_length=120, choices=rideStatus, default='non-confirmed')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.Destination


class Vehicle(models.Model):
    # vehicle_brand = models.CharField(max_length=2, choices=BRANDS, default=HONDA)
    license_plate_number = models.CharField(max_length=200)
    Capacity = models.IntegerField(default=4)
    driverName = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Special_Features = models.CharField(max_length=200, blank=True)

    def __str__(self):
        tmp = copy.copy(self.__dict__)
        del tmp['_state']
        return str(tmp)