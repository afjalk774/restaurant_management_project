#
# STEP 1: DEFINE THE DJANGO MODEL
# ---------------------------------
# In 'orders/models.py', we define the Coupon model. This creates the database
# table to store all coupon details, including the unique code, discount value,
# and validity period. We use validators to ensure the discount is a sensible percentage.
#
# orders/models.py
#
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Coupon(models.Model):
    """
    Represents a discount coupon in the database.
    """
    code = models.CharField(max_length=50, unique=True)
    # Using DecimalField is best practice for financial values to avoid floating-point errors.
    # The validators ensure the discount is always between 0% (0.0) and 100% (1.0).
    discount_percentage = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        # The __str__ method provides a human-readable name for each coupon object,
        # which is useful in the Django admin panel.
        return self.code

#
# STEP 2: CREATE THE API VIEW FOR VALIDATION
# -------------------------------------------
# In 'orders/views.py', we create an APIView to handle the validation logic.
# It expects a POST request containing a coupon 'code'. The view then checks
# the database to see if the coupon exists, is active, and is within its
# valid date range.
#
# orders/views.py
#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Note: Import the Coupon model defined above and timezone for date comparison.
# from .models import Coupon
# from django.utils import timezone

class CouponValidationView(APIView):
    """
    An API view to validate a coupon code.
    Expects a POST request with a 'code' field.
    """
    def post(self, request, *args, **kwargs):
        code_from_request = request.data.get('code')
        if not code_from_request:
            return Response(
                {'error': 'Coupon code not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # We use 'iexact' for a case-insensitive lookup of the coupon code.
            coupon = Coupon.objects.get(code__iexact=code_from_request)
        except Coupon.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'Invalid coupon code.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the coupon is currently active.
        if not coupon.is_active:
            return Response(
                {'valid': False, 'error': 'This coupon is no longer active.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the coupon is within its valid date range.
        today = timezone.now().date()
        if not (coupon.valid_from <= today <= coupon.valid_until):
            return Response(
                {'valid': False, 'error': 'This coupon has expired or is not yet valid.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If all checks pass, the coupon is valid.
        return Response({
            'valid': True,
            'code': coupon.code,
            'discount_percentage': coupon.discount_percentage
        }, status=status.HTTP_200_OK)


#
# STEP 3: CONFIGURE THE URL
# --------------------------
# In 'orders/urls.py', we map a URL path to our CouponValidationView.
# When a POST request is made to '/api/coupons/validate/', Django will route
# it to our view, triggering the validation logic.
#
# orders/urls.py
#
from django.urls import path
# Note: Import the view we created.
# from .views import CouponValidationView

urlpatterns = [
    # Other URLs in your app might be here...
    path('api/coupons/validate/', CouponValidationView.as_view(), name='coupon-validate'),
]