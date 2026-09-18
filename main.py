# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 3

# Imports (Requirement #2)
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
