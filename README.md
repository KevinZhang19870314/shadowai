# ShadowAI

🚀 An AI-powered intelligent mock data generation library

[![PyPI version](https://badge.fury.io/py/shadowai.svg)](https://badge.fury.io/py/shadowai)
[![CI](https://github.com/KevinZhang19870314/shadowai/actions/workflows/ci.yml/badge.svg)](https://github.com/KevinZhang19870314/shadowai/actions/workflows/ci.yml)
[![Release](https://github.com/KevinZhang19870314/shadowai/actions/workflows/release.yml/badge.svg)](https://github.com/KevinZhang19870314/shadowai/actions/workflows/release.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ShadowAI is a powerful Python library that uses AI technology to generate high-quality simulated data. Through a flexible rule engine, you can easily generate structured JSON data.

## 🎯 Design Philosophy

ShadowAI provides flexible and easy-to-use API design, supporting various usage scenarios from simple to complex, allowing users to get started quickly while maintaining powerful customization capabilities.

## 🆚 Comparison with Traditional Mock Libraries

### Core Differences

| Feature | ShadowAI | Traditional Mock Libraries (like faker.js) |
|---------|--------|---------------------------------------------|
| **Generation Method** | AI-powered intelligent generation | Predefined algorithms |
| **Configuration Complexity** | Minimal (description-based) | Medium (requires API combination) |
| **Data Quality** | High (semantic understanding) | Medium (template-based) |
| **Business Relevance** | Strong (context-aware) | Weak (generic patterns) |
| **Generation Speed** | Slow (AI calls) | Very fast (local computation) |
| **Extensibility** | High (AI adaptation) | Medium (requires development) |

### ShadowAI's Unique Advantages

#### 🧠 Intelligent Understanding
```python
# ShadowAI - One line of code, intelligent understanding of business meaning
shadow_ai.generate("company_email")  # Automatically generates company-formatted emails

# Traditional library - Requires manual combination of multiple APIs
faker.internet.email(
    faker.person.firstName(),
    faker.person.lastName(), 
    faker.internet.domainName()
)
```

#### 🎯 Business Scenario Driven
```python
# ShadowAI - Business rule packages ensure data logical consistency
developer_profile = RulePackage(
    name="senior_developer",
    rules=["name", "email", "programming_language", "years_experience", "github_username"]
)
# Generated data automatically maintains logical relationships: high experience corresponds to advanced programming languages
```

#### 🔧 Minimal Configuration
```python
# ShadowAI - Descriptive configuration
Rule(
    name="medical_record_id", 
    description="Generate HIPAA-compliant patient ID",
    constraints={"format": "anonymized"}
)

# Traditional library - Requires custom development
def generate_medical_id():
    # Lots of custom logic...
```

### Use Case Selection

#### ✅ Recommended ShadowAI Scenarios
- **Complex business testing**: Requires logical relationships between data
- **Prototype demonstrations**: Needs highly realistic sample data  
- **Industry-specific data**: Medical, financial, and other professional domains
- **API documentation examples**: Automatically generates business-compliant response examples
- **Rapid iteration**: Frequently adjusting data generation rules

#### ✅ Recommended Traditional Library Scenarios
- **High performance requirements**: Bulk generation of large amounts of data
- **CI/CD pipelines**: Automated testing environments
- **Simple standard data**: Basic names, emails, phone numbers
- **Offline environments**: No network connection restrictions
- **Cost-sensitive**: Avoiding AI API call costs

### 💡 Best Practice Recommendations

**Hybrid Usage Strategy** - Leverage the advantages of both:
```python
# 1. Use ShadowAI to design data templates
business_template = shadow_ai.generate(complex_business_package)

# 2. Use traditional libraries for bulk data population  
for i in range(1000):
    test_data = apply_template_with_faker(business_template)
```

**Selection Guide**:
- 🎯 Pursue **data quality** and **business relevance** → Choose **ShadowAI**
- ⚡ Pursue **generation speed** and **simplicity** → Choose **Traditional Mock Libraries**
- 🔄 Combine both → Get **best development experience**

## ✨ Features

- 🤖 **AI-driven**: Based on Agno framework, supports multiple LLM models
- 📝 **Flexible rules**: Supports rule records, rule combinations, and rule packages
- 📊 **Table generation**: Generate tabular data in Markdown, CSV, HTML, and JSON formats
- 📄 **Multi-format support**: Supports JSON and YAML format rule definitions
- 🎯 **Precise output**: Generates structured JSON data and formatted tables
- 📦 **Ready to use**: Built-in common rule packages and table templates
- ⚡ **Minimal configuration**: Descriptive configuration, quick start

## 📦 Installation

```bash
pip install shadowai
```

## 🚀 Quick Start

### Basic Usage

```python
from shadow_ai import ShadowAI

# Create ShadowAI instance
shadow_ai = ShadowAI()

# Use string directly
result = shadow_ai.generate("email")
print(result)  # {"email": "john.doe@example.com"}

# Generate multiple fields
result = shadow_ai.generate(["email", "name", "age"])
print(result)  # {"email": "...", "name": "...", "age": ...}

# Quick method
result = shadow_ai.quick("email", "name", "phone")
print(result)  # {"email": "...", "name": "...", "phone": "..."}
```

### Creating Custom Rules

```python
from shadow_ai import Rule, RuleCombination, RulePackage

# Create single rule
email_rule = Rule(name="email")
company_rule = Rule(name="company_name")

# Generate data
result = shadow_ai.generate(email_rule)
print(result)  # {"email": "user@example.com"}

# Create rule combination
user_combo = RuleCombination(
    name="user_profile",
    rules=["name", "email", "phone"]
)

# Create rule package
user_package = RulePackage(
    name="user", 
    rules=["username", "email", "age", "location"]
)

result = shadow_ai.generate(user_package)
print(result)  # Complete user information
```

### Using Pre-built Rules

```python
from shadow_ai.rules import email_rule, name_rule
from shadow_ai.rules.packages import person_package

# Use predefined rules
result = shadow_ai.generate(email_rule)
print(result)  # {"email": "john.doe@example.com"}

# Use predefined packages
result = shadow_ai.generate(person_package)
print(result)
# {
#   "fullname": "John Smith", 
#   "age": 25,
#   "email": "john.smith@email.com"
# }
```

### Advanced Custom Rules

```python
from shadow_ai import Rule

# Detailed rule configuration
custom_rule = Rule(
    name="company",
    description="Generate a technology company name",
    examples=["TechCorp", "DataFlow", "CloudByte"],
    constraints={"type": "string", "style": "modern"}
)

result = shadow_ai.generate(custom_rule)
```

### Table Generation

```python
from shadow_ai import ShadowAI, TableOutputFormat, TableRule, Rule

shadow_ai = ShadowAI()

# Quick table generation
table = shadow_ai.quick_table(
    "products", 
    "id", "name", "price", "category",
    rows=5,
    output_format=TableOutputFormat.MARKDOWN
)
print(table)
# Generates a formatted Markdown table

# Use built-in templates
user_table = shadow_ai.generate_table_from_template(
    "user_profiles", 
    rows=10,
    output_format=TableOutputFormat.CSV,
    save_to_file="users.csv"
)

# Custom table with rules
custom_table = TableRule.create(
    name="survey",
    columns=[
        Rule(name="response_id").with_examples("RESP001", "RESP002"),
        Rule(name="score").with_constraints(type="integer", min=1, max=10),
        Rule(name="feedback").with_examples("Great!", "Good", "Average")
    ],
    rows_count=8
)

result = shadow_ai.generate_table(custom_table, TableOutputFormat.MARKDOWN)

# List available templates
templates = shadow_ai.list_table_templates()
print(templates)  # ['user_profiles', 'product_catalog', 'sales_data', 'employees', 'financial_data']
```

## 📖 Documentation

For detailed documentation, please check the [docs/](docs/) directory.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file. 