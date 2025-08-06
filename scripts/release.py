#!/usr/bin/env python3
"""
Release script for ShadowAI

This script helps automate the release process by:
1. Updating version in pyproject.toml
2. Creating git tag
3. Pushing to GitHub (which triggers the release workflow)
"""

import re
import subprocess
import sys
from pathlib import Path


def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def update_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    # Update version
    content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

    pyproject_path.write_text(content)
    print(f"✅ Updated version to {new_version} in pyproject.toml")


def run_command(cmd, check=True):
    """Run shell command"""
    print(f"🔄 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        sys.exit(1)

    return result


def create_and_push_tag(version):
    """Create git tag and push to GitHub"""
    tag_name = f"v{version}"

    # Add and commit changes
    run_command("git add pyproject.toml")
    run_command(f'git commit -m "Bump version to {version}"')

    # Create tag
    run_command(f'git tag -a {tag_name} -m "Release {tag_name}"')

    # Push changes and tag
    run_command("git push origin main")
    run_command(f"git push origin {tag_name}")

    print(f"✅ Created and pushed tag: {tag_name}")
    print(f"🚀 Release workflow will be triggered automatically!")
    print(f"📦 Check: https://github.com/KevinZhang19870314/shadowai/actions")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/release.py <new_version>")
        print("Example: python scripts/release.py 0.1.3")
        sys.exit(1)

    new_version = sys.argv[1]
    current_version = get_current_version()

    print(f"📦 ShadowAI Release Script")
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")

    # Validate version format
    if not re.match(r"^\d+\.\d+\.\d+(-\w+)?$", new_version):
        print("❌ Invalid version format. Use: x.y.z or x.y.z-suffix")
        sys.exit(1)

    # Check git status
    result = run_command("git status --porcelain", check=False)
    if result.stdout.strip():
        print("❌ Working directory is not clean. Please commit changes first.")
        sys.exit(1)

    # Update version
    update_version(new_version)

    # Create and push tag
    create_and_push_tag(new_version)

    print(f"🎉 Release {new_version} initiated successfully!")


if __name__ == "__main__":
    main()
