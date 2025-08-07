"""
ShadowAI - AI-powered mock data generation library

An AI-powered intelligent mock data generation library that supports flexible rule engines and plugin systems.
"""

from .core.rule import Rule, RuleType
from .core.rule_combination import RuleCombination
from .core.rule_package import RulePackage
from .core.table_rule import TableRule, TableOutputFormat
from .core.shadow_ai import ShadowAI
from .utils.table_formatter import TableFormatter, TableTemplates

__version__ = "0.2.0"
__author__ = "ShadowAI Team"
__email__ = "team@shadowai.com"

__all__ = [
    "ShadowAI",
    "Rule",
    "RuleType",
    "RulePackage",
    "RuleCombination",
    "TableRule",
    "TableOutputFormat",
    "TableFormatter",
    "TableTemplates",
]
