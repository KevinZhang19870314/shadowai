"""
Rule Class Unit Tests

Tests all functionality of the Rule class, including creation, validation, methods, etc.
"""

import pytest
from mock_ai import Rule
from mock_ai.core.rule import RuleType
from pydantic import ValidationError


class TestRuleCreation:
    """Test Rule creation functionality"""

    def test_create_rule_with_name_only(self):
        """Test creating Rule with name only"""
        rule = Rule(name="email")

        assert rule.name == "email"
        assert rule.description == "Generate a email"  # auto-generated description
        assert rule.rule_type == RuleType.RECORD
        assert rule.examples is None
        assert rule.constraints is None

    def test_create_rule_with_full_config(self):
        """Test creation with full configuration"""
        rule = Rule(
            name="email",
            description="Generate an email address",
            examples=["test@example.com", "user@domain.com"],
            constraints={"format": "email", "domain": "example.com"},
            rule_type=RuleType.COMBINATION,
        )

        assert rule.name == "email"
        assert rule.description == "Generate an email address"
        assert rule.rule_type == RuleType.COMBINATION
        assert rule.examples == ["test@example.com", "user@domain.com"]
        assert rule.constraints == {"format": "email", "domain": "example.com"}

    def test_create_rule_with_underscore_name(self):
        """Test auto-description generation for names with underscores"""
        rule = Rule(name="user_name")
        assert rule.description == "Generate a user name"

    def test_create_rule_with_complex_name(self):
        """Test description generation for complex names"""
        rule = Rule(name="company_address_line_1")
        assert rule.description == "Generate a company address line 1"


class TestRuleValidation:
    """Test Rule validation functionality"""

    def test_empty_name_raises_error(self):
        """Test empty name raises error"""
        with pytest.raises(ValidationError):
            Rule(name="")

    def test_none_name_raises_error(self):
        """Test None name raises error"""
        with pytest.raises((ValidationError, TypeError)):
            Rule(name=None)

    def test_invalid_rule_type_raises_error(self):
        """Test invalid rule_type raises error"""
        with pytest.raises(ValidationError):
            Rule(name="test", rule_type="invalid_type")


class TestRuleSimpleCreation:
    """Test Rule.simple() method"""

    def test_simple_field_name(self):
        """Test simple field name"""
        rule = Rule.simple("email")

        assert rule.name == "email"
        assert "email" in rule.description.lower()

    def test_simple_with_description(self):
        """Test simple creation with description"""
        rule = Rule.simple("email: user email address")

        assert rule.name == "email"
        assert rule.description == "user email address"

    def test_simple_with_examples(self):
        """Test simple creation with examples"""
        rule = Rule.simple("color|red,blue,green")

        assert rule.name == "color"
        assert rule.examples == ["red", "blue", "green"]
        assert "color" in rule.description.lower()


class TestRuleChainMethods:
    """Test Rule chain methods"""

    def test_with_examples_method(self):
        """Test with_examples method"""
        rule = Rule(name="color").with_examples("red", "blue", "green")

        assert rule.name == "color"
        assert rule.examples == ["red", "blue", "green"]

    def test_with_constraints_method(self):
        """Test with_constraints method"""
        rule = Rule(name="age").with_constraints(min=18, max=65, type="integer")

        assert rule.name == "age"
        assert rule.constraints == {"min": 18, "max": 65, "type": "integer"}

    def test_chain_multiple_methods(self):
        """Test chaining multiple methods"""
        rule = (
            Rule(name="score")
            .with_examples("A", "B", "C")
            .with_constraints(type="string", options=["A", "B", "C", "D", "F"])
        )

        assert rule.name == "score"
        assert rule.examples == ["A", "B", "C"]
        assert rule.constraints == {
            "type": "string",
            "options": ["A", "B", "C", "D", "F"],
        }


class TestRulePromptGeneration:
    """Test Rule prompt generation"""

    def test_to_prompt_basic(self):
        """Test basic prompt generation"""
        rule = Rule(name="email")
        prompt = rule.to_prompt()

        assert "email" in prompt
        assert "Generate a email" in prompt

    def test_to_prompt_with_examples(self):
        """Test prompt generation with examples"""
        rule = Rule(name="color", examples=["red", "blue", "green"])
        prompt = rule.to_prompt()

        assert "color" in prompt
        assert "red" in prompt
        assert "blue" in prompt
        assert "green" in prompt

    def test_to_prompt_with_constraints(self):
        """Test prompt generation with constraints"""
        rule = Rule(name="age", constraints={"min": 18, "max": 65})
        prompt = rule.to_prompt()

        assert "age" in prompt
        assert "18" in prompt
        assert "65" in prompt


class TestRuleDictSerialization:
    """Test Rule dictionary serialization"""

    def test_to_dict_basic(self):
        """Test basic dictionary conversion"""
        rule = Rule(name="email")
        rule_dict = rule.to_dict()

        assert rule_dict["name"] == "email"
        assert rule_dict["description"] == "Generate a email"
        assert rule_dict["rule_type"] == "record"

    def test_to_dict_full(self):
        """Test full dictionary conversion"""
        rule = Rule(
            name="email",
            description="Test email",
            examples=["test@example.com"],
            constraints={"format": "email"},
        )
        rule_dict = rule.to_dict()

        assert rule_dict["name"] == "email"
        assert rule_dict["description"] == "Test email"
        assert rule_dict["examples"] == ["test@example.com"]
        assert rule_dict["constraints"] == {"format": "email"}

    def test_from_dict_simple(self):
        """Test creating Rule from dictionary"""
        rule_dict = {"name": "test_field", "description": "Test description"}
        rule = Rule.from_dict_simple(rule_dict)

        assert rule.name == "test_field"
        assert rule.description == "Test description"


class TestRuleComparison:
    """Test Rule comparison functionality"""

    def test_rule_equality(self):
        """Test Rule equality"""
        rule1 = Rule(name="email", description="Test email")
        rule2 = Rule(name="email", description="Test email")

        assert rule1.name == rule2.name
        assert rule1.description == rule2.description

    def test_rule_inequality(self):
        """Test Rule inequality"""
        rule1 = Rule(name="email")
        rule2 = Rule(name="phone")

        assert rule1.name != rule2.name
