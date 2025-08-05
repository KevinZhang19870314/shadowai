"""
MockAI Main Class Unit Tests

Tests all functionality of the MockAI class, including data generation, string inputs, formatted output, etc.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from mock_ai import MockAI, Rule, RuleCombination, RulePackage
from mock_ai.core.mock_ai import MockDataResponse


class TestMockAIInitialization:
    """Test MockAI initialization"""

    def test_default_initialization(self, mock_api_key):
        """Test default initialization"""
        mock_ai = MockAI()
        assert mock_ai is not None

    def test_initialization_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict("os.environ", {}, clear=True):
            mock_ai = MockAI()
            assert mock_ai is not None


class TestMockAIStringInputs:
    """Test MockAI string input functionality"""

    def test_generate_single_string(self, mock_agno_agent, mock_api_key):
        """Test single string input"""
        mock_ai = MockAI()

        result = mock_ai.generate("email", format_output=False)

        assert isinstance(result, dict)
        assert "email" in result

    def test_generate_string_list(self, mock_agno_agent, mock_api_key):
        """Test string list input"""
        mock_ai = MockAI()

        result = mock_ai.generate(["email", "name", "age"], format_output=False)

        assert isinstance(result, dict)
        # Should contain all requested fields (based on mock return)
        assert len(result) >= 1

    def test_generate_empty_string_list(self, mock_agno_agent, mock_api_key):
        """Test empty string list"""
        mock_ai = MockAI()

        result = mock_ai.generate([], format_output=False)

        # Should handle empty list gracefully
        assert isinstance(result, dict)


class TestMockAIRuleInputs:
    """Test MockAI Rule object input functionality"""

    def test_generate_single_rule(self, mock_agno_agent, mock_api_key):
        """Test single Rule object input"""
        mock_ai = MockAI()

        rule = Rule(name="email", description="Generate an email address")
        result = mock_ai.generate(rule, format_output=False)

        assert isinstance(result, dict)
        assert "email" in result

    def test_generate_rule_list(self, mock_agno_agent, mock_api_key):
        """Test Rule object list input"""
        mock_ai = MockAI()

        rules = [Rule(name="email"), Rule(name="name"), Rule(name="age")]
        result = mock_ai.generate(rules, format_output=False)

        assert isinstance(result, dict)
        assert len(result) >= 1

    def test_generate_rule_combination(self, mock_agno_agent, mock_api_key):
        """Test RuleCombination input"""
        mock_ai = MockAI()

        combo = RuleCombination(name="full_name", rules=["first_name", "last_name"])
        result = mock_ai.generate(combo, format_output=False)

        assert isinstance(result, dict)

    def test_generate_rule_package(self, mock_agno_agent, mock_api_key):
        """Test RulePackage input"""
        mock_ai = MockAI()

        package = RulePackage(name="user", rules=["name", "email", "age"])
        result = mock_ai.generate(package, format_output=False)

        assert isinstance(result, dict)


class TestMockAIFormattedOutput:
    """Test MockAI formatted output functionality"""

    def test_formatted_output_success(self, mock_agno_agent, mock_api_key):
        """Test formatted output success case"""
        mock_ai = MockAI()

        result = mock_ai.generate("email", format_output=True)

        assert isinstance(result, MockDataResponse)
        assert result.success is True
        assert result.data is not None
        assert result.error is None
        assert result.metadata is not None

    def test_formatted_output_metadata(self, mock_agno_agent, mock_api_key):
        """Test formatted output metadata"""
        mock_ai = MockAI()

        result = mock_ai.generate("email", format_output=True)

        assert "model_id" in result.metadata
        assert "rules_count" in result.metadata
        assert "generated_count" in result.metadata


class TestMockAIBatchGeneration:
    """Test MockAI batch generation functionality"""

    def test_generate_multiple_count(self, mock_agno_agent, mock_api_key):
        """Test generating multiple records"""
        mock_ai = MockAI()

        # Mock agent to return array for count > 1
        mock_ai.agent.run.return_value = (
            '[{"email": "test1@example.com"}, {"email": "test2@example.com"}]'
        )

        result = mock_ai.generate("email", count=2, format_output=False)

        assert isinstance(result, list)
        assert len(result) == 2

    def test_generate_single_count(self, mock_agno_agent, mock_api_key):
        """Test generating single record explicitly"""
        mock_ai = MockAI()

        result = mock_ai.generate("email", count=1, format_output=False)

        assert isinstance(result, dict)


class TestMockAIQuickMethod:
    """Test MockAI quick generation method"""

    def test_quick_single_field(self, mock_agno_agent, mock_api_key):
        """Test quick method with single field"""
        mock_ai = MockAI()

        result = mock_ai.quick("email")

        assert isinstance(result, dict)
        assert "email" in result

    def test_quick_multiple_fields(self, mock_agno_agent, mock_api_key):
        """Test quick method with multiple fields"""
        mock_ai = MockAI()

        result = mock_ai.quick("email", "name", "age")

        assert isinstance(result, dict)
        # Should contain all requested fields
        assert len(result) >= 1


class TestMockAIErrorHandling:
    """Test MockAI error handling"""

    def test_json_parse_error_unformatted(self, mock_api_key):
        """Test JSON parse error with unformatted output"""
        mock_ai = MockAI()

        # Mock agent to return invalid JSON
        with patch.object(mock_ai.agent, "run", return_value="invalid json"):
            with pytest.raises(ValueError):
                mock_ai.generate("email", format_output=False)

    def test_json_parse_error_formatted(self, mock_api_key):
        """Test JSON parse error with formatted output"""
        mock_ai = MockAI()

        # Mock agent to return invalid JSON
        with patch.object(mock_ai.agent, "run", return_value="invalid json"):
            result = mock_ai.generate("email", format_output=True)

            assert isinstance(result, MockDataResponse)
            assert result.success is False
            assert result.error is not None

    def test_agent_exception_unformatted(self, mock_api_key):
        """Test agent exception with unformatted output"""
        mock_ai = MockAI()

        # Mock agent to raise exception
        with patch.object(mock_ai.agent, "run", side_effect=Exception("Test error")):
            with pytest.raises(Exception):
                mock_ai.generate("email", format_output=False)

    def test_agent_exception_formatted(self, mock_api_key):
        """Test agent exception with formatted output"""
        mock_ai = MockAI()

        # Mock agent to raise exception
        with patch.object(mock_ai.agent, "run", side_effect=Exception("Test error")):
            result = mock_ai.generate("email", format_output=True)

            assert isinstance(result, MockDataResponse)
            assert result.success is False
            assert "Test error" in result.error


class TestMockAIInputProcessing:
    """Test MockAI input processing functionality"""

    def test_mixed_input_types(self, mock_agno_agent, mock_api_key):
        """Test mixed input types (strings and Rules)"""
        mock_ai = MockAI()

        rules = ["email", Rule(name="name"), "age"]
        result = mock_ai.generate(rules, format_output=False)

        assert isinstance(result, dict)

    def test_dict_input(self, mock_agno_agent, mock_api_key):
        """Test dictionary input (loaded from file)"""
        mock_ai = MockAI()

        rule_dict = {
            "name": "email",
            "description": "Generate an email address",
            "rule_type": "record",
        }
        result = mock_ai.generate(rule_dict, format_output=False)

        assert isinstance(result, dict)

    def test_unsupported_input_type(self, mock_api_key):
        """Test unsupported input type"""
        mock_ai = MockAI()

        with pytest.raises(ValueError):
            mock_ai.generate(123, format_output=False)  # Number is not supported


class TestMockAIPromptBuilding:
    """Test MockAI prompt building functionality"""

    def test_prompt_building_single_rule(self, mock_api_key):
        """Test prompt building for single rule"""
        mock_ai = MockAI()

        rule = Rule(
            name="email",
            description="Generate an email address",
            examples=["test@example.com"],
            constraints={"format": "valid"},
        )

        prompt = mock_ai._build_prompt([rule], count=1)

        assert "email" in prompt
        assert "Generate an email address" in prompt
        assert "test@example.com" in prompt
        assert "valid" in prompt

    def test_prompt_building_multiple_rules(self, mock_api_key):
        """Test prompt building for multiple rules"""
        mock_ai = MockAI()

        rules = [Rule(name="email"), Rule(name="name")]

        prompt = mock_ai._build_prompt(rules, count=1)

        assert "email" in prompt
        assert "name" in prompt
        assert "JSON format" in prompt

    def test_prompt_building_rule_package(self, mock_api_key):
        """Test prompt building for rule package"""
        mock_ai = MockAI()

        package = RulePackage(
            name="user", description="User information", rules=["name", "email"]
        )

        prompt = mock_ai._build_prompt([package], count=1)

        assert "user" in prompt
        assert "User information" in prompt


# Fixtures
@pytest.fixture
def mock_api_key():
    """Mock API key fixture"""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def mock_agno_agent():
    """Mock Agno Agent fixture"""
    with patch("mock_ai.core.mock_ai.Agent") as mock_agent_class:
        mock_agent = Mock()
        mock_agent.run.return_value = '{"email": "test@example.com"}'
        mock_agent_class.return_value = mock_agent
        yield mock_agent
