"""
An add on to improve on matplotlib's aesthetics
https://towardsdatascience.com/making-matplotlib-beautiful-by-default-d0d41e3534fd
"""

import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset('iris')

marron_fonce = "#5D3A2C"
marron_clair = "#C39757"
beige = "#DFCC9E"
blanc_lait = "#E9E5D3"
gris_fonce = "#262D33"

vert_delave = "#C3CD9B"
beige2 = "#DDD2BE"
marron_clair2 = "#A58D6C"

def set_plt() :
    sns.set(font="Agency FB",
            rc={"axes.axisbelow": False,
                "axes.edgecolor": beige,
                "axes.facecolor": "None",
                "axes.grid": True,
                "axes.labelcolor": beige,
                "axes.spines.right": False,
                "axes.spines.top": False,
                "axes.titlesize": "x-large",
                "axes.titleweight": "normal",
                "axes.grid.axis":     "both",    # which axis the grid should apply to
                "axes.grid.which":    "major",
                "grid.color": blanc_lait, 
                "grid.linestyle": "dashed" ,    # solid
                "grid.linewidth": "0.8",     # in points
                "grid.alpha":     "0.2",
                "figure.facecolor": gris_fonce,
                "lines.solid_capstyle": "round",
                "patch.edgecolor": "w",
                "patch.force_edgecolor": True,
                "text.color": beige,
                "xtick.bottom": False,
                "xtick.color": beige,
                "xtick.direction": "out",
                "xtick.top": False,
                "ytick.color": beige,
                "ytick.direction": "out",
                "ytick.left": False,
                "ytick.right": False})


    color_list = [
        "#5C9FB5",
        "#4CAF44",
        "#A05090",
        "#ECC454",
        "#DD6248"
        ]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

if __name__ == "__main__" :
    plt.scatter(iris.sepal_length, iris.sepal_width, label="Length X Width")
    plt.xlabel("Sepal Length")
    plt.ylabel("Sepal Width")
    plt.title("Un beau titre")
    plt.legend()
    plt.show()

