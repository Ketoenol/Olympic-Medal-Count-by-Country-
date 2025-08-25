# medal_stacked_by_country.py
# Year vs Total medals (stacked by country) + value labels above bars

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("Olympics (1896-2024).csv")   # change if your file is elsewhere
TOP_N = 8                                     # how many countries to show
SAVE_PNG = True                               # also save to PNG


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Expect columns: Year, Rank, NOC, Gold, Silver, Bronze, Total
    needed = {"Year", "NOC", "Total"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    return df


def make_pivot(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    # Sum in case duplicates exist
    by_year_noc = df.groupby(["Year", "NOC"])["Total"].sum().reset_index()

    # Choose top-N countries across all years
    top_countries = (
        df.groupby("NOC")["Total"].sum().nlargest(top_n).index.tolist()
    )

    # Keep only those countries and pivot to Year rows × Country columns
    pivot = (
        by_year_noc[by_year_noc["NOC"].isin(top_countries)]
        .pivot(index="Year", columns="NOC", values="Total")
        .fillna(0)
        .sort_index()
    )
    return pivot


def annotate_totals(ax, pivot: pd.DataFrame):
    """Write the total medals above each stacked bar."""
    totals = pivot.sum(axis=1).values
    # bar centers match the xticks
    for x, total in zip(ax.get_xticks(), totals):
        ax.text(
            x, total,                # position: at top of bar
            f"{int(total)}",         # text shown above bar
            ha="center", va="bottom",
            fontsize=9
        )


def plot_stacked(pivot: pd.DataFrame, save_png: bool):
    ax = pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(16, 9)
    )
    ax.set_xlabel("Olympic Year")
    ax.set_ylabel("Total Medals (stacked by country)")
    ax.set_title("Year vs Total Medals (Stacked Barplot by Country)")
    ax.legend(title="Country", bbox_to_anchor=(1.02, 1), loc="upper left")
    annotate_totals(ax, pivot)   # <<— labels above each bar
    plt.tight_layout()

    if save_png:
        out = Path("year_vs_total_stacked_by_country.png")
        plt.savefig(out, dpi=200)
        print(f"Saved figure to {out.resolve()}")

    plt.show()


def main():
    df = load_data(CSV_PATH)
    pivot = make_pivot(df, TOP_N)
    plot_stacked(pivot, SAVE_PNG)


if __name__ == "__main__":
    main()
