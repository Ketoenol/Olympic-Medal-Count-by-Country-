# olympics_barchart_race.py
# Animated Bar Chart Race of Olympic medals by country

import pandas as pd
import bar_chart_race as bcr
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")


CSV_PATH = Path("Olympics (1896-2024).csv")
TOP_N = 10   # top countries to display in the race

# Load dataset
df = pd.read_csv(CSV_PATH)

# Group by Year + Country
medals_by_year = df.groupby(["Year", "NOC"])["Total"].sum().reset_index()

# Pivot: rows = Year, columns = Country, values = medals
pivot = medals_by_year.pivot(index="Year", columns="NOC", values="Total").fillna(0)

# Optionally, filter only top-N overall medal countries
top_countries = df.groupby("NOC")["Total"].sum().nlargest(TOP_N).index
pivot = pivot[top_countries]

# Create the animated race chart
bcr.bar_chart_race(
    df=pivot,
    filename="olympics_medals_race.mp4",   # saves as mp4
    orientation="h",
    sort="desc",
    n_bars=10,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=5,
    interpolate_period=False,
    period_length=800,   # ms between frames
    figsize=(10, 6),
    title="Olympic Medals Race by Country (1896–2024)",
    bar_size=.95,
    cmap='tab20'
)
