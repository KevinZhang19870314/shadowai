#!/usr/bin/env python3
"""
Quick formatting fix script for ShadowAI

This script automatically fixes most formatting issues that cause CI failures.
"""

import subprocess
import sys


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"⚠️ {description} had issues:")
            print(f"   {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    print("🚀 ShadowAI Auto-Formatter")
    print("=" * 50)
    
    commands = [
        ("black .", "Code formatting with Black"),
        ("isort .", "Import sorting with isort"),
    ]
    
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ {success_count}/{len(commands)} formatting tasks completed")
    
    # Check results
    print("\n🔍 Checking results...")
    check_commands = [
        ("black --check .", "Black formatting check"),
        ("isort --check-only .", "isort import order check"),
        ("flake8 . --statistics", "Flake8 style check"),
    ]
    
    all_passed = True
    for cmd, desc in check_commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {desc} passed")
        else:
            print(f"⚠️ {desc} still has issues:")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All formatting checks passed! CI should now succeed.")
    else:
        print("\n📝 Some issues remain. Check the output above for details.")
        print("   Most remaining issues are likely in example/ files, which are now non-blocking in CI.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main()) 