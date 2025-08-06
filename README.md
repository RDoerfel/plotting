# Plotting
This is a high-level interface to create publication ready plots using Python with matplotlib and seaborn. 

## Installation
### Install the package from github
```bash
pip install git+git@github.com:RDoerfel/plotting.git
```

## Usage
```python
from plotting import set_rc_params, get_figures


set_rc_params(fontfamily="serif", small=8, medium=10, big=12)
fig, axs = get_figures(rows=2, cols=1, unit="cm", figwidth=10, figheight=15, sharex=True, sharey=True)

axs[0].plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
axs[0].set_xlim(0, 11)
axs[0].set_ylim(0, 11)
axs[0].set_xticks([0, 5, 10])
axs[0].set_yticks([0, 5, 10])
axs[0].set_xticklabels(["0", "5", "10"])
axs[0].set_yticklabels(["0", "5", "10"])

axs[1].plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")
axs[1].set_xlim(0, 11)
axs[1].set_ylim(-1, 11)
axs[1].set_xticks([0, 5, 10])
axs[1].set_yticks([0, 5, 10])
axs[1].set_xticklabels(["0", "5", "10"])
axs[1].set_yticklabels(["0", "5", "10"])

fig.tight_layout()
fig.savefig("example_plot.png", dpi=300, bbox_inches="tight", pad_inches=0.1)
```