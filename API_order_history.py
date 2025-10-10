from django.db import models
from django.contrib.auth.models import User
import uuid

# It's a good practice to have a base model for common fields.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(models.Model):
    """A simple product model for demonstration."""
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(BaseModel):
    """
    Represents a customer's order.
    """
    # Use a UUID for the order_id for a unique, non-sequential ID.
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ForeignKey to the User model to associate the order with a user.
    # on_delete=models.CASCADE means if a user is deleted, their orders are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    """
    Represents an item within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of purchase

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.order_id}"

    def save(self, *args, **kwargs):
        # Set the price from the product when the order item is created
        if not self.id:
            self.price = self.product.price
        super().save(*args, **kwargs)
