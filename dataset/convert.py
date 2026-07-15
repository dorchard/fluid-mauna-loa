import json
import pandas as pd

# Adjust this to your input file path
input_path = "co2_mlo_surface-insitu_1_ccgg_MonthlyData.txt"
output_path = "co2_mm_mlo.json"

# NOAA surface in-situ files have comment lines starting with #
# followed by a header row, then whitespace-separated data.
df = pd.read_csv(
    input_path,
    comment="#",
    sep=r"\s+",
    header=0,
)

# NOAA uses -999.99 for missing values in this format
df = df[df["value"] != -999.99].copy()

# Keep only the fields Fluid needs
df = df[["year", "month", "value"]].rename(columns={"value": "ppm"})

# Make sure types are clean
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["ppm"] = df["ppm"].astype(float)

records = df.to_dict(orient="records")

with open(output_path, "w") as f:
    json.dump(records, f, indent=2)

print(f"Wrote {len(records)} rows to {output_path}")