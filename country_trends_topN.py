import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("Olympics (1896-2024).csv")
TOP_N = 8

df = pd.read_csv(CSV_PATH)
top = df.groupby("NOC")["Total"].sum().nlargest(TOP_N).index
small = df[df["NOC"].isin(top)].groupby(["Year", "NOC"])["Total"].sum().reset_index()

plt.figure(figsize=(16, 9))
for noc, g in small.groupby("NOC"):
    g = g.sort_values("Year")
    plt.plot(g["Year"], g["Total"], label=noc)
plt.title("Country Medal Trends Across Years (Top countries)")
plt.xlabel("Olympic Year")
plt.ylabel("Total Medals")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Country")
plt.tight_layout()
plt.savefig("country_trends_topN.png", dpi=200)
plt.show()
