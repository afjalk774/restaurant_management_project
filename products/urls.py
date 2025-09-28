# rides/urls.py

from django.urls import path
from .views import RequestRideView, AvailableRidesView, AcceptRideView

urlpatterns = [
    path('ride/request/', RequestRideView.as_view(), name='request-ride'),
    path('ride/available/', AvailableRidesView.as_view(), name='available-rides'),
    path('ride/accept/<int:ride_id>/', AcceptRideView.as_view(), name='accept-ride'),
]