"""
ShadowAI Main Class Unit Tests

Tests all functionality of the ShadowAI class, including data generation, string inputs, formatted output, etc.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from shadow_ai import Rule, RuleCombination, RulePackage, ShadowAI
from shadow_ai.core.shadow_ai import MockDataResponse


class TestShadowAIInitialization:
    """Test ShadowAI initialization"""

    def test_default_initialization(self, mock_api_key):
        """Test default initialization"""
        shadow_ai = ShadowAI()
        assert shadow_ai is not None
        assert shadow_ai.model_id == "gpt-4o-mini"

    def test_custom_model_initialization(self, mock_api_key):
        """Test initialization with custom model"""
        shadow_ai = ShadowAI(model_id="gpt-4")
        assert shadow_ai.model_id == "gpt-4"


class TestShadowAIStringInputs:
    """Test ShadowAI string input functionality"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_string_input_basic(self, mock_agent_class, mock_api_key):
        """Test basic string input"""
        # Mock agent behavior
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"name": "John Doe"}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.generate("name")

        assert isinstance(result, dict)
        assert "name" in result

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_string_input_multiple_count(self, mock_agent_class, mock_api_key):
        """Test string input with multiple count"""
        # Mock agent behavior for array response
        mock_agent = Mock()
        mock_agent.run.return_value.content = '[{"name": "John"}, {"name": "Jane"}]'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.generate("name", count=2)

        assert isinstance(result, list)
        assert len(result) == 2


class TestShadowAIRuleInputs:
    """Test ShadowAI Rule object input functionality"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_rule_input_basic(self, mock_agent_class, mock_api_key):
        """Test basic Rule input"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"email": "test@example.com"}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        rule = Rule(name="email", description="Email address")
        result = shadow_ai.generate(rule)

        assert isinstance(result, dict)
        assert "email" in result

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_rule_combination_input(self, mock_agent_class, mock_api_key):
        """Test RuleCombination input"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"full_name": "John Doe"}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        rule_combo = RuleCombination(
            name="full_name",
            description="Full name combination",
            rules=["first_name", "last_name"],
        )
        result = shadow_ai.generate(rule_combo)

        assert isinstance(result, dict)

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_rule_package_input(self, mock_agent_class, mock_api_key):
        """Test RulePackage input"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"name": "John", "age": 30}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        rule_package = RulePackage(
            name="user", description="User profile", rules=["name", "age"]
        )
        result = shadow_ai.generate(rule_package)

        assert isinstance(result, dict)


class TestShadowAIFormattedOutput:
    """Test ShadowAI formatted output functionality"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_formatted_output_success(self, mock_agent_class, mock_api_key):
        """Test formatted output success response"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"name": "John"}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.generate("name", format_output=True)

        assert isinstance(result, MockDataResponse)
        assert result.success is True
        assert result.error is None
        assert "name" in result.data

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_formatted_output_error(self, mock_agent_class, mock_api_key):
        """Test formatted output error response"""
        mock_agent = Mock()
        mock_agent.run.side_effect = Exception("Test error")
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.generate("name", format_output=True)

        assert isinstance(result, MockDataResponse)
        assert result.success is False
        assert result.error == "Test error"


class TestShadowAIBatchGeneration:
    """Test ShadowAI batch generation functionality"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_batch_generation_list_rules(self, mock_agent_class, mock_api_key):
        """Test batch generation with list of rules"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = (
            '{"name": "John", "email": "john@example.com"}'
        )
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        rules = [
            Rule(name="name", description="Person name"),
            Rule(name="email", description="Email address"),
        ]
        result = shadow_ai.generate(rules)

        assert isinstance(result, dict)
        mock_agent.run.assert_called_once()

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_batch_generation_mixed_rules(self, mock_agent_class, mock_api_key):
        """Test batch generation with mixed rule types"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = (
            '{"name": "John", "email": "john@example.com"}'
        )
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        rules = ["name", Rule(name="email", description="Email address")]
        result = shadow_ai.generate(rules)

        assert isinstance(result, dict)


class TestShadowAIQuickMethod:
    """Test ShadowAI quick generation method"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_quick_method_single_field(self, mock_agent_class, mock_api_key):
        """Test quick method with single field"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"name": "John"}'
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.quick("name")

        assert isinstance(result, dict)

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_quick_method_multiple_fields(self, mock_agent_class, mock_api_key):
        """Test quick method with multiple fields"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = (
            '{"name": "John", "age": 30, "email": "john@example.com"}'
        )
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()
        result = shadow_ai.quick("name", "age", "email")

        assert isinstance(result, dict)


class TestShadowAIErrorHandling:
    """Test ShadowAI error handling"""

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_invalid_json_response(self, mock_agent_class, mock_api_key):
        """Test handling of invalid JSON response"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = "invalid json"
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()

        with pytest.raises(ValueError, match="No valid JSON found in response"):
            shadow_ai.generate("name")

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_malformed_json_response(self, mock_agent_class, mock_api_key):
        """Test handling of malformed JSON response"""
        mock_agent = Mock()
        mock_agent.run.return_value.content = '{"name": "John"'  # Missing closing brace
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()

        with pytest.raises(ValueError, match="No valid JSON found in response"):
            shadow_ai.generate("name")

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_agent_exception_no_format(self, mock_agent_class, mock_api_key):
        """Test agent exception without format_output"""
        mock_agent = Mock()
        mock_agent.run.side_effect = Exception("API Error")
        mock_agent_class.return_value = mock_agent

        shadow_ai = ShadowAI()

        with pytest.raises(Exception, match="API Error"):
            shadow_ai.generate("name")

    @patch("shadow_ai.core.shadow_ai.Agent")
    def test_unsupported_rule_type(self, mock_agent_class, mock_api_key):
        """Test unsupported rule type error"""
        shadow_ai = ShadowAI()

        with pytest.raises(ValueError, match="Unsupported rules type"):
            shadow_ai.generate(123)  # Invalid type


class TestShadowAIInputProcessing:
    """Test ShadowAI input processing functionality"""

    def test_process_string_input(self, shadow_ai_instance):
        """Test processing string input"""
        processed = shadow_ai_instance._process_rules("name")
        assert len(processed) == 1
        assert isinstance(processed[0], Rule)
        assert processed[0].name == "name"

    def test_process_rule_input(self, shadow_ai_instance):
        """Test processing Rule input"""
        rule = Rule(name="email", description="Email address")
        processed = shadow_ai_instance._process_rules(rule)
        assert len(processed) == 1
        assert processed[0] == rule

    def test_process_list_input(self, shadow_ai_instance):
        """Test processing list input"""
        rules = ["name", Rule(name="email")]
        processed = shadow_ai_instance._process_rules(rules)
        assert len(processed) == 2
        assert all(isinstance(r, Rule) for r in processed)

    def test_process_dict_input(self, shadow_ai_instance):
        """Test processing dictionary input"""
        rule_dict = {"name": "test", "description": "Test rule", "rule_type": "record"}
        processed = shadow_ai_instance._process_rules(rule_dict)
        assert len(processed) == 1
        assert isinstance(processed[0], Rule)


class TestShadowAIPromptBuilding:
    """Test ShadowAI prompt building functionality"""

    def test_build_prompt_single_rule(self, shadow_ai_instance):
        """Test building prompt with single rule"""
        rule = Rule(name="name", description="Person name")
        prompt = shadow_ai_instance._build_prompt([rule], 1)

        assert "1 record(s) of mock data with the following fields:" in prompt
        assert "name: Person name" in prompt
        assert "FLAT JSON format" in prompt

    def test_build_prompt_multiple_rules(self, shadow_ai_instance):
        """Test building prompt with multiple rules"""
        rules = [
            Rule(name="name", description="Person name"),
            Rule(name="email", description="Email address"),
        ]
        prompt = shadow_ai_instance._build_prompt(rules, 2)

        assert "2 record(s) of mock data with the following fields:" in prompt
        assert "name: Person name" in prompt
        assert "email: Email address" in prompt

    def test_build_prompt_rule_combination(self, shadow_ai_instance):
        """Test building prompt with RuleCombination"""
        rule_combo = RuleCombination(
            name="full_name",
            description="Full name combination",
            rules=["first_name", "last_name"],
        )
        prompt = shadow_ai_instance._build_prompt([rule_combo], 1)

        assert "Rule Name: full_name" in prompt
        assert "Description: Full name combination" in prompt
        assert "Type: combination" in prompt
