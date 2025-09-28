from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer

'''
NOTE: Conside this as a reference and follow this same coding structure or format to work on you tasks
'''

# Create your views here.
class ItemView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# rides/serializers.py

from rest_framework import serializers
from .models import Ride

class RideRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for a rider to create a new ride request.
    """
    class Meta:
        model = Ride
        fields = [
            'pickup_address', 'dropoff_address', 
            'pickup_lat', 'pickup_lng', 
            'drop_lat', 'drop_lng'
        ]

class RideDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display detailed information about a ride.
    Used for listing available rides to drivers.
    """
    rider = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()

    class Meta:
        model = Ride
        fields = '__all__'