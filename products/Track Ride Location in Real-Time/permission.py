# ride/permissions.py

from rest_framework.permissions import BasePermission
from .models import Ride

class IsRiderOfRide(BasePermission):
    """
    Custom permission to only allow the rider of a ride to access it.
    Ensures the ride is in 'ONGOING' status.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the rider associated with the ride object.
        # Also, crucially, check if the ride's status is 'ONGOING'.
        return obj.rider == request.user.rider and obj.status == 'ONGOING'