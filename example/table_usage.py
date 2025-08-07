#!/usr/bin/env python3
"""
ShadowAI Table Generation Examples

This script demonstrates how to use ShadowAI's table generation capabilities.
"""

import os
import sys

from dotenv import load_dotenv

# Add the lib directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from shadow_ai import ShadowAI, TableRule, TableOutputFormat, Rule, TableTemplates

load_dotenv()

def main():
    """Main demonstration function"""
    # Initialize ShadowAI
    print("🚀 ShadowAI Table Generation Demo")
    print("=" * 50)
    
    # Note: You need to set your OpenAI API key
    # You can do this by setting the OPENAI_API_KEY environment variable
    # or passing it directly: ai = ShadowAI(api_key="your-api-key-here")
    ai = ShadowAI()
    
    print("\n1. 📋 List Available Table Templates")
    print("-" * 30)
    templates = ai.list_table_templates()
    for template in templates:
        print(f"  • {template}")
    
    print("\n2. 🔍 Preview a Template")
    print("-" * 30)
    try:
        preview = ai.preview_table_template("user_profiles", rows=3)
        print(preview)
    except Exception as e:
        print(f"Note: API call needed for preview: {e}")
    
    print("\n3. ⚡ Quick Table Generation")
    print("-" * 30)
    try:
        # Generate a simple table
        table = ai.quick_table(
            "products", 
            "id", "name", "price", "category",
            rows=5,
            output_format=TableOutputFormat.MARKDOWN
        )
        print("Generated Products Table:")
        print(table)
    except Exception as e:
        print(f"Note: API call needed for generation: {e}")
    
    print("\n4. 🏗️ Custom Table Rule")
    print("-" * 30)
    # Create a custom table rule
    custom_table = TableRule.create(
        name="custom_users",
        table_name="Custom User Directory",
        columns=[
            Rule(name="username").with_examples("alice123", "bob_smith", "charlie.doe"),
            Rule(name="age").with_constraints(type="integer", min=18, max=65),
            Rule(name="role").with_examples("admin", "user", "moderator"),
            Rule(name="email").with_examples("user@domain.com", "person@company.org"),
        ],
        rows_count=7,
        output_format=TableOutputFormat.CSV
    )
    
    print("Custom Table Rule Created:")
    print(f"  Name: {custom_table.name}")
    print(f"  Columns: {custom_table.get_column_names()}")
    print(f"  Rows: {custom_table.rows_count}")
    print(f"  Format: {custom_table.output_format}")
    
    try:
        # Generate using custom table rule
        csv_table = ai.generate_table(custom_table, TableOutputFormat.CSV)
        print("\nGenerated CSV Table:")
        print(csv_table)
    except Exception as e:
        print(f"Note: API call needed for generation: {e}")
    
    print("\n5. 📊 Built-in Template Usage")
    print("-" * 30)
    try:
        # Generate from built-in template
        employee_table = ai.generate_table_from_template(
            "employees", 
            rows=4,
            output_format=TableOutputFormat.MARKDOWN
        )
        print("Employee Table from Template:")
        print(employee_table)
    except Exception as e:
        print(f"Note: API call needed for generation: {e}")
    
    print("\n6. 💾 Save to File")
    print("-" * 30)
    try:
        # Generate and save to different formats
        output_dir = "generated_tables"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as markdown
        ai.generate_table_from_template(
            "product_catalog",
            rows=10,
            output_format=TableOutputFormat.MARKDOWN,
            save_to_file=os.path.join(output_dir, "products.md")
        )
        
        # Save as CSV
        ai.generate_table_from_template(
            "sales_data",
            rows=15,
            output_format=TableOutputFormat.CSV,
            save_to_file=os.path.join(output_dir, "sales.csv")
        )
        
        # Save as HTML
        ai.generate_table_from_template(
            "financial_data",
            rows=8,
            output_format=TableOutputFormat.HTML,
            save_to_file=os.path.join(output_dir, "financial.html")
        )
        
        print(f"Tables saved to '{output_dir}' directory:")
        print("  • products.md (Markdown)")
        print("  • sales.csv (CSV)")
        print("  • financial.html (HTML)")
        
    except Exception as e:
        print(f"Note: API call needed for file generation: {e}")
    
    print("\n7. 🎨 Different Output Formats")
    print("-" * 30)
    
    # Show format examples (without API calls)
    sample_data = [
        {"id": 1, "name": "John Doe", "age": 30, "city": "New York"},
        {"id": 2, "name": "Jane Smith", "age": 25, "city": "Los Angeles"},
        {"id": 3, "name": "Bob Johnson", "age": 35, "city": "Chicago"}
    ]
    
    from shadow_ai import TableFormatter
    
    print("Sample data in different formats:")
    print("\n📝 Markdown:")
    print(TableFormatter.to_markdown(sample_data, "Sample Users"))
    
    print("\n📊 CSV:")
    print(TableFormatter.to_csv(sample_data))
    
    print("\n🌐 HTML:")
    html_output = TableFormatter.to_html(sample_data, "Sample Users")
    # Show first few lines of HTML
    html_lines = html_output.split('\n')
    for line in html_lines[:10]:
        print(line)
    if len(html_lines) > 10:
        print("... (truncated)")
    
    print("\n🔧 Configuration Example")
    print("-" * 30)
    
    # Example of using dictionary configuration
    table_config = {
        "name": "survey_responses",
        "table_name": "Customer Survey",
        "rows_count": 6,
        "columns": [
            {
                "name": "response_id",
                "description": "Unique response identifier",
                "examples": ["RESP001", "RESP002", "RESP003"],
                "rule_type": "record"
            },
            {
                "name": "satisfaction_score",
                "description": "Customer satisfaction rating",
                "constraints": {"type": "integer", "min": 1, "max": 10},
                "rule_type": "record"
            },
            {
                "name": "feedback",
                "description": "Customer feedback text",
                "examples": [
                    "Great service!",
                    "Could be better",
                    "Excellent experience",
                    "Average quality"
                ],
                "rule_type": "record"
            }
        ]
    }
    
    print("Configuration dictionary for survey table:")
    import json
    print(json.dumps(table_config, indent=2))
    
    try:
        # Use the configuration
        survey_table = ai.generate_table(
            table_config,
            TableOutputFormat.MARKDOWN
        )
        print("\nGenerated Survey Table:")
        print(survey_table)
    except Exception as e:
        print(f"Note: API call needed for generation: {e}")
    
    print("\n✅ Demo Complete!")
    print("\nTo run actual generation, make sure to:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Install required dependencies: pip install agno openai pydantic")
    print("3. Run this script again")


if __name__ == "__main__":
    main() 