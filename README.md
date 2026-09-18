# MiniProject3

## Question

**Which vendors have the most known exploited vulnerabilities?**

The data comes from CISA's [Known Exploited Vulnerabilities (KEV) Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog),
listed on data.gov. Every entry is a vulnerability that attackers have actually used
in the wild, not just one that was reported. The script counts the catalog entries
for each vendor and prints the top 5.

## Answer

As of 2026-09-18 (1,715 vulnerabilities in the catalog):

| Rank | Vendor | Exploited vulnerabilities | Share of catalog |
| --- | --- | --- | --- |
| 1 | Microsoft | 388 | 22.6% |
| 2 | Cisco | 99 | 5.8% |
| 3 | Apple | 94 | 5.5% |
| 4 | Adobe | 81 | 4.7% |
| 5 | Google | 75 | 4.4% |

Microsoft has nearly four times as many exploited vulnerabilities as the next vendor.
CISA adds to the catalog regularly, so these numbers change over time. The script
always downloads the latest version.

## AI Usage

| Date | Tool | What it did |
| --- | --- | --- |
| 2026-09-18 | Claude Code (Opus 5) | Recommended data.gov telecom/IT datasets; I chose the CISA KEV catalog. |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the data loading section of `main.py`: the `pandas` import, the `KEV_CSV_URL` constant, loading the CSV into the `kev_df` DataFrame with parsed date columns, and the printed sanity check. |
| 2026-09-18 | Claude Code (Opus 5) | Created `requirements.txt` (pinned from `pip freeze`) and `.gitignore` (copied from my Mini Project 2; ignores `.venv/`, `__pycache__/`, and `charts/`). |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the top 5 vendors section of `main.py` (`value_counts()` on `vendorProject`, printed with each vendor's share of the catalog) and added the Question and Answer sections to the README. |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the chart section of `main.py`: a horizontal bar chart of the top 5 vendors by share of the catalog, with a gray "All vendors" 100% bar at the bottom for comparison, saved to `charts/top_vendors.png`. Added `matplotlib` to `requirements.txt`. |
