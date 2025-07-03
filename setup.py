# This file defines the pip-installable CLI package with both runeseal and rs entry points:

from setuptools import find_packages, setup

setup(
    name="runeseal",
    version="1.0.0",
    description="RuneSeal CLI: Secure, headless secrets vault client.",
    author="Orrin",
    author_email="orrin@example.com",  # Replace with yours
    url="https://github.com/YOUR_GITHUB/runeseal",  # Set correct URL
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "runeseal=runeseal.__main__:app",
            "rs=runeseal.__main__:app",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

# Once this is in place, run this from your project root to install globally (during dev or for users with Python):
# pip install .
# And voilà—you’ll be able to invoke runeseal or rs from anywhere on your system.
