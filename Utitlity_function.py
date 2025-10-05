from datetime import date
from django.db.models import Sum
from .models import Order

def get_daily_sales_total(target_date: date) -> float:
    """
    Calculates the total sales for a given date.

    Args:
        target_date: A Python date object for which to calculate sales.

    Returns:
        The total sum of all order prices for the day, or 0 if no sales.
    """
    # Filter orders by the exact date (ignoring the time part of created_at)
    daily_orders = Order.objects.filter(created_at__date=target_date)
    
    # Aggregate the sum of the 'total_price' field for the filtered orders
    aggregation = daily_orders.aggregate(total_sales=Sum('total_price'))
    
    # The result is in a dictionary with the key 'total_sales'
    total = aggregation.get('total_sales')
    
    # If total is None (no orders), return 0, otherwise return the total
    return total or 0.0