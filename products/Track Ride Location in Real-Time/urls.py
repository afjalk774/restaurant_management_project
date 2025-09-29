# ride/urls.py

from django.urls import path
from .views import (
    # ... your other ride views
    UpdateLocationView,
    TrackRideView,
)

urlpatterns = [
    # ... your other ride URLs
    path('update-location/', UpdateLocationView.as_view(), name='update-driver-location'),
    path('track/<int:id>/', TrackRideView.as_view(), name='track-ride'),
]