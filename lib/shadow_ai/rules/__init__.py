"""
ShadowAI Built-in Rules Module

Provides commonly used predefined rules for direct user access.
"""

from .basic_rules import (
    address_rule,
    age_rule,
    boolean_rule,
    company_rule,
    date_rule,
    description_rule,
    email_rule,
    first_name_rule,
    job_title_rule,
    last_name_rule,
    number_rule,
    phone_rule,
    price_rule,
    text_rule,
    time_rule,
    website_rule,
)
from .combinations import (
    datetime_combination,
    full_address_combination,
    full_name_combination,
)
from .packages import (
    company_package,
    person_package,
    product_package,
    user_package,
)

__all__ = [
    # Basic rules
    "email_rule",
    "first_name_rule",
    "last_name_rule",
    "age_rule",
    "phone_rule",
    "address_rule",
    "company_rule",
    "job_title_rule",
    "website_rule",
    "description_rule",
    "price_rule",
    "date_rule",
    "time_rule",
    "boolean_rule",
    "number_rule",
    "text_rule",
    # Combinations
    "full_name_combination",
    "full_address_combination",
    "datetime_combination",
    # Packages
    "person_package",
    "company_package",
    "product_package",
    "user_package",
]
