"""
Data Validation Utilities Module

Provides validation functionality for various data formats.
"""

import re
from typing import Any


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email address

    Returns:
        bool: Whether it's a valid email format
    """
    if not isinstance(email, str):
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format

    Args:
        phone: Phone number

    Returns:
        bool: Whether it's a valid phone number format
    """
    if not isinstance(phone, str):
        return False

    # Remove all non-digit characters
    digits_only = re.sub(r"\D", "", phone)

    # Check length (supports international numbers)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False

    # Common phone number formats
    patterns = [
        r"^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$",  # US format
        r"^\+?[1-9]\d{6,14}$",  # International format
        r"^[0-9]{7,15}$",  # Simple digits
    ]

    for pattern in patterns:
        if re.match(pattern, phone):
            return True

    return False


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL address

    Returns:
        bool: Whether it's a valid URL format
    """
    if not isinstance(url, str):
        return False

    pattern = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
    simple_pattern = r"^(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}$"

    return bool(re.match(pattern, url) or re.match(simple_pattern, url))


def validate_date(date_str: str, format_type: str = "YYYY-MM-DD") -> bool:
    """
    Validate date format

    Args:
        date_str: Date string
        format_type: Date format type

    Returns:
        bool: Whether it's a valid date format
    """
    if not isinstance(date_str, str):
        return False

    patterns = {
        "YYYY-MM-DD": r"^\d{4}-\d{2}-\d{2}$",
        "MM/DD/YYYY": r"^\d{2}/\d{2}/\d{4}$",
        "DD-MM-YYYY": r"^\d{2}-\d{2}-\d{4}$",
        "YYYY/MM/DD": r"^\d{4}/\d{2}/\d{2}$",
    }

    pattern = patterns.get(format_type)
    if not pattern:
        return False

    if not re.match(pattern, date_str):
        return False

    # Further validate date validity
    try:
        from datetime import datetime

        if format_type == "YYYY-MM-DD":
            datetime.strptime(date_str, "%Y-%m-%d")
        elif format_type == "MM/DD/YYYY":
            datetime.strptime(date_str, "%m/%d/%Y")
        elif format_type == "DD-MM-YYYY":
            datetime.strptime(date_str, "%d-%m-%Y")
        elif format_type == "YYYY/MM/DD":
            datetime.strptime(date_str, "%Y/%m/%d")
        return True
    except ValueError:
        return False


def validate_time(time_str: str, format_type: str = "HH:MM:SS") -> bool:
    """
    Validate time format

    Args:
        time_str: Time string
        format_type: Time format type

    Returns:
        bool: Whether it's a valid time format
    """
    if not isinstance(time_str, str):
        return False

    patterns = {
        "HH:MM:SS": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
        "HH:MM": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
        "HH:MM AM/PM": r"^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$",
    }

    pattern = patterns.get(format_type)
    return bool(pattern and re.match(pattern, time_str))


def validate_price(price: Any) -> bool:
    """
    Validate price format

    Args:
        price: Price value

    Returns:
        bool: Whether it's a valid price format
    """
    if isinstance(price, (int, float)):
        return price >= 0

    if isinstance(price, str):
        # Remove currency symbols and spaces
        cleaned_price = re.sub(r"[\$€£¥₹\s,]", "", price)
        try:
            float_price = float(cleaned_price)
            return float_price >= 0
        except ValueError:
            return False

    return False


def validate_json_structure(data: Any, required_fields: list) -> bool:
    """
    Validate JSON structure contains required fields

    Args:
        data: Data to validate
        required_fields: List of required fields

    Returns:
        bool: Whether all required fields are present
    """
    if not isinstance(data, dict):
        return False

    for field in required_fields:
        if field not in data:
            return False

    return True
