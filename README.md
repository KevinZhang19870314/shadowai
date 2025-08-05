# MockAI

🚀 An AI-powered intelligent mock data generation library

MockAI is a powerful Python library that uses AI technology to generate high-quality simulated data. Through a flexible rule engine, you can easily generate structured JSON data.

## 🎯 Design Philosophy

MockAI provides flexible and easy-to-use API design, supporting various usage scenarios from simple to complex, allowing users to get started quickly while maintaining powerful customization capabilities.

## 🆚 Comparison with Traditional Mock Libraries

### Core Differences

| Feature | MockAI | Traditional Mock Libraries (like faker.js) |
|---------|--------|---------------------------------------------|
| **Generation Method** | AI-powered intelligent generation | Predefined algorithms |
| **Configuration Complexity** | Minimal (description-based) | Medium (requires API combination) |
| **Data Quality** | High (semantic understanding) | Medium (template-based) |
| **Business Relevance** | Strong (context-aware) | Weak (generic patterns) |
| **Generation Speed** | Slow (AI calls) | Very fast (local computation) |
| **Extensibility** | High (AI adaptation) | Medium (requires development) |

### MockAI's Unique Advantages

#### 🧠 Intelligent Understanding
```python
# MockAI - One line of code, intelligent understanding of business meaning
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
# MockAI - Business rule packages ensure data logical consistency
developer_profile = RulePackage(
    name="senior_developer",
    rules=["name", "email", "programming_language", "years_experience", "github_username"]
)
# Generated data automatically maintains logical relationships: high experience corresponds to advanced programming languages
```

#### 🔧 Minimal Configuration
```python
# MockAI - Descriptive configuration
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

#### ✅ Recommended MockAI Scenarios
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
# 1. Use MockAI to design data templates
business_template = shadow_ai.generate(complex_business_package)

# 2. Use traditional libraries for bulk data population  
for i in range(1000):
    test_data = apply_template_with_faker(business_template)
```

**Selection Guide**:
- 🎯 Pursue **data quality** and **business relevance** → Choose **MockAI**
- ⚡ Pursue **generation speed** and **simplicity** → Choose **Traditional Mock Libraries**
- 🔄 Combine both → Get **best development experience**

## ✨ Features

- 🤖 **AI-driven**: Based on Agno framework, supports multiple LLM models
- 📝 **Flexible rules**: Supports rule records, rule combinations, and rule packages
- 📄 **Multi-format support**: Supports JSON and YAML format rule definitions
- 🎯 **Precise output**: Generates structured JSON data
- 📦 **Ready to use**: Built-in common rule packages
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

## 📖 Documentation

For detailed documentation, please check the [docs/](docs/) directory.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file. 