# orders/utils.py

import secrets
import string

from .models import Coupon # Make sure to import your Coupon model

def generate_coupon_code(length=10):

    # Define the characters to use for the code (uppercase letters and digits)
    characters = string.ascii_uppercase + string.digits
    
    while True:
        # Generate a random code of the specified length
        coupon_code = ''.join(secrets.choice(characters) for i in range(length))
        
        # Check if a coupon with this code already exists in the database
        if not Coupon.objects.filter(code=coupon_code).exists():
            # If the code is unique, break the loop
            break
            
    return coupon_code