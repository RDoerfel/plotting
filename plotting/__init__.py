"""
Plotting: A high-level interface for creating publication-ready plots.

This package provides a simplified interface to matplotlib and seaborn
for creating publication-quality scientific figures with consistent styling.
"""

__version__ = "0.1.0"
__author__ = "Ruben Doerfel"

from .figures import (
    set_rc_params,
    get_figures,
)

# Constants
CM = 2.54  # centimeters to inches conversion factor

# set public functions
__all__ = [
    "set_rc_params",
    "get_figures",
]
