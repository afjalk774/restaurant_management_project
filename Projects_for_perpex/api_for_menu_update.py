from rest_framework import serializers
from .models import Order, OrderItem, Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Handles validation for creating and updating products.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
    
    def validate_price(self, value):
        """
        Check that the price is a positive number.
        """
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Price must be a positive number.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model. This will be nested within the OrderSerializer.
    """
    # Use ProductSerializer to represent the nested product details.
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        # Fields to include in the serialized output.
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model. Handles nested serialization of OrderItems.
    """
    # 'items' is the `related_name` from the OrderItem model's ForeignKey to Order.
    # This tells the OrderSerializer to use the OrderItemSerializer for the nested 'items' relationship.
    items = OrderItemSerializer(many=True, read_only=True)
    # Use a SerializerMethodField to format the date for better readability.
    date = serializers.DateTimeField(source='created_at', format="%Y-%m-%d %H:%M:%S", read_only=True)


    class Meta:
        model = Order
        # The fields that will be returned in the API response.
        fields = ['order_id', 'date', 'total_price', 'items']
