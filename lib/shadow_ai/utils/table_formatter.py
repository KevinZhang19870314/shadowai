"""
Table Formatter Module

Provides utilities for formatting tabular data into different output formats.
"""

import csv
import json
from io import StringIO
from typing import Any, Dict, List, Union

from ..core.table_rule import TableOutputFormat


class TableFormatter:
    """
    Table Formatter Class
    
    Converts tabular data into various output formats including markdown, CSV, HTML, and JSON.
    """
    
    @staticmethod
    def format_table(
        data: List[Dict[str, Any]], 
        output_format: TableOutputFormat = TableOutputFormat.JSON,
        table_name: str = "table"
    ) -> str:
        """
        Format table data to specified output format
        
        Args:
            data: List of dictionaries representing table rows
            output_format: Desired output format
            table_name: Name of the table (used in some formats)
            
        Returns:
            Formatted table string
        """
        if not data:
            return ""
        
        if output_format == TableOutputFormat.MARKDOWN:
            return TableFormatter.to_markdown(data, table_name)
        elif output_format == TableOutputFormat.CSV:
            return TableFormatter.to_csv(data)
        elif output_format == TableOutputFormat.HTML:
            return TableFormatter.to_html(data, table_name)
        elif output_format == TableOutputFormat.JSON:
            return TableFormatter.to_json(data)
        else:
            return TableFormatter.to_json(data)  # Default fallback
    
    @staticmethod
    def to_markdown(data: List[Dict[str, Any]], table_name: str = "table") -> str:
        """
        Convert table data to Markdown format
        
        Args:
            data: Table data
            table_name: Table name for title
            
        Returns:
            Markdown formatted table
        """
        if not data:
            return f"# {table_name}\n\n*No data available*"
        
        # Get column names from first row
        columns = list(data[0].keys())
        
        # Start with table title
        result = [f"# {table_name}", ""]
        
        # Create header row
        header = "| " + " | ".join(columns) + " |"
        result.append(header)
        
        # Create separator row
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"
        result.append(separator)
        
        # Add data rows
        for row in data:
            row_values = []
            for col in columns:
                value = row.get(col, "")
                # Escape pipes and format value
                formatted_value = str(value).replace("|", "\\|").replace("\n", "<br>")
                row_values.append(formatted_value)
            row_line = "| " + " | ".join(row_values) + " |"
            result.append(row_line)
        
        return "\n".join(result)
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]]) -> str:
        """
        Convert table data to CSV format
        
        Args:
            data: Table data
            
        Returns:
            CSV formatted string
        """
        if not data:
            return ""
        
        # Get column names from first row
        columns = list(data[0].keys())
        
        # Use StringIO to write CSV data
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=columns)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for row in data:
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def to_html(data: List[Dict[str, Any]], table_name: str = "table") -> str:
        """
        Convert table data to HTML format
        
        Args:
            data: Table data
            table_name: Table name for title
            
        Returns:
            HTML formatted table
        """
        if not data:
            return f"<h1>{table_name}</h1><p><em>No data available</em></p>"
        
        # Get column names from first row
        columns = list(data[0].keys())
        
        # Start HTML structure
        html = [
            f"<h1>{table_name}</h1>",
            '<table border="1" cellpadding="5" cellspacing="0">',
            "  <thead>",
            "    <tr>"
        ]
        
        # Add header columns
        for col in columns:
            html.append(f"      <th>{col}</th>")
        
        html.extend([
            "    </tr>",
            "  </thead>",
            "  <tbody>"
        ])
        
        # Add data rows
        for row in data:
            html.append("    <tr>")
            for col in columns:
                value = row.get(col, "")
                # Escape HTML characters
                escaped_value = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                html.append(f"      <td>{escaped_value}</td>")
            html.append("    </tr>")
        
        html.extend([
            "  </tbody>",
            "</table>"
        ])
        
        return "\n".join(html)
    
    @staticmethod
    def to_json(data: List[Dict[str, Any]]) -> str:
        """
        Convert table data to JSON format
        
        Args:
            data: Table data
            
        Returns:
            JSON formatted string
        """
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def auto_detect_format(file_extension: str) -> TableOutputFormat:
        """
        Auto-detect output format from file extension
        
        Args:
            file_extension: File extension (with or without dot)
            
        Returns:
            Detected output format
        """
        ext = file_extension.lower().lstrip(".")
        
        if ext == "md" or ext == "markdown":
            return TableOutputFormat.MARKDOWN
        elif ext == "csv":
            return TableOutputFormat.CSV
        elif ext == "html" or ext == "htm":
            return TableOutputFormat.HTML
        elif ext == "json":
            return TableOutputFormat.JSON
        else:
            return TableOutputFormat.JSON  # Default
    
    @staticmethod
    def save_table(
        data: List[Dict[str, Any]], 
        file_path: str, 
        output_format: TableOutputFormat = None,
        table_name: str = "table"
    ) -> None:
        """
        Save table data to file
        
        Args:
            data: Table data
            file_path: Output file path
            output_format: Output format (auto-detected if None)
            table_name: Table name
        """
        if output_format is None:
            # Auto-detect from file extension
            import os
            _, ext = os.path.splitext(file_path)
            output_format = TableFormatter.auto_detect_format(ext)
        
        # Format the data
        formatted_data = TableFormatter.format_table(data, output_format, table_name)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_data)
    
    @staticmethod
    def preview_table(data: List[Dict[str, Any]], max_rows: int = 5) -> str:
        """
        Generate a preview of the table in markdown format
        
        Args:
            data: Table data
            max_rows: Maximum number of rows to show
            
        Returns:
            Markdown preview
        """
        if not data:
            return "*No data available*"
        
        preview_data = data[:max_rows]
        preview = TableFormatter.to_markdown(preview_data, "Preview")
        
        if len(data) > max_rows:
            preview += f"\n\n*... and {len(data) - max_rows} more rows*"
        
        return preview


class TableTemplates:
    """
    Built-in table templates for common use cases
    """
    
    @staticmethod
    def get_user_profile_table(rows: int = 5) -> Dict[str, Any]:
        """
        Get user profile table template
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        from ..core.rule import Rule
        
        return {
            "name": "user_profiles",
            "table_name": "User Profiles",
            "rows_count": rows,
            "columns": [
                Rule(name="user_id").with_examples("USR001", "USR002", "USR003"),
                Rule(name="first_name").with_examples("John", "Jane", "Mike", "Sarah"),
                Rule(name="last_name").with_examples("Smith", "Doe", "Johnson", "Williams"),
                Rule(name="email").with_examples("john.smith@email.com", "jane.doe@email.com"),
                Rule(name="age").with_constraints(type="integer", min=18, max=80),
                Rule(name="city").with_examples("New York", "Los Angeles", "Chicago", "Houston"),
                Rule(name="country").with_examples("USA", "Canada", "UK", "Australia"),
            ]
        }
    
    @staticmethod
    def get_product_catalog_table(rows: int = 10) -> Dict[str, Any]:
        """
        Get product catalog table template
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        from ..core.rule import Rule
        
        return {
            "name": "product_catalog",
            "table_name": "Product Catalog",
            "rows_count": rows,
            "columns": [
                Rule(name="product_id").with_examples("PRD001", "PRD002", "PRD003"),
                Rule(name="product_name").with_examples("Laptop", "Mouse", "Keyboard", "Monitor"),
                Rule(name="category").with_examples("Electronics", "Office", "Gaming", "Accessories"),
                Rule(name="price").with_constraints(type="float", min=10.0, max=2000.0),
                Rule(name="brand").with_examples("Apple", "Dell", "HP", "Logitech", "Samsung"),
                Rule(name="stock_quantity").with_constraints(type="integer", min=0, max=1000),
                Rule(name="status").with_examples("Active", "Inactive", "Out of Stock"),
            ]
        }
    
    @staticmethod
    def get_sales_data_table(rows: int = 20) -> Dict[str, Any]:
        """
        Get sales data table template
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        from ..core.rule import Rule
        
        return {
            "name": "sales_data",
            "table_name": "Sales Data",
            "rows_count": rows,
            "columns": [
                Rule(name="order_id").with_examples("ORD001", "ORD002", "ORD003"),
                Rule(name="customer_id").with_examples("CUST001", "CUST002", "CUST003"),
                Rule(name="product_id").with_examples("PRD001", "PRD002", "PRD003"),
                Rule(name="quantity").with_constraints(type="integer", min=1, max=10),
                Rule(name="unit_price").with_constraints(type="float", min=5.0, max=500.0),
                Rule(name="sales_rep").with_examples("Alice Johnson", "Bob Smith", "Carol Davis"),
                Rule(name="region").with_examples("North", "South", "East", "West"),
                Rule(name="order_date").with_examples("2024-01-15", "2024-02-20", "2024-03-10"),
            ]
        }
    
    @staticmethod
    def get_employee_table(rows: int = 15) -> Dict[str, Any]:
        """
        Get employee table template
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        from ..core.rule import Rule
        
        return {
            "name": "employees",
            "table_name": "Employee Directory",
            "rows_count": rows,
            "columns": [
                Rule(name="employee_id").with_examples("EMP001", "EMP002", "EMP003"),
                Rule(name="first_name").with_examples("John", "Jane", "Mike", "Sarah"),
                Rule(name="last_name").with_examples("Smith", "Doe", "Johnson", "Williams"),
                Rule(name="department").with_examples("Engineering", "Marketing", "Sales", "HR"),
                Rule(name="position").with_examples("Developer", "Manager", "Analyst", "Director"),
                Rule(name="salary").with_constraints(type="integer", min=40000, max=150000),
                Rule(name="hire_date").with_examples("2020-01-15", "2021-06-01", "2022-03-10"),
                Rule(name="email").with_examples("john.smith@company.com", "jane.doe@company.com"),
            ]
        }
    
    @staticmethod
    def get_financial_data_table(rows: int = 12) -> Dict[str, Any]:
        """
        Get financial data table template
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        from ..core.rule import Rule
        
        return {
            "name": "financial_data",
            "table_name": "Financial Data",
            "rows_count": rows,
            "columns": [
                Rule(name="account_id").with_examples("ACC001", "ACC002", "ACC003"),
                Rule(name="account_type").with_examples("Checking", "Savings", "Credit", "Investment"),
                Rule(name="balance").with_constraints(type="float", min=0.0, max=100000.0),
                Rule(name="currency").with_examples("USD", "EUR", "GBP", "JPY"),
                Rule(name="status").with_examples("Active", "Inactive", "Frozen", "Closed"),
                Rule(name="branch").with_examples("Main Street", "Downtown", "Airport", "Mall"),
                Rule(name="last_transaction_date").with_examples("2024-01-15", "2024-02-20"),
            ]
        }
    
    @staticmethod
    def list_templates() -> List[str]:
        """
        List all available table templates
        
        Returns:
            List of template names
        """
        return [
            "user_profiles",
            "product_catalog", 
            "sales_data",
            "employees",
            "financial_data"
        ]
    
    @staticmethod
    def get_template(template_name: str, rows: int = 5) -> Dict[str, Any]:
        """
        Get template by name
        
        Args:
            template_name: Name of the template
            rows: Number of rows to generate
            
        Returns:
            Table template configuration
        """
        templates = {
            "user_profiles": TableTemplates.get_user_profile_table,
            "product_catalog": TableTemplates.get_product_catalog_table,
            "sales_data": TableTemplates.get_sales_data_table,
            "employees": TableTemplates.get_employee_table,
            "financial_data": TableTemplates.get_financial_data_table,
        }
        
        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}. Available: {list(templates.keys())}")
        
        return templates[template_name](rows) 