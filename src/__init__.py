"""
Plotting: A high-level interface for creating publication-ready plots.

This package provides a simplified interface to matplotlib and seaborn
for creating publication-quality scientific figures with consistent styling.
"""

from pathlib import Path
from .core.figures import Plotting, Plot
from .core.config import PlottingConfig

__version__ = "0.1.0"
__author__ = "Ruben Doerfel"
__email__ = "doerfelruben@aol.com"

__all__ = ["Plotting", "Plot", "PlottingConfig", "PACKAGE_DIR", "FONTS_DIR", "CM"]

# Package directories
PACKAGE_DIR = Path(__file__).parent
FONTS_DIR = PACKAGE_DIR / "fonts"

# Constants
CM = 2.54  # centimeters to inches conversion factor

# Initialize default configuration
_default_config = PlottingConfig()


def get_version():
    """Return the package version."""
    return __version__


def get_fonts_dir():
    """Return the path to the fonts directory."""
    return FONTS_DIR


def list_available_fonts():
    """List all available custom fonts in the package."""
    if not FONTS_DIR.exists():
        return []

    font_extensions = {".ttf", ".otf", ".woff", ".woff2"}
    fonts = []

    for font_file in FONTS_DIR.iterdir():
        if font_file.suffix.lower() in font_extensions:
            fonts.append(font_file.stem)

    return sorted(fonts)
