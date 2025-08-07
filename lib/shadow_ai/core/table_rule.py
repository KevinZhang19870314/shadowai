"""
Table Rule Module

Defines the structure of table rules for generating tabular data.
"""

from typing import Any, Dict, List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from .rule import Rule, RuleType
from .rule_package import RulePackage


class TableOutputFormat(str, Enum):
    """Table output format enumeration"""
    
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    HTML = "html"


class TableRule(RulePackage):
    """
    Table Rule Class
    
    Specialized rule package for generating tabular data with multiple rows and columns.
    """
    
    columns: List[Union[str, Rule]] = Field(..., description="List of column definitions")
    rows_count: int = Field(default=5, description="Number of rows to generate")
    table_name: Optional[str] = Field(default=None, description="Table name")
    output_format: TableOutputFormat = Field(default=TableOutputFormat.JSON, description="Output format")
    
    def __init__(self, **data):
        # Convert columns to rules if needed
        if "columns" in data:
            columns = data["columns"]
            processed_columns = []
            for col in columns:
                if isinstance(col, str):
                    processed_columns.append(Rule(name=col))
                elif isinstance(col, Rule):
                    processed_columns.append(col)
                else:
                    processed_columns.append(Rule(name=str(col)))
            data["columns"] = processed_columns
            
            # Set rules from columns for compatibility with RulePackage
            if "rules" not in data:
                data["rules"] = processed_columns
        
        # Set table_name from name if not provided
        if "table_name" not in data or data["table_name"] is None:
            data["table_name"] = data.get("name", "table")
        
        # Auto-generate description for table
        if "description" not in data or data["description"] is None:
            table_name = data.get("table_name", "table")
            rows_count = data.get("rows_count", 5)
            col_names = []
            for col in data.get("columns", []):
                if isinstance(col, str):
                    col_names.append(col)
                elif hasattr(col, "name"):
                    col_names.append(col.name)
            cols_text = ", ".join(col_names[:3])
            if len(col_names) > 3:
                cols_text += f" and {len(col_names) - 3} more"
            data["description"] = f"Generate a {table_name} table with {rows_count} rows and columns: {cols_text}"
        
        super().__init__(**data)
    
    @property
    def rule_type(self) -> RuleType:
        """Return rule type"""
        return RuleType.PACKAGE  # TableRule extends RulePackage
    
    @classmethod
    def create(
        cls,
        name: str,
        columns: List[Union[str, Rule]],
        rows_count: int = 5,
        output_format: TableOutputFormat = TableOutputFormat.JSON,
        description: str = None,
        table_name: str = None,
    ) -> "TableRule":
        """
        Create table rule
        
        Args:
            name: Rule name
            columns: List of column definitions
            rows_count: Number of rows to generate
            output_format: Output format
            description: Optional description
            table_name: Optional table name
            
        Returns:
            TableRule object
        """
        return cls(
            name=name,
            columns=columns,
            rows_count=rows_count,
            output_format=output_format,
            description=description,
            table_name=table_name or name,
        )
    
    @classmethod
    def quick(cls, name: str, *column_names: str, rows_count: int = 5) -> "TableRule":
        """
        Quick create table rule from column names
        
        Args:
            name: Table name
            *column_names: Column names
            rows_count: Number of rows to generate
            
        Returns:
            TableRule object
        """
        return cls(
            name=name,
            columns=list(column_names),
            rows_count=rows_count,
            table_name=name,
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TableRule":
        """
        Create from dictionary
        
        Args:
            data: Dictionary data
            
        Returns:
            TableRule object
        """
        # Handle columns conversion
        columns = []
        for col_data in data.get("columns", []):
            if isinstance(col_data, dict):
                columns.append(Rule.from_dict(col_data))
            elif isinstance(col_data, str):
                columns.append(col_data)
            else:
                columns.append(str(col_data))
        
        return cls(
            name=data["name"],
            columns=columns,
            rows_count=data.get("rows_count", 5),
            output_format=data.get("output_format", TableOutputFormat.JSON),
            description=data.get("description"),
            table_name=data.get("table_name"),
            category=data.get("category"),
            version=data.get("version", "1.0.0"),
            metadata=data.get("metadata"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        columns_data = []
        for col in self.columns:
            if hasattr(col, "to_dict"):
                columns_data.append(col.to_dict())
            else:
                columns_data.append(str(col))
        
        return {
            "name": self.name,
            "description": self.description,
            "columns": columns_data,
            "rows_count": self.rows_count,
            "table_name": self.table_name,
            "output_format": self.output_format,
            "category": self.category,
            "version": self.version,
            "metadata": self.metadata,
            "rule_type": "table",  # Special type for table rules
        }
    
    def get_column_names(self) -> List[str]:
        """
        Get column names
        
        Returns:
            List of column names
        """
        names = []
        for col in self.columns:
            if isinstance(col, str):
                names.append(col)
            elif hasattr(col, "name"):
                names.append(col.name)
            else:
                names.append(str(col))
        return names
    
    def add_column(self, column: Union[str, Rule]) -> "TableRule":
        """
        Add column to table
        
        Args:
            column: Column to add
            
        Returns:
            Self for chaining
        """
        if isinstance(column, str):
            self.columns.append(Rule(name=column))
            self.rules.append(Rule(name=column))
        else:
            self.columns.append(column)
            self.rules.append(column)
        return self
    
    def set_rows_count(self, count: int) -> "TableRule":
        """
        Set number of rows to generate
        
        Args:
            count: Number of rows
            
        Returns:
            Self for chaining
        """
        self.rows_count = count
        return self
    
    def set_output_format(self, format: TableOutputFormat) -> "TableRule":
        """
        Set output format
        
        Args:
            format: Output format
            
        Returns:
            Self for chaining
        """
        self.output_format = format
        return self
    
    def to_prompt(self) -> str:
        """
        Convert to AI prompt text optimized for table generation
        
        Returns:
            Prompt text
        """
        column_names = self.get_column_names()
        columns_text = ", ".join(column_names)
        
        prompt_parts = [
            f"Generate a table named '{self.table_name}' with {self.rows_count} rows",
            f"Columns: {columns_text}",
            f"Description: {self.description}",
        ]
        
        # Add column details if available
        column_details = []
        for col in self.columns:
            if hasattr(col, "description") and col.description:
                column_details.append(f"  - {col.name}: {col.description}")
                if hasattr(col, "examples") and col.examples:
                    column_details.append(f"    Examples: {col.examples}")
                if hasattr(col, "constraints") and col.constraints:
                    column_details.append(f"    Constraints: {col.constraints}")
        
        if column_details:
            prompt_parts.append("Column specifications:")
            prompt_parts.extend(column_details)
        
        return "\n".join(prompt_parts)
    
    def __str__(self) -> str:
        column_count = len(self.columns)
        return f"TableRule(name='{self.name}', columns={column_count}, rows={self.rows_count})"
    
    def __repr__(self) -> str:
        return self.__str__() 