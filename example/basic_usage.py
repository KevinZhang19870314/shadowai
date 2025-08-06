"""
ShadowAI Basic Usage Examples

Demonstrates how to use the ShadowAI library to generate various types of mock data.
"""

import os
import sys

from dotenv import load_dotenv

# Add project root directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from shadow_ai import Rule, RuleCombination, RulePackage, ShadowAI
from shadow_ai.rules import age_rule, email_rule, first_name_rule, last_name_rule
from shadow_ai.rules.combinations import full_name_combination
from shadow_ai.rules.packages import person_package

load_dotenv()


def main():
    """Main function demonstrating various usage patterns"""

    print("🚀 ShadowAI Basic Usage Examples")
    print("=" * 50)

    # Initialize ShadowAI instance
    shadow_ai = ShadowAI()

    # Example 1: Create single rules
    print("\n📝 Example 1: Create single rules")
    print("-" * 30)

    # Provide name, description will be auto-generated
    email_rule_simple = Rule(name="email")
    user_name_rule = Rule(name="user_name")
    age_rule_simple = Rule(name="age")

    result = shadow_ai.generate(email_rule_simple, format_output=False)
    print(f"Email: {result}")

    result = shadow_ai.generate(user_name_rule, format_output=False)
    print(f"Username: {result}")

    # Example 2: Use pre-built rules
    print("\n📝 Example 2: Use pre-built rules")
    print("-" * 30)

    result = shadow_ai.generate(email_rule, format_output=False)
    print(f"Email: {result}")

    result = shadow_ai.generate(first_name_rule, format_output=False)
    print(f"First name: {result}")

    # Example 3: String-based creation
    print("\n📝 Example 3: String-based creation")
    print("-" * 30)

    result = shadow_ai.generate("phone", format_output=False)
    print(f"Phone number: {result}")

    result = shadow_ai.generate("company_name", format_output=False)
    print(f"Company name: {result}")

    # Use string list
    string_fields = ["email", "name", "age"]
    result = shadow_ai.generate(string_fields, format_output=False)
    print(f"Field combination: {result}")

    # Example 4: Generate data using multiple rules
    print("\n📝 Example 4: Multiple rule combination")
    print("-" * 30)

    rules = [first_name_rule, last_name_rule, age_rule, email_rule]
    result = shadow_ai.generate(rules, format_output=False)
    print(f"Multi-field data: {result}")

    # Example 5: Create rule combinations
    print("\n📝 Example 5: Create rule combinations")
    print("-" * 30)

    # Provide name and rule list, description will be auto-generated
    user_combo = RuleCombination(name="user_profile", rules=["first_name", "last_name", "email"])
    result = shadow_ai.generate(user_combo, format_output=False)
    print(f"User combination: {result}")

    # Use pre-built combination
    result = shadow_ai.generate(full_name_combination, format_output=False)
    print(f"Full name combination: {result}")

    # Example 6: Create rule packages
    print("\n📝 Example 6: Create rule packages")
    print("-" * 30)

    # Provide name and rule list, description will be auto-generated
    user_package = RulePackage(name="basic_user", rules=["username", "email", "phone", "age"])
    result = shadow_ai.generate(user_package, format_output=False)
    print(f"User package: {result}")

    # Use pre-built package
    result = shadow_ai.generate(person_package, format_output=False)
    print(f"Personal information: {result}")

    # Example 7: Generate multiple records
    print("\n📝 Example 7: Batch generation")
    print("-" * 30)

    result = shadow_ai.generate(user_package, count=3, format_output=False)
    print(f"Multiple user information: {result}")

    # Example 8: Use formatted output
    print("\n📝 Example 8: Formatted output")
    print("-" * 30)

    response = shadow_ai.generate(user_package, format_output=True)
    print(f"Formatted response:")
    print(f"  Success: {response.success}")
    print(f"  Data: {response.data}")
    print(f"  Metadata: {response.metadata}")

    # Example 9: Various usage methods
    print("\n📝 Example 9: Various usage methods")
    print("-" * 30)

    print("✅ Quick creation methods:")
    print("   Rule(name='email')  # Auto-generate description")
    print("   shadow_ai.generate('phone')  # Use string directly")
    print("   RuleCombination(name='user', rules=['name', 'email'])")
    print("   RulePackage(name='person', rules=['name', 'age', 'email'])")

    print("\n💡 Pre-built rules:")
    print("   email_rule  # Pre-built rule")
    print("   full_name_combination  # Pre-built combination")
    print("   person_package  # Pre-built package")


if __name__ == "__main__":
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        main()
    except Exception as e:
        print(f"❌ Execution error: {e}")
        print(
            "Please ensure all dependencies are installed: pip install agno openai pydantic pyyaml"
        )
