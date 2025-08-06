#!/usr/bin/env python3
"""
ShadowAI Test Runner Script

Provides convenient test running interface with support for multiple test modes.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run command and display results"""
    print(f"\n🔧 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, check=True, cwd=Path(__file__).parent)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed (exit code: {e.returncode})")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="ShadowAI Test Runner")
    parser.add_argument(
        "--mode",
        choices=["all", "unit", "integration", "coverage", "specific"],
        default="all",
        help="Test mode",
    )
    parser.add_argument("--file", help="Specify test file (used when mode=specific)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")

    args = parser.parse_args()

    print("🧪 ShadowAI Test Runner")
    print("=" * 50)

    # Base pytest command
    base_cmd = ["pytest"]
    if args.verbose:
        base_cmd.append("-v")

    success = True

    if args.mode == "all":
        # Run all tests
        cmd = base_cmd + ["."]
        success = run_command(cmd, "Run all tests")

    elif args.mode == "unit":
        # Run unit tests only
        cmd = base_cmd + ["-m", "unit", "."]
        success = run_command(cmd, "Run unit tests")

    elif args.mode == "integration":
        # Run integration tests only
        cmd = base_cmd + ["-m", "integration", "."]
        success = run_command(cmd, "Run integration tests")

    elif args.mode == "specific":
        # Run specific file
        if not args.file:
            print("❌ Please specify the test file to run (--file)")
            sys.exit(1)

        cmd = base_cmd + [args.file]
        success = run_command(cmd, f"Run test file: {args.file}")

    elif args.mode == "coverage":
        # Generate coverage report
        cmd = base_cmd + [
            "--cov=shadowai",
            "--cov-report=html",
            "--cov-report=term-missing",
            ".",
        ]
        success = run_command(cmd, "Run tests and generate coverage report")

        if success:
            print("\n📊 Coverage report generated:")
            print("   - HTML report: htmlcov/index.html")
            print("   - Terminal report displayed above")

    # If coverage option is specified, run additional coverage
    if args.coverage and args.mode != "coverage":
        print("\n" + "=" * 50)
        cmd = base_cmd + ["--cov=shadowai", "--cov-report=term-missing", "."]
        run_command(cmd, "Generate coverage report")

    # Display results
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tests completed! All tests passed")
        sys.exit(0)
    else:
        print("💥 Tests failed! Please check error messages above")
        sys.exit(1)


def show_help():
    """Display help information"""
    print(
        """
🧪 ShadowAI Test Runner Usage Guide

Basic usage:
  python run_tests.py                    # Run all tests
  python run_tests.py --mode unit        # Run unit tests only
  python run_tests.py --mode integration # Run integration tests only
  python run_tests.py --mode coverage    # Run tests and generate coverage
  python run_tests.py --mode specific --file test_rule.py  # Run specific file

Options:
  --mode     Test mode (all, unit, integration, coverage, specific)
  --file     Specify test file (used with specific mode)
  --verbose  Display verbose output
  --coverage Generate coverage report

Examples:
  python run_tests.py --verbose                 # Run all tests in verbose mode
  python run_tests.py --mode unit --coverage    # Run unit tests and generate coverage
  python run_tests.py --mode specific --file test_shadowai.py  # Run ShadowAI tests only
"""
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
    else:
        main()
