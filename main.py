# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 3

# Imports (Requirement #2)
import os

import matplotlib

# The Agg backend draws straight to a file, which is all this program needs
# since the chart is saved as a PNG instead of opened in a window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

# CISA Known Exploited Vulnerabilities (KEV) catalog, published as a single CSV
# and listed on data.gov. It is downloaded fresh on every run so the numbers are
# always current and no data file has to be committed. (Requirement #3)
KEV_CSV_URL = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"

# Download the catalog straight into a Pandas DataFrame. Each row is one
# vulnerability and each column is one field from the catalog. The two date
# columns are parsed as real dates so they can be grouped by year or month
# later on. (Requirement #4)
kev_df = pd.read_csv(KEV_CSV_URL, parse_dates=["dateAdded", "dueDate"])

# Quick check that the data came back the way it was expected.
print(f"Downloaded {len(kev_df)} known exploited vulnerabilities from CISA.")
print(f"DataFrame shape: {kev_df.shape} (rows = vulnerabilities, columns = fields)")
print(f"Date range: {kev_df['dateAdded'].min():%Y-%m-%d} to {kev_df['dateAdded'].max():%Y-%m-%d}")
print("\nColumns and data types:")
print(kev_df.dtypes)
print("\nFirst 5 rows:")
print(kev_df[["cveID", "vendorProject", "product", "dateAdded", "knownRansomwareCampaignUse"]].head())

# Question: Which vendors have the most known exploited vulnerabilities?
# Count how many catalog entries belong to each vendor, then keep the top 5.
# value_counts() already sorts from most to least, so head() gives the leaders.
TOP_N = 5
top_vendors = kev_df["vendorProject"].value_counts().head(TOP_N)

print(f"\nTop {TOP_N} vendors by known exploited vulnerabilities:")
for rank, (vendor, count) in enumerate(top_vendors.items(), start=1):
    share = count / len(kev_df) * 100
    print(f"{rank}. {vendor}: {count} ({share:.1f}% of the catalog)")

# ---------------------------------------------------------------------------
# Chart - top vendors compared to the whole catalog (Requirements #5 and #6)
# ---------------------------------------------------------------------------

# Folder the finished PNG chart is written to. It is created on each run and is
# listed in .gitignore so the image stays out of the repository.
CHART_DIR = "charts"

# Vendor bars share one color. The comparison bar is a neutral gray so it reads
# as the reference, not as another vendor.
VENDOR_COLOR = "#2a78d6"
TOTAL_COLOR = "#b5b3ad"

# Text and grid colors, kept muted so the data stays the loudest thing on the
# chart.
INK = "#0b0b0b"
INK_SOFT = "#52514e"
GRID = "#dedcd6"
BACKGROUND = "#fcfcfb"

# Build the rows to plot: the top vendors, then one extra row for the entire
# catalog, which is the 100% bar the vendors are compared against.
chart_df = top_vendors.rename("count").to_frame()
chart_df.loc["All vendors"] = len(kev_df)
chart_df["share"] = chart_df["count"] / len(kev_df) * 100
chart_df["color"] = [VENDOR_COLOR] * TOP_N + [TOTAL_COLOR]

figure, ax = plt.subplots(figsize=(11, 5))
figure.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)

# Horizontal bars read top to bottom, so the rows are reversed to put the #1
# vendor at the top and the 100% bar at the bottom.
plot_df = chart_df.iloc[::-1]
bars = ax.barh(plot_df.index, plot_df["share"], color=plot_df["color"],
               height=0.6, zorder=2)

# Label each bar with its count and share so the exact numbers are readable
# without estimating from the axis.
for bar, (count, share) in zip(bars, plot_df[["count", "share"]].itertuples(index=False)):
    ax.annotate(f" {count:,}  ({share:.1f}%)", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                va="center", fontsize=9, color=INK)

# A thin divider separates the vendor bars from the comparison bar.
ax.axhline(0.5, color=GRID, linewidth=1, zorder=1)

ax.set_xlim(0, 115)
ax.set_xticks(range(0, 101, 20))
ax.set_xticklabels([f"{tick}%" for tick in range(0, 101, 20)])
ax.set_xlabel("Share of all known exploited vulnerabilities", color=INK_SOFT, fontsize=10)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

ax.set_title(f"Top {TOP_N} vendors by known exploited vulnerabilities", fontsize=14,
             color=INK, loc="left", fontweight="bold", pad=18)
ax.text(0.0, 1.02, f"CISA KEV catalog, {len(kev_df):,} vulnerabilities as of "
        f"{kev_df['dateAdded'].max():%Y-%m-%d}. Bottom bar is the full catalog (100%).",
        transform=ax.transAxes, fontsize=10, color=INK_SOFT)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GRID)
ax.tick_params(colors=INK_SOFT, labelsize=10, length=0)

os.makedirs(CHART_DIR, exist_ok=True)
chart_path = os.path.join(CHART_DIR, "top_vendors.png")
figure.savefig(chart_path, dpi=150, bbox_inches="tight", facecolor=figure.get_facecolor())
plt.close(figure)
print(f"\nSaved {chart_path}")
