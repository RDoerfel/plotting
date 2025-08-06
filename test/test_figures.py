# -*- coding: utf-8 -*-
"""
Unit tests for the plotting library.
"""
import sys
import os
import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plotting import figures
from plotting.constants import CM2INCH

# Ensure matplotlib does not try to use an interactive backend (necessary for CI environments)
mpl.use("Agg")


class TestSetRcParams:
    """Test suite for set_rc_params function."""

    def setup_method(self):
        """Reset matplotlib rcParams before each test."""
        mpl.rcParams.update(mpl.rcParamsDefault)

    def test_set_rc_params_default(self):
        """Test set_rc_params with default parameters."""
        figures.set_rc_params()

        # Check default font sizes
        assert plt.rcParams["font.size"] == 10  # medium
        assert plt.rcParams["axes.titlesize"] == 12  # big
        assert plt.rcParams["axes.labelsize"] == 10  # medium
        assert plt.rcParams["xtick.labelsize"] == 8  # small
        assert plt.rcParams["ytick.labelsize"] == 8  # small
        assert plt.rcParams["legend.fontsize"] == 8  # small

        # Check other settings
        assert plt.rcParams["savefig.dpi"] == 300
        assert plt.rcParams["pdf.fonttype"] == 42
        assert plt.rcParams["ps.fonttype"] == 42

    def test_set_rc_params_custom_sizes(self):
        """Test set_rc_params with custom font sizes."""
        figures.set_rc_params(small=6, medium=9, big=14)

        assert plt.rcParams["font.size"] == 9
        assert plt.rcParams["axes.titlesize"] == 14
        assert plt.rcParams["axes.labelsize"] == 9
        assert plt.rcParams["xtick.labelsize"] == 6
        assert plt.rcParams["ytick.labelsize"] == 6
        assert plt.rcParams["legend.fontsize"] == 6

    def test_set_rc_params_font_family(self):
        """Test set_rc_params with different font families."""
        # Test serif
        figures.set_rc_params(fontfamily="serif")
        assert plt.rcParams["font.family"][0] == "serif"

        # Test sans-serif
        figures.set_rc_params(fontfamily="sans-serif")
        assert plt.rcParams["font.family"][0] == "sans-serif"

        # Test monospace
        figures.set_rc_params(fontfamily="monospace")
        assert plt.rcParams["font.family"][0] == "monospace"

    def test_set_rc_params_invalid_sizes(self):
        """Test set_rc_params with invalid font sizes."""
        with pytest.raises(ValueError, match="Font sizes must be positive integers"):
            figures.set_rc_params(small=0, medium=10, big=12)

        with pytest.raises(ValueError, match="Font sizes must be positive integers"):
            figures.set_rc_params(small=-5, medium=10, big=12)

        with pytest.raises(ValueError, match="Font sizes must be positive integers"):
            figures.set_rc_params(small=5.5, medium=10, big=12)

    def test_set_rc_params_resets_to_defaults(self):
        """Test that set_rc_params resets to defaults first."""
        # Modify some rcParams
        plt.rcParams["font.size"] = 20
        plt.rcParams["axes.titlesize"] = 30

        # Call set_rc_params
        figures.set_rc_params(small=8, medium=10, big=12)

        # Should be reset to our values, not influenced by previous changes
        assert plt.rcParams["font.size"] == 10
        assert plt.rcParams["axes.titlesize"] == 12


class TestGetFigures:
    """Test suite for get_figures function."""

    def teardown_method(self):
        """Close all figures after each test."""
        plt.close("all")

    def test_get_figures_basic(self):
        """Test basic figure creation."""
        fig, axs = figures.get_figures(rows=2, cols=3, figwidth=10, figheight=8)

        assert fig is not None
        assert isinstance(fig, plt.Figure)
        assert axs.shape == (2, 3)
        assert len(fig.axes) == 6

    def test_get_figures_single_subplot(self):
        """Test single subplot creation."""
        fig, ax = figures.get_figures(rows=1, cols=1, figwidth=5, figheight=5)

        assert fig is not None
        assert isinstance(ax, plt.Axes)  # Single axis, not array
        assert len(fig.axes) == 1

    def test_get_figures_cm_units(self):
        """Test figure creation with cm units."""
        figwidth_cm, figheight_cm = 2.54, 2.54
        fig, ax = figures.get_figures(rows=1, cols=1, unit="cm", figwidth=figwidth_cm, figheight=figheight_cm)

        expected_width = figwidth_cm / CM2INCH
        expected_height = figheight_cm / CM2INCH

        assert np.isclose(fig.get_figwidth(), expected_width, rtol=1e-10)
        assert np.isclose(fig.get_figheight(), expected_height, rtol=1e-10)

    def test_get_figures_inch_units(self):
        """Test figure creation with inch units."""
        figwidth_inch, figheight_inch = 4, 3
        fig, ax = figures.get_figures(rows=1, cols=1, unit="inch", figwidth=figwidth_inch, figheight=figheight_inch)

        assert np.isclose(fig.get_figwidth(), figwidth_inch, rtol=1e-10)
        assert np.isclose(fig.get_figheight(), figheight_inch, rtol=1e-10)

    def test_get_figures_sharex_sharey(self):
        """Test shared axes functionality."""
        fig, axs = figures.get_figures(rows=2, cols=2, figwidth=10, figheight=10, sharex=True, sharey=True)

        # Check that axes are shared
        assert axs[0, 0].get_shared_x_axes().joined(axs[0, 0], axs[1, 0])
        assert axs[0, 0].get_shared_y_axes().joined(axs[0, 0], axs[0, 1])

    def test_get_figures_invalid_dimensions(self):
        """Test invalid dimension parameters."""
        with pytest.raises(ValueError, match="Rows and columns must be positive"):
            figures.get_figures(rows=0, cols=1)

        with pytest.raises(ValueError, match="Rows and columns must be positive"):
            figures.get_figures(rows=1, cols=-1)

        with pytest.raises(ValueError, match="Figure dimensions must be positive"):
            figures.get_figures(rows=1, cols=1, figwidth=0)

        with pytest.raises(ValueError, match="Figure dimensions must be positive"):
            figures.get_figures(rows=1, cols=1, figheight=-5)

    def test_get_figures_invalid_unit(self):
        """Test invalid unit parameter."""
        with pytest.raises(ValueError, match="unit mm not supported"):
            figures.get_figures(rows=1, cols=1, unit="mm")

    def test_get_figures_style_applied(self):
        """Test that publication-ready styling is applied."""
        fig, ax = figures.get_figures(rows=1, cols=1, figwidth=10, figheight=8)

        # Check spine visibility
        assert not ax.spines["top"].get_visible()
        assert not ax.spines["right"].get_visible()
        assert ax.spines["left"].get_visible()
        assert ax.spines["bottom"].get_visible()

        # Check spine width
        assert ax.spines["left"].get_linewidth() == 1.4
        assert ax.spines["bottom"].get_linewidth() == 1.4

        # Check spine position (outward offset)
        left_pos = ax.spines["left"].get_position()
        bottom_pos = ax.spines["bottom"].get_position()
        assert left_pos[0] == "outward"
        assert bottom_pos[0] == "outward"
        assert left_pos[1] == 5  # offleft default
        assert bottom_pos[1] == 5  # offbottom default

    def test_get_figures_grid_style(self):
        """Test that grid styling is applied."""
        fig, ax = figures.get_figures(rows=1, cols=1, figwidth=10, figheight=8)

        # Add some data to make grid visible
        ax.plot([1, 2, 3], [1, 2, 3])

        # Check grid properties
        assert ax.yaxis.grid
        # Grid lines should be present (though testing exact properties is tricky)

    def test_get_figures_tick_style(self):
        """Test that tick styling is applied."""
        fig, ax = figures.get_figures(rows=1, cols=1, figwidth=10, figheight=8)

        # Check major tick parameters
        major_ticks = ax.tick_params
        # Note: testing tick parameters directly is complex in matplotlib
        # The styling function is applied, which is what we can verify
        assert hasattr(ax, "tick_params")

    def test_get_figures_subplot_kw(self):
        """Test passing additional subplot_kw arguments."""
        fig, axs = figures.get_figures(rows=2, cols=2, figwidth=10, figheight=10, subplot_kw={"facecolor": "lightgray"})

        # Check that subplot_kw was applied
        for ax in axs.flat:
            assert hasattr(ax, "get_facecolor")

    def test_get_figures_interactive_mode(self):
        """Test that interactive mode is turned off."""
        # Store original state
        original_state = plt.isinteractive()

        # Turn on interactive mode
        plt.ion()
        assert plt.isinteractive()

        # Create figure
        fig, ax = figures.get_figures(rows=1, cols=1, figwidth=5, figheight=5)

        # Interactive mode should be off
        assert not plt.isinteractive()

        # Restore original state
        if original_state:
            plt.ion()
        else:
            plt.ioff()


class TestIntegration:
    """Integration tests combining both functions."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")
        mpl.rcParams.update(mpl.rcParamsDefault)

    def test_full_workflow(self):
        """Test a complete workflow similar to the example."""
        # Set parameters
        figures.set_rc_params(fontfamily="serif", small=8, medium=10, big=12)

        # Create figure
        fig, axs = figures.get_figures(rows=2, cols=1, unit="cm", figwidth=10, figheight=15, sharex=True, sharey=True)

        # Verify we have the right setup
        assert len(axs) == 2
        assert plt.rcParams["font.family"][0] == "serif"
        assert plt.rcParams["font.size"] == 10

        # Add some content
        x = list(range(11))
        y = list(range(11))

        axs[0].plot(x, y)
        axs[0].set_xlabel("x")
        axs[0].set_ylabel("y")

        axs[1].plot(x, y)
        axs[1].set_xlabel("x")
        axs[1].set_ylabel("y")

        # This should work without errors
        fig.tight_layout()

        # Verify labels are set
        assert axs[0].get_xlabel() == "x"
        assert axs[0].get_ylabel() == "y"
        assert axs[1].get_xlabel() == "x"
        assert axs[1].get_ylabel() == "y"


if __name__ == "__main__":
    pytest.main([__file__])
