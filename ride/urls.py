from django.urls import path
from . import views

app_name = 'ride'

urlpatterns = [
        # path('', views.ride, name='ride'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('requestCreate/', views.ride_create.as_view(), name='ride_create'),
        path('sharingPage/', views.sharing_page, name='share'),
        path('joinRide/<int:ride_id>/<int:passenger_num>', views.join_ride, name='join_ride')

]