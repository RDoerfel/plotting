"""
Core figure and plotting classes for the plotting package.
"""

import warnings
from pathlib import Path
from typing import Tuple, Optional, Union, Any, Dict

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.figure
import seaborn as sns
import numpy as np

from ..config import PlottingConfig
from .. import FONTS_DIR, CM


class FontManager:
    """Manages custom font loading and registration."""

    _fonts_loaded = False
    _available_fonts = set()

    @classmethod
    def load_fonts(cls, font_dir: Optional[Path] = None) -> None:
        """
        Load custom fonts from the specified directory.

        Args:
            font_dir: Directory containing font files. If None, uses package default.
        """
        if cls._fonts_loaded:
            return

        if font_dir is None:
            font_dir = FONTS_DIR

        if not font_dir.exists():
            warnings.warn(f"Font directory {font_dir} not found. Using system fonts only.")
            cls._fonts_loaded = True
            return

        try:
            font_extensions = {".ttf", ".otf", ".woff", ".woff2"}
            font_files = [f for f in font_dir.iterdir() if f.suffix.lower() in font_extensions]

            if not font_files:
                warnings.warn(f"No font files found in {font_dir}")
                cls._fonts_loaded = True
                return

            for font_file in font_files:
                try:
                    mpl.font_manager.fontManager.addfont(str(font_file))
                    cls._available_fonts.add(font_file.stem)
                    print(f"Loaded font: {font_file.stem}")
                except Exception as e:
                    warnings.warn(f"Failed to load font {font_file}: {e}")

        except Exception as e:
            warnings.warn(f"Error loading fonts from {font_dir}: {e}")

        cls._fonts_loaded = True

    @classmethod
    def is_font_available(cls, font_name: str) -> bool:
        """Check if a font is available in the system or loaded."""
        if not cls._fonts_loaded:
            cls.load_fonts()

        # Check if font is in our loaded fonts
        if font_name in cls._available_fonts:
            return True

        # Check if font is available in system
        available_fonts = {f.name for f in mpl.font_manager.fontManager.ttflist}
        return font_name in available_fonts

    @classmethod
    def get_available_fonts(cls) -> set:
        """Get all available fonts (both system and custom)."""
        if not cls._fonts_loaded:
            cls.load_fonts()
        return cls._available_fonts


class Plotting:
    """
    Main class for creating publication-ready plots with custom styling.

    This class provides methods to configure matplotlib settings and create
    styled figures suitable for scientific publications.
    """

    def __init__(self, config: Optional[PlottingConfig] = None) -> None:
        """
        Initialize the plotting environment.

        Args:
            config: Configuration object. If None, uses default configuration.
        """
        self.config = config or PlottingConfig()
        FontManager.load_fonts()

    def set_rc_params(
        self,
        fontfamily: Optional[str] = None,
        small: Optional[int] = None,
        medium: Optional[int] = None,
        big: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Set matplotlib rcParams for consistent plot styling.

        Args:
            fontfamily: Font family name. If None, uses config default.
            small: Font size for small text (ticks, legend).
            medium: Font size for medium text (labels).
            big: Font size for large text (titles).
            **kwargs: Additional rcParams to set.
        """
        # Reset to defaults first
        mpl.rcParams.update(mpl.rcParamsDefault)

        # Use provided values or fall back to config
        fontfamily = fontfamily or self.config.default_font
        small = small or self.config.font_sizes["small"]
        medium = medium or self.config.font_sizes["medium"]
        big = big or self.config.font_sizes["big"]

        # Validate font availability
        if not FontManager.is_font_available(fontfamily):
            warnings.warn(f"Font '{fontfamily}' not available. Using default.")
            fontfamily = "DejaVu Sans"  # matplotlib default

        # Set font and size parameters
        rc_params = {
            "font.family": fontfamily,
            "font.size": medium,
            "axes.titlesize": big,
            "axes.labelsize": medium,
            "xtick.labelsize": small,
            "ytick.labelsize": small,
            "legend.fontsize": small,
            "savefig.dpi": self.config.dpi,
            "figure.dpi": self.config.dpi,
            "pdf.fonttype": 42,  # Embed fonts in PDF
            "ps.fonttype": 42,  # Embed fonts in PostScript
        }

        # Add any additional parameters
        rc_params.update(kwargs)

        # Apply parameters
        mpl.rcParams.update(rc_params)

    def create_figure(
        self,
        rows: int = 1,
        cols: int = 1,
        width: float = 10,
        height: float = 8,
        unit: str = "cm",
        sharex: bool = False,
        sharey: bool = False,
        **kwargs: Any,
    ) -> Tuple["Plot", Union[plt.Axes, np.ndarray]]:
        """
        Create a new figure with specified layout and styling.

        Args:
            rows: Number of subplot rows.
            cols: Number of subplot columns.
            width: Figure width.
            height: Figure height.
            unit: Unit for dimensions ('cm' or 'inch').
            sharex: Whether subplots share x-axis.
            sharey: Whether subplots share y-axis.
            **kwargs: Additional arguments passed to plt.subplots.

        Returns:
            Tuple of (Plot object, axes array or single axis).

        Raises:
            ValueError: If unit is not 'cm' or 'inch'.
        """
        if unit not in ("cm", "inch"):
            raise ValueError(f"Unit must be 'cm' or 'inch', got '{unit}'")

        # Convert dimensions
        if unit == "cm":
            figsize = (width / CM, height / CM)
        else:
            figsize = (width, height)

        # Create figure
        plot = Plot(figsize=figsize)

        # Create subplots
        if rows == 1 and cols == 1:
            axes = plot.add_subplot(1, 1, 1)
        else:
            axes = plot.subplots(nrows=rows, ncols=cols, sharex=sharex, sharey=sharey, **kwargs)

        return plot, axes


class Plot(matplotlib.figure.Figure):
    """
    Custom Figure class with publication-ready styling methods.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the plot figure."""
        super().__init__(*args, **kwargs)
        self._style_applied = False

    def apply_style(
        self,
        despine: bool = True,
        grid: bool = True,
        offset_left: float = 5,
        offset_bottom: float = 5,
        spine_width: float = 1.4,
        grid_color: str = "C7",
        grid_style: str = "--",
        grid_width: float = 0.8,
        **kwargs: Any,
    ) -> None:
        """
        Apply publication-ready styling to the figure.

        Args:
            despine: Whether to remove top and right spines.
            grid: Whether to show grid lines.
            offset_left: Left spine offset in points.
            offset_bottom: Bottom spine offset in points.
            spine_width: Width of axis spines.
            grid_color: Color of grid lines.
            grid_style: Style of grid lines.
            grid_width: Width of grid lines.
            **kwargs: Additional styling parameters.
        """
        if despine:
            sns.despine(
                fig=self,
                top=True,
                right=True,
                left=False,
                bottom=False,
                offset={"left": offset_left, "bottom": offset_bottom},
            )

        for ax in self.axes:
            if grid:
                ax.grid(axis="y", color=grid_color, linestyle=grid_style, linewidth=grid_width, alpha=0.7)

            # Style ticks
            ax.tick_params(which="major", direction="out", length=3, width=spine_width, bottom=True, left=True)
            ax.tick_params(which="minor", direction="out", length=2, width=spine_width / 2, bottom=True, left=True)

            # Style spines
            for spine in ax.spines.values():
                spine.set_linewidth(spine_width)

        self.tight_layout()
        self._style_applied = True

    def save(
        self, filename: Union[str, Path], path: Optional[Path] = None, ensure_style: bool = True, **kwargs: Any
    ) -> None:
        """
        Save the figure to file.

        Args:
            filename: Name of the output file.
            path: Directory to save the file. If None, uses current directory.
            ensure_style: Whether to apply default style if not already applied.
            **kwargs: Additional arguments passed to savefig.
        """
        if ensure_style and not self._style_applied:
            self.apply_style()

        if path is None:
            path = Path.cwd()

        # Ensure path is a Path object
        if isinstance(path, str):
            path = Path(path)

        # Create directory if it doesn't exist
        path.mkdir(parents=True, exist_ok=True)

        # Default save parameters
        save_params = {"bbox_inches": "tight", "dpi": 300, "facecolor": "white", "edgecolor": "none"}
        save_params.update(kwargs)

        # Save figure
        full_path = path / filename
        self.savefig(full_path, **save_params)
        print(f"Figure saved to: {full_path}")

    def show_style_preview(self) -> None:
        """Display a preview of the current styling."""
        if not self.axes:
            print("No axes to preview. Create subplots first.")
            return

        # Apply temporary styling for preview
        temp_applied = self._style_applied
        if not temp_applied:
            self.apply_style()

        # Show the figure
        plt.show()

        # Reset style flag if it wasn't applied before
        if not temp_applied:
            self._style_applied = False
