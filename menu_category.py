# Consolidated Code for Menu Category API Endpoint

# --- Required Imports ---
# These would typically be at the top of their respective files.
from django.urls import path
from rest_framework import serializers
from rest_framework.generics import ListAPIView

# You would also need to import your model, for example:
# from .models import MenuCategory
# For this example, we'll define a placeholder model class.

class MenuCategory:
    """Placeholder for the actual Django model."""
    objects = None # In a real model, this would be the manager.
    pass

# -----------------------------------------------------------
# Step 1: The Serializer (normally in home/serializers.py)
# -----------------------------------------------------------
class MenuCategorySerializer(serializers.ModelSerializer):
    """
    Serializes the MenuCategory model, exposing only the 'name' field.
    """
    class Meta:
        model = MenuCategory
        fields = ['name']


# -----------------------------------------------------------
# Step 2: The View (normally in home/views.py)
# -----------------------------------------------------------
class MenuCategoryView(ListAPIView):
    """
    A read-only API view that lists all MenuCategory instances.
    """
    # In a real view, the queryset would fetch from the database.
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


# -----------------------------------------------------------
# Step 3: The URL Configuration (normally in home/urls.py)
# -----------------------------------------------------------
# This list connects the URL path to the view.
urlpatterns = [
    path('api/menu-categories/', MenuCategoryView.as_view(), name='menu-categories'),
    # ... other URL patterns might be in this list.
]
##