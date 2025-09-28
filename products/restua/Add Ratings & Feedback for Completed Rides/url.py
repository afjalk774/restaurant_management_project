from django.urls import path
from .views import RideFeedbackView

urlpatterns = [
    # ... other urls
    path('api/ride/feedback/<uuid:ride_id>/', RideFeedbackView.as_view(), name='ride-feedback'),
]