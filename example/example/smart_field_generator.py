import json
from typing import Dict, List, Any

from dotenv import load_dotenv
from faker import Faker
from shadow_ai import ShadowAI, Rule


class SmartFieldGenerator:
    """Smart Field Generator - Field-level mixed strategy"""

    def __init__(self, locale='en_US'):
        self.shadow_ai = ShadowAI()
        self.faker = Faker(locale)

        # Predefined Faker generator mapping
        self.faker_generators = {
            'name': lambda: self.faker.name(),
            'first_name': lambda: self.faker.first_name(),
            'last_name': lambda: self.faker.last_name(),
            'email': lambda: self.faker.email(),
            'phone': lambda: self.faker.phone_number(),
            'address': lambda: self.faker.address(),
            'company': lambda: self.faker.company(),
            'job_title': lambda: self.faker.job(),
            'age': lambda: self.faker.random_int(18, 80),
            'date': lambda: self.faker.date(),
            'url': lambda: self.faker.url(),
            'username': lambda: self.faker.user_name(),
            'price': lambda: round(self.faker.random.uniform(10, 1000), 2),
            'quantity': lambda: self.faker.random_int(1, 100),
            'id': lambda: self.faker.uuid4(),
            'rating': lambda: self.faker.random_int(1, 5),  # Add rating
        }

    def generate_mixed_data(self, field_config: Dict[str, Any], count: int = 1) -> List[Dict[str, Any]]:
        """
        Generate mixed data

        Args:
            field_config: Field configuration
                - Format 1: {"field_name": "faker_method"}  # Use Faker
                - Format 2: {"field_name": {"ai": "description"}}   # Use AI
                - Format 3: {"field_name": {"ai": "description", "context": {...}}}  # AI with context
                - Format 4: {"field_name": callable}  # Custom function
            count: Number of records to generate
        """
        results = []

        # Separate AI fields and Faker fields
        ai_fields = {}
        faker_fields = {}
        contextual_ai_fields = {}
        custom_functions = {}

        for field_name, config in field_config.items():
            if isinstance(config, dict) and 'ai' in config:
                if 'context' in config:
                    contextual_ai_fields[field_name] = config
                else:
                    ai_fields[field_name] = config['ai']
            elif callable(config):
                custom_functions[field_name] = config
            else:
                faker_fields[field_name] = config

        for i in range(count):
            record = {}

            # 1. Generate Faker fields first (fast)
            for field_name, faker_method in faker_fields.items():
                if faker_method in self.faker_generators:
                    record[field_name] = self.faker_generators[faker_method]()
                elif isinstance(faker_method, str) and hasattr(self.faker, faker_method):
                    # Handle string method names
                    record[field_name] = getattr(self.faker, faker_method)()
                else:
                    record[field_name] = f"unknown_{faker_method}"

            # 2. Generate custom function fields
            for field_name, func in custom_functions.items():
                record[field_name] = func()

            # 3. Batch generate simple AI fields
            if ai_fields:
                ai_rules = [Rule(name=field, description=desc) for field, desc in ai_fields.items()]
                try:
                    ai_data = self.shadow_ai.generate(ai_rules)
                    record.update(ai_data)
                except Exception as e:
                    print(f"AI generation failed: {e}")
                    # Use default values
                    for field in ai_fields.keys():
                        record[field] = f"ai_generated_{field}"

            # 4. Generate AI fields that need context
            for field_name, config in contextual_ai_fields.items():
                try:
                    context = config.get('context', {})
                    # Use related fields from current record as context
                    related_fields = context.get('related_fields', [])
                    context_str = ", ".join([f"{k}: {record.get(k, 'N/A')}" for k in related_fields if k in record])

                    description = config['ai']
                    if context_str:
                        description += f". Context: {context_str}"

                    ai_rule = Rule(name=field_name, description=description)
                    ai_result = self.shadow_ai.generate(ai_rule)
                    record[field_name] = ai_result.get(field_name, f"ai_generated_{field_name}")
                except Exception as e:
                    print(f"Contextual AI generation failed for {field_name}: {e}")
                    record[field_name] = f"ai_generated_{field_name}"

            results.append(record)

        return results


def generate_ecommerce_data():
    """E-commerce data generation example"""

    generator = SmartFieldGenerator()

    # Field configuration: Mixed use of Faker and AI
    ecommerce_config = {
        # Faker fields (standard, fast)
        'user_id': 'id',
        'name': 'name',
        'email': 'email',
        'phone': 'phone',
        'order_date': 'date',
        'price': 'price',
        'quantity': 'quantity',

        # AI fields (complex, semantic)
        'product_name': {'ai': 'Generate a realistic product name'},
        'product_description': {'ai': 'Generate a detailed product description'},
        'user_review': {
            'ai': 'Generate a realistic user review for the purchased product',
            'context': {'related_fields': ['product_name', 'price']}
        },
        'category': {
            'ai': 'Determine product category based on product name and description',
            'context': {'related_fields': ['product_name', 'product_description']}
        }
    }

    # Generate data
    print("🚀 Generating e-commerce mixed data...")
    data = generator.generate_mixed_data(ecommerce_config, count=2)

    for i, record in enumerate(data, 1):
        print(f"\n📦 Order {i}:")
        print(json.dumps(record, indent=2, ensure_ascii=False))

    return data


def generate_user_feedback():
    """User feedback data generation example"""

    generator = SmartFieldGenerator()

    feedback_config = {
        # Faker standard fields
        'feedback_id': 'id',
        'user_name': 'name',
        'user_email': 'email',
        'submission_date': 'date',
        'rating': 'rating',  # Fix: Use predefined rating

        # AI semantic fields
        'app_feature': {'ai': 'Generate a specific mobile app feature name'},
        'user_comment': {
            'ai': 'Generate realistic user feedback comment about the app feature',
            'context': {'related_fields': ['app_feature', 'rating']}
        },
        'sentiment': {
            'ai': 'Determine sentiment (positive/negative/neutral) based on the comment',
            'context': {'related_fields': ['user_comment', 'rating']}
        },
        'improvement_suggestion': {
            'ai': 'Generate improvement suggestion based on the feedback',
            'context': {'related_fields': ['app_feature', 'user_comment']}
        }
    }

    print("\n💬 Generating user feedback data...")
    data = generator.generate_mixed_data(feedback_config, count=2)

    for i, record in enumerate(data, 1):
        print(f"\n📝 Feedback {i}:")
        print(json.dumps(record, indent=2, ensure_ascii=False))

    return data


# If you need custom functions, you can use them like this:
def custom_example():
    """Custom function example"""

    generator = SmartFieldGenerator()

    custom_config = {
        'name': 'name',
        'email': 'email',
        'custom_rating': lambda: generator.faker.random_int(1, 5),  # Custom function
        'custom_score': lambda: round(generator.faker.random.uniform(0, 100), 1),
        'product_review': {'ai': 'Generate a product review'}
    }

    print("\n🔧 Custom function example...")
    data = generator.generate_mixed_data(custom_config, count=1)
    print(json.dumps(data[0], indent=2, ensure_ascii=False))


# Usage example
if __name__ == "__main__":
    load_dotenv()
    try:
        generate_ecommerce_data()
        generate_user_feedback()
        custom_example()
    except Exception as e:
        print(f"Execution error: {e}")
