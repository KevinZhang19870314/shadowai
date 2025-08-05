#!/usr/bin/env python3
"""
ShadowAI PyPI Publishing Script

Automates the build, test, and publish process to PyPI.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def run_command(command, check=True, capture_output=False):
    """Run command and handle results"""
    print(f"🔄 Running command: {command}")

    try:
        if capture_output:
            result = subprocess.run(
                command, shell=True, check=check, capture_output=True, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=check)
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command execution failed: {e}")
        if capture_output and e.stdout:
            print(f"Output: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Error: {e.stderr}")
        return None


def get_current_version():
    """Get current version number"""
    try:
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
        else:
            print("❌ Could not find version number in pyproject.toml")
            return None
    except FileNotFoundError:
        print("❌ pyproject.toml file not found")
        return None


def update_version(new_version):
    """Update version number"""
    try:
        # Update pyproject.toml
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

        with open("pyproject.toml", "w", encoding="utf-8") as f:
            f.write(content)

        # Update __init__.py
        init_file = "lib/mock_ai/__init__.py"
        if os.path.exists(init_file):
            with open(init_file, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(
                r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', content
            )

            with open(init_file, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✅ Version updated to: {new_version}")
        return True

    except Exception as e:
        print(f"❌ Failed to update version: {e}")
        return False


def clean_build():
    """Clean build files"""
    print("🧹 Cleaning build files...")

    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        run_command(f"rm -rf {dir_pattern}", check=False)

    print("✅ Build files cleaned")


def check_code_quality():
    """Check code quality"""
    print("🔍 Checking code quality...")

    # Format code
    print("📝 Formatting code...")
    run_command("black lib/ example/ scripts/")
    run_command("isort lib/ example/ scripts/")

    # Check code style
    print("🎯 Checking code style...")
    run_command("flake8 lib/ --max-line-length=100 --ignore=E203,W503")

    # Type checking
    print("🔬 Type checking...")
    run_command("mypy lib/ --ignore-missing-imports", check=False)

    print("✅ Code quality check completed")


def run_tests():
    """Run tests"""
    print("🧪 Running tests...")

    # Check if tests exist
    if os.path.exists("tests"):
        run_command("python -m pytest tests/ -v")
    elif os.path.exists("example/test"):
        run_command("python -m pytest example/test/ -v")
    else:
        print("⚠️ No test files found, skipping tests")

    print("✅ Tests completed")


def build_package():
    """Build package"""
    print("📦 Building package...")

    # Clean previous builds
    clean_build()

    # Build package
    run_command("python -m build")

    print("✅ Package built successfully")


def check_package():
    """Check package"""
    print("🔎 Checking package...")

    # Check with twine
    run_command("twine check dist/*")

    print("✅ Package check completed")


def publish_to_testpypi():
    """Publish to Test PyPI"""
    print("🚀 Publishing to Test PyPI...")

    run_command("twine upload --repository testpypi dist/*")

    print("✅ Published to Test PyPI successfully")


def publish_to_pypi():
    """Publish to PyPI"""
    print("🚀 Publishing to PyPI...")

    # Confirm publication
    response = input("⚠️ Are you sure you want to publish to PyPI? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Publication cancelled")
        return False

    run_command("twine upload dist/*")

    print("✅ Published to PyPI successfully")
    return True


def validate_dependencies():
    """Validate dependencies"""
    print("📋 Validating dependencies...")

    # Check Python modules that can be run with -m
    required_modules = {"build": ["python", "-m", "build", "--help"]}
    # Check regular command-line tools
    required_tools = ["twine", "black", "isort", "flake8"]
    missing_tools = []

    # Check modules first
    for module, cmd in required_modules.items():
        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(module)

    # Check regular tools
    for tool in required_tools:
        try:
            subprocess.run([tool, "--help"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)

    if missing_tools:
        print(f"❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install: pip install build twine black isort flake8")
        return False

    print("✅ All dependencies validated")
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="ShadowAI PyPI Publishing Script")
    parser.add_argument("--version", required=True, help="Version number to publish")
    parser.add_argument("--test", action="store_true", help="Publish to Test PyPI only")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument(
        "--skip-quality", action="store_true", help="Skip code quality checks"
    )

    args = parser.parse_args()

    print("🎉 Starting ShadowAI publication process")
    print(f"📝 Target version: {args.version}")
    print(f"🎯 Target: {'Test PyPI' if args.test else 'PyPI'}")

    # Validate dependencies
    if not validate_dependencies():
        sys.exit(1)

    # Get current version
    current_version = get_current_version()
    if current_version:
        print(f"📋 Current version: {current_version}")

    # Update version
    if not update_version(args.version):
        sys.exit(1)

    # Check code quality
    if not args.skip_quality:
        try:
            check_code_quality()
        except Exception as e:
            print(f"❌ Code quality check failed: {e}")
            sys.exit(1)

    # Run tests
    if not args.skip_tests:
        try:
            run_tests()
        except Exception as e:
            print(f"❌ Tests failed: {e}")
            sys.exit(1)

    # Build package
    try:
        build_package()
        check_package()
    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

    # Publish
    try:
        if args.test:
            publish_to_testpypi()
        else:
            if not publish_to_pypi():
                sys.exit(1)
    except Exception as e:
        print(f"❌ Publication failed: {e}")
        sys.exit(1)

    print("🎉 Publication process completed successfully!")

    # Show next steps
    if args.test:
        print("\n📋 Next steps:")
        print(
            f"1. Test installation: pip install -i https://test.pypi.org/simple/ mock-ai=={args.version}"
        )
        print("2. Test functionality")
        print("3. If everything works, run without --test flag")


if __name__ == "__main__":
    main()
