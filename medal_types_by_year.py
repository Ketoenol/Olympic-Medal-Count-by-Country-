import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("Olympics (1896-2024).csv")

df = pd.read_csv(CSV_PATH)
by_year = df.groupby("Year")[["Gold", "Silver", "Bronze"]].sum().sort_index()

ax = by_year.plot(kind="bar", stacked=True, figsize=(16, 9))
ax.set_title("Overall Medal Breakdown by Year (Gold/Silver/Bronze)")
ax.set_xlabel("Olympic Year")
ax.set_ylabel("Total Medals")
# annotate totals
totals = by_year.sum(axis=1).values
for x, total in zip(ax.get_xticks(), totals):
    ax.text(x, total, f"{int(total)}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("medal_types_by_year.png", dpi=200)
plt.show()
