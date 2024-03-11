import pandas as pd
import matplotlib.pyplot as plt
import math


def draw_hist(col: str, df: pd.DataFrame, bin: int, yscale: str = "linear"):
    title = col.capitalize()
    plt.hist(df[col], bins=bin)
    plt.xlabel(title)
    plt.ylabel("log Count")
    plt.yscale(yscale)
    plt.title("Histogram of " + title)


def draw_hist_all(df: pd.DataFrame, bin: int, yscale: str = "linear"):
    row = math.ceil(df.shape[1] / 4)
    plt.figure(figsize=(16, row * 4))
    for idx, col in enumerate(df.columns, 1):
        plt.subplot(row, 4, idx)
        draw_hist(col, df, bin, yscale)
    plt.tight_layout()
    plt.show()
