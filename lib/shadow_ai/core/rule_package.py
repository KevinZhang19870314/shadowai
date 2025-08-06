"""
Rule Package Module

Defines the structure of rule packages for organizing a set of related rules and rule combinations.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .rule import Rule, RuleType
from .rule_combination import RuleCombination


class RulePackage(BaseModel):
    """
    Rule Package Class

    Used to organize a set of related rules and rule combinations into complete data objects.
    """

    name: str = Field(..., description="Rule package name")
    description: Optional[str] = Field(default=None, description="Rule package description")
    rules: List[Union[str, Rule, RuleCombination]] = Field(
        ..., description="List of contained rules"
    )
    category: Optional[str] = Field(default=None, description="Rule package category")
    version: str = Field(default="1.0.0", description="Rule package version")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Package metadata")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v

    def __init__(self, **data):
        # If no description provided, auto-generate
        if "description" not in data or data["description"] is None:
            name = data.get("name", "package")
            if name is None:
                name = "package"
            data["description"] = f"A collection of rules for {name.replace('_', ' ')}"
        super().__init__(**data)

    @property
    def rule_type(self) -> RuleType:
        """Return rule type"""
        return RuleType.PACKAGE

    @classmethod
    def create(
        cls,
        name: str,
        rules: List[Union[str, Rule, RuleCombination]],
        description: str = None,
        category: str = None,
        version: str = "1.0.0",
    ) -> "RulePackage":
        """
        Create rule package

        Args:
            name: Package name
            rules: List of rules to include
            description: Optional description
            category: Package category
            version: Package version

        Returns:
            RulePackage object
        """
        return cls(
            name=name,
            rules=rules,
            description=description,
            category=category,
            version=version,
        )

    @classmethod
    def quick(cls, name: str, *rule_names: str) -> "RulePackage":
        """
        Quick create rule package from rule names

        Args:
            name: Package name
            *rule_names: Rule names to include

        Returns:
            RulePackage object
        """
        return cls(name=name, rules=list(rule_names))

    @classmethod
    def simple(cls, input_str: str) -> "RulePackage":
        """
        Create rule package from string parsing

        Args:
            input_str: Input string like "person [name, email, age, phone]"

        Returns:
            RulePackage object
        """
        # Parse string like "person [name, email, age, phone]"
        if "[" in input_str and "]" in input_str:
            name_part, rules_part = input_str.split("[", 1)
            name = name_part.strip()

            # Extract rule names from brackets
            rules_str = rules_part.split("]")[0]
            rule_names = [rule.strip() for rule in rules_str.split(",") if rule.strip()]

            return cls(name=name, rules=rule_names)
        else:
            raise ValueError(f"Invalid package string format: {input_str}")

    @classmethod
    def from_rules(
        cls, name: str, rules: List[Union[str, Rule, "RuleCombination"]]
    ) -> "RulePackage":
        """
        Create rule package from list of rules

        Args:
            name: Package name
            rules: List of rules

        Returns:
            RulePackage object
        """
        return cls(name=name, rules=rules)

    def with_category(self, category: str) -> "RulePackage":
        """
        Set category (instance method for chaining)

        Args:
            category: Package category

        Returns:
            New RulePackage object with updated category
        """
        return RulePackage(
            name=self.name,
            description=self.description,
            rules=self.rules,
            category=category,
            version=self.version,
            metadata=self.metadata,
        )

    def with_version(self, version: str) -> "RulePackage":
        """
        Set version (instance method for chaining)

        Args:
            version: Package version

        Returns:
            New RulePackage object with updated version
        """
        return RulePackage(
            name=self.name,
            description=self.description,
            rules=self.rules,
            category=self.category,
            version=version,
            metadata=self.metadata,
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

    def get_rule_objects(self) -> List[Union[Rule, RuleCombination]]:
        """
        Get rule objects

        Returns:
            List of Rule/RuleCombination objects
        """
        rule_objects = []
        for rule in self.rules:
            if isinstance(rule, (Rule, RuleCombination)):
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

    def add_rule(self, rule: Union[str, Rule, RuleCombination]) -> "RulePackage":
        """
        Add rule (chain call)

        Args:
            rule: Rule to add

        Returns:
            Self for chain calling
        """
        self.rules.append(rule)
        return self

    def remove_rule(self, rule_name: str) -> "RulePackage":
        """
        Remove rule by name (chain call)

        Args:
            rule_name: Name of rule to remove

        Returns:
            Self for chain calling
        """
        self.rules = [
            rule
            for rule in self.rules
            if not (
                (isinstance(rule, str) and rule == rule_name)
                or (hasattr(rule, "name") and rule.name == rule_name)
            )
        ]
        return self

    def has_rule(self, rule_name: str) -> bool:
        """
        Check if package contains rule

        Args:
            rule_name: Rule name to check

        Returns:
            True if rule exists
        """
        for rule in self.rules:
            if isinstance(rule, str) and rule == rule_name:
                return True
            elif hasattr(rule, "name") and rule.name == rule_name:
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary

        Returns:
            Dictionary representation
        """
        rules_data = []
        for rule in self.rules:
            if isinstance(rule, str):
                rules_data.append(rule)
            elif hasattr(rule, "to_dict"):
                rules_data.append(rule.to_dict())
            else:
                rules_data.append(str(rule))

        return {
            "name": self.name,
            "description": self.description,
            "rules": rules_data,
            "category": self.category,
            "version": self.version,
            "metadata": self.metadata,
            "rule_type": self.rule_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RulePackage":
        """
        Create from dictionary

        Args:
            data: Dictionary data

        Returns:
            RulePackage object
        """
        # Convert rule data to Rule/RuleCombination objects
        rules = []
        for rule_data in data.get("rules", []):
            if isinstance(rule_data, dict):
                rule_type = rule_data.get("rule_type", "record")
                if rule_type == "record":
                    rules.append(Rule.from_dict(rule_data))
                elif rule_type == "combination":
                    rules.append(RuleCombination.from_dict(rule_data))
                else:
                    rules.append(rule_data)
            else:
                rules.append(rule_data)

        return cls(
            name=data["name"],
            description=data.get("description"),
            rules=rules,
            category=data.get("category"),
            version=data.get("version", "1.0.0"),
            metadata=data.get("metadata"),
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
            f"Package: {self.name}",
            f"Description: {self.description}",
            f"Rules: {rules_text}",
        ]

        if self.category:
            prompt_parts.append(f"Category: {self.category}")

        return " | ".join(prompt_parts)

    def get_package_info(self) -> Dict[str, Any]:
        """
        Get package information

        Returns:
            Package information dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "rule_count": len(self.rules),
            "rule_names": self.get_rule_names(),
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        rule_count = len(self.rules)
        return f"RulePackage(name='{self.name}', rules={rule_count})"

    def __repr__(self) -> str:
        return self.__str__()
