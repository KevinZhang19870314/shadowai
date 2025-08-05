"""
ShadowAI Core Module

Provides main data generation functionality, integrating the Agno framework.
"""

import json
from typing import Any, Dict, List, Optional, Union

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel

from .rule import Rule, RuleType
from .rule_combination import RuleCombination
from .rule_package import RulePackage


class MockDataResponse(BaseModel):
    """Mock data response model"""

    data: Union[Dict[str, Any], List[Dict[str, Any]]]
    success: bool = True
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ShadowAI:
    """
    ShadowAI Main Class

    Provides AI-driven mock data generation functionality.
    """

    def __init__(
        self, model_id: str = "gpt-4o-mini", api_key: Optional[str] = None, **kwargs
    ):
        """
        Initialize ShadowAI instance

        Args:
            model_id: AI model ID
            api_key: API key (optional, can be obtained from environment variables)
            **kwargs: Other configuration parameters
        """
        self.model_id = model_id
        self.api_key = api_key

        # Initialize AI model
        self.model = OpenAIChat(id=model_id, api_key=api_key, **kwargs)

        # Initialize Agent
        self.agent = Agent(
            model=self.model,
            name="ShadowAI",
            description="AI-powered mock data generator",
        )

    def generate(
        self,
        rules: Union[
            Rule, RuleCombination, RulePackage, List[Union[Rule, str]], str, list, dict
        ],
        count: int = 1,
        format_output: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], MockDataResponse]:
        """
        Generate mock data

        Args:
            rules: Rules to use for generation (supports multiple formats)
            count: Number of records to generate
            format_output: Whether to return formatted response

        Returns:
            Generated mock data or formatted response
        """
        try:
            # Convert input to Rule objects
            processed_rules = self._process_rules(rules)

            # Generate prompt
            prompt = self._build_prompt(processed_rules, count)

            # Call AI to generate data
            response = self.agent.run(prompt)

            # Parse response
            data = self._parse_response(response)

            # Return based on format_output parameter
            if format_output:
                return MockDataResponse(
                    data=data,
                    success=True,
                    metadata={
                        "model_id": self.model_id,
                        "rules_count": (
                            len(processed_rules)
                            if isinstance(processed_rules, list)
                            else 1
                        ),
                        "generated_count": count,
                    },
                )
            else:
                return data

        except Exception as e:
            if format_output:
                return MockDataResponse(data={}, success=False, error=str(e))
            else:
                raise e

    def quick(self, *field_names: str) -> Dict[str, Any]:
        """
        Quick generation method - generate data for multiple fields at once

        Args:
            *field_names: Field names to generate

        Returns:
            Generated data dictionary
        """
        rules = [Rule(name=name) for name in field_names]
        return self.generate(rules, format_output=False)

    def _process_rules(
        self,
        rules: Union[
            Rule, RuleCombination, RulePackage, List[Union[Rule, str]], str, list, dict
        ],
    ) -> List[Rule]:
        """
        Process input rules into standard Rule objects

        Args:
            rules: Input rules

        Returns:
            List of Rule objects
        """
        if isinstance(rules, str):
            # Single string, create Rule
            return [Rule(name=rules)]

        elif isinstance(rules, Rule):
            # Single Rule object
            return [rules]

        elif isinstance(rules, (RuleCombination, RulePackage)):
            # RuleCombination or RulePackage
            return [rules]

        elif isinstance(rules, list):
            # List of rules
            processed = []
            for rule in rules:
                if isinstance(rule, str):
                    processed.append(Rule(name=rule))
                elif isinstance(rule, Rule):
                    processed.append(rule)
                else:
                    raise ValueError(f"Unsupported rule type in list: {type(rule)}")
            return processed

        elif isinstance(rules, dict):
            # Dictionary format (loaded from file)
            return [self._dict_to_rule(rules)]

        else:
            raise ValueError(f"Unsupported rules type: {type(rules)}")

    def _dict_to_rule(
        self, rule_dict: dict
    ) -> Union[Rule, RuleCombination, RulePackage]:
        """
        Convert dictionary to Rule object

        Args:
            rule_dict: Rule dictionary

        Returns:
            Rule object
        """
        rule_type = rule_dict.get("rule_type", "record")

        if rule_type == "record":
            return Rule(**rule_dict)
        elif rule_type == "combination":
            return RuleCombination(**rule_dict)
        elif rule_type == "package":
            return RulePackage(**rule_dict)
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")

    def _build_prompt(self, rules: List[Rule], count: int) -> str:
        """
        Build generation prompt

        Args:
            rules: Rule list
            count: Number of records to generate

        Returns:
            Generation prompt
        """
        if len(rules) == 1 and isinstance(rules[0], (RuleCombination, RulePackage)):
            # Use RuleCombination or RulePackage
            rule = rules[0]
            prompt_parts = [
                f"Please generate {count} record(s) of mock data based on the following rule definition:",
                f"",
                f"Rule Name: {rule.name}",
                f"Description: {rule.description}",
                f"Type: {rule.rule_type}",
            ]

            if hasattr(rule, "rules") and rule.rules:
                prompt_parts.append(f"Fields to include: {rule.rules}")

            if hasattr(rule, "examples") and rule.examples:
                prompt_parts.append(f"Examples: {rule.examples}")

            if hasattr(rule, "constraints") and rule.constraints:
                prompt_parts.append(f"Constraints: {rule.constraints}")

        else:
            # Use multiple Rule objects
            prompt_parts = [
                f"Please generate {count} record(s) of mock data with the following fields:",
                "",
            ]

            for rule in rules:
                prompt_parts.append(f"- {rule.name}: {rule.description}")
                if rule.examples:
                    prompt_parts.append(f"  Examples: {rule.examples}")
                if rule.constraints:
                    prompt_parts.append(f"  Constraints: {rule.constraints}")

        prompt_parts.extend(
            [
                "",
                "IMPORTANT: Return data in FLAT JSON format only.",
                "- Each field should contain a simple value (string, number, or boolean)",
                "- Do NOT use nested objects or complex structures",
                "- For combination fields, return a single combined string value",
                "",
                f"If generating multiple records, return an array of {count} objects.",
                "If generating a single record, return a single object.",
                "Ensure the data is realistic and follows the given constraints and examples.",
            ]
        )

        return "\n".join(prompt_parts)

    def _parse_response(
        self, response: Union[str, Any]
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse AI response

        Args:
            response: AI response (string or object with .content attribute)

        Returns:
            Parsed data
        """
        try:
            # Extract response content
            if hasattr(response, "content"):
                response_str = response.content
            else:
                response_str = str(response)

            # Try to extract JSON from response
            response_str = response_str.strip()

            # Check for array first (priority over object)
            array_start = response_str.find("[")
            array_end = response_str.rfind("]")

            if array_start != -1 and array_end != -1:
                json_str = response_str[array_start : array_end + 1]
                return json.loads(json_str)

            # Then check for object
            obj_start = response_str.find("{")
            obj_end = response_str.rfind("}")

            if obj_start != -1 and obj_end != -1:
                json_str = response_str[obj_start : obj_end + 1]
                return json.loads(json_str)

            # If no valid JSON structure found
            raise ValueError("No valid JSON found in response")

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

    def load_rules_from_file(
        self, file_path: str
    ) -> Union[Rule, RuleCombination, RulePackage, List]:
        """
        Load rules from file

        Args:
            file_path: File path

        Returns:
            Loaded rules
        """
        from ..utils.file_utils import load_rules_from_json, load_rules_from_yaml

        if file_path.endswith(".json"):
            return load_rules_from_json(file_path)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return load_rules_from_yaml(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}") 