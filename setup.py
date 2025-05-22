from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


# Read version from package
def get_version():
    version_file = this_directory / "plotting" / "__init__.py"
    for line in version_file.read_text().splitlines():
        if line.startswith("__version__"):
            return line.split('"')[1]
    return "0.1.0"


setup(
    name="plotting",
    version=get_version(),
    author="Ruben Doerfel",
    author_email="doerfelruben@aol.com",
    description="High-level interface for creating publication-ready plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RDoerfel/plotting",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="matplotlib seaborn plotting visualization publication scientific",
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.3.4",
        "seaborn>=0.11.1",
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.8",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    package_data={
        "plotting": ["fonts/*"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            # Add CLI tools if needed in future
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/RDoerfel/plotting/issues",
        "Source": "https://github.com/RDoerfel/plotting",
        "Documentation": "https://github.com/RDoerfel/plotting#readme",
    },
)
