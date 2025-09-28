# rides/views.py

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Ride
from accounts.models import Rider, Driver # Assuming models are in 'accounts' app
from .serializers import RideRequestSerializer, RideDetailSerializer

class RequestRideView(generics.CreateAPIView):
    """
    API endpoint for a rider to request a new ride.
    POST /api/ride/request/
    """
    serializer_class = RideRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the Rider instance associated with the logged-in user
        rider = get_object_or_404(Rider, user=self.request.user)
        # Associate the ride with the rider
        serializer.save(rider=rider)

class AvailableRidesView(generics.ListAPIView):
    """
    API endpoint for drivers to see all unassigned ride requests.
    GET /api/ride/available/
    """
    serializer_class = RideDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only drivers can see available rides
        # You might add an IsDriver permission class for more security
        return Ride.objects.filter(status='REQUESTED', driver__isnull=True)

class AcceptRideView(APIView):
    """
    API endpoint for a driver to accept a ride.
    POST /api/ride/accept/<ride_id>/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id, *args, **kwargs):
        driver = get_object_or_404(Driver, user=request.user)
        
        try:
            # Use a transaction to prevent race conditions
            with transaction.atomic():
                # Select the ride for update, locking the row until the transaction is complete
                ride = Ride.objects.select_for_update().get(id=ride_id)

                # Check if the ride is still available
                if ride.status != 'REQUESTED' or ride.driver is not None:
                    return Response(
                        {"error": "This ride has already been accepted."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Assign the driver and update the status
                ride.driver = driver
                ride.status = 'ONGOING'
                ride.save()

                serializer = RideDetailSerializer(ride)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)