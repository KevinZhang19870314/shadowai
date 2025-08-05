"""
ShadowAI setup.py for development installation
"""
from setuptools import setup, find_packages

setup(
    name="shadowai",
    version="0.1.0",
    package_dir={"": "lib"},
    packages=find_packages(where="lib"),
    install_requires=[
        "agno>=1.7.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "typing-extensions>=4.0.0",
    ],
) 