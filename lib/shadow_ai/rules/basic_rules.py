"""
Basic Rule Definitions

Defines commonly used single-field generation rules.
"""

from ..core.rule import Rule

# Personal information related rules
email_rule = Rule(
    name="email",
    description="Generate a realistic email address",
    examples=["john.doe@example.com", "user123@gmail.com", "business@company.org"],
    constraints={"format": "valid_email", "domain_variety": True}
)

first_name_rule = Rule(
    name="first_name",
    description="Generate a person's first name",
    examples=["John", "Mary", "David", "Sarah", "Michael"],
    constraints={"gender_neutral": False, "cultural_diversity": True}
)

last_name_rule = Rule(
    name="last_name",
    description="Generate a person's last name",
    examples=["Smith", "Johnson", "Williams", "Brown", "Jones"],
    constraints={"cultural_diversity": True}
)

age_rule = Rule(
    name="age",
    description="Generate a person's age",
    examples=[25, 30, 45, 22, 67],
    constraints={"min": 18, "max": 80, "type": "integer"}
)

phone_rule = Rule(
    name="phone",
    description="Generate a phone number",
    examples=["+1-555-123-4567", "(555) 987-6543", "555.111.2222"],
    constraints={"format": "international_or_local", "valid": True}
)

address_rule = Rule(
    name="address",
    description="Generate a street address",
    examples=["123 Main St", "456 Oak Avenue", "789 Elm Drive"],
    constraints={"include_number": True, "realistic": True}
)

# Business information related rules
company_rule = Rule(
    name="company",
    description="Generate a company name",
    examples=["TechCorp Inc.", "DataFlow Solutions", "CloudByte Systems"],
    constraints={"style": "professional", "include_suffix": True}
)

job_title_rule = Rule(
    name="job_title",
    description="Generate a job title",
    examples=["Software Engineer", "Marketing Manager", "Data Scientist"],
    constraints={"level_variety": True, "industry_diverse": True}
)

website_rule = Rule(
    name="website",
    description="Generate a website URL",
    examples=["https://example.com", "https://company.org", "https://business.net"],
    constraints={"protocol": "https", "valid_domain": True}
)

description_rule = Rule(
    name="description",
    description="Generate a descriptive text",
    examples=["A innovative technology company", "Leading provider of cloud solutions"],
    constraints={"length": "50-200", "professional": True}
)

price_rule = Rule(
    name="price",
    description="Generate a price value",
    examples=[19.99, 299.0, 1599.99],
    constraints={"currency": "USD", "format": "decimal", "range": "10-5000"}
)

# Date and time related rules
date_rule = Rule(
    name="date",
    description="Generate a date",
    examples=["2024-01-15", "2023-12-25", "2024-06-30"],
    constraints={"format": "YYYY-MM-DD", "range": "recent"}
)

time_rule = Rule(
    name="time",
    description="Generate a time",
    examples=["14:30:00", "09:15:30", "18:45:15"],
    constraints={"format": "HH:MM:SS", "24_hour": True}
)

# Data type rules
boolean_rule = Rule(
    name="boolean",
    description="Generate a boolean value",
    examples=[True, False],
    constraints={"type": "boolean"}
)

number_rule = Rule(
    name="number",
    description="Generate a number",
    examples=[42, 158, 7],
    constraints={"type": "integer", "range": "1-1000"}
)

text_rule = Rule(
    name="text",
    description="Generate text content",
    examples=["Lorem ipsum dolor sit amet", "Sample text content"],
    constraints={"length": "10-100", "readable": True}
)
