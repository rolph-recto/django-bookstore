#bookstore/util.py
#Rolph Recto

from django.core.exceptions import ValidationError

def not_negative(value):
    """validator function to make sure the number value is not negative"""
    if value < 0:
        raise ValidationError('Value cannot be negative')