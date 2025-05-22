# %% Import modules
from src.figures import Plotting

settings = Plotting()
settings.set_rc_params(fontfamily="Arial", small=8, medium=10, big=12)
plot, axs = settings.get_figures(rows=1, cols=2, unit="cm", figwidth=10, figheight=10, sharex=True, sharey=True)

axs[0].plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
axs[0].set_title("title")
axs[0].set_xlim(0, 11)
axs[0].set_ylim(0, 11)
axs[0].set_xticks([0, 5, 10])
axs[0].set_yticks([0, 5, 10])
axs[0].set_xticklabels(["0", "5", "10"])
axs[0].set_yticklabels(["0", "5", "10"])

axs[1].plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")
axs[1].set_title("title")
axs[1].set_xlim(0, 11)
axs[1].set_ylim(0, 11)
axs[1].set_xticks([0, 5, 10])
axs[1].set_yticks([0, 5, 10])
axs[1].set_xticklabels(["0", "5", "10"])
axs[1].set_yticklabels(["0", "5", "10"])

plot.set_style(offleft=5, offbottom=5, spinewidth=1.4)
plot.savefig("test.pdf")


# %%
