"""
MockAI - AI-powered mock data generation library

An AI-powered intelligent mock data generation library that supports flexible rule engines and plugin systems.
"""

from .core.mock_ai import MockAI
from .core.rule import Rule, RuleType
from .core.rule_combination import RuleCombination
from .core.rule_package import RulePackage

__version__ = "0.1.1"
__author__ = "MockAI Team"
__email__ = "team@mock-ai.com"

__all__ = [
    "MockAI",
    "Rule",
    "RuleType",
    "RulePackage",
    "RuleCombination",
]
