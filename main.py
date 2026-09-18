# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 3

# Imports (Requirement #2)
import os

import matplotlib

# Agg backend saves charts to files without opening a window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

# CISA Known Exploited Vulnerabilities catalog from data.gov, downloaded fresh each run. (Requirement #3)
KEV_CSV_URL = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"

# Load the catalog into a DataFrame, one row per vulnerability. (Requirement #4)
kev_df = pd.read_csv(KEV_CSV_URL, parse_dates=["dateAdded", "dueDate"])

# Question: Which vendors have the most known exploited vulnerabilities?
# value_counts() sorts from most to least, so head() gives the top vendors.
TOP_N = 5
top_vendors = kev_df["vendorProject"].value_counts().head(TOP_N)

print(f"Top {TOP_N} vendors by known exploited vulnerabilities:")
for rank, (vendor, count) in enumerate(top_vendors.items(), start=1):
    share = count / len(kev_df) * 100
    print(f"{rank}. {vendor}: {count} ({share:.1f}% of the catalog)")

# ---------------------------------------------------------------------------
# Chart - top vendors compared to the whole catalog (Requirements #5 and #6)
# ---------------------------------------------------------------------------

# Output folder, created on run and ignored by git.
CHART_DIR = "charts"

# Blue for vendors, gray for the 100% comparison bar.
VENDOR_COLOR = "#2a78d6"
TOTAL_COLOR = "#b5b3ad"

# Muted text and grid colors.
INK = "#0b0b0b"
INK_SOFT = "#52514e"
GRID = "#dedcd6"
BACKGROUND = "#fcfcfb"

# Top vendors plus an "All vendors" row for the 100% bar.
chart_df = top_vendors.rename("count").to_frame()
chart_df.loc["All vendors"] = len(kev_df)
chart_df["share"] = chart_df["count"] / len(kev_df) * 100
chart_df["color"] = [VENDOR_COLOR] * TOP_N + [TOTAL_COLOR]

figure, ax = plt.subplots(figsize=(11, 5))
figure.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)

# Reversed so the #1 vendor is on top and the 100% bar is on the bottom.
plot_df = chart_df.iloc[::-1]
bars = ax.barh(plot_df.index, plot_df["share"], color=plot_df["color"],
               height=0.6, zorder=2)

# Count and share label on each bar.
for bar, (count, share) in zip(bars, plot_df[["count", "share"]].itertuples(index=False)):
    ax.annotate(f" {count:,}  ({share:.1f}%)", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                va="center", fontsize=9, color=INK)

# Divider between the vendor bars and the 100% bar.
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
