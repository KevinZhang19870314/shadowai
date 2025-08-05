# ShadowAI Quick Start Guide

🚀 Welcome to ShadowAI! This is an AI-powered intelligent mock data generation library.

## 📦 Installation

### Basic Installation

```bash
pip install agno pydantic pyyaml typing-extensions
```

### Full Installation (Recommended)

```bash
# Clone the project
git clone https://github.com/your-username/shadowai.git
cd shadowai

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

## 🔑 Setting Up API Keys

ShadowAI requires AI services to generate data. Please set one of the following environment variables:

```bash
# OpenAI
export OPENAI_API_KEY=your_openai_api_key

# or Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 🚀 Quick Experience

Run the quick start wizard:

```bash
python scripts/quickstart.py
```

## 📝 Basic Usage

### 1. Simple Example

```python
from shadowai import ShadowAI
from shadowai.rules import email_rule, first_name_rule

# Create ShadowAI instance
shadowai = ShadowAI()

# Generate email
email = shadowai.generate(email_rule, format_output=False)
print(f"Email: {email}")

# Generate name
name = shadowai.generate(first_name_rule, format_output=False)
print(f"Name: {name}")
```

### 2. Using Rule Packages

```python
from shadowai.rules.packages import person_package

# Generate complete personal information
person = shadowai.generate(person_package, format_output=False)
print(person)
# Output: {"full_name": "John Smith", "age": 30, "email": "john@example.com", ...}
```

### 3. Batch Generation

```python
# Generate multiple records
people = shadowai.generate(person_package, count=5, format_output=False)
for person in people:
    print(person["full_name"])
```

## 🎨 Custom Rules

### Creating Single Rules

```python
from shadowai import Rule

# Create custom rule
product_rule = Rule(
    name="product_name",
    description="Generate a creative tech product name",
    examples=["SmartWidget", "DataFlow Pro", "CodeNinja"],
    constraints={"style": "tech", "length": "5-20"}
)

# Use custom rule
result = shadowai.generate(product_rule, format_output=False)
```

### Creating Rule Combinations

```python
from shadowai import RuleCombination

# Create rule combination
tech_skill = RuleCombination(
    name="tech_skill",
    description="Combine programming language with skill level",
    rules=["programming_language", "skill_level"],
    combination_logic="and"
)
```

### Creating Rule Packages

```python
from shadowai import RulePackage

# Create rule package
developer_package = RulePackage(
    name="developer",
    description="Complete developer profile",
    rules=[
        "name",
        "email", 
        tech_skill,
        "years_experience"
    ],
    category="tech"
)
```

## 📁 File Operations

### Saving Rules to Files

```python
from shadowai.utils.file_utils import save_rules_to_json, save_rules_to_yaml

# Save as JSON
save_rules_to_json(person_package, "rules/person.json")

# Save as YAML
save_rules_to_yaml(person_package, "rules/person.yaml")
```

### Loading Rules from Files

```python
from shadowai.utils.file_utils import load_rules_from_json

# Load from file
rules = load_rules_from_json("rules/person.json")
result = shadowai.generate(rules, format_output=False)
```

## 🛠️ Development Tools

### Using Makefile

```bash
# View available commands
make help

# Setup development environment
make dev

# Format code
make format

# Run tests
make test

# Build package
make build

# Run examples
make example-basic
make example-custom
make example-file
```

### Manual Operations

```bash
# Format code
black lib/ example/ scripts/
isort lib/ example/ scripts/

# Check code quality
flake8 lib/
mypy lib/ --ignore-missing-imports

# Run examples
python example/basic_usage.py
python example/custom_rules.py
python example/file_loading.py
```

## 📚 Built-in Rules

ShadowAI provides rich built-in rules:

### Basic Rules

- `email_rule` - Email address
- `first_name_rule` - First name
- `last_name_rule` - Last name
- `age_rule` - Age
- `phone_rule` - Phone number
- `address_rule` - Address
- `company_rule` - Company name
- `price_rule` - Price

### Rule Combinations

- `full_name_combination` - Full name
- `full_address_combination` - Complete address
- `datetime_combination` - Date and time

### Rule Packages

- `person_package` - Personal information
- `company_package` - Company information
- `product_package` - Product information
- `user_package` - User information

## 🚀 Publishing to PyPI

```bash
# Test publish
python scripts/publish.py --test --version 0.1.1

# Production publish
python scripts/publish.py --version 0.1.1
```

## ❓ FAQ

### Q: How to switch AI models?

```python
# Use different models
shadowai = ShadowAI(model_id="gpt-4")

# Use Anthropic models
from agno.models.anthropic import Claude
shadowai = ShadowAI(model=Claude(id="claude-3-sonnet"))
```

### Q: How to handle generation errors?

```python
# Use formatted output to get error information
response = shadowai.generate(rule, format_output=True)
if not response.success:
    print(f"Generation failed: {response.error}")
```

### Q: How to customize generation logic?

Guide AI generation through constraints and examples:

```python
custom_rule = Rule(
    name="special_id",
    description="Generate a special ID format",
    examples=["USR-2024-001", "USR-2024-002"],
    constraints={
        "format": "USR-YYYY-NNN",
        "prefix": "USR",
        "year": 2024
    }
)
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

🎉 Now you've mastered the basic usage of ShadowAI! Start creating your own intelligent mock data! 