#!/usr/bin/env python3
"""
MockAI Quick Start Script

Helps users quickly experience MockAI functionality.
"""

import json
import os
import sys


def check_dependencies():
    """Check if dependencies are installed"""
    print("🔍 Checking dependencies...")

    required_packages = ["agno", "pydantic", "yaml"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not installed")

    if missing_packages:
        print(f"\nPlease install missing dependencies:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    return True


def check_api_key():
    """Check API key"""
    print("\n🔑 Checking API key...")

    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY is set")
        return "openai"
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("✅ ANTHROPIC_API_KEY is set")
        return "anthropic"
    else:
        print("⚠️ No API key set")
        print("Please set one of the following environment variables:")
        print("  export OPENAI_API_KEY=your_openai_key")
        print("  export ANTHROPIC_API_KEY=your_anthropic_key")
        return None


def demonstrate_basic_usage():
    """Demonstrate basic usage"""
    print("\n🚀 Basic Usage Demo")
    print("=" * 30)

    # Add project path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_path = os.path.join(project_root, "lib")
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

    try:
        from mock_ai import MockAI
        from mock_ai.rules import email_rule, first_name_rule
        from mock_ai.rules.packages import person_package

        # Initialize MockAI
        mock_ai = MockAI()

        # Example 1: Generate email
        print("\n📧 Example 1: Generate email")
        print("-" * 25)
        try:
            result = mock_ai.generate(email_rule, format_output=False)
            print(f"Generated email: {result}")
        except Exception as e:
            print(f"❌ Email generation failed: {e}")

        # Example 2: Generate name
        print("\n👤 Example 2: Generate name")
        print("-" * 25)
        try:
            result = mock_ai.generate(first_name_rule, format_output=False)
            print(f"Generated name: {result}")
        except Exception as e:
            print(f"❌ Name generation failed: {e}")

        # Example 3: Generate using strings
        print("\n🎯 Example 3: String-based generation")
        print("-" * 35)
        try:
            result = mock_ai.generate("phone", format_output=False)
            print(f"Generated phone: {result}")

            result = mock_ai.generate("company_name", format_output=False)
            print(f"Generated company: {result}")
        except Exception as e:
            print(f"❌ String-based generation failed: {e}")

        # Example 4: Generate using rule package
        print("\n📦 Example 4: Generate using rule package")
        print("-" * 40)
        try:
            result = mock_ai.generate(person_package, format_output=False)
            print(f"Generated person: {result}")
        except Exception as e:
            print(f"❌ Package generation failed: {e}")

        # Example 5: Batch generation
        print("\n🔄 Example 5: Batch generation")
        print("-" * 30)
        try:
            result = mock_ai.generate(person_package, count=2, format_output=False)
            print(f"Generated multiple people: {result}")
        except Exception as e:
            print(f"❌ Batch generation failed: {e}")

        print("\n✅ Basic demos completed!")

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please ensure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Demo execution failed: {e}")


def show_available_rules():
    """Show available pre-built rules"""
    print("\n📚 Available Pre-built Rules")
    print("=" * 35)

    # Add project path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_path = os.path.join(project_root, "lib")
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

    try:
        from mock_ai.rules import (
            address_rule,
            age_rule,
            company_rule,
            email_rule,
            first_name_rule,
            last_name_rule,
            phone_rule,
        )
        from mock_ai.rules.combinations import (
            full_address_combination,
            full_name_combination,
        )
        from mock_ai.rules.packages import company_package, person_package, user_package

        print("\n🔧 Basic Rules:")
        rules = [
            ("email_rule", email_rule),
            ("first_name_rule", first_name_rule),
            ("last_name_rule", last_name_rule),
            ("age_rule", age_rule),
            ("phone_rule", phone_rule),
            ("address_rule", address_rule),
            ("company_rule", company_rule),
        ]

        for name, rule in rules:
            print(f"  • {name}: {rule.description}")

        print("\n🔗 Rule Combinations:")
        combinations = [
            ("full_name_combination", full_name_combination),
            ("full_address_combination", full_address_combination),
        ]

        for name, combo in combinations:
            print(f"  • {name}: {combo.description}")

        print("\n📦 Rule Packages:")
        packages = [
            ("person_package", person_package),
            ("company_package", company_package),
            ("user_package", user_package),
        ]

        for name, package in packages:
            print(f"  • {name}: {package.description}")

    except ImportError as e:
        print(f"❌ Failed to load rules: {e}")


def interactive_demo():
    """Interactive demo menu"""
    print("\n🎮 Interactive Demo")
    print("=" * 20)

    while True:
        print("\nChoose an option:")
        print("1. Basic usage demo")
        print("2. Show available rules")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            demonstrate_basic_usage()
        elif choice == "2":
            show_available_rules()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Main function"""
    print("🎊 Welcome to MockAI Quick Start!")
    print("=" * 40)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies check failed. Please install missing packages.")
        return

    # Check API key
    api_provider = check_api_key()
    if not api_provider:
        print("\n❌ API key check failed. Please set API key.")
        return

    print(f"\n✅ Environment setup complete! Using {api_provider} API.")

    # Show quick help
    print("\n💡 Quick Tips:")
    print("  • Make sure you're running from the project root directory")
    print("  • All examples use the MockAI library from lib/ directory")
    print("  • Generated data may vary each time due to AI randomness")

    # Start interactive demo
    interactive_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 User interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your environment and try again.")
