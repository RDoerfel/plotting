# %%

import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Literal, Tuple, Optional
from .constants import CM2INCH


def set_rc_params(fontfamily: Optional[str] = None, small: int = 8, medium: int = 10, big: int = 12) -> None:
    """Set rc parameters for plots.

    Args:
        fontfamily: Font family (e.g., 'serif', 'sans-serif', 'monospace')
        small: Font size for small text (ticks, legend)
        medium: Font size for medium text (labels, default)
        big: Font size for big text (titles)

    Raises:
        ValueError: If font sizes are not positive integers
    """
    if not all(isinstance(size, int) and size > 0 for size in [small, medium, big]):
        raise ValueError("Font sizes must be positive integers")

    # Reset to defaults first
    mpl.rcParams.update(mpl.rcParamsDefault)

    if fontfamily is not None:
        plt.rc("font", family=fontfamily)

    plt.rc("font", size=medium)
    plt.rc("axes", titlesize=big)
    plt.rc("axes", labelsize=medium)
    plt.rc("xtick", labelsize=small)
    plt.rc("ytick", labelsize=small)
    plt.rc("legend", fontsize=small)
    plt.rc("savefig", dpi=300)
    plt.rc("pdf", fonttype=42)  # Embed fonts properly
    plt.rc("ps", fonttype=42)


def _set_spine_style(fig: plt.Figure, offleft: float = 5, offbottom: float = 5, spinewidth: float = 1.4) -> plt.Figure:
    """Set spine style for all axes in figure."""
    for ax in fig.axes:
        # Remove top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Position remaining spines
        ax.spines["left"].set_position(("outward", offleft))
        ax.spines["bottom"].set_position(("outward", offbottom))

        # Set spine width
        for spine in ax.spines.values():
            spine.set_linewidth(spinewidth)

    return fig


def _set_grid_style(fig: plt.Figure, gridlinewidth: float = 0.8) -> plt.Figure:
    """Set grid style for all axes in figure."""
    for ax in fig.axes:
        ax.grid(which="major", axis="y", color="lightgray", linestyle="--", linewidth=gridlinewidth, zorder=0)
    return fig


def _set_tick_style(fig: plt.Figure, spinewidth: float = 1.4) -> plt.Figure:
    """Set tick style for all axes in figure."""
    for ax in fig.axes:
        ax.tick_params(which="major", direction="out", length=3, width=spinewidth, bottom=True, left=True)
        ax.tick_params(which="minor", direction="out", length=2, width=spinewidth / 2, bottom=True, left=True)
    return fig


def _set_style(
    fig: plt.Figure,
    offleft: float = 5,
    offbottom: float = 5,
    spinewidth: float = 1.4,
    gridlinewidth: float = 0.8,
    tight_layout: bool = True,
) -> plt.Figure:
    """Set publication-ready style for plots.

    Args:
        fig: Figure object to style
        offleft: Left spine offset in points
        offbottom: Bottom spine offset in points
        spinewidth: Width of spines in points
        gridlinewidth: Width of grid lines in points
        tight_layout: Whether to apply tight_layout

    Returns:
        Styled figure object
    """
    fig = _set_spine_style(fig, offleft=offleft, offbottom=offbottom, spinewidth=spinewidth)
    fig = _set_grid_style(fig, gridlinewidth=gridlinewidth)
    fig = _set_tick_style(fig, spinewidth=spinewidth)

    if tight_layout:
        fig.tight_layout()

    return fig


def get_figures(
    rows: int,
    cols: int,
    unit: Literal["cm", "inch"] = "cm",
    figwidth: float = 10,
    figheight: float = 8,
    sharex: bool = False,
    sharey: bool = False,
    **subplot_kw,
) -> Tuple[plt.Figure, plt.Axes]:
    """Create figure and axes with publication-ready styling.

    Args:
        rows: Number of subplot rows
        cols: Number of subplot columns
        unit: Unit for figure dimensions ("cm" or "inch")
        figwidth: Figure width in specified units
        figheight: Figure height in specified units
        sharex: Share x-axis across subplots
        sharey: Share y-axis across subplots
        **subplot_kw: Additional arguments passed to plt.subplots()

    Returns:
        Tuple of (figure, axes) objects

    Raises:
        ValueError: If dimensions or layout parameters are invalid
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Rows and columns must be positive")
    if figwidth <= 0 or figheight <= 0:
        raise ValueError("Figure dimensions must be positive")
    if unit == "cm":
        figsize = (figwidth / CM2INCH, figheight / CM2INCH)
    elif unit == "inch":
        figsize = (figwidth, figheight)
    else:
        raise ValueError(f"unit {unit} not supported")
    plt.ioff()  # Turn interactive mode off to prevent automatic plotting
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=figsize, sharex=sharex, sharey=sharey, **subplot_kw)
    fig = _set_style(fig)
    return fig, axes


# %%
