[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![CI](https://github.com/RDoerfel/plotting/workflows/CI/badge.svg)](https://github.com/RDoerfel/plotting/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/RDoerfel/plotting/branch/main/graph/badge.svg)](https://codecov.io/gh/RDoerfel/plotting)
<br>

# Plotting

A lightweight, high-level Python library for creating publication-ready scientific figures with consistent styling. Built on top of matplotlib, this package provides a simplified interface for generating plots that meet the standards of scientific journals.

## Features

- **Publication-ready styling**: Clean, professional appearance with proper font embedding
- **Consistent layout**: Standardized spine positioning, grid styling, and tick formatting
- **Flexible units**: Support for both centimeters and inches for figure dimensions
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Minimal dependencies**: Only requires matplotlib
- **Easy customization**: Simple font and size configuration

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/RDoerfel/plotting.git
```

## Quick Start

```python
from plotting import set_rc_params, get_figures
import numpy as np

# Configure publication-ready styling
set_rc_params(fontfamily="serif", small=8, medium=10, big=12)

# Create figure with subplots
fig, axs = get_figures(rows=2, cols=1, unit="cm", figwidth=10, figheight=15)

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Plot data
axs[0].plot(x, y1, label='sin(x)')
axs[0].set_xlabel("x")
axs[0].set_ylabel("sin(x)")
axs[0].legend()

axs[1].plot(x, y2, 'r--', label='cos(x)')
axs[1].set_xlabel("x")
axs[1].set_ylabel("cos(x)")
axs[1].legend()

# Save with high quality
fig.savefig("scientific_plot.pdf", dpi=300, bbox_inches="tight")
```

## API Reference

### `set_rc_params(fontfamily=None, small=8, medium=10, big=12)`

Configure global matplotlib parameters for publication-ready plots.

**Parameters:**
- `fontfamily` (str, optional): Font family ('serif', 'sans-serif', 'monospace')
- `small` (int): Font size for ticks and legend (default: 8)
- `medium` (int): Font size for labels and default text (default: 10)
- `big` (int): Font size for titles (default: 12)

**Example:**
```python
# Use serif fonts with larger text
set_rc_params(fontfamily="serif", small=10, medium=12, big=14)
```

### `get_figures(rows, cols, unit="cm", figwidth=10, figheight=8, sharex=False, sharey=False, **subplot_kw)`

Create styled figure and axes with publication-ready formatting.

**Parameters:**
- `rows` (int): Number of subplot rows
- `cols` (int): Number of subplot columns
- `unit` (str): Units for dimensions ("cm" or "inch", default: "cm")
- `figwidth` (float): Figure width in specified units (default: 10)
- `figheight` (float): Figure height in specified units (default: 8)
- `sharex` (bool): Share x-axis across subplots (default: False)
- `sharey` (bool): Share y-axis across subplots (default: False)
- `**subplot_kw`: Additional arguments passed to `plt.subplots()`

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object
- `axs` (matplotlib.axes.Axes or array): Axes object(s)

**Examples:**
```python
# Single plot
fig, ax = get_figures(1, 1, figwidth=8, figheight=6)

# Multiple subplots with shared x-axis
fig, axs = get_figures(3, 2, unit="inch", figwidth=8, figheight=10, sharex=True)

# Custom subplot parameters
fig, axs = get_figures(2, 2, subplot_kw={'facecolor': 'white'})
```

## Styling Features

The library automatically applies several publication-ready styling features:

- **Clean spines**: Removes top and right spines, positions left and bottom spines with appropriate offsets
- **Grid styling**: Adds subtle horizontal grid lines for better readability
- **Tick formatting**: Consistent tick styling with proper direction and sizing
- **Font embedding**: Ensures fonts are properly embedded in PDF outputs (fonttype 42)
- **High DPI**: Default 300 DPI for crisp figures

## Best Practices

1. **Always call `set_rc_params()` first** to ensure consistent styling across all figures
2. **Use centimeters for dimensions** when targeting specific journal requirements
3. **Set explicit axis limits and ticks** for precise control over the appearance
4. **Save as PDF or PNG** with `bbox_inches="tight"` for best quality

## Requirements

- Python ≥ 3.10
- matplotlib ≥ 3.5.0

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Development

This library is designed to be minimal and focused. For testing:

```bash
pytest test/ --cov=plotting
```

The package is tested across Python 3.10, 3.11, and 3.12 on Linux, macOS, and Windows.