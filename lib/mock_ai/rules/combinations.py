"""
Rule Combination Definitions

Defines commonly used rule combinations that merge multiple rules into single fields.
"""

from ..core.rule_combination import RuleCombination
from .basic_rules import (
    address_rule,
    date_rule,
    first_name_rule,
    last_name_rule,
    time_rule,
)

# Full name combination - combines first and last name into full name
full_name_combination = RuleCombination(
    name="full_name",
    description="Combine first name and last name into a full name",
    rules=[first_name_rule, last_name_rule],
    combination_logic="and",
    metadata={
        "format": "first_name last_name",
        "example": "John Smith"
    }
)

# Full address combination - combines multiple address components
full_address_combination = RuleCombination(
    name="full_address",
    description="Combine street address, city, state, and zip code into a complete address",
    rules=[
        "street_address",
        "city", 
        "state",
        "zip_code"
    ],
    combination_logic="and",
    metadata={
        "format": "street, city, state zip",
        "example": "123 Main St, New York, NY 10001"
    }
)

# DateTime combination - combines date and time into complete timestamp
datetime_combination = RuleCombination(
    name="datetime",
    description="Combine date and time into a complete datetime",
    rules=[date_rule, time_rule],
    combination_logic="and",
    metadata={
        "format": "YYYY-MM-DD HH:MM:SS",
        "example": "2024-01-15 14:30:00"
    }
)

# Contact information combination - combines email and phone
contact_combination = RuleCombination(
    name="contact_info",
    description="Combine email and phone into contact information",
    rules=[
        "email",
        "phone"
    ],
    combination_logic="and",
    metadata={
        "format": "email and phone",
        "example": "john@example.com, +1-555-123-4567"
    }
)

# Price information combination - combines price and currency
price_info_combination = RuleCombination(
    name="price_info",
    description="Combine price value with currency information",
    rules=[
        "price",
        "currency"
    ],
    combination_logic="and", 
    metadata={
        "format": "currency price",
        "example": "USD 29.99"
    }
)

# Geographic coordinates combination - combines latitude and longitude
coordinates_combination = RuleCombination(
    name="coordinates",
    description="Combine latitude and longitude into geographic coordinates",
    rules=[
        "latitude",
        "longitude"
    ],
    combination_logic="and",
    metadata={
        "format": "lat, lng",
        "example": "40.7128, -74.0060"
    }
) 