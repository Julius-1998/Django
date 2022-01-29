# Generated by Django 4.0.1 on 2022-01-28 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(max_length=50)),
                ('driver', models.CharField(default='', max_length=50)),
                ('sharers', models.CharField(default='', max_length=500)),
                ('PassengersNum', models.IntegerField(default=1)),
                ('Pick_Up_Location', models.CharField(max_length=500)),
                ('Destination', models.CharField(max_length=500)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('Arrive_Time', models.DateTimeField(verbose_name='expected arrival date and time')),
                ('Special_Request', models.CharField(blank=True, max_length=200)),
                ('vehicleType', models.CharField(choices=[('Poor', 'Poor'), ('XL', 'XL'), ('PetAccept', 'PetAccept'), ('Black', 'Black')], max_length=200, null=True)),
                ('WantShare', models.BooleanField(null=True)),
                ('shareFound', models.BooleanField(default=False, null=True)),
                ('status', models.CharField(choices=[('non-confirmed', 'non-confirmed'), ('confirmed', 'confirmed'), ('completed', 'completed')], default='non-confirmed', max_length=120, null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate_number', models.CharField(max_length=200)),
                ('Capacity', models.IntegerField(default=4)),
                ('Special_Features', models.CharField(blank=True, max_length=200)),
                ('driverName', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]