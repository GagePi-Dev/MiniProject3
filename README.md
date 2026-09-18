# INF 601 - Mini Project 3

A small Pandas and Matplotlib project that answers one question with public data:
which software vendors show up most often in CISA's catalog of vulnerabilities that
attackers are actively exploiting. The script downloads the catalog, loads it into a
Pandas DataFrame, prints the top 5 vendors, and saves a bar chart of the result.

## Question

**Which vendors have the most known exploited vulnerabilities?**

The data comes from CISA's [Known Exploited Vulnerabilities (KEV) Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog),
listed on data.gov. Every entry is a vulnerability that attackers have actually used
in the wild, not just one that was reported. The script counts the catalog entries
for each vendor and prints the top 5.

## Answer

As of 2026-09-18 (1,716 vulnerabilities in the catalog):

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

## Setup

This project was built with Python 3.14. From the project folder, create and
activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

No API key or data download is needed. The script pulls the catalog CSV directly from
`https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv`
each time it runs, so an internet connection is required.

## Running

```bash
python main.py
```

The script:

1. Downloads the KEV catalog into a Pandas DataFrame (`kev_df`) and prints a quick
   check of the data: row count, shape, date range, column types, and the first 5 rows.
2. Counts the entries for each vendor and prints the top 5 with each vendor's share of
   the catalog.
3. Saves a bar chart to `charts/top_vendors.png`.

The `charts/` folder is created automatically on each run and is listed in
`.gitignore`, so the generated PNG is never committed. To chart more or fewer
vendors, change `TOP_N` in `main.py`.

## Chart

`charts/top_vendors.png` is a horizontal bar chart of the top vendors, measured as a
share of the whole catalog. A gray **All vendors** bar at the bottom represents 100%
of the catalog, so each vendor's bar can be compared against the total. Every bar is
labeled with its count and percentage.

## Structure

| File | Purpose |
| --- | --- |
| `main.py` | Downloads the catalog, builds the DataFrame, prints the top vendors, and saves the chart. |
| `requirements.txt` | Pinned package versions (`pandas`, `matplotlib`, and their dependencies). |
| `.gitignore` | Keeps the virtual environment, cache files, and `charts/` out of the repository. |

Main pieces of `main.py`:

| Name | Purpose |
| --- | --- |
| `KEV_CSV_URL` | Link to the CISA KEV catalog CSV. |
| `kev_df` | DataFrame of the full catalog, one row per vulnerability, with `dateAdded` and `dueDate` parsed as dates. |
| `TOP_N` / `top_vendors` | How many vendors to show, and their counts from `value_counts()` on `vendorProject`. |
| `chart_df` | The top vendors plus an "All vendors" row, with each row's share and bar color, used to draw the chart. |
| `CHART_DIR` | Folder the PNG is saved to (`charts`). |

## AI Usage

### What I used Claude Code for

Claude Code (Opus 5) recommended data.gov datasets in the telecom and IT field, and
I chose the CISA KEV catalog from its list. It then wrote each section of
`main.py` as I asked for it: loading the data into a DataFrame, printing the top 5
vendors, and the bar chart. It also created `requirements.txt` and `.gitignore` and
wrote this README. I directed the project section by section and decided the question,
the dataset, and the chart design, including the 100% comparison bar.

| Date | Tool | What it did |
| --- | --- | --- |
| 2026-09-18 | Claude Code (Opus 5) | Recommended data.gov telecom/IT datasets; I chose the CISA KEV catalog. |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the data loading section of `main.py`: the `pandas` import, the `KEV_CSV_URL` constant, loading the CSV into the `kev_df` DataFrame with parsed date columns, and the printed sanity check. |
| 2026-09-18 | Claude Code (Opus 5) | Created `requirements.txt` (pinned from `pip freeze`) and `.gitignore` (copied from my Mini Project 2; ignores `.venv/`, `__pycache__/`, and `charts/`). |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the top 5 vendors section of `main.py` (`value_counts()` on `vendorProject`, printed with each vendor's share of the catalog) and added the Question and Answer sections to the README. |
| 2026-09-18 | Claude Code (Opus 5) | Wrote the chart section of `main.py`: a horizontal bar chart of the top 5 vendors by share of the catalog, with a gray "All vendors" 100% bar at the bottom for comparison, saved to `charts/top_vendors.png`. Added `matplotlib` to `requirements.txt`. |
| 2026-09-18 | Claude Code (Opus 5) | Updated the catalog count in the Answer section and wrote the rest of the README (description, Setup, Running, Chart, Structure, and the AI Usage summary). |

### What I wrote myself

_To be filled in._

### What I changed in AI-generated code

_To be filled in._
