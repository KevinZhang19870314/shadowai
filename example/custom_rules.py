"""
ShadowAI Custom Rules Examples

Demonstrates how to create and use custom rules.
"""

import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from shadow_ai import ShadowAI, Rule, RuleCombination, RulePackage


def create_basic_rules():
    """Create basic custom rules"""

    print("🚀 Method 1: Basic Creation")
    print("-" * 30)

    # Basic method: provide name, description auto-generated
    language_rule = Rule(name="programming_language")
    framework_rule = Rule(name="web_framework")
    skill_rule = Rule(name="skill_level")

    print(f"Language rule: {language_rule.name} - {language_rule.description}")
    print(f"Framework rule: {framework_rule.name} - {framework_rule.description}")
    print(f"Skill rule: {skill_rule.name} - {skill_rule.description}")

    return language_rule, framework_rule, skill_rule


def create_rules_with_examples():
    """Create rules with examples"""

    print("\n🎯 Method 2: Rules with Examples")
    print("-" * 30)

    # Name + examples, description auto-generated
    language_rule = Rule(
        name="programming_language",
        examples=["Python", "JavaScript", "Java", "Go", "Rust"],
    )

    framework_rule = Rule(
        name="framework",
        examples=["React", "Vue.js", "Django", "FastAPI", "Express.js"],
    )

    skill_rule = Rule(
        name="skill_level", examples=["Beginner", "Intermediate", "Advanced", "Expert"]
    )

    print(f"Language rule: {language_rule.description}")
    print(f"Examples: {language_rule.examples}")

    return language_rule, framework_rule, skill_rule


def create_detailed_rules():
    """Create detailed configured rules"""

    print("\n📋 Method 3: Detailed Configuration")
    print("-" * 30)

    # Full configuration, suitable for complex scenarios
    programming_language_rule = Rule(
        name="programming_language",
        description="Generate a popular programming language name",
        examples=["Python", "JavaScript", "Java", "Go", "Rust"],
        constraints={"type": "string", "popular": True},
    )

    framework_rule = Rule(
        name="framework",
        description="Generate a web development framework",
        examples=["React", "Vue.js", "Django", "FastAPI", "Express.js"],
        constraints={"type": "string", "category": "web_development"},
    )

    tech_skill_rule = Rule(
        name="skill_level",
        description="Generate a skill proficiency level",
        examples=["Beginner", "Intermediate", "Advanced", "Expert"],
        constraints={"type": "string", "levels": 4},
    )

    print(f"Language rule: {programming_language_rule.description}")
    print(f"Constraints: {programming_language_rule.constraints}")

    return programming_language_rule, framework_rule, tech_skill_rule


def create_basic_combinations():
    """Create basic rule combinations"""

    print("\n🔗 Method 4: Create Rule Combinations")
    print("-" * 30)

    # Provide name and rule list, description auto-generated
    tech_skill_combo = RuleCombination(
        name="tech_skill", rules=["programming_language", "skill_level"]
    )

    tech_stack_combo = RuleCombination(
        name="tech_stack", rules=["programming_language", "framework"]
    )

    developer_profile_combo = RuleCombination(
        name="developer_profile",
        rules=["name", "email", "programming_language", "skill_level"],
    )

    print(f"Skill combination: {tech_skill_combo.description}")
    print(f"Tech stack combination: {tech_stack_combo.description}")
    print(f"Developer profile: {developer_profile_combo.description}")

    return tech_skill_combo, tech_stack_combo, developer_profile_combo


def create_detailed_combinations():
    """Create detailed configured rule combinations"""

    print("\n📋 Method 5: Detailed Rule Combination Configuration")
    print("-" * 35)

    # Full configuration, suitable for complex scenarios
    tech_skill_combination = RuleCombination(
        name="tech_skill",
        description="Combine programming language with skill level",
        rules=["programming_language", "skill_level"],
        combination_logic="combine",
    )

    tech_stack_combination = RuleCombination(
        name="tech_stack",
        description="Combine programming language with framework",
        rules=["programming_language", "framework"],
        combination_logic="combine",
    )

    print(f"Skill combination: {tech_skill_combination.description}")
    print(f"Combination logic: {tech_skill_combination.combination_logic}")

    return tech_skill_combination, tech_stack_combination


def create_basic_packages():
    """Create basic rule packages"""

    print("\n📦 Method 6: Create Rule Packages")
    print("-" * 30)

    # Provide name and rule list, description auto-generated
    developer_package = RulePackage(
        name="developer",
        rules=[
            "name",
            "email",
            "programming_language",
            "skill_level",
            "years_experience",
            "github_username",
        ],
    )

    startup_package = RulePackage(
        name="startup",
        rules=[
            "company_name",
            "description",
            "funding_stage",
            "founded_year",
            "employee_count",
            "location",
        ],
    )

    project_package = RulePackage(
        name="project",
        rules=[
            "project_name",
            "description",
            "programming_language",
            "framework",
            "status",
        ],
    )

    print(f"Developer package: {developer_package.description}")
    print(f"Startup package: {startup_package.description}")
    print(f"Project package: {project_package.description}")

    return developer_package, startup_package, project_package


def create_detailed_packages():
    """Create detailed configured rule packages"""

    print("\n📋 Method 7: Detailed Rule Package Configuration")
    print("-" * 35)

    # Full configuration, suitable for complex scenarios
    developer_package = RulePackage(
        name="developer",
        description="Complete developer profile information",
        rules=[
            "name",
            "email",
            "programming_language",
            "skill_level",
            "years_experience",
            "github_username",
        ],
        category="tech",
        version="1.0.0",
    )

    print(f"Developer package: {developer_package.description}")
    print(f"Category: {developer_package.category}")
    print(f"Version: {developer_package.version}")

    return developer_package


def demonstrate_data_generation():
    """Demonstrate data generation"""

    print("\n🎮 Data Generation Demo")
    print("=" * 50)

    # Initialize ShadowAI instance
    shadow_ai = ShadowAI()

    # Get created rules and packages
    basic_rules = create_basic_rules()
    example_rules = create_rules_with_examples()
    basic_combos = create_basic_combinations()
    basic_packages = create_basic_packages()

    print("\n🔧 Generate data using rules:")
    print("-" * 30)

    try:
        # Generate data using rules
        result = shadow_ai.generate(basic_rules[0], format_output=False)  # language_rule
        print(f"Programming language: {result}")

        result = shadow_ai.generate(
            example_rules[1], format_output=False
        )  # framework_rule
        print(f"Framework: {result}")

        # Generate data using combinations
        result = shadow_ai.generate(
            basic_combos[0], format_output=False
        )  # tech_skill_combo
        print(f"Tech skill combination: {result}")

        # Generate data using packages
        result = shadow_ai.generate(
            basic_packages[0], format_output=False
        )  # developer_package
        print(f"Developer information: {result}")

        # Batch generation
        result = shadow_ai.generate(
            basic_packages[2], count=2, format_output=False
        )  # project_package
        print(f"Multiple projects: {result}")

    except Exception as e:
        print(f"❌ Error generating data: {e}")
        print("This might be due to missing API key or network issues")


def main():
    """Main function demonstrating custom rule creation"""

    print("🎨 ShadowAI Custom Rules Examples")
    print("=" * 50)
    print("Shows how to create and use custom rules, combinations and packages")

    # Demonstrate various creation methods
    create_basic_rules()
    create_rules_with_examples()
    create_detailed_rules()
    create_basic_combinations()
    create_detailed_combinations()
    create_basic_packages()
    create_detailed_packages()

    # Demonstrate data generation
    demonstrate_data_generation()

    print("\n🎯 Summary:")
    print("=" * 30)
    print("✅ Quick creation methods:")
    print("   • Rule(name='field_name')  # Auto-generate description")
    print("   • RuleCombination(name='combo', rules=['field1', 'field2'])")
    print("   • RulePackage(name='package', rules=['field1', 'field2', 'field3'])")
    print("   • Support direct string generation: shadow_ai.generate('field_name')")
    print("\n✅ Detailed configuration suitable for complex scenarios")
    print("✅ Flexible API design meets different needs")


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
