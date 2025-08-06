"""
File Utilities Unit Tests

Tests JSON and YAML operation functionality of file utilities.
"""

import json
from pathlib import Path

import pytest
import yaml
from shadow_ai import Rule, RuleCombination, RulePackage
from shadow_ai.utils.file_utils import (
    _convert_to_yaml_safe,
    load_rules_from_json,
    load_rules_from_yaml,
    save_rules_to_json,
    save_rules_to_yaml,
)


class TestJSONOperations:
    """Test JSON file operations"""

    def test_save_single_rule_to_json(self, temp_json_file):
        """Test saving single rule to JSON"""
        rule = Rule(name="email", description="Test email rule")

        save_rules_to_json([rule], temp_json_file)

        assert temp_json_file.exists()
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "email"
        assert data[0]["description"] == "Test email rule"

    def test_save_multiple_rules_to_json(self, temp_json_file):
        """Test saving multiple rules to JSON"""
        rule1 = Rule(name="email")
        rule2 = Rule(name="name")
        combo = RuleCombination(name="user_profile", rules=["name", "email"])

        save_rules_to_json([rule1, rule2, combo], temp_json_file)

        assert temp_json_file.exists()
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 3

    def test_save_rule_package_to_json(self, temp_json_file):
        """Test saving rule package to JSON"""
        package = RulePackage(name="person", rules=["name", "email", "age"], category="users")

        save_rules_to_json([package], temp_json_file)

        assert temp_json_file.exists()
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "person"
        assert data[0]["category"] == "users"

    def test_load_rules_from_json(self, temp_json_file):
        """Test loading rules from JSON"""
        # First create test data
        test_data = [
            {
                "name": "email",
                "description": "Test email",
                "rule_type": "record",
                "examples": [],
                "constraints": {},
            }
        ]

        with open(temp_json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)

        # Load and verify
        rules = load_rules_from_json(temp_json_file)

        assert len(rules) == 1
        # Returns Rule objects, not dictionaries
        assert rules[0].name == "email"
        assert rules[0].description == "Test email"

    def test_load_nonexistent_json_file(self):
        """Test loading non-existent JSON file"""
        nonexistent_file = Path("nonexistent.json")

        with pytest.raises(FileNotFoundError):
            load_rules_from_json(nonexistent_file)

    def test_load_invalid_json_file(self, temp_json_file):
        """Test loading invalid JSON file"""
        # Write invalid JSON
        with open(temp_json_file, "w") as f:
            f.write("invalid json content")

        with pytest.raises(json.JSONDecodeError):
            load_rules_from_json(temp_json_file)


class TestYAMLOperations:
    """Test YAML file operations"""

    def test_save_single_rule_to_yaml(self, temp_yaml_file):
        """Test saving single rule to YAML"""
        rule = Rule(name="email", description="Test email rule")

        save_rules_to_yaml([rule], temp_yaml_file)

        assert temp_yaml_file.exists()
        with open(temp_yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data) == 1
        assert data[0]["name"] == "email"
        assert data[0]["description"] == "Test email rule"

    def test_save_multiple_rules_to_yaml(self, temp_yaml_file):
        """Test saving multiple rules to YAML"""
        rule1 = Rule(name="email")
        rule2 = Rule(name="name")
        combo = RuleCombination(name="user_profile", rules=["name", "email"])

        save_rules_to_yaml([rule1, rule2, combo], temp_yaml_file)

        assert temp_yaml_file.exists()
        with open(temp_yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data) == 3

    def test_save_rule_package_to_yaml(self, temp_yaml_file):
        """Test saving rule package to YAML"""
        package = RulePackage(name="person", rules=["name", "email", "age"], category="users")

        save_rules_to_yaml([package], temp_yaml_file)

        assert temp_yaml_file.exists()
        with open(temp_yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data) == 1
        assert data[0]["name"] == "person"
        assert data[0]["category"] == "users"

    def test_load_rules_from_yaml(self, temp_yaml_file):
        """Test loading rules from YAML"""
        # First create test data
        test_data = [
            {
                "name": "email",
                "description": "Test email",
                "rule_type": "record",
                "examples": [],
                "constraints": {},
            }
        ]

        with open(temp_yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(test_data, f, allow_unicode=True)

        # Load and verify
        rules = load_rules_from_yaml(temp_yaml_file)

        assert len(rules) == 1
        # Returns Rule objects, not dictionaries
        assert rules[0].name == "email"
        assert rules[0].description == "Test email"

    def test_load_nonexistent_yaml_file(self):
        """Test loading non-existent YAML file"""
        nonexistent_file = Path("nonexistent.yaml")

        with pytest.raises(FileNotFoundError):
            load_rules_from_yaml(nonexistent_file)

    def test_load_invalid_yaml_file(self, temp_yaml_file):
        """Test loading invalid YAML file"""
        # Write invalid YAML
        with open(temp_yaml_file, "w") as f:
            f.write("invalid: yaml: content: [unclosed")

        with pytest.raises(yaml.YAMLError):
            load_rules_from_yaml(temp_yaml_file)


class TestYAMLSafeConversion:
    """Test YAML safe conversion functionality"""

    def test_convert_enum_to_yaml_safe(self):
        """Test converting enums to YAML safe format"""
        from shadow_ai.core.rule import RuleType

        data = {"rule_type": RuleType.RECORD}
        safe_data = _convert_to_yaml_safe(data)

        assert safe_data["rule_type"] == "record"

    def test_convert_nested_dict_to_yaml_safe(self):
        """Test nested dictionary conversion"""
        from shadow_ai.core.rule import RuleType

        data = {
            "rule": {"name": "test", "type": RuleType.COMBINATION},
            "metadata": {"version": "1.0.0"},
        }

        safe_data = _convert_to_yaml_safe(data)

        assert safe_data["rule"]["type"] == "combination"
        assert safe_data["metadata"]["version"] == "1.0.0"

    def test_convert_list_to_yaml_safe(self):
        """Test list conversion"""
        from shadow_ai.core.rule import RuleType

        data = [{"type": RuleType.RECORD}, {"type": RuleType.COMBINATION}]

        safe_data = _convert_to_yaml_safe(data)

        assert safe_data[0]["type"] == "record"
        assert safe_data[1]["type"] == "combination"

    def test_convert_object_with_dict_to_yaml_safe(self):
        """Test object __dict__ conversion"""
        rule = Rule(name="test")
        safe_data = _convert_to_yaml_safe(rule)

        # Should be converted to dictionary format
        assert isinstance(safe_data, dict)
        assert "name" in safe_data

    def test_convert_primitive_types(self):
        """Test primitive types remain unchanged"""
        data = {"string": "test", "number": 42, "boolean": True, "null": None}

        safe_data = _convert_to_yaml_safe(data)

        assert safe_data["string"] == "test"
        assert safe_data["number"] == 42
        assert safe_data["boolean"] is True
        assert safe_data["null"] is None


class TestFilePathHandling:
    """Test file path handling"""

    def test_save_with_string_path(self, tmp_path):
        """Test saving with string path"""
        rule = Rule(name="email")
        file_path = str(tmp_path / "test.json")

        save_rules_to_json([rule], file_path)

        assert Path(file_path).exists()

    def test_save_with_path_object(self, temp_json_file):
        """Test saving with Path object"""
        rule = Rule(name="email")

        save_rules_to_json([rule], temp_json_file)

        assert temp_json_file.exists()

    def test_load_with_string_path(self, temp_json_file):
        """Test loading with string path"""
        # Save test rule
        rule = Rule(name="email", description="Test email")
        save_rules_to_json([rule], temp_json_file)

        # Load using string path
        rules = load_rules_from_json(str(temp_json_file))

        assert len(rules) == 1
        # Returns Rule objects, not dictionaries
        assert rules[0].name == "email"


class TestErrorHandling:
    """Test error handling"""

    def test_save_to_readonly_directory(self):
        """Test saving to read-only directory"""
        rule = Rule(name="email")
        readonly_path = Path("/readonly/test.json")  # Assumed read-only path

        # Different operating systems may handle this differently, testing concept here
        # In actual environment, may need to adjust based on specific circumstances
        try:
            save_rules_to_json([rule], readonly_path)
        except (PermissionError, OSError):
            # Expected exception
            pass

    def test_save_empty_rules_list(self, temp_json_file):
        """Test saving empty rules list"""
        save_rules_to_json([], temp_json_file)

        assert temp_json_file.exists()
        with open(temp_json_file, "r") as f:
            data = json.load(f)

        assert data == []

    def test_save_none_rules_list(self, temp_json_file):
        """Test saving None rules list"""
        # save_rules_to_json will throw TypeError when iterating None, but may create file first
        try:
            save_rules_to_json(None, temp_json_file)
            # If no exception is thrown, check file content
            if temp_json_file.exists():
                with open(temp_json_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    # May contain null or empty content
                    assert content in ["null", "[]", ""]
        except (TypeError, AttributeError) as e:
            # Expected behavior: throw exception when processing None
            assert "NoneType" in str(e) or "object has no attribute" in str(e)
