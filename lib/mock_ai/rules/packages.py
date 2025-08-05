"""
规则包定义

定义了常用的规则包，提供完整的对象生成模板。
"""

from ..core.rule_package import RulePackage
from .basic_rules import (
    address_rule,
    age_rule,
    company_rule,
    date_rule,
    description_rule,
    email_rule,
    first_name_rule,
    job_title_rule,
    last_name_rule,
    phone_rule,
    price_rule,
    website_rule,
)
from .combinations import full_address_combination, full_name_combination

# 个人信息包 - 包含完整的个人信息
person_package = RulePackage(
    name="person",
    description="Complete person information including name, contact, and demographics",
    rules=[
        full_name_combination,
        age_rule,
        email_rule,
        phone_rule,
        address_rule
    ],
    category="personal",
    metadata={
        "use_cases": ["user_profiles", "contact_lists", "customer_data"],
        "fields": ["full_name", "age", "email", "phone", "address"]
    }
)

# 公司信息包 - 包含完整的公司信息
company_package = RulePackage(
    name="company",
    description="Complete company information including business details",
    rules=[
        company_rule,
        full_address_combination,
        website_rule,
        phone_rule,
        email_rule,
        "industry",
        "employee_count"
    ],
    category="business",
    metadata={
        "use_cases": ["business_directory", "company_profiles", "vendor_data"],
        "fields": ["company", "full_address", "website", "phone", "email", "industry", "employee_count"]
    }
)

# 产品信息包 - 包含完整的产品信息
product_package = RulePackage(
    name="product", 
    description="Complete product information including details and pricing",
    rules=[
        "product_name",
        description_rule,
        price_rule,
        "category",
        "brand",
        "sku",
        "availability"
    ],
    category="ecommerce",
    metadata={
        "use_cases": ["product_catalog", "inventory_management", "ecommerce_data"],
        "fields": ["product_name", "description", "price", "category", "brand", "sku", "availability"]
    }
)

# 用户信息包 - 包含用户账户相关信息
user_package = RulePackage(
    name="user",
    description="User account information with authentication and profile data",
    rules=[
        "username",
        email_rule,
        first_name_rule,
        last_name_rule,
        "password_hash",
        date_rule,  # 注册日期
        "role",
        "status"
    ],
    category="authentication",
    metadata={
        "use_cases": ["user_management", "authentication_testing", "user_analytics"],
        "fields": ["username", "email", "first_name", "last_name", "password_hash", "registration_date", "role", "status"]
    }
)

# 订单信息包 - 包含完整的订单信息
order_package = RulePackage(
    name="order",
    description="Complete order information for ecommerce transactions",
    rules=[
        "order_id",
        "customer_id", 
        "product_id",
        "quantity",
        price_rule,
        "total_amount",
        date_rule,  # 订单日期
        "status",
        "shipping_address"
    ],
    category="ecommerce",
    metadata={
        "use_cases": ["order_management", "sales_analytics", "transaction_testing"],
        "fields": ["order_id", "customer_id", "product_id", "quantity", "price", "total_amount", "order_date", "status", "shipping_address"]
    }
)

# 文章信息包 - 包含博客文章或新闻内容
article_package = RulePackage(
    name="article",
    description="Article or blog post information with content and metadata",
    rules=[
        "title",
        "author", 
        description_rule,  # 摘要
        "content",
        date_rule,  # 发布日期
        "tags",
        "category",
        "read_time",
        "views"
    ],
    category="content",
    metadata={
        "use_cases": ["cms_testing", "blog_data", "content_analytics"],
        "fields": ["title", "author", "summary", "content", "publish_date", "tags", "category", "read_time", "views"]
    }
)

# 事件信息包 - 包含事件或活动信息
event_package = RulePackage(
    name="event",
    description="Event information including scheduling and location details",
    rules=[
        "event_name",
        description_rule,
        date_rule,  # 开始日期
        "end_date",
        "start_time",
        "end_time",
        "location",
        "organizer",
        "capacity",
        "price"
    ],
    category="events",
    metadata={
        "use_cases": ["event_management", "calendar_apps", "booking_systems"],
        "fields": ["event_name", "description", "start_date", "end_date", "start_time", "end_time", "location", "organizer", "capacity", "price"]
    }
) 