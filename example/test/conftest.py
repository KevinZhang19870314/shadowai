"""
pytest Configuration File

Defines test fixtures and global configuration.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add lib directory to Python path for importing mock_ai
project_root = Path(__file__).parent.parent.parent
lib_path = project_root / "lib"
sys.path.insert(0, str(lib_path))

# Import MockAI components
from mock_ai import MockAI, Rule, RuleCombination, RulePackage
from mock_ai.utils.file_utils import load_rules_from_json, save_rules_to_json

# Also need to import agno components for mocking
try:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
except ImportError:
    # If agno is not installed, create dummy classes
    Agent = None
    OpenAIChat = None


@pytest.fixture
def mock_ai_instance():
    """Fixture for creating MockAI instance"""
    return MockAI()


@pytest.fixture
def sample_rule():
    """Fixture for creating sample Rule"""
    return Rule(
        name="test_email",
        description="Generate a test email address",
        examples=["test@example.com", "user@domain.com"],
    )


@pytest.fixture
def sample_combination():
    """Fixture for creating sample RuleCombination"""
    return RuleCombination(
        name="test_user",
        description="Test user profile combination",
        rules=["name", "email", "age"],
    )


@pytest.fixture
def sample_package():
    """Fixture for creating sample RulePackage"""
    return RulePackage(
        name="test_person",
        description="Test person information package",
        rules=["name", "email", "age", "phone"],
        category="test",
        version="1.0.0",
    )


@pytest.fixture
def temp_json_file(tmp_path):
    """Fixture for creating temporary JSON file"""
    return tmp_path / "test_rules.json"


@pytest.fixture
def temp_yaml_file(tmp_path):
    """Fixture for creating temporary YAML file"""
    return tmp_path / "test_rules.yaml"


@pytest.fixture
def mock_agno_agent():
    """Mock Agno agent fixture to avoid real API calls"""
    # Mock both OpenAIChat and Agent to completely bypass actual agno calls
    with patch("mock_ai.core.mock_ai.OpenAIChat") as mock_openai, patch(
        "mock_ai.core.mock_ai.Agent"
    ) as mock_agent:

        # Create mock OpenAIChat instance
        mock_openai_instance = Mock()
        mock_openai.return_value = mock_openai_instance

        # Create mock Agent instance
        mock_agent_instance = Mock()

        def mock_run(prompt, stream=False):
            """Mock run method that returns JSON format content"""
            # Check if prompt contains count information
            import re

            # Match "Generate an array of {count} JSON objects" format
            count_match = re.search(r"Generate an array of (\d+) JSON objects", prompt)

            if count_match:
                count = int(count_match.group(1))
                # Return array format
                data = []
                for i in range(count):
                    data.append(
                        {
                            "email": f"test{i+1}@example.com",
                            "name": f"John Doe {i+1}",
                            "age": 30 + i,
                        }
                    )
            else:
                # Return single object
                data = {"email": "test@example.com", "name": "John Doe", "age": 30}

            # Create mock response object
            mock_response = Mock()
            mock_response.content = json.dumps(data)
            return mock_response

        # Set Agent.run method to use our mock function
        mock_agent_instance.run.side_effect = mock_run

        # Set Agent constructor to return our mock instance
        mock_agent.return_value = mock_agent_instance

        yield mock_agent_instance


@pytest.fixture
def mock_api_key():
    """Mock API key fixture"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield "test-key"


# pytest configuration
def pytest_configure(config):
    """pytest configuration"""
    # Add custom markers
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "slow: slow tests")


def pytest_collection_modifyitems(config, items):
    """Modify collected test items"""
    # Add unit marker to tests without markers
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)
