"""
ShadowAI File Loading Examples

Demonstrates how to load rules from JSON and YAML files.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Add project root directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from shadow_ai import ShadowAI
from shadow_ai.rules.packages import person_package
from shadow_ai.utils.file_utils import (
    create_rule_template,
    load_rules_from_json,
    load_rules_from_yaml,
    save_rules_to_json,
    save_rules_to_yaml,
)


def create_sample_rule_files():
    """Create sample rule files"""

    # Create sample rules
    sample_rules = [
        create_rule_template("record"),
        create_rule_template("combination"),
        create_rule_template("package"),
    ]

    # Custom sample rules
    sample_rules[0].update(
        {
            "name": "product_name",
            "description": "Generate a creative product name",
            "examples": ["Super Widget", "Magic Tool", "Smart Device"],
            "constraints": {"length": "10-50", "creative": True},
        }
    )

    sample_rules[1].update(
        {
            "name": "full_product_info",
            "description": "Combine product name with category",
            "rules": ["product_name", "category"],
        }
    )

    sample_rules[2].update(
        {
            "name": "ecommerce_product",
            "description": "Complete ecommerce product information",
            "rules": ["product_name", "description", "price", "category", "brand"],
        }
    )

    return sample_rules


def demonstrate_json_operations():
    """Demonstrate JSON file operations"""

    print("📄 JSON File Operations")
    print("=" * 30)

    # Create demo_output directory
    output_dir = "demo_output"
    os.makedirs(output_dir, exist_ok=True)

    # Save rules to JSON
    print("\n💾 Saving rules to JSON...")
    json_path = os.path.join(output_dir, "person_package.json")
    save_rules_to_json(person_package, json_path)
    print(f"✅ Saved person_package to: {json_path}")

    # Save custom sample rules
    sample_rules = create_sample_rule_files()
    for i, rule in enumerate(sample_rules):
        rule_path = os.path.join(output_dir, f"sample_rule_{i+1}.json")
        save_rules_to_json(rule, rule_path)
        print(f"✅ Saved sample rule {i+1} to: {rule_path}")

    # Load rules from JSON
    print("\n📖 Loading rules from JSON...")
    loaded_person = load_rules_from_json(json_path)
    print(f"✅ Loaded person package: {loaded_person['name']}")
    print(f"   Description: {loaded_person['description']}")
    print(f"   Rules count: {len(loaded_person['rules'])}")

    return loaded_person, sample_rules


def demonstrate_yaml_operations():
    """Demonstrate YAML file operations"""

    print("\n📄 YAML File Operations")
    print("=" * 30)

    # Create demo_output directory
    output_dir = "demo_output"
    os.makedirs(output_dir, exist_ok=True)

    # Save rules to YAML
    print("\n💾 Saving rules to YAML...")
    yaml_path = os.path.join(output_dir, "person_package.yaml")
    save_rules_to_yaml(person_package, yaml_path)
    print(f"✅ Saved person_package to: {yaml_path}")

    # Save custom sample rules
    sample_rules = create_sample_rule_files()
    for i, rule in enumerate(sample_rules):
        rule_path = os.path.join(output_dir, f"sample_rule_{i+1}.yaml")
        save_rules_to_yaml(rule, rule_path)
        print(f"✅ Saved sample rule {i+1} to: {rule_path}")

    # Load rules from YAML
    print("\n📖 Loading rules from YAML...")
    loaded_person = load_rules_from_yaml(yaml_path)
    print(f"✅ Loaded person package: {loaded_person['name']}")
    print(f"   Description: {loaded_person['description']}")
    print(f"   Rules count: {len(loaded_person['rules'])}")

    return loaded_person


def demonstrate_data_generation_from_files():
    """Demonstrate data generation from loaded files"""

    print("\n🎮 Data Generation from Files")
    print("=" * 35)

    # Initialize ShadowAI
    shadow_ai = ShadowAI()

    # Load rules from files
    output_dir = "demo_output"

    try:
        # Load and use JSON rules
        json_path = os.path.join(output_dir, "person_package.json")
        if os.path.exists(json_path):
            json_rules = load_rules_from_json(json_path)
            print(f"\n🔧 Using JSON loaded rules:")
            result = shadow_ai.generate(json_rules, format_output=False)
            print(f"Generated person: {result}")

        # Load and use YAML rules
        yaml_path = os.path.join(output_dir, "person_package.yaml")
        if os.path.exists(yaml_path):
            yaml_rules = load_rules_from_yaml(yaml_path)
            print(f"\n🔧 Using YAML loaded rules:")
            result = shadow_ai.generate(yaml_rules, format_output=False)
            print(f"Generated person: {result}")

        # Load and use sample rules
        sample_rule_path = os.path.join(output_dir, "sample_rule_3.json")
        if os.path.exists(sample_rule_path):
            sample_rules = load_rules_from_json(sample_rule_path)
            print(f"\n🔧 Using sample rule package:")
            result = shadow_ai.generate(sample_rules, format_output=False)
            print(f"Generated product: {result}")

    except Exception as e:
        print(f"❌ Error generating data: {e}")
        print("This might be due to missing API key or network issues")


def demonstrate_file_templates():
    """Demonstrate rule template creation"""

    print("\n📋 Rule Template Creation")
    print("=" * 30)

    # Create templates for different rule types
    record_template = create_rule_template("record")
    combination_template = create_rule_template("combination")
    package_template = create_rule_template("package")

    print("🏗️ Created rule templates:")
    print(f"Record template: {record_template}")
    print(f"Combination template: {combination_template}")
    print(f"Package template: {package_template}")

    # Save templates to files
    output_dir = "demo_output"
    templates = [
        ("record_template.json", record_template),
        ("combination_template.json", combination_template),
        ("package_template.json", package_template),
    ]

    print("\n💾 Saving templates to files:")
    for filename, template in templates:
        filepath = os.path.join(output_dir, filename)
        save_rules_to_json(template, filepath)
        print(f"✅ Saved {filename}")


def main():
    """Main function demonstrating file operations"""

    print("📁 MockAI File Loading Examples")
    print("=" * 50)
    print("Shows how to save and load rules from JSON and YAML files")

    # Demonstrate various file operations
    demonstrate_json_operations()
    demonstrate_yaml_operations()
    demonstrate_file_templates()
    demonstrate_data_generation_from_files()

    print("\n🎯 Summary:")
    print("=" * 30)
    print("✅ Supported file formats:")
    print("   • JSON - save_rules_to_json() / load_rules_from_json()")
    print("   • YAML - save_rules_to_yaml() / load_rules_from_yaml()")
    print("\n✅ Template creation:")
    print("   • create_rule_template('record')")
    print("   • create_rule_template('combination')")
    print("   • create_rule_template('package')")
    print("\n✅ All files saved to demo_output/ directory")
    print("✅ Support for both loading and generating from files")


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
