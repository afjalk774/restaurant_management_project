# ride/views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ride
from .serializers import DriverLocationUpdateSerializer, RideTrackingSerializer
from .permissions import IsRiderOfRide
from accounts.permissions import IsDriver # Assuming you have an IsDriver permission

class UpdateLocationView(APIView):
    """
    API endpoint for authenticated drivers to update their current location.
    """
    permission_classes = [IsAuthenticated, IsDriver]
    serializer_class = DriverLocationUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the driver profile associated with the authenticated user
        driver = request.user.driver
        driver.current_latitude = serializer.validated_data['latitude']
        driver.current_longitude = serializer.validated_data['longitude']
        driver.save()

        return Response({"status": "success", "message": "Location updated successfully."}, status=status.HTTP_200_OK)


class TrackRideView(generics.RetrieveAPIView):
    """
    API endpoint for the rider to track the driver's location for a specific ride.
    """
    queryset = Ride.objects.all()
    serializer_class = RideTrackingSerializer
    permission_classes = [IsAuthenticated, IsRiderOfRide]
    lookup_field = 'id' # Use 'id' to match the URL parameter <ride_id>