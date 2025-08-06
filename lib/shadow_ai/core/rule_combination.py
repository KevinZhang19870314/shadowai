"""
Rule Combination Module

Defines the structure of rule combinations for combining multiple rules to generate composite fields.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .rule import Rule, RuleType


class RuleCombination(BaseModel):
    """
    Rule Combination Class

    Used to define combination logic for multiple rules, generating composite field data.
    """

    name: str = Field(..., description="Combination name")
    description: Optional[str] = Field(default=None, description="Combination description")
    rules: List[Union[str, Rule]] = Field(
        ..., description="List of contained rules (rule names or rule objects)"
    )
    combination_logic: Optional[str] = Field(
        default="combine", description="Combination logic description"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v

    def __init__(self, **data):
        # If no description provided, auto-generate
        if "description" not in data or data["description"] is None:
            name = data.get("name", "combination")
            rules = data.get("rules", [])
            if name is None:
                name = "combination"

            if rules:
                rule_names = []
                for rule in rules:
                    if isinstance(rule, str):
                        rule_names.append(rule)
                    elif hasattr(rule, "name"):
                        rule_names.append(rule.name)
                rules_text = ", ".join(rule_names[:3])  # Limit the number of displayed rules
                data["description"] = f"Combine {rules_text} to create {name.replace('_', ' ')}"
            else:
                data["description"] = f"Combination for {name.replace('_', ' ')}"

        super().__init__(**data)

    @property
    def rule_type(self) -> RuleType:
        """Return rule type"""
        return RuleType.COMBINATION

    @classmethod
    def create(
        cls,
        name: str,
        rules: List[Union[str, Rule]],
        description: str = None,
        combination_logic: str = "combine",
    ) -> "RuleCombination":
        """
        Create rule combination

        Args:
            name: Combination name
            rules: Rule list
            description: Description (optional, auto-generated if not provided)
            combination_logic: Combination logic

        Returns:
            RuleCombination object
        """
        return cls(
            name=name,
            rules=rules,
            description=description,
            combination_logic=combination_logic,
        )

    @classmethod
    def quick(cls, name: str, *rule_names: str) -> "RuleCombination":
        """
        Quick create rule combination from rule names

        Args:
            name: Combination name
            *rule_names: Rule names to combine

        Returns:
            RuleCombination object
        """
        return cls(name=name, rules=list(rule_names), combination_logic="combine")

    @classmethod
    def simple(cls, input_str: str) -> "RuleCombination":
        """
        Create rule combination from string parsing

        Args:
            input_str: Input string like "full_name = first_name + last_name"

        Returns:
            RuleCombination object
        """
        # Parse string like "full_name = first_name + last_name"
        if "=" in input_str:
            name, rules_part = input_str.split("=", 1)
            name = name.strip()

            # Extract rule names (split by + and clean up)
            rule_names = []
            for part in rules_part.split("+"):
                rule_name = part.strip()
                if rule_name:
                    rule_names.append(rule_name)

            return cls(name=name, rules=rule_names, combination_logic="join")
        else:
            raise ValueError(f"Invalid combination string format: {input_str}")

    def with_logic(self, logic: str) -> "RuleCombination":
        """
        Set combination logic (instance method for chaining)

        Args:
            logic: Combination logic

        Returns:
            New RuleCombination object with updated logic
        """
        return RuleCombination(
            name=self.name,
            description=self.description,
            rules=self.rules,
            combination_logic=logic,
        )

    def get_rule_names(self) -> List[str]:
        """
        Get rule names

        Returns:
            List of rule names
        """
        names = []
        for rule in self.rules:
            if isinstance(rule, str):
                names.append(rule)
            elif hasattr(rule, "name"):
                names.append(rule.name)
            else:
                names.append(str(rule))
        return names

    def get_rule_objects(self) -> List[Rule]:
        """
        Get rule objects

        Returns:
            List of Rule objects
        """
        rule_objects = []
        for rule in self.rules:
            if isinstance(rule, Rule):
                rule_objects.append(rule)
            elif isinstance(rule, str):
                # Create simple rule for string
                rule_objects.append(Rule(name=rule))
            else:
                # Try to convert to Rule
                if hasattr(rule, "name"):
                    rule_objects.append(Rule(name=rule.name))
                else:
                    rule_objects.append(Rule(name=str(rule)))
        return rule_objects

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "rules": [r.to_dict() if hasattr(r, "to_dict") else r for r in self.rules],
            "combination_logic": self.combination_logic,
            "rule_type": self.rule_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RuleCombination":
        """
        Create from dictionary

        Args:
            data: Dictionary data

        Returns:
            RuleCombination object
        """
        # Convert rule data to Rule objects
        rules = []
        for rule_data in data.get("rules", []):
            if isinstance(rule_data, dict):
                if rule_data.get("rule_type") == "record":
                    rules.append(Rule.from_dict(rule_data))
                else:
                    rules.append(rule_data)
            else:
                rules.append(rule_data)

        return cls(
            name=data["name"],
            description=data.get("description"),
            rules=rules,
            combination_logic=data.get("combination_logic", "combine"),
        )

    def to_prompt(self) -> str:
        """
        Convert to AI prompt text

        Returns:
            Prompt text
        """
        rule_names = self.get_rule_names()
        rules_text = ", ".join(rule_names)

        prompt_parts = [
            f"Combination: {self.name}",
            f"Description: {self.description}",
            f"Rules: {rules_text}",
            f"Logic: {self.combination_logic}",
        ]

        return " | ".join(prompt_parts)

    def add_rule(self, rule: Union[str, Rule]) -> "RuleCombination":
        """
        Add rule (chain call)

        Args:
            rule: Rule to add

        Returns:
            Self for chain calling
        """
        self.rules.append(rule)
        return self

    def __str__(self) -> str:
        rule_names = self.get_rule_names()
        return f"RuleCombination(name='{self.name}', rules={rule_names})"

    def __repr__(self) -> str:
        return self.__str__()
