from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-blender",
    version="0.1.0",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "blender-cli=cli_anything.blender.blender_cli:cli",
        ],
    },
    python_requires=">=3.10",
    description="AI-friendly CLI interface for Blender",
)
