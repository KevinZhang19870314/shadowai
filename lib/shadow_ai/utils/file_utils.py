"""
File Processing Utilities Module

Provides read and write functionality for JSON and YAML files.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

from ..core.rule import Rule
from ..core.rule_combination import RuleCombination
from ..core.rule_package import RulePackage


def _convert_to_yaml_safe(data: Any) -> Any:
    """
    Convert data to YAML-safe format, handling enums and other Python-specific objects

    Args:
        data: Data to convert

    Returns:
        YAML-safe data
    """
    if isinstance(data, dict):
        return {key: _convert_to_yaml_safe(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_convert_to_yaml_safe(item) for item in data]
    elif isinstance(data, Enum):
        return data.value
    elif hasattr(data, "__dict__"):
        # Handle other object types
        return _convert_to_yaml_safe(data.__dict__)
    else:
        return data


def load_rules_from_json(
    file_path: str,
) -> Union[Rule, RuleCombination, RulePackage, List]:
    """
    Load rules from JSON file

    Args:
        file_path: JSON file path

    Returns:
        Loaded rule object
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return _parse_rules_data(data)


def load_rules_from_yaml(
    file_path: str,
) -> Union[Rule, RuleCombination, RulePackage, List]:
    """
    Load rules from YAML file

    Args:
        file_path: YAML file path

    Returns:
        Loaded rule object
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return _parse_rules_data(data)


def save_rules_to_json(
    rules: Union[Rule, RuleCombination, RulePackage, List], file_path: str
) -> None:
    """
    Save rules to JSON file

    Args:
        rules: Rules to save
        file_path: JSON file path
    """
    # Ensure directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    # Convert rules to dictionary and handle special types
    if isinstance(rules, list):
        data = [
            _convert_to_yaml_safe(rule.to_dict() if hasattr(rule, "to_dict") else rule)
            for rule in rules
        ]
    elif hasattr(rules, "to_dict"):
        data = _convert_to_yaml_safe(rules.to_dict())
    else:
        data = _convert_to_yaml_safe(rules)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_rules_to_yaml(
    rules: Union[Rule, RuleCombination, RulePackage, List], file_path: str
) -> None:
    """
    Save rules to YAML file

    Args:
        rules: Rules to save
        file_path: YAML file path
    """
    # Ensure directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    # Convert rules to dictionary and handle special types
    if isinstance(rules, list):
        data = [
            _convert_to_yaml_safe(rule.to_dict() if hasattr(rule, "to_dict") else rule)
            for rule in rules
        ]
    elif hasattr(rules, "to_dict"):
        data = _convert_to_yaml_safe(rules.to_dict())
    else:
        data = _convert_to_yaml_safe(rules)

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)


def _parse_rules_data(
    data: Union[Dict[str, Any], List],
) -> Union[Rule, RuleCombination, RulePackage, List]:
    """
    Parse rules data

    Args:
        data: Rules data

    Returns:
        Parsed rule object
    """
    if isinstance(data, list):
        # Handle list of rules
        parsed_rules = []
        for item in data:
            parsed_rules.append(_parse_single_rule(item))
        return parsed_rules
    else:
        # Handle single rule
        return _parse_single_rule(data)


def _parse_single_rule(
    data: Dict[str, Any],
) -> Union[Rule, RuleCombination, RulePackage]:
    """
    Parse single rule data

    Args:
        data: Single rule data dictionary

    Returns:
        Parsed rule object
    """
    rule_type = data.get("rule_type", "record")

    if rule_type == "record":
        return Rule.from_dict(data)
    elif rule_type == "combination":
        return RuleCombination.from_dict(data)
    elif rule_type == "package":
        return RulePackage.from_dict(data)
    else:
        # Default to record type
        return Rule.from_dict(data)


def create_rule_template(rule_type: str = "record") -> Dict[str, Any]:
    """
    Create rule template

    Args:
        rule_type: Rule type ('record', 'combination', 'package')

    Returns:
        Rule template dictionary
    """
    if rule_type == "record":
        return {
            "name": "example_field",
            "description": "Generate an example field",
            "rule_type": "record",
            "examples": ["example1", "example2"],
            "constraints": {"type": "string", "min_length": 1, "max_length": 100},
            "metadata": {},
        }
    elif rule_type == "combination":
        return {
            "name": "example_combination",
            "description": "Combine multiple fields",
            "rules": ["field1", "field2"],
            "combination_logic": "and",
            "rule_type": "combination",
            "metadata": {},
        }
    elif rule_type == "package":
        return {
            "name": "example_package",
            "description": "Complete example object",
            "rules": ["field1", "field2", "field3"],
            "rule_type": "package",
            "category": "general",
            "version": "1.0.0",
            "metadata": {},
        }
    else:
        raise ValueError(f"Unknown rule type: {rule_type}")
