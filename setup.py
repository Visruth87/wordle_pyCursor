"""
Setup script for the Wordle game.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wordle-game",
    version="1.0.0",
    author="Wordle Game Developer",
    author_email="developer@example.com",
    description="A Python implementation of the popular Wordle word guessing game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wordle-game",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "wordle=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "wordle": ["data/*.txt"],
    },
    keywords="wordle, game, word, puzzle, terminal",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/wordle-game/issues",
        "Source": "https://github.com/yourusername/wordle-game",
        "Documentation": "https://github.com/yourusername/wordle-game#readme",
    },
) 