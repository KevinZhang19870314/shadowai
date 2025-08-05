"""
RuleCombination Class Unit Tests

Tests all functionality of the RuleCombination class, including creation, validation, methods, etc.
"""

import pytest
from mock_ai import Rule, RuleCombination
from pydantic import ValidationError


class TestRuleCombinationCreation:
    """Test RuleCombination creation functionality"""

    def test_create_combination_basic(self):
        """Test basic RuleCombination creation"""
        combo = RuleCombination(name="user_profile", rules=["name", "email"])

        assert combo.name == "user_profile"
        assert combo.description == "Combine name, email to create user profile"
        assert combo.rules == ["name", "email"]
        assert combo.combination_logic == "combine"

    def test_create_combination_with_rule_objects(self):
        """Test creating RuleCombination with Rule objects"""
        rule1 = Rule(name="name")
        rule2 = Rule(name="email")

        combo = RuleCombination(name="user_info", rules=[rule1, rule2])

        assert combo.name == "user_info"
        assert len(combo.rules) == 2
        assert combo.rules[0] == rule1
        assert combo.rules[1] == rule2

    def test_create_combination_mixed_rules(self):
        """Test creating with mixed strings and Rule objects"""
        rule1 = Rule(name="name")

        combo = RuleCombination(name="mixed_profile", rules=[rule1, "email", "age"])

        assert combo.name == "mixed_profile"
        assert len(combo.rules) == 3
        assert combo.rules[0] == rule1
        assert combo.rules[1] == "email"
        assert combo.rules[2] == "age"

    def test_create_combination_full_config(self):
        """Test creation with full configuration"""
        combo = RuleCombination(
            name="detailed_user",
            description="Detailed user profile information",
            rules=["name", "email", "phone"],
            combination_logic="join",
        )

        assert combo.name == "detailed_user"
        assert combo.description == "Detailed user profile information"
        assert combo.rules == ["name", "email", "phone"]
        assert combo.combination_logic == "join"


class TestRuleCombinationAutoDescription:
    """Test RuleCombination auto-description generation"""

    def test_auto_description_simple(self):
        """Test auto-description generation for simple rule lists"""
        combo = RuleCombination(name="contact_info", rules=["email", "phone"])

        assert combo.description == "Combine email, phone to create contact info"

    def test_auto_description_many_rules(self):
        """Test auto-description generation for multiple rules (only shows first 3)"""
        combo = RuleCombination(
            name="full_profile", rules=["name", "email", "phone", "address", "age"]
        )

        # Only shows first 3 rules
        assert "name, email, phone" in combo.description
        assert combo.description == "Combine name, email, phone to create full profile"

    def test_auto_description_with_rule_objects(self):
        """Test auto-description generation with Rule objects"""
        rule1 = Rule(name="first_name")
        rule2 = Rule(name="last_name")

        combo = RuleCombination(name="full_name", rules=[rule1, rule2])

        assert combo.description == "Combine first_name, last_name to create full name"

    def test_auto_description_empty_rules(self):
        """Test auto-description generation for empty rule list"""
        combo = RuleCombination(name="empty_combo", rules=[])

        assert combo.description == "Combination for empty combo"


class TestRuleCombinationValidation:
    """Test RuleCombination validation functionality"""

    def test_empty_name_raises_error(self):
        """Test empty name raises error"""
        with pytest.raises(ValidationError):
            RuleCombination(name="", rules=["name"])

    def test_none_name_raises_error(self):
        """Test None name raises error"""
        with pytest.raises((ValidationError, TypeError)):
            RuleCombination(name=None, rules=["name"])

    def test_invalid_rules_type_raises_error(self):
        """Test invalid rules type raises error"""
        with pytest.raises(ValidationError):
            RuleCombination(name="test", rules="invalid")  # should be a list


class TestRuleCombinationSimpleCreation:
    """Test RuleCombination.simple() method"""

    def test_simple_creation(self):
        """Test simple creation"""
        # Use quick method instead of simple method, as simple method is for string parsing
        combo = RuleCombination.quick("user_profile", "name", "email")

        assert combo.name == "user_profile"
        assert combo.rules == ["name", "email"]
        assert "name" in combo.description
        assert "email" in combo.description

    def test_simple_string_parsing(self):
        """Test string parsing creation"""
        combo = RuleCombination.simple("full_name = first_name + last_name")

        assert combo.name == "full_name"
        assert "first_name" in combo.rules
        assert "last_name" in combo.rules


class TestRuleCombinationChainMethods:
    """Test RuleCombination chain methods"""

    def test_with_logic_method(self):
        """Test with_logic method"""
        combo = RuleCombination(name="test", rules=["name", "email"]).with_logic("join")

        assert combo.combination_logic == "join"

    def test_add_rule_method(self):
        """Test add_rule method"""
        combo = (
            RuleCombination(name="test", rules=["name"])
            .add_rule("email")
            .add_rule("phone")
        )

        assert len(combo.rules) == 3
        assert "name" in combo.rules
        assert "email" in combo.rules
        assert "phone" in combo.rules


class TestRuleCombinationPromptGeneration:
    """Test RuleCombination prompt generation"""

    def test_to_prompt_basic(self):
        """Test basic prompt generation"""
        combo = RuleCombination(name="user_profile", rules=["name", "email"])
        prompt = combo.to_prompt()

        assert "user_profile" in prompt
        assert "name" in prompt
        assert "email" in prompt
        assert "combine" in prompt.lower()

    def test_to_prompt_with_custom_logic(self):
        """Test prompt generation with custom logic"""
        combo = RuleCombination(
            name="contact", rules=["email", "phone"], combination_logic="merge"
        )
        prompt = combo.to_prompt()

        assert "contact" in prompt
        assert "merge" in prompt

    def test_to_prompt_with_rule_objects(self):
        """Test prompt generation with Rule objects"""
        rule1 = Rule(name="name", description="Person's full name")
        combo = RuleCombination(name="identity", rules=[rule1, "email"])
        prompt = combo.to_prompt()

        assert "identity" in prompt
        assert "name" in prompt
        assert "email" in prompt


class TestRuleCombinationDictSerialization:
    """Test RuleCombination dictionary serialization"""

    def test_to_dict_basic(self):
        """Test basic dictionary conversion"""
        combo = RuleCombination(name="user_profile", rules=["name", "email"])
        combo_dict = combo.to_dict()

        assert combo_dict["name"] == "user_profile"
        assert combo_dict["rules"] == ["name", "email"]
        assert combo_dict["combination_logic"] == "combine"

    def test_to_dict_with_rule_objects(self):
        """Test dictionary conversion with Rule objects"""
        rule1 = Rule(name="name")
        combo = RuleCombination(name="profile", rules=[rule1, "email"])
        combo_dict = combo.to_dict()

        # Rule objects should be converted to string names or dictionaries
        assert "name" in str(combo_dict["rules"])
        assert "email" in str(combo_dict["rules"])


class TestRuleCombinationMethods:
    """Test other RuleCombination methods"""

    def test_get_rule_names(self):
        """Test getting rule names"""
        rule1 = Rule(name="first_name")
        combo = RuleCombination(name="full_name", rules=[rule1, "last_name"])

        names = combo.get_rule_names()
        assert "first_name" in names
        assert "last_name" in names

    def test_rule_count(self):
        """Test rule count"""
        combo = RuleCombination(name="profile", rules=["name", "email", "phone"])

        assert len(combo.rules) == 3
