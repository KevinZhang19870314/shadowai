#!/usr/bin/env python3
"""
Simple test script for MockAI
"""

# Add project root directory to path
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from mock_ai import MockAI


def main():
    print("🚀 MockAI Basic Usage Example")

    # Initialize MockAI instance
    mock_ai = MockAI()

    result = mock_ai.generate("email", format_output=False)
    print(f"Generated email: {result}")


if __name__ == "__main__":
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        main()
    except Exception as e:
        print(f"❌ Execution error: {e}")
