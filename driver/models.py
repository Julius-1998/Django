from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    vehicleTypes = (
        ('Poor', 'Poor'),
        ('XL', 'XL'),
        ('PetAccept', 'PetAccept'),
        ('Black', 'Black'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=vehicleTypes)
    passenger_number = models.IntegerField(default=2,
                                          validators=[
                                              MinValueValidator(1),
                                              MaxValueValidator(100),
                                          ])
    special_info = models.CharField(max_length=100)

