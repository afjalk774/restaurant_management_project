from django.db import models
from django.contrib.auth.models import User
import uuid

class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides_as_driver')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    # ... other ride fields like pickup_location, dropoff_location, etc.

class Feedback(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='feedback')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only submit one feedback per ride
        unique_together = ('ride', 'submitted_by')