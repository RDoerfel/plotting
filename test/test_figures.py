# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:00:00 2021
Unit tests for the Plotting class.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plotting import figures


def test_get_figures():
    """Test the get_figures method."""
    fig, axs = figures.get_figures(rows=2, cols=1, unit="cm", figwidth=10, figheight=15, sharex=True, sharey=True)
    assert fig is not None
    assert len(axs) == 2
    assert axs[0].get_xlabel() == ""
    assert axs[1].get_xlabel() == ""


def test_set_style():
    """Test the set_style method."""
    fig, axs = figures.get_figures(rows=1, cols=1, unit="cm", figwidth=10, figheight=5)
    fig = figures.set_style(fig, offleft=5, offbottom=5, spinewidth=1.4, gridlinewidth=0.8)
    assert fig is not None
    for ax in fig.axes:
        assert ax.spines["left"].get_linewidth() == 1.4
        assert ax.spines["bottom"].get_linewidth() == 1.4


def test_save_fig(tmp_path):
    """Test the save_fig method."""
    fig, axs = figures.get_figures(rows=1, cols=1, unit="cm", figwidth=10, figheight=5)
    filename = tmp_path / "test_plot.png"
    figures.save_fig(fig, filename, dpi=300, bbox_inches="tight", pad_inches=0.1)
    assert filename.exists()
    assert filename.stat().st_size > 0  # Check if file is not empty
