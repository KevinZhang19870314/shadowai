"""
ShadowAI Rule Definition Module

Defines core types for the rule engine: Rule (rule record)
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class RuleType(str, Enum):
    """Rule type enumeration"""

    RECORD = "record"  # Rule record: generation rule for a single field
    COMBINATION = "combination"  # Rule combination: combination rule for multiple fields
    PACKAGE = "package"  # Rule package: a set of related rules


class Rule(BaseModel):
    """
    Rule Class - Basic unit of the rule engine

    Defines the structure of a single rule record, including field name, description, and generation instructions.
    """

    name: str = Field(..., description="Rule name/field name")
    description: Optional[str] = Field(
        default=None, description="Rule description, guides AI data generation"
    )
    rule_type: RuleType = Field(default=RuleType.RECORD, description="Rule type")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Rule metadata")
    examples: Optional[list] = Field(default=None, description="Example data")
    constraints: Optional[Dict[str, Any]] = Field(default=None, description="Constraint conditions")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v

    def __init__(self, **data):
        # If no description provided, auto-generate
        if "description" not in data or data["description"] is None:
            name = data.get("name", "field")
            if name is not None:
                data["description"] = f"Generate a {name.replace('_', ' ')}"
            else:
                data["description"] = "Generate a field"
        super().__init__(**data)

    @classmethod
    def simple(cls, input_str: str, description: str = None) -> "Rule":
        """
        Create a simple rule with string parsing support

        Args:
            input_str: Field input string (supports "name", "name: description", "name|example1,example2")
            description: Field description (optional, auto-generated if not provided)

        Returns:
            Rule object
        """
        # Parse input string
        if ": " in input_str:
            # Format: "name: description"
            name, parsed_description = input_str.split(": ", 1)
            if description is None:
                description = parsed_description
        elif "|" in input_str:
            # Format: "name|example1,example2,example3"
            name, examples_str = input_str.split("|", 1)
            examples = [ex.strip() for ex in examples_str.split(",")]
            if description is None:
                description = (
                    f"Generate a {name.replace('_', ' ')} similar to the provided examples"
                )
            return cls(
                name=name,
                description=description,
                examples=examples,
                rule_type=RuleType.RECORD,
            )
        else:
            # Simple name
            name = input_str
            if description is None:
                description = f"Generate a {name.replace('_', ' ')}"

        return cls(name=name, description=description, rule_type=RuleType.RECORD)

    @classmethod
    def with_examples(cls, name: str, examples: List[Any], description: str = None) -> "Rule":
        """
        Create a rule with examples

        Args:
            name: Field name
            examples: Example list
            description: Field description (optional)

        Returns:
            Rule object
        """
        if description is None:
            description = f"Generate a {name.replace('_', ' ')} similar to the provided examples"

        return cls(
            name=name,
            description=description,
            examples=examples,
            rule_type=RuleType.RECORD,
        )

    @classmethod
    def with_constraints(
        cls, name: str, constraints: Dict[str, Any], description: str = None
    ) -> "Rule":
        """
        Create a rule with constraints

        Args:
            name: Field name
            constraints: Constraint dictionary
            description: Field description (optional)

        Returns:
            Rule object
        """
        if description is None:
            description = f"Generate a {name.replace('_', ' ')} following specified constraints"

        return cls(
            name=name,
            description=description,
            constraints=constraints,
            rule_type=RuleType.RECORD,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "rule_type": self.rule_type,
            "metadata": self.metadata,
            "examples": self.examples,
            "constraints": self.constraints,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rule":
        """
        Create from dictionary

        Args:
            data: Dictionary data

        Returns:
            Rule object
        """
        return cls(**data)

    def to_prompt(self) -> str:
        """
        Convert to AI prompt text

        Returns:
            Prompt text
        """
        prompt_parts = [f"{self.name} ({self.description})"]

        if self.examples:
            prompt_parts.append(f"Examples: {self.examples}")

        if self.constraints:
            constraints_text = ", ".join([f"{k}={v}" for k, v in self.constraints.items()])
            prompt_parts.append(f"Constraints: {constraints_text}")

        return ". ".join(prompt_parts)

    def __str__(self) -> str:
        return f"Rule(name='{self.name}', type='{self.rule_type}')"

    def __repr__(self) -> str:
        return self.__str__()

    def with_examples(self, *examples: Any) -> "Rule":
        """
        Add examples to this rule (instance method for chaining)

        Args:
            *examples: Examples to add

        Returns:
            New Rule object with examples
        """
        return Rule(
            name=self.name,
            description=self.description,
            examples=list(examples),
            constraints=self.constraints,
            rule_type=self.rule_type,
            metadata=self.metadata,
        )

    def with_constraints(self, **constraints: Any) -> "Rule":
        """
        Add constraints to this rule (instance method for chaining)

        Args:
            **constraints: Constraints to add

        Returns:
            New Rule object with constraints
        """
        return Rule(
            name=self.name,
            description=self.description,
            examples=self.examples,
            constraints=constraints,
            rule_type=self.rule_type,
            metadata=self.metadata,
        )

    @classmethod
    def from_dict_simple(cls, data: Dict[str, Any]) -> "Rule":
        """
        Create from dictionary with simple validation

        Args:
            data: Dictionary data

        Returns:
            Rule object
        """
        return cls(**data)
