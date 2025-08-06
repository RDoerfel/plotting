# %%

import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Tuple
from plotting import CM


def set_rc_params(fontfamily: str = None, small=8, medium=10, big=12) -> None:
    """set rc parameters for plots
    args:
        fontfamily: font family
        small: fontsize for small text
        medium: fontsize for medium text
        big: fontsize for big text
    """
    mpl.rcParams.update()
    if fontfamily is not None:
        plt.rc("font", family=fontfamily)
    plt.rc("font", size=medium)  # controls default text sizes
    plt.rc("axes", titlesize=big)  # fontsize of the axes title
    plt.rc("axes", labelsize=medium)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=small)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=small)  # fontsize of the tick labels
    plt.rc("legend", fontsize=small)  # legend fontsize
    plt.rc("savefig", dpi=300)  # figure resolution
    plt.rc("pdf", fonttype=42)
    plt.rc("ps", fonttype=42)


def _set_spine_style(fig: plt.Figure, offleft: float = 5, offbottom: float = 5, spinewidth: float = 1.4) -> plt.Figure:
    """set spine style for axes
    args:
        ax: axes object
        offleft: offset left
        offbottom: offset bottom
        spinewidth: width of spines
    returns: figure object"""
    for ax in fig.axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_position(("outward", offleft))
        ax.spines["bottom"].set_position(("outward", offbottom))
        plt.setp(ax.spines.values(), linewidth=spinewidth)
    return fig


def _set_grid_style(fig: plt.Figure, gridlinewidth: float = 0.8) -> plt.Figure:
    """set grid style for axes
    args:
        fig: figure object
        gridlinewidth: width of grid lines
    returns: figure object"""
    for ax in fig.axes:
        ax.grid(which="major", axis="y", color="C7", linestyle="--", lw=gridlinewidth, zorder=0)
    return fig


def _set_tick_style(fig: plt.Figure, spinewidth: float = 1.4) -> plt.Figure:
    """set tick style for axes
    args:
        fig: figure object
        spinewidth: width of spines
    returns: figure object"""
    for ax in fig.axes:
        ax.tick_params(which="major", direction="out", length=3, width=spinewidth, bottom=True, left=True)
        ax.tick_params(which="minor", direction="out", length=2, width=spinewidth / 2, bottom=True, left=True)
        plt.setp(ax.spines.values(), linewidth=spinewidth)
    return fig


def set_style(
    fig: plt.Figure, offleft: float = 5, offbottom: float = 5, spinewidth: float = 1.4, gridlinewidth: float = 0.8
) -> plt.Figure:
    """set style for plots (despine, grid, ticks)
    args:
        offleft: offset left
        offbottom: offset bottom
        spinewidth: width of spines
    """
    fig = _set_spine_style(fig, offleft=offleft, offbottom=offbottom, spinewidth=spinewidth)
    fig = _set_grid_style(fig, gridlinewidth=gridlinewidth)
    fig = _set_tick_style(fig, spinewidth=spinewidth)
    fig.tight_layout()
    return fig


def get_figures(
    rows: int, cols: int, unit: str, figwidth: float, figheight: float, sharex=True, sharey=True
) -> plt.Figure:
    """Get figure and axes object
    args:
        rows: number of rows
        cols: number of columns
        unit: unit of figure size (cm or inch)
        figwidth: figure width
        figheight: figure height
        sharex: share x axis
    returns: figure object, axes object"""
    if unit == "cm":
        figsize = (figwidth / CM, figheight / CM)
    elif unit == "inch":
        figsize = (figwidth, figheight)
    else:
        raise ValueError(f"unit {unit} not supported")
    plt.ioff()  # Turn interactive mode off to prevent automatic plotting
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=figsize, sharex=sharex, sharey=sharey)
    fig = set_style(fig)
    return fig, axes


# %%
