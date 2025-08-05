"""
RulePackage Class Unit Tests

Tests all functionality of the RulePackage class, including creation, validation, methods, etc.
"""

import pytest
from pydantic import ValidationError
from shadow_ai import Rule, RuleCombination, RulePackage


class TestRulePackageCreation:
    """Test RulePackage creation functionality"""

    def test_create_package_basic(self):
        """Test basic RulePackage creation"""
        package = RulePackage(name="person", rules=["name", "email", "age"])

        assert package.name == "person"
        assert package.description == "A collection of rules for person"
        assert package.rules == ["name", "email", "age"]
        assert package.category is None
        assert package.version == "1.0.0"

    def test_create_package_with_rule_objects(self):
        """Test creating RulePackage with Rule objects"""
        rule1 = Rule(name="name")
        rule2 = Rule(name="email")
        combo = RuleCombination(name="contact", rules=["email", "phone"])

        package = RulePackage(name="user_profile", rules=[rule1, rule2, combo])

        assert package.name == "user_profile"
        assert len(package.rules) == 3
        assert package.rules[0] == rule1
        assert package.rules[1] == rule2
        assert package.rules[2] == combo

    def test_create_package_full_config(self):
        """Test creation with full configuration"""
        package = RulePackage(
            name="employee",
            description="Employee information package",
            rules=["name", "email", "department", "salary"],
            category="hr",
            version="2.1.0",
        )

        assert package.name == "employee"
        assert package.description == "Employee information package"
        assert package.rules == ["name", "email", "department", "salary"]
        assert package.category == "hr"
        assert package.version == "2.1.0"

    def test_create_package_mixed_rules(self):
        """Test creating with mixed type rules"""
        rule = Rule(name="name")
        combo = RuleCombination(name="contact", rules=["email", "phone"])

        package = RulePackage(
            name="mixed_package", rules=[rule, combo, "age", "location"]
        )

        assert package.name == "mixed_package"
        assert len(package.rules) == 4
        assert package.rules[0] == rule
        assert package.rules[1] == combo
        assert package.rules[2] == "age"
        assert package.rules[3] == "location"


class TestRulePackageAutoDescription:
    """Test RulePackage auto-description generation"""

    def test_auto_description_simple(self):
        """Test auto-description generation for simple package names"""
        package = RulePackage(name="user", rules=["name", "email"])

        assert package.description == "A collection of rules for user"

    def test_auto_description_underscore_name(self):
        """Test description generation for names with underscores"""
        package = RulePackage(name="user_profile", rules=["name", "email"])

        assert package.description == "A collection of rules for user profile"

    def test_auto_description_complex_name(self):
        """Test description generation for complex package names"""
        package = RulePackage(
            name="employee_contact_info", rules=["name", "email", "phone"]
        )

        assert package.description == "A collection of rules for employee contact info"


class TestRulePackageValidation:
    """Test RulePackage validation functionality"""

    def test_empty_name_raises_error(self):
        """Test empty name raises error"""
        with pytest.raises(ValidationError):
            RulePackage(name="", rules=["name"])

    def test_none_name_raises_error(self):
        """Test None name raises error"""
        with pytest.raises((ValidationError, TypeError)):
            RulePackage(name=None, rules=["name"])

    def test_invalid_rules_type_raises_error(self):
        """Test invalid rules type raises error"""
        with pytest.raises(ValidationError):
            RulePackage(name="test", rules="invalid")  # should be a list

    def test_empty_rules_list_valid(self):
        """Test empty rules list is valid"""
        package = RulePackage(name="empty", rules=[])
        assert package.name == "empty"
        assert package.rules == []


class TestRulePackageSimpleCreation:
    """Test RulePackage.simple() method"""

    def test_simple_creation(self):
        """Test simple creation"""
        # Use quick method instead of simple method
        package = RulePackage.quick("user", "name", "email", "age")

        assert package.name == "user"
        assert package.rules == ["name", "email", "age"]
        assert "user" in package.description

    def test_simple_string_parsing(self):
        """Test string parsing creation"""
        package = RulePackage.simple("person [name, email, age, phone]")

        assert package.name == "person"
        assert "name" in package.rules
        assert "email" in package.rules
        assert "age" in package.rules
        assert "phone" in package.rules


class TestRulePackageFromRules:
    """Test RulePackage.from_rules() method"""

    def test_from_rules_basic(self):
        """Test creating package from rules"""
        rule1 = Rule(name="name")
        rule2 = Rule(name="email")

        package = RulePackage.from_rules("user", [rule1, rule2])

        assert package.name == "user"
        assert len(package.rules) == 2
        assert package.rules[0] == rule1
        assert package.rules[1] == rule2

    def test_from_rules_mixed(self):
        """Test creating package from mixed type rules"""
        rule = Rule(name="name")
        combo = RuleCombination(name="contact", rules=["email", "phone"])

        package = RulePackage.from_rules("profile", [rule, combo, "age"])

        assert package.name == "profile"
        assert len(package.rules) == 3
        assert package.rules[0] == rule
        assert package.rules[1] == combo
        assert package.rules[2] == "age"


class TestRulePackageChainMethods:
    """Test RulePackage chain methods"""

    def test_add_rule_method(self):
        """Test add_rule method"""
        package = (
            RulePackage(name="test", rules=["name"]).add_rule("email").add_rule("phone")
        )

        assert len(package.rules) == 3
        assert "name" in package.rules
        assert "email" in package.rules
        assert "phone" in package.rules

    def test_with_category_method(self):
        """Test with_category method"""
        package = RulePackage(name="user", rules=["name", "email"]).with_category(
            "users"
        )

        assert package.category == "users"

    def test_with_version_method(self):
        """Test with_version method"""
        package = RulePackage(name="user", rules=["name", "email"]).with_version(
            "2.0.0"
        )

        assert package.version == "2.0.0"

    def test_chain_multiple_methods(self):
        """Test chaining multiple methods"""
        package = (
            RulePackage(name="product", rules=["name", "price"])
            .add_rule("description")
            .with_category("products")
            .with_version("1.5.0")
        )

        assert len(package.rules) == 3
        assert package.category == "products"
        assert package.version == "1.5.0"


class TestRulePackagePromptGeneration:
    """Test RulePackage prompt generation"""

    def test_to_prompt_basic(self):
        """Test basic prompt generation"""
        package = RulePackage(name="user", rules=["name", "email", "age"])
        prompt = package.to_prompt()

        assert "user" in prompt
        assert "name" in prompt
        assert "email" in prompt
        assert "age" in prompt

    def test_to_prompt_with_category(self):
        """Test prompt generation with category"""
        package = RulePackage(
            name="employee", rules=["name", "department"], category="hr"
        )
        prompt = package.to_prompt()

        assert "employee" in prompt
        assert "hr" in prompt

    def test_to_prompt_with_rule_objects(self):
        """Test prompt generation with Rule objects"""
        rule = Rule(name="name", description="Full name of person")
        package = RulePackage(name="person", rules=[rule, "age"])
        prompt = package.to_prompt()

        assert "person" in prompt
        assert "name" in prompt
        assert "age" in prompt


class TestRulePackageDictSerialization:
    """Test RulePackage dictionary serialization"""

    def test_to_dict_basic(self):
        """Test basic dictionary conversion"""
        package = RulePackage(name="user", rules=["name", "email"])
        package_dict = package.to_dict()

        assert package_dict["name"] == "user"
        assert package_dict["rules"] == ["name", "email"]
        assert package_dict["version"] == "1.0.0"

    def test_to_dict_full(self):
        """Test full dictionary conversion"""
        package = RulePackage(
            name="employee",
            description="Employee data",
            rules=["name", "department"],
            category="hr",
            version="2.0.0",
        )
        package_dict = package.to_dict()

        assert package_dict["name"] == "employee"
        assert package_dict["description"] == "Employee data"
        assert package_dict["rules"] == ["name", "department"]
        assert package_dict["category"] == "hr"
        assert package_dict["version"] == "2.0.0"

    def test_to_dict_with_rule_objects(self):
        """Test dictionary conversion with Rule objects"""
        rule = Rule(name="name")
        package = RulePackage(name="profile", rules=[rule, "email"])
        package_dict = package.to_dict()

        # Rule objects should be converted
        assert "name" in str(package_dict["rules"])
        assert "email" in str(package_dict["rules"])


class TestRulePackageMethods:
    """Test other RulePackage methods"""

    def test_get_rule_names(self):
        """Test getting rule names"""
        rule = Rule(name="first_name")
        combo = RuleCombination(name="contact", rules=["email", "phone"])

        package = RulePackage(name="profile", rules=[rule, combo, "age"])

        names = package.get_rule_names()
        assert "first_name" in names
        assert "contact" in names
        assert "age" in names

    def test_rule_count(self):
        """Test rule count"""
        package = RulePackage(name="user", rules=["name", "email", "age", "phone"])

        assert len(package.rules) == 4

    def test_has_rule(self):
        """Test checking if package contains rule"""
        rule = Rule(name="name")
        package = RulePackage(name="profile", rules=[rule, "email"])

        # Check if contains Rule object
        assert rule in package.rules
        # Check if contains string rule
        assert "email" in package.rules

    def test_get_rules_by_type(self):
        """Test getting rules by type"""
        rule = Rule(name="name")
        combo = RuleCombination(name="contact", rules=["email", "phone"])

        package = RulePackage(name="profile", rules=[rule, combo, "age", "location"])

        # Count different types of rules
        rule_objects = [r for r in package.rules if isinstance(r, Rule)]
        combo_objects = [r for r in package.rules if isinstance(r, RuleCombination)]
        string_rules = [r for r in package.rules if isinstance(r, str)]

        assert len(rule_objects) == 1
        assert len(combo_objects) == 1
        assert len(string_rules) == 2
