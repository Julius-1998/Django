from django.urls import path
from . import views

app_name = 'ride'

urlpatterns = [
        # path('', views.ride, name='ride'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('requestCreate/', views.ride_create.as_view(), name='ride_create'),
        path('sharingPage/', views.sharing_page, name='share'),
        path('joinRide/<int:ride_id>/<int:passenger_num>', views.join_ride, name='join_ride'),
        path('ride_view/', views.ride_view.as_view(), name='ride_view'),
        path('driver_ride_list/', views.driver_ride_list, name='driver_ride_list')
        path('ride_update/<str:ride_id>/', views.ride_update, name='ride_update')
        path('confirm_ride/<int:ride_id>/', views.confirm_ride, name='confirm_ride'),

]