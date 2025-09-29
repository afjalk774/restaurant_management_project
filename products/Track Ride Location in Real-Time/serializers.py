# ride/serializers.py

from rest_framework import serializers
from .models import Ride

class DriverLocationUpdateSerializer(serializers.Serializer):
    """
    Serializer to validate latitude and longitude data sent by the driver.
    """
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    class Meta:
        fields = ['latitude', 'longitude']


class RideTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer to format the driver's location for the rider.
    It sources the location data from the related driver model.
    """
    driver_latitude = serializers.FloatField(source='driver.current_latitude', read_only=True)
    driver_longitude = serializers.FloatField(source='driver.current_longitude', read_only=True)

    class Meta:
        model = Ride
        fields = ['driver_latitude', 'driver_longitude']