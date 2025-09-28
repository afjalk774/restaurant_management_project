from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Feedback
from .serializers import FeedbackSerializer

class RideFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id, *args, **kwargs):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        if ride.status != 'COMPLETED':
            return Response({"error": "Feedback can only be submitted for completed rides."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user != ride.rider and request.user != ride.driver:
            return Response({"error": "You are not authorized to submit feedback for this ride."}, status=status.HTTP_403_FORBIDDEN)

        if Feedback.objects.filter(ride=ride, submitted_by=request.user).exists():
            return Response({"error": "You have already submitted feedback for this ride."}, status=status.HTTP_409_CONFLICT)

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ride=ride, submitted_by=request.user)
            return Response({"message": "Feedback submitted successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)