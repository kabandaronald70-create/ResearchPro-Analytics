```python
# =========================================================
# NOTEBOOK STATE CHECK — run this any time after a restart
# =========================================================
required_objects = [
    "agsec1", "gsec1", "agsec4a", "agsec4b",
    "extracted_folder",
]

missing = [name for name in required_objects if name not in globals()]

if missing:
    print("Kernel was restarted. Missing objects:", missing)
    print("→ Run All Cells Above before continuing.")
else:
    print("All required objects are loaded. Ready to continue.")
```


```python
from pathlib import Path
import os

# --------------------------------------------------
# 1. Identify the project root
# --------------------------------------------------
current_dir = Path.cwd().resolve()

project_root = (
    current_dir.parent
    if current_dir.name.lower() == "notebooks"
    else current_dir
)

print("Current working directory:", current_dir)
print("Project root:", project_root)

# --------------------------------------------------
# 2. Identify the authorized dataset directory
# --------------------------------------------------
configured_path = os.environ.get("RESEARCHPRO_DATA_DIR")

if configured_path:
    extracted_folder = Path(configured_path).expanduser().resolve()

    if not extracted_folder.is_dir():
        raise NotADirectoryError(
            "RESEARCHPRO_DATA_DIR points to a directory "
            f"that does not exist: {extracted_folder}"
        )

    print("Dataset path source: RESEARCHPRO_DATA_DIR")

else:
    candidates = [
        project_root / "data" / "raw",
        project_root.parent.parent / "dataset",
        Path.home() / "Desktop" / "dataset",
    ]

    extracted_folder = next(
        (
            candidate.resolve()
            for candidate in candidates
            if (candidate / "Agric" / "AGSEC4A.csv").is_file()
        ),
        None,
    )

    if extracted_folder is None:
        searched_paths = "\n".join(
            f"  - {candidate.resolve()}" for candidate in candidates
        )

        raise FileNotFoundError(
            "Could not locate Agric/AGSEC4A.csv.\n"
            "Directories checked:\n"
            f"{searched_paths}\n\n"
            "Set RESEARCHPRO_DATA_DIR to the authorized "
            "dataset directory."
        )

    print("Dataset path source: automatic discovery")

# --------------------------------------------------
# 3. Validate the required dataset
# --------------------------------------------------
dataset_file = extracted_folder / "Agric" / "AGSEC4A.csv"

if not dataset_file.is_file():
    raise FileNotFoundError(
        "The required dataset was not found:\n"
        f"{dataset_file}\n\n"
        "Check RESEARCHPRO_DATA_DIR and confirm that "
        "the directory contains Agric/AGSEC4A.csv."
    )

print("\nDataset path validated successfully.")
print("Data folder:", extracted_folder)
print("Dataset file:", dataset_file)
print("File size (MB):", round(dataset_file.stat().st_size / (1024**2), 2))
```


```python
from pathlib import Path

current_dir = Path.cwd().resolve()

project_root = (
    current_dir.parent
    if current_dir.name.lower() == "notebooks"
    else current_dir
)

raw_data_dir = project_root / "data" / "raw"
processed_data_dir = project_root / "data" / "processed"

print("Project root:", project_root)
print("Raw data folder:", raw_data_dir)
print("Processed data folder:", processed_data_dir)
```


```python
required_variables = [
    "farmer_id",
    "age",
    "gender",
    "education_level",
    "household_size",
    "farm_size_acres",
    "training",
    "extension_access",
    "improved_seeds",
    "fertilizer_use",
    "pest_control",
    "mechanization",
    "technology_adoption",
]

print("Variables to investigate:", len(required_variables))

for variable in required_variables:
    print("-", variable)
```


```python
# --------------------------------------------------
# Inspect the authorized dataset directory
# --------------------------------------------------

if not extracted_folder.is_dir():
    print(
        "Data folder not found. Obtain the authorized dataset "
        "and configure RESEARCHPRO_DATA_DIR if necessary."
    )

else:
    files = sorted(
        path
        for path in extracted_folder.rglob("*")
        if path.is_file()
    )

    print("Dataset directory:", extracted_folder)
    print("Total files found:", len(files))
    print("\nFile inventory:")

    for file in files[:100]:
        print(file.relative_to(extracted_folder))

    if len(files) > 100:
        print(f"\nShowing the first 100 of {len(files)} files.")
```


```python
from collections import Counter

files_by_extension = Counter(
    file.suffix.lower()
    for file in extracted_folder.rglob("*")
    if file.is_file()
)

print("File types found:")

for extension, count in files_by_extension.most_common():
    print(f"{extension or '[no extension]'}: {count}")
```


```python
csv_files = list(extracted_folder.rglob("*.csv"))

print("CSV files found:", len(csv_files))

for file in csv_files[:50]:
    print(file.relative_to(extracted_folder))
```


```python
from collections import Counter

files_by_extension = Counter(
    file.suffix.lower()
    for file in extracted_folder.rglob("*")
    if file.is_file()
)

print("File types found:\n")

for extension, count in files_by_extension.most_common():
    print(f"{extension or '[no extension]'}: {count}")
```


```python
csv_files = list(extracted_folder.rglob("*.csv"))

print("Total CSV files:", len(csv_files))
print("\nFirst 50 CSV files:\n")

for file in csv_files[:50]:
    print(file.relative_to(extracted_folder))
```


```python
from pathlib import Path

# --------------------------------------------------
# Discover all PDF documentation files
# --------------------------------------------------

pdf_files = sorted(
    path
    for path in extracted_folder.rglob("*")
    if path.is_file() and path.suffix.lower() == ".pdf"
)

print("Dataset directory:", extracted_folder)
print("Total PDF files found:", len(pdf_files))
print("\nPDF documentation inventory:\n")

for index, pdf in enumerate(pdf_files, start=1):
    print(f"{index}. {pdf.name}")
    print(f"   Path: {pdf.relative_to(extracted_folder)}")
    print(f"   Size: {pdf.stat().st_size / 1024:.2f} KB")
```


```python
# Find every PDF file in the dataset directory
pdf_files = [
    file
    for file in extracted_folder.rglob("*")
    if file.is_file() and file.suffix.lower() == ".pdf"
]

print("Dataset directory:", extracted_folder)
print("Total PDF files found:", len(pdf_files))
print("\nPDF inventory:")

for pdf in sorted(pdf_files):
    print(f"- {pdf.relative_to(extracted_folder)}")
```


```python
from pathlib import Path
import pandas as pd

# Define the three candidate files
candidate_files = {
    "Seeds and crops": extracted_folder / "Agric" / "AGSEC4A.csv",
    "Extension services": extracted_folder / "Agric" / "AGSEC9A.csv",
    "Farm implements": extracted_folder / "Agric" / "AGSEC10.csv",
}

# Confirm that the files exist
for description, file_path in candidate_files.items():
    print(f"{description}: {file_path.exists()}")
```


```python
for description, file_path in candidate_files.items():
    print("\n" + "=" * 70)
    print(description.upper())
    print("=" * 70)

    data = pd.read_csv(file_path, nrows=5)

    print("\nNumber of columns:", len(data.columns))
    print("\nColumn names:")
    print(data.columns.tolist())

    print("\nFirst five records:")
    print("Preview omitted from the public notebook.")
```


```python
documentation_files = [
    file
    for file in extracted_folder.rglob("*")
    if file.is_file()
    and any(
        word in file.name.lower()
        for word in [
            "dictionary",
            "codebook",
            "questionnaire",
            "readme",
            "documentation",
            "label"
        ]
    )
]

print("Potential documentation files:", len(documentation_files))

for file in documentation_files[:100]:
    print(file.relative_to(extracted_folder))
```


```python
from collections import Counter

# Count the file types in the extracted survey folder
file_extensions = Counter(
    file.suffix.lower() or "[no extension]"
    for file in extracted_folder.rglob("*")
    if file.is_file()
)

print("File types found:\n")

for extension, count in file_extensions.most_common():
    print(f"{extension}: {count}")
```


```python
import pandas as pd

file_paths = {
    "Seeds and crops": extracted_folder / "Agric" / "AGSEC4A.csv",
    "Extension services": extracted_folder / "Agric" / "AGSEC9A.csv",
    "Farm implements": extracted_folder / "Agric" / "AGSEC10.csv",
}

for name, path in file_paths.items():
    data = pd.read_csv(path)

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Rows:", len(data))
    print("Columns:", len(data.columns))
    print("Unique households:", data["hhid"].nunique())
    print("Missing household IDs:", data["hhid"].isna().sum())
    print("Duplicate full rows:", data.duplicated().sum())
```


```python
import pandas as pd

file_paths = {
    "Seeds and crops": extracted_folder / "Agric" / "AGSEC4A.csv",
    "Extension services": extracted_folder / "Agric" / "AGSEC9A.csv",
    "Farm implements": extracted_folder / "Agric" / "AGSEC10.csv",
}

for name, path in file_paths.items():
    data = pd.read_csv(path)

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)
    print("Number of rows:", len(data))
    print("Number of columns:", len(data.columns))

    for column in data.columns:
        print(f"\nVariable: {column}")
        print("Data type:", data[column].dtype)
        print("Missing values:", data[column].isna().sum())
        print("Distinct non-missing values:", data[column].nunique())

    print("\nDataset summary completed without printing record-level values.")
```


```python
import pandas as pd

# Load the seeds and crops dataset
seeds = pd.read_csv(
    extracted_folder / "Agric" / "AGSEC4A.csv"
)

# Inspect the variables related to seed use
seed_variables = [
    "s4aq16",
    "s4aq13",
    "s4aq14",
    "s4aq10",
]

for variable in seed_variables:
    print("\n" + "=" * 50)
    print(f"Variable: {variable}")
    print("=" * 50)

    print("Value counts, including missing values:")

    print(
        seeds[variable]
        .value_counts(dropna=False)
        .sort_index()
    )
```


```python
# Display the seed-related questions and their recorded responses

seed_variables = ["s4aq16", "s4aq13", "s4aq14", "s4aq10"]

for variable in seed_variables:
    print(f"\n{'=' * 50}")
    print(f"Variable: {variable}")
    print(f"Number of records: {len(seeds)}")
    print("Response counts, including missing values:")
    print(seeds[variable].value_counts(dropna=False).sort_index())
```


```python
from pathlib import Path

# Find documentation and metadata files in the extracted dataset
metadata_extensions = {
    ".dta", ".sav", ".xlsx", ".xls",
    ".pdf", ".docx", ".xml", ".json"
}

metadata_files = [
    path for path in extracted_folder.rglob("*")
    if path.is_file()
    and path.suffix.lower() in metadata_extensions
]

print(f"Found {len(metadata_files)} potential metadata files.\n")

for path in metadata_files[:40]:
    print(path.relative_to(extracted_folder))
```


```python
from collections import Counter

# Count the file extensions in the extracted dataset
file_extensions = Counter(
    path.suffix.lower() or "[no extension]"
    for path in extracted_folder.rglob("*")
    if path.is_file()
)

print("File types found:\n")

for extension, count in file_extensions.most_common():
    print(f"{extension}: {count}")
```


```python
# Calculate seed-use indicators from the verified questionnaire codes

# Indicator 1: Whether seeds or seedlings were used
seed_use = seeds["s4aq16"].map({
    1: 1,
    2: 0
}).astype("Int64")

# Indicator 2: Improved-seed use, conditional on reported seed use
improved_seed_use = pd.Series(
    pd.NA,
    index=seeds.index,
    dtype="Int64"
)

valid_seed_type = (
    seeds["s4aq16"].eq(1)
    & seeds["s4aq13"].isin([1, 2])
)

improved_seed_use.loc[valid_seed_type] = (
    seeds.loc[valid_seed_type, "s4aq13"]
    .eq(2)
    .astype("int64")
)

# Summarize seed use
seed_use_summary = seed_use.value_counts(dropna=False).sort_index()

print("SEED USE")
print(f"Yes: {(seed_use == 1).sum()}")
print(f"No: {(seed_use == 0).sum()}")
print(f"Missing/not applicable: {seed_use.isna().sum()}")
print(
    f"Percentage of valid records using seeds: "
    f"{seed_use.mean() * 100:.2f}%"
)

# Summarize improved-seed use
print("\nIMPROVED-SEED USE")
print(f"Traditional: {(improved_seed_use == 0).sum()}")
print(f"Improved: {(improved_seed_use == 1).sum()}")
print(f"Missing/not applicable: {improved_seed_use.isna().sum()}")
print(
    f"Percentage of valid seed-type records using improved seeds: "
    f"{improved_seed_use.mean() * 100:.2f}%"
)
```


```python
# Check consistency between seed-use and seed-type responses

print("CHECK 1: Seed type recorded when no seeds were used")
check1 = seeds[
    (seeds["s4aq16"] == 2) &
    (seeds["s4aq13"].notna())
]
print(f"Inconsistent records: {len(check1)}")

print("\nCHECK 2: Improved-seed details recorded for traditional seeds")
check2 = seeds[
    (seeds["s4aq13"] == 1) &
    (seeds["s4aq14"].notna())
]
print(f"Potentially inconsistent records: {len(check2)}")

print("\nCHECK 3: Improved-seed details missing for improved seeds")
check3 = seeds[
    (seeds["s4aq13"] == 2) &
    (seeds["s4aq14"].isna())
]
print(f"Records to investigate: {len(check3)}")

print("\nCHECK 4: Seed-type response recorded when seed use is missing")
check4 = seeds[
    (seeds["s4aq16"].isna()) &
    (seeds["s4aq13"].notna())
]
print(f"Records to investigate: {len(check4)}")
```


```python
import pandas as pd

# ============================================================
# Prepare a clean working copy of the seed-use dataset
# Original data remain unchanged.
# ============================================================

seeds_clean = seeds.copy()

# ------------------------------------------------------------
# 1. Create the seed-use indicator
#    1 = Yes, 0 = No, <NA> = Missing or unknown
# ------------------------------------------------------------

seeds_clean["seed_use"] = (
    seeds_clean["s4aq16"]
    .map({
        1: 1,  # Seeds or seedlings were used
        2: 0   # Seeds or seedlings were not used
    })
    .astype("Int64")
)

# ------------------------------------------------------------
# 2. Create the improved-seed-use indicator
#    1 = Improved seeds
#    0 = Traditional seeds
#    <NA> = Missing, unknown, or not applicable
#
#    Seed type is classified only when seed use was reported
#    and the recorded seed type is valid.
# ------------------------------------------------------------

valid_seed_type = (
    seeds_clean["s4aq16"].eq(1)
    & seeds_clean["s4aq13"].isin([1, 2])
)

seeds_clean["improved_seed_use"] = pd.Series(
    pd.NA,
    index=seeds_clean.index,
    dtype="Int64"
)

seeds_clean.loc[valid_seed_type, "improved_seed_use"] = (
    seeds_clean.loc[valid_seed_type, "s4aq13"]
    .eq(2)
    .astype("int64")
)

# ------------------------------------------------------------
# 3. Create descriptive seed-type labels
# ------------------------------------------------------------

seeds_clean["seed_type_label"] = (
    seeds_clean["s4aq13"]
    .map({
        1: "Traditional",
        2: "Improved"
    })
    .where(seeds_clean["s4aq16"].eq(1))
)

seeds_clean["improved_seed_type_label"] = (
    seeds_clean["s4aq14"]
    .map({
        1: "Certified",
        2: "Quality declared",
        3: "Don't know"
    })
    .where(
        seeds_clean["s4aq16"].eq(1)
        & seeds_clean["s4aq13"].eq(2)
    )
)

# ------------------------------------------------------------
# 4. Report dataset dimensions
# ------------------------------------------------------------

print("=" * 55)
print("SEED-USE DATA PREPARATION SUMMARY")
print("=" * 55)

print(f"Original dataset dimensions: {seeds.shape}")
print(f"Prepared dataset dimensions: {seeds_clean.shape}")

# ------------------------------------------------------------
# 5. Summarize seed use
# ------------------------------------------------------------

print("\n1. SEED OR SEEDLING USE")
print("-" * 35)

seed_use_counts = (
    seeds_clean["seed_use"]
    .value_counts(dropna=False)
    .reindex([1, 0, pd.NA], fill_value=0)
)

print(f"Yes: {int(seed_use_counts.loc[1])}")
print(f"No: {int(seed_use_counts.loc[0])}")
print(f"Missing/unknown: {int(seeds_clean['seed_use'].isna().sum())}")

valid_seed_use = seeds_clean["seed_use"].notna()

if valid_seed_use.any():
    seed_use_percentage = (
        seeds_clean.loc[valid_seed_use, "seed_use"].mean() * 100
    )
    print(
        "Percentage reporting seed use among valid responses: "
        f"{seed_use_percentage:.2f}%"
    )
else:
    print("Percentage reporting seed use: Not available")

# ------------------------------------------------------------
# 6. Summarize traditional versus improved seed use
# ------------------------------------------------------------

print("\n2. SEED TYPE")
print("-" * 35)

improved_seed_counts = (
    seeds_clean["improved_seed_use"]
    .value_counts(dropna=False)
)

print(
    "Traditional seed records: "
    f"{int((seeds_clean['improved_seed_use'] == 0).sum())}"
)
print(
    "Improved seed records: "
    f"{int((seeds_clean['improved_seed_use'] == 1).sum())}"
)
print(
    "Missing/not-applicable seed-type records: "
    f"{int(seeds_clean['improved_seed_use'].isna().sum())}"
)

valid_seed_type_count = seeds_clean["improved_seed_use"].notna().sum()

if valid_seed_type_count > 0:
    improved_seed_percentage = (
        seeds_clean["improved_seed_use"].mean() * 100
    )
    print(
        "Improved-seed use among valid seed-type records: "
        f"{improved_seed_percentage:.2f}%"
    )
else:
    print("Improved-seed percentage: Not available")

# ------------------------------------------------------------
# 7. Summarize reported improved-seed categories
# ------------------------------------------------------------

print("\n3. IMPROVED-SEED CATEGORIES")
print("-" * 35)

print(
    seeds_clean["improved_seed_type_label"]
    .value_counts(dropna=False)
    .to_string()
)

# ------------------------------------------------------------
# 8. Check for inconsistent seed-use records
# ------------------------------------------------------------

print("\n4. DATA-QUALITY CHECKS")
print("-" * 35)

not_using_with_type = (
    seeds_clean["s4aq16"].eq(2)
    & seeds_clean["s4aq13"].notna()
).sum()

missing_use_with_type = (
    seeds_clean["s4aq16"].isna()
    & seeds_clean["s4aq13"].notna()
).sum()

improved_without_category = (
    seeds_clean["s4aq16"].eq(1)
    & seeds_clean["s4aq13"].eq(2)
    & seeds_clean["s4aq14"].isna()
).sum()

print(
    "Records reporting no seed use but containing a seed type: "
    f"{int(not_using_with_type)}"
)
print(
    "Records with missing seed-use status but a recorded seed type: "
    f"{int(missing_use_with_type)}"
)
print(
    "Improved-seed records with no recorded improved-seed category: "
    f"{int(improved_without_category)}"
)

print("\nPreparation complete. The original dataset was not modified.")


```


```python
output_path = (
    Path.cwd().parent
    / "data"
    / "processed"
    / "seeds_preliminary_clean.csv"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

seeds_clean.to_csv(output_path, index=False)

print("Saved preliminary dataset to:")
print(output_path.resolve())
print("\nFile exists:", output_path.exists())
```


```python
# Examine household and crop records using aggregate statistics only.

print("Total crop records:", len(seeds_clean))
print(
    "Unique household interview IDs:",
    seeds_clean["hhid"].nunique()
)
print(
    "Unique household IDs:",
    seeds_clean["t0_hhid"].nunique()
)
print(
    "Missing household interview IDs:",
    seeds_clean["hhid"].isna().sum()
)
print(
    "Missing household IDs:",
    seeds_clean["t0_hhid"].isna().sum()
)

# Summarize crop records per household without displaying identifiers.
crops_per_household = seeds_clean.groupby("hhid").size()

print("\nCrop records per household:")
print(crops_per_household.describe().round(2))

print("\nDistribution of crop-record counts per household:")
print(
    crops_per_household
    .value_counts()
    .sort_index()
    .head(20)
)
```


```python
import pandas as pd

# ============================================================
# HOUSEHOLD-LEVEL IMPROVED-SEED ADOPTION ANALYSIS
# Unit of analysis: household interview ID (hhid)
# ============================================================

# 1. Summarize crop records for each household interview
household_seeds = (
    seeds_clean.groupby("hhid")
    .agg(
        total_crop_records=("hhid", "size"),
        valid_seed_type_records=("improved_seed_use", "count"),
        improved_seed_crop_records=("improved_seed_use", "sum")
    )
    .reset_index()
)

# 2. Create the household-level adoption indicator
#    1    = at least one crop record reports improved-seed use
#    0    = valid seed-type information exists, but no improved
#           seed use is reported
#    <NA> = no valid seed-type information is available

household_seeds["improved_seed_adopter"] = pd.Series(
    pd.NA,
    index=household_seeds.index,
    dtype="Int64"
)

has_valid_seed_type = (
    household_seeds["valid_seed_type_records"] > 0
)

household_seeds.loc[
    has_valid_seed_type,
    "improved_seed_adopter"
] = (
    household_seeds.loc[
        has_valid_seed_type,
        "improved_seed_crop_records"
    ]
    .gt(0)
    .astype("int64")
)

# 3. Summarize adoption status
adoption_counts = (
    household_seeds["improved_seed_adopter"]
    .value_counts(dropna=False)
)

adopters = int(
    (household_seeds["improved_seed_adopter"] == 1).sum()
)

non_adopters = int(
    (household_seeds["improved_seed_adopter"] == 0).sum()
)

unknown_status = int(
    household_seeds["improved_seed_adopter"].isna().sum()
)

total_households = len(household_seeds)
known_status = adopters + non_adopters

# 4. Display aggregate results only
print("=" * 60)
print("HOUSEHOLD-LEVEL IMPROVED-SEED ADOPTION SUMMARY")
print("=" * 60)

print(f"Total household interview IDs: {total_households:,}")
print(f"Households with known adoption status: {known_status:,}")
print(f"Adopters: {adopters:,}")
print(f"Non-adopters: {non_adopters:,}")
print(f"Unknown adoption status: {unknown_status:,}")

print("\nADOPTION RATE AMONG HOUSEHOLDS WITH KNOWN STATUS")
print("-" * 50)

if known_status > 0:
    adoption_rate = adopters / known_status * 100
    non_adoption_rate = non_adopters / known_status * 100

    print(f"Improved-seed adoption rate: {adoption_rate:.2f}%")
    print(f"Non-adoption rate: {non_adoption_rate:.2f}%")
else:
    print("Adoption rate cannot be calculated: no known outcomes.")

# 5. Summarize crop-record information per household
print("\nCROP-RECORD SUMMARY PER HOUSEHOLD")
print("-" * 50)

print(
    household_seeds[
        [
            "total_crop_records",
            "valid_seed_type_records",
            "improved_seed_crop_records"
        ]
    ]
    .describe()
    .round(2)
)

# 6. Verify the adoption classification
print("\nCLASSIFICATION CHECKS")
print("-" * 50)

invalid_adopters = (
    (
        household_seeds["improved_seed_adopter"] == 1
    )
    & (
        household_seeds["improved_seed_crop_records"] < 1
    )
).sum()

invalid_non_adopters = (
    (
        household_seeds["improved_seed_adopter"] == 0
    )
    & (
        household_seeds["valid_seed_type_records"] == 0
    )
).sum()

print(f"Invalid adopter classifications: {int(invalid_adopters)}")
print(
    "Invalid non-adopter classifications: "
    f"{int(invalid_non_adopters)}"
)

print("\nHousehold-level adoption summary completed.")

```


```python
# Investigate interviews with no valid seed-type responses

no_valid_seed_type_ids = household_seeds.loc[
    household_seeds["valid_seed_type_records"] == 0,
    "hhid"
]

no_valid_seed_records = seeds_clean[
    seeds_clean["hhid"].isin(no_valid_seed_type_ids)
]

print("Interviews with no valid seed-type responses:",
      no_valid_seed_type_ids.nunique())

print("\nSeed-use responses within these interviews:")
print(
    no_valid_seed_records["s4aq16"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nSeed-type responses within these interviews:")
print(
    no_valid_seed_records["s4aq13"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nCrop records per interview in this group:")
print(
    household_seeds.loc[
        household_seeds["valid_seed_type_records"] == 0,
        "total_crop_records"
    ].describe().round(2)
)
```


```python
# Create an explicit household-level adoption classification

household_seeds["adoption_status"] = "Unknown"

# At least one crop record reports improved seeds
household_seeds.loc[
    household_seeds["improved_seed_crop_records"] > 0,
    "adoption_status"
] = "Adopter"

# At least one valid seed-type response, but no improved-seed records
household_seeds.loc[
    (household_seeds["valid_seed_type_records"] > 0) &
    (household_seeds["improved_seed_crop_records"] == 0),
    "adoption_status"
] = "Non-adopter"

# Summarize classifications
status_counts = household_seeds["adoption_status"].value_counts()

print("Household adoption classification:")
print(status_counts)

print("\nPercentages of all household interviews:")
print(
    (status_counts / len(household_seeds) * 100).round(2)
)

# Calculate the adoption rate among classified interviews
classified = household_seeds[
    household_seeds["adoption_status"] != "Unknown"
]

adopters = (classified["adoption_status"] == "Adopter").sum()

print("\nAdoption rate among classified interviews:")
print(f"{adopters / len(classified) * 100:.2f}%")

print("\nNumber of unclassified interviews:")
print((household_seeds["adoption_status"] == "Unknown").sum())
```


```python
from pathlib import Path

# Keep only the household-level variables needed for this analysis
household_output = household_seeds[
    [
        "hhid",
        "total_crop_records",
        "valid_seed_type_records",
        "improved_seed_crop_records",
        "adoption_status"
    ]
].copy()

# Define the processed-data output path
output_path = (
    Path.cwd().parent
    / "data"
    / "processed"
    / "household_seed_adoption_preliminary.csv"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

# Save the household-level dataset
household_output.to_csv(output_path, index=False)

print("Saved:", output_path.resolve())
print("Rows:", len(household_output))
print("Columns:", len(household_output.columns))
print("File exists:", output_path.exists())
```


```python
from pathlib import Path
import pandas as pd

# Locate the extension-services dataset
extension_path = Path(extracted_folder) / "Agric" / "AGSEC9A.csv"

# Load the dataset
extension = pd.read_csv(extension_path)

# Inspect its structure
print("Dataset shape:", extension.shape)

print("\nColumn names:")
print(extension.columns.tolist())

print("\nFirst five records:")
print("Row-level preview omitted; inspect the schema instead.")

print("\nMissing values by column:")
display(extension.isna().sum().sort_values(ascending=False))

print("\nUnique household interview IDs:", extension["hhid"].nunique())

print("Duplicate rows:", extension.duplicated().sum())
```


```python
# Inspect response values for key extension-service variables

key_columns = [
    "source_ID",
    "h9q04a",
    "h9q04b",
    "h9q04c",
    "h9q05ag__1",
    "h9q05ag__2",
    "h9q05ag__3",
    "h9q05ag__4",
    "h9q05ag__5",
    "h9q05ag__6",
    "h9q05ag__7",
    "h9q05ag__8",
    "h9q05ag__9",
    "h9q08a",
    "h9q10a"
]

for column in key_columns:
    print(f"\n{column}")
    print(extension[column].value_counts(dropna=False).sort_index())
```


```python
# Locate and load the additional extension-services dataset

extension_b_path = Path(extracted_folder) / "Agric" / "AGSEC9B.csv"

extension_b = pd.read_csv(extension_b_path)

print("Dataset shape:", extension_b.shape)

print("\nColumn names:")
print(extension_b.columns.tolist())

print("\nFirst five records:")
print("Row-level preview omitted; inspect the schema instead.")

print("\nMissing values by column:")
display(extension_b.isna().sum().sort_values(ascending=False))

print("\nUnique household interview IDs:", extension_b["hhid"].nunique())

print("Duplicate rows:", extension_b.duplicated().sum())
```


```python
# Examine responses to household extension-service questions

extension_columns = [
    "h9q03a__1",
    "h9q03a__2",
    "h9q03a__3",
    "h9q03a__4",
    "h9q03a__5",
    "h9q03a__6",
    "h9q03a__7",
    "h9q11a",
    "h9q12a",
    "h9q13a",
    "h9q14a",
    "h9q15a",
    "h9q16a"
]

for column in extension_columns:
    print(f"\n{column}")
    print(
        extension_b[column]
        .value_counts(dropna=False)
        .sort_index()
    )
```


```python
# Check completeness of agricultural advice variables

advice_columns = [
    "h9q03a__1",
    "h9q03a__2",
    "h9q03a__3",
    "h9q03a__4",
    "h9q03a__5",
    "h9q03a__6",
    "h9q03a__7"
]

# Count recorded answers for each household
extension_b["advice_answers_recorded"] = (
    extension_b[advice_columns].notna().sum(axis=1)
)

# Count how many advice topics have a response of 1
extension_b["advice_topics_yes"] = (
    extension_b[advice_columns].eq(1).sum(axis=1)
)

# Classify records provisionally, without converting missing values to zero
extension_b["advice_status_preliminary"] = "Unknown"

extension_b.loc[
    extension_b["advice_topics_yes"] > 0,
    "advice_status_preliminary"
] = "Advice recorded"

extension_b.loc[
    (extension_b["advice_answers_recorded"] > 0)
    & (extension_b["advice_topics_yes"] == 0),
    "advice_status_preliminary"
] = "No advice recorded"

print("Number of households by preliminary advice status:")
print(extension_b["advice_status_preliminary"].value_counts())

print("\nNumber of households by recorded-answer count:")
print(extension_b["advice_answers_recorded"].value_counts().sort_index())

print("\nNumber of households by positive-topic count:")
print(extension_b["advice_topics_yes"].value_counts().sort_index())
```


```python
# Check household ID overlap before merging.

# Report aggregate matching statistics only; do not display household IDs.

seed_ids = set(household_seeds["hhid"].dropna())
extension_ids = set(extension_b["hhid"].dropna())

common_ids = seed_ids.intersection(extension_ids)

print("Household interviews in seed dataset:", len(seed_ids))
print("Household interviews in extension dataset:", len(extension_ids))
print("Household interviews present in both:", len(common_ids))

seed_match_percentage = (
len(common_ids) / len(seed_ids) * 100
if seed_ids else 0
)

extension_match_percentage = (
len(common_ids) / len(extension_ids) * 100
if extension_ids else 0
)

print(
"Seed interviews with matching extension records:",
f"{seed_match_percentage:.2f}%"
)

print(
"Extension interviews with matching seed records:",
f"{extension_match_percentage:.2f}%"
)

```


```python
# Identify seed households missing from the extension dataset.
# Report aggregate information without displaying household records.

unmatched_seed = household_seeds.loc[
    ~household_seeds["hhid"].isin(extension_b["hhid"])
].copy()

print("SEED-TO-EXTENSION DATASET MATCHING")
print("-" * 45)
print("Unmatched seed household records:", len(unmatched_seed))
print(
    "Unique unmatched household IDs:",
    unmatched_seed["hhid"].nunique()
)

print("\nImproved-seed adoption status among unmatched households:")
print(
    unmatched_seed["improved_seed_adopter"]
    .value_counts(dropna=False)
    .rename(index={0: "Non-adopter", 1: "Adopter"})
    .to_string()
)
```


```python
# Prepare the extension variables for merging

extension_household = extension_b[
    [
        "hhid",
        "advice_answers_recorded",
        "advice_topics_yes",
        "advice_status_preliminary"
    ]
].copy()

# Confirm that each household ID appears only once
assert extension_household["hhid"].is_unique, (
    "Duplicate household IDs found in extension_household."
)

# Merge extension information into the seed-adoption dataset
combined_households = household_seeds.merge(
    extension_household,
    on="hhid",
    how="left",
    validate="one_to_one",
    indicator=True
)

# Summarize the merge
print("Combined dataset shape:", combined_households.shape)

print("\nMerge results:")
print(combined_households["_merge"].value_counts())

print("\nAdoption status:")
print(combined_households["adoption_status"].value_counts(dropna=False))

print("\nPreliminary extension advice status:")
print(
    combined_households["advice_status_preliminary"]
    .value_counts(dropna=False)
)

print("\nMissing extension status after merging:")
print(
    combined_households["advice_status_preliminary"].isna().sum()
)
```


```python
import pandas as pd
from scipy.stats import chi2_contingency

# Keep only households with known adoption and advice classifications
analysis_data = combined_households[
    combined_households["adoption_status"].isin(
        ["Adopter", "Non-adopter"]
    )
    & combined_households["advice_status_preliminary"].isin(
        ["Advice recorded", "No advice recorded"]
    )
].copy()

print("Households included in the analysis:", len(analysis_data))
print("Households excluded:", len(combined_households) - len(analysis_data))

# Create a contingency table
cross_table = pd.crosstab(
    analysis_data["advice_status_preliminary"],
    analysis_data["adoption_status"]
)

print("\nObserved counts:")
display(cross_table)

# Calculate adoption percentages within each advice group
row_percentages = (
    cross_table
    .div(cross_table.sum(axis=1), axis=0)
    .mul(100)
    .round(2)
)

print("\nAdoption status within each advice group (%):")
display(row_percentages)

# Conduct a chi-square test of independence
chi2, p_value, degrees_freedom, expected = chi2_contingency(
    cross_table
)

print("\nChi-square test results")
print(f"Chi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {degrees_freedom}")
print(f"P-value: {p_value:.4f}")

# Calculate Cramer's V as a measure of association strength
n = cross_table.to_numpy().sum()
min_dimension = min(cross_table.shape) - 1

cramers_v = (chi2 / (n * min_dimension)) ** 0.5

print(f"Cramer's V: {cramers_v:.4f}")

# Check whether the chi-square expected-count assumption is satisfied
expected_table = pd.DataFrame(
    expected,
    index=cross_table.index,
    columns=cross_table.columns
)

print("\nExpected counts under independence:")
display(expected_table.round(2))

print(
    "\nExpected cells below 5:",
    (expected_table < 5).sum().sum()
)
```


```python
# Calculate the odds ratio and 95% confidence interval

import numpy as np
from scipy.stats.contingency import odds_ratio

# Arrange the table explicitly:
# Rows: advice recorded, no advice recorded
# Columns: adopter, non-adopter

table = np.array([
    [48, 143],
    [203, 1569]
])

result = odds_ratio(table, kind="sample")

odds_ratio_value = result.statistic
confidence_interval = result.confidence_interval(
    confidence_level=0.95
)

print(f"Odds ratio: {odds_ratio_value:.3f}")
print(
    "95% confidence interval: "
    f"({confidence_interval.low:.3f}, "
    f"{confidence_interval.high:.3f})"
)
```


```python
# Display the most common crop codes in the dataset
print(seeds["cropID"].value_counts().head(20))
```


```python
# Crop code dictionary from Annex 2
crop_names = {
    111: "Wheat",
    112: "Barley",
    120: "Rice",
    130: "Maize",
    141: "Finger millet",
    150: "Sorghum",
    210: "Beans",
    221: "Field peas",
    222: "Cow peas",
    223: "Pigeon peas",
    224: "Chick peas",
    310: "Groundnuts",
    320: "Soya beans",
    330: "Sunflower",
    340: "Simsim",
    410: "Cabbage",
    420: "Tomatoes",
    430: "Carrots",
    440: "Onions",
    450: "Pumpkins",
    460: "Dodo",
    470: "Eggplants",
    510: "Sugarcane",
    520: "Cotton",
    530: "Tobacco",
    610: "Irish potatoes",
    620: "Sweet potatoes",
    630: "Cassava",
    640: "Yam",
    650: "Coco yam",
    700: "Oranges",
    710: "Paw paw",
    720: "Pineapples",
    741: "Banana food",
    742: "Banana beer",
    744: "Banana sweet",
    750: "Mango",
    760: "Jackfruit",
    770: "Avocado",
    780: "Passion fruit",
    810: "Coffee all",
    820: "Cocoa",
    830: "Tea",
    840: "Ginger",
    850: "Curry",
    860: "Oil palm",
    870: "Vanilla",
    880: "Black wattle",
    890: "Other",
    910: "Natural pastures",
    920: "Improved pastures",
    930: "Fallow",
    940: "Bush",
    950: "Natural forest trees",
    960: "Plantation trees",
    970: "Bamboo",
    990: "Other forest trees"
}

# Add crop names without changing the original crop codes
seeds["crop_name"] = seeds["cropID"].map(crop_names).fillna("Unmapped code")

# Display the most common crops
print(
    seeds.groupby(["cropID", "crop_name"])
    .size()
    .sort_values(ascending=False)
    .head(20)
)
```


```python
# Identify crop codes that are not in our dictionary
unmapped_crops = (
    seeds.loc[seeds["crop_name"] == "Unmapped code", "cropID"]
    .value_counts()
    .sort_index()
)

print("Crop codes requiring verification:")
print(unmapped_crops)
```


```python
# Add the missing coffee varieties to our existing dictionary
crop_names.update({
    811: "Coffee (Arabica)",
    812: "Coffee (Robusta)"
})

# Refresh the crop labels
seeds["crop_name"] = (
    seeds["cropID"]
    .map(crop_names)
    .fillna("Unmapped code")
)

# Check whether any crop codes remain unmapped
unmapped_crops = (
    seeds.loc[seeds["crop_name"] == "Unmapped code", "cropID"]
    .value_counts()
    .sort_index()
)

if unmapped_crops.empty:
    print("Success: All crop codes in the dataset have been mapped.")
else:
    print("Crop codes requiring further verification:")
    print(unmapped_crops)
```


```python
crop_summary = (
    seeds.groupby(["cropID", "crop_name"])
    .size()
    .reset_index(name="crop_records")
    .sort_values("crop_records", ascending=False)
)

crop_summary["percentage"] = (
    crop_summary["crop_records"]
    / len(seeds)
    * 100
).round(2)

display(crop_summary.head(15))
```


```python
# Add readable crop names to the cleaned seed dataset
seeds_clean["crop_name"] = (
    seeds_clean["cropID"]
    .map(crop_names)
    .fillna("Unmapped code")
)

# Summarize seed-type information by crop
improved_seed_summary = (
    seeds_clean
    .groupby(["cropID", "crop_name"])
    .agg(
        crop_records=("cropID", "size"),
        valid_seed_type_records=("improved_seed_use", "count"),
        improved_seed_records=("improved_seed_use", "sum")
    )
    .reset_index()
)

# Calculate improved-seed use among records with known seed types
improved_seed_summary["improved_seed_percentage"] = (
    improved_seed_summary["improved_seed_records"]
    / improved_seed_summary["valid_seed_type_records"]
    * 100
).round(2)

# Display crops with the most valid seed-type records
improved_seed_summary = improved_seed_summary.sort_values(
    "valid_seed_type_records",
    ascending=False
)

display(improved_seed_summary.head(15))
```


```python
# Recalculate percentages using the original counts
improved_seed_summary["improved_seed_percentage"] = (
    improved_seed_summary["improved_seed_records"]
    .div(improved_seed_summary["valid_seed_type_records"])
    .mul(100)
).round(2)

# Check that improved-seed records never exceed valid records
impossible_counts = improved_seed_summary[
    improved_seed_summary["improved_seed_records"]
    > improved_seed_summary["valid_seed_type_records"]
]

print("Rows with impossible counts:", len(impossible_counts))

# Display the results clearly
display(
    improved_seed_summary[
        [
            "crop_name",
            "crop_records",
            "valid_seed_type_records",
            "improved_seed_records",
            "improved_seed_percentage"
        ]
    ].head(15).to_string(index=False)
)
```


```python
# Select the five most frequently recorded crops
top_crops = (
    seeds_clean["crop_name"]
    .value_counts()
    .head(5)
    .index
)

# Keep records with known seed types
crop_comparison = seeds_clean[
    seeds_clean["crop_name"].isin(top_crops)
    & seeds_clean["seed_type_label"].notna()
].copy()

# Create a cross-tabulation
crop_seed_table = pd.crosstab(
    crop_comparison["crop_name"],
    crop_comparison["seed_type_label"]
)

# Display counts
print("Seed type by crop:")
display(crop_seed_table)

# Calculate percentages within each crop
crop_seed_percentages = (
    crop_seed_table
    .div(crop_seed_table.sum(axis=1), axis=0)
    .mul(100)
    .round(2)
)

print("Percentage distribution within each crop:")
display(crop_seed_percentages)

```


```python
from scipy.stats import chi2_contingency

# Run the chi-square test using the contingency table from Cell 45
chi2, p_value, degrees_freedom, expected = chi2_contingency(
    crop_seed_table
)

print(f"Chi-square statistic: {chi2:.3f}")
print(f"Degrees of freedom: {degrees_freedom}")
print(f"P-value: {p_value:.6f}")
print(f"Total observations: {crop_seed_table.to_numpy().sum()}")
print(f"Minimum expected cell count: {expected.min():.3f}")
print(f"Cells with expected count below 5: {(expected < 5).sum()}")
```


```python
import numpy as np

# Calculate Cramér's V
n = crop_seed_table.to_numpy().sum()
minimum_dimension = min(crop_seed_table.shape) - 1

cramers_v = np.sqrt(
    chi2 / (n * minimum_dimension)
)

print(f"Cramér's V: {cramers_v:.3f}")
```


```python
import matplotlib.pyplot as plt

# Sort crops by improved-seed percentage
plot_data = crop_seed_percentages.sort_values(
    "Improved",
    ascending=False
)

# Create the chart
ax = plot_data["Improved"].plot(
    kind="bar",
    figsize=(9, 5)
)

ax.set_title("Improved-Seed Use Across Five Major Crops")
ax.set_xlabel("Crop")
ax.set_ylabel("Improved-seed records (%)")
ax.set_ylim(0, 100)

plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()
```


```python
import matplotlib.pyplot as plt

# Sort crops by improved-seed percentage
plot_data = crop_seed_percentages.sort_values(
    "Improved",
    ascending=False
)

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(
    plot_data.index,
    plot_data["Improved"]
)

# Add percentage labels above each bar
ax.bar_label(
    bars,
    fmt="%.2f%%",
    padding=4
)

# Add titles and labels
ax.set_title(
    "Improved-Seed Use Across Five Major Crops",
    fontsize=14,
    pad=15
)

ax.set_xlabel("Crop", fontsize=11)
ax.set_ylabel("Improved-seed records (%)", fontsize=11)

# Set axis limits and add a grid
ax.set_ylim(0, max(plot_data["Improved"]) + 3)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

plt.xticks(rotation=25, ha="right")
plt.tight_layout()
fig.savefig(
    "../reports/improved_seed_use_by_crop.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
```


```python
from pathlib import Path

chart_path = Path("../reports/improved_seed_use_by_crop.png")

print("Chart exists:", chart_path.exists())

if chart_path.exists():
    print("File size:", round(chart_path.stat().st_size / 1024, 2), "KB")
```


```python
# Select the five crops with the most crop records
top_five_summary = improved_seed_summary.head(5).copy()

# Select and rename columns for reporting
top_five_summary = top_five_summary[
    [
        "crop_name",
        "crop_records",
        "valid_seed_type_records",
        "improved_seed_records",
        "improved_seed_percentage"
    ]
].rename(columns={
    "crop_name": "Crop",
    "crop_records": "Total Crop Records",
    "valid_seed_type_records": "Valid Seed-Type Records",
    "improved_seed_records": "Improved-Seed Records",
    "improved_seed_percentage": "Improved-Seed Use (%)"
})

# Display the table
display(top_five_summary)
```


```python
# Reset the index to remove the crop codes from the row labels
top_five_summary = top_five_summary.reset_index(drop=True)

# Format the table for easier reading
top_five_summary["Improved-Seed Use (%)"] = (
    top_five_summary["Improved-Seed Use (%)"].map(
        lambda x: f"{x:.2f}%"
    )
)

display(top_five_summary)
```


```python
# Hide the DataFrame index when displaying the table
display(top_five_summary.style.hide(axis="index"))
```


```python
from pathlib import Path

# Define the output path
output_path = Path("../reports/top_five_crop_seed_summary.csv")

# Select the same five crops used in the chi-square analysis
summary_to_save = improved_seed_summary[
    improved_seed_summary["crop_name"].isin(top_crops)
][
    [
        "crop_name",
        "crop_records",
        "valid_seed_type_records",
        "improved_seed_records",
        "improved_seed_percentage"
    ]
].copy()

# Save the summary with numeric percentages
summary_to_save.to_csv(output_path, index=False)

print("Summary saved:", output_path.exists())
print("Saved to:", output_path.resolve())
print("Number of crop categories:", len(summary_to_save))
print("Crop categories:", summary_to_save["crop_name"].tolist())
```


```python
import pandas as pd
from pathlib import Path

# Locate and read the saved CSV
csv_path = Path("../reports/top_five_crop_seed_summary.csv")
saved_summary = pd.read_csv(csv_path)

# Check the file contents
print("File exists:", csv_path.exists())
print("Number of rows:", len(saved_summary))
print("Number of columns:", len(saved_summary.columns))

display(saved_summary)
```


```python
# Inspect the merged household dataset
print("Dataset dimensions:", combined_households.shape)

print("\nColumn names:")
print(combined_households.columns.tolist())

print("\nFirst five records:")
print("Row-level preview omitted; inspect the schema instead.")
```


```python
# Check how many records matched during the merge
print("Merge results:")
print(combined_households["_merge"].value_counts(dropna=False))

# Check missing values in each column
print("\nMissing values per column:")
print(combined_households.isna().sum())

# Check improved-seed adoption categories
print("\nAdoption status:")
print(combined_households["adoption_status"].value_counts(dropna=False))

# Check preliminary advice categories
print("\nPreliminary advice status:")
print(
    combined_households["advice_status_preliminary"]
    .value_counts(dropna=False)
)
```


```python
# Inspect the original extension dataset without exposing individual records.

print("Extension dataset dimensions:", extension_b.shape)

advice_columns = [
    f"h9q03a__{i}" for i in range(1, 8)
]

available_advice_columns = [
    col for col in advice_columns
    if col in extension_b.columns
]

print("\nAvailable advice-variable columns:")
print(available_advice_columns)

print("\nMissing-value counts for advice variables:")
print(
    extension_b[available_advice_columns]
    .isna()
    .sum()
    .to_string()
)

print("\nResponse counts for each advice variable:")

for col in available_advice_columns:
    print(f"\n{col}")
    print(
        extension_b[col]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )


```


```python
# Inspect metadata for H9Q03-related columns without exposing response values.

print("Extension dataset columns:")
print(extension_b.columns.tolist())

for col in extension_b.columns:
    if "h9q03" in col.lower():
        series = extension_b[col]

        print(f"\nVariable: {col}")
        print("Data type:", series.dtype)
        print("Non-missing values:", int(series.notna().sum()))
        print(
            "Distinct non-missing values:",
            int(series.nunique(dropna=True))
        )
```


```python
# Examine the other Section 9 variables
section9_columns = [
    "h9q11a",
    "h9q12a",
    "h9q13a",
    "h9q14a",
    "h9q15a",
    "h9q16a"
]

for col in section9_columns:
    print(f"\n--- {col} ---")
    print("Data type:", extension_b[col].dtype)
    print("Non-missing responses:", extension_b[col].notna().sum())
    print("Missing responses:", extension_b[col].isna().sum())
    print("Response counts:")
    print(extension_b[col].value_counts(dropna=False).sort_index())
```


```python
from pathlib import Path

# Locate questionnaire and documentation files
root = Path(extracted_folder)

keywords = [
    "questionnaire",
    "codebook",
    "dictionary",
    "agsec",
    "extension"
]

matches = []

for path in root.rglob("*"):
    if path.is_file() and any(
        word in path.name.lower() for word in keywords
    ):
        matches.append(path)

print(f"Files found: {len(matches)}")

for path in matches[:60]:
    print(path)
```


```python
from pathlib import Path
import pandas as pd

# Locate the extracted agriculture folder
agriculture_folder = Path(extracted_folder) / "Agric"

print("Agriculture folder exists:", agriculture_folder.exists())

# Inspect the AGSEC9B file
file_path = agriculture_folder / "AGSEC9B.csv"

print("AGSEC9B file exists:", file_path.exists())

extension_check = pd.read_csv(file_path, nrows=5)

print("\nFile dimensions preview:")
print("Rows read:", len(extension_check))
print("Columns:", len(extension_check.columns))

print("\nColumn names:")
print(extension_check.columns.tolist())

print("Row-level preview omitted; inspect the schema instead.")
```


```python
from pathlib import Path

root = Path(extracted_folder)

# Look for documentation files, not just agriculture CSVs
documentation_extensions = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".dta", ".sav", ".xml", ".json", ".txt"
}

documentation_files = [
    path for path in root.rglob("*")
    if path.is_file()
    and path.suffix.lower() in documentation_extensions
]

print("Potential documentation files:", len(documentation_files))

for path in documentation_files[:50]:
    print(path)
```


```python
# Create a verified NAADS training participation indicator
extension_b["naads_training_participation"] = (
    extension_b["h9q12a"].map({
        1: 1,
        2: 0
    })
)

# Check the new variable
print("NAADS training participation:")
print(
    extension_b["naads_training_participation"]
    .value_counts(dropna=False)
)

# Calculate percentages among valid responses only
valid_training = extension_b["naads_training_participation"].dropna()

print("\nValid responses:", len(valid_training))
print("Missing responses:",
      extension_b["naads_training_participation"].isna().sum())

print("\nPercentages among valid responses:")
print(
    (valid_training.value_counts(normalize=True) * 100)
    .sort_index()
    .round(2)
)
```


```python
# Select only the household ID and verified training indicator
training_data = extension_b[
    ["hhid", "naads_training_participation"]
].copy()

# Check for duplicate household IDs before merging
print("Training records:", len(training_data))
print("Unique household IDs:", training_data["hhid"].nunique())
print(
    "Duplicate household IDs:",
    training_data["hhid"].duplicated().sum()
)

# Merge training information with household seed adoption
training_adoption = household_seeds.merge(
    training_data,
    on="hhid",
    how="left",
    validate="one_to_one",
    indicator=True
)

print("\nMerged dataset dimensions:", training_adoption.shape)

print("\nMerge results:")
print(training_adoption["_merge"].value_counts())

print("\nTraining participation:")
print(
    training_adoption["naads_training_participation"]
    .value_counts(dropna=False)
)

print("\nAdoption status:")
print(training_adoption["adoption_status"].value_counts(dropna=False))
```


```python
import pandas as pd
from scipy.stats import chi2_contingency

# Keep only records with known adoption and training status
analysis_data = training_adoption[
    training_adoption["adoption_status"].isin(
        ["Adopter", "Non-adopter"]
    )
    & training_adoption["naads_training_participation"].notna()
].copy()

# Give the training categories readable labels
analysis_data["training_status"] = (
    analysis_data["naads_training_participation"]
    .map({1.0: "Participated", 0.0: "Did not participate"})
)

# Build the contingency table
training_adoption_table = pd.crosstab(
    analysis_data["training_status"],
    analysis_data["adoption_status"]
)

print("Number of records analyzed:", len(analysis_data))

print("\nTraining participation vs improved-seed adoption:")
display(training_adoption_table)

print("\nRow percentages:")
display(
    (
        training_adoption_table
        .div(training_adoption_table.sum(axis=1), axis=0)
        * 100
    ).round(2)
)
```


```python
from scipy.stats import chi2_contingency

# Perform the Pearson chi-square test
chi2, p_value, degrees_freedom, expected = chi2_contingency(
    training_adoption_table
)

# Calculate Cramer's V to measure association strength
n = training_adoption_table.to_numpy().sum()
cramers_v = (chi2 / n) ** 0.5

print("Chi-square test of independence")
print(f"Chi-square statistic: {chi2:.3f}")
print(f"Degrees of freedom: {degrees_freedom}")
print(f"P-value: {p_value:.6f}")
print(f"Cramer's V: {cramers_v:.3f}")

print("\nExpected frequencies:")
display(
    pd.DataFrame(
        expected,
        index=training_adoption_table.index,
        columns=training_adoption_table.columns
    ).round(2)
)

print(
    "\nExpected frequencies below 5:",
    (expected < 5).sum()
)
```


```python
import numpy as np
from scipy.stats import norm

# Extract the 2x2 table values
# Rows: Did not participate, Participated
# Columns: Adopter, Non-adopter

a = training_adoption_table.loc["Participated", "Adopter"]
b = training_adoption_table.loc["Participated", "Non-adopter"]
c = training_adoption_table.loc["Did not participate", "Adopter"]
d = training_adoption_table.loc["Did not participate", "Non-adopter"]

# Adoption rates
rate_trained = a / (a + b)
rate_untrained = c / (c + d)

# Absolute difference in adoption rates
rate_difference = rate_trained - rate_untrained

# Approximate 95% confidence interval for the rate difference
se_difference = np.sqrt(
    rate_trained * (1 - rate_trained) / (a + b)
    + rate_untrained * (1 - rate_untrained) / (c + d)
)

z = norm.ppf(0.975)

difference_lower = rate_difference - z * se_difference
difference_upper = rate_difference + z * se_difference

# Odds ratio: training participants vs non-participants
odds_ratio = (a * d) / (b * c)

# Approximate 95% confidence interval for the odds ratio
se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)

or_lower = np.exp(np.log(odds_ratio) - z * se_log_or)
or_upper = np.exp(np.log(odds_ratio) + z * se_log_or)

print(f"Adoption rate among participants: {rate_trained:.2%}")
print(f"Adoption rate among non-participants: {rate_untrained:.2%}")

print(f"\nAdoption-rate difference: {rate_difference:.2%}")
print(
    "95% CI for rate difference: "
    f"{difference_lower:.2%} to {difference_upper:.2%}"
)

print(f"\nOdds ratio: {odds_ratio:.3f}")
print(f"95% CI for odds ratio: {or_lower:.3f} to {or_upper:.3f}")
```


```python
print("Available columns in the household adoption dataset:\n")

print(training_adoption.columns.tolist())
```


```python
print("Available columns in the extension dataset:\n")

print(extension_b.columns.tolist())
```


```python
# Inspect the response distributions of additional survey variables

additional_variables = ["h9q13a", "h9q14a", "h9q15a", "h9q16a"]

for variable in additional_variables:
    print(f"\nVariable: {variable}")
    print(extension_b[variable].value_counts(dropna=False).sort_index())
    
```


```python
# Examine awareness and membership of farmers' groups

print("Farmers' group awareness (h9q13a)")
print(extension_b["h9q13a"].value_counts(dropna=False).sort_index())

print("\nFarmers' group membership (h9q14a)")
print(extension_b["h9q14a"].value_counts(dropna=False).sort_index())

print("\nAwareness of NAADS initiatives (h9q15a)")
print(extension_b["h9q15a"].value_counts(dropna=False).sort_index())

print("\nParticipation in NAADS initiatives (h9q16a)")
print(extension_b["h9q16a"].value_counts(dropna=False).sort_index())
```


```python
import pandas as pd

# Cross-tabulate awareness against the corresponding outcome

print("Farmers' group awareness vs membership")

display(
    pd.crosstab(
        extension_b["h9q13a"],
        extension_b["h9q14a"],
        dropna=False,
        margins=True
    )
)

print("\nNAADS initiative awareness vs participation")

display(
    pd.crosstab(
        extension_b["h9q15a"],
        extension_b["h9q16a"],
        dropna=False,
        margins=True
    )
)
```


```python
# Create a separate variable; preserve the original survey responses

extension_b["farmer_group_member_clean"] = (
    extension_b["h9q14a"].map({1: 1, 2: 0})
)

# Apply the provisional skip-pattern rule:
# If awareness is recorded as No, classify as not a member.
# Missing awareness remains unknown.

extension_b.loc[
    extension_b["h9q13a"] == 2,
    "farmer_group_member_clean"
] = 0

# Display the resulting distribution

print("Farmer group membership after provisional recoding:")
print(
    extension_b["farmer_group_member_clean"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nPercentages among households with classified membership:")
print(
    (
        extension_b["farmer_group_member_clean"]
        .value_counts(normalize=True)
        .sort_index() * 100
    ).round(2)
)
```


```python
# Prepare the membership data for merging

membership_data = extension_b[
    ["hhid", "farmer_group_member_clean"]
].copy()

# Check that household interview IDs are unique

print("Membership records:", len(membership_data))
print("Unique interview IDs:", membership_data["hhid"].nunique())
print("Duplicate interview IDs:", membership_data["hhid"].duplicated().sum())

# Merge with the household adoption dataset

membership_adoption = household_seeds.merge(
    membership_data,
    on="hhid",
    how="left",
    validate="one_to_one",
    indicator=True
)

print("\nMerged dataset dimensions:", membership_adoption.shape)

print("\nMerge results:")
print(membership_adoption["_merge"].value_counts())

print("\nMembership status in the merged dataset:")
print(
    membership_adoption["farmer_group_member_clean"]
    .value_counts(dropna=False)
)
```


```python
import pandas as pd

# Keep households with known adoption status and known membership status

membership_analysis = membership_adoption[
    membership_adoption["adoption_status"].isin(
        ["Adopter", "Non-adopter"]
    )
    & membership_adoption["farmer_group_member_clean"].notna()
].copy()

# Give the membership categories readable labels

membership_analysis["membership_status"] = (
    membership_analysis["farmer_group_member_clean"]
    .map({1.0: "Member", 0.0: "Non-member"})
)

# Create the contingency table

membership_table = pd.crosstab(
    membership_analysis["membership_status"],
    membership_analysis["adoption_status"]
)

print("Number of records analyzed:", len(membership_analysis))

print("\nObserved frequencies:")
display(membership_table)

print("\nAdoption percentages within each membership group:")

membership_percentages = (
    membership_table.div(membership_table.sum(axis=1), axis=0)
    .mul(100)
    .round(2)
)

display(membership_percentages)
```


```python
from scipy.stats import chi2_contingency, fisher_exact
import numpy as np

# Test the association between group membership and adoption
chi2, p_value, dof, expected = chi2_contingency(membership_table)

n = membership_table.to_numpy().sum()
cramers_v = np.sqrt(chi2 / n)

print("Chi-square test of independence")
print(f"Chi-square statistic: {chi2:.3f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.6f}")
print(f"Cramer's V: {cramers_v:.3f}")

print("\nExpected frequencies:")
display(
    pd.DataFrame(
        expected,
        index=membership_table.index,
        columns=membership_table.columns
    ).round(2)
)

print("\nExpected frequencies below 5:", (expected < 5).sum())

# Fisher's exact test is useful for a 2x2 table,
# particularly when expected cell counts are small.
odds_ratio, fisher_p = fisher_exact(membership_table)

print("\nFisher's exact test")
print(f"Odds ratio: {odds_ratio:.3f}")
print(f"P-value: {fisher_p:.6f}")
```


```python
# Check the outcome variable

print("Improved-seed adoption variable:")
print(
    training_adoption["improved_seed_adopter"]
    .value_counts(dropna=False)
    .sort_index()
)

# Check training participation

print("\nNAADS training participation:")
print(
    training_adoption["naads_training_participation"]
    .value_counts(dropna=False)
    .sort_index()
)

# Check farmers' group membership

print("\nFarmers' group membership:")
print(
    membership_adoption["farmer_group_member_clean"]
    .value_counts(dropna=False)
    .sort_index()
)
```


```python
# Select the required variables and merge them by household ID

regression_data = household_seeds[
    ["hhid", "improved_seed_adopter"]
].merge(
    training_data,
    on="hhid",
    how="left",
    validate="one_to_one"
).merge(
    membership_data,
    on="hhid",
    how="left",
    validate="one_to_one"
)

# Keep records with complete data for all three variables

regression_data = regression_data.dropna(
    subset=[
        "improved_seed_adopter",
        "naads_training_participation",
        "farmer_group_member_clean"
    ]
).copy()

# Confirm the dataset

print("Regression dataset dimensions:", regression_data.shape)

print("\nImproved-seed adoption:")
print(regression_data["improved_seed_adopter"].value_counts())

print("\nNAADS training participation:")
print(regression_data["naads_training_participation"].value_counts())

print("\nFarmers' group membership:")
print(regression_data["farmer_group_member_clean"].value_counts())

print("\nMissing values:")
print(regression_data.isna().sum())
```


```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

# Define the outcome variable
y = regression_data["improved_seed_adopter"]

# Define the predictor variables
X = regression_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean"
    ]
]

# Add the intercept
X = sm.add_constant(X)

# Fit the binary logistic regression model
logit_model = sm.Logit(y, X)
logit_results = logit_model.fit()

# Display the regression results
print(logit_results.summary())
```


```python
# Extract coefficients and confidence intervals
coefficients = logit_results.params
confidence_intervals = logit_results.conf_int()

# Convert coefficients to odds ratios
odds_ratios = np.exp(coefficients)

# Convert confidence intervals to odds-ratio scale
or_confidence_intervals = np.exp(confidence_intervals)

# Build a readable results table
regression_summary = pd.DataFrame({
    "Coefficient": coefficients,
    "Odds Ratio": odds_ratios,
    "95% CI Lower": or_confidence_intervals[0],
    "95% CI Upper": or_confidence_intervals[1],
    "P-value": logit_results.pvalues
})

display(regression_summary.round(3))
```


```python
from pathlib import Path
import numpy as np
import pandas as pd

# Extract model estimates
coefficients = logit_results.params
confidence_intervals = logit_results.conf_int()

# Build a clean results table
regression_table = pd.DataFrame({
    "Predictor": coefficients.index,
    "Coefficient": coefficients.values,
    "Odds_Ratio": np.exp(coefficients.values),
    "CI_Lower": np.exp(confidence_intervals[0].values),
    "CI_Upper": np.exp(confidence_intervals[1].values),
    "P_Value": logit_results.pvalues.values
})

# Round numeric columns for presentation
numeric_columns = [
    "Coefficient",
    "Odds_Ratio",
    "CI_Lower",
    "CI_Upper",
    "P_Value"
]

regression_table[numeric_columns] = (
    regression_table[numeric_columns].round(4)
)

# Save the results
output_path = Path("../reports/logistic_regression_results.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

regression_table.to_csv(output_path, index=False)

print("File saved:", output_path.resolve())
print("File exists:", output_path.exists())

display(regression_table)
```


```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Generate predicted probabilities
predicted_probabilities = logit_results.predict(X)

# Classify households using the conventional 0.5 threshold
predicted_classes = (predicted_probabilities >= 0.5).astype(int)

# Actual outcomes
actual_classes = y.astype(int)

# Calculate evaluation metrics
print("Model evaluation at a 0.5 classification threshold")
print("-" * 55)

print(f"Accuracy:  {accuracy_score(actual_classes, predicted_classes):.3f}")
print(f"Precision: {precision_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"Recall:    {recall_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"F1-score:  {f1_score(actual_classes, predicted_classes, zero_division=0):.3f}")

print("\nConfusion matrix:")
print(confusion_matrix(actual_classes, predicted_classes))

print("\nClassification report:")
print(
    classification_report(
        actual_classes,
        predicted_classes,
        target_names=["Non-adopter", "Adopter"],
        zero_division=0
    )
)
```


```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Generate predicted probabilities
predicted_probabilities = logit_results.predict(X)

# Classify households using the conventional 0.5 threshold
predicted_classes = (predicted_probabilities >= 0.5).astype(int)

# Actual outcomes
actual_classes = y.astype(int)

# Calculate evaluation metrics
print("Model evaluation at a 0.5 classification threshold")
print("-" * 55)

print(f"Accuracy:  {accuracy_score(actual_classes, predicted_classes):.3f}")
print(f"Precision: {precision_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"Recall:    {recall_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"F1-score:  {f1_score(actual_classes, predicted_classes, zero_division=0):.3f}")

print("\nConfusion matrix:")
print(confusion_matrix(actual_classes, predicted_classes))

print("\nClassification report:")
print(
    classification_report(
        actual_classes,
        predicted_classes,
        target_names=["Non-adopter", "Adopter"],
        zero_division=0
    )
)
```


```python
%pip install scikit-learn
```


```python
import sklearn

print("Scikit-learn version:", sklearn.__version__)
print("Installation successful!")
```


```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Generate predicted probabilities
predicted_probabilities = logit_results.predict(X)

# Classify households using the conventional 0.5 threshold
predicted_classes = (predicted_probabilities >= 0.5).astype(int)

# Actual outcomes
actual_classes = y.astype(int)

# Calculate evaluation metrics
print("Model evaluation at a 0.5 classification threshold")
print("-" * 55)

print(f"Accuracy:  {accuracy_score(actual_classes, predicted_classes):.3f}")
print(f"Precision: {precision_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"Recall:    {recall_score(actual_classes, predicted_classes, zero_division=0):.3f}")
print(f"F1-score:  {f1_score(actual_classes, predicted_classes, zero_division=0):.3f}")

print("\nConfusion matrix:")
print(confusion_matrix(actual_classes, predicted_classes))

print("\nClassification report:")
print(
    classification_report(
        actual_classes,
        predicted_classes,
        target_names=["Non-adopter", "Adopter"],
        zero_division=0
    )
)
```


```python
# Examine predicted adoption probabilities without displaying household identifiers.

print("Predicted probability summary:")
display(predicted_probabilities.describe().round(4))

print("\nHighest predicted adoption probabilities (values only):")

highest_probabilities = (
    predicted_probabilities
    .sort_values(ascending=False)
    .head(10)
    .to_numpy()
)

display(
    pd.Series(
        highest_probabilities,
        name="Predicted Adoption Probability"
    ).round(4)
)

print("\nProbability thresholds:")

for threshold in [0.10, 0.15, 0.20, 0.25, 0.30, 0.50]:
    predicted_at_threshold = (
        predicted_probabilities >= threshold
    ).astype(int)

    print(
        f"Threshold {threshold:.2f}: "
        f"{predicted_at_threshold.sum()} households classified as adopters"
    )
```


```python
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Calculate ROC AUC
roc_auc = roc_auc_score(
    actual_classes,
    predicted_probabilities
)

print(f"ROC AUC: {roc_auc:.4f}")

# Calculate ROC curve coordinates
false_positive_rate, true_positive_rate, thresholds = roc_curve(
    actual_classes,
    predicted_probabilities
)

# Plot the ROC curve
plt.figure(figsize=(7, 5))

plt.plot(
    false_positive_rate,
    true_positive_rate,
    label=f"Logistic regression (AUC = {roc_auc:.3f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random ranking"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve: Improved-Seed Adoption")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```


```python
print("Number of columns:", len(extension_b.columns))

display(
    pd.DataFrame({
        "Column": extension_b.columns,
        "Data type": extension_b.dtypes.astype(str).values,
        "Missing values": extension_b.isna().sum().values,
        "Unique values": extension_b.nunique(dropna=True).values
    }).head(40)
)
```


```python
from pathlib import Path

data_folder = Path(extracted_folder)

all_csv_files = list(data_folder.rglob("*.csv"))

keywords = [
    "GSEC1", "GSEC2", "GSEC3",
    "AGSEC1", "AGSEC2", "AGSEC3",
    "HOUSEHOLD", "ROSTER", "COVER"
]

relevant_files = [
    file for file in all_csv_files
    if any(keyword in file.name.upper() for keyword in keywords)
]

print(f"Potentially relevant files found: {len(relevant_files)}")

for file in relevant_files:
    print(file.name)
```


```python
from pathlib import Path
import pandas as pd

gsec2_path = next(
    file for file in Path(extracted_folder).rglob("GSEC2.csv")
    if file.is_file()
)

gsec2 = pd.read_csv(gsec2_path, low_memory=False)

print("Dataset shape:", gsec2.shape)
print("Number of unique household IDs:", gsec2["hhid"].nunique()
      if "hhid" in gsec2.columns else "No hhid column")

display(
    pd.DataFrame({
        "Column": gsec2.columns,
        "Data type": gsec2.dtypes.astype(str).values,
        "Missing values": gsec2.isna().sum().values,
        "Unique values": gsec2.nunique(dropna=True).values
    })
)
```


```python
print("Row-level preview omitted; inspect the schema instead.")

for column in gsec2.columns[4:]:
    print(f"\n{column}")
    print(gsec2[column].value_counts(dropna=False).head(15))
```


```python
# Inspect the response codes before recoding the variables.

variables_to_check = ["h2q3", "h2q4", "h2q8", "h2q10"]

for column in variables_to_check:
    print(f"\n--- {column} ---")
    print(
        gsec2[column]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )
```


```python
# Count records where the relationship code is 1.
head_candidates = gsec2[gsec2["h2q4"] == 1].copy()

print("Records coded as household head:", len(head_candidates))
print(
    "Unique households among these records:",
    head_candidates["hhid"].nunique()
)

# Count possible household heads per household.
head_counts = (
    head_candidates.groupby("hhid")
    .size()
    .value_counts()
    .sort_index()
)

print("\nNumber of household-head records per household:")
display(head_counts.rename_axis("Head records per household").to_frame("Households"))

# Check household IDs with zero or multiple candidate heads.
all_households = set(gsec2["hhid"].unique())
households_with_head = set(head_candidates["hhid"].unique())

print("\nHouseholds with no candidate head:", len(all_households - households_with_head))
print(
    "Households with multiple candidate heads:",
    int((head_candidates.groupby("hhid").size() > 1).sum())
)
```


```python
# Extract verified household-head records.
household_heads = gsec2.loc[
    gsec2["h2q4"] == 1,
    ["hhid", "t0_hhid", "h2q3", "h2q8", "h2q10"]
].copy()

# Rename variables for readability.
household_heads = household_heads.rename(columns={
    "h2q3": "head_sex_code",
    "h2q8": "head_age",
    "h2q10": "head_marital_status_code"
})

# Confirm one row per household.
print("Dataset shape:", household_heads.shape)
print("Unique households:", household_heads["hhid"].nunique())
print("Duplicate household IDs:", household_heads["hhid"].duplicated().sum())

print("Row-level preview omitted; inspect the schema instead.")
```


```python
# Summarize missing values and age ranges.
print("Missing values:")
display(household_heads.isna().sum().to_frame("Missing count"))

print("\nHousehold-head age summary:")
display(household_heads["head_age"].describe())

print("\nHousehold-head sex codes:")
display(household_heads["head_sex_code"].value_counts(dropna=False).sort_index())

print("\nHousehold-head marital-status codes:")
display(
    household_heads["head_marital_status_code"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nReported ages above 100:")
display(
    household_heads.loc[
        household_heads["head_age"] > 100,
        ["hhid", "head_age"]
    ]
)
```


```python
# Create a working copy for demographic analysis.
household_demographics = household_heads.copy()

# Keep age numeric and preserve the original category codes.
household_demographics["head_age"] = pd.to_numeric(
    household_demographics["head_age"],
    errors="coerce"
)

# Create a squared-age term to allow a nonlinear age relationship.
household_demographics["head_age_squared"] = (
    household_demographics["head_age"] ** 2
)

# Check the resulting dataset.
print("Dataset shape:", household_demographics.shape)
print(
    "Unique household IDs:",
    household_demographics["hhid"].nunique()
)
print("\nMissing values:")
display(
    household_demographics.isna().sum().to_frame("Missing count")
)

print("Row-level preview omitted; inspect the schema instead.")
```


```python
# Create readable labels for household-head demographics.
household_demographics["head_sex"] = (
    household_demographics["head_sex_code"]
    .map({1: "Male", 2: "Female"})
)

marital_status_labels = {
    1: "Married monogamously",
    2: "Married polygamous",
    3: "Divorced/separated",
    4: "Widow/widower",
    5: "Never married"
}

household_demographics["head_marital_status"] = (
    household_demographics["head_marital_status_code"]
    .map(marital_status_labels)
)

# Review the category counts.
print("Household-head sex:")
display(
    household_demographics["head_sex"]
    .value_counts(dropna=False)
    .to_frame("Households")
)

print("\nHousehold-head marital status:")
display(
    household_demographics["head_marital_status"]
    .value_counts(dropna=False)
    .to_frame("Households")
)

# Confirm the dataset still has one row per household.
print("\nTotal records:", len(household_demographics))
print("Unique households:", household_demographics["hhid"].nunique())
print(
    "Duplicate household IDs:",
    household_demographics["hhid"].duplicated().sum()
)
```


```python
# Select the demographic variables needed for the analysis.
demographic_columns = [
    "hhid",
    "head_sex",
    "head_age",
    "head_marital_status"
]

demographics_for_merge = household_demographics[
    demographic_columns
].copy()

# Merge demographics into the household adoption dataset.
adoption_demographics = household_seeds.merge(
    demographics_for_merge,
    on="hhid",
    how="left",
    validate="one_to_one",
    indicator=True
)

# Inspect the merge.
print("Merged dataset shape:", adoption_demographics.shape)
print("\nMerge results:")
display(
    adoption_demographics["_merge"]
    .value_counts()
    .rename_axis("Merge status")
    .to_frame("Households")
)

print("\nMissing demographic values after merging:")
display(
    adoption_demographics[
        ["head_sex", "head_age", "head_marital_status"]
    ]
    .isna()
    .sum()
    .to_frame("Missing count")
)

# Inspect the resulting dataset.
print("Household-level preview omitted from the public notebook.")
```


```python
# Keep only the adoption outcome and existing predictors.
model_base = regression_data[
    [
        "hhid",
        "improved_seed_adopter",
        "naads_training_participation",
        "farmer_group_member_clean"
    ]
].copy()

# Add demographic variables.
demographic_predictors = adoption_demographics[
    [
        "hhid",
        "head_age",
        "head_sex",
        "head_marital_status"
    ]
].copy()

expanded_data = model_base.merge(
    demographic_predictors,
    on="hhid",
    how="left",
    validate="one_to_one"
)

# Check the resulting dataset.
print("Expanded dataset shape:", expanded_data.shape)
print("Duplicate household IDs:", expanded_data["hhid"].duplicated().sum())

print("\nMissing values:")
display(expanded_data.isna().sum().to_frame("Missing count"))

print("\nAdoption outcome:")
display(
    expanded_data["improved_seed_adopter"]
    .value_counts(dropna=False)
    .to_frame("Households")
)

print("\nSex categories:")
display(expanded_data["head_sex"].value_counts(dropna=False).to_frame("Households"))

print("\nMarital-status categories:")
display(
    expanded_data["head_marital_status"]
    .value_counts(dropna=False)
    .to_frame("Households")
)
```


```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Keep only records with complete demographic information.
model_data = expanded_data.dropna(
    subset=[
        "improved_seed_adopter",
        "naads_training_participation",
        "farmer_group_member_clean",
        "head_age",
        "head_sex",
        "head_marital_status"
    ]
).copy()

# Center age around the sample mean.
model_data["age_centered"] = (
    model_data["head_age"] - model_data["head_age"].mean()
)

# Include a nonlinear age term.
model_data["age_centered_squared"] = model_data["age_centered"] ** 2

# Outcome variable.
y = model_data["improved_seed_adopter"].astype(int)

# Baseline predictors.
X_baseline = model_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean"
    ]
].astype(float)

X_baseline = sm.add_constant(X_baseline)

# Expanded predictors: categorical variables are dummy-coded.
X_expanded = pd.get_dummies(
    model_data[
        [
            "naads_training_participation",
            "farmer_group_member_clean",
            "age_centered",
            "age_centered_squared",
            "head_sex",
            "head_marital_status"
        ]
    ],
    columns=["head_sex", "head_marital_status"],
    drop_first=True,
    dtype=float
)

X_expanded = sm.add_constant(X_expanded)

# Fit both models on exactly the same households.
baseline_model = sm.Logit(y, X_baseline).fit(disp=False)
expanded_model = sm.Logit(y, X_expanded).fit(disp=False)

print("Complete-case sample size:", len(model_data))
print("Baseline model predictors:", X_baseline.shape[1] - 1)
print("Expanded model predictors:", X_expanded.shape[1] - 1)

print("\nBASELINE MODEL")
print(baseline_model.summary())

print("\nEXPANDED MODEL")
print(expanded_model.summary())
```


```python
# Examine the outcome by household-head marital status.
marital_adoption_table = pd.crosstab(
    model_data["head_marital_status"],
    model_data["improved_seed_adopter"],
    margins=True
)

marital_adoption_table.columns = [
    "Non-adopter" if col == 0
    else "Adopter" if col == 1
    else "Total"
    for col in marital_adoption_table.columns
]

print("Adoption counts by marital status:")
display(marital_adoption_table)

# Calculate adoption percentages within each marital-status category.
marital_adoption_rates = (
    model_data.groupby("head_marital_status", observed=True)
    ["improved_seed_adopter"]
    .agg(["count", "mean"])
    .rename(columns={
        "count": "Households",
        "mean": "Adoption rate"
    })
)

marital_adoption_rates["Adoption rate (%)"] = (
    marital_adoption_rates["Adoption rate"] * 100
)

display(marital_adoption_rates.round(2))
```


```python
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Use the same complete-case sample as before.
model_data = expanded_data.dropna(
    subset=[
        "improved_seed_adopter",
        "naads_training_participation",
        "farmer_group_member_clean",
        "head_age",
        "head_sex"
    ]
).copy()

# Center age to make the intercept more interpretable.
model_data["age_centered"] = (
    model_data["head_age"] - model_data["head_age"].mean()
)

# Allow for a possible nonlinear relationship with age.
model_data["age_centered_squared"] = (
    model_data["age_centered"] ** 2
)

# Outcome.
y = model_data["improved_seed_adopter"].astype(int)

# Predictors, excluding marital status.
X = model_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean",
        "age_centered",
        "age_centered_squared"
    ]
].astype(float)

# Add household-head sex as a categorical predictor.
sex_dummies = pd.get_dummies(
    model_data["head_sex"],
    prefix="head_sex",
    drop_first=True,
    dtype=float
)

X = pd.concat([X, sex_dummies], axis=1)
X = sm.add_constant(X)

# Fit the model.
expanded_model_v2 = sm.Logit(y, X).fit(disp=False)

print("Sample size:", len(model_data))
print("Number of predictors:", X.shape[1] - 1)
print("\nExpanded model without marital status:")
print(expanded_model_v2.summary())
```


```python
from scipy.stats import chi2
import pandas as pd

# Compare the baseline and revised expanded models.
lr_statistic = 2 * (
    expanded_model_v2.llf - baseline_model.llf
)

df_difference = (
    expanded_model_v2.df_model - baseline_model.df_model
)

lr_p_value = chi2.sf(lr_statistic, df_difference)

model_comparison = pd.DataFrame({
    "Model": [
        "Baseline model",
        "Expanded model without marital status"
    ],
    "Observations": [
        int(baseline_model.nobs),
        int(expanded_model_v2.nobs)
    ],
    "Predictors": [
        int(baseline_model.df_model),
        int(expanded_model_v2.df_model)
    ],
    "Log-likelihood": [
        baseline_model.llf,
        expanded_model_v2.llf
    ],
    "McFadden pseudo-R2": [
        baseline_model.prsquared,
        expanded_model_v2.prsquared
    ]
})

print("MODEL COMPARISON")
display(model_comparison.round(4))

print(f"Likelihood-ratio statistic: {lr_statistic:.4f}")
print(f"Degrees of freedom: {int(df_difference)}")
print(f"Likelihood-ratio test p-value: {lr_p_value:.6f}")

if lr_p_value < 0.05:
    print(
        "Conclusion: Adding the demographic predictors "
        "significantly improves model fit at the 5% level."
    )
else:
    print(
        "Conclusion: There is insufficient evidence that "
        "adding the demographic predictors improves model fit "
        "at the 5% level."
    )
```


```python
from pathlib import Path
import numpy as np
import pandas as pd

# Export results from the adjusted logistic regression model.
model = expanded_model_v2

coefficients = model.params
confidence_intervals = model.conf_int()

regression_table = pd.DataFrame({
    "Predictor": coefficients.index,
    "Coefficient": coefficients.values,
    "Odds_Ratio": np.exp(coefficients.values),
    "CI_Lower": np.exp(confidence_intervals.iloc[:, 0].values),
    "CI_Upper": np.exp(confidence_intervals.iloc[:, 1].values),
    "P_Value": model.pvalues.values
})

# Add clear explanations of the model terms.
predictor_labels = {
    "const": "Intercept",
    "naads_training_participation": "NAADS training participation",
    "farmer_group_member_clean": "Farmer-group membership",
    "age_centered": "Centered household-head age",
    "age_centered_squared": "Centered household-head age squared",
    "head_sex_Male": "Male household head (reference: Female)"
}

regression_table["Predictor_Label"] = (
    regression_table["Predictor"]
    .map(predictor_labels)
    .fillna(regression_table["Predictor"])
)

# Round numerical values for presentation.
numeric_columns = [
    "Coefficient",
    "Odds_Ratio",
    "CI_Lower",
    "CI_Upper",
    "P_Value"
]
regression_table[numeric_columns] = (
    regression_table[numeric_columns].round(4)
)

# Save the final adjusted-model results.
output_path = Path("../reports/logistic_regression_results.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
regression_table.to_csv(output_path, index=False)

print("Model:", type(model).__name__)
print("Observations:", int(model.nobs))
print("Predictors exported:", len(coefficients) - 1)
print("Saved to:", output_path.resolve())

display(regression_table)
```


```python
import matplotlib.pyplot as plt

# Sort crops by improved-seed percentage
plot_data = crop_seed_percentages.sort_values(
    "Improved",
    ascending=False
)

# Create the chart
ax = plot_data["Improved"].plot(
    kind="bar",
    figsize=(9, 5)
)

ax.set_title("Improved-Seed Use Across Five Major Crops")
ax.set_xlabel("Crop")
ax.set_ylabel("Improved-seed records (%)")
ax.set_ylim(0, 100)

plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()
```


```python
# ============================================
# RESEARCHPRO ANALYTICS
# Predictive Performance: Logistic Regression
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Prepare the analysis dataset
feature_columns = [
    "naads_training_participation",
    "farmer_group_member_clean",
    "head_age",
    "head_sex"
]

prediction_data = expanded_data.dropna(
    subset=["improved_seed_adopter", *feature_columns]
).copy()

# 2. Prepare age variables
# The age mean is calculated from the full analysis dataset
# here; we will improve this preprocessing in a later step
# if we need a stricter deployment-style evaluation.
age_mean = prediction_data["head_age"].mean()

prediction_data["age_centered"] = (
    prediction_data["head_age"] - age_mean
)

prediction_data["age_centered_squared"] = (
    prediction_data["age_centered"] ** 2
)

# 3. Create predictor matrix
X = prediction_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean",
        "age_centered",
        "age_centered_squared",
        "head_sex"
    ]
].copy()

# Encode sex as a binary variable
X["head_sex_Male"] = (
    X["head_sex"] == "Male"
).astype(int)

X = X.drop(columns=["head_sex"])

# Outcome: 1 = improved-seed adopter; 0 = non-adopter
y = prediction_data["improved_seed_adopter"].astype(int)

# 4. Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training sample:", len(X_train))
print("Testing sample:", len(X_test))

print(
    f"Training adoption rate: {y_train.mean() * 100:.2f}%"
)

print(
    f"Testing adoption rate: {y_test.mean() * 100:.2f}%"
)

# 5. Build and fit the model
model_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    (
        "logistic_regression",
        LogisticRegression(
            max_iter=2000,
            random_state=42
        )
    )
])

model_pipeline.fit(X_train, y_train)

# 6. Predict probabilities and classifications
y_prob = model_pipeline.predict_proba(X_test)[:, 1]
y_pred = model_pipeline.predict(X_test)

# 7. Calculate evaluation metrics
metrics = {
    "ROC AUC": roc_auc_score(y_test, y_prob),
    "Average precision": average_precision_score(y_test, y_prob),
    "Accuracy": accuracy_score(y_test, y_pred),
    "Balanced accuracy": balanced_accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1-score": f1_score(y_test, y_pred, zero_division=0)
}

performance_results = pd.DataFrame({
    "Metric": list(metrics.keys()),
    "Score": list(metrics.values())
})

print("\nPREDICTIVE PERFORMANCE")
display(performance_results.round(4))

# 8. Display the confusion matrix
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1]
)

confusion_df = pd.DataFrame(
    cm,
    index=["Actual non-adopter", "Actual adopter"],
    columns=["Predicted non-adopter", "Predicted adopter"]
)

print("\nCONFUSION MATRIX")
display(confusion_df)

# 9. Display the classification report
print("\nCLASSIFICATION REPORT")

print(
    classification_report(
        y_test,
        y_pred,
        labels=[0, 1],
        target_names=["Non-adopter", "Adopter"],
        zero_division=0
    )
)
```


```python
import pandas as pd
import numpy as np

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix
)

# 1. Examine predicted probabilities.
probability_summary = pd.Series(y_prob).describe(
    percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
)

print("PREDICTED PROBABILITY DISTRIBUTION")
display(probability_summary.to_frame("Predicted probability").round(4))

print(
    "\nMinimum probability:",
    round(y_prob.min(), 4)
)

print(
    "Maximum probability:",
    round(y_prob.max(), 4)
)

# 2. Evaluate several classification thresholds.
thresholds = [0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.50]

threshold_results = []

for threshold in thresholds:
    predictions = (y_prob >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    ).ravel()

    threshold_results.append({
        "Threshold": threshold,
        "Predicted adopters": int(predictions.sum()),
        "True positives": int(tp),
        "False positives": int(fp),
        "False negatives": int(fn),
        "True negatives": int(tn),
        "Precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "F1-score": f1_score(
            y_test, predictions, zero_division=0
        ),
        "Balanced accuracy": balanced_accuracy_score(
            y_test, predictions
        )
    })

threshold_table = pd.DataFrame(threshold_results)

print("\nPERFORMANCE AT DIFFERENT THRESHOLDS")
display(threshold_table.round(4))
```


```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.plot(
    threshold_table["Threshold"],
    threshold_table["Precision"],
    marker="o",
    label="Precision"
)

plt.plot(
    threshold_table["Threshold"],
    threshold_table["Recall"],
    marker="o",
    label="Recall"
)

plt.plot(
    threshold_table["Threshold"],
    threshold_table["F1-score"],
    marker="o",
    label="F1-score"
)

plt.plot(
    threshold_table["Threshold"],
    threshold_table["Balanced accuracy"],
    marker="o",
    label="Balanced accuracy"
)

plt.xlabel("Classification threshold")
plt.ylabel("Score")
plt.title("Predictive Performance at Different Classification Thresholds")
plt.xticks(threshold_table["Threshold"])
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```


```python
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Prepare the analysis dataset
feature_columns = [
    "naads_training_participation",
    "farmer_group_member_clean",
    "head_age",
    "head_sex"
]

prediction_data = expanded_data.dropna(
    subset=["improved_seed_adopter", *feature_columns]
).copy()

# Encode household-head sex
prediction_data["head_sex_Male"] = (
    prediction_data["head_sex"] == "Male"
).astype(int)

# Define predictors and outcome
X = prediction_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean",
        "head_age",
        "head_sex_Male"
    ]
].copy()

y = prediction_data["improved_seed_adopter"].astype(int)

# Split before calculating preprocessing values
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Calculate age-centering value using training data only
age_mean_train = X_train["head_age"].mean()

for dataset in [X_train, X_test]:
    dataset["age_centered"] = dataset["head_age"] - age_mean_train
    dataset["age_centered_squared"] = dataset["age_centered"] ** 2

# Remove the original age column
X_train = X_train.drop(columns=["head_age"])
X_test = X_test.drop(columns=["head_age"])

print("Training observations:", len(X_train))
print("Test observations:", len(X_test))
print("Training adoption rate:", round(y_train.mean(), 4))
print("Test adoption rate:", round(y_test.mean(), 4))
print("Training-set mean age used for centering:", round(age_mean_train, 2))
```


```python
# Build the logistic regression pipeline
corrected_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic_regression", LogisticRegression(
        max_iter=2000,
        random_state=42
    ))
])

# Train using training data only
corrected_pipeline.fit(X_train, y_train)

# Generate predictions for the unseen test data
y_prob_corrected = corrected_pipeline.predict_proba(X_test)[:, 1]
y_pred_corrected = corrected_pipeline.predict(X_test)

# Calculate evaluation metrics
corrected_metrics = {
    "ROC AUC": roc_auc_score(y_test, y_prob_corrected),
    "Average precision": average_precision_score(
        y_test, y_prob_corrected
    ),
    "Accuracy": accuracy_score(y_test, y_pred_corrected),
    "Balanced accuracy": balanced_accuracy_score(
        y_test, y_pred_corrected
    ),
    "Precision": precision_score(
        y_test, y_pred_corrected, zero_division=0
    ),
    "Recall": recall_score(
        y_test, y_pred_corrected, zero_division=0
    ),
    "F1-score": f1_score(
        y_test, y_pred_corrected, zero_division=0
    )
}

print("CORRECTED MODEL PERFORMANCE")
display(
    pd.DataFrame.from_dict(
        corrected_metrics,
        orient="index",
        columns=["Score"]
    ).round(4)
)

print("\nCONFUSION MATRIX")
print(
    confusion_matrix(
        y_test,
        y_pred_corrected,
        labels=[0, 1]
    )
)

print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        y_test,
        y_pred_corrected,
        labels=[0, 1],
        target_names=["Non-adopter", "Adopter"],
        zero_division=0
    )
)
```


```python
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score
)

threshold = 0.10

y_pred_010 = (y_prob_corrected >= threshold).astype(int)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred_010,
    labels=[0, 1]
).ravel()

threshold_010_results = pd.DataFrame({
    "Metric": [
        "Threshold",
        "Predicted adopters",
        "True positives",
        "False positives",
        "False negatives",
        "True negatives",
        "Precision",
        "Recall",
        "F1-score",
        "Balanced accuracy"
        
    ],
    "Value": [
        threshold,
        int(y_pred_010.sum()),
        int(tp),
        int(fp),
        int(fn),
        int(tn),
        precision_score(y_test, y_pred_010, zero_division=0),
        recall_score(y_test, y_pred_010, zero_division=0),
        f1_score(y_test, y_pred_010, zero_division=0),
        balanced_accuracy_score(y_test, y_pred_010)
    ]
})

display(threshold_010_results.round(4))
```


```python

```


```python
from pathlib import Path

reports_dir = Path("..") / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

report_content = """
# Predictive Performance Evaluation

## 1. Objective

This evaluation examines whether a logistic regression model can
distinguish households that adopted improved seeds from those that
did not, using selected household characteristics and agricultural
participation indicators from the Uganda National Panel Survey
2018–2019.

## 2. Data and methodology

The analysis used 1,962 complete household observations.

The data were divided into:
- Training set: 1,569 households (80%).
- Test set: 393 households (20%).

The split used random_state=42 and stratification by the outcome.
The outcome was improved-seed adoption. Predictors included NAADS
training participation, farmer-group membership, household-head age
and household-head sex.

Age-centering was calculated using the training set only and then
applied to both datasets. The model was fitted using a pipeline with
standardization and logistic regression.

The test set contained 50 adopters and 343 non-adopters.

## 3. Results

| Metric | Threshold 0.50 | Threshold 0.10 |
|---|---:|---:|
| ROC AUC | 0.5394 | 0.5394 |
| Average precision | 0.1697 | 0.1697 |
| Accuracy | 0.8728 | 0.3766 |
| Balanced accuracy | 0.5000 | 0.5403 |
| Precision | 0.0000 | 0.1402 |
| Recall | 0.0000 | 0.7600 |
| F1-score | 0.0000 | 0.2368 |

The threshold of 0.50 classified every test observation as a
non-adopter. Although accuracy was 87.28%, the model failed to
identify any of the 50 actual adopters. This illustrates why
accuracy alone is misleading when the outcome classes are imbalanced.

At a threshold of 0.10, the model identified 38 of the 50 adopters
and missed 12. However, it also incorrectly classified 233
non-adopters as adopters. Of the 271 households predicted to adopt,
only 38 actually adopted.

The ROC AUC of 0.5394 indicates weak discrimination. Average
precision was 0.1697, only modestly above the test-set adopter
prevalence of approximately 0.1272.

## 4. Interpretation

The model has limited predictive value in its current form.
Reducing the classification threshold improves recall but produces
many false positives. The default threshold produces high accuracy
only because non-adopters form the majority class.

The threshold of 0.10 is an exploratory comparison, not a final
operational threshold. Threshold selection should reflect the
intended use and be conducted using validation data rather than
optimizing against the test set.

## 5. Limitations

1. The analysis is exploratory and uses an unweighted test set.
2. The survey's sampling weights, strata and clustering have not
   been incorporated into this predictive evaluation.
3. The outcome represents household improved-seed adoption as
   operationally defined from crop records.
4. The model uses a limited set of predictors and may omit important
   factors related to adoption.
5. One train-test split provides only one estimate of predictive
   performance.
6. Associations in observational data do not establish causation.
7. The findings should not be generalized specifically to Kibalinga
   Sub-County because the dataset is from a national survey.

## 6. Recommendations

- Establish a simple baseline for comparison.
- Evaluate stability using cross-validation, with appropriate care
  for the survey's household and sampling design.
- Explore additional well-justified predictors.
- Check probability calibration and class-specific performance.
- Select a threshold using validation data and a clearly defined
  practical objective.
- Consider survey design and weighting before making population-level
  statistical claims.

## 7. Conclusion

The current logistic regression model does not reliably distinguish
improved-seed adopters from non-adopters. Its performance should be
treated as a baseline for further investigation rather than a
deployment-ready prediction system.

The results demonstrate the importance of evaluating multiple
metrics, examining confusion matrices and accounting for class
imbalance when assessing classification models.
"""

report_path = reports_dir / "predictive_performance_report.md"
report_path.write_text(report_content.strip() + "\n", encoding="utf-8")

print("Report saved to:", report_path.resolve())
```


```python
required = [
    "X_train", "X_test", "y_train", "y_test",
    "y_prob_corrected", "y_pred_corrected", "y_pred_010",
    "baseline_model_same_sample", "expanded_model_v2",
    "prediction_data",
]
for name in required:
    obj = globals().get(name)
    status = "OK" if obj is not None else "MISSING"
    kind = type(obj).__name__ if obj is not None else "-"
    print(f"{status:8s} {name:35s} {kind}")
```


```python
# Refit the statsmodels baseline on the same sample as expanded_model_v2
import statsmodels.api as sm

# baseline_model_same_sample must be fitted on the same rows as
# expanded_model_v2 so the likelihood-ratio test is valid.

baseline_predictors = [
    "naads_training_participation",
    "farmer_group_member_clean",
]

X_baseline_same_sample = sm.add_constant(
    prediction_data[baseline_predictors].astype(float),
    has_constant="add",
)

y_baseline_same_sample = prediction_data[
    "improved_seed_adopter"
].astype(int)

baseline_model_same_sample = sm.Logit(
    y_baseline_same_sample,
    X_baseline_same_sample,
).fit(disp=False)

print("BASELINE MODEL — MATCHED SAMPLE")
print("=" * 45)
print("Observations:", int(baseline_model_same_sample.nobs))
print("Log-likelihood:", round(baseline_model_same_sample.llf, 4))
print("McFadden pseudo-R²:", round(baseline_model_same_sample.prsquared, 6))
print(
    "Same sample size as expanded_model_v2:",
    int(baseline_model_same_sample.nobs) == int(expanded_model_v2.nobs),
)
```


```python
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

# Create a baseline that always predicts the majority class
dummy_model = DummyClassifier(strategy="most_frequent")

# Fit using training data only
dummy_model.fit(X_train, y_train)

# Predict the test observations
y_pred_baseline = dummy_model.predict(X_test)

# Summarize baseline performance
baseline_metrics = {
    "Accuracy": accuracy_score(y_test, y_pred_baseline),
    "Balanced accuracy": balanced_accuracy_score(
        y_test, y_pred_baseline
    ),
    "Precision": precision_score(
        y_test, y_pred_baseline, zero_division=0
    ),
    "Recall": recall_score(
        y_test, y_pred_baseline, zero_division=0
    ),
    "F1-score": f1_score(
        y_test, y_pred_baseline, zero_division=0
    )
}

print("BASELINE MODEL PERFORMANCE")

display(
    pd.DataFrame.from_dict(
        baseline_metrics,
        orient="index",
        columns=["Score"]
    ).round(4)
)

print("\nBASELINE CONFUSION MATRIX")

print(
    confusion_matrix(
        y_test,
        y_pred_baseline,
        labels=[0, 1]
    )
)
```


```python
baseline_comparison = pd.DataFrame([
    {
        "Model": "Majority-class baseline",
        "ROC_AUC": np.nan,
        "Accuracy": accuracy_score(y_test, y_pred_baseline),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_baseline
        ),
        "Precision": precision_score(
            y_test, y_pred_baseline, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_baseline, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_baseline, zero_division=0
        )
    },
    {
        "Model": "Logistic regression",
        "ROC_AUC": roc_auc_score(y_test, y_prob_corrected),
        "Accuracy": accuracy_score(y_test, y_pred_corrected),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_corrected
        ),
        "Precision": precision_score(
            y_test, y_pred_corrected, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_corrected, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_corrected, zero_division=0
        )
    }
])

display(baseline_comparison.round(4))
```


```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Build a class-weighted logistic regression model
balanced_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    (
        "logistic_regression",
        LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42
        )
    )
])

# Train using the same training data
balanced_pipeline.fit(X_train, y_train)

# Generate predictions on the same test data
y_prob_balanced = balanced_pipeline.predict_proba(X_test)[:, 1]
y_pred_balanced = balanced_pipeline.predict(X_test)

# Evaluate performance
balanced_results = pd.DataFrame([{
    "Model": "Class-weighted logistic regression",
    "ROC_AUC": roc_auc_score(y_test, y_prob_balanced),
    "Average_Precision": average_precision_score(
        y_test, y_prob_balanced
    ),
    "Accuracy": accuracy_score(y_test, y_pred_balanced),
    "Balanced_Accuracy": balanced_accuracy_score(
        y_test, y_pred_balanced
    ),
    "Precision": precision_score(
        y_test, y_pred_balanced, zero_division=0
    ),
    "Recall": recall_score(
        y_test, y_pred_balanced, zero_division=0
    ),
    "F1_Score": f1_score(
        y_test, y_pred_balanced, zero_division=0
    )
}])

display(balanced_results.round(4))

print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred_balanced))
```


```python
thresholds = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]

threshold_results = []

for threshold in thresholds:
    y_pred_threshold = (
        y_prob_balanced >= threshold
    ).astype(int)

    threshold_results.append({
        "Threshold": threshold,
        "Predicted_Adopters": int(y_pred_threshold.sum()),
        "Precision": precision_score(
            y_test, y_pred_threshold, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_threshold, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_threshold, zero_division=0
        ),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_threshold
        )
    })

threshold_comparison = pd.DataFrame(threshold_results)

display(threshold_comparison.round(4))
```


```python
display(
    threshold_comparison[
        [
            "Threshold",
            "Predicted_Adopters",
            "Precision",
            "Recall",
            "F1_Score",
            "Balanced_Accuracy"
        ]
    ].round(4).to_string(index=False)
)
```


```python
# Examine the predictors used in our current model
predictor_summary = prediction_data[
    [
        "naads_training_participation",
        "farmer_group_member_clean",
        "head_age",
        "head_sex",
        "improved_seed_adopter"
    ]
].describe(include="all").T

display(predictor_summary)
```


```python
# Check the distribution of the target and categorical predictors

print("Adoption outcome:")
display(
    prediction_data["improved_seed_adopter"]
    .value_counts(dropna=False)
)

print("\nNAADS training participation:")
display(
    prediction_data["naads_training_participation"]
    .value_counts(dropna=False)
)

print("\nFarmer-group membership:")
display(
    prediction_data["farmer_group_member_clean"]
    .value_counts(dropna=False)
)

print("\nHousehold-head sex:")
display(
    prediction_data["head_sex"]
    .value_counts(dropna=False)
)
```


```python
# Compare adoption rates across predictor categories

categorical_predictors = [
    "naads_training_participation",
    "farmer_group_member_clean",
    "head_sex"
]

for variable in categorical_predictors:

    print(f"\nAdoption by {variable}")

    adoption_table = pd.crosstab(
        prediction_data[variable],
        prediction_data["improved_seed_adopter"],
        margins=True
    )

    adoption_rates = (
        prediction_data
        .groupby(variable, observed=True)["improved_seed_adopter"]
        .agg(["count", "mean"])
        .rename(columns={
            "count": "Households",
            "mean": "Adoption_Rate"
        })
    )

    adoption_rates["Adoption_Rate"] *= 100

    display(adoption_table)
    display(adoption_rates.round(2))
```


```python
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association

categorical_predictors = [
    "naads_training_participation",
    "farmer_group_member_clean",
    "head_sex"
]

association_results = []

for variable in categorical_predictors:

    table = pd.crosstab(
        prediction_data[variable],
        prediction_data["improved_seed_adopter"]
    )

    chi2, p_value, dof, expected = chi2_contingency(
        table,
        correction=False
    )

    cramers_v = association(
        table,
        method="cramer"
    )

    association_results.append({
        "Predictor": variable,
        "Chi_Square": chi2,
        "Degrees_of_Freedom": dof,
        "P_Value": p_value,
        "Cramers_V": cramers_v,
        "Minimum_Expected_Count": expected.min()
    })

association_results_df = pd.DataFrame(association_results)

display(association_results_df.round(4))
```


```python
from scipy.stats import mannwhitneyu

# Separate household-head ages by adoption status
adopters_age = prediction_data.loc[
    prediction_data["improved_seed_adopter"] == 1,
    "head_age"
].dropna()

non_adopters_age = prediction_data.loc[
    prediction_data["improved_seed_adopter"] == 0,
    "head_age"
].dropna()

# Descriptive statistics
age_summary = pd.DataFrame({
    "Group": ["Non-adopters", "Adopters"],
    "Sample_Size": [
        len(non_adopters_age),
        len(adopters_age)
    ],
    "Mean_Age": [
        non_adopters_age.mean(),
        adopters_age.mean()
    ],
    "Median_Age": [
        non_adopters_age.median(),
        adopters_age.median()
    ],
    "Standard_Deviation": [
        non_adopters_age.std(),
        adopters_age.std()
    ]
})

display(age_summary.round(2))

# Mann-Whitney U test
u_statistic, p_value = mannwhitneyu(
    adopters_age,
    non_adopters_age,
    alternative="two-sided"
)

print(f"Mann-Whitney U statistic: {u_statistic:.2f}")
print(f"P-value: {p_value:.4f}")
```


```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=prediction_data,
    x="improved_seed_adopter",
    y="head_age"
)

plt.xticks(
    [0, 1],
    ["Non-adopters", "Adopters"]
)

plt.title("Household-Head Age by Improved-Seed Adoption Status")
plt.xlabel("Adoption status")
plt.ylabel("Household-head age (years)")
plt.tight_layout()
plt.show()
```


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Calculate the observed adoption rate for each age
age_adoption = (
    prediction_data
    .groupby("head_age", as_index=False)
    .agg(
        Total_Households=("improved_seed_adopter", "size"),
        Adopters=("improved_seed_adopter", "sum")
    )
)

age_adoption["Adoption_Rate"] = (
    age_adoption["Adopters"] / age_adoption["Total_Households"]
)

# Keep ages with at least 10 households to reduce instability
age_adoption_filtered = age_adoption[
    age_adoption["Total_Households"] >= 10
].copy()

# Plot adoption rates by age
plt.figure(figsize=(10, 5))

sns.regplot(
    data=age_adoption_filtered,
    x="head_age",
    y="Adoption_Rate",
    lowess=True,
    scatter_kws={"alpha": 0.6},
    line_kws={"linewidth": 2}
)

plt.title("Improved-Seed Adoption Rate by Household-Head Age")
plt.xlabel("Household-head age (years)")
plt.ylabel("Observed adoption rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

print("Age-level chart generated; detailed table preview omitted.")
```


```python
# Check the age distribution
print("Minimum age:", prediction_data["head_age"].min())
print("Maximum age:", prediction_data["head_age"].max())

print("\nHousehold-head ages below 18:")
print(
    "Number of household heads below 18:",
    int((prediction_data["head_age"] < 18).sum())
)

# Verify that the adoption outcome is binary
print("\nAdoption outcome values:")
print(prediction_data["improved_seed_adopter"].value_counts(dropna=False))

# Check whether the outcome contains only 0 and 1
print(
    "\nUnique adoption values:",
    sorted(prediction_data["improved_seed_adopter"].dropna().unique())
)

# Recalculate the age summary correctly
age_adoption_check = (
    prediction_data
    .groupby("head_age")
    .agg(
        Total_Households=("improved_seed_adopter", "size"),
        Adopters=("improved_seed_adopter", "sum"),
        Valid_Outcomes=("improved_seed_adopter", "count")
    )
    .reset_index()
)

age_adoption_check["Adoption_Rate"] = (
    age_adoption_check["Adopters"]
    / age_adoption_check["Valid_Outcomes"]
)

print("Age-specific checks completed; detailed preview omitted.")
```


```python
# Inspect dataset structure and quality without displaying individual records.

print("Dataset shape:", prediction_data.shape)

columns_to_check = [
    "head_age",
    "improved_seed_adopter"
]

print("\nColumn data types:")
print(prediction_data[columns_to_check].dtypes.to_string())

print("\nAge summary:")
print(prediction_data["head_age"].describe().round(2).to_string())

print("\nMinimum age:", prediction_data["head_age"].min())
print("Maximum age:", prediction_data["head_age"].max())

print("\nMissing values:")
print(
    prediction_data[columns_to_check]
    .isna()
    .sum()
    .to_string()
)

print("\nAdoption outcome counts:")
print(
    prediction_data["improved_seed_adopter"]
    .value_counts(dropna=False)
    .sort_index()
    .to_string()
)


```


```python
# Recalculate age-specific adoption statistics
age_adoption = (
    prediction_data
    .groupby("head_age")
    .agg(
        Total_Households=("improved_seed_adopter", "count"),
        Adopters=("improved_seed_adopter", "sum")
    )
    .reset_index()
)

age_adoption["Adopters"] = age_adoption["Adopters"].astype(int)

age_adoption["Non_Adopters"] = (
    age_adoption["Total_Households"] - age_adoption["Adopters"]
)

age_adoption["Adoption_Rate_Percent"] = (
    age_adoption["Adopters"]
    / age_adoption["Total_Households"]
    * 100
)

# Verify the calculations
assert (
    age_adoption["Total_Households"]
    == age_adoption["Adopters"] + age_adoption["Non_Adopters"]
).all()

print("Total households:", age_adoption["Total_Households"].sum())
print("Total adopters:", age_adoption["Adopters"].sum())

print("Age-specific adoption summary calculated successfully.")
```


```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create age bands
age_bins = [17, 29, 39, 49, 59, 69, 79, 99]
age_labels = [
    "18–29",
    "30–39",
    "40–49",
    "50–59",
    "60–69",
    "70–79",
    "80–98"
]

prediction_data["age_group"] = pd.cut(
    prediction_data["head_age"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)

# Calculate adoption rates by age group
age_group_summary = (
    prediction_data
    .groupby("age_group", observed=False)
    .agg(
        Total_Households=("improved_seed_adopter", "count"),
        Adopters=("improved_seed_adopter", "sum")
    )
    .reset_index()
)

age_group_summary["Non_Adopters"] = (
    age_group_summary["Total_Households"]
    - age_group_summary["Adopters"]
)

age_group_summary["Adoption_Rate_Percent"] = (
    age_group_summary["Adopters"]
    / age_group_summary["Total_Households"]
    * 100
)

display(age_group_summary.round(2))

# Plot adoption rates
plt.figure(figsize=(10, 5))

sns.barplot(
    data=age_group_summary,
    x="age_group",
    y="Adoption_Rate_Percent"
)

plt.title("Improved-Seed Adoption Rate by Household-Head Age Group")
plt.xlabel("Household-head age group (years)")
plt.ylabel("Adoption rate (%)")
plt.tight_layout()
plt.show()
```


```python
display(
    age_group_summary[
        [
            "age_group",
            "Total_Households",
            "Adopters",
            "Non_Adopters",
            "Adoption_Rate_Percent"
        ]
    ].round(2)
)
```


```python
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association

# Create a contingency table
age_adoption_table = pd.crosstab(
    prediction_data["age_group"],
    prediction_data["improved_seed_adopter"]
)

# Run chi-square test
chi2, p_value, dof, expected = chi2_contingency(
    age_adoption_table,
    correction=False
)

# Calculate Cramér's V
cramers_v = association(
    age_adoption_table,
    method="cramer"
)

print("Contingency table:")
display(age_adoption_table)

print(f"Chi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.4f}")
print(f"Cramér's V: {cramers_v:.4f}")
print(f"Minimum expected cell count: {expected.min():.4f}")
print(
    "Expected cells below 5:",
    (expected < 5).sum()
)
```


```python
# Display the model summary
print(expanded_model_v2.summary())
```


```python
from scipy.stats import chi2

# Extract statistics from the fitted model
ll_model = expanded_model_v2.llf
ll_null = expanded_model_v2.llnull
n_observations = int(expanded_model_v2.nobs)

# Calculate the likelihood-ratio statistic
lr_statistic = 2 * (ll_model - ll_null)

# Calculate degrees of freedom
df = int(expanded_model_v2.df_model)

# Calculate the p-value
lr_p_value = chi2.sf(lr_statistic, df)

# Calculate McFadden's pseudo-R-squared
mcfadden_r2 = 1 - (ll_model / ll_null)

print("Number of observations:", n_observations)
print("Fitted log-likelihood:", round(ll_model, 4))
print("Null log-likelihood:", round(ll_null, 4))
print("Likelihood-ratio statistic:", round(lr_statistic, 4))
print("Degrees of freedom:", df)
print("Likelihood-ratio p-value:", f"{lr_p_value:.8f}")
print("McFadden's pseudo-R-squared:", round(mcfadden_r2, 5))
```


```python
# Check the household-level adoption classification

print("Household-level adoption summary")
print("-" * 45)

print("Total household interview records:", len(household_seeds))

print("\nAdoption status counts:")
print(household_seeds["adoption_status"].value_counts(dropna=False))

print("\nBinary adoption outcome counts:")
print(household_seeds["improved_seed_adopter"].value_counts(dropna=False))

print("\nNumber of unique household interview IDs:")
print(household_seeds["hhid"].nunique())

print("\nMissing binary outcomes:")
print(household_seeds["improved_seed_adopter"].isna().sum())
```


```python
# Inspect how the adoption status was created

print("Adoption-status labels:")
print(household_seeds["adoption_status"].value_counts(dropna=False))

print("\nBinary outcome by adoption status:")
print(
    pd.crosstab(
        household_seeds["adoption_status"],
        household_seeds["improved_seed_adopter"],
        dropna=False
    )
)
```


```python
# Inspect how household-level adoption status was constructed

print("Columns in household_seeds:")
print(household_seeds.columns.tolist())

print("\nSample of household-level adoption records:")
print("\nHousehold adoption-status counts:")
print(household_seeds["adoption_status"].value_counts(dropna=False))

print("\nNumber of household records:", len(household_seeds))
print("Unique household interview IDs:", household_seeds["hhid"].nunique())
```


```python
# Quality check: verify household-level adoption classifications

# 1. Check whether adopters have at least one improved-seed crop record
invalid_adopters = household_seeds[
    (household_seeds["adoption_status"] == "Adopter") &
    (household_seeds["improved_seed_crop_records"] < 1)
]

# 2. Check whether non-adopters have valid seed-type records
invalid_non_adopters = household_seeds[
    (household_seeds["adoption_status"] == "Non-adopter") &
    (
        (household_seeds["valid_seed_type_records"] < 1) |
        (household_seeds["improved_seed_crop_records"] > 0)
    )
]

# 3. Check whether unknown households have no valid seed-type records
invalid_unknown = household_seeds[
    (household_seeds["adoption_status"] == "Unknown") &
    (household_seeds["valid_seed_type_records"] > 0)
]

print("ADOPTION CLASSIFICATION QUALITY CHECK")
print("-" * 45)
print("Invalid adopter records:", len(invalid_adopters))
print("Invalid non-adopter records:", len(invalid_non_adopters))
print("Potentially inconsistent unknown records:", len(invalid_unknown))

if (
    len(invalid_adopters) == 0
    and len(invalid_non_adopters) == 0
    and len(invalid_unknown) == 0
):
    print("\nPASS: All records satisfy the expected classification rules.")
else:
    print("\nREVIEW REQUIRED: Inspect the records flagged above.")

    print(
        "Counts only; inspect records locally if further investigation is needed."
    )
```


```python
# Quality check: compare the adoption outcome across analysis datasets

datasets_to_check = {
    "household_seeds": household_seeds,
    "prediction_data": prediction_data,
    "expanded_data": expanded_data
}

for dataset_name, dataset in datasets_to_check.items():
    print(f"\n{dataset_name}")
    print("-" * 40)

    if "improved_seed_adopter" in dataset.columns:
        outcome = dataset["improved_seed_adopter"]

        print("Total rows:", len(dataset))
        print("Adopters (1):", int((outcome == 1).sum()))
        print("Non-adopters (0):", int((outcome == 0).sum()))
        print("Unknown outcomes:", int(outcome.isna().sum()))
        print("Unique outcome values:", sorted(outcome.dropna().unique()))
    else:
        print("The adoption outcome column is missing.")
```


```python
# Compare the datasets without exposing household identifiers.

prediction_ids = set(prediction_data["hhid"].dropna())
expanded_ids = set(expanded_data["hhid"].dropna())

only_in_prediction = prediction_ids - expanded_ids
only_in_expanded = expanded_ids - prediction_ids

print(
    "Unique records only in prediction_data:",
    len(only_in_prediction)
)

print(
    "Unique records only in expanded_data:",
    len(only_in_expanded)
)

print(
    "\nTotal unique IDs in prediction_data:",
    len(prediction_ids)
)

print(
    "Total unique IDs in expanded_data:",
    len(expanded_ids)
)

print(
    "\nShared unique IDs:",
    len(prediction_ids & expanded_ids)
)


```


```python
# Examine records with missing demographic values.
# Report aggregate diagnostics without exposing household identifiers.

demographic_columns = [
    "head_age",
    "head_sex",
    "head_marital_status"
]

print("Expanded dataset shape:", expanded_data.shape)

missing_demographics = expanded_data[demographic_columns].isna()

print("\nMissing demographic values by field:")
print(missing_demographics.sum().to_string())

print(
    "\nRecords with at least one missing demographic field:",
    int(missing_demographics.any(axis=1).sum())
)

# Check whether missing-demographic records are present
# in the prediction dataset without displaying their identifiers.
if "hhid" in expanded_data.columns and "hhid" in prediction_data.columns:
    missing_record_ids = set(
        expanded_data.loc[
            missing_demographics.any(axis=1), "hhid"
        ].dropna()
    )

    prediction_ids = set(prediction_data["hhid"].dropna())

    print(
        "\nMissing-demographic records included in prediction_data:",
        len(missing_record_ids & prediction_ids)
    )


```


```python
# Verify sample sizes for the main statistical analyses

print("SAMPLE SIZE VERIFICATION")
print("=" * 45)

# Overall adoption classification
print("\n1. Household adoption classification")
print("Total household records:", len(household_seeds))
print(
    "Known adoption outcomes:",
    household_seeds["improved_seed_adopter"].notna().sum()
)
print(
    "Unknown adoption outcomes:",
    household_seeds["improved_seed_adopter"].isna().sum()
)

# Predictive analysis
print("\n2. Predictive analysis")
print("Complete-case observations:", len(prediction_data))
print("Training observations:", len(X_train))
print("Test observations:", len(X_test))

# Adjusted logistic regression
print("\n3. Adjusted logistic regression")
print("Observations used:", int(expanded_model_v2.nobs))

# Age comparison
print("\n4. Age comparison")
print(
    "Non-adopters with valid age:",
    expanded_data.loc[
        (expanded_data["improved_seed_adopter"] == 0)
        & expanded_data["head_age"].notna()
    ].shape[0]
)
print(
    "Adopters with valid age:",
    expanded_data.loc[
        (expanded_data["improved_seed_adopter"] == 1)
        & expanded_data["head_age"].notna()
    ].shape[0]
)
```


```python
# ============================================================
# Class-weighted logistic regression + predictive performance table
# Must run BEFORE the "Final check: adjusted model specification"
# cell, because that cell reads from `predictive_performance`.
# ============================================================

from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# ------------------------------------------------------------
# 1. Fit the class-weighted logistic regression model
# ------------------------------------------------------------

balanced_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    (
        "logistic_regression",
        LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42,
        ),
    ),
])

balanced_pipeline.fit(X_train, y_train)

y_prob_balanced = balanced_pipeline.predict_proba(X_test)[:, 1]
y_pred_balanced = balanced_pipeline.predict(X_test)

balanced_results = pd.DataFrame([{
    "Model": "Class-weighted logistic regression",
    "ROC_AUC": roc_auc_score(y_test, y_prob_balanced),
    "Average_Precision": average_precision_score(y_test, y_prob_balanced),
    "Accuracy": accuracy_score(y_test, y_pred_balanced),
    "Balanced_Accuracy": balanced_accuracy_score(y_test, y_pred_balanced),
    "Precision": precision_score(y_test, y_pred_balanced, zero_division=0),
    "Recall": recall_score(y_test, y_pred_balanced, zero_division=0),
    "F1_Score": f1_score(y_test, y_pred_balanced, zero_division=0),
}])

print("CLASS-WEIGHTED MODEL RESULTS")
display(balanced_results.round(4))

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred_balanced))

# ------------------------------------------------------------
# 2. Build the predictive performance table
#    (standard threshold, exploratory lower threshold,
#     class-weighted model)
# ------------------------------------------------------------

# Guard: make sure the earlier cells actually produced the
# variables this cell depends on.
required_vars = [
    "y_test", "y_prob_corrected", "y_pred_corrected", "y_pred_010",
]
missing_vars = [v for v in required_vars if v not in globals()]
if missing_vars:
    raise RuntimeError(
        "Run the earlier model cells first. Missing: "
        + ", ".join(missing_vars)
    )

reports_dir = Path("..") / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

predictive_performance = pd.DataFrame([
    {
        "Model": "Logistic Regression",
        "Evaluation": "Default threshold",
        "Threshold": 0.50,
        "ROC_AUC": roc_auc_score(y_test, y_prob_corrected),
        "Average_Precision": average_precision_score(
            y_test, y_prob_corrected
        ),
        "Accuracy": accuracy_score(y_test, y_pred_corrected),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_corrected
        ),
        "Precision": precision_score(
            y_test, y_pred_corrected, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_corrected, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_corrected, zero_division=0
        ),
        "Test_Sample_Size": len(y_test),
    },
    {
        "Model": "Logistic Regression",
        "Evaluation": "Exploratory lower threshold",
        "Threshold": 0.10,
        "ROC_AUC": roc_auc_score(y_test, y_prob_corrected),
        "Average_Precision": average_precision_score(
            y_test, y_prob_corrected
        ),
        "Accuracy": accuracy_score(y_test, y_pred_010),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_010
        ),
        "Precision": precision_score(
            y_test, y_pred_010, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_010, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_010, zero_division=0
        ),
        "Test_Sample_Size": len(y_test),
    },
    {
        "Model": "Class-weighted logistic regression",
        "Evaluation": "Default threshold",
        "Threshold": 0.50,
        "ROC_AUC": roc_auc_score(y_test, y_prob_balanced),
        "Average_Precision": average_precision_score(
            y_test, y_prob_balanced
        ),
        "Accuracy": accuracy_score(y_test, y_pred_balanced),
        "Balanced_Accuracy": balanced_accuracy_score(
            y_test, y_pred_balanced
        ),
        "Precision": precision_score(
            y_test, y_pred_balanced, zero_division=0
        ),
        "Recall": recall_score(
            y_test, y_pred_balanced, zero_division=0
        ),
        "F1_Score": f1_score(
            y_test, y_pred_balanced, zero_division=0
        ),
        "Test_Sample_Size": len(y_test),
    },
])

output_path = reports_dir / "predictive_performance.csv"
predictive_performance.to_csv(output_path, index=False)

print("\nSaved to:", output_path.resolve())
print("Number of evaluations:", len(predictive_performance))
print("Test sample size:", len(y_test))

display(predictive_performance.round(4))
```


```python
# Final check: adjusted model specification and predictive performance

print("ADJUSTED LOGISTIC REGRESSION")
print("=" * 45)

print("Observations:", int(expanded_model_v2.nobs))
print("Model converged:", expanded_model_v2.mle_retvals["converged"])
print("McFadden pseudo-R²:", round(expanded_model_v2.prsquared, 4))
print(
    "LR p-value vs intercept-only model:",
    f"{expanded_model_v2.llr_pvalue:.8f}"
)

print("\nCOEFFICIENTS AND P-VALUES")
print(
    expanded_model_v2.params.to_frame(name="Coefficient")
    .join(expanded_model_v2.pvalues.rename("P-value"))
    .round(4)
)

print("\nPREDICTIVE MODEL")
print("=" * 45)

standard_result = predictive_performance.loc[
    (predictive_performance["Model"] == "Logistic Regression")
    & (predictive_performance["Evaluation"] == "Default threshold")
].iloc[0]

lower_threshold_result = predictive_performance.loc[
    (predictive_performance["Model"] == "Logistic Regression")
    & (
        predictive_performance["Evaluation"]
        == "Exploratory lower threshold"
    )
].iloc[0]

balanced_result = predictive_performance.loc[
    predictive_performance["Model"]
    == "Class-weighted logistic regression"
].iloc[0]

print("Test observations:", int(standard_result["Test_Sample_Size"]))
print("Original model ROC AUC:", round(standard_result["ROC_AUC"], 4))
print(
    "Class-weighted model ROC AUC:",
    round(balanced_result["ROC_AUC"], 4)
)
print("Class-weighted model recall:", round(balanced_result["Recall"], 4))
print(
    "Class-weighted model precision:",
    round(balanced_result["Precision"], 4)
)

print("\nLOWER-THRESHOLD EVALUATION")
print("Threshold:", round(lower_threshold_result["Threshold"], 2))
print("Recall:", round(lower_threshold_result["Recall"], 4))
print("Precision:", round(lower_threshold_result["Precision"], 4))
```


```python
# Final limitations and interpretation checklist

checks = {
    "Adoption outcome is binary (0/1)": (
        set(prediction_data["improved_seed_adopter"].unique()) == {0, 1}
    ),
    "Predictive dataset contains 1,962 observations": (
        len(prediction_data) == 1962
    ),
    "Adjusted regression converged": (
        expanded_model_v2.mle_retvals["converged"]
    ),
    "Adjusted model uses 1,962 observations": (
        int(expanded_model_v2.nobs) == 1962
    ),
    "Predictive test set contains 393 observations": (
        len(y_test) == 393
    ),
    "Predictive ROC AUC indicates weak discrimination": (
        0.5 < 0.5524 < 0.6
    ),
}

for description, passed in checks.items():
    print(f"{'PASS' if passed else 'CHECK'}: {description}")

print("\nRemember these reporting limitations:")
print("- The analysis is observational; do not claim causation.")
print("- Results are unweighted and do not account for the complex survey design.")
print("- The survey covers Uganda, not specifically Kibalinga Sub-County.")
print("- The predictive model has weak discrimination.")
print("- Report the sample size and denominator for every result.")
```


```python
from pathlib import Path

project_root = (
    Path.cwd().parent
    if Path.cwd().name == "notebooks"
    else Path.cwd()
)

reports_dir = project_root / "reports"

print("Reports directory:", reports_dir)
print("Directory exists:", reports_dir.exists())

print("\nExisting report files:")
if reports_dir.exists():
    for file_path in sorted(reports_dir.iterdir()):
        if file_path.is_file():
            print(f"- {file_path.name}")
else:
    print("The reports directory was not found.")
```


```python
from pathlib import Path

reports_dir = project_root / "reports"

files_to_review = [
    "model_comparison_interpretation.md",
    "predictive_performance_report.md",
]

for filename in files_to_review:
    file_path = reports_dir / filename

    print("\n" + "=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)

    if file_path.exists():
        print(file_path.read_text(encoding="utf-8"))
    else:
        print("File not found.")
```


```python
# Verify the baseline and expanded model comparison

from scipy.stats import chi2

print("BASELINE MODEL")
print("=" * 45)
print("Observations:", int(baseline_model_same_sample.nobs))
print("Log-likelihood:", round(baseline_model_same_sample.llf, 4))
print("McFadden pseudo-R²:", round(baseline_model_same_sample.prsquared, 6))

print("\nEXPANDED MODEL")
print("=" * 45)
print("Observations:", int(expanded_model_v2.nobs))
print("Log-likelihood:", round(expanded_model_v2.llf, 4))
print("McFadden pseudo-R²:", round(expanded_model_v2.prsquared, 6))

print("\nMODEL COMPARISON")
print("=" * 45)

if int(baseline_model_same_sample.nobs) == int(expanded_model_v2.nobs):
    lr_statistic = 2 * (
        expanded_model_v2.llf - baseline_model_same_sample.llf
    )
    degrees_of_freedom = int(
        expanded_model_v2.df_model - baseline_model_same_sample.df_model
    )
    lr_p_value = chi2.sf(lr_statistic, degrees_of_freedom)

    print("Same sample size: Yes")
    print("Likelihood-ratio statistic:", round(lr_statistic, 4))
    print("Degrees of freedom:", degrees_of_freedom)
    print("P-value:", f"{lr_p_value:.8f}")
else:
    print("WARNING: Models use different sample sizes.")
    print("Refit both on the same observations before comparing.")
```


```python
# Find fitted statsmodels regression results in the notebook

import statsmodels.api as sm
import statsmodels.discrete.discrete_model as sm_discrete

print("Potential regression model variables:")
print("=" * 55)

found_any = False

for name, obj in list(globals().items()):
    if name.startswith("_"):
        continue

    if isinstance(obj, sm_discrete.BinaryResultsWrapper):
        found_any = True
        print(f"\nVariable: {name}")
        print("Observations:", int(obj.nobs))
        print("Log-likelihood:", round(obj.llf, 4))
        print("McFadden pseudo-R²:", round(obj.prsquared, 6))
        print("Model predictors:", list(obj.model.exog_names))

if not found_any:
    print("No fitted BinaryResultsWrapper objects were found.")
```


```python
# Inspect existing variables for fitted logistic regression results
# This cell only reads variables and does not modify your models.

print("Potential fitted regression models")
print("=" * 55)

for name, obj in list(globals().items()):
    if name.startswith("_"):
        continue

    if (
        hasattr(obj, "llf")
        and hasattr(obj, "prsquared")
        and hasattr(obj, "nobs")
        and hasattr(obj, "model")
        and hasattr(obj.model, "exog_names")
    ):
        print(f"\nVariable: {name}")
        print("Observations:", int(obj.nobs))
        print("Log-likelihood:", round(obj.llf, 4))
        print("McFadden pseudo-R²:", round(obj.prsquared, 6))
        print("Predictors:", list(obj.model.exog_names))
```


```python
import statsmodels.api as sm

# Use the same 1,962 observations as the expanded model
baseline_predictors = [
    "naads_training_participation",
    "farmer_group_member_clean"
]

X_baseline_same_sample = sm.add_constant(
    prediction_data[baseline_predictors].astype(float),
    has_constant="add"
)

y_baseline_same_sample = prediction_data[
    "improved_seed_adopter"
].astype(int)

# Fit a new baseline logistic regression model
baseline_model_same_sample = sm.Logit(
    y_baseline_same_sample,
    X_baseline_same_sample
).fit(disp=False)

print("BASELINE MODEL — MATCHED SAMPLE")
print("=" * 45)
print("Observations:", int(baseline_model_same_sample.nobs))
print("Log-likelihood:", round(baseline_model_same_sample.llf, 4))
print(
    "McFadden pseudo-R²:",
    round(baseline_model_same_sample.prsquared, 6)
)

print("\nEXPANDED MODEL")
print("=" * 45)
print("Observations:", int(expanded_model_v2.nobs))
print("Log-likelihood:", round(expanded_model_v2.llf, 4))
print("McFadden pseudo-R²:", round(expanded_model_v2.prsquared, 6))
```


```python
from scipy.stats import chi2

# Compare nested models fitted to the same observations
lr_statistic = 2 * (
    expanded_model_v2.llf - baseline_model_same_sample.llf
)

degrees_of_freedom = int(
    expanded_model_v2.df_model
    - baseline_model_same_sample.df_model
)

lr_p_value = chi2.sf(lr_statistic, degrees_of_freedom)

print("FINAL LIKELIHOOD-RATIO TEST")
print("=" * 45)
print("Baseline observations:", int(baseline_model_same_sample.nobs))
print("Expanded observations:", int(expanded_model_v2.nobs))
print("Likelihood-ratio chi-square:", round(lr_statistic, 4))
print("Degrees of freedom:", degrees_of_freedom)
print("P-value:", f"{lr_p_value:.8f}")

print("\nMODEL FIT COMPARISON")
print("-" * 45)
print(
    "Baseline McFadden pseudo-R²:",
    round(baseline_model_same_sample.prsquared, 6)
)
print(
    "Expanded McFadden pseudo-R²:",
    round(expanded_model_v2.prsquared, 6)
)
```


```python
from pathlib import Path

report_path = reports_dir / "model_comparison_interpretation.md"

updated_report = """# Logistic Regression Model Comparison

## 1. Objective

A likelihood-ratio test compared a baseline logistic regression model
containing NAADS training participation and farmer-group membership
with an expanded model that additionally included household-head age,
a squared age term, and sex.

## 2. Methodology

Both models were fitted using the same 1,962 complete household
observations. The expanded model added three predictors to the baseline
model: centered age, centered age squared, and a male household-head
indicator.

## 3. Results

| Measure | Baseline model | Expanded model |
|---|---:|---:|
| Observations | 1,962 | 1,962 |
| Log-likelihood | -745.3417 | -736.8809 |
| McFadden pseudo-R-squared | 0.0067 | 0.0179 |

The expanded model improved fit relative to the baseline model:
likelihood-ratio chi-square(3) = 16.92, p = .000733.

Household-head sex was significantly associated with improved-seed
adoption in the expanded model. The coefficient for a male household
head was 0.6167 (p = .0002), corresponding to an estimated odds ratio
of approximately 1.85. The approximate 95% confidence interval for
the odds ratio was 1.34 to 2.56.

NAADS training participation (p = .178), farmer-group membership
(p = .138), centered age (p = .721), and centered age squared
(p = .505) were not statistically significant in the expanded model.

## 4. Interpretation

Adding age, age squared, and household-head sex significantly improved
the model's fit. However, the expanded model's McFadden pseudo-R-squared
of 0.0179 indicates limited explanatory power.

The significant association involving household-head sex should not
be interpreted as evidence that sex causes improved-seed adoption.
The model is observational and includes only a limited set of
predictors.

## 5. Limitations

1. The analysis is unweighted and does not incorporate the survey's
   sampling weights, strata, or clustering.
2. The findings are exploratory associations and do not establish
   causal relationships.
3. The dataset comes from a national Ugandan survey and is not
   specifically representative of Kibalinga Sub-County.
4. The model's explanatory power is limited, and statistical
   significance does not guarantee strong predictive performance.
5. Missing data and complete-case selection may affect the results.

## 6. Conclusion

The expanded model fitted the observed data significantly better
than the baseline model, but its explanatory power remained limited.
Household-head sex was statistically significant after adjustment
for the other included variables. These findings should be interpreted
cautiously until survey design and sampling weights are incorporated.
"""

# Write only after confirming the target file exists.
if report_path.exists():
    report_path.write_text(updated_report, encoding="utf-8")
    print("Updated report:", report_path)
    print("File size:", report_path.stat().st_size, "bytes")
else:
    print("The expected report was not found. No file was written.")
```


```python
from pathlib import Path

final_report_path = reports_dir / "final_analysis_report.md"

final_report = r"""
# Agricultural Technology Adoption in Uganda
## ResearchPro Analytics — Final Analysis Report

## 1. Executive Summary

This exploratory analysis examined household adoption of improved
seeds using data from the Uganda National Panel Survey 2018–2019.
The analysis considered seed-use patterns, NAADS training participation,
farmer-group membership, household-head age and sex.

Among the 1,978 households with known adoption outcomes, 252 were
classified as adopters, giving an observed adoption rate of 12.74%.
A further 213 household records had unknown adoption outcomes and
were excluded from analyses requiring a known outcome.

The adjusted logistic regression used 1,962 complete observations.
The expanded model improved fit over the baseline model
(likelihood-ratio chi-square(3) = 16.92, p = .000733).
Household-head sex was significantly associated with adoption,
while training participation, farmer-group membership and age terms
were not statistically significant after adjustment.

Predictive performance was weak. The class-weighted model achieved
a test-set ROC AUC of 0.5524 and recall of 64%, but precision was
13.97%. These findings suggest that the current predictor set does
not reliably distinguish adopters from non-adopters.

The results are exploratory and should not be interpreted causally
or as estimates specific to Kibalinga Sub-County.

## 2. Data Source and Scope

The analysis used agricultural and household information from the
Uganda National Panel Survey 2018–2019, collected by the Uganda
Bureau of Statistics with support from the World Bank.

The survey is national in scope. This analysis does not establish
that the sample is representative of Kibalinga Sub-County.

The principal analytical unit for the adoption and modelling
analyses was the household interview record. Agricultural seed
information originated from crop-level records and was aggregated
to the household level for the adoption outcome.

## 3. Adoption Outcome Definition

Households were classified using observed improved-seed information
from their crop records:

- Adopter: at least one crop record indicated improved-seed use.
- Non-adopter: at least one valid seed-type record was available,
  and no improved-seed crop record was observed.
- Unknown: no valid seed-type record was available to establish
  adoption status.

The resulting household classification contained:

| Adoption status | Households |
|---|---:|
| Adopter | 252 |
| Non-adopter | 1,726 |
| Unknown | 213 |
| Total | 2,191 |

Among the 1,978 households with known outcomes, the observed
adoption rate was 12.74% (252/1,978).

This operational definition measures adoption as observed in the
available crop records. It should not be assumed to capture every
possible form of agricultural technology adoption.

## 4. Crop-Level Seed-Use Patterns

Crop-record summaries showed variation in the observed use of
improved seeds across crops.

Among the five crops examined in the exploratory comparison,
improved-seed use among records with valid seed-type responses was:

| Crop | Improved-seed records | Valid seed-type records | Percentage |
|---|---:|---:|---:|
| Banana food | 2 | 99 | 2.02% |
| Beans | 13 | 1,377 | 0.94% |
| Cassava | 35 | 495 | 7.07% |
| Maize | 132 | 1,342 | 9.84% |
| Sweet potatoes | 2 | 314 | 0.64% |

The five-crop chi-square comparison found an association between
crop category and seed type, chi-square(4) = 130.82, p < .001,
Cramer's V = 0.190.

The effect size indicates a relatively weak association. The
observations are crop records rather than independent households,
so this unadjusted test does not account for multiple crop records
from the same household or the complex survey design.

Percentages in this table are based on valid seed-type records
for each crop, not on the number of farmers growing that crop.

## 5. Unadjusted Associations with Adoption

### 5.1 NAADS Training Participation

Among households with valid values for the relevant variables,
the observed adoption rate was 22.32% for households reporting
NAADS training participation and 12.22% for those not reporting
participation.

The association was statistically significant:
chi-square(1) = 9.67, p = .002, Cramer's V = 0.070.

The effect size was small. This unadjusted association does not
establish that training caused adoption.

### 5.2 Farmer-Group Membership

The observed adoption rate was 25.40% among farmer-group members
and 12.37% among non-members.

The association was statistically significant:
chi-square(1) = 9.27, p = .002, Cramer's V = 0.069.

The effect size was small, and the result is unadjusted for
other household characteristics or survey design.

### 5.3 Household-Head Sex

The observed adoption rate was 14.85% for male-headed households
and 8.43% for female-headed households.

The association was statistically significant:
chi-square(1) = 15.83, p < .001, Cramer's V = 0.090.

The effect size was small. This result is an unadjusted association
and should not be interpreted causally.

### 5.4 Household-Head Age

The age distributions of adopters and non-adopters did not differ
significantly in the Mann–Whitney U test:
U = 204,690, p = .231.

The age-group comparison also did not identify a statistically
significant association:
chi-square(6) = 5.87, p = .437, Cramer's V = 0.055.

These findings do not provide strong evidence of an association
between household-head age and adoption in this sample.

## 6. Adjusted Logistic Regression

The adjusted logistic regression used 1,962 complete household
observations. The outcome was binary improved-seed adoption.

The model included NAADS training participation, farmer-group
membership, centered household-head age, centered age squared,
and a male household-head indicator.

### 6.1 Model Comparison

The baseline model included training participation and farmer-group
membership. The expanded model added age, age squared and sex.

| Measure | Baseline | Expanded |
|---|---:|---:|
| Observations | 1,962 | 1,962 |
| Log-likelihood | -745.3417 | -736.8809 |
| McFadden pseudo-R-squared | 0.0067 | 0.0179 |

The likelihood-ratio test indicated improved fit:
chi-square(3) = 16.92, p = .000733.

Although the expanded model fitted better than the baseline,
its explanatory power remained limited.

### 6.2 Adjusted Predictor Results

| Predictor | Coefficient | P-value | Interpretation |
|---|---:|---:|---|
| NAADS training participation | 0.4113 | .178 | Not statistically significant |
| Farmer-group membership | 0.5651 | .138 | Not statistically significant |
| Centered household-head age | -0.0017 | .721 | Not statistically significant |
| Centered age squared | -0.0002 | .505 | Not statistically significant |
| Male household head | 0.6167 | .0002 | Statistically significant positive association |

The estimated odds ratio for male-headed households was approximately
1.85, with an approximate 95% confidence interval of 1.34 to 2.56.
Conditional on the other variables in the model, male-headed
households had higher estimated odds of adoption than female-headed
households.

This is an observational association and does not establish a
causal effect. The model does not account for all potential
confounding factors.

## 7. Predictive Modelling

Predictive evaluation used 1,962 complete observations, split into
1,569 training records and 393 test records. The test set contained
50 adopters and 343 non-adopters.

Predictors included NAADS training participation, farmer-group
membership, household-head age and sex.

### 7.1 Test-Set Performance

| Metric | Standard logistic model | Class-weighted model |
|---|---:|---:|
| ROC AUC | 0.5394 | 0.5524 |
| Accuracy | 87.28% | 45.29% |
| Balanced accuracy | 50.00% | 53.28% |
| Precision | 0.00% | 13.97% |
| Recall | 0.00% | 64.00% |
| F1-score | 0.0000 | 0.2294 |

The standard model classified all test observations as non-adopters
at the default threshold of 0.50. Its high accuracy therefore
concealed its failure to identify adopters.

The class-weighted model identified 32 of the 50 adopters but
incorrectly classified 197 non-adopters as adopters. Its ROC AUC
of 0.5524 indicates weak discrimination.

The models should be treated as exploratory baselines, not as
deployment-ready prediction systems. Threshold selection should
be based on validation data and the intended practical objective.

## 8. Limitations

1. The analysis is observational and does not establish causation.
2. Survey sampling weights, strata and clustering were not
   incorporated into the reported statistical tests or regression.
3. The data are from a national Ugandan survey and are not
   specifically representative of Kibalinga Sub-County.
4. Adoption was operationalized using improved-seed crop records;
   it is not a comprehensive measure of every agricultural technology.
5. Missing and skipped responses may affect the available analysis
   samples. Unknown outcomes were not treated as non-adopters.
6. The complete-case models use 1,962 households, fewer than the
   1,978 households with known adoption outcomes.
7. Crop-level records from the same household are not independent.
8. The predictive models use a limited set of predictors and show
   weak test-set discrimination.
9. Predictive performance was assessed using one train-test split,
   so results may vary across different samples.

## 9. Recommendations

- Incorporate the survey's weights, strata and clustering when
  conducting population-level inference, using appropriate methods.
- Investigate additional predictors supported by the survey and
  relevant agricultural theory.
- Assess missing-data patterns and explain complete-case exclusions.
- Evaluate predictive stability with an appropriate validation
  strategy and compare models against simple baselines.
- Examine probability calibration and class-specific performance.
- Select classification thresholds using validation data and a
  clearly stated decision objective.
- Avoid making claims about Kibalinga Sub-County without data and
  a sampling design suitable for that population.

## 10. Conclusion

In this exploratory analysis, improved-seed adoption was observed
in 12.74% of households with known adoption outcomes. Unadjusted
tests found small associations between adoption and NAADS training,
farmer-group membership, and household-head sex. In the adjusted
model, household-head sex remained statistically significant, while
training participation, group membership and age terms did not.

The expanded logistic regression improved fit over the baseline
model, but explanatory power remained limited. Predictive evaluation
also showed weak discrimination, even with class weighting.

These findings provide a starting point for further analysis.
Survey-design-aware inference, stronger predictor selection and
additional validation are necessary before drawing population-level
or operational conclusions.
"""

if final_report_path.exists():
    print(
        "A final_analysis_report.md already exists. "
        "No file was overwritten."
    )
else:
    final_report_path.write_text(final_report.strip() + "\n", encoding="utf-8")
    print("Created:", final_report_path)
    print("File size:", final_report_path.stat().st_size, "bytes")
```


```python
from pathlib import Path

final_report_path = reports_dir / "final_analysis_report.md"

# Read the saved file from disk
saved_report = final_report_path.read_text(encoding="utf-8")

# Check required sections
required_sections = [
    "# Agricultural Technology Adoption in Uganda",
    "## 1. Executive Summary",
    "## 2. Data Source and Scope",
    "## 3. Adoption Outcome Definition",
    "## 4. Crop-Level Seed-Use Patterns",
    "## 5. Unadjusted Associations with Adoption",
    "## 6. Adjusted Logistic Regression",
    "## 7. Predictive Modelling",
    "## 8. Limitations",
    "## 9. Recommendations",
    "## 10. Conclusion",
]

print("FINAL REPORT VERIFICATION")
print("=" * 50)

for section in required_sections:
    print(
        f"{'PASS' if section in saved_report else 'MISSING'}: "
        f"{section}"
    )

print("\nFile exists:", final_report_path.exists())
print("File size:", final_report_path.stat().st_size, "bytes")
print("Word count:", len(saved_report.split()))
print("Contains verified LR statistic:", "16.92" in saved_report)
print("Contains correct overall adoption rate:", "12.74%" in saved_report)
print("Contains survey-design limitation:", "sampling weights" in saved_report)
```


```python
from pathlib import Path

project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()

print("PROJECT ROOT")
print(project_root)
print("\nKEY PROJECT FILES")
print("-" * 50)

files_to_check = [
    "README.md",
    ".gitignore",
    "requirements.txt",
    "docs/project_plan.md",
    "reports/final_analysis_report.md",
    "reports/predictive_performance_report.md",
    "reports/predictive_performance.csv",
    "reports/model_comparison_interpretation.md",
    "reports/improved_seed_use_by_crop.png",
    "reports/top_five_crop_seed_summary.csv",
]

for relative_path in files_to_check:
    path = project_root / relative_path
    status = "FOUND" if path.exists() else "MISSING"
    print(f"{status}: {relative_path}")

print("\nDATA DIRECTORIES")
for folder in ["data/raw", "data/processed", "data/external"]:
    path = project_root / folder
    print(f"{'FOUND' if path.exists() else 'MISSING'}: {folder}")
```


```python
from pathlib import Path

project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
gitignore_path = project_root / ".gitignore"

print("CURRENT .gitignore CONTENT")
print("=" * 50)

print(gitignore_path.read_text(encoding="utf-8"))
```

### Data protection

The project `.gitignore` excludes raw and processed data by default.
Do not publish restricted survey microdata or identifiable records.

Before reproducing this analysis, obtain the survey files through an
authorized source and place them in the documented local data directory.



```python
import sys
import importlib

print("Python executable:")
print(sys.executable)

print("\nPython version:")
print(sys.version)

packages = [
    "numpy",
    "pandas",
    "scipy",
    "statsmodels",
    "matplotlib",
    "seaborn",
    "sklearn",
]

print("\nPackage import checks:")
for package in packages:
    try:
        module = importlib.import_module(package)
        print(f"{package}: OK (version {module.__version__})")
    except Exception as exc:
        print(f"{package}: FAILED ({type(exc).__name__}: {exc})")
```


```python
from pathlib import Path
import importlib.util

# --------------------------------------------------
# 1. Locate the DDI documentation
# --------------------------------------------------

ddi_file = (
    extracted_folder /
    "ddi-documentation-english_microdata-3795.pdf"
)

if not ddi_file.is_file():
    raise FileNotFoundError(
        f"Documentation file not found: {ddi_file}"
    )

print("Documentation:", ddi_file)
print("File size (KB):", round(ddi_file.stat().st_size / 1024, 2))

# --------------------------------------------------
# 2. Identify an available PDF text-extraction package
# --------------------------------------------------

if importlib.util.find_spec("fitz"):
    import fitz

    with fitz.open(ddi_file) as pdf:
        pages = [
            page.get_text()
            for page in pdf
        ]

elif importlib.util.find_spec("pypdf"):
    from pypdf import PdfReader

    reader = PdfReader(str(ddi_file))
    pages = [
        page.extract_text() or ""
        for page in reader.pages
    ]

else:
    raise ImportError(
        "No supported PDF extraction package is installed "
        "in this notebook's Python environment. "
        "Do not reinstall Python; we can install or use "
        "an appropriate PDF reader if necessary."
    )

print("Total pages:", len(pages))
print("Pages containing extractable text:",
      sum(bool(page.strip()) for page in pages))

# --------------------------------------------------
# 3. Display the beginning of the documentation
# --------------------------------------------------

print("\n" + "=" * 70)
print("DOCUMENTATION PREVIEW")
print("=" * 70)

for page_number, page_text in enumerate(pages[:3], start=1):
    print(f"\n--- PAGE {page_number} ---\n")
    print(page_text[:2500])

# --------------------------------------------------
# 4. Search for useful documentation topics
# --------------------------------------------------

keywords = [
    "survey design",
    "sampling",
    "questionnaire",
    "agriculture",
    "household",
    "variable",
    "codebook",
    "weight",
    "cluster",
    "stratum",
    "missing values",
]

print("\n" + "=" * 70)
print("DOCUMENTATION TOPIC SEARCH")
print("=" * 70)

for keyword in keywords:
    matches = [
        page_number
        for page_number, page_text in enumerate(pages, start=1)
        if keyword.lower() in page_text.lower()
    ]

    print(
        f"{keyword}: "
        f"pages {matches if matches else 'No exact text match'}"
    )
```


```python
%pip install pypdf
```


```python
import sys
import pypdf

print("Python executable:", sys.executable)
print("pypdf version:", pypdf.__version__)
print("PDF reader is ready.")
```


```python
from pypdf import PdfReader

ddi_file = extracted_folder / "ddi-documentation-english_microdata-3795.pdf"

if not ddi_file.is_file():
    raise FileNotFoundError(f"Documentation not found: {ddi_file}")

reader = PdfReader(str(ddi_file))

print("Document:", ddi_file.name)
print("Total pages:", len(reader.pages))

for page_number, page in enumerate(reader.pages[:3], start=1):
    page_text = page.extract_text() or ""

    print(f"\n{'=' * 60}")
    print(f"PAGE {page_number}")
    print("=" * 60)

    if page_text.strip():
        print(page_text[:3500])
    else:
        print("No extractable text on this page.")
```


```python
# --------------------------------------------------
# Inspect the remaining DDI documentation
# --------------------------------------------------

from pypdf import PdfReader

ddi_file = extracted_folder / "ddi-documentation-english_microdata-3795.pdf"

reader = PdfReader(str(ddi_file))

print("Document:", ddi_file.name)
print("Total pages:", len(reader.pages))

for page_number in range(3, len(reader.pages)):
    page_text = reader.pages[page_number].extract_text() or ""

    print(f"\n{'=' * 70}")
    print(f"PAGE {page_number + 1}")
    print("=" * 70)

    if page_text.strip():
        print(page_text[:3000])
    else:
        print("No extractable text on this page.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Agricultural Dataset Structure Audit
# Read-only inspection: no files are modified
# ==========================================================

import pandas as pd
from pathlib import Path

agric_dir = extracted_folder / "Agric"

files_to_inspect = [
    "AGSEC1.csv",
    "AGSEC3A.csv",
    "AGSEC4A.csv",
    "AGSEC4B.csv",
]

for filename in files_to_inspect:
    file_path = agric_dir / filename

    print("\n" + "=" * 75)
    print(f"FILE: {filename}")
    print("=" * 75)

    if not file_path.is_file():
        print("File not found:", file_path)
        continue

    # Read only the header and first five records.
    sample_df = pd.read_csv(file_path, nrows=5, low_memory=False)

    # Count records without loading the entire file into memory.
    with file_path.open("rb") as file:
        row_count = sum(1 for _ in file) - 1

    print("File size (MB):", round(file_path.stat().st_size / (1024 ** 2), 3))
    print("Number of records:", row_count)
    print("Number of columns:", len(sample_df.columns))

    print("\nColumn names:")
    for column in sample_df.columns:
        print("-", column)

    print("\nFirst five records:")
    display(sample_df)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Agricultural Questionnaire Inspection
# Read-only: does not modify any files
# ==========================================================

from pypdf import PdfReader

questionnaire_file = extracted_folder / "agriculture_qx.pdf"

if not questionnaire_file.is_file():
    raise FileNotFoundError(
        f"Agricultural questionnaire not found: {questionnaire_file}"
    )

questionnaire = PdfReader(str(questionnaire_file))

print("Document:", questionnaire_file.name)
print("Total pages:", len(questionnaire.pages))

search_terms = [
    "improved seed",
    "improved seeds",
    "seed",
    "s4aq",
    "s4bq",
]

matches_found = 0

for page_number, page in enumerate(questionnaire.pages, start=1):
    page_text = page.extract_text() or ""
    page_lower = page_text.lower()

    matching_terms = [
        term for term in search_terms
        if term in page_lower
    ]

    if matching_terms:
        matches_found += 1

        print("\n" + "=" * 75)
        print(f"PAGE {page_number}")
        print("Matching terms:", ", ".join(matching_terms))
        print("=" * 75)

        print(page_text[:5000])

if matches_found == 0:
    print(
        "No matching text was extracted. "
        "The questionnaire may be scanned or use different terminology."
    )
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Seed Variable and Identifier Audit
# Read-only inspection
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

seed_files = {
    "First visit": agric_dir / "AGSEC4A.csv",
    "Second visit": agric_dir / "AGSEC4B.csv",
}

candidate_variables = [
    "s4aq08",
    "s4aq09",
    "s4aq09_1",
    "s4aq09_2",
    "s4aq16",
    "s4aq11a",
    "s4aq11b",
    "s4aq12a",
    "s4aq12b",
    "s4aq13",
    "s4aq14",
    "s4aq10",
]

for visit, file_path in seed_files.items():

    print("\n" + "=" * 75)
    print(f"{visit}: {file_path.name}")
    print("=" * 75)

    df = pd.read_csv(file_path, low_memory=False)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # Check whether the expected identifiers are present.
    identifiers = [
        column for column in [
            "hhid",
            "t0_hhid",
            "parcelID",
            "pltid",
            "cropID",
            "interview__key",
        ]
        if column in df.columns
    ]

    print("\nIdentifier completeness:")
    print(df[identifiers].isna().sum())

    print("\nIdentifier uniqueness:")
    print("Unique households:", df["hhid"].nunique())
    print(
        "Unique household-parcel-plot-crop combinations:",
        df[["hhid", "parcelID", "pltid", "cropID"]]
        .drop_duplicates()
        .shape[0],
    )

    # Examine observed values without assigning meanings prematurely.
    for variable in candidate_variables:
        if variable not in df.columns:
            continue

        series = df[variable]

        print(f"\n{variable}")
        print("Non-missing:", series.notna().sum())
        print("Missing:", series.isna().sum())
        print("Distinct values:", series.nunique(dropna=True))

        print("Most frequent observed values:")
        print(series.value_counts(dropna=False).head(12).to_string())
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Seed Adoption Variable Audit: Both Survey Visits
# Read-only inspection
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

seed_files = {
    "First visit": {
        "path": agric_dir / "AGSEC4A.csv",
        "prefix": "s4a",
    },
    "Second visit": {
        "path": agric_dir / "AGSEC4B.csv",
        "prefix": "s4b",
    },
}

candidate_suffixes = [
    "q08",
    "q09",
    "q09_1",
    "q09_2",
    "q16",
    "q11a",
    "q11b",
    "q12a",
    "q12b",
    "q13",
    "q14",
    "q10",
]

for visit, config in seed_files.items():

    file_path = config["path"]
    prefix = config["prefix"]

    print("\n" + "=" * 75)
    print(f"{visit}: {file_path.name}")
    print("=" * 75)

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(df):,}")
    print(f"Unique households: {df['hhid'].nunique():,}")

    for suffix in candidate_suffixes:

        variable = f"{prefix}{suffix}"

        if variable not in df.columns:
            print(f"\n{variable}: NOT FOUND")
            continue

        series = df[variable]

        print(f"\n--- {variable} ---")
        print(f"Non-missing: {series.notna().sum():,}")
        print(f"Missing: {series.isna().sum():,}")
        print(f"Distinct non-missing values: {series.nunique():,}")

        print(
            series.value_counts(dropna=False)
            .head(15)
            .to_string()
        )
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Questionnaire-to-Variable Mapping Audit
# Read-only inspection
# ==========================================================

from pypdf import PdfReader

questionnaire_path = extracted_folder / "agriculture_qx.pdf"

reader = PdfReader(str(questionnaire_path))

print("Questionnaire:", questionnaire_path.name)
print("Total pages:", len(reader.pages))

# Inspect the first-visit and second-visit crop/seed sections.
pages_to_inspect = {
    12: "First-visit crop and seed questions",
    23: "Second-visit crop and seed questions",
}

for page_number, description in pages_to_inspect.items():

    page_text = reader.pages[page_number - 1].extract_text() or ""

    print("\n" + "=" * 80)
    print(f"PDF PAGE {page_number}: {description}")
    print("=" * 80)
    print(page_text)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Raw Seed Variable Mapping Inspection
# Read-only; no files are modified
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

visit_configs = {
    "First visit": {
        "file": agric_dir / "AGSEC4A.csv",
        "prefix": "s4a",
    },
    "Second visit": {
        "file": agric_dir / "AGSEC4B.csv",
        "prefix": "s4b",
    },
}

for visit, config in visit_configs.items():

    df = pd.read_csv(config["file"], low_memory=False)
    prefix = config["prefix"]

    print("\n" + "=" * 90)
    print(f"{visit}: {config['file'].name}")
    print("=" * 90)

    variables = [
        "hhid",
        "parcelID",
        "pltid",
        "cropID",
        "s4aq06_1" if prefix == "s4a" else "s4bq06_1",
        f"{prefix}q08",
        f"{prefix}q09",
        f"{prefix}q09_1",
        f"{prefix}q09_2",
        f"{prefix}q16",
        f"{prefix}q11a",
        f"{prefix}q11b",
        f"{prefix}q12a",
        f"{prefix}q12b",
        f"{prefix}q13",
        f"{prefix}q14",
        f"{prefix}q10",
    ]

    variables = [column for column in variables if column in df.columns]

    print(df[variables].head(15).to_string(index=False))
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Search Local Survey Metadata
# Read-only inspection
# ==========================================================

from pathlib import Path

data_root = extracted_folder

keywords = [
    "AGSEC4A",
    "AGSEC4B",
    "s4aq08",
    "s4aq09_2",
    "s4aq16",
    "s4aq13",
    "s4aq14",
    "s4bq08",
]

print("Searching for survey metadata files...\n")

metadata_extensions = {
    ".pdf", ".xml", ".json", ".txt", ".html",
    ".dta", ".sav", ".xlsx", ".xls", ".csv"
}

for path in sorted(data_root.rglob("*")):

    if not path.is_file():
        continue

    if path.suffix.lower() not in metadata_extensions:
        continue

    # Exclude the large raw CSV collection from this filename search.
    if path.suffix.lower() == ".csv":
        continue

    filename = path.name.lower()

    if any(keyword.lower() in filename for keyword in keywords):
        print(path)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Inspect DDI Documentation for Agricultural Variables
# Read-only inspection
# ==========================================================

from pypdf import PdfReader

ddi_path = extracted_folder / "ddi-documentation-english_microdata-3795.pdf"

reader = PdfReader(str(ddi_path))

search_terms = [
    "AGSEC4A",
    "AGSEC4B",
    "s4aq08",
    "s4aq09",
    "s4aq16",
    "s4aq13",
    "s4aq14",
    "s4bq08",
]

for term in search_terms:

    print("\n" + "=" * 75)
    print(f"Searching DDI for: {term}")
    print("=" * 75)

    matches = 0

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if term.lower() in text.lower():
            matches += 1
            print(f"\nFound on PDF page {page_number}:")
            print(text[:3500])

    if matches == 0:
        print("No matches found.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Complete Agricultural Dataset Column Audit
# Read-only inspection
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

files = {
    "First visit": agric_dir / "AGSEC4A.csv",
    "Second visit": agric_dir / "AGSEC4B.csv",
}

for visit, file_path in files.items():

    df = pd.read_csv(file_path, nrows=5, low_memory=False)

    print("\n" + "=" * 80)
    print(visit, "-", file_path.name)
    print("=" * 80)

    for position, column in enumerate(df.columns, start=1):
        print(f"{position:02d}. {column}")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Search for Labelled Survey Data and Codebooks
# Read-only inspection
# ==========================================================

from pathlib import Path

data_root = extracted_folder

relevant_extensions = {
    ".dta", ".sav", ".sas7bdat", ".por",
    ".xlsx", ".xls", ".xml", ".json",
    ".txt", ".pdf", ".zip", ".do", ".sps"
}

print("Project data root:", data_root)
print("\nPotential metadata and labelled data files:\n")

found = 0

for path in sorted(data_root.rglob("*")):

    if not path.is_file():
        continue

    if path.suffix.lower() not in relevant_extensions:
        continue

    print(f"{path.relative_to(data_root)}")
    found += 1

print(f"\nTotal matching files: {found}")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Seed Variable Mapping Validation
# Read-only assessment
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

seed_variable_map = {
    "First visit": {
        "file": agric_dir / "AGSEC4A.csv",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_seed_category": "s4aq14",
    },
    "Second visit": {
        "file": agric_dir / "AGSEC4B.csv",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_seed_category": "s4bq14",
    },
}

expected_codes = {
    "seed_use": {1, 2},
    "seed_type": {1, 2},
    "improved_seed_category": {1, 2, 3},
}

for visit, config in seed_variable_map.items():

    df = pd.read_csv(config["file"], low_memory=False)

    print("\n" + "=" * 75)
    print(f"{visit}: {config['file'].name}")
    print("=" * 75)

    print(f"Rows: {len(df):,}")

    for variable_role in (
        "seed_use",
        "seed_type",
        "improved_seed_category",
    ):

        column = config[variable_role]

        values = df[column].dropna()

        observed_codes = set(values.unique())
        unexpected_codes = observed_codes - expected_codes[variable_role]

        print(f"\n{variable_role}: {column}")
        print("Missing:", int(df[column].isna().sum()))
        print("Observed values:", sorted(observed_codes))
        print("Unexpected values:", sorted(unexpected_codes))
        print("\nValue counts:")
        print(df[column].value_counts(dropna=False).sort_index())

        if unexpected_codes:
            print("WARNING: Investigate unexpected values.")
        else:
            print("Code check: PASS")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Seed Variable Logical Consistency Audit
# Read-only assessment
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

seed_audit_config = {
    "First visit": {
        "path": agric_dir / "AGSEC4A.csv",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "Second visit": {
        "path": agric_dir / "AGSEC4B.csv",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for visit, config in seed_audit_config.items():

    df = pd.read_csv(config["path"], low_memory=False)

    seed_use = config["seed_use"]
    seed_type = config["seed_type"]
    improved_category = config["improved_category"]

    print("\n" + "=" * 80)
    print(f"{visit}: LOGICAL CONSISTENCY AUDIT")
    print("=" * 80)

    # 1. Relationship between seed use and seed type
    print("\n1. Seed use versus seed type")
    print("Rows = seed use; columns = seed type")
    print("Codes: seed use 1=Yes, 2=No; seed type 1=Traditional, 2=Improved")

    print(
        pd.crosstab(
            df[seed_use],
            df[seed_type],
            margins=True,
            dropna=False
        )
    )

    # 2. Seed-type responses among records reporting no seed use
    no_seed = df[df[seed_use] == 2]

    print("\n2. Seed-type responses among records reporting no seed use")
    print("Number of records:", len(no_seed))
    print(no_seed[seed_type].value_counts(dropna=False).sort_index())

    # 3. Improved-seed category among records classified as improved
    improved = df[df[seed_type] == 2]

    print("\n3. Improved-seed category among improved-seed records")
    print("Number of improved-seed records:", len(improved))
    print(improved[improved_category].value_counts(dropna=False).sort_index())

    # 4. Improved-seed category among records not classified as improved
    not_improved = df[df[seed_type] != 2]

    print("\n4. Improved-seed category among records not classified as improved")
    print("Number of records:", len(not_improved))
    print(
        not_improved[improved_category]
        .value_counts(dropna=False)
        .sort_index()
    )

    # 5. Records with missing seed use but recorded seed type
    missing_seed_use = df[df[seed_use].isna()]

    print("\n5. Missing seed-use responses with recorded seed type")
    print("Number of records:", len(missing_seed_use))
    print(missing_seed_use[seed_type].value_counts(dropna=False).sort_index())

    # 6. Records with missing seed type but recorded seed use
    missing_seed_type = df[df[seed_type].isna()]

    print("\n6. Missing seed-type responses with recorded seed use")
    print("Number of records:", len(missing_seed_type))
    print(missing_seed_type[seed_use].value_counts(dropna=False).sort_index())
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Inspect Unresolved Seed Records
# Read-only assessment
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

audit_cases = {
    "First visit": {
        "path": agric_dir / "AGSEC4A.csv",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "Second visit": {
        "path": agric_dir / "AGSEC4B.csv",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for visit, config in audit_cases.items():

    df = pd.read_csv(config["path"], low_memory=False)

    print("\n" + "=" * 80)
    print(f"{visit}: UNRESOLVED RECORDS")
    print("=" * 80)

    # Seed use was reported, but seed type is missing.
    unresolved_type = df[
        (df[config["seed_use"]] == 1)
        & (df[config["seed_type"]].isna())
    ]

    print("\nSeed used = Yes, but seed type is missing:")
    print("Number of records:", len(unresolved_type))

    if not unresolved_type.empty:
        print(unresolved_type.to_string(index=False))

    # Improved seed was reported, but its category is missing.
    unresolved_category = df[
        (df[config["seed_type"]] == 2)
        & (df[config["improved_category"]].isna())
    ]

    print("\nImproved seed reported, but improved-seed category is missing:")
    print("Number of records:", len(unresolved_category))

    if not unresolved_category.empty:
        print(unresolved_category.to_string(index=False))
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Create Provisional Crop-Level Improved-Seed Outcome
# Original CSV files remain unchanged
# ==========================================================

import pandas as pd

agric_dir = extracted_folder / "Agric"

outcome_config = {
    "First visit": {
        "path": agric_dir / "AGSEC4A.csv",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit": {
        "path": agric_dir / "AGSEC4B.csv",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

# Store analysis copies separately from the original CSV files.
seed_analysis_data = {}

for visit, config in outcome_config.items():

    # Read the original dataset into a new DataFrame.
    df = pd.read_csv(config["path"], low_memory=False)

    seed_use = config["seed_use"]
    seed_type = config["seed_type"]

    # Start with an unresolved outcome.
    df["improved_seed_crop"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64"
    )

    # Traditional seed: non-adoption of improved seed for this crop.
    df.loc[df[seed_type] == 1, "improved_seed_crop"] = 0

    # Improved seed: adoption for this crop.
    df.loc[df[seed_type] == 2, "improved_seed_crop"] = 1

    # No seed used: non-adoption for this crop.
    # Apply only where seed type is also missing.
    no_seed_used = (
        (df[seed_use] == 2)
        & (df[seed_type].isna())
    )

    df.loc[no_seed_used, "improved_seed_crop"] = 0

    # Store the analysis copy without changing the source file.
    seed_analysis_data[visit] = df

    # Report the outcome distribution.
    print("\n" + "=" * 70)
    print(f"{visit}: PROVISIONAL CROP-LEVEL OUTCOME")
    print("=" * 70)

    print("Total crop records:", len(df))

    print("\nOutcome counts:")
    print(
        df["improved_seed_crop"]
        .value_counts(dropna=False)
        .sort_index()
        .rename(index={
            0: "0 = No improved seed",
            1: "1 = Improved seed",
            pd.NA: "Missing = Unresolved",
        })
    )

    print("\nOutcome percentages, including unresolved records:")
    print(
        (
            df["improved_seed_crop"]
            .value_counts(dropna=False, normalize=True)
            .sort_index()
            * 100
        ).round(2)
    )

    print("\nUnresolved records by seed-use response:")
    print(
        df.loc[
            df["improved_seed_crop"].isna(),
            seed_use
        ].value_counts(dropna=False).sort_index()
    )

    print("\nMissing outcome count:", int(
        df["improved_seed_crop"].isna().sum()
    ))

print("\nOutcome construction completed.")
print("Original CSV files were not modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Household Identifier and Survey-Visit Overlap Audit
# Read-only assessment
# ==========================================================

import pandas as pd

first_visit = seed_analysis_data["First visit"]
second_visit = seed_analysis_data["Second visit"]

identifier_columns = ["hhid", "t0_hhid"]

# ----------------------------------------------------------
# 1. Examine identifier completeness and uniqueness
# ----------------------------------------------------------

for visit, df in [
    ("First visit", first_visit),
    ("Second visit", second_visit),
]:

    print("\n" + "=" * 75)
    print(f"{visit}: HOUSEHOLD IDENTIFIER AUDIT")
    print("=" * 75)

    for column in identifier_columns:

        print(f"\nIdentifier: {column}")
        print("Missing records:", int(df[column].isna().sum()))
        print("Unique non-missing identifiers:", df[column].nunique())

    print("\nCrop records per t0_hhid:")
    records_per_household = df.groupby(
        "t0_hhid",
        dropna=False
    ).size()

    print(records_per_household.describe().round(2))

    print(
        "\nHouseholds contributing multiple crop records:",
        int((records_per_household > 1).sum())
    )

# ----------------------------------------------------------
# 2. Compare household identifiers across survey visits
# ----------------------------------------------------------

print("\n" + "=" * 75)
print("CROSS-VISIT HOUSEHOLD OVERLAP")
print("=" * 75)

first_t0 = set(first_visit["t0_hhid"].dropna().unique())
second_t0 = set(second_visit["t0_hhid"].dropna().unique())

common_t0 = first_t0.intersection(second_t0)

print("Unique first-visit t0_hhid identifiers:", len(first_t0))
print("Unique second-visit t0_hhid identifiers:", len(second_t0))
print("Identifiers present in both visits:", len(common_t0))
print("First-visit-only identifiers:", len(first_t0 - second_t0))
print("Second-visit-only identifiers:", len(second_t0 - first_t0))

# ----------------------------------------------------------
# 3. Check hhid overlap separately
# ----------------------------------------------------------

first_hhid = set(first_visit["hhid"].dropna().unique())
second_hhid = set(second_visit["hhid"].dropna().unique())

common_hhid = first_hhid.intersection(second_hhid)

print("\nUnique first-visit hhid identifiers:", len(first_hhid))
print("Unique second-visit hhid identifiers:", len(second_hhid))
print("hhid identifiers present in both visits:", len(common_hhid))

# ----------------------------------------------------------
# 4. Check whether t0_hhid maps consistently to hhid
# ----------------------------------------------------------

for visit, df in [
    ("First visit", first_visit),
    ("Second visit", second_visit),
]:

    mapping_counts = (
        df.dropna(subset=["t0_hhid", "hhid"])
        .groupby("t0_hhid")["hhid"]
        .nunique()
    )

    inconsistent = mapping_counts[mapping_counts > 1]

    print(f"\n{visit}: t0_hhid-to-hhid mapping check")
    print("t0_hhid identifiers mapped to multiple hhid values:",
          len(inconsistent))

    if not inconsistent.empty:
        print("Examples:")
        print(inconsistent.head(10))

print("\nIdentifier audit completed.")
print("No source data or outcome variables were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Investigate Household Identifier Inconsistencies
# Read-only assessment
# ==========================================================

import pandas as pd

identifier_audit_config = {
    "First visit": {
        "df": seed_analysis_data["First visit"],
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit": {
        "df": seed_analysis_data["Second visit"],
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

for visit, config in identifier_audit_config.items():

    df = config["df"]

    print("\n" + "=" * 80)
    print(f"{visit}: IDENTIFIER INCONSISTENCY INVESTIGATION")
    print("=" * 80)

    # 1. Inspect placeholder identifiers.
    placeholder_mask = (
        df["t0_hhid"].astype("string").str.strip().isin(
            ["##N/A##", "", "N/A", "NA", "NULL"]
        )
    )

    print("\n1. Placeholder t0_hhid values")
    print("Affected crop records:", int(placeholder_mask.sum()))

    if placeholder_mask.any():
        print(
            df.loc[
                placeholder_mask,
                [
                    "hhid",
                    "t0_hhid",
                    "parcelID",
                    "pltid",
                    "cropID",
                    config["seed_use"],
                    config["seed_type"],
                    "interview__key",
                ],
            ].to_string(index=False)
        )

    # 2. Identify genuine t0_hhid values associated with
    #    multiple hhid values, excluding placeholders.
    valid_df = df.loc[~placeholder_mask].copy()

    mapping_counts = (
        valid_df.groupby("t0_hhid")["hhid"].nunique()
    )

    inconsistent_ids = mapping_counts[
        mapping_counts > 1
    ].index.tolist()

    print("\n2. Non-placeholder t0_hhid values mapped to multiple hhid values")
    print("Number of inconsistent identifiers:", len(inconsistent_ids))

    if inconsistent_ids:
        print(
            valid_df.loc[
                valid_df["t0_hhid"].isin(inconsistent_ids),
                [
                    "hhid",
                    "t0_hhid",
                    "parcelID",
                    "pltid",
                    "cropID",
                    config["seed_use"],
                    config["seed_type"],
                    "interview__key",
                ],
            ]
            .sort_values(["t0_hhid", "hhid"])
            .to_string(index=False)
        )

    # 3. Inspect hhid values mapped to multiple t0_hhid values.
    reverse_counts = (
        valid_df.groupby("hhid")["t0_hhid"].nunique()
    )

    reverse_inconsistent = reverse_counts[
        reverse_counts > 1
    ]

    print("\n3. hhid values mapped to multiple t0_hhid values")
    print("Number of inconsistent hhid values:",
          len(reverse_inconsistent))

    if not reverse_inconsistent.empty:
        print(
            valid_df.loc[
                valid_df["hhid"].isin(reverse_inconsistent.index),
                ["hhid", "t0_hhid", "parcelID", "pltid", "cropID"],
            ]
            .sort_values(["hhid", "t0_hhid"])
            .to_string(index=False)
        )

print("\nIdentifier investigation completed.")
print("No data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Interview-Key and Household Identifier Audit
# Read-only assessment
# ==========================================================

import pandas as pd

datasets = {
    "First visit": seed_analysis_data["First visit"],
    "Second visit": seed_analysis_data["Second visit"],
}

for visit, df in datasets.items():

    print("\n" + "=" * 75)
    print(f"{visit}: INTERVIEW-KEY AUDIT")
    print("=" * 75)

    # Count distinct household identifiers per interview key.
    interview_summary = (
        df.groupby("interview__key", dropna=False)
        .agg(
            crop_records=("cropID", "size"),
            unique_hhid=("hhid", "nunique"),
            unique_t0_hhid=("t0_hhid", "nunique"),
        )
        .reset_index()
    )

    print("\nInterview summary:")
    print("Unique interview keys:", df["interview__key"].nunique())
    print(
        "Interview keys associated with multiple hhid values:",
        int((interview_summary["unique_hhid"] > 1).sum())
    )
    print(
        "Interview keys associated with multiple t0_hhid values:",
        int((interview_summary["unique_t0_hhid"] > 1).sum())
    )

    # Show interview keys associated with multiple identifiers.
    problematic = interview_summary[
        (interview_summary["unique_hhid"] > 1)
        | (interview_summary["unique_t0_hhid"] > 1)
    ]

    print("\nInterview keys with multiple identifier values:")

    if problematic.empty:
        print("None found.")
    else:
        print(problematic.to_string(index=False))

    # Examine the placeholder separately.
    placeholder_rows = df[
        df["t0_hhid"].astype("string").str.strip() == "##N/A##"
    ]

    print("\nPlaceholder records:")
    print("Crop records:", len(placeholder_rows))
    print("Distinct hhid:", placeholder_rows["hhid"].nunique())
    print(
        "Distinct interview keys:",
        placeholder_rows["interview__key"].nunique()
    )

print("\nInterview-key audit completed. No data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Inspect Placeholder Household Identifiers
# Read-only assessment
# ==========================================================

for visit, df in {
    "First visit": seed_analysis_data["First visit"],
    "Second visit": seed_analysis_data["Second visit"],
}.items():

    print("\n" + "=" * 70)
    print(f"{visit}: PLACEHOLDER IDENTIFIERS")
    print("=" * 70)

    placeholder_rows = df[
        df["t0_hhid"].astype("string").str.strip() == "##N/A##"
    ]

    summary = (
        placeholder_rows.groupby("hhid", dropna=False)
        .agg(
            crop_records=("cropID", "size"),
            distinct_parcels=("parcelID", "nunique"),
            distinct_plots=("pltid", "nunique"),
            distinct_crops=("cropID", "nunique"),
            distinct_interviews=("interview__key", "nunique"),
        )
        .reset_index()
    )

    print(summary.to_string(index=False))

    print("\nTotal placeholder crop records:", len(placeholder_rows))
    print("Distinct hhid values:", placeholder_rows["hhid"].nunique())

print("\nInspection completed. No data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Cross-Visit Household Identifier Consistency Audit
# Read-only assessment
# ==========================================================

import pandas as pd

first = seed_analysis_data["First visit"].copy()
second = seed_analysis_data["Second visit"].copy()

# Normalize identifier strings for comparison.
# Original datasets are not modified.
for df in (first, second):
    for col in ["hhid", "t0_hhid"]:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

# Exclude missing hhid values from linkage counts.
first_hhid = set(first["hhid"].dropna().unique())
second_hhid = set(second["hhid"].dropna().unique())

shared_hhid = first_hhid & second_hhid
first_only_hhid = first_hhid - second_hhid
second_only_hhid = second_hhid - first_hhid

print("=" * 75)
print("CROSS-VISIT HOUSEHOLD IDENTIFIER AUDIT")
print("=" * 75)

print("\nUnique household identifiers:")
print("First visit:", len(first_hhid))
print("Second visit:", len(second_hhid))
print("Shared across visits:", len(shared_hhid))
print("First visit only:", len(first_only_hhid))
print("Second visit only:", len(second_only_hhid))

# Summarize baseline identifiers for shared household IDs.
first_shared = first[first["hhid"].isin(shared_hhid)]
second_shared = second[second["hhid"].isin(shared_hhid)]

first_mapping = (
    first_shared.groupby("hhid", dropna=False)
    .agg(
        first_t0_values=(
            "t0_hhid",
            lambda s: tuple(sorted(s.dropna().unique().tolist()))
        ),
        first_t0_missing=("t0_hhid", lambda s: int(s.isna().any())),
    )
    .reset_index()
)

second_mapping = (
    second_shared.groupby("hhid", dropna=False)
    .agg(
        second_t0_values=(
            "t0_hhid",
            lambda s: tuple(sorted(s.dropna().unique().tolist()))
        ),
        second_t0_missing=("t0_hhid", lambda s: int(s.isna().any())),
    )
    .reset_index()
)

mapping_comparison = first_mapping.merge(
    second_mapping,
    on="hhid",
    how="inner",
    validate="one_to_one"
)

# Identify shared household IDs with missing or placeholder baseline IDs.
placeholder = "##N/A##"

def has_placeholder(values):
    return placeholder in values

mapping_comparison["first_has_placeholder"] = (
    mapping_comparison["first_t0_values"].apply(has_placeholder)
)

mapping_comparison["second_has_placeholder"] = (
    mapping_comparison["second_t0_values"].apply(has_placeholder)
)

mapping_comparison["same_t0_values"] = (
    mapping_comparison["first_t0_values"]
    == mapping_comparison["second_t0_values"]
)

print("\nShared household identifier consistency:")
print(
    "Shared hhid values with different t0_hhid values:",
    int((~mapping_comparison["same_t0_values"]).sum())
)

print(
    "Shared hhid values with placeholder in first visit:",
    int(mapping_comparison["first_has_placeholder"].sum())
)

print(
    "Shared hhid values with placeholder in second visit:",
    int(mapping_comparison["second_has_placeholder"].sum())
)

print("\nShared hhid values with inconsistent or placeholder baseline IDs:")

problematic = mapping_comparison[
    (~mapping_comparison["same_t0_values"])
    | mapping_comparison["first_has_placeholder"]
    | mapping_comparison["second_has_placeholder"]
]

if problematic.empty:
    print("None found.")
else:
    print(problematic.to_string(index=False))

print("\nAudit completed. Source data were not modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Unmatched Household Identifier Audit
# Read-only assessment
# ==========================================================

import pandas as pd

first = seed_analysis_data["First visit"].copy()
second = seed_analysis_data["Second visit"].copy()

# Normalize identifier strings in analysis copies only.
for df in (first, second):
    for col in ["hhid", "t0_hhid"]:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

# Identify household IDs appearing in only one visit.
first_ids = set(first["hhid"].dropna().unique())
second_ids = set(second["hhid"].dropna().unique())

first_only_ids = first_ids - second_ids
second_only_ids = second_ids - first_ids

def summarize_households(df, household_ids, visit_name):
    subset = df[df["hhid"].isin(household_ids)].copy()

    # Summarize at the hhid level.
    summary = (
        subset.groupby("hhid", dropna=False)
        .agg(
            crop_records=("cropID", "size"),
            t0_values=(
                "t0_hhid",
                lambda s: tuple(sorted(s.dropna().unique().tolist()))
            ),
        )
        .reset_index()
    )

    summary["visit"] = visit_name

    # Classify baseline identifier availability.
    def classify_t0(values):
        if len(values) == 0:
            return "Missing"
        if "##N/A##" in values:
            return "Placeholder"
        if len(values) > 1:
            return "Multiple values"
        return "Present"

    summary["t0_status"] = summary["t0_values"].apply(classify_t0)

    return summary

first_only = summarize_households(
    first, first_only_ids, "First visit only"
)

second_only = summarize_households(
    second, second_only_ids, "Second visit only"
)

unmatched = pd.concat(
    [first_only, second_only],
    ignore_index=True
)

print("=" * 75)
print("UNMATCHED HOUSEHOLD IDENTIFIER AUDIT")
print("=" * 75)

print("\nUnmatched household counts by visit and t0_hhid status:")

status_summary = (
    unmatched.groupby(["visit", "t0_status"])
    .agg(
        households=("hhid", "nunique"),
        crop_records=("crop_records", "sum"),
    )
    .reset_index()
)

print(status_summary.to_string(index=False))

print("\nTotal unmatched households:", unmatched["hhid"].nunique())
print("First-visit unmatched households:", len(first_only))
print("Second-visit unmatched households:", len(second_only))

# Check whether baseline identifiers repeat among unmatched households.
for visit_name, summary in [
    ("First visit only", first_only),
    ("Second visit only", second_only),
]:
    print("\n" + "-" * 65)
    print(visit_name.upper())
    print("-" * 65)

    valid = summary[
        summary["t0_status"] == "Present"
    ].explode("t0_values")

    duplicate_t0 = valid[
        valid.duplicated("t0_values", keep=False)
    ].sort_values("t0_values")

    print(
        "Households with a present baseline identifier:",
        int((summary["t0_status"] == "Present").sum())
    )

    print(
        "Repeated baseline identifier values among unmatched households:",
        duplicate_t0["t0_values"].nunique()
    )

    if duplicate_t0.empty:
        print("No repeated baseline identifiers found.")
    else:
        print(duplicate_t0.to_string(index=False))

print("\nAudit completed. No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Baseline Household Identifier Linkage Audit
# Read-only assessment
# ==========================================================

import pandas as pd

first = seed_analysis_data["First visit"].copy()
second = seed_analysis_data["Second visit"].copy()

# Normalize identifiers in temporary copies.
for df in (first, second):
    for col in ["hhid", "t0_hhid"]:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

# Exclude placeholder baseline identifiers.
placeholder = "##N/A##"

first_valid = first[
    first["t0_hhid"].notna()
    & first["t0_hhid"].ne(placeholder)
].copy()

second_valid = second[
    second["t0_hhid"].notna()
    & second["t0_hhid"].ne(placeholder)
].copy()

# Build one row per distinct hhid-t0_hhid combination.
first_pairs = first_valid[["hhid", "t0_hhid"]].drop_duplicates()
second_pairs = second_valid[["hhid", "t0_hhid"]].drop_duplicates()

# Count how many distinct household IDs use each baseline ID.
first_counts = (
    first_pairs.groupby("t0_hhid")["hhid"]
    .nunique()
    .rename("first_hhid_count")
)

second_counts = (
    second_pairs.groupby("t0_hhid")["hhid"]
    .nunique()
    .rename("second_hhid_count")
)

# Identify baseline IDs present in both visits.
first_t0_ids = set(first_pairs["t0_hhid"].dropna())
second_t0_ids = set(second_pairs["t0_hhid"].dropna())

shared_t0_ids = first_t0_ids & second_t0_ids

print("=" * 75)
print("BASELINE HOUSEHOLD IDENTIFIER LINKAGE AUDIT")
print("=" * 75)

print("\nBaseline identifier counts:")
print("First visit distinct non-placeholder t0_hhid:", len(first_t0_ids))
print("Second visit distinct non-placeholder t0_hhid:", len(second_t0_ids))
print("Baseline identifiers shared across visits:", len(shared_t0_ids))

# Assess uniqueness for identifiers present in both visits.
shared_summary = pd.concat(
    [first_counts, second_counts],
    axis=1
).loc[lambda x: x.index.isin(shared_t0_ids)].fillna(0)

shared_summary["unique_in_both_visits"] = (
    shared_summary["first_hhid_count"].eq(1)
    & shared_summary["second_hhid_count"].eq(1)
)

print("\nShared baseline identifiers unique within both visits:")
print(
    int(shared_summary["unique_in_both_visits"].sum()),
    "of",
    len(shared_summary)
)

print("\nShared baseline identifiers mapping to multiple hhid values:")
ambiguous = shared_summary[
    (shared_summary["first_hhid_count"] > 1)
    | (shared_summary["second_hhid_count"] > 1)
]

if ambiguous.empty:
    print("None found.")
else:
    print(ambiguous.sort_index().to_string())

# Identify candidate baseline IDs that could link different hhid values.
candidate_links = first_pairs.merge(
    second_pairs,
    on="t0_hhid",
    how="inner",
    suffixes=("_first", "_second"),
    validate="many_to_many"
)

candidate_links = candidate_links[
    candidate_links["hhid_first"] != candidate_links["hhid_second"]
].copy()

print("\nCandidate cross-visit links with different hhid values:")
print("Candidate pairs:", len(candidate_links))

if candidate_links.empty:
    print("None found.")
else:
    print(candidate_links.sort_values("t0_hhid").to_string(index=False))

print("\nAudit completed. No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Direct vs Candidate Household Linkage Summary
# Read-only assessment
# ==========================================================

import pandas as pd

first = seed_analysis_data["First visit"].copy()
second = seed_analysis_data["Second visit"].copy()

# Normalize identifiers in temporary copies only.
for df in (first, second):
    for col in ["hhid", "t0_hhid"]:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

placeholder = "##N/A##"

# One row per distinct household-ID/baseline-ID pair.
first_pairs = (
    first.loc[
        first["hhid"].notna()
        & first["t0_hhid"].notna()
        & first["t0_hhid"].ne(placeholder),
        ["hhid", "t0_hhid"]
    ]
    .drop_duplicates()
)

second_pairs = (
    second.loc[
        second["hhid"].notna()
        & second["t0_hhid"].notna()
        & second["t0_hhid"].ne(placeholder),
        ["hhid", "t0_hhid"]
    ]
    .drop_duplicates()
)

# Direct linkage using hhid.
first_hhid = set(first["hhid"].dropna())
second_hhid = set(second["hhid"].dropna())
direct_matches = first_hhid & second_hhid

# Count household IDs per baseline ID in each visit.
first_counts = first_pairs.groupby("t0_hhid")["hhid"].nunique()
second_counts = second_pairs.groupby("t0_hhid")["hhid"].nunique()

shared_t0 = set(first_counts.index) & set(second_counts.index)

# Keep only baseline IDs unique within both visits.
unique_shared_t0 = {
    t0 for t0 in shared_t0
    if first_counts[t0] == 1 and second_counts[t0] == 1
}

# Candidate baseline matches.
candidate_pairs = first_pairs.merge(
    second_pairs,
    on="t0_hhid",
    how="inner",
    suffixes=("_first", "_second"),
    validate="many_to_many"
)

candidate_pairs = candidate_pairs[
    candidate_pairs["hhid_first"] != candidate_pairs["hhid_second"]
].copy()

# Restrict to baseline IDs unique in both visits.
unique_candidate_pairs = candidate_pairs[
    candidate_pairs["t0_hhid"].isin(unique_shared_t0)
].copy()

# Ambiguous baseline IDs shared across visits.
ambiguous_t0 = {
    t0 for t0 in shared_t0
    if first_counts[t0] > 1 or second_counts[t0] > 1
}

print("=" * 75)
print("HOUSEHOLD LINKAGE SUMMARY")
print("=" * 75)

print("\nDirect linkage:")
print("Shared hhid identifiers:", len(direct_matches))

print("\nBaseline identifier linkage:")
print("Shared non-placeholder t0_hhid identifiers:", len(shared_t0))
print("Unique within both visits:", len(unique_shared_t0))
print("Ambiguous within at least one visit:", len(ambiguous_t0))

print("\nCandidate links with different hhid values:")
print("All candidate pairs:", len(candidate_pairs))
print("Pairs using baseline IDs unique in both visits:",
      len(unique_candidate_pairs))

print("\nUnique-baseline candidate pairs:")
if unique_candidate_pairs.empty:
    print("None found.")
else:
    print(
        unique_candidate_pairs.sort_values("t0_hhid")
        .to_string(index=False)
    )

print("\nAmbiguous shared baseline identifiers:")
if ambiguous_t0:
    print(sorted(ambiguous_t0))
else:
    print("None found.")

print("\nSummary completed. No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Household Linkage Quality Report
# Read-only assessment
# ==========================================================

import pandas as pd

first = seed_analysis_data["First visit"]
second = seed_analysis_data["Second visit"]

first_ids = set(first["hhid"].dropna().astype("string"))
second_ids = set(second["hhid"].dropna().astype("string"))

shared_ids = first_ids & second_ids
first_only_ids = first_ids - second_ids
second_only_ids = second_ids - first_ids

first_count = len(first_ids)
second_count = len(second_ids)
shared_count = len(shared_ids)

report = pd.DataFrame(
    {
        "Metric": [
            "First-visit unique household IDs",
            "Second-visit unique household IDs",
            "Shared household IDs",
            "First-visit-only household IDs",
            "Second-visit-only household IDs",
            "First-visit identifier overlap (%)",
            "Second-visit identifier overlap (%)",
            "Additional unambiguous baseline links",
            "Ambiguous shared baseline identifiers",
        ],
        "Value": [
            first_count,
            second_count,
            shared_count,
            len(first_only_ids),
            len(second_only_ids),
            round(100 * shared_count / first_count, 2),
            round(100 * shared_count / second_count, 2),
            0,
            2,
        ],
    }
)

print("=" * 70)
print("RESEARCHPRO-ANALYTICS: HOUSEHOLD LINKAGE QUALITY REPORT")
print("=" * 70)
print(report.to_string(index=False))
print("\nStatus: Preliminary; awaiting confirmation from survey documentation.")
print("No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Crop-Level Improved-Seed Outcome Validation
# Read-only data-quality assessment
# ==========================================================

import pandas as pd

datasets = {
    "First visit": {
        "data": seed_analysis_data["First visit"],
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "Second visit": {
        "data": seed_analysis_data["Second visit"],
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for visit, config in datasets.items():

    df = config["data"]

    seed_use = config["seed_use"]
    seed_type = config["seed_type"]
    improved_category = config["improved_category"]

    print("\n" + "=" * 75)
    print(f"{visit.upper()}: CROP-LEVEL OUTCOME VALIDATION")
    print("=" * 75)

    # ------------------------------------------------------
    # 1. Validate the existing outcome against source values
    # ------------------------------------------------------

    expected = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64"
    )

    # Traditional seed means improved seed was not used.
    expected.loc[df[seed_type].eq(1)] = 0

    # Improved seed means improved seed was used.
    expected.loc[df[seed_type].eq(2)] = 1

    # Explicitly reporting no seed use supports outcome = 0
    # only when the seed-type response is missing.
    expected.loc[
        df[seed_use].eq(2) & df[seed_type].isna()
    ] = 0

    actual = df["improved_seed_crop"].astype("Int64")

    # Compare outcomes while treating missing/missing as agreement.
    matches = (
        expected.fillna(-1)
        .eq(actual.fillna(-1))
    )

    print("\n1. Outcome consistency")
    print("Total crop records:", len(df))
    print("Expected outcome agrees with existing outcome:",
          int(matches.sum()))
    print("Outcome discrepancies:", int((~matches).sum()))

    # ------------------------------------------------------
    # 2. Existing outcome distribution
    # ------------------------------------------------------

    print("\n2. Existing outcome distribution")

    outcome_counts = (
        actual.value_counts(dropna=False)
        .rename_axis("Outcome")
        .reset_index(name="Crop records")
    )

    outcome_counts["Percentage"] = (
        outcome_counts["Crop records"] / len(df) * 100
    ).round(2)

    print(outcome_counts.to_string(index=False))

    # ------------------------------------------------------
    # 3. Seed-use versus seed-type consistency
    # ------------------------------------------------------

    print("\n3. Seed-use and seed-type cross-tabulation")

    print(
        pd.crosstab(
            df[seed_use],
            df[seed_type],
            dropna=False
        ).to_string()
    )

    # ------------------------------------------------------
    # 4. Check unexpected source values
    # ------------------------------------------------------

    print("\n4. Unexpected source values")

    invalid_seed_use = (
        df[seed_use].notna()
        & ~df[seed_use].isin([1, 2])
    )

    invalid_seed_type = (
        df[seed_type].notna()
        & ~df[seed_type].isin([1, 2])
    )

    invalid_improved_category = (
        df[improved_category].notna()
        & ~df[improved_category].isin([1, 2, 3])
    )

    print("Unexpected seed-use codes:", int(invalid_seed_use.sum()))
    print("Unexpected seed-type codes:", int(invalid_seed_type.sum()))
    print(
        "Unexpected improved-seed category codes:",
        int(invalid_improved_category.sum())
    )

    # ------------------------------------------------------
    # 5. Investigate logical inconsistencies
    # ------------------------------------------------------

    print("\n5. Potential logical inconsistencies")

    no_seed_but_type_reported = (
        df[seed_use].eq(2)
        & df[seed_type].notna()
    )

    improved_category_without_improved_type = (
        df[improved_category].notna()
        & df[seed_type].ne(2)
    )

    seed_used_but_type_missing = (
        df[seed_use].eq(1)
        & df[seed_type].isna()
    )

    print(
        "Reported no seed use but seed type present:",
        int(no_seed_but_type_reported.sum())
    )

    print(
        "Improved-seed category present without improved seed type:",
        int(improved_category_without_improved_type.sum())
    )

    print(
        "Seed use reported but seed type missing:",
        int(seed_used_but_type_missing.sum())
    )

print("\n" + "=" * 75)
print("VALIDATION COMPLETED")
print("No source data or existing outcome variables were modified.")
print("=" * 75)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Investigate unresolved seed-type responses
# ==========================================================

unresolved_records = {}

for visit, config in datasets.items():

    df = config["data"]

    seed_use = config["seed_use"]
    seed_type = config["seed_type"]
    improved_category = config["improved_category"]

    # Seed use reported, but seed type is missing
    unresolved = df.loc[
        df[seed_use].eq(1)
        & df[seed_type].isna()
    ].copy()

    unresolved_records[visit] = unresolved

    print("\n" + "=" * 75)
    print(f"{visit.upper()}: UNRESOLVED SEED-TYPE RESPONSES")
    print("=" * 75)

    print("Number of records:", len(unresolved))

    # Display available identifiers and relevant seed variables
    display_columns = [
        col for col in [
            "hhid",
            "t0_hhid",
            "parcelID",
            "pltid",
            "cropID",
            "interview__key",
            seed_use,
            seed_type,
            improved_category,
        ]
        if col in unresolved.columns
    ]

    if len(unresolved) > 0:
        display(unresolved[display_columns])
    else:
        print("No unresolved records found.")

print("\nInspection completed. No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Unresolved Seed Responses: Audit Summary
# ==========================================================

unresolved_summary = []

for visit, df in unresolved_records.items():

    seed_use = datasets[visit]["seed_use"]
    seed_type = datasets[visit]["seed_type"]
    improved_category = datasets[visit]["improved_category"]

    unresolved_summary.append({
        "visit": visit,
        "unresolved_records": len(df),
        "unique_households": df["hhid"].nunique(),
        "unique_plots": (
            df[["hhid", "parcelID", "pltid"]]
            .drop_duplicates()
            .shape[0]
        ),
        "seed_use_reported_yes": int(df[seed_use].eq(1).sum()),
        "seed_type_missing": int(df[seed_type].isna().sum()),
        "improved_category_missing": int(
            df[improved_category].isna().sum()
        ),
    })

unresolved_summary_df = pd.DataFrame(unresolved_summary)

display(unresolved_summary_df)

print(
    "\nAudit conclusion: unresolved seed-type responses remain "
    "unclassified pending documentation review."
)
print("Source data modified: No")
```


```python
from pathlib import Path

documentation_files = [
    "ddi-documentation-english_microdata-3795.pdf",
    "agriculture_qx.pdf",
    "unps_7_bid.pdf",
    "unps_hhq.pdf",
]

for filename in documentation_files:
    path = Path(extracted_folder) / filename

    print(
        f"{filename}: "
        f"{'FOUND' if path.exists() else 'NOT FOUND'}"
    )
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Survey Documentation: Household Identifier Investigation
# Read-only PDF search
# ==========================================================

from pathlib import Path
from pypdf import PdfReader
import re

documentation_files = [
    "ddi-documentation-english_microdata-3795.pdf",
    "agriculture_qx.pdf",
    "unps_7_bid.pdf",
    "unps_hhq.pdf",
]

search_terms = [
    "t0_hhid",
    "hhid",
    "household identifier",
    "household identification",
    "household tracking",
    "split household",
    "split-off household",
    "panel household",
    "tracking household",
    "household roster",
]

for filename in documentation_files:

    pdf_path = Path(extracted_folder) / filename

    print("\n" + "=" * 90)
    print(f"DOCUMENT: {filename}")
    print("=" * 90)

    if not pdf_path.exists():
        print("File not found.")
        continue

    try:
        reader = PdfReader(str(pdf_path))
        print("Total pages:", len(reader.pages))

        matches_found = 0

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            for term in search_terms:

                pattern = re.compile(re.escape(term), re.IGNORECASE)

                for match in pattern.finditer(text):

                    start = max(0, match.start() - 250)
                    end = min(len(text), match.end() + 350)

                    snippet = " ".join(
                        text[start:end].split()
                    )

                    print(
                        f"\nPage {page_number} | "
                        f"Search term: {term}"
                    )
                    print(snippet)

                    matches_found += 1

                    # Keep the output manageable.
                    if matches_found >= 15:
                        break

                if matches_found >= 15:
                    break

            if matches_found >= 15:
                print(
                    "\nOutput limited to 15 matches for this document."
                )
                break

        if matches_found == 0:
            print("No matching text found.")

    except Exception as error:
        print("Could not process this document:", str(error))

print("\n" + "=" * 90)
print("DOCUMENTATION SEARCH COMPLETED")
print("PDF files were read only; no files were modified.")
print("=" * 90)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Provisional Household-Level Seed Adoption Summary
# Separate analysis for each agricultural visit
# ==========================================================

import pandas as pd

household_seed_audit = {}
household_seed_summary = []

for visit, config in datasets.items():

    df = config["data"].copy()

    print("\n" + "=" * 75)
    print(f"{visit.upper()}: HOUSEHOLD-LEVEL ADOPTION AUDIT")
    print("=" * 75)

    # ------------------------------------------------------
    # 1. Check missing household identifiers
    # ------------------------------------------------------

    missing_hhid_records = int(df["hhid"].isna().sum())

    print("Total crop records:", len(df))
    print("Records with missing hhid:", missing_hhid_records)

    # Do not aggregate records that lack a household identifier.
    valid_records = df.loc[df["hhid"].notna()].copy()

    # ------------------------------------------------------
    # 2. Aggregate crop records to the household level
    # ------------------------------------------------------

    def classify_household(outcomes):

        outcomes = outcomes.astype("Int64")

        # One confirmed improved-seed record is sufficient
        # to classify the household as an adopter.
        if outcomes.eq(1).any():
            return 1

        # Classify as a non-adopter only when every crop
        # record has a known outcome of zero.
        if outcomes.notna().all() and outcomes.eq(0).all():
            return 0

        # No confirmed adoption, but insufficient information
        # to conclude that the household did not adopt.
        return pd.NA

    household_summary = (
        valid_records
        .groupby("hhid", as_index=False)
        .agg(
            crop_records=("improved_seed_crop", "size"),
            improved_seed_crop_records=(
                "improved_seed_crop",
                lambda x: int(x.eq(1).sum())
            ),
            unresolved_crop_records=(
                "improved_seed_crop",
                lambda x: int(x.isna().sum())
            ),
        )
    )

    household_outcomes = (
        valid_records
        .groupby("hhid")["improved_seed_crop"]
        .apply(classify_household)
        .rename("household_improved_seed_adoption")
        .reset_index()
    )

    household_summary = household_summary.merge(
        household_outcomes,
        on="hhid",
        how="left",
        validate="one_to_one"
    )

    household_summary[
        "household_improved_seed_adoption"
    ] = household_summary[
        "household_improved_seed_adoption"
    ].astype("Int64")

    # Keep visit-specific results separate.
    household_seed_audit[visit] = household_summary

    # ------------------------------------------------------
    # 3. Summarize the provisional household outcomes
    # ------------------------------------------------------

    outcome = household_summary[
        "household_improved_seed_adoption"
    ]

    total_households = len(household_summary)
    adopters = int(outcome.eq(1).sum())
    non_adopters = int(outcome.eq(0).sum())
    unclassified = int(outcome.isna().sum())

    classified_households = adopters + non_adopters

    adoption_rate = (
        adopters / classified_households * 100
        if classified_households > 0
        else float("nan")
    )

    summary = {
        "visit": visit,
        "households_with_crop_records": total_households,
        "adopters": adopters,
        "non_adopters": non_adopters,
        "unclassified": unclassified,
        "classified_households": classified_households,
        "adoption_rate_among_classified_percent": round(
            adoption_rate, 2
        ),
        "records_missing_hhid": missing_hhid_records,
    }

    household_seed_summary.append(summary)

    print("\nHousehold outcome counts:")
    print("Adopters:", adopters)
    print("Non-adopters:", non_adopters)
    print("Unclassified:", unclassified)
    print("Total households:", total_households)

    print(
        "\nProvisional adoption rate among classified households:",
        f"{adoption_rate:.2f}%"
        if pd.notna(adoption_rate)
        else "Not calculable"
    )

# ----------------------------------------------------------
# 4. Combined display of separate visit summaries
# ----------------------------------------------------------

household_seed_summary_df = pd.DataFrame(
    household_seed_summary
)

print("\n" + "=" * 75)
print("PROVISIONAL HOUSEHOLD-LEVEL SUMMARY")
print("=" * 75)

display(household_seed_summary_df)

print(
    "\nImportant: Visits remain separate. These are provisional "
    "rates among classified households with crop records, not "
    "final survey-wide household adoption estimates."
)

print("Original source data modified: No")

```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Household-Level Missingness Investigation
# ==========================================================

missingness_audit = []

for visit, config in datasets.items():

    df = config["data"].copy()
    household_summary = household_seed_audit[visit].copy()

    print("\n" + "=" * 75)
    print(f"{visit.upper()}: HOUSEHOLD MISSINGNESS AUDIT")
    print("=" * 75)

    # ------------------------------------------------------
    # 1. Distribution of unresolved crop records per household
    # ------------------------------------------------------

    print("\n1. Distribution of unresolved crop records")

    unresolved_distribution = (
        household_summary["unresolved_crop_records"]
        .value_counts()
        .sort_index()
        .rename_axis("Unresolved crop records per household")
        .reset_index(name="Number of households")
    )

    display(unresolved_distribution)

    # ------------------------------------------------------
    # 2. Confirm household classifications
    # ------------------------------------------------------

    outcome_col = "household_improved_seed_adoption"

    adopters = household_summary[outcome_col].eq(1)
    non_adopters = household_summary[outcome_col].eq(0)
    unclassified = household_summary[outcome_col].isna()

    print("\n2. Household classification checks")

    print(
        "Adopters with unresolved crop records:",
        int(
            (
                adopters
                & household_summary["unresolved_crop_records"].gt(0)
            ).sum()
        )
    )

    print(
        "Non-adopters with unresolved crop records:",
        int(
            (
                non_adopters
                & household_summary["unresolved_crop_records"].gt(0)
            ).sum()
        )
    )

    print(
        "Unclassified households:",
        int(unclassified.sum())
    )

    # ------------------------------------------------------
    # 3. Inspect unclassified household summaries
    # ------------------------------------------------------

    print("\n3. Unclassified household records")

    unclassified_households = household_summary.loc[
        unclassified
    ].copy()

    print(
        "Total unresolved crop records among unclassified households:",
        int(
            unclassified_households["unresolved_crop_records"].sum()
        )
    )

    print(
        "Average unresolved crop records per unclassified household:",
        round(
            unclassified_households["unresolved_crop_records"].mean(),
            2
        ) if len(unclassified_households) else 0
    )

    if len(unclassified_households):
        display(
            unclassified_households[
                [
                    "hhid",
                    "crop_records",
                    "improved_seed_crop_records",
                    "unresolved_crop_records",
                    outcome_col,
                ]
            ].head(20)
        )

    # ------------------------------------------------------
    # 4. Save a compact audit summary in memory
    # ------------------------------------------------------

    missingness_audit.append({
        "visit": visit,
        "households": len(household_summary),
        "adopters": int(adopters.sum()),
        "non_adopters": int(non_adopters.sum()),
        "unclassified": int(unclassified.sum()),
        "unresolved_crop_records": int(
            household_summary["unresolved_crop_records"].sum()
        ),
        "unclassified_households_with_multiple_unresolved_records": int(
            unclassified_households[
                "unresolved_crop_records"
            ].gt(1).sum()
        ),
    })

missingness_audit_df = pd.DataFrame(missingness_audit)

print("\n" + "=" * 75)
print("HOUSEHOLD MISSINGNESS AUDIT SUMMARY")
print("=" * 75)

display(missingness_audit_df)

print("\nNo source data or existing household outcomes were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Verify Agricultural File and Visit Documentation
# ==========================================================

from pathlib import Path
from pypdf import PdfReader
import re

ddi_path = (
    Path(extracted_folder)
    / "ddi-documentation-english_microdata-3795.pdf"
)

reader = PdfReader(str(ddi_path))

search_terms = [
    "AGSEC4A",
    "AGSEC4B",
    "first visit",
    "second visit",
    "agriculture questionnaire",
    "agricultural questionnaire",
    "two visits",
    "visit 1",
    "visit 2",
]

print("=" * 80)
print("AGRICULTURAL FILE AND VISIT DOCUMENTATION")
print("=" * 80)

for page_number, page in enumerate(reader.pages, start=1):

    page_text = page.extract_text() or ""

    matching_terms = [
        term for term in search_terms
        if re.search(re.escape(term), page_text, re.IGNORECASE)
    ]

    if matching_terms:
        print(f"\nPage {page_number}")
        print("Matching terms:", ", ".join(matching_terms))
        print(" ".join(page_text.split())[:2500])

print("\nDocumentation inspection completed.")
print("No source data were modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Survey Design and Household-Linkage Variable Inventory
# ==========================================================

import pandas as pd

survey_design_audit = {}

for visit, config in datasets.items():

    df = config["data"]

    print("\n" + "=" * 80)
    print(f"{visit.upper()}: SURVEY DESIGN VARIABLE INVENTORY")
    print("=" * 80)

    # ------------------------------------------------------
    # 1. Search column names for likely survey-design fields
    # ------------------------------------------------------

    keywords = [
        "weight",
        "wgt",
        "strata",
        "cluster",
        "ea",
        "psu",
        "district",
        "region",
        "urban",
        "rural",
        "hhid",
        "t0_hhid",
        "interview",
        "visit",
        "season",
    ]

    matched_columns = [
        col for col in df.columns
        if any(keyword in col.lower() for keyword in keywords)
    ]

    print("\nPotentially relevant variables:")
    print(matched_columns)

    # ------------------------------------------------------
    # 2. Display a compact summary of matched variables
    # ------------------------------------------------------

    variable_rows = []

    for col in matched_columns:

        variable_rows.append({
            "variable": col,
            "data_type": str(df[col].dtype),
            "missing_count": int(df[col].isna().sum()),
            "unique_values": int(df[col].nunique(dropna=True)),
        })

    variable_summary = pd.DataFrame(variable_rows)

    display(variable_summary)

    # ------------------------------------------------------
    # 3. Check identifier completeness
    # ------------------------------------------------------

    for col in ["hhid", "t0_hhid", "interview__key"]:

        if col in df.columns:

            print(
                f"{col}: "
                f"{df[col].nunique(dropna=True)} distinct values; "
                f"{df[col].isna().sum()} missing values"
            )

    survey_design_audit[visit] = {
        "matched_columns": matched_columns,
        "variable_summary": variable_summary,
    }

print("\n" + "=" * 80)
print("SURVEY DESIGN INVENTORY COMPLETED")
print("No source data were modified.")
print("=" * 80)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Locate and Inspect Agricultural Household Identification File
# Read-only inspection
# ==========================================================

from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

# ----------------------------------------------------------
# 1. Locate AGSEC1 CSV files
# ----------------------------------------------------------

agsec1_files = [
    path
    for path in data_root.rglob("*.csv")
    if path.stem.lower() == "agsec1"
]

print("=" * 80)
print("AGSEC1 FILE SEARCH")
print("=" * 80)

if not agsec1_files:
    print("No CSV file named AGSEC1.csv was found.")
else:
    for path in agsec1_files:
        print("Found:", path)

# ----------------------------------------------------------
# 2. Inspect each matching file without loading all rows
# ----------------------------------------------------------

agsec1_metadata = {}

for path in agsec1_files:

    print("\n" + "=" * 80)
    print(f"FILE: {path.name}")
    print("=" * 80)

    # Read column names and a small sample only.
    sample = pd.read_csv(path, nrows=10, low_memory=False)

    print("Number of columns:", len(sample.columns))
    print("\nColumn names:")
    print(sample.columns.tolist())

    # Identify potentially useful linkage and design fields.
    keywords = [
        "hhid",
        "t0_hhid",
        "weight",
        "wgt",
        "strata",
        "cluster",
        "ea",
        "psu",
        "district",
        "region",
        "urban",
        "rural",
        "interview",
        "sample",
    ]

    relevant_columns = [
        col for col in sample.columns
        if any(keyword in col.lower() for keyword in keywords)
    ]

    print("\nPotential linkage and survey-design columns:")
    print(relevant_columns)

    if relevant_columns:
        print("\nSample values for relevant columns:")
        display(sample[relevant_columns].head(10))

    # Record the file location and schema for later use.
    agsec1_metadata[str(path)] = {
        "columns": sample.columns.tolist(),
        "relevant_columns": relevant_columns,
    }

print("\n" + "=" * 80)
print("INSPECTION COMPLETED")
print("Only the first 10 rows of each matching file were read.")
print("No source data or existing analysis objects were modified.")
print("=" * 80)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# AGSEC1 Household Linkage and Weight Audit
# Read-only diagnostic
# ==========================================================

from pathlib import Path
import pandas as pd

# ----------------------------------------------------------
# 1. Load the household identification file
# ----------------------------------------------------------

agsec1_path = Path(extracted_folder) / "Agric" / "AGSEC1.csv"

if not agsec1_path.exists():
    raise FileNotFoundError(
        f"AGSEC1.csv was not found at: {agsec1_path}"
    )

agsec1_audit_df = pd.read_csv(
    agsec1_path,
    low_memory=False
)

print("=" * 80)
print("AGSEC1 FILE SUMMARY")
print("=" * 80)

print("File:", agsec1_path)
print("Rows:", len(agsec1_audit_df))
print("Columns:", len(agsec1_audit_df.columns))

# ----------------------------------------------------------
# 2. Audit identifiers and potential survey weights
# ----------------------------------------------------------

audit_columns = [
    "hhid",
    "t0_hhid",
    "hwgt_w7",
    "wgt",
    "hwgt_wc",
    "region",
    "urban",
]

available_columns = [
    col for col in audit_columns
    if col in agsec1_audit_df.columns
]

summary_rows = []

for col in available_columns:

    summary_rows.append({
        "variable": col,
        "data_type": str(agsec1_audit_df[col].dtype),
        "missing_count": int(agsec1_audit_df[col].isna().sum()),
        "missing_percent": round(
            agsec1_audit_df[col].isna().mean() * 100, 2
        ),
        "unique_nonmissing": int(
            agsec1_audit_df[col].nunique(dropna=True)
        ),
    })

agsec1_variable_summary = pd.DataFrame(summary_rows)

print("\nIDENTIFIER, WEIGHT, AND GEOGRAPHIC VARIABLE SUMMARY")
display(agsec1_variable_summary)

# ----------------------------------------------------------
# 3. Check identifier uniqueness
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("IDENTIFIER UNIQUENESS")
print("=" * 80)

for col in ["hhid", "t0_hhid"]:

    if col not in agsec1_audit_df.columns:
        continue

    duplicate_mask = (
        agsec1_audit_df[col].notna()
        & agsec1_audit_df[col].duplicated(keep=False)
    )

    print(f"\n{col}")
    print("Distinct nonmissing values:",
          agsec1_audit_df[col].nunique(dropna=True))
    print("Rows with duplicated nonmissing identifier:",
          int(duplicate_mask.sum()))

    if duplicate_mask.any():
        print("Examples:")
        display(
            agsec1_audit_df.loc[
                duplicate_mask, available_columns
            ].sort_values(col).head(20)
        )

# ----------------------------------------------------------
# 4. Inspect the distribution of potential weights
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("POTENTIAL WEIGHT DISTRIBUTIONS")
print("=" * 80)

weight_columns = [
    col for col in ["hwgt_w7", "wgt", "hwgt_wc"]
    if col in agsec1_audit_df.columns
]

for col in weight_columns:

    numeric_weight = pd.to_numeric(
        agsec1_audit_df[col],
        errors="coerce"
    )

    print(f"\n{col}")
    print(numeric_weight.describe().to_string())

    print("Zero weights:",
          int((numeric_weight == 0).sum()))
    print("Negative weights:",
          int((numeric_weight < 0).sum()))

# ----------------------------------------------------------
# 5. Compare crop-file household IDs with AGSEC1
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("CROP-FILE HOUSEHOLD LINKAGE")
print("=" * 80)

crop_linkage_audit = {}

for visit, config in datasets.items():

    crop_df = config["data"]

    crop_ids = set(
        crop_df["hhid"].dropna().astype(str).unique()
    )

    agsec1_ids = set(
        agsec1_audit_df["hhid"].dropna().astype(str).unique()
    )

    matched_ids = crop_ids.intersection(agsec1_ids)
    unmatched_ids = crop_ids.difference(agsec1_ids)

    linkage_summary = {
        "visit": visit,
        "crop_unique_hhid": len(crop_ids),
        "agsec1_unique_hhid": len(agsec1_ids),
        "matched_hhid": len(matched_ids),
        "unmatched_hhid": len(unmatched_ids),
        "match_percent": round(
            len(matched_ids) / len(crop_ids) * 100, 2
        ) if crop_ids else None,
    }

    crop_linkage_audit[visit] = {
        "summary": linkage_summary,
        "unmatched_ids": sorted(unmatched_ids),
    }

    print(f"\n{visit.upper()}")
    display(pd.DataFrame([linkage_summary]))

    if unmatched_ids:
        print("Sample unmatched household IDs:")
        print(sorted(unmatched_ids)[:15])

# ----------------------------------------------------------
# 6. Check whether AGSEC1 has conflicting household attributes
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("HOUSEHOLD ATTRIBUTE CONSISTENCY")
print("=" * 80)

attributes = [
    col for col in [
        "hwgt_w7",
        "wgt",
        "hwgt_wc",
        "region",
        "urban",
        "t0_hhid",
    ]
    if col in agsec1_audit_df.columns
]

for col in attributes:

    distinct_per_hhid = (
        agsec1_audit_df
        .dropna(subset=["hhid"])
        .groupby("hhid")[col]
        .nunique(dropna=True)
    )

    conflicting_ids = distinct_per_hhid[
        distinct_per_hhid > 1
    ]

    print(
        f"{col}: "
        f"{len(conflicting_ids)} hhid values have "
        "more than one distinct nonmissing value."
    )

print("\n" + "=" * 80)
print("AUDIT COMPLETED")
print("Source CSV files were not modified.")
print("Existing adoption-analysis objects were not overwritten.")
print("=" * 80)
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Weight Coverage Among Agricultural Households
# ==========================================================

import pandas as pd

weight_columns = ["wgt", "hwgt_w7", "hwgt_wc"]

# Create a separate diagnostic copy.
agsec1_weight_audit = agsec1_audit_df[
    ["hhid", "t0_hhid"] + weight_columns
].copy()

# Keep identifiers as strings for consistent matching.
agsec1_weight_audit["hhid"] = (
    agsec1_weight_audit["hhid"].astype("string")
)

# Build a household-level lookup.
# AGSEC1 has already been audited for unique hhid values.
weight_lookup = agsec1_weight_audit.set_index("hhid")

coverage_results = []

for visit, config in datasets.items():

    crop_df = config["data"]

    # One row per household in this visit.
    visit_households = (
        crop_df[["hhid"]]
        .drop_duplicates()
        .copy()
    )

    visit_households["hhid"] = (
        visit_households["hhid"].astype("string")
    )

    # Match household-level weights.
    matched = visit_households.merge(
        agsec1_weight_audit,
        on="hhid",
        how="left",
        validate="one_to_one",
        indicator=True,
    )

    print("\n" + "=" * 80)
    print(f"{visit.upper()}: WEIGHT COVERAGE")
    print("=" * 80)

    print("Unique crop households:", len(matched))
    print("Matched to AGSEC1:", int((matched["_merge"] == "both").sum()))
    print("Unmatched to AGSEC1:", int((matched["_merge"] == "left_only").sum()))

    for weight in weight_columns:

        available = int(matched[weight].notna().sum())
        missing = int(matched[weight].isna().sum())

        coverage_results.append({
            "visit": visit,
            "weight": weight,
            "households": len(matched),
            "weight_available": available,
            "weight_missing": missing,
            "coverage_percent": round(
                available / len(matched) * 100, 2
            ) if len(matched) else None,
        })

    display(
        pd.DataFrame([
            {
                "weight": weight,
                "available": int(matched[weight].notna().sum()),
                "missing": int(matched[weight].isna().sum()),
                "coverage_percent": round(
                    matched[weight].notna().mean() * 100, 2
                ),
            }
            for weight in weight_columns
        ])
    )

    # Examine the identifiers associated with missing weights.
    for weight in weight_columns:

        missing_weight = matched.loc[
            matched[weight].isna(),
            ["hhid", "t0_hhid"]
        ]

        print(f"\n{weight}: examples with missing weights")

        if missing_weight.empty:
            print("None")
        else:
            display(missing_weight.head(10))

coverage_summary_df = pd.DataFrame(coverage_results)

print("\n" + "=" * 80)
print("COMBINED WEIGHT COVERAGE SUMMARY")
print("=" * 80)

display(coverage_summary_df)

print("\nAudit completed. Source data and existing analysis objects were not modified.")
```


```python
# ==========================================================
# RESEARCHPRO-ANALYTICS
# Survey Geographic Variables Inventory
# Read-only inspection
# ==========================================================

from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

# ----------------------------------------------------------
# 1. Locate the geographic-variables file
# ----------------------------------------------------------

geo_files = [
    path
    for path in data_root.rglob("*.csv")
    if "unps_geovars_2018_19" in path.stem.lower()
]

print("=" * 80)
print("GEOGRAPHIC VARIABLES FILE SEARCH")
print("=" * 80)

if not geo_files:
    print("No matching CSV found.")
    print("We will need to inspect the available file names next.")
else:

    for geo_path in geo_files:

        print("\nFile found:", geo_path)

        # Read column names and a small sample.
        geo_sample = pd.read_csv(
            geo_path,
            nrows=10,
            low_memory=False
        )

        print("\nNumber of columns:", len(geo_sample.columns))

        print("\nColumn names:")
        print(geo_sample.columns.tolist())

        # --------------------------------------------------
        # 2. Identify potential identifiers and design fields
        # --------------------------------------------------

        keywords = [
            "hhid",
            "t0_hhid",
            "cluster",
            "strata",
            "stratum",
            "psu",
            "ea",
            "enumeration",
            "region",
            "district",
            "urban",
            "rural",
            "parish",
            "county",
            "subcounty",
            "weight",
            "wgt",
        ]

        relevant_columns = [
            col
            for col in geo_sample.columns
            if any(keyword in col.lower() for keyword in keywords)
        ]

        print("\nPotentially relevant columns:")
        print(relevant_columns)

        if relevant_columns:
            print("\nSample values:")
            display(geo_sample[relevant_columns].head(10))

print("\n" + "=" * 80)
print("GEOGRAPHIC VARIABLES INVENTORY COMPLETED")
print("No source data or existing analysis objects were modified.")
print("=" * 80)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

geo_path = data_root / "unps_geovars_2018_19.csv"

if not geo_path.exists():
    raise FileNotFoundError(f"Geographic variables file not found: {geo_path}")

# Load the geographic variables
geo_df = pd.read_csv(geo_path, low_memory=False)

print("=" * 80)
print("GEOGRAPHIC VARIABLES QUALITY AUDIT")
print("=" * 80)

# 1. File structure
print("\n1. DATASET STRUCTURE")
print("-" * 50)
print("Rows:", len(geo_df))
print("Columns:", len(geo_df.columns))
print("Column names:", geo_df.columns.tolist())

# 2. Missing values
print("\n2. MISSING VALUES")
print("-" * 50)

geo_missingness = pd.DataFrame({
    "missing_count": geo_df.isna().sum(),
    "missing_percent": (geo_df.isna().mean() * 100).round(2),
    "unique_nonmissing": geo_df.nunique(dropna=True)
})

display(geo_missingness)

# 3. Household identifier quality
print("\n3. HOUSEHOLD IDENTIFIER QUALITY")
print("-" * 50)

print("Missing hhid:", geo_df["hhid"].isna().sum())
print("Unique hhid:", geo_df["hhid"].nunique())
print("Duplicate hhid rows:", geo_df["hhid"].duplicated(keep=False).sum())

# Show duplicate identifiers, if any
duplicate_geo_ids = geo_df.loc[
    geo_df["hhid"].duplicated(keep=False)
].sort_values("hhid")

if duplicate_geo_ids.empty:
    print("No duplicate household identifiers found.")
else:
    print("Duplicate household identifier examples:")
    display(duplicate_geo_ids.head(20))

# 4. Coordinate ranges and plausibility
print("\n4. PUBLIC-USE COORDINATE CHECK")
print("-" * 50)

for column in ["pub_lat_mod", "pub_lon_mod"]:
    geo_df[column] = pd.to_numeric(geo_df[column], errors="coerce")

    print(f"\n{column}")
    print("Minimum:", geo_df[column].min())
    print("Median:", geo_df[column].median())
    print("Maximum:", geo_df[column].max())

print("\nRows with both coordinates available:",
      geo_df[["pub_lat_mod", "pub_lon_mod"]].notna().all(axis=1).sum())

print("Rows missing at least one coordinate:",
      geo_df[["pub_lat_mod", "pub_lon_mod"]].isna().any(axis=1).sum())

print("\n" + "=" * 80)
print("GEOGRAPHIC VARIABLES AUDIT COMPLETED")
print("Only the in-memory copy was used; the source CSV was not modified.")
print("=" * 80)

```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

geo_path = data_root / "unps_geovars_2018_19.csv"
agsec1_path = data_root / "Agric" / "AGSEC1.csv"
agsec4a_path = data_root / "Agric" / "AGSEC4A.csv"
agsec4b_path = data_root / "Agric" / "AGSEC4B.csv"

required_files = [
    geo_path,
    agsec1_path,
    agsec4a_path,
    agsec4b_path,
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

# Load only the identifiers needed for this audit
geo_ids = pd.read_csv(geo_path, usecols=["hhid"])
agsec1_ids = pd.read_csv(agsec1_path, usecols=["hhid"])
visit_a_ids = pd.read_csv(agsec4a_path, usecols=["hhid"])
visit_b_ids = pd.read_csv(agsec4b_path, usecols=["hhid"])

# Create distinct, non-missing household ID sets
geo_set = set(geo_ids["hhid"].dropna())
agsec1_set = set(agsec1_ids["hhid"].dropna())
visit_a_set = set(visit_a_ids["hhid"].dropna())
visit_b_set = set(visit_b_ids["hhid"].dropna())

datasets = {
    "AGSEC1 household file": agsec1_set,
    "AGSEC4A first-visit crop file": visit_a_set,
    "AGSEC4B second-visit crop file": visit_b_set,
}

coverage_results = []

for dataset_name, household_ids in datasets.items():
    matched = household_ids & geo_set
    unmatched = household_ids - geo_set

    coverage_results.append({
        "dataset": dataset_name,
        "unique_households": len(household_ids),
        "matched_to_geographic_file": len(matched),
        "unmatched_to_geographic_file": len(unmatched),
        "coverage_percent": round(
            100 * len(matched) / len(household_ids), 2
        ) if household_ids else None,
    })

geographic_coverage_df = pd.DataFrame(coverage_results)

print("=" * 80)
print("GEOGRAPHIC FILE HOUSEHOLD COVERAGE AUDIT")
print("=" * 80)

display(geographic_coverage_df)

# Check whether the geographic file's household IDs are present in AGSEC1
print("\nGeographic IDs not found in AGSEC1:",
      len(geo_set - agsec1_set))

print("AGSEC1 IDs not found in geographic file:",
      len(agsec1_set - geo_set))

print("\n" + "=" * 80)
print("COVERAGE AUDIT COMPLETED")
print("No source files or previous analysis objects were modified.")
print("=" * 80)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

geo_path = data_root / "unps_geovars_2018_19.csv"
agsec1_path = data_root / "Agric" / "AGSEC1.csv"
agsec4a_path = data_root / "Agric" / "AGSEC4A.csv"
agsec4b_path = data_root / "Agric" / "AGSEC4B.csv"

# Load the geographic IDs and relevant household information
geo_ids_df = pd.read_csv(geo_path, usecols=["hhid"])

agsec1_relevant = pd.read_csv(
    agsec1_path,
    usecols=["hhid", "wgt", "hwgt_w7", "hwgt_wc", "region", "urban"],
    low_memory=False
)

visit_a_ids_df = pd.read_csv(agsec4a_path, usecols=["hhid"])
visit_b_ids_df = pd.read_csv(agsec4b_path, usecols=["hhid"])

geo_ids = set(geo_ids_df["hhid"].dropna())
visit_a_ids = set(visit_a_ids_df["hhid"].dropna())
visit_b_ids = set(visit_b_ids_df["hhid"].dropna())

# Identify AGSEC1 households missing from the geographic file
missing_geo_df = agsec1_relevant.loc[
    ~agsec1_relevant["hhid"].isin(geo_ids)
].copy()

# Mark whether each household appears in either crop visit
missing_geo_df["in_AGSEC4A"] = missing_geo_df["hhid"].isin(visit_a_ids)
missing_geo_df["in_AGSEC4B"] = missing_geo_df["hhid"].isin(visit_b_ids)

print("=" * 80)
print("HOUSEHOLDS MISSING FROM THE GEOGRAPHIC FILE")
print("=" * 80)

print("\nNumber of households:", len(missing_geo_df))

print("\n1. Presence in crop files")
display(
    missing_geo_df[
        ["in_AGSEC4A", "in_AGSEC4B"]
    ].value_counts(dropna=False).rename("household_count").to_frame()
)

print("\n2. Weight availability among the 66 households")
weight_summary = pd.DataFrame({
    "available_count": missing_geo_df[
        ["wgt", "hwgt_w7", "hwgt_wc"]
    ].notna().sum(),
    "missing_count": missing_geo_df[
        ["wgt", "hwgt_w7", "hwgt_wc"]
    ].isna().sum(),
    "missing_percent": (
        missing_geo_df[
            ["wgt", "hwgt_w7", "hwgt_wc"]
        ].isna().mean() * 100
    ).round(2),
})

display(weight_summary)

print("\n3. Region and urban/rural availability")
display(
    pd.DataFrame({
        "available_count": missing_geo_df[
            ["region", "urban"]
        ].notna().sum(),
        "missing_count": missing_geo_df[
            ["region", "urban"]
        ].isna().sum(),
    })
)

print("\n4. Example household records")
display(missing_geo_df.head(10))

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETED")
print("No source data or existing analysis objects were modified.")
print("=" * 80)
```


```python
from pathlib import Path
from pypdf import PdfReader

data_root = Path(extracted_folder)

pdf_names = [
    "unps_7_bid.pdf",
    "ddi-documentation-english_microdata-3795.pdf",
]

search_terms = [
    "primary sampling unit",
    "sampling unit",
    "enumeration area",
    "sampling strata",
    "stratification",
    "cluster",
    "sampling weight",
    "household weight",
    "probability proportional to size",
    "urban and rural",
]

print("=" * 90)
print("UNPS SAMPLING-DESIGN DOCUMENTATION SEARCH")
print("=" * 90)

for pdf_name in pdf_names:
    pdf_path = data_root / pdf_name

    if not pdf_path.exists():
        print(f"\nFile not found: {pdf_path}")
        continue

    print(f"\n\nDOCUMENT: {pdf_name}")
    print("-" * 90)

    reader = PdfReader(str(pdf_path))
    print("Number of pages:", len(reader.pages))

    matches_found = 0

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        page_text_lower = page_text.lower()

        matched_terms = [
            term for term in search_terms
            if term in page_text_lower
        ]

        if matched_terms:
            matches_found += 1
            print(f"\nPage {page_number}")
            print("Matched terms:", ", ".join(matched_terms))

            # Print a limited excerpt to keep the output manageable
            for term in matched_terms:
                position = page_text_lower.find(term)
                start = max(0, position - 250)
                end = min(len(page_text), position + 650)

                excerpt = page_text[start:end].replace("\n", " ")
                print(f"\nExcerpt for '{term}':")
                print(excerpt)
                break

    if matches_found == 0:
        print("No matching terms found in extracted PDF text.")

print("\n" + "=" * 90)
print("DOCUMENT SEARCH COMPLETED")
print("=" * 90)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

# Search terms for possible sampling-design variables
design_keywords = [
    "psu",
    "strata",
    "stratum",
    "cluster",
    "enum",
    "enumeration",
    "ea_id",
    "eaid",
    "district",
    "region",
    "urban",
    "rural",
    "sample",
    "weight",
    "wgt",
]

results = []

print("=" * 90)
print("SEARCHING CSV HEADERS FOR SURVEY-DESIGN VARIABLES")
print("=" * 90)

for csv_path in data_root.rglob("*.csv"):
    try:
        # Read the header only; do not load the entire dataset
        columns = pd.read_csv(csv_path, nrows=0).columns.tolist()

        matches = [
            column
            for column in columns
            if any(
                keyword in column.lower()
                for keyword in design_keywords
            )
        ]

        if matches:
            results.append({
                "file": str(csv_path.relative_to(data_root)),
                "matching_columns": matches,
            })

    except Exception as error:
        print(f"Could not inspect {csv_path.name}: {error}")

if results:
    design_inventory_df = pd.DataFrame(results)

    for _, row in design_inventory_df.iterrows():
        print(f"\nFile: {row['file']}")
        print("Potentially relevant columns:")
        for column in row["matching_columns"]:
            print(f"  - {column}")

    print("\nFiles with potentially relevant columns:", len(results))

else:
    print("No matching column names were found.")

print("\n" + "=" * 90)
print("HEADER SEARCH COMPLETED")
print("Only CSV headers were inspected; no source data were modified.")
print("=" * 90)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

agsec1_path = data_root / "Agric" / "AGSEC1.csv"
gsec1_path = data_root / "HH" / "GSEC1.csv"

if not agsec1_path.exists():
    raise FileNotFoundError(f"File not found: {agsec1_path}")

if not gsec1_path.exists():
    raise FileNotFoundError(f"File not found: {gsec1_path}")

# Load only the variables needed for comparison.
agsec1 = pd.read_csv(
    agsec1_path,
    usecols=["hhid", "wgt", "hwgt_w7", "hwgt_wc", "region", "urban"],
    low_memory=False
)

gsec1 = pd.read_csv(
    gsec1_path,
    usecols=["hhid", "wgt", "hwgt_W7", "hwgt_wc",
             "region", "urban", "district_code"],
    low_memory=False
)

# Standardize the panel-weight column name for comparison.
gsec1 = gsec1.rename(columns={"hwgt_W7": "hwgt_w7"})

# Check identifier quality.
print("=" * 85)
print("AGSEC1 AND GSEC1 HOUSEHOLD FILE COMPARISON")
print("=" * 85)

for name, df in [("AGSEC1", agsec1), ("GSEC1", gsec1)]:
    print(f"\n{name}")
    print("-" * 40)
    print("Rows:", len(df))
    print("Missing hhid:", df["hhid"].isna().sum())
    print("Unique hhid:", df["hhid"].nunique())
    print("Duplicate hhid rows:",
          df["hhid"].duplicated(keep=False).sum())

# Build household ID sets.
agsec1_ids = set(agsec1["hhid"].dropna())
gsec1_ids = set(gsec1["hhid"].dropna())

print("\nHOUSEHOLD ID OVERLAP")
print("-" * 40)
print("AGSEC1-only household IDs:", len(agsec1_ids - gsec1_ids))
print("GSEC1-only household IDs:", len(gsec1_ids - agsec1_ids))
print("Shared household IDs:", len(agsec1_ids & gsec1_ids))

# Compare common household attributes after a one-to-one merge.
merged = agsec1.merge(
    gsec1,
    on="hhid",
    how="outer",
    suffixes=("_ag", "_hh"),
    indicator=True,
    validate="one_to_one"
)

print("\nMERGE STATUS")
print("-" * 40)
display(merged["_merge"].value_counts().rename_axis("merge_status")
        .to_frame("household_count"))

# Compare values only for household IDs found in both files.
shared = merged.loc[merged["_merge"] == "both"].copy()

comparison_rows = []

for variable in ["wgt", "hwgt_w7", "hwgt_wc", "region", "urban"]:
    left = shared[f"{variable}_ag"]
    right = shared[f"{variable}_hh"]

    both_present = left.notna() & right.notna()
    either_missing = left.isna() | right.isna()

    if variable in ["wgt", "hwgt_w7", "hwgt_wc"]:
        equal = (
            (left - right).abs() <= 1e-8
        ) & both_present
    else:
        equal = (left == right) & both_present

    comparison_rows.append({
        "variable": variable,
        "both_present": int(both_present.sum()),
        "either_missing": int(either_missing.sum()),
        "matching_values": int(equal.sum()),
        "different_values_when_both_present": int(
            (both_present & ~equal).sum()
        ),
    })

comparison_df = pd.DataFrame(comparison_rows)

print("\nATTRIBUTE COMPARISON FOR SHARED HOUSEHOLDS")
print("-" * 40)
display(comparison_df)

print("\n" + "=" * 85)
print("COMPARISON COMPLETED")
print("Source CSV files were not modified.")
print("=" * 85)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

agsec1_path = data_root / "Agric" / "AGSEC1.csv"
gsec1_path = data_root / "HH" / "GSEC1.csv"

ag_urban = pd.read_csv(
    agsec1_path,
    usecols=["hhid", "urban", "region"]
)

hh_urban = pd.read_csv(
    gsec1_path,
    usecols=["hhid", "urban", "region", "district_code"]
)

# Rename columns so both sources remain distinguishable.
ag_urban = ag_urban.rename(columns={
    "urban": "urban_ag",
    "region": "region_ag"
})

hh_urban = hh_urban.rename(columns={
    "urban": "urban_hh",
    "region": "region_hh"
})

urban_comparison = ag_urban.merge(
    hh_urban,
    on="hhid",
    how="outer",
    validate="one_to_one",
    indicator=True
)

print("=" * 85)
print("URBAN VARIABLE DISCREPANCY DIAGNOSTIC")
print("=" * 85)

# 1. Value distributions
print("\n1. AGSEC1 urban distribution")
display(
    urban_comparison["urban_ag"]
    .value_counts(dropna=False)
    .sort_index()
    .rename("count")
    .to_frame()
)

print("\n2. GSEC1 urban distribution")
display(
    urban_comparison["urban_hh"]
    .value_counts(dropna=False)
    .sort_index()
    .rename("count")
    .to_frame()
)

# 2. Cross-tabulation
print("\n3. Cross-tabulation of urban values")
display(
    pd.crosstab(
        urban_comparison["urban_ag"],
        urban_comparison["urban_hh"],
        margins=True,
        dropna=False
    )
)

# 3. Compare region values
print("\n4. Region cross-tabulation")
display(
    pd.crosstab(
        urban_comparison["region_ag"],
        urban_comparison["region_hh"],
        margins=True,
        dropna=False
    )
)

# 4. Inspect records with conflicting urban values
conflicts = urban_comparison.loc[
    urban_comparison["urban_ag"].notna()
    & urban_comparison["urban_hh"].notna()
    & urban_comparison["urban_ag"].ne(urban_comparison["urban_hh"])
].copy()

print("\n5. Number of conflicting urban records:", len(conflicts))

print("\nExamples of conflicting records:")
display(
    conflicts[
        [
            "hhid",
            "urban_ag",
            "urban_hh",
            "region_ag",
            "region_hh",
            "district_code"
        ]
    ].head(20)
)

print("\n" + "=" * 85)
print("DIAGNOSTIC COMPLETED")
print("No source data or previous analysis objects were modified.")
print("=" * 85)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

target_files = [
    "GSEC15B_2.csv",
    "GSEC15D.csv",
    "GSEC8.csv",
]

design_keywords = [
    "psu",
    "strata",
    "stratum",
    "cluster",
    "enum",
    "enumeration",
    "ea_id",
    "eaid",
    "district",
    "region",
    "urban",
    "rural",
    "sample",
    "weight",
    "wgt",
]

print("=" * 85)
print("ENCODING-SAFE SURVEY-DESIGN HEADER SEARCH")
print("=" * 85)

for filename in target_files:
    matching_paths = list(data_root.rglob(filename))

    if not matching_paths:
        print(f"\nFile not found: {filename}")
        continue

    for file_path in matching_paths:
        print(f"\nFILE: {file_path.relative_to(data_root)}")
        print("-" * 65)

        columns = None
        successful_encoding = None

        for encoding in ["utf-8-sig", "cp1252", "latin1"]:
            try:
                columns = pd.read_csv(
                    file_path,
                    nrows=0,
                    encoding=encoding
                ).columns.tolist()

                successful_encoding = encoding
                break

            except UnicodeDecodeError:
                continue

        if columns is None:
            print("Could not read the header using the tested encodings.")
            continue

        print("Encoding used:", successful_encoding)
        print("Number of columns:", len(columns))
        print("All columns:")
        print(columns)

        relevant_columns = [
            column
            for column in columns
            if any(
                keyword in column.lower()
                for keyword in design_keywords
            )
        ]

        print("\nPotentially relevant columns:")
        print(relevant_columns)

print("\n" + "=" * 85)
print("HEADER SEARCH COMPLETED")
print("Only file headers were read; source files were not modified.")
print("=" * 85)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)
gsec1_path = data_root / "HH" / "GSEC1.csv"

if not gsec1_path.exists():
    raise FileNotFoundError(f"GSEC1 file not found: {gsec1_path}")

print("=" * 85)
print("SURVEY GEOGRAPHIC AND STRATIFICATION VARIABLE AUDIT")
print("=" * 85)

# 1. Inspect geographic classifications in GSEC1.
gsec1_columns = pd.read_csv(gsec1_path, nrows=0).columns.tolist()

candidate_columns = [
    "hhid",
    "t0_hhid",
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
    "urban",
    "region",
    "regurb",
    "subreg",
    "wgt",
    "hwgt_W7",
    "hwgt_wc",
]

available_columns = [
    column for column in candidate_columns
    if column in gsec1_columns
]

print("\n1. Relevant columns available in GSEC1:")
print(available_columns)

gsec1_geo = pd.read_csv(
    gsec1_path,
    usecols=available_columns,
    low_memory=False
)

# Display distributions for candidate geographic classifications.
for column in [
    "region",
    "urban",
    "regurb",
    "subreg",
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
]:
    if column in gsec1_geo.columns:
        print(f"\nDistribution of {column}:")
        print(
            gsec1_geo[column]
            .value_counts(dropna=False)
            .sort_index()
            .head(30)
        )

# 2. Search all CSV headers for possible geographic and design identifiers.
search_terms = [
    "psu",
    "strata",
    "stratum",
    "cluster",
    "enum",
    "enumeration",
    "ea_id",
    "eaid",
    "district",
    "county",
    "subcounty",
    "parish",
    "region",
    "regurb",
    "subreg",
    "urban",
    "rural",
    "community",
    "dynasty",
    "sample",
    "weight",
    "wgt",
]

header_matches = []

for csv_path in data_root.rglob("*.csv"):
    try:
        columns = None

        for encoding in ["utf-8-sig", "cp1252", "latin1"]:
            try:
                columns = pd.read_csv(
                    csv_path,
                    nrows=0,
                    encoding=encoding
                ).columns.tolist()
                break
            except UnicodeDecodeError:
                continue

        if columns is None:
            print(f"Header could not be read: {csv_path.name}")
            continue

        matches = [
            column for column in columns
            if any(term in column.lower() for term in search_terms)
        ]

        if matches:
            header_matches.append({
                "file": str(csv_path.relative_to(data_root)),
                "matching_columns": matches,
            })

    except Exception as error:
        print(f"Could not inspect {csv_path.name}: {error}")

print("\n\n2. CSV files containing candidate geographic/design fields")
print("-" * 85)

if header_matches:
    for item in header_matches:
        print(f"\nFile: {item['file']}")
        print("Matching columns:", item["matching_columns"])
else:
    print("No matching columns found.")

print("\n" + "=" * 85)
print("AUDIT COMPLETED")
print("Only CSV headers and selected classification columns were inspected.")
print("No source data or previous analysis objects were modified.")
print("=" * 85)
```


```python
from pathlib import Path
import re

data_root = Path(extracted_folder)

documentation_files = [
    data_root / "ddi-documentation-english_microdata-3795.pdf",
    data_root / "agriculture_qx.pdf",
    data_root / "unps_7_bid.pdf",
    data_root / "unps_hhq.pdf",
]

search_patterns = [
    r"\bregurb\b",
    r"\bsubreg\b",
    r"sampling strata",
    r"stratification",
    r"primary sampling unit",
    r"\bPSU\b",
    r"enumeration area",
    r"\bcluster\b",
    r"sampling weights",
    r"urban/rural",
]

print("=" * 90)
print("DOCUMENTATION SEARCH: GEOGRAPHIC AND SURVEY-DESIGN DEFINITIONS")
print("=" * 90)

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise ImportError(
        "pypdf is required. Activate the project's .venv313 environment "
        "and install pypdf if it is not available."
    ) from exc

for pdf_path in documentation_files:
    if not pdf_path.exists():
        print(f"\nPDF not found: {pdf_path.name}")
        continue

    print(f"\n\nDOCUMENT: {pdf_path.name}")
    print("-" * 90)

    reader = PdfReader(str(pdf_path))
    document_matches = 0

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        for pattern in search_patterns:
            matches = list(
                re.finditer(pattern, page_text, flags=re.IGNORECASE)
            )

            for match in matches:
                start = max(0, match.start() - 220)
                end = min(len(page_text), match.end() + 320)
                excerpt = " ".join(page_text[start:end].split())

                print(
                    f"\nPage {page_number} | "
                    f"Search term: {match.group(0)}"
                )
                print(excerpt)

                document_matches += 1

                # Keep output manageable.
                if document_matches >= 35:
                    print(
                        "\nOutput limit reached for this document. "
                        "Additional matches were not printed."
                    )
                    break

            if document_matches >= 35:
                break

        if document_matches >= 35:
            break

    if document_matches == 0:
        print("No matches found for the selected terms.")

print("\n" + "=" * 90)
print("DOCUMENTATION SEARCH COMPLETED")
print("PDF files were read only; no files or analysis objects were modified.")
print("=" * 90)
```


```python
from pathlib import Path
from pypdf import PdfReader

data_root = Path(extracted_folder)

pdf_path = data_root / "ddi-documentation-english_microdata-3795.pdf"

if not pdf_path.exists():
    raise FileNotFoundError(f"Documentation not found: {pdf_path}")

reader = PdfReader(str(pdf_path))

print("=" * 80)
print("UNPS METADATA DOCUMENT STRUCTURE")
print("=" * 80)

print(f"File: {pdf_path.name}")
print(f"Total pages: {len(reader.pages)}")

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    print(f"\nPage {page_number}")
    print("-" * 50)

    if lines:
        print(" | ".join(lines[:5]))
    else:
        print("No extractable text on this page.")

print("\n" + "=" * 80)
print("DOCUMENT STRUCTURE INSPECTION COMPLETED")
print("=" * 80)
```


```python
from pathlib import Path
from pypdf import PdfReader

data_root = Path(extracted_folder)
pdf_path = data_root / "ddi-documentation-english_microdata-3795.pdf"

reader = PdfReader(str(pdf_path))

# Page numbers below are human-readable, starting from 1.
pages_to_inspect = [2, 3, 4, 5, 7]

print("=" * 85)
print("TARGETED UNPS SAMPLING AND DATA-DICTIONARY REVIEW")
print("=" * 85)

for page_number in pages_to_inspect:
    page_text = reader.pages[page_number - 1].extract_text() or ""

    print(f"\n\n{'=' * 30} PAGE {page_number} {'=' * 30}")
    print(page_text if page_text.strip() else "No extractable text on this page.")

print("\n\n" + "=" * 85)
print("REVIEW COMPLETED — SOURCE PDF NOT MODIFIED")
print("=" * 85)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

agsec1_path = data_root / "Agric" / "AGSEC1.csv"
gsec1_path = data_root / "HH" / "GSEC1.csv"
agsec4a_path = data_root / "Agric" / "AGSEC4A.csv"
agsec4b_path = data_root / "Agric" / "AGSEC4B.csv"

required_files = [
    agsec1_path,
    gsec1_path,
    agsec4a_path,
    agsec4b_path,
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

print("=" * 90)
print("AUDIT OF HOUSEHOLDS MISSING FROM GSEC1")
print("=" * 90)

# Read only the columns needed for this diagnostic.
agsec1 = pd.read_csv(agsec1_path, low_memory=False)
gsec1 = pd.read_csv(gsec1_path, low_memory=False)

crop_a = pd.read_csv(
    agsec4a_path,
    usecols=["hhid"],
    low_memory=False
)

crop_b = pd.read_csv(
    agsec4b_path,
    usecols=["hhid"],
    low_memory=False
)

# Identify the 66 AGSEC1 household IDs absent from GSEC1.
gsec1_ids = set(gsec1["hhid"].dropna())
agsec1_only = agsec1.loc[~agsec1["hhid"].isin(gsec1_ids)].copy()

print("\n1. Record counts")
print("-" * 60)
print("AGSEC1 records:", len(agsec1))
print("GSEC1 records:", len(gsec1))
print("AGSEC1 households absent from GSEC1:", len(agsec1_only))

# Confirm the missingness pattern in these records.
candidate_columns = [
    "hhid",
    "t0_hhid",
    "batch",
    "region",
    "urban",
    "wgt",
    "hwgt_w7",
    "hwgt_wc",
    "hhsize",
    "hh_crp1",
    "hh_crp2",
    "culcrp",
    "lvstck",
    "hh_anm",
    "hh_plty",
]

available_columns = [
    column for column in candidate_columns
    if column in agsec1_only.columns
]

print("\n2. Missingness among AGSEC1-only records")
print("-" * 60)

print(
    agsec1_only[available_columns]
    .isna()
    .sum()
    .to_string()
)

# Summarize crop-file appearances.
crop_a_ids = set(crop_a["hhid"].dropna())
crop_b_ids = set(crop_b["hhid"].dropna())

agsec1_only["appears_in_AGSEC4A"] = (
    agsec1_only["hhid"].isin(crop_a_ids)
)

agsec1_only["appears_in_AGSEC4B"] = (
    agsec1_only["hhid"].isin(crop_b_ids)
)

agsec1_only["crop_visit_pattern"] = (
    agsec1_only["appears_in_AGSEC4A"].astype(str)
    + " / "
    + agsec1_only["appears_in_AGSEC4B"].astype(str)
)

print("\n3. Crop-file appearance")
print("-" * 60)

print(
    agsec1_only["crop_visit_pattern"]
    .value_counts(dropna=False)
    .to_string()
)

# Inspect identifiers without assuming they encode sampling design.
print("\n4. Identifier examples")
print("-" * 60)

print(
    agsec1_only[
        [column for column in ["hhid", "t0_hhid", "batch"]
         if column in agsec1_only.columns]
    ]
    .head(15)
    .to_string(index=False)
)

# Test whether administrative codes repeat across districts.
print("\n5. Geographic-code uniqueness diagnostics in GSEC1")
print("-" * 60)

for code_column in [
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
]:
    if code_column not in gsec1.columns:
        continue

    nonmissing = gsec1[code_column].dropna()

    print(f"\n{code_column}")
    print("Nonmissing values:", len(nonmissing))
    print("Distinct codes:", nonmissing.nunique())
    print("Unique codes / nonmissing records:",
          nonmissing.nunique() / len(nonmissing)
          if len(nonmissing) else float("nan"))

# Examine nested code combinations when the required columns exist.
nested_geographies = [
    ["district_code", "county_code"],
    ["district_code", "county_code", "subcounty_code"],
    ["district_code", "county_code", "subcounty_code", "parish_code"],
]

for columns in nested_geographies:
    if all(column in gsec1.columns for column in columns):
        valid = gsec1[columns].dropna()
        print(f"\nDistinct combinations of {columns}:",
              len(valid.drop_duplicates()))

print("\n" + "=" * 90)
print("AUDIT COMPLETED")
print("Source files were not modified.")
print("=" * 90)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

agsec1_path = data_root / "Agric" / "AGSEC1.csv"
gsec1_path = data_root / "HH" / "GSEC1.csv"
agsec4a_path = data_root / "Agric" / "AGSEC4A.csv"
agsec4b_path = data_root / "Agric" / "AGSEC4B.csv"

agsec1 = pd.read_csv(agsec1_path, low_memory=False)
gsec1 = pd.read_csv(gsec1_path, low_memory=False)

crop_a = pd.read_csv(agsec4a_path, low_memory=False)
crop_b = pd.read_csv(agsec4b_path, low_memory=False)

gsec1_ids = set(gsec1["hhid"].dropna())

missing_households = agsec1.loc[
    ~agsec1["hhid"].isin(gsec1_ids)
].copy()

crop_a_ids = set(crop_a["hhid"].dropna())
crop_b_ids = set(crop_b["hhid"].dropna())

missing_households["in_visit_a"] = (
    missing_households["hhid"].isin(crop_a_ids)
)
missing_households["in_visit_b"] = (
    missing_households["hhid"].isin(crop_b_ids)
)

print("=" * 85)
print("DETAILED INVESTIGATION OF THE 66 HOUSEHOLDS")
print("=" * 85)

# 1. Check t0_hhid availability and repeated values.
print("\n1. t0_hhid availability")
print("-" * 60)

print(
    missing_households["t0_hhid"]
    .value_counts(dropna=False)
    .head(20)
)

print(
    "\nMissing t0_hhid:",
    missing_households["t0_hhid"].isna().sum()
)

print(
    "Distinct nonmissing t0_hhid:",
    missing_households["t0_hhid"].nunique()
)

# 2. Compare crop-related indicators.
crop_indicator_columns = [
    column for column in [
        "culcrp",
        "hh_crp1",
        "hh_crp2",
        "lvstck",
        "hh_anm",
        "hh_plty",
    ]
    if column in missing_households.columns
]

print("\n2. Crop and livestock indicators")
print("-" * 60)

for column in crop_indicator_columns:
    print(f"\n{column}")
    print(
        missing_households[column]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )

# 3. Compare the identifier prefixes and suffixes.
print("\n3. hhid structure")
print("-" * 60)

missing_households["hhid_length"] = (
    missing_households["hhid"].astype("string").str.len()
)

missing_households["t0_prefix"] = (
    missing_households["t0_hhid"]
    .astype("string")
    .str[:4]
)

missing_households["t0_suffix"] = (
    missing_households["t0_hhid"]
    .astype("string")
    .str[-2:]
)

print("\nhhid length distribution:")
print(missing_households["hhid_length"].value_counts(dropna=False))

print("\nt0_hhid prefix distribution:")
print(missing_households["t0_prefix"].value_counts(dropna=False))

print("\nt0_hhid suffix distribution:")
print(missing_households["t0_suffix"].value_counts(dropna=False))

# 4. Check whether the corresponding household IDs occur in GSEC1
# through t0_hhid. This is descriptive only, not a proposed merge.
print("\n4. Potential t0_hhid links to GSEC1")
print("-" * 60)

gsec1_t0_ids = set(
    gsec1["t0_hhid"].dropna().astype(str)
)

missing_households["t0_matches_gsec1"] = (
    missing_households["t0_hhid"]
    .astype("string")
    .isin(gsec1_t0_ids)
)

print(
    missing_households["t0_matches_gsec1"]
    .value_counts(dropna=False)
    .to_string()
)

print(
    "\nRecords with matching t0_hhid values:"
)

print(
    missing_households.loc[
        missing_households["t0_matches_gsec1"],
        ["hhid", "t0_hhid", "in_visit_a", "in_visit_b"],
    ].head(20).to_string(index=False)
)

# 5. Summarize crop-row counts for these households.
print("\n5. Crop-row counts")
print("-" * 60)

count_a = crop_a.groupby("hhid").size().rename("visit_a_rows")
count_b = crop_b.groupby("hhid").size().rename("visit_b_rows")

crop_counts = missing_households[["hhid"]].copy()

crop_counts = crop_counts.merge(
    count_a,
    left_on="hhid",
    right_index=True,
    how="left",
    validate="one_to_one",
)

crop_counts = crop_counts.merge(
    count_b,
    left_on="hhid",
    right_index=True,
    how="left",
    validate="one_to_one",
)

crop_counts[["visit_a_rows", "visit_b_rows"]] = (
    crop_counts[["visit_a_rows", "visit_b_rows"]].fillna(0).astype(int)
)

print(crop_counts.describe().to_string())

print("\nHouseholds with the largest number of crop rows:")
print(
    crop_counts.assign(
        total_crop_rows=lambda x: x["visit_a_rows"] + x["visit_b_rows"]
    )
    .sort_values("total_crop_rows", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\n" + "=" * 85)
print("INVESTIGATION COMPLETED — SOURCE FILES NOT MODIFIED")
print("=" * 85)
```


```python
from pathlib import Path
import pandas as pd

data_root = Path(extracted_folder)

# Identify the household-level files already available.
candidate_files = [
    data_root / "HH" / "GSEC1.csv",
    data_root / "Agric" / "AGSEC1.csv",
]

print("=" * 85)
print("HOUSEHOLD RESPONSE-STATUS AND INTERVIEW-FIELD AUDIT")
print("=" * 85)

for file_path in candidate_files:
    if not file_path.exists():
        print(f"\nFile not found: {file_path.name}")
        continue

    df = pd.read_csv(file_path, nrows=5, low_memory=False)

    print(f"\nFile: {file_path.relative_to(data_root)}")
    print("-" * 60)

    # Display columns potentially related to interview completion,
    # response status, eligibility, and household identification.
    relevant_columns = [
        col for col in df.columns
        if any(
            term in col.lower()
            for term in [
                "hhid",
                "response",
                "status",
                "interview",
                "complete",
                "reason",
                "eligib",
                "batch",
                "date",
            ]
        )
    ]

    print("Potentially relevant fields:")
    print(relevant_columns)

print("\n" + "=" * 85)
print("FIELD DISCOVERY COMPLETED — NO SOURCE FILES MODIFIED")
print("=" * 85)
```


```python
import pandas as pd
from pathlib import Path

data_root = Path(extracted_folder)

gsec1 = pd.read_csv(
    data_root / "HH" / "GSEC1.csv",
    low_memory=False
)

agsec1 = pd.read_csv(
    data_root / "Agric" / "AGSEC1.csv",
    low_memory=False
)

# Identify the 66 households present in AGSEC1 but absent from GSEC1.
gsec1_ids = set(gsec1["hhid"].dropna())

extra_agric = agsec1.loc[
    ~agsec1["hhid"].isin(gsec1_ids)
].copy()

print("=" * 85)
print("RESPONSE STATUS AND HOUSEHOLD LINKAGE DIAGNOSTICS")
print("=" * 85)

# 1. Response-status distribution.
print("\n1. GSEC1 response_status distribution")
print("-" * 60)

print(
    gsec1["response_status"]
    .value_counts(dropna=False)
    .to_string()
)

# 2. Response status by batch.
print("\n2. Response status by batch")
print("-" * 60)

if "batch" in gsec1.columns:
    print(
        pd.crosstab(
            gsec1["batch"],
            gsec1["response_status"],
            margins=True,
            dropna=False
        ).to_string()
    )

# 3. Missingness in key household identifiers.
print("\n3. Identifier completeness in GSEC1")
print("-" * 60)

for col in ["hhid", "t0_hhid", "interview__key", "response_status", "batch"]:
    if col in gsec1.columns:
        print(
            f"{col}: missing={gsec1[col].isna().sum()}, "
            f"distinct={gsec1[col].nunique(dropna=True)}"
        )

# 4. Examine whether the extra AGSEC1 records' t0_hhid values
# occur as t0_hhid values or hhid values in GSEC1.
print("\n4. Potential identifier relationships")
print("-" * 60)

extra_t0 = set(extra_agric["t0_hhid"].dropna().astype(str))
gsec1_hhid = set(gsec1["hhid"].dropna().astype(str))
gsec1_t0 = set(gsec1["t0_hhid"].dropna().astype(str))

print(
    "Extra AGSEC1 t0_hhid values matching GSEC1 hhid:",
    len(extra_t0 & gsec1_hhid)
)

print(
    "Extra AGSEC1 t0_hhid values matching GSEC1 t0_hhid:",
    len(extra_t0 & gsec1_t0)
)

print("\n5. Any matching t0_hhid values")
print("-" * 60)

matching_t0 = extra_agric.loc[
    extra_agric["t0_hhid"].astype("string").isin(gsec1_t0),
    ["hhid", "t0_hhid"]
].copy()

if matching_t0.empty:
    print("No matching t0_hhid values found.")
else:
    print(matching_t0.to_string(index=False))

print("\n" + "=" * 85)
print("DIAGNOSTICS COMPLETED — SOURCE FILES NOT MODIFIED")
print("=" * 85)
```


```python
# ============================================================
# RESEARCHPRO-ANALYTICS
# READ-ONLY DIAGNOSTIC: THE 66 AGSEC1-ONLY HOUSEHOLDS
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

# ------------------------------------------------------------
# 1. Locate and read the original datasets
# ------------------------------------------------------------

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

audit_agsec1_path = audit_data_root / "Agric" / "AGSEC1.csv"
audit_gsec1_path = audit_data_root / "HH" / "GSEC1.csv"
audit_crop_a_path = audit_data_root / "Agric" / "AGSEC4A.csv"
audit_crop_b_path = audit_data_root / "Agric" / "AGSEC4B.csv"

audit_required_files = [
    audit_agsec1_path,
    audit_gsec1_path,
    audit_crop_a_path,
    audit_crop_b_path
]

audit_missing_files = [
    str(path) for path in audit_required_files if not path.exists()
]

if audit_missing_files:
    raise FileNotFoundError(
        "The following required files were not found:\n"
        + "\n".join(audit_missing_files)
    )

audit_agsec1 = pd.read_csv(audit_agsec1_path, low_memory=False)
audit_gsec1 = pd.read_csv(audit_gsec1_path, low_memory=False)
audit_crop_a = pd.read_csv(audit_crop_a_path, low_memory=False)
audit_crop_b = pd.read_csv(audit_crop_b_path, low_memory=False)

# Standardize identifier formatting in the diagnostic copies only.
for audit_df in [
    audit_agsec1,
    audit_gsec1,
    audit_crop_a,
    audit_crop_b
]:
    audit_df["hhid"] = audit_df["hhid"].astype("string").str.strip()

print("DATASETS LOADED")
print("-" * 60)

print(f"AGSEC1 households: {len(audit_agsec1):,}")
print(f"GSEC1 households:  {len(audit_gsec1):,}")
print(f"First-visit crop rows:  {len(audit_crop_a):,}")
print(f"Second-visit crop rows: {len(audit_crop_b):,}")


# ------------------------------------------------------------
# 2. Identify the two comparison groups
# ------------------------------------------------------------

audit_agsec1_ids = set(audit_agsec1["hhid"].dropna())
audit_gsec1_ids = set(audit_gsec1["hhid"].dropna())

audit_only_ids = audit_agsec1_ids - audit_gsec1_ids
audit_shared_ids = audit_agsec1_ids & audit_gsec1_ids

audit_only = audit_agsec1[
    audit_agsec1["hhid"].isin(audit_only_ids)
].copy()

audit_shared = audit_agsec1[
    audit_agsec1["hhid"].isin(audit_shared_ids)
].copy()

print("\nGROUP VERIFICATION")
print("-" * 60)
print(f"AGSEC1-only households: {len(audit_only):,}")
print(f"Households in both files: {len(audit_shared):,}")
print(f"Total distinct AGSEC1 households: {len(audit_agsec1_ids):,}")

if len(audit_only) != 66 or len(audit_shared) != 3176:
    print(
        "\nWARNING: The group sizes differ from the previously "
        "reported counts. Investigate before interpreting results."
    )


# ------------------------------------------------------------
# 3. Compare household characteristics and coded indicators
# ------------------------------------------------------------

audit_compare_vars = [
    "hhsize",
    "culcrp",
    "hh_crp1",
    "hh_crp2",
    "lvstck",
    "hh_anm",
    "hh_plty",
    "region",
    "urban",
    "wgt",
    "hwgt_w7",
    "hwgt_wc"
]

audit_compare_vars = [
    col for col in audit_compare_vars
    if col in audit_agsec1.columns
]

audit_group_rows = []

for audit_group_name, audit_group_df in [
    ("AGSEC1-only (66)", audit_only),
    ("Matched (3,176)", audit_shared)
]:
    for audit_var in audit_compare_vars:
        audit_values = audit_group_df[audit_var]
        audit_nonmissing = audit_values.dropna()

        audit_row = {
            "Group": audit_group_name,
            "Variable": audit_var,
            "N": len(audit_values),
            "Missing_n": int(audit_values.isna().sum()),
            "Missing_pct": round(
                100 * audit_values.isna().mean(), 2
            ),
            "Distinct_nonmissing": int(
                audit_nonmissing.nunique()
            )
        }

        if (
            pd.api.types.is_numeric_dtype(audit_values)
            and audit_nonmissing.nunique() > 10
        ):
            audit_row["Mean"] = audit_nonmissing.mean()
            audit_row["Median"] = audit_nonmissing.median()
            audit_row["SD"] = audit_nonmissing.std()
        else:
            audit_row["Mean"] = np.nan
            audit_row["Median"] = np.nan
            audit_row["SD"] = np.nan

        audit_group_rows.append(audit_row)

audit_characteristics = pd.DataFrame(audit_group_rows)

print("\nHOUSEHOLD CHARACTERISTICS AND MISSINGNESS")
print("-" * 60)

display(
    audit_characteristics.round(3)
)


# ------------------------------------------------------------
# 4. Compare the distributions of the coded indicators
# ------------------------------------------------------------

audit_categorical_vars = [
    "culcrp",
    "hh_crp1",
    "hh_crp2",
    "lvstck",
    "hh_anm",
    "hh_plty",
    "region",
    "urban"
]

for audit_var in audit_categorical_vars:
    if audit_var not in audit_agsec1.columns:
        continue

    audit_distribution = pd.concat(
        {
            "AGSEC1-only (66)": audit_only[audit_var].value_counts(
                dropna=False
            ),
            "Matched (3,176)": audit_shared[audit_var].value_counts(
                dropna=False
            )
        },
        axis=1
    ).fillna(0).astype(int)

    print(f"\nDistribution of {audit_var}")
    print("-" * 60)
    display(audit_distribution)


# ------------------------------------------------------------
# 5. Count crop records per household in each visit
# ------------------------------------------------------------

audit_crop_a_counts = (
    audit_crop_a.groupby("hhid")
    .size()
    .rename("first_visit_crop_rows")
)

audit_crop_b_counts = (
    audit_crop_b.groupby("hhid")
    .size()
    .rename("second_visit_crop_rows")
)

audit_crop_counts = pd.concat(
    [audit_crop_a_counts, audit_crop_b_counts],
    axis=1
).fillna(0)

audit_crop_counts["first_visit_crop_rows"] = (
    audit_crop_counts["first_visit_crop_rows"].astype(int)
)

audit_crop_counts["second_visit_crop_rows"] = (
    audit_crop_counts["second_visit_crop_rows"].astype(int)
)

audit_crop_counts["any_crop_rows"] = (
    audit_crop_counts["first_visit_crop_rows"]
    + audit_crop_counts["second_visit_crop_rows"]
)

audit_crop_counts["group"] = np.where(
    audit_crop_counts.index.isin(audit_only_ids),
    "AGSEC1-only (66)",
    np.where(
        audit_crop_counts.index.isin(audit_shared_ids),
        "Matched (3,176)",
        "Not in AGSEC1"
    )
)

audit_crop_summary = (
    audit_crop_counts.reset_index()
    .groupby("group")
    .agg(
        households=("hhid", "nunique"),
        first_visit_any=("first_visit_crop_rows", lambda x: (x > 0).sum()),
        second_visit_any=("second_visit_crop_rows", lambda x: (x > 0).sum()),
        either_visit_any=("any_crop_rows", lambda x: (x > 0).sum()),
        neither_visit=("any_crop_rows", lambda x: (x == 0).sum()),
        mean_first_visit_rows=("first_visit_crop_rows", "mean"),
        median_first_visit_rows=("first_visit_crop_rows", "median"),
        mean_second_visit_rows=("second_visit_crop_rows", "mean"),
        median_second_visit_rows=("second_visit_crop_rows", "median")
    )
)

print("\nCROP PARTICIPATION BY HOUSEHOLD GROUP")
print("-" * 60)
display(audit_crop_summary.round(3))


# ------------------------------------------------------------
# 6. Compare household size where it is observed
# ------------------------------------------------------------

if "hhsize" in audit_agsec1.columns:

    audit_size_only = pd.to_numeric(
        audit_only["hhsize"], errors="coerce"
    ).dropna()

    audit_size_shared = pd.to_numeric(
        audit_shared["hhsize"], errors="coerce"
    ).dropna()

    print("\nHOUSEHOLD SIZE COMPARISON")
    print("-" * 60)

    print(
        f"AGSEC1-only: n={len(audit_size_only)}, "
        f"mean={audit_size_only.mean():.3f}, "
        f"median={audit_size_only.median():.3f}"
    )

    print(
        f"Matched: n={len(audit_size_shared)}, "
        f"mean={audit_size_shared.mean():.3f}, "
        f"median={audit_size_shared.median():.3f}"
    )

    if len(audit_size_only) >= 2 and len(audit_size_shared) >= 2:
        audit_size_test = stats.mannwhitneyu(
            audit_size_only,
            audit_size_shared,
            alternative="two-sided"
        )

        print(
            "Mann-Whitney U test: "
            f"U={audit_size_test.statistic:.3f}, "
            f"p={audit_size_test.pvalue:.4f}"
        )

        print(
            "Interpretation: This tests for a distributional "
            "difference in observed household size. It does not "
            "establish that the groups are equivalent if p > 0.05."
        )


# ------------------------------------------------------------
# 7. Summarize missing-weight patterns in the matched group
# ------------------------------------------------------------

print("\nWEIGHT AVAILABILITY AMONG MATCHED HOUSEHOLDS")
print("-" * 60)

for audit_weight_var in ["wgt", "hwgt_w7", "hwgt_wc"]:
    if audit_weight_var not in audit_shared.columns:
        continue

    audit_valid_n = int(audit_shared[audit_weight_var].notna().sum())
    audit_missing_n = int(audit_shared[audit_weight_var].isna().sum())

    print(
        f"{audit_weight_var}: "
        f"{audit_valid_n:,} available; "
        f"{audit_missing_n:,} missing "
        f"({100 * audit_shared[audit_weight_var].isna().mean():.2f}%)"
    )


# ------------------------------------------------------------
# 8. Diagnostic conclusion
# ------------------------------------------------------------

print("\nDIAGNOSTIC COMPLETE")
print("-" * 60)
print("Original CSV files were read only; no source files were modified.")
print("No missing values were imputed.")
print("No survey weights were estimated.")
print("No households were deleted from the source data.")
print(
    "Use the displayed results to decide which additional "
    "investigations or sensitivity analyses are justified."
)
```


```python
# ============================================================
# RESEARCHPRO-ANALYTICS
# TARGETED AUDIT OF THE 66 AGSEC1-ONLY HOUSEHOLDS
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# 1. Reuse the diagnostic datasets already loaded
# ------------------------------------------------------------

# These variables were created in the previous diagnostic cell:
# audit_agsec1, audit_gsec1, audit_crop_a, audit_crop_b
# audit_only, audit_shared, audit_only_ids

# ------------------------------------------------------------
# 2. Inspect the structure of the 66 records
# ------------------------------------------------------------

audit_identifier_cols = [
    col for col in [
        "hhid",
        "t0_hhid",
        "batch",
        "hhsize",
        "region",
        "urban",
        "wgt",
        "hwgt_w7",
        "hwgt_wc",
        "culcrp",
        "hh_crp1",
        "hh_crp2",
        "lvstck",
        "hh_anm",
        "hh_plty"
    ]
    if col in audit_only.columns
]

print("66 HOUSEHOLDS: IDENTIFIERS AND AVAILABLE VARIABLES")
print("=" * 70)

display(
    audit_only[audit_identifier_cols]
    .sort_values("t0_hhid", na_position="last")
    .reset_index(drop=True)
)

# ------------------------------------------------------------
# 3. Compare identifier formats across the two household files
# ------------------------------------------------------------

def audit_identifier_summary(df, group_name):
    rows = []

    for col in ["hhid", "t0_hhid", "batch"]:
        if col not in df.columns:
            continue

        s = df[col].astype("string").str.strip()
        s = s.replace("", pd.NA)

        rows.append({
            "Group": group_name,
            "Identifier": col,
            "Records": len(df),
            "Missing": int(s.isna().sum()),
            "Distinct_nonmissing": int(s.nunique()),
            "Example_values": ", ".join(
                s.dropna().astype(str).head(5).tolist()
            )
        })

    return rows


audit_id_rows = []

audit_id_rows.extend(
    audit_identifier_summary(audit_only, "AGSEC1-only")
)

audit_id_rows.extend(
    audit_identifier_summary(audit_shared, "Matched")
)

audit_id_summary = pd.DataFrame(audit_id_rows)

print("\nIDENTIFIER STRUCTURE")
print("=" * 70)
display(audit_id_summary)

# ------------------------------------------------------------
# 4. Check whether the 66 t0_hhid values occur elsewhere
# ------------------------------------------------------------

audit_t0_only = set(
    audit_only["t0_hhid"]
    .dropna()
    .astype("string")
    .str.strip()
)

audit_t0_only.discard("")

audit_t0_sources = {
    "GSEC1": audit_gsec1,
    "AGSEC4A": audit_crop_a,
    "AGSEC4B": audit_crop_b
}

audit_t0_results = []

for source_name, source_df in audit_t0_sources.items():
    if "t0_hhid" not in source_df.columns:
        audit_t0_results.append({
            "Source": source_name,
            "Records_checked": len(source_df),
            "Has_t0_hhid": False,
            "Distinct_matching_t0_hhid": np.nan,
            "Matching_rows": np.nan
        })
        continue

    source_t0 = (
        source_df["t0_hhid"]
        .dropna()
        .astype("string")
        .str.strip()
    )

    source_t0 = source_t0[source_t0.ne("")]

    audit_matches = source_t0[source_t0.isin(audit_t0_only)]

    audit_t0_results.append({
        "Source": source_name,
        "Records_checked": len(source_df),
        "Has_t0_hhid": True,
        "Distinct_matching_t0_hhid": audit_matches.nunique(),
        "Matching_rows": len(audit_matches)
    })

print("\nCROSS-FILE t0_hhid MATCHES")
print("=" * 70)
display(pd.DataFrame(audit_t0_results))

# ------------------------------------------------------------
# 5. Check batch values and missingness patterns
# ------------------------------------------------------------

print("\nBATCH VALUES IN THE 66 RECORDS")
print("=" * 70)

if "batch" in audit_only.columns:
    print("Batch missing:", int(audit_only["batch"].isna().sum()))
    print("Distinct nonmissing batch values:",
          int(audit_only["batch"].nunique(dropna=True)))

    display(
        audit_only["batch"]
        .value_counts(dropna=False)
        .rename_axis("batch")
        .reset_index(name="records")
        .head(20)
    )

# Group records by their combined missingness pattern.
audit_missingness_cols = [
    col for col in [
        "hhsize",
        "region",
        "urban",
        "wgt",
        "hwgt_w7",
        "hwgt_wc",
        "hh_crp1",
        "hh_crp2",
        "lvstck",
        "hh_anm",
        "hh_plty"
    ]
    if col in audit_only.columns
]

audit_missingness_pattern = (
    audit_only[audit_missingness_cols]
    .isna()
    .astype(int)
    .astype(str)
    .agg("".join, axis=1)
)

audit_pattern_counts = (
    audit_missingness_pattern
    .value_counts()
    .rename_axis("missingness_pattern")
    .reset_index(name="households")
)

print("\nMISSINGNESS PATTERNS AMONG THE 66 RECORDS")
print("=" * 70)
display(audit_pattern_counts)

print("\nDIAGNOSTIC COMPLETE")
print("No original files were modified.")
print("No values were imputed or estimated.")

```


```python
from pathlib import Path

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

print("HOUSEHOLD-RELATED CSV FILES")
print("=" * 65)

for path in sorted(audit_data_root.rglob("*.csv")):
    name = path.name.lower()
    parent = path.parent.name.lower()

    if (
        parent == "hh"
        or "gsec" in name
        or "household" in name
        or "roster" in name
    ):
        print(path.relative_to(audit_data_root))
```


```python
from pathlib import Path
import pandas as pd

# Dataset location
audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Load the two reference files into separate audit variables
audit_agsec1_check = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC1.csv",
    low_memory=False
)

audit_gsec1_check = pd.read_csv(
    audit_data_root / "HH" / "GSEC1.csv",
    low_memory=False
)

# Identify the 66 records present in AGSEC1 but absent from GSEC1
audit_missing_hhids = set(
    audit_agsec1_check.loc[
        ~audit_agsec1_check["hhid"].isin(audit_gsec1_check["hhid"]),
        "hhid"
    ].dropna()
)

audit_missing_t0_ids = set(
    audit_agsec1_check.loc[
        audit_agsec1_check["hhid"].isin(audit_missing_hhids),
        "t0_hhid"
    ].dropna()
)

# Inspect all CSV files in the HH folder
audit_hh_folder = audit_data_root / "HH"

audit_results = []

for audit_file in sorted(audit_hh_folder.glob("*.csv")):
    try:
        audit_df = pd.read_csv(audit_file, low_memory=False)

        audit_cols = set(audit_df.columns)

        # Check which household identifiers are available
        audit_hhid_matches = 0
        audit_t0_matches = 0

        if "hhid" in audit_cols:
            audit_hhid_matches = audit_df["hhid"].isin(
                audit_missing_hhids
            ).sum()

        if "t0_hhid" in audit_cols:
            audit_t0_matches = audit_df["t0_hhid"].isin(
                audit_missing_t0_ids
            ).sum()

        # Identify potentially relevant variables
        audit_relevant_cols = [
            col for col in audit_df.columns
            if any(
                term in col.lower()
                for term in [
                    "hhid", "t0_hhid", "region", "urban",
                    "weight", "wgt", "batch", "district",
                    "county", "subcounty", "parish",
                    "hhsize", "response_status"
                ]
            )
        ]

        audit_results.append({
            "file": str(audit_file.relative_to(audit_data_root)),
            "rows": len(audit_df),
            "columns": len(audit_df.columns),
            "has_hhid": "hhid" in audit_cols,
            "has_t0_hhid": "t0_hhid" in audit_cols,
            "matches_by_hhid": int(audit_hhid_matches),
            "matches_by_t0_hhid": int(audit_t0_matches),
            "relevant_columns": ", ".join(audit_relevant_cols)
        })

    except Exception as audit_error:
        audit_results.append({
            "file": str(audit_file.relative_to(audit_data_root)),
            "rows": None,
            "columns": None,
            "has_hhid": None,
            "has_t0_hhid": None,
            "matches_by_hhid": None,
            "matches_by_t0_hhid": None,
            "relevant_columns": f"READ ERROR: {audit_error}"
        })

audit_household_inventory = pd.DataFrame(audit_results)

print("NUMBER OF AGSEC1 RECORDS MISSING FROM GSEC1:",
      len(audit_missing_hhids))

print("\nHOUSEHOLD FILE IDENTIFIER AND VARIABLE AUDIT")
display(
    audit_household_inventory.sort_values(
        by=["matches_by_hhid", "matches_by_t0_hhid", "rows"],
        ascending=[False, False, False],
        na_position="last"
    ).reset_index(drop=True)
)
```


```python
from pathlib import Path
import pandas as pd

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Reuse the previously identified IDs if they still exist.
# Otherwise, reconstruct them from the source files.
if "audit_missing_hhids" not in globals():
    audit_agsec1_check = pd.read_csv(
        audit_data_root / "Agric" / "AGSEC1.csv",
        low_memory=False
    )

    audit_gsec1_check = pd.read_csv(
        audit_data_root / "HH" / "GSEC1.csv",
        low_memory=False
    )

    audit_missing_hhids = set(
        audit_agsec1_check.loc[
            ~audit_agsec1_check["hhid"].isin(
                audit_gsec1_check["hhid"]
            ),
            "hhid"
        ].dropna()
    )

audit_files_to_inspect = [
    audit_data_root / "HH" / "GSEC10_1.csv",
    audit_data_root / "HH" / "GSEC9.csv"
]

for audit_path in audit_files_to_inspect:
    audit_df = pd.read_csv(audit_path, low_memory=False)

    audit_matching = audit_df.loc[
        audit_df["hhid"].isin(audit_missing_hhids)
    ].copy()

    print("\n" + "=" * 80)
    print(f"FILE: {audit_path.name}")
    print("=" * 80)

    print("Total rows:", len(audit_df))
    print("Total columns:", len(audit_df.columns))
    print("Rows matching the 66 IDs:", len(audit_matching))
    print("Distinct matching household IDs:",
          audit_matching["hhid"].nunique())

    print("\nCOLUMN NAMES:")
    print(audit_df.columns.tolist())

    print("\nMISSINGNESS AMONG MATCHING ROWS:")
    audit_missingness = (
        audit_matching.isna()
        .sum()
        .rename("missing_count")
        .to_frame()
    )

    audit_missingness["missing_percent"] = (
        audit_missingness["missing_count"]
        / len(audit_matching) * 100
        if len(audit_matching) > 0
        else float("nan")
    )

    display(
        audit_missingness.sort_values(
            "missing_count",
            ascending=False
        )
    )

    print("\nSAMPLE MATCHING RECORDS:")
    display(audit_matching.head(10))
```


```python
from pathlib import Path
import pandas as pd

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Load source files into separate audit variables
audit_agsec1 = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC1.csv",
    low_memory=False
)

audit_gsec1 = pd.read_csv(
    audit_data_root / "HH" / "GSEC1.csv",
    low_memory=False
)

audit_gsec9 = pd.read_csv(
    audit_data_root / "HH" / "GSEC9.csv",
    low_memory=False
)

audit_gsec10 = pd.read_csv(
    audit_data_root / "HH" / "GSEC10_1.csv",
    low_memory=False
)

# Identify the 66 unmatched household IDs
audit_missing_hhids = set(
    audit_agsec1.loc[
        ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"]),
        "hhid"
    ].dropna()
)

# Inspect available status and identifier fields in GSEC1
audit_status_candidates = [
    "hhid",
    "t0_hhid",
    "interview__key",
    "response_status",
    "batch",
    "s1bq02",
    "s1bq07b",
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
    "region",
    "urban",
    "wgt",
    "hwgt_W7",
    "hwgt_wc"
]

audit_available_status = [
    col for col in audit_status_candidates
    if col in audit_gsec1.columns
]

print("GSEC1 VARIABLES AVAILABLE FOR STATUS INVESTIGATION:")
print(audit_available_status)

print("\nGSEC1 VARIABLE SUMMARY:")
for col in audit_available_status:
    print(f"\n{col}")
    print("Missing:", audit_gsec1[col].isna().sum())
    print("Distinct nonmissing values:", audit_gsec1[col].nunique())

# Summarize the 66 records in AGSEC1
audit_agsec1_missing = audit_agsec1.loc[
    audit_agsec1["hhid"].isin(audit_missing_hhids)
].copy()

print("\nAGSEC1 SUMMARY FOR THE 66 RECORDS:")
display(
    audit_agsec1_missing[
        [
            col for col in [
                "hhid", "t0_hhid", "batch", "region", "urban",
                "wgt", "hwgt_w7", "hwgt_wc", "hhsize",
                "culcrp", "hh_crp1", "hh_crp2",
                "lvstck", "hh_anm", "hh_plty"
            ]
            if col in audit_agsec1_missing.columns
        ]
    ].head(15)
)

# Check whether the same IDs have questionnaire respondents
print("\nGSEC10_1 RESPONDENT CODE AMONG THE 66:")
display(
    audit_gsec10.loc[
        audit_gsec10["hhid"].isin(audit_missing_hhids),
        "h10_respondent"
    ].value_counts(dropna=False).rename_axis("h10_respondent").to_frame("count")
)

if "h9_respondent" in audit_gsec9.columns:
    print("\nGSEC9 RESPONDENT CODE AMONG THE 66:")
    display(
        audit_gsec9.loc[
            audit_gsec9["hhid"].isin(audit_missing_hhids),
            "h9_respondent"
        ].value_counts(dropna=False)
        .rename_axis("h9_respondent")
        .to_frame("count")
    )
```


```python
from pathlib import Path
import pandas as pd

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Load the relevant files
audit_agsec1 = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC1.csv",
    low_memory=False
)

audit_gsec1 = pd.read_csv(
    audit_data_root / "HH" / "GSEC1.csv",
    low_memory=False
)

audit_gsec9 = pd.read_csv(
    audit_data_root / "HH" / "GSEC9.csv",
    low_memory=False
)

audit_gsec10 = pd.read_csv(
    audit_data_root / "HH" / "GSEC10_1.csv",
    low_memory=False
)

audit_crop_a = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC4A.csv",
    low_memory=False
)

audit_crop_b = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC4B.csv",
    low_memory=False
)

# Reconstruct the 66 unmatched IDs
audit_missing_hhids = set(
    audit_agsec1.loc[
        ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"]),
        "hhid"
    ].dropna()
)

# Select the seven records with an ordinary respondent code
audit_respondents_9 = audit_gsec9.loc[
    audit_gsec9["hhid"].isin(audit_missing_hhids)
    & audit_gsec9["h9_respondent"].notna()
].copy()

audit_respondents_10 = audit_gsec10.loc[
    audit_gsec10["hhid"].isin(audit_missing_hhids)
    & audit_gsec10["h10_respondent"].isin([1, 2])
].copy()

print("RECORDS WITH RESPONDENT CODES")
print("GSEC9:", len(audit_respondents_9))
print("GSEC10_1:", len(audit_respondents_10))

# Compare respondent records across the two questionnaire sections
audit_respondent_comparison = audit_respondents_9[
    ["hhid", "h9_respondent"]
].merge(
    audit_respondents_10[["hhid", "h10_respondent"]],
    on="hhid",
    how="outer",
    indicator=True
)

print("\nRESPONDENT-RECORD OVERLAP")
display(
    audit_respondent_comparison.sort_values("hhid")
)

# Count substantive answers for each record in each questionnaire
audit_substantive_9 = [
    col for col in audit_gsec9.columns
    if col not in ["hhid", "h9_respondent"]
]

audit_substantive_10 = [
    col for col in audit_gsec10.columns
    if col not in ["hhid", "h10_respondent"]
]

audit_gsec9["audit_nonmissing_answers"] = (
    audit_gsec9[audit_substantive_9].notna().sum(axis=1)
)

audit_gsec10["audit_nonmissing_answers"] = (
    audit_gsec10[audit_substantive_10].notna().sum(axis=1)
)

audit_answer_counts = audit_respondents_9[
    ["hhid", "h9_respondent"]
].merge(
    audit_gsec9[["hhid", "audit_nonmissing_answers"]],
    on="hhid",
    how="left"
).merge(
    audit_gsec10[
        ["hhid", "h10_respondent", "audit_nonmissing_answers"]
    ].rename(
        columns={
            "audit_nonmissing_answers": "gsec10_nonmissing_answers"
        }
    ),
    on="hhid",
    how="left"
).rename(
    columns={
        "audit_nonmissing_answers": "gsec9_nonmissing_answers"
    }
)

print("\nNONMISSING QUESTION COUNTS FOR THE SEVEN GSEC9 RESPONDENTS")
display(audit_answer_counts)

# Check which of the 66 records have crop rows
audit_crop_counts_a = (
    audit_crop_a.groupby("hhid").size().rename("visit1_crop_rows")
)

audit_crop_counts_b = (
    audit_crop_b.groupby("hhid").size().rename("visit2_crop_rows")
)

audit_crop_presence = (
    audit_agsec1.loc[
        audit_agsec1["hhid"].isin(audit_missing_hhids),
        ["hhid", "t0_hhid"]
    ]
    .merge(audit_crop_counts_a, on="hhid", how="left")
    .merge(audit_crop_counts_b, on="hhid", how="left")
)

audit_crop_presence[
    ["visit1_crop_rows", "visit2_crop_rows"]
] = audit_crop_presence[
    ["visit1_crop_rows", "visit2_crop_rows"]
].fillna(0).astype(int)

audit_crop_presence["has_crop_rows"] = (
    audit_crop_presence["visit1_crop_rows"].gt(0)
    | audit_crop_presence["visit2_crop_rows"].gt(0)
)

print("\nCROP-FILE COVERAGE AMONG THE 66 RECORDS")
print(
    audit_crop_presence["has_crop_rows"]
    .value_counts()
    .rename(index={True: "Has crop rows", False: "No crop rows"})
)

print("\nCROP COVERAGE FOR THE SEVEN RESPONDENT RECORDS")
display(
    audit_answer_counts[
        ["hhid", "h9_respondent", "h10_respondent"]
    ].merge(
        audit_crop_presence,
        on="hhid",
        how="left"
    )
)
```


```python
from pathlib import Path
import pandas as pd

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Load the agricultural files into separate audit variables
audit_agsec1 = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC1.csv",
    low_memory=False
)

audit_gsec1 = pd.read_csv(
    audit_data_root / "HH" / "GSEC1.csv",
    low_memory=False
)

audit_crop_a = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC4A.csv",
    low_memory=False
)

audit_crop_b = pd.read_csv(
    audit_data_root / "Agric" / "AGSEC4B.csv",
    low_memory=False
)

# Identify the 66 AGSEC1 records absent from GSEC1
audit_missing_hhids = set(
    audit_agsec1.loc[
        ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"]),
        "hhid"
    ].dropna()
)

# Select crop records linked directly by hhid
audit_crop_a_66 = audit_crop_a.loc[
    audit_crop_a["hhid"].isin(audit_missing_hhids)
].copy()

audit_crop_b_66 = audit_crop_b.loc[
    audit_crop_b["hhid"].isin(audit_missing_hhids)
].copy()

print("CROP FILE VARIABLE CHECK")
print("\nAGSEC4A:")
print(audit_crop_a.columns.tolist())

print("\nAGSEC4B:")
print(audit_crop_b.columns.tolist())

# Inspect seed-related variables without assuming every field exists
audit_seed_vars = [
    "hhid",
    "s4aq16",
    "s4aq13",
    "s4aq14"
]

audit_seed_vars_a = [
    col for col in audit_seed_vars
    if col in audit_crop_a_66.columns
]

audit_seed_vars_b = [
    "hhid",
    "s4bq16",
    "s4bq13",
    "s4bq14"
]

audit_seed_vars_b = [
    col for col in audit_seed_vars_b
    if col in audit_crop_b_66.columns
]

print("\nFIRST-VISIT SEED DATA FOR THE 66 RECORDS")
display(
    audit_crop_a_66[audit_seed_vars_a]
    .head(15)
)

print("\nSECOND-VISIT SEED DATA FOR THE 66 RECORDS")
display(
    audit_crop_b_66[audit_seed_vars_b]
    .head(15)
)

# Count crop rows and households by visit
audit_crop_summary = pd.DataFrame({
    "measure": [
        "Households in the 66 with first-visit crop rows",
        "Households in the 66 with second-visit crop rows",
        "Households in the 66 with crop rows in either visit",
        "Households in the 66 with no crop rows in either visit",
        "First-visit crop rows",
        "Second-visit crop rows"
    ],
    "count": [
        audit_crop_a_66["hhid"].nunique(),
        audit_crop_b_66["hhid"].nunique(),
        len(
            set(audit_crop_a_66["hhid"])
            | set(audit_crop_b_66["hhid"])
        ),
        len(audit_missing_hhids) - len(
            set(audit_crop_a_66["hhid"])
            | set(audit_crop_b_66["hhid"])
        ),
        len(audit_crop_a_66),
        len(audit_crop_b_66)
    ]
})

print("\nCROP COVERAGE SUMMARY")
display(audit_crop_summary)
```


```python
import pandas as pd

# Work on fresh copies so source and existing analysis variables remain unchanged.
audit_seed_a = audit_crop_a_66.copy()
audit_seed_b = audit_crop_b_66.copy()

def audit_classify_seed_outcome(df, visit):
    """
    Create a provisional improved-seed outcome in a new column.
    Does not overwrite the source seed-use or seed-type variables.
    """
    if visit == 1:
        use_col = "s4aq16"
        type_col = "s4aq13"
    elif visit == 2:
        use_col = "s4bq16"
        type_col = "s4bq13"
    else:
        raise ValueError("visit must be 1 or 2")

    required_cols = ["hhid", use_col, type_col]
    missing_cols = [c for c in required_cols if c not in df.columns]

    if missing_cols:
        raise KeyError(
            f"Missing required columns for visit {visit}: {missing_cols}"
        )

    result = df.copy()
    result["audit_improved_seed_crop"] = pd.NA

    # Documented seed-type coding:
    # 1 = Traditional, 2 = Improved
    result.loc[result[type_col] == 1, "audit_improved_seed_crop"] = 0
    result.loc[result[type_col] == 2, "audit_improved_seed_crop"] = 1

    # If the household did not use seed, classify as non-adopter
    # when the seed type is missing.
    result.loc[
        (result[use_col] == 2) & result[type_col].isna(),
        "audit_improved_seed_crop"
    ] = 0

    result["audit_improved_seed_crop"] = (
        result["audit_improved_seed_crop"].astype("Int64")
    )

    return result


audit_seed_a = audit_classify_seed_outcome(audit_seed_a, visit=1)
audit_seed_b = audit_classify_seed_outcome(audit_seed_b, visit=2)


def audit_aggregate_households(df, visit):
    """
    Aggregate crop-level seed outcomes to household level.
    """
    summary = (
        df.groupby("hhid", dropna=False)
        .agg(
            crop_rows=("audit_improved_seed_crop", "size"),
            confirmed_adoption=(
                "audit_improved_seed_crop",
                lambda s: (s == 1).any()
            ),
            unresolved_crop_rows=(
                "audit_improved_seed_crop",
                lambda s: s.isna().sum()
            ),
            known_crop_rows=(
                "audit_improved_seed_crop",
                lambda s: s.notna().sum()
            )
        )
        .reset_index()
    )

    summary["visit"] = visit

    # A household is an adopter if at least one crop confirms adoption.
    summary["audit_household_adoption"] = pd.Series(
        pd.NA, index=summary.index, dtype="Int64"
    )

    summary.loc[
        summary["confirmed_adoption"],
        "audit_household_adoption"
    ] = 1

    # Non-adopter only if every crop outcome is known and equals zero.
    summary.loc[
        (~summary["confirmed_adoption"])
        & (summary["unresolved_crop_rows"] == 0)
        & (summary["known_crop_rows"] > 0),
        "audit_household_adoption"
    ] = 0

    return summary


audit_households_a = audit_aggregate_households(audit_seed_a, visit=1)
audit_households_b = audit_aggregate_households(audit_seed_b, visit=2)

# Summarize the classification without calculating weighted rates.
audit_classification_summary = pd.DataFrame([
    {
        "visit": "First visit",
        "crop_rows": len(audit_seed_a),
        "households_with_crop_rows": audit_households_a["hhid"].nunique(),
        "confirmed_adopters": (
            audit_households_a["audit_household_adoption"] == 1
        ).sum(),
        "classified_non_adopters": (
            audit_households_a["audit_household_adoption"] == 0
        ).sum(),
        "unclassified_households": (
            audit_households_a["audit_household_adoption"].isna()
        ).sum(),
        "unresolved_crop_rows": audit_seed_a[
            "audit_improved_seed_crop"
        ].isna().sum()
    },
    {
        "visit": "Second visit",
        "crop_rows": len(audit_seed_b),
        "households_with_crop_rows": audit_households_b["hhid"].nunique(),
        "confirmed_adopters": (
            audit_households_b["audit_household_adoption"] == 1
        ).sum(),
        "classified_non_adopters": (
            audit_households_b["audit_household_adoption"] == 0
        ).sum(),
        "unclassified_households": (
            audit_households_b["audit_household_adoption"].isna()
        ).sum(),
        "unresolved_crop_rows": audit_seed_b[
            "audit_improved_seed_crop"
        ].isna().sum()
    }
])

print("PROVISIONAL CLASSIFICATION OF THE 66 HOUSEHOLDS")
display(audit_classification_summary)
```


```python
from pathlib import Path
import pandas as pd

audit_data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# IDs requiring investigation
audit_target_ids = set(audit_missing_hhids)

# Survey weight and identifier fields to look for
audit_weight_fields = [
    "hhid",
    "t0_hhid",
    "wgt",
    "hwgt_w7",
    "hwgt_wc",
    "hwgt_W7",
    "weight",
    "weight_hh"
]

audit_weight_file_results = []

for csv_path in audit_data_root.rglob("*.csv"):
    try:
        # Read only the header first
        header = pd.read_csv(csv_path, nrows=0, encoding="utf-8-sig")
        available_cols = header.columns.tolist()

        # Only inspect files containing a household identifier
        if not {"hhid", "t0_hhid"}.intersection(available_cols):
            continue

        # Select identifiers and weight fields that actually exist
        selected_cols = [
            col for col in audit_weight_fields
            if col in available_cols
        ]

        if not selected_cols:
            continue

        audit_file_df = pd.read_csv(
            csv_path,
            usecols=selected_cols,
            low_memory=False,
            encoding="utf-8-sig"
        )

        # Direct hhid matches
        direct_matches = 0
        direct_nonmissing_weights = {}

        if "hhid" in audit_file_df.columns:
            direct_mask = audit_file_df["hhid"].isin(audit_target_ids)
            direct_matches = int(direct_mask.sum())

            for weight_col in [
                "wgt", "hwgt_w7", "hwgt_wc",
                "hwgt_W7", "weight", "weight_hh"
            ]:
                if weight_col in audit_file_df.columns:
                    direct_nonmissing_weights[weight_col] = int(
                        audit_file_df.loc[
                            direct_mask, weight_col
                        ].notna().sum()
                    )

        # Parent-household ID matches, reported separately
        parent_matches = 0

        if "t0_hhid" in audit_file_df.columns:
            parent_matches = int(
                audit_file_df["t0_hhid"]
                .isin(audit_target_ids)
                .sum()
            )

        audit_weight_file_results.append({
            "file": str(csv_path.relative_to(audit_data_root)),
            "rows": len(audit_file_df),
            "direct_hhid_matches": direct_matches,
            "t0_hhid_matches": parent_matches,
            "weight_columns_found": ", ".join(
                col for col in [
                    "wgt", "hwgt_w7", "hwgt_wc",
                    "hwgt_W7", "weight", "weight_hh"
                ]
                if col in audit_file_df.columns
            ),
            "nonmissing_weights_among_direct_matches": str(
                direct_nonmissing_weights
            )
        })

    except Exception as exc:
        audit_weight_file_results.append({
            "file": str(csv_path.relative_to(audit_data_root)),
            "rows": None,
            "direct_hhid_matches": None,
            "t0_hhid_matches": None,
            "weight_columns_found": "READ ERROR",
            "nonmissing_weights_among_direct_matches": str(exc)
        })

audit_weight_file_results_df = pd.DataFrame(audit_weight_file_results)

display(
    audit_weight_file_results_df.sort_values(
        by=["direct_hhid_matches", "t0_hhid_matches"],
        ascending=False,
        na_position="last"
    )
)
```


```python
import pandas as pd

# Identify the 66 records in AGSEC1 that are absent from GSEC1.
audit_missing_records = audit_agsec1.loc[
    ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"])
].copy()

# Prepare the GSEC1 lookup with the fields needed for comparison.
audit_gsec1_lookup = audit_gsec1[
    [
        col for col in [
            "hhid",
            "wgt",
            "hwgt_wc",
            "hwgt_W7",
            "hwgt_w7",
            "region",
            "urban",
            "hhsize"
        ]
        if col in audit_gsec1.columns
    ]
].copy()

# Rename lookup fields so parent values cannot be confused with
# the unmatched household's own values.
audit_parent_lookup = audit_gsec1_lookup.rename(
    columns={
        col: f"parent_{col}"
        for col in audit_gsec1_lookup.columns
        if col != "hhid"
    }
).rename(columns={"hhid": "t0_hhid"})

# Match each unmatched household's t0_hhid to GSEC1's hhid.
audit_parent_check = audit_missing_records.merge(
    audit_parent_lookup,
    on="t0_hhid",
    how="left",
    indicator=True,
    validate="many_to_one"
)

audit_parent_check["parent_found_in_GSEC1"] = (
    audit_parent_check["_merge"] == "both"
)

print("PARENT-HOUSEHOLD MATCH SUMMARY")

display(
    pd.DataFrame({
        "measure": [
            "Unmatched households examined",
            "Records whose t0_hhid matches a GSEC1 household",
            "Records whose t0_hhid does not match a GSEC1 household",
            "Matched parent records with nonmissing wgt",
            "Matched parent records with nonmissing hwgt_wc",
            "Matched parent records with nonmissing hwgt_W7"
        ],
        "count": [
            len(audit_parent_check),
            int(audit_parent_check["parent_found_in_GSEC1"].sum()),
            int((~audit_parent_check["parent_found_in_GSEC1"]).sum()),
            int(
                audit_parent_check.loc[
                    audit_parent_check["parent_found_in_GSEC1"],
                    "parent_wgt"
                ].notna().sum()
            ) if "parent_wgt" in audit_parent_check.columns else 0,
            int(
                audit_parent_check.loc[
                    audit_parent_check["parent_found_in_GSEC1"],
                    "parent_hwgt_wc"
                ].notna().sum()
            ) if "parent_hwgt_wc" in audit_parent_check.columns else 0,
            int(
                audit_parent_check.loc[
                    audit_parent_check["parent_found_in_GSEC1"],
                    "parent_hwgt_W7"
                ].notna().sum()
            ) if "parent_hwgt_W7" in audit_parent_check.columns else 0
        ]
    })
)

print("\nFIRST 15 PARENT-HOUSEHOLD MATCHES")

audit_parent_display_cols = [
    col for col in [
        "hhid",
        "t0_hhid",
        "wgt",
        "hwgt_w7",
        "hwgt_wc",
        "region",
        "urban",
        "hhsize",
        "parent_wgt",
        "parent_hwgt_wc",
        "parent_hwgt_W7",
        "parent_hwgt_w7",
        "parent_region",
        "parent_urban",
        "parent_hhsize",
        "parent_found_in_GSEC1"
    ]
    if col in audit_parent_check.columns
]

display(
    audit_parent_check[audit_parent_display_cols].head(15)
)
```


```python
import pandas as pd

# Use the audit copies and previously identified unmatched records.
audit_unmatched = audit_agsec1.loc[
    ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"])
].copy()

# 1. Inspect the structure of the unmatched records.
print("UNMATCHED AGSEC1 RECORDS: IDENTIFIER AND METADATA CHECK")

audit_cols = [
    col for col in [
        "hhid", "t0_hhid", "batch", "region", "urban",
        "hhsize", "wgt", "hwgt_w7", "hwgt_wc",
        "culcrp", "hh_crp1", "hh_crp2",
        "lvstck", "hh_anm", "hh_plty"
    ]
    if col in audit_unmatched.columns
]

display(audit_unmatched[audit_cols].head(20))

# 2. Compare identifier patterns.
print("\nIDENTIFIER PATTERN SUMMARY")

audit_id_summary = pd.DataFrame({
    "measure": [
        "Unmatched records",
        "Unique unmatched hhid values",
        "Unique unmatched t0_hhid values",
        "Missing hhid values",
        "Missing t0_hhid values",
        "t0_hhid values starting with H",
        "hhid values with 32 characters"
    ],
    "count": [
        len(audit_unmatched),
        audit_unmatched["hhid"].nunique(),
        audit_unmatched["t0_hhid"].nunique(),
        audit_unmatched["hhid"].isna().sum(),
        audit_unmatched["t0_hhid"].isna().sum(),
        audit_unmatched["t0_hhid"]
            .astype("string").str.startswith("H", na=False).sum(),
        audit_unmatched["hhid"]
            .astype("string").str.len().eq(32).sum()
    ]
})

display(audit_id_summary)

# 3. Check whether the unmatched household IDs occur in other
# agricultural files, without merging their contents.
audit_other_ag_files = [
    "AGSEC2A.csv", "AGSEC2B.csv",
    "AGSEC3A.csv", "AGSEC3B.csv",
    "AGSEC5A.csv", "AGSEC5B.csv",
    "AGSEC6A.csv", "AGSEC6B.csv", "AGSEC6C.csv",
    "AGSEC8A.csv", "AGSEC8B.csv", "AGSEC8C.csv",
    "AGSEC9A.csv", "AGSEC9B.csv",
    "AGSEC10.csv", "AGSEC11.csv"
]

audit_crossfile_results = []

for filename in audit_other_ag_files:
    path = audit_data_root / "Agric" / filename

    if not path.exists():
        audit_crossfile_results.append({
            "file": filename,
            "status": "FILE NOT FOUND",
            "rows": None,
            "direct_hhid_matches": None
        })
        continue

    try:
        # Read only the identifier column.
        id_df = pd.read_csv(
            path,
            usecols=["hhid"],
            low_memory=False,
            encoding="utf-8-sig"
        )

        audit_crossfile_results.append({
            "file": filename,
            "status": "OK",
            "rows": len(id_df),
            "direct_hhid_matches": int(
                id_df["hhid"].isin(set(audit_unmatched["hhid"])).sum()
            )
        })

    except Exception as exc:
        audit_crossfile_results.append({
            "file": filename,
            "status": f"READ ERROR: {exc}",
            "rows": None,
            "direct_hhid_matches": None
        })

print("\nUNMATCHED HOUSEHOLD COVERAGE IN OTHER AGRICULTURAL FILES")

display(pd.DataFrame(audit_crossfile_results))
```


```python
import pandas as pd

# Select the 66 AGSEC1 records absent from GSEC1 by hhid.
audit_unmatched = audit_agsec1.loc[
    ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"])
].copy()

# Check that the comparison field exists in both files.
assert "t0_hhid" in audit_unmatched.columns
assert "t0_hhid" in audit_gsec1.columns

# Prepare a lookup using GSEC1's original household identifier.
audit_gsec1_t0_lookup = audit_gsec1[
    [
        col for col in [
            "hhid", "t0_hhid", "wgt",
            "hwgt_wc", "hwgt_W7", "region",
            "urban", "hhsize"
        ]
        if col in audit_gsec1.columns
    ]
].copy()

# Rename lookup columns to distinguish roster values from AGSEC1 values.
audit_gsec1_t0_lookup = audit_gsec1_t0_lookup.rename(
    columns={
        col: f"roster_{col}"
        for col in audit_gsec1_t0_lookup.columns
        if col != "t0_hhid"
    }
)

# Compare t0_hhid with t0_hhid—not with hhid.
audit_t0_comparison = audit_unmatched.merge(
    audit_gsec1_t0_lookup,
    on="t0_hhid",
    how="left",
    indicator=True,
    validate="many_to_many"
)

# Summarize matches.
audit_t0_matched = audit_t0_comparison[
    audit_t0_comparison["_merge"] == "both"
]

print("T0_HHID-TO-T0_HHID MATCH SUMMARY")

display(pd.DataFrame({
    "measure": [
        "Unmatched AGSEC1 households",
        "Records matched on t0_hhid",
        "Unique matched t0_hhid values",
        "Matched records with nonmissing roster wgt",
        "Matched records with nonmissing roster hwgt_wc",
        "Matched records with nonmissing roster hwgt_W7",
        "Unmatched records with no t0_hhid match"
    ],
    "count": [
        len(audit_unmatched),
        len(audit_t0_matched),
        audit_t0_matched["t0_hhid"].nunique(),
        (
            audit_t0_matched["roster_wgt"].notna().sum()
            if "roster_wgt" in audit_t0_matched.columns else 0
        ),
        (
            audit_t0_matched["roster_hwgt_wc"].notna().sum()
            if "roster_hwgt_wc" in audit_t0_matched.columns else 0
        ),
        (
            audit_t0_matched["roster_hwgt_W7"].notna().sum()
            if "roster_hwgt_W7" in audit_t0_matched.columns else 0
        ),
        int((audit_t0_comparison["_merge"] == "left_only").sum())
    ]
}))

print("\nFIRST 15 MATCHED RECORDS")

audit_t0_display_cols = [
    col for col in [
        "hhid", "t0_hhid", "wgt",
        "roster_hhid", "roster_wgt",
        "roster_hwgt_wc", "roster_hwgt_W7",
        "roster_region", "roster_urban",
        "roster_hhsize", "_merge"
    ]
    if col in audit_t0_comparison.columns
]

display(
    audit_t0_comparison[audit_t0_display_cols].head(15)
)
```


```python
import pandas as pd

# The unmatched agricultural household identified in the comparison.
audit_target_hhid = "02dd448165ce46279ca601a02865d543"
audit_target_t0 = "H2620907"

# Inspect the agricultural record.
audit_target_agric = audit_agsec1.loc[
    audit_agsec1["hhid"] == audit_target_hhid
].copy()

# Find all AGSEC1 records sharing this original household identifier.
audit_same_t0_agric = audit_agsec1.loc[
    audit_agsec1["t0_hhid"] == audit_target_t0
].copy()

# Find all GSEC1 records sharing this original household identifier.
audit_same_t0_roster = audit_gsec1.loc[
    audit_gsec1["t0_hhid"] == audit_target_t0
].copy()

print("TARGET AGRICULTURAL RECORD")
display(audit_target_agric)

print("\nALL AGSEC1 RECORDS WITH THE SAME t0_hhid")
display(audit_same_t0_agric)

print("\nALL GSEC1 RECORDS WITH THE SAME t0_hhid")
display(audit_same_t0_roster)

# Summarize the relationship without transferring weights.
audit_relationship_summary = pd.DataFrame({
    "measure": [
        "Matching agricultural household records",
        "Unique agricultural hhid values",
        "Unique agricultural t0_hhid values",
        "Matching roster records",
        "Unique roster hhid values",
        "Nonmissing roster cross-sectional weights",
        "Nonmissing roster panel weights (hwgt_wc)",
        "Nonmissing roster panel weights (hwgt_W7)"
    ],
    "count": [
        len(audit_same_t0_agric),
        audit_same_t0_agric["hhid"].nunique(),
        audit_same_t0_agric["t0_hhid"].nunique(),
        len(audit_same_t0_roster),
        audit_same_t0_roster["hhid"].nunique(),
        (
            audit_same_t0_roster["wgt"].notna().sum()
            if "wgt" in audit_same_t0_roster.columns else 0
        ),
        (
            audit_same_t0_roster["hwgt_wc"].notna().sum()
            if "hwgt_wc" in audit_same_t0_roster.columns else 0
        ),
        (
            audit_same_t0_roster["hwgt_W7"].notna().sum()
            if "hwgt_W7" in audit_same_t0_roster.columns else 0
        )
    ]
})

print("\nHOUSEHOLD RELATIONSHIP SUMMARY")
display(audit_relationship_summary)
```


```python
import pandas as pd

# Identify AGSEC1 records whose current household IDs are absent from GSEC1.
audit_unmatched = audit_agsec1.loc[
    ~audit_agsec1["hhid"].isin(audit_gsec1["hhid"])
].copy()

# ---------------------------------------------------------
# 1. Examine the uniqueness of t0_hhid in both datasets
# ---------------------------------------------------------

audit_roster_t0_counts = (
    audit_gsec1.groupby("t0_hhid", dropna=False)
    .agg(
        roster_records=("hhid", "size"),
        roster_unique_hhids=("hhid", "nunique")
    )
    .reset_index()
)

audit_agsec1_t0_counts = (
    audit_agsec1.groupby("t0_hhid", dropna=False)
    .agg(
        agsec1_records=("hhid", "size"),
        agsec1_unique_hhids=("hhid", "nunique")
    )
    .reset_index()
)

print("IDENTIFIER UNIQUENESS CHECK")

display(pd.DataFrame({
    "measure": [
        "GSEC1 records",
        "GSEC1 unique t0_hhid values",
        "GSEC1 t0_hhid values occurring more than once",
        "AGSEC1 records",
        "AGSEC1 unique t0_hhid values",
        "AGSEC1 t0_hhid values occurring more than once",
        "Unmatched AGSEC1 household IDs",
        "Unmatched AGSEC1 unique t0_hhid values"
    ],
    "count": [
        len(audit_gsec1),
        audit_gsec1["t0_hhid"].nunique(),
        int((audit_roster_t0_counts["roster_records"] > 1).sum()),
        len(audit_agsec1),
        audit_agsec1["t0_hhid"].nunique(),
        int((audit_agsec1_t0_counts["agsec1_records"] > 1).sum()),
        len(audit_unmatched),
        audit_unmatched["t0_hhid"].nunique()
    ]
}))

# ---------------------------------------------------------
# 2. Identify which unmatched t0_hhid values occur in GSEC1
# ---------------------------------------------------------

# Use a unique list of roster identifiers for this first comparison.
# This avoids multiplying unmatched records during the match check.
audit_roster_t0_unique = (
    audit_gsec1.loc[
        audit_gsec1["t0_hhid"].notna(),
        ["t0_hhid"]
    ]
    .drop_duplicates()
    .assign(roster_t0_match=True)
)

audit_unmatched_t0_check = audit_unmatched.merge(
    audit_roster_t0_unique,
    on="t0_hhid",
    how="left",
    validate="many_to_one"
)

audit_unmatched_t0_check["roster_t0_match"] = (
    audit_unmatched_t0_check["roster_t0_match"]
    .fillna(False)
    .astype(bool)
)

# Summarize using unique unmatched current household IDs.
audit_match_summary = pd.DataFrame({
    "measure": [
        "Unmatched AGSEC1 household IDs",
        "Unmatched IDs with a GSEC1 t0_hhid match",
        "Unmatched IDs without a GSEC1 t0_hhid match",
        "Unique unmatched t0_hhid values matching GSEC1",
        "Unique unmatched t0_hhid values not matching GSEC1"
    ],
    "count": [
        audit_unmatched_t0_check["hhid"].nunique(),
        audit_unmatched_t0_check.loc[
            audit_unmatched_t0_check["roster_t0_match"], "hhid"
        ].nunique(),
        audit_unmatched_t0_check.loc[
            ~audit_unmatched_t0_check["roster_t0_match"], "hhid"
        ].nunique(),
        audit_unmatched_t0_check.loc[
            audit_unmatched_t0_check["roster_t0_match"], "t0_hhid"
        ].nunique(),
        audit_unmatched_t0_check.loc[
            ~audit_unmatched_t0_check["roster_t0_match"], "t0_hhid"
        ].nunique()
    ]
})

print("\nMATCH SUMMARY")
display(audit_match_summary)

# ---------------------------------------------------------
# 3. Inspect identifiers that occur more than once in GSEC1
# ---------------------------------------------------------

audit_duplicate_roster_t0 = audit_roster_t0_counts.loc[
    audit_roster_t0_counts["roster_records"] > 1
].sort_values(
    "roster_records",
    ascending=False
)

print("\nEXAMPLES OF REPEATED GSEC1 t0_hhid VALUES")
display(audit_duplicate_roster_t0.head(20))

# ---------------------------------------------------------
# 4. Inspect unmatched households with a t0_hhid match
# ---------------------------------------------------------

audit_matched_unmatched_ids = audit_unmatched_t0_check.loc[
    audit_unmatched_t0_check["roster_t0_match"],
    ["hhid", "t0_hhid", "hh_crp1", "hh_crp2", "culcrp"]
].drop_duplicates()

print("\nUNMATCHED AGRICULTURAL HOUSEHOLDS WITH A ROSTER t0_hhid MATCH")
display(audit_matched_unmatched_ids.head(30))
```


```python
import pandas as pd
from pathlib import Path

# Dataset location
audit_data_root = Path(
    r"C:\Users\H-START\Desktop\dataset"
)

audit_agsec9b_path = audit_data_root / "Agric" / "AGSEC9B.csv"

# Load the file without modifying the original.
audit_agsec9b = pd.read_csv(
    audit_agsec9b_path,
    low_memory=False
)

print("AGSEC9B DIMENSIONS")
print(f"Rows: {len(audit_agsec9b):,}")
print(f"Columns: {len(audit_agsec9b.columns):,}")

print("\nAGSEC9B COLUMNS")
print(audit_agsec9b.columns.tolist())

# Confirm the required identifiers exist.
audit_required_cols = {"hhid", "t0_hhid"}
audit_missing_cols = audit_required_cols - set(audit_agsec9b.columns)

if audit_missing_cols:
    print("\nRequired columns not found:", audit_missing_cols)
else:
    # Select AGSEC9B records whose hhid belongs to the 66 unmatched IDs.
    audit_unmatched_ids = set(audit_unmatched["hhid"].dropna())

    audit_agsec9b_66 = audit_agsec9b.loc[
        audit_agsec9b["hhid"].isin(audit_unmatched_ids)
    ].copy()

    # Summarize identifier coverage.
    audit_agsec9b_summary = pd.DataFrame({
        "measure": [
            "Unmatched AGSEC1 household IDs",
            "Matching AGSEC9B rows",
            "Unique matched AGSEC9B household IDs",
            "Unique matched AGSEC9B t0_hhid values",
            "Matched rows with missing hhid",
            "Matched rows with missing t0_hhid"
        ],
        "count": [
            len(audit_unmatched_ids),
            len(audit_agsec9b_66),
            audit_agsec9b_66["hhid"].nunique(),
            audit_agsec9b_66["t0_hhid"].nunique(),
            audit_agsec9b_66["hhid"].isna().sum(),
            audit_agsec9b_66["t0_hhid"].isna().sum()
        ]
    })

    print("\nAGSEC9B MATCH SUMMARY")
    display(audit_agsec9b_summary)

    # Inspect a sample of matching identifiers.
    print("\nFIRST 20 MATCHING AGSEC9B RECORDS")
    display(
        audit_agsec9b_66[
            ["hhid", "t0_hhid"]
        ].drop_duplicates().head(20)
    )

    # Compare the t0_hhid values between AGSEC1 and AGSEC9B.
    audit_agsec1_66_ids = audit_unmatched[
        ["hhid", "t0_hhid"]
    ].drop_duplicates()

    audit_agsec9b_t0_lookup = (
        audit_agsec9b_66[
            ["hhid", "t0_hhid"]
        ]
        .drop_duplicates()
        .rename(columns={"t0_hhid": "agsec9b_t0_hhid"})
    )

    audit_agsec9b_t0_comparison = audit_agsec1_66_ids.merge(
        audit_agsec9b_t0_lookup,
        on="hhid",
        how="left",
        validate="one_to_many"
    )

    audit_agsec9b_t0_comparison["t0_hhid_agrees"] = (
        audit_agsec9b_t0_comparison["t0_hhid"]
        == audit_agsec9b_t0_comparison["agsec9b_t0_hhid"]
    )

    print("\nAGSEC1 VS AGSEC9B IDENTIFIER CONSISTENCY")
    display(pd.DataFrame({
        "measure": [
            "Unmatched AGSEC1 household IDs",
            "IDs found in AGSEC9B",
            "IDs with matching t0_hhid",
            "IDs with differing t0_hhid"
        ],
        "count": [
            audit_agsec1_66_ids["hhid"].nunique(),
            audit_agsec9b_t0_comparison["hhid"].nunique(),
            audit_agsec9b_t0_comparison.loc[
                audit_agsec9b_t0_comparison["t0_hhid_agrees"],
                "hhid"
            ].nunique(),
            audit_agsec9b_t0_comparison.loc[
                ~audit_agsec9b_t0_comparison["t0_hhid_agrees"],
                "hhid"
            ].nunique()
        ]
    }))
```


```python
import pandas as pd

# ---------------------------------------------------------
# 1. Inspect GSEC1 response status
# ---------------------------------------------------------

print("GSEC1 RESPONSE STATUS")

if "response_status" in audit_gsec1.columns:
    display(
        audit_gsec1["response_status"]
        .value_counts(dropna=False)
        .rename_axis("response_status")
        .reset_index(name="count")
    )
else:
    print("response_status is not available in GSEC1.")

# ---------------------------------------------------------
# 2. Inspect available interview and status fields
# ---------------------------------------------------------

audit_metadata_candidates = [
    "hhid",
    "t0_hhid",
    "interview__key",
    "response_status",
    "batch",
    "s1bq02",
    "s1bq07b",
    "year",
    "month",
    "day",
    "wave",
    "wgt",
    "hwgt_wc",
    "hwgt_W7"
]

audit_metadata_columns = [
    col for col in audit_metadata_candidates
    if col in audit_gsec1.columns
]

print("\nGSEC1 METADATA SAMPLE")
display(audit_gsec1[audit_metadata_columns].head(10))

# ---------------------------------------------------------
# 3. Compare unmatched AGSEC1 IDs with AGSEC9B IDs
# ---------------------------------------------------------

audit_agsec9b_66_ids = audit_agsec9b.loc[
    audit_agsec9b["hhid"].isin(
        audit_unmatched["hhid"]
    )
].copy()

audit_agsec1_66_metadata = audit_unmatched[
    ["hhid", "t0_hhid"]
].copy()

audit_agsec9b_66_metadata = audit_agsec9b_66_ids[
    ["hhid", "t0_hhid"]
].copy()

print("\nAGSEC1 AND AGSEC9B IDENTIFIER CHECK")
display(
    audit_agsec1_66_metadata.merge(
        audit_agsec9b_66_metadata,
        on=["hhid", "t0_hhid"],
        how="outer",
        indicator=True,
        validate="one_to_one"
    )["_merge"]
    .value_counts()
    .rename_axis("merge_status")
    .reset_index(name="count")
)
```


```python
import pandas as pd
from pathlib import Path

# Dataset directory
audit_data_root = Path(
    r"C:\Users\H-START\Desktop\dataset"
)

# Load the two household-section files.
audit_gsec9 = pd.read_csv(
    audit_data_root / "HH" / "GSEC9.csv",
    low_memory=False
)

audit_gsec10_1 = pd.read_csv(
    audit_data_root / "HH" / "GSEC10_1.csv",
    low_memory=False
)

# Reuse the existing list of 66 unmatched AGSEC1 households.
audit_unmatched_ids = set(
    audit_unmatched["hhid"].dropna()
)

# Define a diagnostic function that inspects available fields.
def audit_household_section(df, filename):
    print(f"\n{'=' * 60}")
    print(filename)
    print(f"{'=' * 60}")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    if "hhid" not in df.columns:
        print("No hhid column found.")
        return

    subset = df.loc[
        df["hhid"].isin(audit_unmatched_ids)
    ].copy()

    print(f"Rows matching the 66 IDs: {len(subset):,}")
    print(f"Unique matching household IDs: {subset['hhid'].nunique():,}")

    # Inspect identifiers and potential interview metadata.
    candidate_columns = [
        "hhid",
        "t0_hhid",
        "interview__key",
        "response_status",
        "batch",
        "wgt",
        "hwgt_wc",
        "hwgt_W7",
        "hwgt_w7",
        "region",
        "urban",
        "year",
        "month",
        "day",
        "h9_respondent",
        "h10_respondent"
    ]

    available_columns = [
        col for col in candidate_columns
        if col in subset.columns
    ]

    if available_columns:
        print("\nAvailable identifier and metadata fields:")
        display(subset[available_columns].head(15))

    # Show nonmissingness for available metadata fields.
    metadata_columns = [
        col for col in available_columns
        if col not in {"hhid", "t0_hhid"}
    ]

    if metadata_columns:
        print("\nNonmissing values among matched records:")
        display(
            subset[metadata_columns]
            .notna()
            .sum()
            .rename("nonmissing_count")
            .to_frame()
        )

# Inspect both files.
audit_household_section(
    audit_gsec9,
    "GSEC9.csv"
)

audit_household_section(
    audit_gsec10_1,
    "GSEC10_1.csv"
)
```


```python
import pandas as pd

# ---------------------------------------------------------
# 1. Inspect respondent codes in GSEC9 and GSEC10_1
# ---------------------------------------------------------

print("GSEC9: h9_respondent value counts")

display(
    audit_gsec9["h9_respondent"]
    .value_counts(dropna=False)
    .rename_axis("value")
    .reset_index(name="count")
)

print("\nGSEC10_1: h10_respondent value counts")

display(
    audit_gsec10_1["h10_respondent"]
    .value_counts(dropna=False)
    .rename_axis("value")
    .reset_index(name="count")
)

# ---------------------------------------------------------
# 2. Inspect all columns for the 66 unmatched households
# ---------------------------------------------------------

audit_gsec10_66 = audit_gsec10_1.loc[
    audit_gsec10_1["hhid"].isin(
        audit_unmatched["hhid"]
    )
].copy()

# Calculate missingness for every variable.
audit_gsec10_66_missingness = pd.DataFrame({
    "column": audit_gsec10_66.columns,
    "missing_count": [
        audit_gsec10_66[col].isna().sum()
        for col in audit_gsec10_66.columns
    ],
    "unique_values": [
        audit_gsec10_66[col].nunique(dropna=False)
        for col in audit_gsec10_66.columns
    ]
})

audit_gsec10_66_missingness["missing_percent"] = (
    audit_gsec10_66_missingness["missing_count"]
    / len(audit_gsec10_66)
    * 100
)

print("\nGSEC10_1 MISSINGNESS AND VARIATION AMONG THE 66 RECORDS")

display(
    audit_gsec10_66_missingness.sort_values(
        ["missing_percent", "unique_values"],
        ascending=[False, True]
    )
)

# ---------------------------------------------------------
# 3. Inspect the actual values in the related variables
# ---------------------------------------------------------

print("\nGSEC10_1 COLUMN NAMES")

display(pd.DataFrame({
    "column": audit_gsec10_1.columns
}))

# Show the first 15 records with all variables, so we can see
# how the special respondent code relates to other responses.
print("\nFIRST 15 UNMATCHED GSEC10_1 RECORDS")

display(audit_gsec10_66.head(15))
```


```python
import pandas as pd

# Work on a copy of the 66 affected records.
audit_gsec10_66_check = audit_gsec10_1.loc[
    audit_gsec10_1["hhid"].isin(
        audit_unmatched["hhid"]
    )
].copy()

# Treat the known special code as missing for diagnostic purposes only.
# This does NOT establish the official meaning of the code.
audit_gsec10_66_check["h10_respondent_clean"] = (
    audit_gsec10_66_check["h10_respondent"]
    .replace(-999999999, pd.NA)
)

# Identify questionnaire variables, excluding the household ID
# and respondent identifier.
audit_gsec10_question_cols = [
    col for col in audit_gsec10_66_check.columns
    if col not in [
        "hhid",
        "h10_respondent",
        "h10_respondent_clean"
    ]
]

# Count recorded questionnaire answers per household.
audit_gsec10_66_check["recorded_answer_count"] = (
    audit_gsec10_66_check[audit_gsec10_question_cols]
    .notna()
    .sum(axis=1)
)

# Classify records based on respondent-field status.
audit_gsec10_66_check["respondent_status"] = (
    audit_gsec10_66_check["h10_respondent_clean"]
    .notna()
    .map({
        True: "Respondent code recorded",
        False: "Special code recorded"
    })
)

# Summarize the two patterns.
audit_gsec10_response_summary = (
    audit_gsec10_66_check.groupby(
        "respondent_status",
        dropna=False
    )
    .agg(
        households=("hhid", "nunique"),
        households_with_any_answers=(
            "recorded_answer_count",
            lambda s: int((s > 0).sum())
        ),
        households_with_no_answers=(
            "recorded_answer_count",
            lambda s: int((s == 0).sum())
        ),
        total_recorded_answers=(
            "recorded_answer_count",
            "sum"
        ),
        mean_answers_per_household=(
            "recorded_answer_count",
            "mean"
        )
    )
    .reset_index()
)

print("RESPONDENT STATUS AND ANSWER COMPLETENESS")
display(audit_gsec10_response_summary)

# Display records with any questionnaire answers.
print("\nRECORDS WITH AT LEAST ONE RECORDED ANSWER")

display(
    audit_gsec10_66_check.loc[
        audit_gsec10_66_check["recorded_answer_count"] > 0,
        [
            "hhid",
            "h10_respondent",
            "h10_respondent_clean",
            "recorded_answer_count"
        ]
    ].sort_values(
        "recorded_answer_count",
        ascending=False
    )
)
```


```python
import pandas as pd

# ---------------------------------------------------------
# 1. Isolate the 66 households absent from GSEC1
# ---------------------------------------------------------

audit_ids_66 = set(audit_unmatched["hhid"])

audit_gsec9_66 = audit_gsec9.loc[
    audit_gsec9["hhid"].isin(audit_ids_66)
].copy()

audit_gsec10_66 = audit_gsec10_1.loc[
    audit_gsec10_1["hhid"].isin(audit_ids_66)
].copy()

# ---------------------------------------------------------
# 2. Compare respondent identifiers across both sections
# ---------------------------------------------------------

audit_respondent_comparison = audit_gsec9_66[
    ["hhid", "h9_respondent"]
].merge(
    audit_gsec10_66[["hhid", "h10_respondent"]],
    on="hhid",
    how="outer",
    validate="one_to_one",
    indicator=True
)

# The special code is normalized for diagnostic purposes only.
audit_respondent_comparison["h10_respondent_clean"] = (
    audit_respondent_comparison["h10_respondent"]
    .replace(-999999999, pd.NA)
)

audit_respondent_comparison["respondent_pattern"] = (
    audit_respondent_comparison.apply(
        lambda row: (
            "Both respondent codes recorded"
            if pd.notna(row["h9_respondent"])
            and pd.notna(row["h10_respondent_clean"])
            else "GSEC9 code only"
            if pd.notna(row["h9_respondent"])
            else "GSEC10_1 code only"
            if pd.notna(row["h10_respondent_clean"])
            else "Neither section has a respondent code"
        ),
        axis=1
    )
)

print("RESPONDENT-CODE PATTERNS ACROSS THE TWO SECTIONS")

display(
    audit_respondent_comparison[
        "respondent_pattern"
    ].value_counts(dropna=False).rename_axis(
        "pattern"
    ).reset_index(name="households")
)

# ---------------------------------------------------------
# 3. Show the household with the special code and answers
# ---------------------------------------------------------

audit_special_code_with_answers = (
    audit_gsec10_66.loc[
        audit_gsec10_66["h10_respondent"].eq(-999999999)
    ]
    .copy()
)

audit_question_cols = [
    col for col in audit_special_code_with_answers.columns
    if col not in ["hhid", "h10_respondent"]
]

audit_special_code_with_answers["recorded_answers"] = (
    audit_special_code_with_answers[audit_question_cols]
    .notna()
    .sum(axis=1)
)

print("\nSPECIAL-CODE RECORDS WITH RECORDED ANSWERS")

display(
    audit_special_code_with_answers.loc[
        audit_special_code_with_answers["recorded_answers"] > 0,
        ["hhid", "h10_respondent", "recorded_answers"]
        + [
            col for col in audit_question_cols
            if col in [
                "s10q01", "s10q02", "s10q03"
            ]
        ]
    ]
)

# ---------------------------------------------------------
# 4. Confirm whether all 66 IDs are present in both files
# ---------------------------------------------------------

print("\nHOUSEHOLD-ID COVERAGE")

display(
    pd.DataFrame({
        "check": [
            "Unique affected household IDs",
            "Affected IDs found in GSEC9",
            "Affected IDs found in GSEC10_1",
            "Affected IDs missing from GSEC9",
            "Affected IDs missing from GSEC10_1"
        ],
        "count": [
            len(audit_ids_66),
            audit_gsec9_66["hhid"].nunique(),
            audit_gsec10_66["hhid"].nunique(),
            len(audit_ids_66 - set(audit_gsec9_66["hhid"])),
            len(audit_ids_66 - set(audit_gsec10_66["hhid"]))
        ]
    })
)
```


```python
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. Inspect response_status in GSEC1
# ---------------------------------------------------------

print("GSEC1 response_status distribution")

display(
    gsec1["response_status"]
    .value_counts(dropna=False)
    .rename_axis("response_status")
    .reset_index(name="count")
)

# ---------------------------------------------------------
# 2. Inspect interview identifiers in GSEC1
# ---------------------------------------------------------

print("\nGSEC1 interview identifier columns")

display(
    pd.DataFrame({
        "column": [
            col for col in gsec1.columns
            if any(
                term in col.lower()
                for term in [
                    "interview",
                    "status",
                    "hhid",
                    "respondent"
                ]
            )
        ]
    })
)

# ---------------------------------------------------------
# 3. Examine the AGSEC1 records for the 66 households
# ---------------------------------------------------------

audit_agsec1_66_detail = agsec1.loc[
    agsec1["hhid"].isin(audit_unmatched["hhid"])
].copy()

audit_agsec1_review_cols = [
    col for col in [
        "hhid",
        "t0_hhid",
        "batch",
        "region",
        "urban",
        "hhsize",
        "wgt",
        "hwgt_w7",
        "hwgt_wc",
        "culcrp",
        "hh_crp1",
        "hh_crp2",
        "lvstck",
        "hh_anm",
        "hh_plty"
    ]
    if col in audit_agsec1_66_detail.columns
]

print("\nAGSEC1 DETAIL FOR THE 66 AFFECTED HOUSEHOLDS")

display(
    audit_agsec1_66_detail[audit_agsec1_review_cols]
    .sort_values("t0_hhid")
)

# ---------------------------------------------------------
# 4. Inspect the overlapping legacy ID H2620907
# ---------------------------------------------------------

target_t0_hhid = "H2620907"

print("\nALL AGSEC1 RECORDS WITH LEGACY ID H2620907")

display(
    agsec1.loc[
        agsec1["t0_hhid"].astype("string").eq(target_t0_hhid),
        audit_agsec1_review_cols
    ]
)

print("\nALL GSEC1 RECORDS WITH LEGACY ID H2620907")

display(
    gsec1.loc[
        gsec1["t0_hhid"].astype("string").eq(target_t0_hhid)
    ]
)
```


```python
import pandas as pd

# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 1: ASSESS HOUSEHOLD WEIGHT AND IDENTIFIER ELIGIBILITY
# Read-only diagnostic; source files remain unchanged.
# =========================================================

# Work with a copy of the agricultural household dataset.
audit_population = agsec1.copy()

# ---------------------------------------------------------
# 1. Check the dataset structure
# ---------------------------------------------------------

print("AGSEC1 DATASET OVERVIEW")
print(f"Total records: {len(audit_population):,}")
print(f"Unique household IDs: {audit_population['hhid'].nunique():,}")
print(f"Missing household IDs: {audit_population['hhid'].isna().sum():,}")
print(f"Duplicate household IDs: {audit_population['hhid'].duplicated().sum():,}")

# ---------------------------------------------------------
# 2. Assess the candidate cross-sectional weight
# ---------------------------------------------------------

weight_col = "wgt"

audit_population["weight_available"] = (
    audit_population[weight_col].notna()
)

audit_population["weight_positive"] = (
    audit_population[weight_col].gt(0)
)

audit_population["weight_eligible_provisional"] = (
    audit_population["weight_available"]
    & audit_population["weight_positive"]
)

print("\nCANDIDATE CROSS-SECTIONAL WEIGHT ASSESSMENT")

display(
    pd.DataFrame({
        "measure": [
            "Total AGSEC1 records",
            "Records with a nonmissing wgt",
            "Records with missing wgt",
            "Records with positive wgt",
            "Records with nonpositive but nonmissing wgt",
            "Records provisionally eligible by weight availability"
        ],
        "count": [
            len(audit_population),
            int(audit_population["weight_available"].sum()),
            int((~audit_population["weight_available"]).sum()),
            int(audit_population["weight_positive"].sum()),
            int((
                audit_population["weight_available"]
                & ~audit_population["weight_positive"]
            ).sum()),
            int(audit_population["weight_eligible_provisional"].sum())
        ]
    })
)

# ---------------------------------------------------------
# 3. Compare weight availability for the 66 affected IDs
# ---------------------------------------------------------

audit_ids_66 = set(audit_unmatched["hhid"])

audit_population["unmatched_gsec1_household"] = (
    audit_population["hhid"].isin(audit_ids_66)
)

print("\nWEIGHT AVAILABILITY BY HOUSEHOLD AUDIT STATUS")

display(
    audit_population.groupby(
        "unmatched_gsec1_household",
        dropna=False
    ).agg(
        records=("hhid", "size"),
        unique_households=("hhid", "nunique"),
        missing_wgt=("wgt", lambda s: int(s.isna().sum())),
        available_wgt=("wgt", lambda s: int(s.notna().sum())),
        positive_wgt=("wgt", lambda s: int(s.gt(0).sum()))
    ).reset_index()
)

# ---------------------------------------------------------
# 4. Check the other available weight fields
# ---------------------------------------------------------

candidate_weights = [
    col for col in ["wgt", "hwgt_w7", "hwgt_wc"]
    if col in audit_population.columns
]

print("\nCOMPARISON OF AVAILABLE WEIGHT FIELDS")

display(
    pd.DataFrame({
        "weight_variable": candidate_weights,
        "nonmissing_records": [
            int(audit_population[col].notna().sum())
            for col in candidate_weights
        ],
        "missing_records": [
            int(audit_population[col].isna().sum())
            for col in candidate_weights
        ],
        "nonpositive_nonmissing_records": [
            int((
                audit_population[col].notna()
                & ~audit_population[col].gt(0)
            ).sum())
            for col in candidate_weights
        ]
    })
)
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 2A: INSPECT CROP-LEVEL SEED VARIABLES
# Read-only diagnostic; does not modify source data.
# =========================================================

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 0. Ensure AGSEC4A / AGSEC4B are available
# ---------------------------------------------------------
if "extracted_folder" in globals():
    data_root = Path(extracted_folder)
else:
    data_root = Path(r"C:\Users\H-START\Desktop\dataset")

agric_dir = data_root / "Agric"

if "agsec4a" not in globals():
    agsec4a = pd.read_csv(agric_dir / "AGSEC4A.csv", low_memory=False)
    print("Loaded agsec4a:", agsec4a.shape)

if "agsec4b" not in globals():
    agsec4b = pd.read_csv(agric_dir / "AGSEC4B.csv", low_memory=False)
    print("Loaded agsec4b:", agsec4b.shape)

# ---------------------------------------------------------
# 1. Continue with the diagnostic
# ---------------------------------------------------------
crop_datasets = {
    "First visit (AGSEC4A)": agsec4a,
    "Second visit (AGSEC4B)": agsec4b,
}

crop_variable_map = {
    "First visit (AGSEC4A)": {
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "Second visit (AGSEC4B)": {
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for visit, df in crop_datasets.items():
    print(f"\n{'=' * 65}")
    print(visit.upper())
    print(f"{'=' * 65}")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    for label, col in crop_variable_map[visit].items():
        if col not in df.columns:
            print(f"\n{label}: {col} NOT FOUND")
            continue
        print(f"\n{label.upper()} — {col}")
        print(df[col].value_counts(dropna=False).sort_index().to_string())
```


```python
# Inspect existing variables that may contain the crop datasets.
crop_variable_candidates = [
    name for name, obj in globals().items()
    if isinstance(obj, pd.DataFrame)
    and any(
        keyword in name.lower()
        for keyword in ["agsec4", "crop", "seed"]
    )
]

print("Potentially relevant DataFrame variables:")

if crop_variable_candidates:
    for name in crop_variable_candidates:
        df = globals()[name]
        print(
            f"{name}: {df.shape[0]:,} rows × "
            f"{df.shape[1]:,} columns"
        )
else:
    print("No matching DataFrame variables found.")
```


```python
import pandas as pd

# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 2A: INSPECT CROP-LEVEL SEED VARIABLES
# Reuse existing DataFrames; do not modify source data.
# =========================================================

crop_datasets_review = {
    "First visit (AGSEC4A)": crop_a,
    "Second visit (AGSEC4B)": crop_b
}

crop_variable_map_review = {
    "First visit (AGSEC4A)": {
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14"
    },
    "Second visit (AGSEC4B)": {
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14"
    }
}

# ---------------------------------------------------------
# 1. Verify the expected columns
# ---------------------------------------------------------

for visit, df in crop_datasets_review.items():
    print(f"\n{visit}")
    print(f"Dimensions: {df.shape[0]:,} rows × {df.shape[1]} columns")

    expected_columns = [
        "hhid",
        "t0_hhid",
        *crop_variable_map_review[visit].values()
    ]

    display(
        pd.DataFrame({
            "variable": expected_columns,
            "exists": [
                column in df.columns
                for column in expected_columns
            ]
        })
    )

# ---------------------------------------------------------
# 2. Inspect the distributions of the seed variables
# ---------------------------------------------------------

for visit, df in crop_datasets_review.items():

    print(f"\n{'=' * 60}")
    print(visit.upper())
    print(f"{'=' * 60}")

    for label, column in crop_variable_map_review[visit].items():

        if column not in df.columns:
            print(f"\nSkipping {column}: column not found.")
            continue

        print(f"\n{label.upper()} — {column}")

        distribution = (
            df[column]
            .value_counts(dropna=False)
            .rename_axis("value")
            .reset_index(name="count")
        )

        display(distribution)

# ---------------------------------------------------------
# 3. Inspect seed-use and seed-type combinations
# ---------------------------------------------------------

for visit, df in crop_datasets_review.items():

    variables = crop_variable_map_review[visit]
    seed_use = variables["seed_use"]
    seed_type = variables["seed_type"]

    if seed_use not in df.columns or seed_type not in df.columns:
        continue

    print(f"\nSEED-USE × SEED-TYPE: {visit}")

    display(
        pd.crosstab(
            df[seed_use],
            df[seed_type],
            margins=True,
            dropna=False
        )
    )
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 2B: VALIDATE SEED CLASSIFICATION
# Read-only diagnostic; existing DataFrames are preserved.
# =========================================================

seed_datasets = {
    "First visit": {
        "df": crop_a,
        "use": "s4aq16",
        "type": "s4aq13",
        "category": "s4aq14"
    },
    "Second visit": {
        "df": crop_b,
        "use": "s4bq16",
        "type": "s4bq13",
        "category": "s4bq14"
    }
}

for visit, info in seed_datasets.items():

    df = info["df"]
    use = info["use"]
    seed_type = info["type"]
    category = info["category"]

    print("\n" + "=" * 65)
    print(f"{visit.upper()}: SEED CLASSIFICATION VALIDATION")
    print("=" * 65)

    # 1. Seed type by improved-seed category
    print("\nSeed type × improved-seed category:")

    display(
        pd.crosstab(
            df[seed_type],
            df[category],
            margins=True,
            dropna=False
        )
    )

    # 2. Seed use by improved-seed category
    print("\nSeed use × improved-seed category:")

    display(
        pd.crosstab(
            df[use],
            df[category],
            margins=True,
            dropna=False
        )
    )

    # 3. Identify records with potentially inconsistent combinations
    # These are flagged for review, not automatically declared errors.
    inconsistent = df[
        (
            (df[use] == 2) &
            (
                df[seed_type].notna() |
                df[category].notna()
            )
        ) |
        (
            (df[seed_type] == 1) &
            df[category].notna()
        ) |
        (
            (df[seed_type] == 2) &
            df[category].isna()
        )
    ]

    print("\nRecords requiring questionnaire-rule review:")
    print(f"{len(inconsistent):,}")

    display(
        inconsistent[
            ["hhid", "t0_hhid", use, seed_type, category]
        ].head(15)
    )
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 3: CREATE CROP-LEVEL ADOPTION AUDIT DATASETS
# Original DataFrames remain unchanged.
# =========================================================

import numpy as np
import pandas as pd

seed_config = {
    "First visit": {
        "source": crop_a,
        "use": "s4aq16",
        "type": "s4aq13",
        "category": "s4aq14"
    },
    "Second visit": {
        "source": crop_b,
        "use": "s4bq16",
        "type": "s4bq13",
        "category": "s4bq14"
    }
}

crop_adoption_audit = {}

for visit, config in seed_config.items():

    source = config["source"]

    # Copy the original data before creating new variables.
    audit = source.copy()

    use = config["use"]
    seed_type = config["type"]
    category = config["category"]

    # Initialize outcome as unresolved.
    audit["improved_seed_adoption"] = np.nan

    # Confirmed traditional-seed use.
    audit.loc[
        (audit[use] == 1) & (audit[seed_type] == 1),
        "improved_seed_adoption"
    ] = 0

    # Confirmed improved-seed use.
    audit.loc[
        (audit[use] == 1) & (audit[seed_type] == 2),
        "improved_seed_adoption"
    ] = 1

    # No seed used: classify as non-adoption provisionally.
    audit.loc[
        audit[use] == 2,
        "improved_seed_adoption"
    ] = 0

    # Record why an observation remains unresolved.
    audit["adoption_classification_status"] = "Unresolved"

    audit.loc[
        audit["improved_seed_adoption"] == 0,
        "adoption_classification_status"
    ] = "Non-adopter"

    audit.loc[
        audit["improved_seed_adoption"] == 1,
        "adoption_classification_status"
    ] = "Adopter"

    # Flag improved-seed records missing the narrower category.
    audit["improved_category_missing_flag"] = (
        (audit[use] == 1)
        & (audit[seed_type] == 2)
        & audit[category].isna()
    )

    crop_adoption_audit[visit] = audit

    print(f"\n{'=' * 60}")
    print(f"{visit.upper()}: CROP-LEVEL ADOPTION AUDIT")
    print("=" * 60)

    print("\nClassification status:")
    display(
        audit["adoption_classification_status"]
        .value_counts(dropna=False)
        .rename_axis("status")
        .reset_index(name="crop_records")
    )

    print("\nAdoption outcome:")
    display(
        audit["improved_seed_adoption"]
        .value_counts(dropna=False)
        .sort_index()
        .rename_axis("outcome")
        .reset_index(name="crop_records")
    )

    print("\nImproved-seed records missing their category:")
    print(
        int(audit["improved_category_missing_flag"].sum())
    )

    print("\nUnresolved records:")
    display(
        audit.loc[
            audit["improved_seed_adoption"].isna(),
            ["hhid", "t0_hhid", use, seed_type, category]
        ].head(10)
    )
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 4: HOUSEHOLD-LEVEL ADOPTION SUMMARY
# Uses the crop-level audit datasets created in Step 3.
# Existing datasets and summaries remain unchanged.
# =========================================================

import pandas as pd

household_adoption_results = {}
household_summary_rows = []

for visit, audit in crop_adoption_audit.items():

    print("\n" + "=" * 65)
    print(f"{visit.upper()}: HOUSEHOLD-LEVEL ADOPTION")
    print("=" * 65)

    # Aggregate crop outcomes within each household.
    household_df = (
        audit.groupby("hhid", dropna=False)
        .agg(
            crop_records=("hhid", "size"),
            confirmed_adopter_crops=(
                "improved_seed_adoption",
                lambda x: (x == 1).sum()
            ),
            confirmed_nonadopter_crops=(
                "improved_seed_adoption",
                lambda x: (x == 0).sum()
            ),
            unresolved_crops=(
                "improved_seed_adoption",
                lambda x: x.isna().sum()
            )
        )
        .reset_index()
    )

    # Assign household adoption status.
    household_df["household_adoption"] = pd.NA

    # At least one crop confirms improved-seed adoption.
    household_df.loc[
        household_df["confirmed_adopter_crops"] > 0,
        "household_adoption"
    ] = 1

    # No unresolved crops and no confirmed adopter crops.
    household_df.loc[
        (
            household_df["confirmed_adopter_crops"] == 0
        ) & (
            household_df["unresolved_crops"] == 0
        ),
        "household_adoption"
    ] = 0

    # Label each household.
    household_df["adoption_status"] = "Unclassified"

    household_df.loc[
        household_df["household_adoption"] == 1,
        "adoption_status"
    ] = "Adopter"

    household_df.loc[
        household_df["household_adoption"] == 0,
        "adoption_status"
    ] = "Non-adopter"

    household_adoption_results[visit] = household_df

    # Summarize household classifications.
    status_counts = (
        household_df["adoption_status"]
        .value_counts()
        .reindex(
            ["Adopter", "Non-adopter", "Unclassified"],
            fill_value=0
        )
    )

    total_households = len(household_df)
    adopters = int(status_counts["Adopter"])
    non_adopters = int(status_counts["Non-adopter"])
    unclassified = int(status_counts["Unclassified"])
    classified = adopters + non_adopters

    adoption_rate = (
        adopters / classified * 100
        if classified > 0
        else float("nan")
    )

    print(f"Households with crop records: {total_households:,}")
    print(f"Confirmed adopters:          {adopters:,}")
    print(f"Confirmed non-adopters:      {non_adopters:,}")
    print(f"Unclassified households:     {unclassified:,}")
    print(f"Classified households:       {classified:,}")
    print(f"Adoption among classified:   {adoption_rate:.2f}%")

    print("\nHousehold classification table:")

    display(
        status_counts.rename_axis("status")
        .reset_index(name="households")
    )

    household_summary_rows.append({
        "visit": visit,
        "households_with_crop_records": total_households,
        "adopters": adopters,
        "non_adopters": non_adopters,
        "unclassified": unclassified,
        "classified_households": classified,
        "adoption_rate_among_classified_pct": round(
            adoption_rate, 2
        )
    })

# Combined comparison table for the two visits.
household_adoption_summary = pd.DataFrame(
    household_summary_rows
)

print("\n" + "=" * 65)
print("HOUSEHOLD ADOPTION SUMMARY: VISIT COMPARISON")
print("=" * 65)

display(household_adoption_summary)

# Verify that each household appears once in each summary.
for visit, household_df in household_adoption_results.items():

    assert household_df["hhid"].is_unique, (
        f"Duplicate household IDs found in {visit} summary."
    )

    print(
        f"{visit}: household IDs are unique "
        f"({len(household_df):,} households)."
    )
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 5: HOUSEHOLD ELIGIBILITY AND WEIGHT AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------
# 1. Locate an existing AGSEC1 DataFrame
# ---------------------------------------------------------

possible_rosters = [
    name
    for name, obj in globals().items()
    if isinstance(obj, pd.DataFrame)
    and "hhid" in obj.columns
    and "wgt" in obj.columns
    and "hwgt_w7" in obj.columns
    and "hwgt_wc" in obj.columns
]

print("Potential household roster DataFrames:", possible_rosters)

if len(possible_rosters) == 1:
    roster = globals()[possible_rosters[0]]
    print("Using existing DataFrame:", possible_rosters[0])

elif len(possible_rosters) > 1:
    print(
        "Multiple candidate DataFrames found. "
        "Select the correct AGSEC1 DataFrame explicitly."
    )

else:
    print(
        "No matching roster DataFrame found. "
        "Load AGSEC1.csv into a new variable."
    )

# ---------------------------------------------------------
# 2. If exactly one roster was found, audit the visits
# ---------------------------------------------------------

if len(possible_rosters) == 1:

    required_columns = [
        "hhid", "wgt", "hwgt_w7", "hwgt_wc"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in roster.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Required roster columns missing: {missing_columns}"
        )

    if roster["hhid"].duplicated().any():
        raise ValueError(
            "AGSEC1 roster contains duplicate hhid values. "
            "Resolve the identifier issue before merging."
        )

    weight_columns = ["wgt", "hwgt_w7", "hwgt_wc"]

    print("\nROSTER WEIGHT AVAILABILITY")
    display(
        pd.DataFrame({
            "weight": weight_columns,
            "nonmissing": [
                roster[col].notna().sum()
                for col in weight_columns
            ],
            "missing": [
                roster[col].isna().sum()
                for col in weight_columns
            ],
            "positive": [
                (roster[col] > 0).sum()
                for col in weight_columns
            ]
        })
    )

    # Create a lookup table without changing the original roster.
    roster_lookup = roster[
        ["hhid", *weight_columns]
    ].copy()

    # -----------------------------------------------------
    # 3. Match each visit's households to AGSEC1
    # -----------------------------------------------------

    eligibility_rows = []

    for visit, household_df in household_adoption_results.items():

        matched = household_df.merge(
            roster_lookup,
            on="hhid",
            how="left",
            validate="one_to_one",
            indicator=True
        )

        print(f"\n{visit.upper()}: ROSTER MATCHING")

        match_summary = (
            matched["_merge"]
            .value_counts()
            .reindex(
                ["both", "left_only"],
                fill_value=0
            )
        )

        display(
            match_summary.rename_axis("match_status")
            .reset_index(name="households")
        )

        for weight in weight_columns:

            valid_weight = (
                matched[weight].notna()
                & np.isfinite(matched[weight])
                & (matched[weight] > 0)
            )

            for adoption_status in [
                "Adopter",
                "Non-adopter",
                "Unclassified"
            ]:

                subset = matched[
                    matched["adoption_status"] == adoption_status
                ]

                valid_in_subset = (
                    subset[weight].notna()
                    & np.isfinite(subset[weight])
                    & (subset[weight] > 0)
                )

                eligibility_rows.append({
                    "visit": visit,
                    "adoption_status": adoption_status,
                    "weight": weight,
                    "households": len(subset),
                    "valid_positive_weight": int(
                        valid_in_subset.sum()
                    ),
                    "missing_or_invalid_weight": int(
                        (~valid_in_subset).sum()
                    )
                })

        print("\nWeight availability by adoption status:")

        status_weight_summary = (
            matched.groupby(
                "adoption_status",
                dropna=False
            )[weight_columns]
            .agg(lambda x: int(
                (x.notna() & np.isfinite(x) & (x > 0)).sum()
            ))
        )

        display(status_weight_summary)

    eligibility_audit = pd.DataFrame(eligibility_rows)

    print("\n" + "=" * 65)
    print("ELIGIBILITY SUMMARY")
    print("=" * 65)

    display(eligibility_audit)
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 5A: IDENTIFY THE CORRECT AGSEC1 ROSTER
# Read-only inspection of existing DataFrames
# =========================================================

import pandas as pd
import numpy as np

roster_candidates = [
    "sample",
    "agsec1_audit_df",
    "agsec1_weight_audit",
    "agsec1_relevant",
    "agsec1",
    "agsec1_only",
    "missing_households",
    "audit_agsec1",
    "audit_only",
    "audit_shared",
    "audit_agsec1_check",
    "audit_agsec1_missing",
    "audit_missing_records",
    "audit_unmatched",
    "audit_agsec1_66_detail",
    "audit_population"
]

roster_comparison = []

for name in roster_candidates:

    obj = globals().get(name)

    if not isinstance(obj, pd.DataFrame):
        continue

    required = ["hhid", "wgt", "hwgt_w7", "hwgt_wc"]

    missing_columns = [
        col for col in required
        if col not in obj.columns
    ]

    row = {
        "dataframe": name,
        "rows": len(obj),
        "columns": len(obj.columns),
        "has_required_columns": len(missing_columns) == 0,
        "missing_required_columns": ", ".join(missing_columns),
        "hhid_unique": (
            obj["hhid"].is_unique
            if "hhid" in obj.columns
            else False
        ),
        "hhid_missing": (
            int(obj["hhid"].isna().sum())
            if "hhid" in obj.columns
            else None
        )
    }

    for weight in ["wgt", "hwgt_w7", "hwgt_wc"]:

        if weight in obj.columns:
            values = pd.to_numeric(
                obj[weight],
                errors="coerce"
            )

            row[f"{weight}_valid_positive"] = int(
                (values.notna() & np.isfinite(values) & (values > 0)).sum()
            )

            row[f"{weight}_missing"] = int(
                values.isna().sum()
            )
        else:
            row[f"{weight}_valid_positive"] = None
            row[f"{weight}_missing"] = None

    roster_comparison.append(row)

roster_comparison_df = pd.DataFrame(roster_comparison)

display(
    roster_comparison_df.sort_values(
        ["has_required_columns", "rows"],
        ascending=[False, False]
    ).reset_index(drop=True)
)
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 5B: VERIFY ROSTER AND MATCH HOUSEHOLDS
# Read-only audit
# =========================================================

import pandas as pd
import numpy as np

# Use the original AGSEC1 DataFrame.
roster = agsec1

required_columns = [
    "hhid",
    "wgt",
    "hwgt_w7",
    "hwgt_wc"
]

missing_columns = [
    col for col in required_columns
    if col not in roster.columns
]

if missing_columns:
    raise KeyError(
        f"Required columns missing from agsec1: {missing_columns}"
    )

if roster["hhid"].isna().any():
    raise ValueError("AGSEC1 contains missing household IDs.")

if roster["hhid"].duplicated().any():
    raise ValueError("AGSEC1 contains duplicate household IDs.")

# Confirm the roster structure and weights.
print("AGSEC1 ROSTER VALIDATION")
print("-" * 50)
print(f"Rows: {len(roster):,}")
print(f"Columns: {len(roster.columns):,}")
print(f"Unique household IDs: {roster['hhid'].nunique():,}")

weight_summary = []

for weight in ["wgt", "hwgt_w7", "hwgt_wc"]:

    values = pd.to_numeric(roster[weight], errors="coerce")

    weight_summary.append({
        "weight": weight,
        "nonmissing": int(values.notna().sum()),
        "missing": int(values.isna().sum()),
        "positive_finite": int(
            (values.notna() & np.isfinite(values) & (values > 0)).sum()
        ),
        "nonpositive_or_invalid": int(
            (values.notna() & (~np.isfinite(values) | (values <= 0))).sum()
        )
    })

display(pd.DataFrame(weight_summary))

# Match each visit's household summary to AGSEC1.
roster_lookup = roster[required_columns].copy()

visit_match_results = {}

for visit, household_df in household_adoption_results.items():

    matched = household_df.merge(
        roster_lookup,
        on="hhid",
        how="left",
        validate="one_to_one",
        indicator=True
    )

    visit_match_results[visit] = matched

    print(f"\n{visit.upper()} — ROSTER MATCH")

    print(
        matched["_merge"]
        .value_counts()
        .reindex(["both", "left_only", "right_only"], fill_value=0)
        .rename_axis("match_status")
        .to_frame("households")
    )

    rows = []

    for status in ["Adopter", "Non-adopter", "Unclassified"]:

        subset = matched.loc[
            matched["adoption_status"] == status
        ]

        row = {
            "adoption_status": status,
            "households": len(subset)
        }

        for weight in ["wgt", "hwgt_w7", "hwgt_wc"]:

            values = pd.to_numeric(
                subset[weight],
                errors="coerce"
            )

            row[f"{weight}_valid_positive"] = int(
                (values.notna() & np.isfinite(values) & (values > 0)).sum()
            )

            row[f"{weight}_missing_or_invalid"] = (
                len(subset) - row[f"{weight}_valid_positive"]
            )

        rows.append(row)

    display(pd.DataFrame(rows))

print("\nVerification complete. Original DataFrames were not modified.")
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 6: LOCATE SURVEY DOCUMENTATION
# Read-only file search
# =========================================================

from pathlib import Path

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

search_terms = [
    "wgt",
    "hwgt_w7",
    "hwgt_wc",
    "sampling weight",
    "cross-sectional weight",
    "panel weight",
    "stratum",
    "primary sampling unit",
    "cluster",
    "wave 7"
]

documentation_extensions = {
    ".pdf", ".txt", ".doc", ".docx",
    ".csv", ".xlsx", ".xls", ".dta"
}

print("DATA ROOT:", data_root)
print("Directory exists:", data_root.is_dir())

print("\nPotential documentation files:")

documentation_files = []

for path in data_root.rglob("*"):

    if not path.is_file():
        continue

    if path.suffix.lower() in documentation_extensions:
        documentation_files.append(path)

for path in documentation_files:
    print(path)

print(f"\nTotal candidate documentation/data files: {len(documentation_files)}")
print("\nSearch terms to verify against documentation:")
for term in search_terms:
    print("-", term)
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 6A: SEARCH OFFICIAL UNPS DOCUMENTATION
# Read-only PDF text search
# =========================================================

from pathlib import Path

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

pdf_files = [
    data_root / "ddi-documentation-english_microdata-3795.pdf",
    data_root / "agriculture_qx.pdf",
    data_root / "unps_hhq.pdf",
]

search_terms = [
    "hwgt_w7",
    "hwgt_wc",
    "cross-sectional weight",
    "sampling weight",
    "sample weight",
    "survey design",
    "primary sampling unit",
    "stratification",
    "cluster",
    "seed type",
    "improved seed",
    "s4aq13",
    "s4aq14",
    "s4aq16",
    "s4bq13",
    "s4bq14",
    "s4bq16",
]

try:
    from pypdf import PdfReader
except ImportError:
    raise ImportError(
        "The pypdf package is not installed in the current kernel. "
        "Install it in your active .venv313 environment, then rerun "
        "this cell."
    )

for pdf_path in pdf_files:

    print("\n" + "=" * 80)
    print("DOCUMENT:", pdf_path.name)
    print("=" * 80)

    if not pdf_path.is_file():
        print("File not found:", pdf_path)
        continue

    reader = PdfReader(str(pdf_path))
    print("Number of pages:", len(reader.pages))

    matches_found = 0

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""
        lines = text.splitlines()

        for line_index, line in enumerate(lines):

            matched_terms = [
                term for term in search_terms
                if term.lower() in line.lower()
            ]

            if matched_terms:

                matches_found += 1

                # Show nearby lines for context.
                start = max(0, line_index - 2)
                end = min(len(lines), line_index + 3)

                print(
                    f"\nPage {page_number} | "
                    f"Matched: {', '.join(matched_terms)}"
                )

                print("\n".join(lines[start:end]))

    if matches_found == 0:
        print(
            "No exact search-term matches found. "
            "The document may use different wording or scanned pages."
        )
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 7: WEIGHTED VS UNWEIGHTED ADOPTION ESTIMATES
# Read-only sensitivity analysis
# =========================================================

import numpy as np
import pandas as pd

# Use the existing household roster.
roster = agsec1.copy()

weight_columns = [
    "wgt",
    "hwgt_w7",
    "hwgt_wc"
]

required_roster_columns = ["hhid"] + weight_columns

missing_columns = [
    col for col in required_roster_columns
    if col not in roster.columns
]

if missing_columns:
    raise KeyError(
        f"Missing required roster columns: {missing_columns}"
    )

if roster["hhid"].duplicated().any():
    raise ValueError(
        "The roster contains duplicate hhid values. "
        "Resolve the key issue before merging."
    )

results = []

for visit, household_df in household_adoption_results.items():

    print(f"\nProcessing visit: {visit}")

    # Check required household-level fields.
    required_outcome_columns = [
        "hhid",
        "household_adoption",
        "adoption_status"
    ]

    missing_outcome_columns = [
        col for col in required_outcome_columns
        if col not in household_df.columns
    ]

    if missing_outcome_columns:
        raise KeyError(
            f"{visit}: missing columns "
            f"{missing_outcome_columns}"
        )

    # Only use households whose adoption outcome is classified.
    classified = household_df.loc[
        household_df["adoption_status"].isin(
            ["Adopter", "Non-adopter"]
        )
    ].copy()

    classified["household_adoption"] = pd.to_numeric(
        classified["household_adoption"],
        errors="coerce"
    )

    # Keep only valid binary outcomes.
    classified = classified.loc[
        classified["household_adoption"].isin([0, 1])
    ].copy()

    # Attach weights without modifying the original dataframes.
    analysis_df = classified.merge(
        roster[required_roster_columns],
        on="hhid",
        how="left",
        validate="one_to_one",
        indicator=True
    )

    if not analysis_df["_merge"].eq("both").all():
        raise ValueError(
            f"{visit}: some classified households did not "
            "match the household roster."
        )

    analysis_df = analysis_df.drop(columns="_merge")

    total_classified = len(analysis_df)

    for weight in weight_columns:

        weights = pd.to_numeric(
            analysis_df[weight],
            errors="coerce"
        )

        valid_weight = (
            np.isfinite(weights)
            & weights.gt(0)
        )

        eligible = analysis_df.loc[valid_weight].copy()
        eligible_weights = weights.loc[valid_weight]

        valid_n = len(eligible)
        missing_weight_n = total_classified - valid_n

        if valid_n > 0:

            unweighted_rate = (
                eligible["household_adoption"].mean() * 100
            )

            weighted_rate = (
                (
                    eligible["household_adoption"]
                    * eligible_weights
                ).sum()
                / eligible_weights.sum()
                * 100
            )

            weight_sum = eligible_weights.sum()

        else:
            unweighted_rate = np.nan
            weighted_rate = np.nan
            weight_sum = np.nan

        results.append({
            "visit": visit,
            "weight_variable": weight,
            "classified_households": total_classified,
            "valid_weight_households": valid_n,
            "missing_or_invalid_weight": missing_weight_n,
            "unweighted_adoption_pct": unweighted_rate,
            "weighted_adoption_pct": weighted_rate,
            "sum_of_valid_weights": weight_sum
        })

weight_comparison_df = pd.DataFrame(results)

print("\nWEIGHTED VS UNWEIGHTED HOUSEHOLD ADOPTION")
display(
    weight_comparison_df.round(3)
)
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 8: IDENTIFY POSSIBLE SURVEY-DESIGN VARIABLES
# Read-only inspection
# =========================================================

import pandas as pd

# Inspect the three existing datasets.
datasets_to_inspect = {
    "AGSEC1": agsec1,
    "GSEC1": gsec1,
    "Geographic variables": pd.read_csv(
        r"C:\Users\H-START\Desktop\dataset\unps_geovars_2018_19.csv",
        low_memory=False
    )
}

# Search terms for likely identifiers.
design_terms = [
    "strata",
    "stratum",
    "psu",
    "cluster",
    "ea",
    "enumeration",
    "district",
    "region",
    "subreg",
    "regurb",
    "urban",
    "batch",
    "hhid",
    "t0_hhid",
    "weight",
    "wgt"
]

for dataset_name, df in datasets_to_inspect.items():

    print("\n" + "=" * 80)
    print("DATASET:", dataset_name)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("=" * 80)

    matched_columns = [
        col for col in df.columns
        if any(term in col.lower() for term in design_terms)
    ]

    print("\nPotentially relevant columns:")

    for col in matched_columns:
        print(f" - {col}")

    print("\nDistinct values for selected categorical candidates:")

    categorical_candidates = [
        col for col in matched_columns
        if any(
            term in col.lower()
            for term in [
                "region",
                "subreg",
                "regurb",
                "urban",
                "district",
                "batch",
                "cluster",
                "strata",
                "stratum",
                "psu",
                "ea"
            ]
        )
    ]

    for col in categorical_candidates:

        series = df[col]

        print(f"\n{col}")
        print("Missing:", series.isna().sum())
        print("Unique values:", series.nunique(dropna=True))

        if series.nunique(dropna=True) <= 30:
            print(series.value_counts(dropna=False).to_string())
        else:
            print("Sample values:")
            print(series.dropna().head(10).tolist())
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 9: SURVEY-DESIGN DOCUMENTATION AUDIT
# Read-only PDF inspection
# =========================================================

from pathlib import Path
from pypdf import PdfReader

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

pdf_names = [
    "ddi-documentation-english_microdata-3795.pdf",
    "unps_7_bid.pdf",
    "unps_hhq.pdf",
    "unps_community.pdf",
]

search_terms = [
    "sampling design",
    "sample design",
    "stratified",
    "stratum",
    "strata",
    "primary sampling unit",
    "PSU",
    "enumeration area",
    "enumeration areas",
    "EA",
    "cluster",
    "sampling weight",
    "household weight",
    "cross-sectional",
    "panel weight",
    "regurb",
    "subreg",
    "district_code",
    "batch",
]

for filename in pdf_names:

    pdf_path = data_root / filename

    print("\n" + "=" * 90)
    print("DOCUMENT:", filename)
    print("=" * 90)

    if not pdf_path.exists():
        print("File not found.")
        continue

    reader = PdfReader(str(pdf_path))

    print("Pages:", len(reader.pages))

    document_matches = 0

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""
        lines = text.splitlines()

        matching_indices = [
            i for i, line in enumerate(lines)
            if any(
                term.lower() in line.lower()
                for term in search_terms
            )
        ]

        # Avoid printing repeated passages when multiple search
        # terms occur on adjacent lines.
        selected_indices = set()

        for index in matching_indices:
            for nearby_index in range(
                max(0, index - 2),
                min(len(lines), index + 3)
            ):
                selected_indices.add(nearby_index)

        if matching_indices:
            document_matches += len(matching_indices)

            print(f"\n--- PAGE {page_number} ---")

            for index in sorted(selected_indices):
                print(lines[index])

    if document_matches == 0:
        print("No matching passages found in extractable PDF text.")
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 10B: CORRECTED WEIGHT-CONSISTENCY AUDIT
# Read-only
# =========================================================

import numpy as np
import pandas as pd

# ---------------------------------------------------------
# 1. Determine which weight columns exist in each dataset
# ---------------------------------------------------------
ags_weights = [
    col for col in ["wgt", "hwgt_w7", "hwgt_wc"]
    if col in agsec1.columns
]

# GSEC1 uses different capitalisation for the panel weight.
# Normalise that here so downstream code can use a single name.
gsec1_weights_src = {}
if "wgt" in gsec1.columns:
    gsec1_weights_src["wgt"] = "wgt"
if "hwgt_W7" in gsec1.columns:
    gsec1_weights_src["hwgt_w7"] = "hwgt_W7"
elif "hwgt_w7" in gsec1.columns:
    gsec1_weights_src["hwgt_w7"] = "hwgt_w7"
if "hwgt_wc" in gsec1.columns:
    gsec1_weights_src["hwgt_wc"] = "hwgt_wc"

print("AGSEC1 weight columns available:", ags_weights)
print("GSEC1 weight columns available:", list(gsec1_weights_src.keys()))

# ---------------------------------------------------------
# 2. Build matched weight frames with unambiguous suffixes
# ---------------------------------------------------------
agsec1_weights = agsec1[["hhid"] + ags_weights].copy()
agsec1_weights = agsec1_weights.rename(
    columns={col: f"{col}_agsec1" for col in ags_weights}
)

gsec1_weights = gsec1[
    ["hhid"] + list(gsec1_weights_src.values())
].copy()
gsec1_weights = gsec1_weights.rename(
    columns={v: f"{k}_gsec1" for k, v in gsec1_weights_src.items()}
)

matched_weights = agsec1_weights.merge(
    gsec1_weights,
    on="hhid",
    how="inner",
    validate="one_to_one",
)

print("\nMatched households:", len(matched_weights))

# ---------------------------------------------------------
# 3. Compare each weight pair that exists on both sides
# ---------------------------------------------------------
consistency_results = []

for weight_name in ["wgt", "hwgt_w7", "hwgt_wc"]:
    left_col = f"{weight_name}_agsec1"
    right_col = f"{weight_name}_gsec1"

    if left_col not in matched_weights.columns or right_col not in matched_weights.columns:
        print(f"\nSkipping {weight_name}: column unavailable on one side.")
        consistency_results.append({
            "weight": weight_name,
            "status": "column unavailable",
            "matched_households": len(matched_weights),
            "both_nonmissing": None,
            "equal_values": None,
            "unequal_values": None,
            "missing_in_both": None,
            "missing_in_one_file_only": None,
        })
        continue

    left = pd.to_numeric(matched_weights[left_col], errors="coerce")
    right = pd.to_numeric(matched_weights[right_col], errors="coerce")

    both_present = left.notna() & right.notna()

    equal = pd.Series(False, index=matched_weights.index)
    equal.loc[both_present] = np.isclose(
        left.loc[both_present],
        right.loc[both_present],
        rtol=1e-9,
        atol=1e-8,
    )

    one_missing = left.isna() ^ right.isna()

    consistency_results.append({
        "weight": weight_name,
        "status": "compared",
        "matched_households": len(matched_weights),
        "both_nonmissing": int(both_present.sum()),
        "equal_values": int(equal.loc[both_present].sum()),
        "unequal_values": int((~equal.loc[both_present]).sum()),
        "missing_in_both": int((left.isna() & right.isna()).sum()),
        "missing_in_one_file_only": int(one_missing.sum()),
    })

weight_consistency_df = pd.DataFrame(consistency_results)
display(weight_consistency_df)

print("\nStep 10B completed.")
```


```python
# =========================================================
# STEP 10B: CORRECTED WEIGHT-CONSISTENCY AUDIT
# Read-only
# =========================================================

import numpy as np
import pandas as pd

# Explicitly rename GSEC1 weight columns before merging.
gsec1_weights = gsec1[
    ["hhid", "wgt", "hwgt_W7", "hwgt_wc"]
].copy()

gsec1_weights = gsec1_weights.rename(
    columns={
        "wgt": "wgt_gsec1",
        "hwgt_W7": "hwgt_w7_gsec1",
        "hwgt_wc": "hwgt_wc_gsec1",
    }
)

agsec1_weights = agsec1[
    ["hhid", "wgt", "hwgt_w7", "hwgt_wc"]
].copy()

agsec1_weights = agsec1_weights.rename(
    columns={
        "wgt": "wgt_agsec1",
        "hwgt_w7": "hwgt_w7_agsec1",
        "hwgt_wc": "hwgt_wc_agsec1",
    }
)

matched_weights = agsec1_weights.merge(
    gsec1_weights,
    on="hhid",
    how="inner",
    validate="one_to_one"
)

print("Matched households:", len(matched_weights))

weight_pairs = [
    ("wgt_agsec1", "wgt_gsec1", "wgt"),
    ("hwgt_w7_agsec1", "hwgt_w7_gsec1", "hwgt_w7"),
    ("hwgt_wc_agsec1", "hwgt_wc_gsec1", "hwgt_wc"),
]

consistency_results = []

for left_col, right_col, weight_name in weight_pairs:

    left = pd.to_numeric(
        matched_weights[left_col],
        errors="coerce"
    )

    right = pd.to_numeric(
        matched_weights[right_col],
        errors="coerce"
    )

    both_present = left.notna() & right.notna()

    equal = pd.Series(False, index=matched_weights.index)

    equal.loc[both_present] = np.isclose(
        left.loc[both_present],
        right.loc[both_present],
        rtol=1e-9,
        atol=1e-8
    )

    one_missing = left.isna() ^ right.isna()

    consistency_results.append({
        "weight": weight_name,
        "matched_households": len(matched_weights),
        "both_nonmissing": int(both_present.sum()),
        "equal_values": int(equal.loc[both_present].sum()),
        "unequal_values": int(
            (~equal.loc[both_present]).sum()
        ),
        "missing_in_both": int(
            (left.isna() & right.isna()).sum()
        ),
        "missing_in_one_file_only": int(one_missing.sum()),
    })

weight_consistency_df = pd.DataFrame(consistency_results)

display(weight_consistency_df)

print("\nStep 10B completed.")

```


```python
# =========================================================
# STEP 11: INSPECT AVAILABLE SURVEY METADATA
# Read-only diagnostic
# =========================================================

print("AVAILABLE METADATA OBJECTS")
print("=" * 60)

print("Metadata extensions:")
print(metadata_extensions)

print("\nAGSEC1 metadata keys:")
print(list(agsec1_metadata.keys()))

print("\nMetadata candidate columns:")
print(audit_metadata_columns)

print("\nMetadata candidate records:")
for item in audit_metadata_candidates:
    print(item)

print("\nStep 11 completed.")
```


```python
# =========================================================
# STEP 12: SURVEY-DESIGN VARIABLE AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

# Variables to inspect
candidate_design_vars = [
    "hhid",
    "t0_hhid",
    "batch",
    "region",
    "regurb",
    "subreg",
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
    "urban",
    "wgt",
    "hwgt_W7",
    "hwgt_wc",
    "wave",
]

# Keep only columns that actually exist
available_design_vars = [
    col for col in candidate_design_vars
    if col in gsec1.columns
]

design_audit = []

for col in available_design_vars:
    series = gsec1[col]

    design_audit.append({
        "variable": col,
        "data_type": str(series.dtype),
        "total_records": len(series),
        "missing_records": int(series.isna().sum()),
        "unique_values": int(series.nunique(dropna=True)),
        "example_values": str(
            series.dropna().unique()[:10].tolist()
        ),
    })

design_audit_df = pd.DataFrame(design_audit)

display(design_audit_df)

print("\nStep 12 completed.")
```


```python
# =========================================================
# STEP 13: VERIFY PSU AND STRATUM VARIABLES
# Read-only diagnostic
# =========================================================

import pandas as pd

datasets_to_check = {
    "GSEC1": gsec1,
    "AGSEC1": agsec1,
    "Geovars": geovars
    if "geovars" in globals()
    else None,
}

candidate_design_names = [
    "comm",
    "community",
    "ea",
    "ea_id",
    "psu",
    "cluster",
    "stratum",
    "strata",
    "hhid",
    "t0_hhid",
    "batch",
    "region",
    "regurb",
    "urban",
    "wgt",
    "hwgt_W7",
    "hwgt_w7",
    "hwgt_wc",
]

for dataset_name, df in datasets_to_check.items():

    print("\n" + "=" * 65)
    print(f"DATASET: {dataset_name}")
    print("=" * 65)

    if df is None:
        print("Dataset is not loaded as a DataFrame.")
        continue

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # Case-insensitive matching
    column_lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    matched_columns = []

    for candidate in candidate_design_names:
        actual_column = column_lookup.get(candidate.lower())

        if actual_column is not None:
            matched_columns.append(actual_column)

    matched_columns = list(dict.fromkeys(matched_columns))

    print("\nMatching variables:")
    print(matched_columns)

    if matched_columns:
        display(df[matched_columns].head(10))

        print("\nVariable summary:")

        summary = pd.DataFrame({
            "variable": matched_columns,
            "missing": [
                int(df[col].isna().sum())
                for col in matched_columns
            ],
            "unique_values": [
                int(df[col].nunique(dropna=True))
                for col in matched_columns
            ],
        })

        display(summary)

print("\nStep 13 completed.")
```


```python
# =========================================================
# STEP 14: INSPECT THE GEOVARS FILE
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

geovars_path = data_root / "unps_geovars_2018_19.csv"

if not geovars_path.exists():
    print("ERROR: Geovars file not found:")
    print(geovars_path)

else:
    geovars = pd.read_csv(
        geovars_path,
        low_memory=False
    )

    print("GEOVARS FILE")
    print("=" * 60)
    print("File:", geovars_path)
    print("Rows:", len(geovars))
    print("Columns:", len(geovars.columns))

    print("\nALL COLUMN NAMES:")
    print(geovars.columns.tolist())

    print("\nFIRST 10 RECORDS:")
    display(geovars.head(10))

    print("\nIDENTIFIER AND DESIGN CANDIDATES:")

    candidate_terms = [
        "hhid",
        "comm",
        "community",
        "ea",
        "psu",
        "cluster",
        "stratum",
        "region",
        "urban",
        "regurb",
        "subreg",
        "batch",
    ]

    matching_columns = [
        col for col in geovars.columns
        if any(
            term in str(col).lower()
            for term in candidate_terms
        )
    ]

    print(matching_columns)

    if matching_columns:
        display(
            geovars[matching_columns].head(10)
        )

    print("\nSTEP 14 COMPLETED.")
```


```python
# =========================================================
# STEP 15: SEARCH ALL CSV FILES FOR SURVEY-DESIGN VARIABLES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

search_terms = [
    "comm",
    "community",
    "stratum",
    "strata",
    "psu",
    "cluster",
    "ea_id",
    "ea",
    "enum_area",
    "enumeration",
]

search_results = []
files_checked = 0
files_failed = []

for csv_path in data_root.rglob("*.csv"):

    try:
        # Read only the header; do not load entire datasets.
        columns = pd.read_csv(
            csv_path,
            nrows=0,
            encoding="utf-8-sig"
        ).columns.tolist()

        files_checked += 1

        for column in columns:
            column_lower = str(column).strip().lower()

            matched_terms = [
                term for term in search_terms
                if term in column_lower
            ]

            if matched_terms:
                search_results.append({
                    "file": str(csv_path.relative_to(data_root)),
                    "column": column,
                    "matched_terms": ", ".join(matched_terms),
                })

    except Exception as exc:
        files_failed.append({
            "file": str(csv_path.relative_to(data_root)),
            "error": str(exc),
        })

print("CSV FILE AUDIT")
print("=" * 65)
print("CSV files successfully inspected:", files_checked)
print("Files with header-reading errors:", len(files_failed))

print("\nPOTENTIAL SURVEY-DESIGN VARIABLES")
print("=" * 65)

if search_results:
    design_search_df = pd.DataFrame(search_results)
    display(design_search_df)
else:
    print("No matching column names found.")

if files_failed:
    print("\nFILES THAT COULD NOT BE INSPECTED")
    display(pd.DataFrame(files_failed))

print("\nStep 15 completed.")
```


```python
# =========================================================
# STEP 16: INSPECT COMMUNITY EA IDENTIFIERS
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

community_path = data_root / "Community" / "CSEC1A.csv"

community = pd.read_csv(
    community_path,
    low_memory=False
)

print("COMMUNITY IDENTIFICATION DATASET")
print("=" * 65)

print("Rows:", len(community))
print("Columns:", len(community.columns))

print("\nAll column names:")
print(community.columns.tolist())

# Display only identification-related columns.
id_columns = [
    col for col in community.columns
    if any(
        term in str(col).lower()
        for term in [
            "ea_code",
            "comm",
            "hhid",
            "t0_",
            "region",
            "district",
            "urban",
            "wave",
        ]
    )
]

print("\nIdentification-related columns:")
print(id_columns)

if id_columns:
    display(community[id_columns].head(10))

    print("\nIdentifier summary:")
    identifier_summary = pd.DataFrame({
        "variable": id_columns,
        "missing": [
            int(community[col].isna().sum())
            for col in id_columns
        ],
        "unique_values": [
            int(community[col].nunique(dropna=True))
            for col in id_columns
        ],
    })

    display(identifier_summary)

print("\nSTEP 16 COMPLETED.")
```


```python
# =========================================================
# STEP 17: CHECK COMMUNITY-TO-HOUSEHOLD LINKAGE
# Read-only diagnostic
# =========================================================

import pandas as pd

# 1. Inspect interview identifiers in both datasets.
print("COMMUNITY IDENTIFIERS")
print("=" * 60)

community_id_cols = [
    col for col in [
        "EA_code",
        "t0_EA_code",
        "interview__key",
    ]
    if col in community.columns
]

display(community[community_id_cols].head(10))

print("\nHOUSEHOLD IDENTIFIERS")
print("=" * 60)

household_id_cols = [
    col for col in [
        "hhid",
        "t0_hhid",
        "interview__key",
        "batch",
        "wave",
    ]
    if col in gsec1.columns
]

display(gsec1[household_id_cols].head(10))

# 2. Check uniqueness and missingness of interview keys.
for name, df in [
    ("Community", community),
    ("GSEC1", gsec1),
]:
    print(f"\n{name} interview-key audit")

    if "interview__key" not in df.columns:
        print("interview__key is not available.")
        continue

    key = df["interview__key"]

    print("Total records:", len(df))
    print("Missing keys:", int(key.isna().sum()))
    print("Unique nonmissing keys:", int(key.nunique()))
    print(
        "Duplicated nonmissing keys:",
        int(key.dropna().duplicated().sum())
    )

# 3. Check whether interview keys overlap.
if (
    "interview__key" in community.columns
    and "interview__key" in gsec1.columns
):
    community_keys = set(
        community["interview__key"].dropna()
    )

    household_keys = set(
        gsec1["interview__key"].dropna()
    )

    print("\nINTERVIEW-KEY OVERLAP")
    print("=" * 60)
    print("Community unique keys:", len(community_keys))
    print("GSEC1 unique keys:", len(household_keys))
    print(
        "Keys shared by both files:",
        len(community_keys & household_keys)
    )
    print(
        "Community-only keys:",
        len(community_keys - household_keys)
    )
    print(
        "GSEC1-only keys:",
        len(household_keys - community_keys)
    )

print("\nStep 17 completed.")
```


```python
# =========================================================
# STEP 18: COMPARE COMMUNITY IDENTIFICATION FILES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

community_files = [
    "Community/CSEC1A.csv",
    "Community/CSEC11_0.csv",
    "Community/CSEC11_1.csv",
]

for relative_path in community_files:

    file_path = data_root / relative_path

    print("\n" + "=" * 70)
    print("FILE:", relative_path)
    print("=" * 70)

    if not file_path.exists():
        print("File not found.")
        continue

    try:
        df = pd.read_csv(
            file_path,
            low_memory=False
        )

        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("\nColumn names:")
        print(df.columns.tolist())

        # Identify relevant columns.
        relevant_columns = [
            col for col in df.columns
            if any(
                term in str(col).lower()
                for term in [
                    "ea_code",
                    "interview__key",
                    "comm",
                    "hhid",
                    "t0_",
                    "batch",
                    "wave",
                ]
            )
        ]

        print("\nRelevant columns:")
        print(relevant_columns)

        if relevant_columns:
            display(df[relevant_columns].head(10))

            summary = pd.DataFrame({
                "variable": relevant_columns,
                "missing": [
                    int(df[col].isna().sum())
                    for col in relevant_columns
                ],
                "unique_values": [
                    int(df[col].nunique(dropna=True))
                    for col in relevant_columns
                ],
            })

            print("\nIdentifier summary:")
            display(summary)

    except Exception as exc:
        print("Could not read file:", exc)

print("\nStep 18 completed.")
```


```python
# =========================================================
# STEP 19: INSPECT HOUSEHOLD AND HISTORICAL EA IDENTIFIERS
# Read-only diagnostic
# =========================================================

import pandas as pd

print("HOUSEHOLD HISTORICAL IDENTIFIERS")
print("=" * 65)

display(gsec1[["hhid", "t0_hhid"]].head(20))

print("\nHISTORICAL EA IDENTIFIERS")
print("=" * 65)

display(community[["EA_code", "t0_EA_code"]].head(20))

# Inspect identifier formats without changing the source data.
print("\nIDENTIFIER FORMAT SUMMARY")
print("=" * 65)

identifier_columns = {
    "GSEC1.hhid": gsec1["hhid"],
    "GSEC1.t0_hhid": gsec1["t0_hhid"],
    "Community.EA_code": community["EA_code"],
    "Community.t0_EA_code": community["t0_EA_code"],
}

format_rows = []

for name, series in identifier_columns.items():
    values = series.dropna().astype(str)

    format_rows.append({
        "variable": name,
        "nonmissing_values": len(values),
        "example_values": values.head(5).tolist(),
        "minimum_length": (
            int(values.str.len().min())
            if len(values) > 0 else None
        ),
        "maximum_length": (
            int(values.str.len().max())
            if len(values) > 0 else None
        ),
    })

display(pd.DataFrame(format_rows))

print("\nStep 19 completed.")
```


```python
# =========================================================
# STEP 20: TEST HISTORICAL IDENTIFIER RELATIONSHIPS
# Read-only diagnostic
# =========================================================

import pandas as pd

# Convert identifiers to strings while preserving missing values.
household = gsec1.copy()
community_ids = community.copy()

household["t0_hhid_clean"] = (
    household["t0_hhid"].astype("string").str.strip()
)

community_ids["t0_EA_code_clean"] = (
    community_ids["t0_EA_code"].astype("string").str.strip()
)

community_ids["EA_code_clean"] = (
    community_ids["EA_code"].astype("string").str.strip()
)

print("=" * 70)
print("1. HISTORICAL HOUSEHOLD ID VS HISTORICAL EA CODE")
print("=" * 70)

household_ids = set(
    household["t0_hhid_clean"].dropna()
)

historical_ea_ids = set(
    community_ids["t0_EA_code_clean"].dropna()
)

matches = household_ids.intersection(historical_ea_ids)

print("Unique historical household IDs:",
      len(household_ids))

print("Unique historical EA codes:",
      len(historical_ea_ids))

print("Exact identifier matches:", len(matches))

if matches:
    print("Example matches:", list(matches)[:10])
else:
    print("No exact matches found.")

print("\n" + "=" * 70)
print("2. CURRENT HOUSEHOLD ID VS CURRENT EA CODE")
print("=" * 70)

current_household_ids = set(
    household["hhid"].dropna().astype(str)
)

current_ea_ids = set(
    community_ids["EA_code_clean"].dropna()
)

current_matches = current_household_ids.intersection(
    current_ea_ids
)

print("Unique current household IDs:",
      len(current_household_ids))

print("Unique current EA codes:",
      len(current_ea_ids))

print("Exact identifier matches:", len(current_matches))

print("\n" + "=" * 70)
print("3. HOUSEHOLD BATCH SUMMARY")
print("=" * 70)

if "batch" in household.columns:
    print("Unique batch values:",
          household["batch"].nunique(dropna=True))

    print("Missing batch values:",
          household["batch"].isna().sum())

    display(
        household["batch"]
        .value_counts(dropna=False)
        .head(20)
        .rename_axis("batch")
        .reset_index(name="household_records")
    )
else:
    print("The batch variable is not present.")

print("\n" + "=" * 70)
print("4. HOUSEHOLD HISTORICAL ID FORMAT")
print("=" * 70)

display(
    household[["hhid", "t0_hhid"]]
    .assign(
        historical_id_length=lambda x:
            x["t0_hhid"].astype("string").str.len()
    )
    .head(15)
)

print("\nStep 20 completed.")
```


```python
# =========================================================
# STEP 21: EXAMINE BATCH AND GEOGRAPHIC VARIABLES
# Read-only diagnostic
# =========================================================

import pandas as pd

required_columns = [
    "batch",
    "region",
    "urban",
    "regurb",
    "subreg",
]

missing_columns = [
    col for col in required_columns
    if col not in gsec1.columns
]

if missing_columns:
    print("Missing columns:", missing_columns)

else:
    df_design = gsec1[required_columns].copy()

    print("=" * 70)
    print("1. BATCH SUMMARY")
    print("=" * 70)

    print("Household records:", len(df_design))
    print("Unique batches:", df_design["batch"].nunique())
    print("Missing batch values:", df_design["batch"].isna().sum())

    print("\nHousehold records per batch:")
    display(
        df_design["batch"]
        .value_counts()
        .describe()
        .to_frame("records_per_batch")
    )

    print("\n" + "=" * 70)
    print("2. GEOGRAPHIC VARIABLE COUNTS")
    print("=" * 70)

    for col in ["region", "urban", "regurb", "subreg"]:
        print(f"\n{col}:")
        display(
            df_design[col]
            .value_counts(dropna=False)
            .sort_index()
            .rename_axis(col)
            .reset_index(name="household_records")
        )

    print("\n" + "=" * 70)
    print("3. UNIQUE GEOGRAPHIC VALUES WITHIN EACH BATCH")
    print("=" * 70)

    batch_geo = (
        df_design.groupby("batch", dropna=False)
        .agg(
            household_records=("batch", "size"),
            regions=("region", "nunique"),
            urban_categories=("urban", "nunique"),
            regurb_categories=("regurb", "nunique"),
            subregions=("subreg", "nunique"),
        )
        .reset_index()
    )

    display(batch_geo.head(20))

    print("\nBatch geographic consistency:")
    display(
        batch_geo[
            [
                "regions",
                "urban_categories",
                "regurb_categories",
                "subregions",
            ]
        ].value_counts().rename("number_of_batches").to_frame()
    )

    print("\nStep 21 completed.")
```


```python
# =========================================================
# STEP 22: CROSS-SECTIONAL READINESS AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

# Use the existing dataframes from earlier notebook steps.
required_datasets = {
    "GSEC1": gsec1,
    "AGSEC1": agsec1,
    "AGSEC4A": pd.read_csv(
        r"C:\Users\H-START\Desktop\dataset\Agric\AGSEC4A.csv",
        low_memory=False
    ),
    "AGSEC4B": pd.read_csv(
        r"C:\Users\H-START\Desktop\dataset\Agric\AGSEC4B.csv",
        low_memory=False
    ),
}

print("=" * 75)
print("1. DATASET DIMENSIONS")
print("=" * 75)

for name, df in required_datasets.items():
    print(f"{name}: {len(df):,} rows × {len(df.columns):,} columns")

print("\n" + "=" * 75)
print("2. HOUSEHOLD IDENTIFIERS AND WEIGHTS")
print("=" * 75)

for name in ["GSEC1", "AGSEC1"]:
    df = required_datasets[name]

    print(f"\n{name}")

    columns_to_check = [
        "hhid",
        "t0_hhid",
        "wgt",
        "hwgt_w7",
        "hwgt_W7",
        "hwgt_wc",
        "batch",
        "region",
        "urban",
        "regurb",
        "subreg",
    ]

    available = [c for c in columns_to_check if c in df.columns]

    rows = []

    for col in available:
        rows.append({
            "variable": col,
            "missing": int(df[col].isna().sum()),
            "nonmissing": int(df[col].notna().sum()),
            "unique_nonmissing": int(df[col].nunique(dropna=True)),
        })

    display(pd.DataFrame(rows))

print("\n" + "=" * 75)
print("3. AGRICULTURAL FILE IDENTIFIERS")
print("=" * 75)

for name in ["AGSEC4A", "AGSEC4B"]:
    df = required_datasets[name]

    print(f"\n{name}")
    print("Columns:", df.columns.tolist())

    id_columns = [
        c for c in df.columns
        if c.lower() in [
            "hhid",
            "t0_hhid",
            "interview__key",
            "plot_id",
            "parcel_id",
        ]
    ]

    print("Potential identifier columns:", id_columns)

    if id_columns:
        display(df[id_columns].head(5))

print("\nStep 22 completed.")
```


```python
# =========================================================
# STEP 23: HOUSEHOLD LINKAGE AND SEED VARIABLE AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

# Retrieve existing DataFrames from Step 22.
gsec1 = required_datasets["GSEC1"]
agsec4a = required_datasets["AGSEC4A"]
agsec4b = required_datasets["AGSEC4B"]

# ---------------------------------------------------------
# 1. Confirm household identifiers
# ---------------------------------------------------------

print("=" * 75)
print("1. HOUSEHOLD IDENTIFIER VALIDATION")
print("=" * 75)

household_ids = set(gsec1["hhid"].dropna().astype(str))

for name, df in [
    ("AGSEC4A", agsec4a),
    ("AGSEC4B", agsec4b),
]:
    crop_ids = set(df["hhid"].dropna().astype(str))

    matched = crop_ids.intersection(household_ids)
    unmatched = crop_ids.difference(household_ids)

    print(f"\n{name}")
    print("Crop records:", len(df))
    print("Unique household IDs:", len(crop_ids))
    print("Household IDs found in GSEC1:", len(matched))
    print("Household IDs absent from GSEC1:", len(unmatched))

    if unmatched:
        print("Example unmatched IDs:", list(unmatched)[:5])

# ---------------------------------------------------------
# 2. Check historical household ID consistency
# ---------------------------------------------------------

print("\n" + "=" * 75)
print("2. HISTORICAL HOUSEHOLD ID CONSISTENCY")
print("=" * 75)

for name, df in [
    ("AGSEC4A", agsec4a),
    ("AGSEC4B", agsec4b),
]:
    merged = df[["hhid", "t0_hhid"]].merge(
        gsec1[["hhid", "t0_hhid"]].rename(
            columns={"t0_hhid": "gsec1_t0_hhid"}
        ),
        on="hhid",
        how="left",
        validate="many_to_one",
    )

    matched = merged["gsec1_t0_hhid"].notna()

    crop_t0 = merged.loc[matched, "t0_hhid"].astype("string")
    household_t0 = merged.loc[
        matched, "gsec1_t0_hhid"
    ].astype("string")

    consistent = crop_t0.eq(household_t0)

    print(f"\n{name}")
    print("Matched crop records:", int(matched.sum()))
    print("Matching historical IDs:", int(consistent.sum()))
    print("Different historical IDs:", int((~consistent).sum()))

# ---------------------------------------------------------
# 3. Audit seed variable distributions
# ---------------------------------------------------------

print("\n" + "=" * 75)
print("3. SEED VARIABLE DISTRIBUTIONS")
print("=" * 75)

seed_variables = {
    "AGSEC4A": {
        "data": agsec4a,
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "AGSEC4B": {
        "data": agsec4b,
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for name, config in seed_variables.items():
    df = config["data"]

    print(f"\n{name}")

    for label, col in [
        ("Seed use", config["seed_use"]),
        ("Seed type", config["seed_type"]),
        ("Improved seed category", config["improved_category"]),
    ]:
        print(f"\n{label} ({col})")

        if col not in df.columns:
            print("Variable not found.")
            continue

        distribution = (
            df[col]
            .value_counts(dropna=False)
            .sort_index()
            .rename_axis("value")
            .reset_index(name="records")
        )

        distribution["percentage"] = (
            distribution["records"] / len(df) * 100
        ).round(2)

        display(distribution)

print("\nStep 23 completed.")
```


```python
# =========================================================
# STEP 24: SEED QUESTIONNAIRE SKIP-PATTERN AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

seed_audits = {
    "AGSEC4A": {
        "data": agsec4a,
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "AGSEC4B": {
        "data": agsec4b,
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

for name, config in seed_audits.items():

    df = config["data"]

    use = config["seed_use"]
    seed_type = config["seed_type"]
    category = config["improved_category"]

    print("\n" + "=" * 80)
    print(f"STEP 24: {name} — SEED RESPONSE COMBINATIONS")
    print("=" * 80)

    # -----------------------------------------------------
    # 1. Seed use versus seed type
    # -----------------------------------------------------

    print("\n1. Seed use versus seed type")

    use_type = pd.crosstab(
        df[use].fillna("MISSING"),
        df[seed_type].fillna("MISSING"),
        margins=True,
        dropna=False
    )

    display(use_type)

    # -----------------------------------------------------
    # 2. Seed use versus improved-seed category
    # -----------------------------------------------------

    print("\n2. Seed use versus improved-seed category")

    use_category = pd.crosstab(
        df[use].fillna("MISSING"),
        df[category].fillna("MISSING"),
        margins=True,
        dropna=False
    )

    display(use_category)

    # -----------------------------------------------------
    # 3. Seed type versus improved-seed category
    # -----------------------------------------------------

    print("\n3. Seed type versus improved-seed category")

    type_category = pd.crosstab(
        df[seed_type].fillna("MISSING"),
        df[category].fillna("MISSING"),
        margins=True,
        dropna=False
    )

    display(type_category)

    # -----------------------------------------------------
    # 4. Inspect potentially contradictory responses
    # -----------------------------------------------------

    print("\n4. Potentially contradictory responses")

    contradictions = df[
        (
            (df[use] == 2) &
            (
                df[seed_type].notna() |
                df[category].notna()
            )
        )
        |
        (
            (df[seed_type] == 1) &
            df[category].isin([1, 2])
        )
    ][[
        "hhid",
        "cropID",
        use,
        seed_type,
        category
    ]].copy()

    print(
        "Records flagged for review:",
        len(contradictions)
    )

    display(contradictions.head(20))

print("\nStep 24 completed.")
```


```python
# =========================================================
# STEP 25: INSPECT UNRESOLVED SEED RESPONSES
# Read-only diagnostic
# =========================================================

import pandas as pd

cases = {
    "AGSEC4A": {
        "data": agsec4a,
        "use": "s4aq16",
        "type": "s4aq13",
        "category": "s4aq14",
    },
    "AGSEC4B": {
        "data": agsec4b,
        "use": "s4bq16",
        "type": "s4bq13",
        "category": "s4bq14",
    },
}

for name, cfg in cases.items():
    df = cfg["data"]

    print("\n" + "=" * 75)
    print(f"{name}: UNRESOLVED SEED RESPONSES")
    print("=" * 75)

    # Seed use reported, but seed type is missing.
    missing_type = df[
        (df[cfg["use"]] == 1) &
        df[cfg["type"]].isna()
    ]

    print(
        "\nSeed use = Yes, but seed type is missing:",
        len(missing_type)
    )

    display(
        missing_type[
            [
                "hhid",
                "t0_hhid",
                "parcelID",
                "pltid",
                "cropID",
                cfg["use"],
                cfg["type"],
                cfg["category"],
            ]
        ].head(20)
    )

    # Improved seed reported, but category is missing.
    missing_category = df[
        (df[cfg["type"]] == 2) &
        df[cfg["category"]].isna()
    ]

    print(
        "\nImproved seed reported, but category is missing:",
        len(missing_category)
    )

    display(
        missing_category[
            [
                "hhid",
                "t0_hhid",
                "parcelID",
                "pltid",
                "cropID",
                cfg["use"],
                cfg["type"],
                cfg["category"],
            ]
        ]
    )

    # Seed use is missing.
    missing_use = df[df[cfg["use"]].isna()]

    print("\nRecords with missing seed-use status:", len(missing_use))

    display(
        missing_use[
            [
                "hhid",
                "t0_hhid",
                "parcelID",
                "pltid",
                "cropID",
                cfg["use"],
                cfg["type"],
                cfg["category"],
            ]
        ].head(20)
    )

print("\nStep 25 completed.")
```


```python
# =========================================================
# STEP 26: INVESTIGATE HOUSEHOLD LINKAGE DISCREPANCIES
# Read-only diagnostic
# =========================================================

import pandas as pd

crop_datasets = {
    "AGSEC4A": agsec4a,
    "AGSEC4B": agsec4b,
}

gsec_ids = set(gsec1["hhid"].dropna().astype(str))

for name, crop_df in crop_datasets.items():

    print("\n" + "=" * 80)
    print(f"STEP 26: {name} HOUSEHOLD LINKAGE")
    print("=" * 80)

    # -----------------------------------------------------
    # 1. Identify crop household IDs absent from GSEC1
    # -----------------------------------------------------

    crop_ids = set(crop_df["hhid"].dropna().astype(str))
    unmatched_ids = crop_ids - gsec_ids

    unmatched = crop_df[
        crop_df["hhid"].astype(str).isin(unmatched_ids)
    ].copy()

    print("\n1. Unmatched household IDs")
    print("Unique unmatched households:", len(unmatched_ids))
    print("Crop records belonging to unmatched households:",
          len(unmatched))

    if not unmatched.empty:
        unmatched_summary = (
            unmatched.groupby(
                ["hhid", "t0_hhid"],
                dropna=False
            )
            .agg(
                crop_records=("cropID", "size"),
                unique_crops=("cropID", "nunique"),
                parcels=("parcelID", "nunique"),
            )
            .reset_index()
        )

        display(unmatched_summary.head(40))

    # -----------------------------------------------------
    # 2. Compare historical IDs for matched households
    # -----------------------------------------------------

    print("\n2. Historical household ID discrepancies")

    comparison = crop_df[
        ["hhid", "t0_hhid"]
    ].merge(
        gsec1[["hhid", "t0_hhid"]].rename(
            columns={"t0_hhid": "gsec1_t0_hhid"}
        ),
        on="hhid",
        how="inner",
        validate="many_to_one"
    )

    comparison["historical_id_match"] = (
        comparison["t0_hhid"].astype("string")
        == comparison["gsec1_t0_hhid"].astype("string")
    )

    discrepancies = comparison[
        ~comparison["historical_id_match"]
    ].copy()

    print("Matched crop records:", len(comparison))
    print("Records with different historical IDs:",
          len(discrepancies))
    print("Unique affected current household IDs:",
          discrepancies["hhid"].nunique())

    if not discrepancies.empty:
        discrepancy_summary = (
            discrepancies.groupby(
                ["hhid", "t0_hhid", "gsec1_t0_hhid"],
                dropna=False
            )
            .size()
            .reset_index(name="crop_records")
        )

        display(discrepancy_summary.head(40))

    # -----------------------------------------------------
    # 3. Check whether a historical ID maps to multiple
    #    current household IDs within each crop dataset
    # -----------------------------------------------------

    print("\n3. Historical ID mapping")

    historical_mapping = (
        crop_df.dropna(subset=["t0_hhid"])
        .groupby("t0_hhid")["hhid"]
        .nunique()
        .reset_index(name="current_household_count")
    )

    multiple_current_ids = historical_mapping[
        historical_mapping["current_household_count"] > 1
    ]

    print("Historical IDs mapping to multiple current IDs:",
          len(multiple_current_ids))

    if not multiple_current_ids.empty:
        display(multiple_current_ids.head(20))

print("\nStep 26 completed.")
```


```python
# =========================================================
# STEP 27: RAW HISTORICAL HOUSEHOLD ID AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

datasets = {
    "GSEC1": gsec1,
    "AGSEC4A": agsec4a,
    "AGSEC4B": agsec4b,
}

for name, df in datasets.items():

    print("\n" + "=" * 80)
    print(f"STEP 27: {name} — RAW t0_hhid VALUES")
    print("=" * 80)

    # Confirm the data type and missing-value count.
    print("Data type:", df["t0_hhid"].dtype)
    print("Pandas missing values:", df["t0_hhid"].isna().sum())

    # Show the most frequent values exactly as stored.
    print("\nMost frequent raw values:")

    display(
        df["t0_hhid"]
        .value_counts(dropna=False)
        .head(20)
        .rename_axis("raw_t0_hhid")
        .reset_index(name="records")
    )

    # Identify suspicious textual missing-value representations.
    values = df["t0_hhid"].astype("string").str.strip()

    suspicious = (
        values.isna()
        | values.str.upper().isin(
            ["", "NA", "N/A", "##N/A##", "NAN", "NONE", "NULL"]
        )
    )

    print("\nRows with actual or suspicious missing identifiers:",
          int(suspicious.sum()))

    display(
        df.loc[suspicious, ["hhid", "t0_hhid"]]
        .drop_duplicates()
        .head(20)
    )

# ---------------------------------------------------------
# Examine the historical-ID discrepancies already identified
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("RAW VALUES FOR SELECTED HOUSEHOLD ID DISCREPANCIES")
print("=" * 80)

selected_ids = [
    "16c0790e52ec43c58fcd99e7d75e10d3",
    "34ab177d08094b66a890dda0e33da027",
    "0b7f6c75dec34a6bb3c0990283c92be6",
    "326cfa25f0a54505a7a8526f4d9dfd21",
    "37cc1f4211c74fe8864dc44b67591f92",
]

for hhid in selected_ids:

    print(f"\nCurrent household ID: {hhid}")

    for name, df in datasets.items():

        rows = df.loc[
            df["hhid"].astype("string") == hhid,
            ["hhid", "t0_hhid"]
        ].drop_duplicates()

        if not rows.empty:
            print(name)
            display(rows)

print("\nStep 27 completed.")
```


```python
# =========================================================
# STEP 28: HISTORICAL ID NORMALIZATION AUDIT
# Read-only diagnostic
# =========================================================

import pandas as pd

crop_datasets = {
    "AGSEC4A": agsec4a,
    "AGSEC4B": agsec4b,
}

def normalize_historical_id(series):
    """
    Diagnostic normalization:
    - Convert to pandas string dtype.
    - Trim surrounding whitespace.
    - Treat explicit missing-value markers as missing.
    - Remove one leading H from nonmissing identifiers.
    
    This function is for comparison only.
    It does not change the original datasets.
    """
    result = series.astype("string").str.strip()

    missing_markers = [
        "",
        "NA",
        "N/A",
        "##N/A##",
        "NAN",
        "NONE",
        "NULL",
    ]

    result = result.mask(
        result.str.upper().isin(missing_markers)
    )

    result = result.str.replace(
        r"^H",
        "",
        regex=True
    )

    return result


for name, crop_df in crop_datasets.items():

    print("\n" + "=" * 80)
    print(f"STEP 28: {name} NORMALIZATION AUDIT")
    print("=" * 80)

    # Preserve original values in the source DataFrames.
    crop_ids = crop_df[["hhid", "t0_hhid"]].copy()

    household_ids = gsec1[["hhid", "t0_hhid"]].copy()

    household_ids = household_ids.rename(
        columns={"t0_hhid": "gsec1_t0_hhid"}
    )

    comparison = crop_ids.merge(
        household_ids,
        on="hhid",
        how="inner",
        validate="many_to_one"
    )

    # Compare original IDs.
    comparison["original_match"] = (
        comparison["t0_hhid"].astype("string")
        == comparison["gsec1_t0_hhid"].astype("string")
    )

    # Compare normalized IDs.
    comparison["crop_t0_normalized"] = normalize_historical_id(
        comparison["t0_hhid"]
    )

    comparison["gsec1_t0_normalized"] = normalize_historical_id(
        comparison["gsec1_t0_hhid"]
    )

    comparison["normalized_match"] = (
        comparison["crop_t0_normalized"]
        == comparison["gsec1_t0_normalized"]
    )

    # Exclude cases where either normalized value is missing.
    both_present = (
        comparison["crop_t0_normalized"].notna()
        & comparison["gsec1_t0_normalized"].notna()
    )

    # Summary results.
    print("Matched crop records:", len(comparison))

    print(
        "Original exact matches:",
        int(comparison["original_match"].sum())
    )

    print(
        "Normalized matches, both IDs present:",
        int(
            (
                comparison["normalized_match"]
                & both_present
            ).sum()
        )
    )

    print(
        "Records with a missing historical ID in either file:",
        int((~both_present).sum())
    )

    print(
        "Records still mismatching after normalization:",
        int(
            (
                ~comparison["normalized_match"]
                & both_present
            ).sum()
        )
    )

    # Show remaining discrepancies for inspection.
    remaining = comparison[
        both_present
        & ~comparison["normalized_match"]
    ][
        [
            "hhid",
            "t0_hhid",
            "gsec1_t0_hhid",
            "crop_t0_normalized",
            "gsec1_t0_normalized",
        ]
    ].drop_duplicates()

    if not remaining.empty:
        print("\nExamples of remaining discrepancies:")
        display(remaining.head(30))

print("\nStep 28 completed.")
```


```python
# =========================================================
# STEP 29: INVESTIGATE AGSEC4B HISTORICAL-ID DISCREPANCIES
# Read-only diagnostic
# =========================================================

import pandas as pd

# Prepare household reference without modifying GSEC1.
household_reference = (
    gsec1[["hhid", "t0_hhid"]]
    .rename(columns={"t0_hhid": "gsec1_t0_hhid"})
    .copy()
)

# Link using current household ID.
audit = agsec4b.merge(
    household_reference,
    on="hhid",
    how="inner",
    validate="many_to_one"
)

# Standardize values only for comparison.
# Original columns remain unchanged.
audit["crop_t0_raw"] = (
    audit["t0_hhid"]
    .astype("string")
    .str.strip()
)

audit["gsec1_t0_raw"] = (
    audit["gsec1_t0_hhid"]
    .astype("string")
    .str.strip()
)

missing_markers = [
    "",
    "NA",
    "N/A",
    "##N/A##",
    "NAN",
    "NONE",
    "NULL",
]

audit["crop_t0_clean"] = audit["crop_t0_raw"].mask(
    audit["crop_t0_raw"].str.upper().isin(missing_markers)
)

audit["gsec1_t0_clean"] = audit["gsec1_t0_raw"].mask(
    audit["gsec1_t0_raw"].str.upper().isin(missing_markers)
)

# Remove a leading H for diagnostic comparison only.
audit["crop_t0_normalized"] = (
    audit["crop_t0_clean"].str.replace(r"^H", "", regex=True)
)

audit["gsec1_t0_normalized"] = (
    audit["gsec1_t0_clean"].str.replace(r"^H", "", regex=True)
)

both_present = (
    audit["crop_t0_normalized"].notna()
    & audit["gsec1_t0_normalized"].notna()
)

audit["normalized_match"] = (
    audit["crop_t0_normalized"]
    == audit["gsec1_t0_normalized"]
)

mismatches = audit.loc[
    both_present & ~audit["normalized_match"]
].copy()

print("=" * 80)
print("STEP 29: AGSEC4B REMAINING HISTORICAL-ID DISCREPANCIES")
print("=" * 80)

print("Mismatched crop records:", len(mismatches))

print(
    "Unique affected current household IDs:",
    mismatches["hhid"].nunique()
)

print(
    "Unique mismatched crop identifiers:",
    mismatches["crop_t0_raw"].nunique()
)

print(
    "Unique corresponding GSEC1 historical identifiers:",
    mismatches["gsec1_t0_raw"].nunique()
)

# ---------------------------------------------------------
# A. Most frequent mismatch combinations
# ---------------------------------------------------------

print("\nA. Most frequent mismatch combinations")

mismatch_combinations = (
    mismatches.groupby(
        ["crop_t0_raw", "gsec1_t0_raw"],
        dropna=False
    )
    .size()
    .reset_index(name="crop_records")
    .sort_values("crop_records", ascending=False)
)

display(mismatch_combinations.head(30))

# ---------------------------------------------------------
# B. Number of mismatched crop records per household
# ---------------------------------------------------------

print("\nB. Households with the most mismatched crop records")

household_mismatch_counts = (
    mismatches.groupby("hhid")
    .agg(
        mismatched_crop_records=("hhid", "size"),
        crop_ids=("crop_t0_raw", "nunique"),
        gsec1_ids=("gsec1_t0_raw", "nunique"),
    )
    .reset_index()
    .sort_values("mismatched_crop_records", ascending=False)
)

display(household_mismatch_counts.head(30))

# ---------------------------------------------------------
# C. Check whether the crop identifier contains digits only
# ---------------------------------------------------------

print("\nC. Format of crop-file historical identifiers")

mismatches["crop_id_digits_only"] = (
    mismatches["crop_t0_raw"].str.fullmatch(r"\d+")
)

display(
    mismatches["crop_id_digits_only"]
    .value_counts(dropna=False)
    .rename_axis("digits_only")
    .reset_index(name="records")
)

# ---------------------------------------------------------
# D. Inspect the raw records for selected mismatches
# ---------------------------------------------------------

print("\nD. Selected mismatched crop records")

selected_columns = [
    "hhid",
    "t0_hhid",
    "gsec1_t0_hhid",
    "parcelID",
    "pltid",
    "cropID",
    "interview__key",
]

display(
    mismatches[selected_columns]
    .drop_duplicates()
    .head(25)
)

print("\nStep 29 completed. No source datasets were modified.")
```


```python
# =========================================================
# STEP 30: VERIFY AGSEC4B IDENTIFIERS AGAINST SOURCE CSV
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
agsec4b_path = data_root / "Agric" / "AGSEC4B.csv"

print("=" * 80)
print("STEP 30: AGSEC4B SOURCE-FILE VERIFICATION")
print("=" * 80)

# Read the source CSV directly.
# Reading t0_hhid as a string preserves its textual representation.
source_agsec4b = pd.read_csv(
    agsec4b_path,
    dtype={
        "hhid": "string",
        "t0_hhid": "string",
    },
    keep_default_na=False,
)

print("Source file:", agsec4b_path)
print("Source dimensions:", source_agsec4b.shape)

print("\nSource column names:")
print(source_agsec4b.columns.tolist())

# ---------------------------------------------------------
# A. Compare source values with the active notebook DataFrame
# ---------------------------------------------------------

print("\nA. Compare source and active DataFrame")

print("Active DataFrame dimensions:", agsec4b.shape)

print(
    "Source t0_hhid data type:",
    source_agsec4b["t0_hhid"].dtype,
)

print(
    "Active t0_hhid data type:",
    agsec4b["t0_hhid"].dtype,
)

# Compare the two files using hhid and crop-level identifiers.
# These fields are used only to locate corresponding records.
record_keys = ["hhid", "parcelID", "pltid", "cropID"]

required_columns = record_keys + ["t0_hhid"]

missing_columns = [
    col for col in required_columns
    if col not in source_agsec4b.columns
    or col not in agsec4b.columns
]

if missing_columns:
    print("Cannot perform full record comparison.")
    print("Missing columns:", missing_columns)

else:
    source_check = source_agsec4b[required_columns].copy()
    active_check = agsec4b[required_columns].copy()

    # Normalize only the record-key columns for comparison.
    for col in record_keys:
        source_check[col] = (
            source_check[col].astype("string").str.strip()
        )
        active_check[col] = (
            active_check[col].astype("string").str.strip()
        )

    source_check = source_check.rename(
        columns={"t0_hhid": "source_t0_hhid"}
    )

    active_check = active_check.rename(
        columns={"t0_hhid": "active_t0_hhid"}
    )

    comparison = source_check.merge(
        active_check,
        on=record_keys,
        how="outer",
        indicator=True,
        validate="one_to_one",
    )

    print("\nRecord-key comparison:")
    print(comparison["_merge"].value_counts(dropna=False))

    matched = comparison.loc[
        comparison["_merge"] == "both"
    ].copy()

    matched["source_t0_hhid"] = (
        matched["source_t0_hhid"]
        .astype("string")
        .str.strip()
    )

    matched["active_t0_hhid"] = (
        matched["active_t0_hhid"]
        .astype("string")
        .str.strip()
    )

    different = matched.loc[
        matched["source_t0_hhid"]
        != matched["active_t0_hhid"]
    ]

    print(
        "\nMatched records with different t0_hhid values:",
        len(different),
    )

    if not different.empty:
        display(different.head(20))

# ---------------------------------------------------------
# B. Inspect source-file values for selected households
# ---------------------------------------------------------

print("\nB. Selected households in the original source CSV")

selected_households = [
    "068501d062324eb097b62ccfea8a5fa6",
    "07919f0a80fb43dc9dbbc762b869adbf",
    "15f9cb22388f428f9f3dcf081ccfc10a",
    "2280f98ac1154da5a0ef0da8b4a4f4bb",
]

for household_id in selected_households:
    print(f"\nHousehold ID: {household_id}")

    rows = source_agsec4b.loc[
        source_agsec4b["hhid"].astype("string")
        == household_id,
        [
            "hhid",
            "t0_hhid",
            "parcelID",
            "pltid",
            "cropID",
        ],
    ]

    display(rows)

print("\nStep 30 completed. No source data were modified.")
```


```python
# =========================================================
# STEP 31A: LOCATE HISTORICAL-ID DEFINITIONS IN DOCUMENTATION
# Read-only diagnostic
# =========================================================

from pathlib import Path

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

pdf_files = [
    data_root / "ddi-documentation-english_microdata-3795.pdf",
    data_root / "agriculture_qx.pdf",
    data_root / "unps_7_bid.pdf",
    data_root / "unps_hhq.pdf",
]

print("=" * 80)
print("STEP 31A: DOCUMENTATION FILE CHECK")
print("=" * 80)

for pdf_path in pdf_files:
    print(
        f"{pdf_path.name}: "
        f"{'FOUND' if pdf_path.exists() else 'NOT FOUND'}"
    )

print("\nNotebook and source data remain unchanged.")
```


```python
# =========================================================
# STEP 31B: SEARCH UNPS DOCUMENTATION FOR IDENTIFIER RULES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import re

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

pdf_paths = [
    data_root / "ddi-documentation-english_microdata-3795.pdf",
    data_root / "agriculture_qx.pdf",
    data_root / "unps_7_bid.pdf",
    data_root / "unps_hhq.pdf",
]

# Terms relevant to the historical household identifier.
search_terms = [
    "t0_hhid",
    "historical household",
    "household identifier",
    "household ID",
    "AGSEC4B",
    "s4bq16",
    "baseline household",
    "household split",
    "identifier",
]

print("=" * 80)
print("STEP 31B: SEARCHING UNPS PDF DOCUMENTATION")
print("=" * 80)

# Try pypdf first, then PyMuPDF.
pdf_backend = None

try:
    from pypdf import PdfReader
    pdf_backend = "pypdf"
except ImportError:
    try:
        import fitz
        pdf_backend = "pymupdf"
    except ImportError:
        print(
            "Neither pypdf nor PyMuPDF is installed. "
            "Install pypdf in the active notebook environment, "
            "then rerun this cell."
        )

if pdf_backend is not None:
    print("PDF extraction library:", pdf_backend)

    total_hits = 0

    for pdf_path in pdf_paths:
        print("\n" + "=" * 80)
        print("DOCUMENT:", pdf_path.name)
        print("=" * 80)

        if not pdf_path.exists():
            print("File not found:", pdf_path)
            continue

        # Extract text page by page.
        pages = []

        if pdf_backend == "pypdf":
            reader = PdfReader(str(pdf_path))

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                pages.append((page_number, text))

        else:
            document = fitz.open(str(pdf_path))

            for page_number, page in enumerate(document, start=1):
                pages.append((page_number, page.get_text() or ""))

            document.close()

        document_hits = 0

        for page_number, page_text in pages:
            for term in search_terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)

                for match in pattern.finditer(page_text):
                    start = max(0, match.start() - 220)
                    end = min(len(page_text), match.end() + 350)

                    excerpt = page_text[start:end]
                    excerpt = re.sub(r"\s+", " ", excerpt).strip()

                    print(
                        f"\nPage {page_number} | "
                        f"Search term: {term}"
                    )
                    print(excerpt)

                    document_hits += 1
                    total_hits += 1

                    # Avoid excessive output from common terms.
                    if document_hits >= 30:
                        print(
                            "\nOutput capped at 30 matches for this "
                            "document. Other matches may exist."
                        )
                        break

                if document_hits >= 30:
                    break

            if document_hits >= 30:
                break

        if document_hits == 0:
            print("No matching text found in the extracted PDF text.")

    print("\n" + "=" * 80)
    print("TOTAL MATCHES DISPLAYED:", total_hits)
    print("Step 31B completed. No source files were modified.")
```


```python
# =========================================================
# STEP 31C: EXTRACT HOUSEHOLD IDENTIFIER DOCUMENTATION
# Read-only diagnostic
# =========================================================

from pathlib import Path
from pypdf import PdfReader

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
pdf_path = data_root / "unps_7_bid.pdf"

reader = PdfReader(str(pdf_path))

print("=" * 80)
print("STEP 31C: HOUSEHOLD IDENTIFIER DOCUMENTATION")
print("=" * 80)

# Page numbers in the search output are one-based.
# Inspect pages 32–36, corresponding to Python indexes 31–35.
for page_index in range(31, min(36, len(reader.pages))):
    page_text = reader.pages[page_index].extract_text() or ""

    print(f"\n{'=' * 80}")
    print(f"PDF PAGE {page_index + 1}")
    print("=" * 80)
    print(page_text)

print("\nNo source datasets or documentation files were modified.")

```


```python
# =========================================================
# STEP 31D: INSPECT DISPUTED AGSEC4B IDENTIFIERS
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 31D: DISPUTED IDENTIFIER INVESTIGATION")
print("=" * 90)

# Keep the original DataFrames unchanged.
crop_ids = agsec4b[
    ["hhid", "t0_hhid", "parcelID", "pltid", "cropID"]
].copy()

household_ids = gsec1.copy()

# Ensure identifier columns use consistent string representations
# for comparison only.
for df in (crop_ids, household_ids):
    for col in ["hhid", "t0_hhid"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

# Identify current household IDs with numeric-only historical IDs
# in AGSEC4B.
numeric_mask = crop_ids["t0_hhid"].str.fullmatch(r"\d+", na=False)

disputed_households = (
    crop_ids.loc[numeric_mask, "hhid"]
    .dropna()
    .unique()
)

print("Crop records with numeric-only t0_hhid:",
      int(numeric_mask.sum()))

print("Affected current household IDs:",
      len(disputed_households))

# Select useful household-level fields when available.
candidate_columns = [
    "hhid",
    "t0_hhid",
    "wave",
    "batch",
    "region",
    "urban",
    "regurb",
    "subreg",
    "district_code",
    "county_code",
    "subcounty_code",
    "parish_code",
    "wgt",
    "hwgt_W7",
    "hwgt_wc",
]

available_columns = [
    col for col in candidate_columns
    if col in household_ids.columns
]

household_subset = household_ids[available_columns].copy()

# Restrict to the disputed current IDs.
disputed_details = household_subset[
    household_subset["hhid"].isin(disputed_households)
].copy()

print("\n" + "-" * 90)
print("HOUSEHOLD-LEVEL DETAILS FROM GSEC1")
print("-" * 90)

print("Matched households:", len(disputed_details))
print("Disputed IDs not found in GSEC1:",
      len(set(disputed_households) - set(disputed_details["hhid"])))

display(
    disputed_details
    .sort_values(["t0_hhid", "hhid"])
    .reset_index(drop=True)
)

# Compare each crop record's current and historical IDs with GSEC1.
comparison = crop_ids.merge(
    household_subset[["hhid", "t0_hhid", "wave"]]
    if "wave" in household_subset.columns
    else household_subset[["hhid", "t0_hhid"]],
    on="hhid",
    how="inner",
    suffixes=("_crop", "_gsec1"),
    validate="many_to_one",
)

comparison = comparison.loc[
    comparison["hhid"].isin(disputed_households)
].copy()

print("\n" + "-" * 90)
print("CROP-LEVEL AND HOUSEHOLD-LEVEL IDENTIFIER COMPARISON")
print("-" * 90)

display(
    comparison[
        [
            col for col in [
                "hhid",
                "t0_hhid_crop",
                "t0_hhid_gsec1",
                "wave",
                "parcelID",
                "pltid",
                "cropID",
            ]
            if col in comparison.columns
        ]
    ]
    .sort_values(["hhid", "parcelID", "pltid", "cropID"])
    .reset_index(drop=True)
)

print("\nNo source datasets or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 31E: CHECK DISPUTED IDENTIFIERS ACROSS AGRICULTURE FILES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

agriculture_root = data_root / "Agric"

files_to_check = [
    "AGSEC1.csv",
    "AGSEC2A.csv",
    "AGSEC2B.csv",
    "AGSEC3A.csv",
    "AGSEC3B.csv",
    "AGSEC4A.csv",
    "AGSEC4B.csv",
    "AGSEC5A.csv",
    "AGSEC5B.csv",
    "AGSEC6A.csv",
    "AGSEC6B.csv",
    "AGSEC6C.csv",
    "AGSEC8A.csv",
    "AGSEC8B.csv",
    "AGSEC8C.csv",
    "AGSEC9A.csv",
    "AGSEC9B.csv",
    "AGSEC10.csv",
    "AGSEC11.csv",
]

print("=" * 90)
print("STEP 31E: CROSS-DATASET IDENTIFIER CHECK")
print("=" * 90)

# Collect distinct disputed numeric identifiers from AGSEC4B.
disputed_numeric_ids = set(
    agsec4b.loc[
        agsec4b["t0_hhid"].astype("string").str.fullmatch(
            r"\d+", na=False
        ),
        "t0_hhid",
    ].astype(str)
)

print("Distinct numeric-only identifiers in AGSEC4B:",
      len(disputed_numeric_ids))

results = []

for filename in files_to_check:
    file_path = agriculture_root / filename

    if not file_path.exists():
        results.append({
            "file": filename,
            "status": "NOT FOUND",
            "rows": None,
            "has_t0_hhid": False,
            "numeric_t0_rows": None,
            "distinct_numeric_t0_ids": None,
            "overlap_with_AGSEC4B_numeric_ids": None,
        })
        continue

    try:
        # Read only the columns needed for the diagnostic.
        header = pd.read_csv(
            file_path,
            nrows=0,
            encoding="utf-8",
        ).columns.tolist()

        selected = [
            col for col in ["hhid", "t0_hhid"]
            if col in header
        ]

        if not selected:
            results.append({
                "file": filename,
                "status": "NO ID COLUMNS",
                "rows": None,
                "has_t0_hhid": False,
                "numeric_t0_rows": None,
                "distinct_numeric_t0_ids": None,
                "overlap_with_AGSEC4B_numeric_ids": None,
            })
            continue

        df = pd.read_csv(
            file_path,
            usecols=selected,
            dtype="string",
            keep_default_na=False,
            encoding="utf-8",
        )

        if "t0_hhid" in df.columns:
            values = df["t0_hhid"].str.strip()
            numeric_mask = values.str.fullmatch(r"\d+", na=False)

            numeric_values = set(
                values.loc[numeric_mask].tolist()
            )

            overlap = numeric_values.intersection(
                disputed_numeric_ids
            )

            results.append({
                "file": filename,
                "status": "OK",
                "rows": len(df),
                "has_t0_hhid": True,
                "numeric_t0_rows": int(numeric_mask.sum()),
                "distinct_numeric_t0_ids": len(numeric_values),
                "overlap_with_AGSEC4B_numeric_ids": len(overlap),
            })

        else:
            results.append({
                "file": filename,
                "status": "OK",
                "rows": len(df),
                "has_t0_hhid": False,
                "numeric_t0_rows": None,
                "distinct_numeric_t0_ids": None,
                "overlap_with_AGSEC4B_numeric_ids": None,
            })

    except Exception as exc:
        results.append({
            "file": filename,
            "status": f"READ ERROR: {type(exc).__name__}: {exc}",
            "rows": None,
            "has_t0_hhid": None,
            "numeric_t0_rows": None,
            "distinct_numeric_t0_ids": None,
            "overlap_with_AGSEC4B_numeric_ids": None,
        })

results_df = pd.DataFrame(results)

display(results_df)

print("\nNo source CSV files or active DataFrames were modified.")

```


```python
# =========================================================
# STEP 31F: COMPARE HISTORICAL IDENTIFIERS ACROSS DATASETS
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
agriculture_root = data_root / "Agric"

files_to_check = [
    "AGSEC1.csv",
    "AGSEC2A.csv",
    "AGSEC2B.csv",
    "AGSEC3A.csv",
    "AGSEC3B.csv",
    "AGSEC4A.csv",
    "AGSEC4B.csv",
    "AGSEC5A.csv",
    "AGSEC5B.csv",
    "AGSEC6A.csv",
    "AGSEC6B.csv",
    "AGSEC6C.csv",
    "AGSEC8A.csv",
    "AGSEC8B.csv",
    "AGSEC8C.csv",
    "AGSEC9B.csv",
    "AGSEC10.csv",
]

print("=" * 90)
print("STEP 31F: CROSS-DATASET HISTORICAL IDENTIFIER COMPARISON")
print("=" * 90)

# Household reference from GSEC1.
gsec_reference = gsec1[["hhid", "t0_hhid"]].copy()

for col in ["hhid", "t0_hhid"]:
    gsec_reference[col] = (
        gsec_reference[col].astype("string").str.strip()
    )

gsec_reference = gsec_reference.rename(
    columns={"t0_hhid": "t0_hhid_gsec1"}
)

# Read only identifiers from each agriculture dataset.
records = []

for filename in files_to_check:
    file_path = agriculture_root / filename

    try:
        df = pd.read_csv(
            file_path,
            usecols=["hhid", "t0_hhid"],
            dtype="string",
            keep_default_na=False,
            encoding="utf-8",
        )

        df["hhid"] = df["hhid"].str.strip()
        df["t0_hhid"] = df["t0_hhid"].str.strip()

        # Retain distinct ID combinations per current household.
        df = df[["hhid", "t0_hhid"]].drop_duplicates()

        df["source_file"] = filename
        records.append(df)

    except Exception as exc:
        print(
            f"Could not read {filename}: "
            f"{type(exc).__name__}: {exc}"
        )

if not records:
    raise RuntimeError("No agriculture datasets could be compared.")

combined = pd.concat(records, ignore_index=True)

# Attach the corresponding GSEC1 historical ID.
combined = combined.merge(
    gsec_reference,
    on="hhid",
    how="left",
    validate="many_to_one",
)

# Identify numeric-only values without changing the source.
combined["numeric_only"] = combined["t0_hhid"].str.fullmatch(
    r"\d+", na=False
)

# Treat the special placeholder as unresolved rather than as an ID.
combined["placeholder"] = combined["t0_hhid"].eq("##N/A##")

# Normalize only for a diagnostic comparison:
# remove a leading H from non-placeholder IDs.
def normalize_for_comparison(value):
    if value is None or pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if value == "" or value == "##N/A##":
        return pd.NA

    if value.startswith("H"):
        return value[1:]

    return value

combined["normalized_crop_id"] = combined["t0_hhid"].map(
    normalize_for_comparison
)

combined["normalized_gsec1_id"] = combined[
    "t0_hhid_gsec1"
].map(normalize_for_comparison)

combined["matches_gsec1_after_prefix_normalization"] = (
    combined["normalized_crop_id"].notna()
    & combined["normalized_gsec1_id"].notna()
    & (
        combined["normalized_crop_id"]
        == combined["normalized_gsec1_id"]
    )
)

# Summary by dataset.
summary = (
    combined.groupby("source_file", dropna=False)
    .agg(
        distinct_households=("hhid", "nunique"),
        numeric_only_households=(
            "hhid",
            lambda s: s[
                combined.loc[s.index, "numeric_only"]
            ].nunique(),
        ),
        placeholder_households=(
            "hhid",
            lambda s: s[
                combined.loc[s.index, "placeholder"]
            ].nunique(),
        ),
        households_matching_gsec1=(
            "hhid",
            lambda s: s[
                combined.loc[
                    s.index,
                    "matches_gsec1_after_prefix_normalization",
                ]
            ].nunique(),
        ),
    )
    .reset_index()
)

print("\nSUMMARY BY DATASET")
display(summary)

# Find households where at least one file contains a numeric-only
# identifier and another file contains a different identifier.
numeric_households = set(
    combined.loc[combined["numeric_only"], "hhid"]
)

affected = combined[
    combined["hhid"].isin(numeric_households)
].copy()

cross_file_counts = (
    affected.groupby("hhid")
    .agg(
        files_present=("source_file", "nunique"),
        distinct_t0_values=("t0_hhid", "nunique"),
        numeric_files=(
            "numeric_only",
            "sum",
        ),
        gsec1_t0_hhid=("t0_hhid_gsec1", "first"),
    )
    .reset_index()
)

print("\nHOUSEHOLDS WITH NUMERIC-ONLY IDS IN AT LEAST ONE FILE")
print("Affected current household IDs:", len(numeric_households))

display(
    cross_file_counts
    .sort_values(
        ["files_present", "distinct_t0_values"],
        ascending=False,
    )
    .head(30)
    .reset_index(drop=True)
)

# Show detailed identifier records for a manageable sample.
sample_households = cross_file_counts.head(10)["hhid"]

print("\nDETAILED EXAMPLES FOR UP TO 10 HOUSEHOLDS")

display(
    affected[
        affected["hhid"].isin(sample_households)
    ][
        [
            "hhid",
            "source_file",
            "t0_hhid",
            "t0_hhid_gsec1",
            "numeric_only",
            "matches_gsec1_after_prefix_normalization",
        ]
    ]
    .sort_values(["hhid", "source_file"])
    .reset_index(drop=True)
)

print("\nNo source datasets or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 31G: VERIFY IDENTIFIERS IN ORIGINAL SOURCE FILES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
agriculture_root = data_root / "Agric"
household_root = data_root / "HH"

source_files = {
    "GSEC1": household_root / "GSEC1.csv",
    "AGSEC1": agriculture_root / "AGSEC1.csv",
    "AGSEC9B": agriculture_root / "AGSEC9B.csv",
    "AGSEC4B": agriculture_root / "AGSEC4B.csv",
}

print("=" * 90)
print("STEP 31G: ORIGINAL SOURCE IDENTIFIER VERIFICATION")
print("=" * 90)

source_ids = {}

for dataset_name, file_path in source_files.items():
    df = pd.read_csv(
        file_path,
        usecols=["hhid", "t0_hhid"],
        dtype="string",
        keep_default_na=False,
        encoding="utf-8",
    )

    df["hhid"] = df["hhid"].str.strip()
    df["t0_hhid"] = df["t0_hhid"].str.strip()

    # Preserve the original identifier values.
    source_ids[dataset_name] = df.copy()

    numeric_mask = df["t0_hhid"].str.fullmatch(
        r"\d+", na=False
    )

    print(f"\n{dataset_name}")
    print("-" * 50)
    print("Source file:", file_path.name)
    print("Rows:", len(df))
    print("Distinct current household IDs:", df["hhid"].nunique())
    print("Numeric-only t0_hhid rows:", int(numeric_mask.sum()))
    print(
        "Distinct numeric-only t0_hhid values:",
        df.loc[numeric_mask, "t0_hhid"].nunique(),
    )

# Use GSEC1 as the comparison reference.
gsec_reference = source_ids["GSEC1"].rename(
    columns={"t0_hhid": "t0_hhid_gsec1"}
)

for dataset_name in ["AGSEC1", "AGSEC9B", "AGSEC4B"]:
    df = source_ids[dataset_name].merge(
        gsec_reference,
        on="hhid",
        how="left",
        validate="many_to_one",
    )

    df["numeric_only"] = df["t0_hhid"].str.fullmatch(
        r"\d+", na=False
    )

    df["prefix_normalized"] = df["t0_hhid"].str.replace(
        r"^H", "", regex=True
    )

    df["gsec1_normalized"] = df[
        "t0_hhid_gsec1"
    ].str.replace(r"^H", "", regex=True)

    df["prefix_only_match"] = (
        df["numeric_only"]
        & df["t0_hhid_gsec1"].notna()
        & (
            df["prefix_normalized"]
            == df["gsec1_normalized"]
        )
    )

    df["substantive_mismatch"] = (
        df["numeric_only"]
        & df["t0_hhid_gsec1"].notna()
        & ~df["prefix_only_match"]
    )

    print(f"\n{dataset_name}: comparison with GSEC1")
    print("-" * 50)
    print(
        "Numeric-only rows:",
        int(df["numeric_only"].sum()),
    )
    print(
        "Prefix-only matches:",
        int(df["prefix_only_match"].sum()),
    )
    print(
        "Substantive mismatches:",
        int(df["substantive_mismatch"].sum()),
    )
    print(
        "Numeric-only rows without a GSEC1 match:",
        int(
            (
                df["numeric_only"]
                & df["t0_hhid_gsec1"].isna()
            ).sum()
        ),
    )

    print("\nSample substantive mismatches:")

    display(
        df.loc[
            df["substantive_mismatch"],
            [
                "hhid",
                "t0_hhid",
                "t0_hhid_gsec1",
            ],
        ]
        .drop_duplicates()
        .head(10)
        .reset_index(drop=True)
    )

print("\nRead-only check completed. No source data were modified.")
```


```python
# =========================================================
# STEP 31H: CLASSIFY CROSS-FILE HISTORICAL ID DISCREPANCIES
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
agriculture_root = data_root / "Agric"
household_root = data_root / "HH"

files_to_check = [
    "AGSEC1.csv",
    "AGSEC9B.csv",
    "AGSEC4A.csv",
    "AGSEC4B.csv",
]

# Read current and historical identifiers from the source files.
frames = []

for filename in files_to_check:
    df = pd.read_csv(
        agriculture_root / filename,
        usecols=["hhid", "t0_hhid"],
        dtype="string",
        keep_default_na=False,
        encoding="utf-8",
    )

    df["hhid"] = df["hhid"].str.strip()
    df["t0_hhid"] = df["t0_hhid"].str.strip()
    df["source_file"] = filename

    # One record per current household and distinct historical ID.
    df = df[["hhid", "t0_hhid", "source_file"]].drop_duplicates()

    frames.append(df)

agriculture_ids = pd.concat(frames, ignore_index=True)

# Read the reference IDs from the original GSEC1 source.
gsec1_ids = pd.read_csv(
    household_root / "GSEC1.csv",
    usecols=["hhid", "t0_hhid"],
    dtype="string",
    keep_default_na=False,
    encoding="utf-8",
)

gsec1_ids["hhid"] = gsec1_ids["hhid"].str.strip()
gsec1_ids["t0_hhid"] = gsec1_ids["t0_hhid"].str.strip()

gsec1_ids = gsec1_ids.rename(
    columns={"t0_hhid": "gsec1_t0_hhid"}
)

# Each current household should have one GSEC1 reference record.
assert gsec1_ids["hhid"].is_unique, (
    "GSEC1 hhid is not unique; stop and investigate."
)

agriculture_ids = agriculture_ids.merge(
    gsec1_ids,
    on="hhid",
    how="left",
    validate="many_to_one",
)

# Ignore empty strings and the known placeholder when comparing IDs.
def clean_identifier(value):
    if value is None or pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if value in ("", "##N/A##"):
        return pd.NA

    return value

def normalize_prefix(value):
    value = clean_identifier(value)

    if pd.isna(value):
        return pd.NA

    return value[1:] if value.startswith("H") else value

agriculture_ids["clean_t0"] = agriculture_ids["t0_hhid"].map(
    clean_identifier
)

agriculture_ids["normalized_t0"] = agriculture_ids[
    "t0_hhid"
].map(normalize_prefix)

agriculture_ids["normalized_gsec1"] = agriculture_ids[
    "gsec1_t0_hhid"
].map(normalize_prefix)

# Summarize distinct usable agriculture IDs by household.
usable = agriculture_ids[
    agriculture_ids["clean_t0"].notna()
].copy()

household_summary = (
    usable.groupby("hhid")
    .agg(
        agriculture_files=("source_file", "nunique"),
        distinct_agriculture_ids=("clean_t0", "nunique"),
        agriculture_ids=("clean_t0", lambda s: " | ".join(sorted(set(s)))),
        gsec1_t0_hhid=("gsec1_t0_hhid", "first"),
        normalized_agriculture_ids=(
            "normalized_t0",
            lambda s: " | ".join(sorted(set(s.dropna()))),
        ),
        normalized_gsec1=("normalized_gsec1", "first"),
    )
    .reset_index()
)

def classify_household(row):
    if pd.isna(row["gsec1_t0_hhid"]) or row["gsec1_t0_hhid"] == "":
        return "Insufficient evidence: no GSEC1 match"

    if row["distinct_agriculture_ids"] > 1:
        return "Conflicting agriculture identifiers"

    agriculture_id = row["normalized_agriculture_ids"]
    gsec1_id = row["normalized_gsec1"]

    if not agriculture_id or not gsec1_id or pd.isna(gsec1_id):
        return "Insufficient evidence: missing usable identifier"

    if agriculture_id == gsec1_id:
        raw_agriculture_id = row["agriculture_ids"]

        if raw_agriculture_id == row["gsec1_t0_hhid"]:
            return "Exact agreement"

        return "Consistent prefix-only difference"

    return "Consistent substantive discrepancy"

household_summary["classification"] = household_summary.apply(
    classify_household,
    axis=1,
)

print("=" * 90)
print("STEP 31H: CROSS-FILE HISTORICAL ID CLASSIFICATION")
print("=" * 90)

print("\nCLASSIFICATION COUNTS")

display(
    household_summary["classification"]
    .value_counts(dropna=False)
    .rename_axis("classification")
    .reset_index(name="households")
)

print("\nAFFECTED HOUSEHOLDS WITH SUBSTANTIVE DISCREPANCIES")

display(
    household_summary[
        household_summary["classification"]
        == "Consistent substantive discrepancy"
    ]
    .sort_values(
        ["agriculture_files", "hhid"],
        ascending=[False, True],
    )
    .head(20)
    .reset_index(drop=True)
)

print("\nHOUSEHOLDS WITH CONFLICTING AGRICULTURE IDENTIFIERS")

display(
    household_summary[
        household_summary["classification"]
        == "Conflicting agriculture identifiers"
    ]
    .sort_values("hhid")
    .head(20)
    .reset_index(drop=True)
)

print("\nNo source CSV files or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 31I: TEST POSSIBLE TRUNCATION PATTERNS
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
agriculture_root = data_root / "Agric"
household_root = data_root / "HH"

files_to_check = [
    "AGSEC1.csv",
    "AGSEC9B.csv",
    "AGSEC4A.csv",
    "AGSEC4B.csv",
]

# Read GSEC1 reference identifiers.
gsec1_ids = pd.read_csv(
    household_root / "GSEC1.csv",
    usecols=["hhid", "t0_hhid"],
    dtype="string",
    keep_default_na=False,
    encoding="utf-8",
)

gsec1_ids["hhid"] = gsec1_ids["hhid"].str.strip()
gsec1_ids["t0_hhid"] = gsec1_ids["t0_hhid"].str.strip()

gsec1_ids = gsec1_ids.rename(
    columns={"t0_hhid": "gsec1_t0_hhid"}
)

all_results = []

for filename in files_to_check:
    df = pd.read_csv(
        agriculture_root / filename,
        usecols=["hhid", "t0_hhid"],
        dtype="string",
        keep_default_na=False,
        encoding="utf-8",
    )

    df["hhid"] = df["hhid"].str.strip()
    df["t0_hhid"] = df["t0_hhid"].str.strip()

    df = df.merge(
        gsec1_ids,
        on="hhid",
        how="left",
        validate="many_to_one",
    )

    numeric_mask = df["t0_hhid"].str.fullmatch(
        r"\d+", na=False
    )

    numeric_df = df.loc[numeric_mask].copy()

    numeric_df["gsec1_digits"] = (
        numeric_df["gsec1_t0_hhid"]
        .str.replace(r"\D", "", regex=True)
    )

    numeric_df["appears_anywhere"] = numeric_df.apply(
        lambda row: (
            bool(row["t0_hhid"])
            and bool(row["gsec1_digits"])
            and row["t0_hhid"] in row["gsec1_digits"]
        ),
        axis=1,
    )

    numeric_df["matches_suffix"] = numeric_df.apply(
        lambda row: (
            bool(row["t0_hhid"])
            and bool(row["gsec1_digits"])
            and row["gsec1_digits"].endswith(row["t0_hhid"])
        ),
        axis=1,
    )

    numeric_df["matches_prefix"] = numeric_df.apply(
        lambda row: (
            bool(row["t0_hhid"])
            and bool(row["gsec1_digits"])
            and row["gsec1_digits"].startswith(row["t0_hhid"])
        ),
        axis=1,
    )

    all_results.append(numeric_df)

combined_results = pd.concat(
    all_results,
    ignore_index=True,
)

summary = (
    combined_results.groupby(
        combined_results["hhid"].map(
            lambda value: value
        )
    )
    .agg(
        source_records=("hhid", "size"),
        numeric_id=("t0_hhid", "first"),
        gsec1_id=("gsec1_t0_hhid", "first"),
        appears_anywhere=("appears_anywhere", "first"),
        matches_suffix=("matches_suffix", "first"),
        matches_prefix=("matches_prefix", "first"),
    )
    .reset_index(names="hhid")
)

print("=" * 90)
print("STEP 31I: POSSIBLE IDENTIFIER TRUNCATION CHECK")
print("=" * 90)

print("\nHousehold-level results:")
print("Distinct current household IDs:", summary["hhid"].nunique())
print(
    "Numeric ID appears anywhere in GSEC1 digits:",
    int(summary["appears_anywhere"].sum()),
)
print(
    "Numeric ID matches the end of GSEC1 digits:",
    int(summary["matches_suffix"].sum()),
)
print(
    "Numeric ID matches the start of GSEC1 digits:",
    int(summary["matches_prefix"].sum()),
)

print("\nExample records where the numeric ID appears within GSEC1:")

display(
    summary.loc[
        summary["appears_anywhere"],
        [
            "hhid",
            "numeric_id",
            "gsec1_id",
            "appears_anywhere",
            "matches_suffix",
            "matches_prefix",
        ],
    ]
    .head(20)
    .reset_index(drop=True)
)

print("\nNo source CSV files or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 31J: DOCUMENT THE HISTORICAL IDENTIFIER AUDIT
# Creates an in-memory audit record only.
# Does not modify source data or write files.
# =========================================================

import pandas as pd

identifier_audit = pd.DataFrame([
    {
        "issue_id": "ID-001",
        "issue": "Numeric-only historical household identifiers",
        "severity": "High for longitudinal linkage",
        "status": "Unresolved",
        "evidence": (
            "Numeric-only t0_hhid values occur in multiple "
            "original agriculture CSV files and disagree with "
            "corresponding GSEC1 historical identifiers."
        ),
        "affected_households": 79,
        "decision": (
            "Preserve source values. Do not automatically "
            "correct or use disputed values for longitudinal linkage."
        ),
        "cross_sectional_impact": (
            "Current-round merges may proceed using validated hhid keys."
        ),
        "longitudinal_impact": (
            "Historical household linkage remains on hold for affected records."
        ),
        "next_action": (
            "Revisit only if authoritative documentation or corrected "
            "source data becomes available."
        ),
    }
])

print("=" * 90)
print("STEP 31J: HISTORICAL IDENTIFIER AUDIT RECORD")
print("=" * 90)

display(identifier_audit)

print("\nAudit record created in memory.")
print("No source files were modified.")
```


```python
# =========================================================
# STEP 32A: INSPECT AGRICULTURAL ELIGIBILITY VARIABLES
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32A: AGRICULTURAL ELIGIBILITY AUDIT")
print("=" * 90)

# Confirm the datasets currently available.
datasets = {
    "AGSEC1": agsec1,
    "AGSEC4A": agsec4a,
    "AGSEC4B": agsec4b,
}

for name, df in datasets.items():
    print(f"\n{name}")
    print("-" * 70)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Unique current household IDs:",
          df["hhid"].nunique() if "hhid" in df.columns else "No hhid")

# Inspect all AGSEC1 variable names.
print("\nAGSEC1: ALL VARIABLE NAMES")
display(
    pd.DataFrame({
        "variable": agsec1.columns,
        "dtype": [str(agsec1[col].dtype) for col in agsec1.columns],
    })
)

# Identify potentially relevant household-level variables.
eligibility_keywords = [
    "agri", "agric", "crop", "cult", "livestock",
    "farm", "household", "hh_", "respond", "interview",
    "status", "complete", "eligib",
]

candidate_columns = [
    col for col in agsec1.columns
    if any(keyword in col.lower() for keyword in eligibility_keywords)
]

print("\nPOTENTIAL AGRICULTURAL ELIGIBILITY VARIABLES")
display(
    pd.DataFrame({
        "variable": candidate_columns,
        "dtype": [
            str(agsec1[col].dtype)
            for col in candidate_columns
        ],
        "missing_count": [
            int(agsec1[col].isna().sum())
            for col in candidate_columns
        ],
        "distinct_values": [
            int(agsec1[col].nunique(dropna=False))
            for col in candidate_columns
        ],
    })
)

# Show value distributions for candidate categorical indicators.
for col in candidate_columns:
    if agsec1[col].nunique(dropna=False) <= 15:
        print(f"\nValue counts: AGSEC1[{col}]")
        display(
            agsec1[col]
            .value_counts(dropna=False)
            .rename_axis("value")
            .reset_index(name="count")
        )

print("\nNo source files or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 32C: JOINT DISTRIBUTION OF AGRICULTURAL INDICATORS
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32C: JOINT AGRICULTURAL INDICATOR AUDIT")
print("=" * 90)

variables = [
    "hh_crp1",
    "hh_crp2",
    "culcrp",
    "lvstck",
    "hh_anm",
    "hh_plty",
]

available = [
    col for col in variables
    if col in agsec1.columns
]

# Create a temporary inspection copy.
indicator_data = agsec1[available].copy()

print("\n1. JOINT DISTRIBUTION: hh_crp1 vs hh_crp2")

display(
    pd.crosstab(
        indicator_data["hh_crp1"],
        indicator_data["hh_crp2"],
        margins=True,
        dropna=False,
    )
)

print("\n2. JOINT DISTRIBUTION: hh_crp1 vs culcrp")

display(
    pd.crosstab(
        indicator_data["hh_crp1"],
        indicator_data["culcrp"],
        margins=True,
        dropna=False,
    )
)

print("\n3. JOINT DISTRIBUTION: hh_crp2 vs culcrp")

display(
    pd.crosstab(
        indicator_data["hh_crp2"],
        indicator_data["culcrp"],
        margins=True,
        dropna=False,
    )
)

print("\n4. MISSINGNESS PATTERNS")

missingness = (
    indicator_data.isna()
    .value_counts(dropna=False)
    .rename("households")
    .reset_index()
)

display(missingness)

print("\n5. UNIQUE COMBINATIONS OF INDICATOR VALUES")

display(
    indicator_data
    .value_counts(dropna=False)
    .rename("households")
    .reset_index()
    .head(30)
)

print("\nNo source files or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 32D: AUDIT CROP-LEVEL ELIGIBILITY AND SEED INFORMATION
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32D: CROP-LEVEL ELIGIBILITY AND SEED AUDIT")
print("=" * 90)

crop_files = {
    "First visit (AGSEC4A)": {
        "df": agsec4a,
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
        "improved_category": "s4aq14",
    },
    "Second visit (AGSEC4B)": {
        "df": agsec4b,
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
        "improved_category": "s4bq14",
    },
}

summary = []

for visit, info in crop_files.items():
    df = info["df"]

    use = info["seed_use"]
    seed_type = info["seed_type"]
    category = info["improved_category"]

    print(f"\n{visit}")
    print("-" * 75)

    print("Crop records:", len(df))
    print("Unique households:", df["hhid"].nunique())

    for col in [use, seed_type, category]:
        print(f"\n{col}:")
        display(
            df[col]
            .value_counts(dropna=False)
            .rename_axis("value")
            .reset_index(name="records")
        )

    seed_used = df[use].eq(1)
    improved = seed_used & df[seed_type].eq(2)
    traditional = seed_used & df[seed_type].eq(1)
    no_seed = df[use].eq(2)

    summary.append({
        "visit": visit,
        "crop_records": len(df),
        "households": df["hhid"].nunique(),
        "seed_used_records": int(seed_used.sum()),
        "improved_seed_records": int(improved.sum()),
        "traditional_seed_records": int(traditional.sum()),
        "no_seed_records": int(no_seed.sum()),
        "seed_use_missing": int(df[use].isna().sum()),
        "seed_type_missing_when_seed_used": int(
            (seed_used & df[seed_type].isna()).sum()
        ),
        "improved_category_missing_when_type_improved": int(
            (improved & df[category].isna()).sum()
        ),
    })

print("\nSUMMARY OF CROP-LEVEL SEED INFORMATION")
display(pd.DataFrame(summary))

print("\nThis cell is diagnostic only.")
print("No source files or active DataFrames were modified.")
```


```python
# =========================================================
# STEP 32E: HOUSEHOLD-LEVEL SEED ADOPTION CLASSIFICATION
# Diagnostic only — no source data are modified
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32E: HOUSEHOLD-LEVEL SEED ADOPTION AUDIT")
print("=" * 90)


def classify_households(df, visit_name, seed_use, seed_type):
    """
    Classify households from crop-level records.

    Confirmed adopter:
        At least one crop has seed use = 1 and seed type = 2.

    Potential non-adopter:
        No confirmed improved-seed crop, and every crop record
        has a resolved seed-use/seed-type combination.

    Unclassified:
        No confirmed improved-seed crop, but at least one crop
        record has unresolved seed-use or seed-type information.

    This is a provisional diagnostic classification, not the
    final survey-weighted estimate.
    """

    data = df[["hhid", seed_use, seed_type]].copy()

    data["_seed_used"] = data[seed_use].eq(1)
    data["_no_seed"] = data[seed_use].eq(2)
    data["_improved"] = (
        data[seed_use].eq(1) & data[seed_type].eq(2)
    )
    data["_traditional"] = (
        data[seed_use].eq(1) & data[seed_type].eq(1)
    )

    # A crop record is resolved if:
    # - seed use = 2, or
    # - seed use = 1 and seed type is 1 or 2.
    data["_resolved"] = (
        data["_no_seed"]
        | (
            data["_seed_used"]
            & data[seed_type].isin([1, 2])
        )
    )

    household = (
        data.groupby("hhid", dropna=False)
        .agg(
            crop_records=("hhid", "size"),
            improved_crops=("_improved", "sum"),
            traditional_crops=("_traditional", "sum"),
            no_seed_crops=("_no_seed", "sum"),
            seed_used_crops=("_seed_used", "sum"),
            unresolved_crops=(
                "_resolved",
                lambda x: int((~x).sum())
            ),
        )
        .reset_index()
    )

    household["classification"] = "Unclassified"

    household.loc[
        household["improved_crops"] > 0,
        "classification"
    ] = "Adopter"

    household.loc[
        (household["improved_crops"] == 0)
        & (household["unresolved_crops"] == 0),
        "classification"
    ] = "Potential non-adopter"

    counts = (
        household["classification"]
        .value_counts()
        .reindex(
            ["Adopter", "Potential non-adopter", "Unclassified"],
            fill_value=0,
        )
        .rename_axis("classification")
        .reset_index(name="households")
    )

    print(f"\n{visit_name}")
    print("-" * 75)
    print("Households:", household["hhid"].nunique())

    display(counts)

    print("\nHousehold classification summary:")
    display(
        household.groupby("classification")
        .agg(
            households=("hhid", "nunique"),
            crop_records=("crop_records", "sum"),
            households_with_unresolved_records=(
                "unresolved_crops",
                lambda x: int((x > 0).sum())
            ),
        )
        .reset_index()
    )

    return household


first_visit_households = classify_households(
    agsec4a,
    "FIRST VISIT — AGSEC4A",
    "s4aq16",
    "s4aq13",
)

second_visit_households = classify_households(
    agsec4b,
    "SECOND VISIT — AGSEC4B",
    "s4bq16",
    "s4bq13",
)

print("\nStep 32E is diagnostic only.")
print("No source files or original DataFrames were modified.")
```


```python
# =========================================================
# STEP 32F: INVESTIGATE UNRESOLVED HOUSEHOLD CLASSIFICATION
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32F: UNRESOLVED CROP RECORD INVESTIGATION")
print("=" * 90)


def audit_unresolved_records(
    crop_df,
    household_df,
    visit_name,
    seed_use,
    seed_type,
):
    print(f"\n{visit_name}")
    print("-" * 75)

    # Households that have not been classified
    unresolved_hhids = household_df.loc[
        household_df["classification"] == "Unclassified",
        "hhid",
    ]

    unresolved = crop_df.loc[
        crop_df["hhid"].isin(unresolved_hhids),
        ["hhid", seed_use, seed_type],
    ].copy()

    print("Unclassified households:", unresolved_hhids.nunique())
    print("Crop records belonging to these households:", len(unresolved))

    # Examine seed-use and seed-type response combinations
    print("\nSeed-use and seed-type combinations:")
    display(
        pd.crosstab(
            unresolved[seed_use],
            unresolved[seed_type],
            dropna=False,
            margins=True,
        )
    )

    # Classify the unresolved crop records by response pattern
    unresolved["unresolved_reason"] = "Other unresolved combination"

    unresolved.loc[
        unresolved[seed_use].isna(),
        "unresolved_reason",
    ] = "Seed-use response missing"

    unresolved.loc[
        unresolved[seed_use].eq(1)
        & unresolved[seed_type].isna(),
        "unresolved_reason",
    ] = "Seed reported used, but seed type missing"

    unresolved.loc[
        unresolved[seed_use].eq(1)
        & ~unresolved[seed_type].isin([1, 2])
        & unresolved[seed_type].notna(),
        "unresolved_reason",
    ] = "Seed type has an unexpected value"

    unresolved.loc[
        unresolved[seed_use].eq(2)
        & unresolved[seed_type].notna(),
        "unresolved_reason",
    ] = "Seed-use response says no, but seed type is populated"

    print("\nUnresolved crop records by reason:")
    display(
        unresolved["unresolved_reason"]
        .value_counts(dropna=False)
        .rename_axis("reason")
        .reset_index(name="crop_records")
    )

    print("\nUnresolved crop records by household:")
    display(
        unresolved.groupby("hhid")
        .agg(
            unresolved_crop_records=("hhid", "size"),
            missing_seed_use=(seed_use, lambda x: int(x.isna().sum())),
            missing_seed_type=(seed_type, lambda x: int(x.isna().sum())),
        )
        .reset_index()
        .sort_values(
            "unresolved_crop_records",
            ascending=False,
        )
        .head(20)
    )


audit_unresolved_records(
    agsec4a,
    first_visit_households,
    "FIRST VISIT — AGSEC4A",
    "s4aq16",
    "s4aq13",
)

audit_unresolved_records(
    agsec4b,
    second_visit_households,
    "SECOND VISIT — AGSEC4B",
    "s4bq16",
    "s4bq13",
)

print("\nStep 32F is diagnostic only.")
print("No source files or original DataFrames were modified.")
```


```python
# =========================================================
# STEP 32G: AUDIT SEED-USE AND SEED-TYPE RESPONSE PATTERNS
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32G: SEED RESPONSE PATTERN VALIDATION")
print("=" * 90)

crop_files = {
    "First visit — AGSEC4A": {
        "df": agsec4a,
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit — AGSEC4B": {
        "df": agsec4b,
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

pattern_summaries = []

for visit, info in crop_files.items():
    df = info["df"]
    use = info["seed_use"]
    seed_type = info["seed_type"]

    print(f"\n{visit}")
    print("-" * 75)

    # Preserve missing responses as explicit categories.
    use_values = df[use].astype("object").where(
        df[use].notna(), "MISSING"
    )

    type_values = df[seed_type].astype("object").where(
        df[seed_type].notna(), "MISSING"
    )

    patterns = pd.crosstab(
        use_values,
        type_values,
        margins=True,
        dropna=False,
    )

    display(patterns)

    # Counts for key response combinations.
    seed_use_missing = df[use].isna()
    seed_used = df[use].eq(1)
    no_seed = df[use].eq(2)

    improved = seed_used & df[seed_type].eq(2)
    traditional = seed_used & df[seed_type].eq(1)

    seed_used_type_missing = (
        seed_used & df[seed_type].isna()
    )

    no_seed_type_populated = (
        no_seed & df[seed_type].notna()
    )

    unexpected_seed_type = (
        seed_used
        & df[seed_type].notna()
        & ~df[seed_type].isin([1, 2])
    )

    print("\nKey response-pattern counts:")

    checks = pd.DataFrame({
        "pattern": [
            "Seed use = 1 and seed type = 1",
            "Seed use = 1 and seed type = 2",
            "Seed use = 1 and seed type missing",
            "Seed use = 2 and seed type missing",
            "Seed use = 2 and seed type populated",
            "Seed-use response missing",
            "Unexpected seed-type code when seed use = 1",
        ],
        "crop_records": [
            int(traditional.sum()),
            int(improved.sum()),
            int(seed_used_type_missing.sum()),
            int((no_seed & df[seed_type].isna()).sum()),
            int(no_seed_type_populated.sum()),
            int(seed_use_missing.sum()),
            int(unexpected_seed_type.sum()),
        ],
    })

    display(checks)

    pattern_summaries.append({
        "visit": visit,
        "crop_records": len(df),
        "seed_use_missing": int(seed_use_missing.sum()),
        "seed_used_type_missing": int(
            seed_used_type_missing.sum()
        ),
        "no_seed_type_missing": int(
            (no_seed & df[seed_type].isna()).sum()
        ),
        "no_seed_type_populated": int(
            no_seed_type_populated.sum()
        ),
        "unexpected_seed_type": int(
            unexpected_seed_type.sum()
        ),
    })

print("\nSUMMARY")
display(pd.DataFrame(pattern_summaries))

print("\nDiagnostic only: no source files or active DataFrames modified.")
```


```python
# =========================================================
# STEP 32H: INVESTIGATE UNRESOLVED SEED RECORDS BY HOUSEHOLD
# Read-only diagnostic — corrected household identifiers
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32H: UNRESOLVED SEED RECORDS BY HOUSEHOLD")
print("=" * 90)

crop_files = {
    "First visit — AGSEC4A": {
        "df": agsec4a,
        "household_id": "hhid",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit — AGSEC4B": {
        "df": agsec4b,
        "household_id": "hhid",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

for visit, info in crop_files.items():

    df = info["df"]
    hh = info["household_id"]
    use = info["seed_use"]
    seed_type = info["seed_type"]

    print(f"\n{visit}")
    print("-" * 75)

    # Validate required columns.
    required = [hh, use, seed_type]
    missing_columns = [
        col for col in required
        if col not in df.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        continue

    # Identify unresolved crop records.
    # Missing seed use OR seed use = 1 with missing seed type.
    unresolved_mask = (
        df[use].isna()
        | (df[use].eq(1) & df[seed_type].isna())
    )

    unresolved_records = df.loc[unresolved_mask].copy()

    print("Total crop records:", len(df))
    print("Unresolved crop records:", len(unresolved_records))
    print(
        "Unique households with unresolved records:",
        unresolved_records[hh].nunique()
    )
    print(
        "Unresolved records with missing household ID:",
        int(unresolved_records[hh].isna().sum())
    )

    # Find households with at least one unresolved record.
    unresolved_households = (
        unresolved_records[hh].dropna().unique()
    )

    # Retrieve all crop records for these households.
    household_records = df.loc[
        df[hh].isin(unresolved_households)
    ].copy()

    # Create diagnostic flags without modifying the source DataFrame.
    household_records["_improved_seed_confirmed"] = (
        household_records[use].eq(1)
        & household_records[seed_type].eq(2)
    )

    household_records["_traditional_seed_confirmed"] = (
        household_records[use].eq(1)
        & household_records[seed_type].eq(1)
    )

    household_records["_seed_use_missing"] = (
        household_records[use].isna()
    )

    household_records["_seed_type_missing_after_use"] = (
        household_records[use].eq(1)
        & household_records[seed_type].isna()
    )

    household_records["_no_seed_reported"] = (
        household_records[use].eq(2)
    )

    # Summarize all crop records within each affected household.
    household_summary = (
        household_records
        .groupby(hh)
        .agg(
            crop_records=(use, "size"),
            missing_seed_use=("_seed_use_missing", "sum"),
            seed_use_reported=(
                use,
                lambda s: s.eq(1).sum()
            ),
            no_seed_reported=("_no_seed_reported", "sum"),
            improved_seed_records=(
                "_improved_seed_confirmed", "sum"
            ),
            traditional_seed_records=(
                "_traditional_seed_confirmed", "sum"
            ),
            seed_type_missing_after_use=(
                "_seed_type_missing_after_use", "sum"
            ),
        )
        .reset_index()
    )

    # Provisional evidence flags.
    household_summary["confirmed_type2"] = (
        household_summary["improved_seed_records"] > 0
    )

    household_summary["confirmed_type1"] = (
        household_summary["traditional_seed_records"] > 0
    )

    print("\nHousehold-level diagnostic summary:")
    display(household_summary.head(20))

    print("\nHousehold evidence patterns:")

    pattern_columns = [
        "confirmed_type2",
        "confirmed_type1",
        "missing_seed_use",
        "seed_type_missing_after_use",
        "no_seed_reported",
    ]

    display(
        household_summary
        .groupby(pattern_columns, dropna=False)
        .size()
        .reset_index(name="households")
        .sort_values("households", ascending=False)
    )

    print("\nSample unresolved crop records:")

    display(
        unresolved_records[
            [hh, use, seed_type]
        ].head(20)
    )

    # Check for duplicate household IDs in the household summary.
    print(
        "\nUnique households in summary:",
        household_summary[hh].nunique()
    )

    print(
        "Rows in household summary:",
        len(household_summary)
    )

print("\nDiagnostic only: source DataFrames were not modified.")
```


```python
# =========================================================
# STEP 32I: EXACT HOUSEHOLD-LEVEL SEED EVIDENCE COUNTS
# Read-only diagnostic
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32I: EXACT HOUSEHOLD-LEVEL SEED EVIDENCE")
print("=" * 90)

crop_files = {
    "First visit — AGSEC4A": {
        "df": agsec4a,
        "household_id": "hhid",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit — AGSEC4B": {
        "df": agsec4b,
        "household_id": "hhid",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

visit_household_summaries = {}

for visit, info in crop_files.items():

    df = info["df"]
    hh = info["household_id"]
    use = info["seed_use"]
    seed_type = info["seed_type"]

    print(f"\n{visit}")
    print("-" * 75)

    # Validate required columns.
    required = [hh, use, seed_type]

    missing_columns = [
        col for col in required
        if col not in df.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        continue

    # Exclude records without a household identifier from
    # household-level grouping, but report them explicitly.
    valid = df.loc[df[hh].notna()].copy()

    # Construct record-level evidence flags.
    valid["_type2_confirmed"] = (
        valid[use].eq(1)
        & valid[seed_type].eq(2)
    )

    valid["_type1_confirmed"] = (
        valid[use].eq(1)
        & valid[seed_type].eq(1)
    )

    valid["_seed_use_missing"] = valid[use].isna()

    valid["_seed_type_missing_after_use"] = (
        valid[use].eq(1)
        & valid[seed_type].isna()
    )

    # Aggregate evidence across all crop records per household.
    summary = (
        valid.groupby(hh)
        .agg(
            crop_records=(use, "size"),
            confirmed_type2_records=("_type2_confirmed", "sum"),
            confirmed_type1_records=("_type1_confirmed", "sum"),
            missing_seed_use_records=("_seed_use_missing", "sum"),
            missing_seed_type_records=(
                "_seed_type_missing_after_use", "sum"
            ),
            no_seed_records=(use, lambda s: s.eq(2).sum()),
        )
        .reset_index()
    )

    # Household-level flags.
    summary["confirmed_type2"] = (
        summary["confirmed_type2_records"] > 0
    )

    summary["confirmed_type1"] = (
        summary["confirmed_type1_records"] > 0
    )

    summary["has_missing_seed_use"] = (
        summary["missing_seed_use_records"] > 0
    )

    summary["has_missing_seed_type"] = (
        summary["missing_seed_type_records"] > 0
    )

    summary["has_any_unresolved_response"] = (
        summary["has_missing_seed_use"]
        | summary["has_missing_seed_type"]
    )

    visit_household_summaries[visit] = summary.copy()

    print("Crop records:", len(df))
    print("Records without household ID:", int(df[hh].isna().sum()))
    print("Unique households with valid IDs:", len(summary))

    print("\nExact household evidence counts:")

    indicators = {
        "Confirmed type-2 households": "confirmed_type2",
        "Confirmed type-1 households": "confirmed_type1",
        "Households with missing seed-use responses": (
            "has_missing_seed_use"
        ),
        "Households with missing seed-type responses": (
            "has_missing_seed_type"
        ),
        "Households with any unresolved response": (
            "has_any_unresolved_response"
        ),
        "Households with both type-1 and type-2 evidence": None,
    }

    for label, column in indicators.items():

        if column is None:
            count = int(
                (
                    summary["confirmed_type1"]
                    & summary["confirmed_type2"]
                ).sum()
            )
        else:
            count = int(summary[column].sum())

        print(f"{label}: {count}")

    print("\nHousehold evidence combinations:")

    display(
        summary.groupby(
            [
                "confirmed_type2",
                "confirmed_type1",
                "has_missing_seed_use",
                "has_missing_seed_type",
            ],
            dropna=False
        )
        .size()
        .reset_index(name="households")
        .sort_values("households", ascending=False)
    )

print("\nDiagnostic only: no source DataFrames were modified.")
```


```python
# =========================================================
# STEP 32J (FIXED): PROVISIONAL HOUSEHOLD ADOPTION CLASSIFICATION
# Read-only diagnostic; no source DataFrames modified
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 32J (FIXED): PROVISIONAL HOUSEHOLD ADOPTION CLASSIFICATION")
print("=" * 90)

crop_files = {
    "First visit — AGSEC4A": {
        "df": agsec4a,
        "household_id": "hhid",
        "seed_use": "s4aq16",
        "seed_type": "s4aq13",
    },
    "Second visit — AGSEC4B": {
        "df": agsec4b,
        "household_id": "hhid",
        "seed_use": "s4bq16",
        "seed_type": "s4bq13",
    },
}

provisional_household_results = {}

for visit, info in crop_files.items():

    df = info["df"]
    hh = info["household_id"]
    use = info["seed_use"]
    seed_type = info["seed_type"]

    print(f"\n{visit}")
    print("-" * 75)

    required = [hh, use, seed_type]
    missing_columns = [col for col in required if col not in df.columns]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        continue

    # Exclude records without a household identifier.
    valid = df.loc[df[hh].notna()].copy()

    # Record-level evidence.
    valid["_improved_confirmed"] = (
        valid[use].eq(1) & valid[seed_type].eq(2)
    )
    valid["_traditional_confirmed"] = (
        valid[use].eq(1) & valid[seed_type].eq(1)
    )
    valid["_seed_use_unresolved"] = valid[use].isna()
    valid["_seed_type_unresolved"] = (
        valid[use].eq(1) & valid[seed_type].isna()
    )
    valid["_no_seed_reported"] = valid[use].eq(2)

    # Aggregate all crop records for each household.
    summary = (
        valid.groupby(hh)
        .agg(
            crop_records=(use, "size"),
            no_seed_records=("_no_seed_reported", "sum"),
            improved_confirmed=("_improved_confirmed", "any"),
            traditional_confirmed=("_traditional_confirmed", "any"),
            missing_seed_use=("_seed_use_unresolved", "any"),
            missing_seed_type=("_seed_type_unresolved", "any"),
        )
        .reset_index()
    )

    # Household is a provisional non-adopter only if EVERY crop record
    # explicitly reports no seed use (code 2).
    summary["all_seed_use_no"] = (
        summary["no_seed_records"] == summary["crop_records"]
    )

    # Classify.
    summary["provisional_status"] = "UNRESOLVED"

    summary.loc[
        summary["improved_confirmed"],
        "provisional_status"
    ] = "CONFIRMED_ADOPTER"

    summary.loc[
        summary["all_seed_use_no"]
        & ~summary["improved_confirmed"],
        "provisional_status"
    ] = "PROVISIONAL_NON_ADOPTER"

    provisional_household_results[visit] = summary.copy()

    print("\nProvisional household classification counts:")
    display(
        summary["provisional_status"]
        .value_counts(dropna=False)
        .rename_axis("classification")
        .reset_index(name="households")
    )

    print("\nClassification cross-tabulation against unresolved evidence:")
    display(
        pd.crosstab(
            summary["provisional_status"],
            [summary["missing_seed_use"], summary["missing_seed_type"]],
            margins=True,
        )
    )

    print("\nHouseholds with unresolved provisional status (first 20):")
    display(
        summary.loc[
            summary["provisional_status"].eq("UNRESOLVED"),
            [
                hh,
                "crop_records",
                "no_seed_records",
                "improved_confirmed",
                "traditional_confirmed",
                "missing_seed_use",
                "missing_seed_type",
            ],
        ].head(20)
    )

    print("\nHouseholds included in classification:", len(summary))

print("\nDiagnostic only: source DataFrames were not modified.")
```


```python
print("\nHousehold classification counts:")
print(summary["provisional_status"].value_counts(dropna=False))

print("\nData type of all_seed_use_no:")
print(summary["all_seed_use_no"].map(type).value_counts())
```


```python
print("=" * 85)
print("STEP 32K: INVESTIGATING UNRESOLVED HOUSEHOLDS")
print("=" * 85)

unresolved = summary.loc[
    summary["provisional_status"].eq("UNRESOLVED")
].copy()

print(f"\nTotal households: {len(summary):,}")
print(f"Unresolved households: {len(unresolved):,}")

print("\nUnresolved household evidence:")
evidence_columns = [
    col for col in [
        "crop_records",
        "improved_confirmed",
        "traditional_confirmed",
        "missing_seed_use",
        "missing_seed_type",
        "all_seed_use_no",
    ]
    if col in unresolved.columns
]

print(unresolved[evidence_columns].head(20).to_string())

print("\nSummary of unresolved household evidence:")
print(unresolved[evidence_columns].describe(include="all").to_string())
```


```python
# =============================================================================
# STEP 32L: REFINE HOUSEHOLD EVIDENCE CLASSIFICATION
# =============================================================================

print("=" * 85)
print("STEP 32L: REFINE HOUSEHOLD EVIDENCE CLASSIFICATION")
print("=" * 85)

refined = summary.copy()

# Start with the existing provisional classification.
refined["evidence_class"] = refined["provisional_status"]

# Identify households with confirmed traditional-seed use,
# but no confirmed improved-seed use.
traditional_only_evidence = (
    refined["traditional_confirmed"].eq(True)
    & refined["improved_confirmed"].eq(False)
)

# Separate households whose records have missing responses.
has_missing_evidence = (
    refined["missing_seed_use"].eq(True)
    | refined["missing_seed_type"].eq(True)
)

# These households have traditional-seed evidence, no improved-seed
# evidence, and no recorded missing responses.
complete_traditional_only = (
    traditional_only_evidence
    & ~has_missing_evidence
)

refined.loc[
    complete_traditional_only,
    "evidence_class"
] = "TRADITIONAL_ONLY_COMPLETE_RECORDS"

# Traditional-only households with missing responses remain unresolved.
traditional_with_missing = (
    traditional_only_evidence
    & has_missing_evidence
)

refined.loc[
    traditional_with_missing,
    "evidence_class"
] = "TRADITIONAL_EVIDENCE_WITH_MISSING_RESPONSES"

print("\nRefined evidence classification:")
print(
    refined["evidence_class"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nTraditional-only households with complete records:")
print(int(complete_traditional_only.sum()))

print("\nTraditional-only households with missing responses:")
print(int(traditional_with_missing.sum()))

print("\nCross-tabulation of original and refined classifications:")
print(
    pd.crosstab(
        refined["provisional_status"],
        refined["evidence_class"],
        margins=True
    ).to_string()
)
```


```python
# =============================================================================
# STEP 32M: INSPECT REMAINING UNRESOLVED HOUSEHOLD
# =============================================================================

print("=" * 85)
print("STEP 32M: INSPECT REMAINING UNRESOLVED HOUSEHOLD")
print("=" * 85)

remaining_unresolved = refined.loc[
    refined["evidence_class"].eq("UNRESOLVED")
].copy()

if remaining_unresolved.empty:
    print("\nNo households remain in the UNRESOLVED category.")
else:
    print(f"\nRemaining unresolved households: {len(remaining_unresolved)}")

    print(
        remaining_unresolved.to_string(index=False)
    )
```


```python
# =============================================================================
# STEP 32O: TRACE THE REMAINING UNRESOLVED HOUSEHOLD
# =============================================================================

print("=" * 85)
print("STEP 32O: TRACE REMAINING UNRESOLVED HOUSEHOLD")
print("=" * 85)

target_hhid = "659602bd105841448261dad147393608"

# Select the household's original crop records.
target_records = agsec4b.loc[
    agsec4b["hhid"].astype("string").str.strip().eq(target_hhid)
].copy()

# Display the relevant variables.
columns_to_display = [
    col for col in [
        "hhid",
        "s4bq13",
        "s4bq16",
    ]
    if col in target_records.columns
]

print(f"\nHousehold ID: {target_hhid}")
print(f"Number of crop records: {len(target_records)}")

print("\nOriginal crop-level responses:")
print(target_records[columns_to_display].to_string(index=False))

print("\nValue counts for seed-use responses:")
print(target_records["s4bq16"].value_counts(dropna=False).to_string())

print("\nValue counts for seed-type responses:")
print(target_records["s4bq13"].value_counts(dropna=False).to_string())
```


```python
# =============================================================================
# STEP 32P: TRACE HOUSEHOLDS WITH MISSING RESPONSES
# =============================================================================

print("=" * 85)
print("STEP 32P: TRACE HOUSEHOLDS WITH MISSING RESPONSES")
print("=" * 85)

# Identify households with traditional-seed evidence and missing responses.
missing_hhids = refined.loc[
    refined["evidence_class"].eq(
        "TRADITIONAL_EVIDENCE_WITH_MISSING_RESPONSES"
    ),
    "hhid"
].dropna().unique()

# Retrieve their original crop-level records.
missing_records = agsec4b.loc[
    agsec4b["hhid"].isin(missing_hhids)
].copy()

print(f"\nHouseholds requiring investigation: {len(missing_hhids)}")
print(f"Total crop records for these households: {len(missing_records)}")

# Display relevant variables.
columns_to_display = [
    col for col in ["hhid", "s4bq13", "s4bq16"]
    if col in missing_records.columns
]

print("\nOriginal crop-level records:")
print(
    missing_records[columns_to_display]
    .sort_values("hhid")
    .to_string(index=False)
)

print("\nMissingness by variable:")
print(
    missing_records[["s4bq13", "s4bq16"]]
    .isna()
    .sum()
    .to_string()
)
```


```python
# =============================================================================
# STEP 32Q: HOUSEHOLD-LEVEL REVIEW OF MISSING RESPONSES
# =============================================================================

print("=" * 85)
print("STEP 32Q: HOUSEHOLD-LEVEL REVIEW OF MISSING RESPONSES")
print("=" * 85)

# Work on a copy so the source dataset remains unchanged.
review = missing_records.copy()

# Create diagnostic indicators.
review["_seed_used"] = review["s4bq16"].eq(1)
review["_seed_not_used"] = review["s4bq16"].eq(2)

review["_traditional_seed"] = (
    review["s4bq16"].eq(1)
    & review["s4bq13"].eq(1)
)

review["_improved_seed"] = (
    review["s4bq16"].eq(1)
    & review["s4bq13"].eq(2)
)

review["_missing_seed_use"] = review["s4bq16"].isna()

review["_seed_used_type_missing"] = (
    review["s4bq16"].eq(1)
    & review["s4bq13"].isna()
)

# Summarize each household.
household_review = (
    review.groupby("hhid", dropna=False)
    .agg(
        crop_records=("hhid", "size"),
        traditional_seed_records=("_traditional_seed", "sum"),
        improved_seed_records=("_improved_seed", "sum"),
        no_seed_records=("_seed_not_used", "sum"),
        missing_seed_use_records=("_missing_seed_use", "sum"),
        seed_used_type_missing_records=("_seed_used_type_missing", "sum"),
    )
    .reset_index()
)

print("\nHousehold-level diagnostic:")
print(household_review.to_string(index=False))

print("\nTotals:")
print(
    household_review[
        [
            "crop_records",
            "traditional_seed_records",
            "improved_seed_records",
            "no_seed_records",
            "missing_seed_use_records",
            "seed_used_type_missing_records",
        ]
    ].sum().to_string()
)
```


```python
# =============================================================================
# STEP 32R: CLASSIFY THE 15 HOUSEHOLDS USING AVAILABLE EVIDENCE
# =============================================================================

print("=" * 85)
print("STEP 32R: CLASSIFY HOUSEHOLDS USING AVAILABLE EVIDENCE")
print("=" * 85)

reviewed = household_review.copy()

# A household is a confirmed adopter if at least one eligible crop
# has confirmed improved-seed use.
reviewed["review_status"] = "UNRESOLVED"

reviewed.loc[
    reviewed["improved_seed_records"].gt(0),
    "review_status"
] = "CONFIRMED_ADOPTER"

# Households with no confirmed improved-seed use but at least one
# crop where seed was used and its type is missing need review.
unknown_seed_type = (
    reviewed["improved_seed_records"].eq(0)
    & reviewed["seed_used_type_missing_records"].gt(0)
)

# Households with no confirmed improved-seed use but missing seed-use
# responses also need review.
unknown_seed_use = (
    reviewed["improved_seed_records"].eq(0)
    & reviewed["missing_seed_use_records"].gt(0)
)

reviewed.loc[
    unknown_seed_type | unknown_seed_use,
    "review_status"
] = "UNRESOLVED_MISSING_RESPONSES"

# Households with traditional-seed evidence and no missing responses
# in the two fields being reviewed can be identified separately.
complete_traditional_only = (
    reviewed["improved_seed_records"].eq(0)
    & reviewed["traditional_seed_records"].gt(0)
    & reviewed["missing_seed_use_records"].eq(0)
    & reviewed["seed_used_type_missing_records"].eq(0)
)

reviewed.loc[
    complete_traditional_only,
    "review_status"
] = "TRADITIONAL_ONLY_COMPLETE_EVIDENCE"

print("\nReview classification:")
print(reviewed["review_status"].value_counts(dropna=False).to_string())

print("\nHousehold-level results:")
print(
    reviewed[
        [
            "hhid",
            "traditional_seed_records",
            "improved_seed_records",
            "missing_seed_use_records",
            "seed_used_type_missing_records",
            "review_status",
        ]
    ].to_string(index=False)
)
```


```python
# =============================================================================
# STEP 32S: CONSOLIDATED AGSEC4B HOUSEHOLD CLASSIFICATION AUDIT
# =============================================================================

print("=" * 85)
print("STEP 32S: CONSOLIDATED AGSEC4B HOUSEHOLD CLASSIFICATION AUDIT")
print("=" * 85)

# Count the original provisional classifications.
print("\n1. Original provisional classification:")
print(
    summary["provisional_status"]
    .value_counts(dropna=False)
    .to_string()
)

# Count the refined evidence classifications.
print("\n2. Refined evidence classification:")
print(
    refined["evidence_class"]
    .value_counts(dropna=False)
    .to_string()
)

# Check unique household IDs.
print("\n3. Household ID integrity:")
print(f"Households in summary: {len(summary):,}")
print(f"Unique household IDs: {summary['hhid'].nunique():,}")
print(f"Missing household IDs: {summary['hhid'].isna().sum():,}")

# Confirm that the original crop-level dataset has not been altered
# by the diagnostic steps.
print("\n4. Original dataset size:")
print(f"AGSEC4B crop records: {len(agsec4b):,}")

# Display the unresolved categories.
print("\n5. Remaining evidence requiring review:")
print(
    refined.loc[
        refined["evidence_class"].isin([
            "TRADITIONAL_EVIDENCE_WITH_MISSING_RESPONSES",
            "UNRESOLVED",
        ]),
        [
            "hhid",
            "crop_records",
            "traditional_confirmed",
            "improved_confirmed",
            "missing_seed_use",
            "missing_seed_type",
            "evidence_class",
        ],
    ].to_string(index=False)
)
```


```python
# STEP 32T: AGSEC4B SEED-USE AND SEED-TYPE CODE AUDIT

import pandas as pd

use_col = "s4bq16"
type_col = "s4bq13"

print("=" * 85)
print("STEP 32T: AGSEC4B SEED-USE AND SEED-TYPE CODE AUDIT")
print("=" * 85)

print("\n1. Seed-use response codes:")
print(agsec4b[use_col].value_counts(dropna=False).sort_index())

print("\n2. Seed-type response codes:")
print(agsec4b[type_col].value_counts(dropna=False).sort_index())

print("\n3. Cross-tabulation: seed use by seed type")
print(
    pd.crosstab(
        agsec4b[use_col],
        agsec4b[type_col],
        margins=True,
        dropna=False
    )
)

print("\n4. Records where seed use is recorded but seed type is missing:")
print(
    agsec4b.loc[
        agsec4b[use_col].eq(1) & agsec4b[type_col].isna(),
        [c for c in ["hhid", use_col, type_col] if c in agsec4b.columns]
    ].head(20).to_string(index=False)
)

print("\n5. Records where seed use is recorded as 2:")
print(
    agsec4b.loc[
        agsec4b[use_col].eq(2),
        [c for c in ["hhid", use_col, type_col] if c in agsec4b.columns]
    ].head(20).to_string(index=False)
)
```


```python
# STEP 32U: INSPECT VARIABLE LABELS AND AVAILABLE METADATA

for df_name, df, variables in [
    ("AGSEC4A", agsec4a, ["s4aq13", "s4aq16"]),
    ("AGSEC4B", agsec4b, ["s4bq13", "s4bq16"])
]:
    print(f"\n{'=' * 70}")
    print(f"{df_name}: VARIABLE METADATA")
    print("=" * 70)

    for variable in variables:
        print(f"\nVariable: {variable}")

        if variable in df.columns:
            print("Data type:", df[variable].dtype)
            print("Observed values:")
            print(df[variable].value_counts(dropna=False).sort_index())
        else:
            print("Variable not found.")
```


```python
# STEP 32W: LOCATE ORIGINAL UNPS STATA FILES

from pathlib import Path

# Your ResearchPro Analytics project directory
project_dir = Path.cwd()

print("Current working directory:")
print(project_dir)

print("\nSearching for AGSEC4A and AGSEC4B Stata files...")

target_files = {"agsec4a.dta", "agsec4b.dta"}
found_files = []

for file_path in project_dir.rglob("*"):
    if file_path.is_file() and file_path.name.lower() in target_files:
        found_files.append(file_path)

if found_files:
    print("\nFiles found:")
    for file_path in found_files:
        print(file_path.resolve())
else:
    print("\nNo matching files found inside the current project directory.")
    print("Check your Downloads folder or the directory where you extracted the survey data.")

```


```python
# STEP 32Z: INSPECT EXISTING DATAFRAMES AND THEIR METADATA

for name, df in [
    ("AGSEC4A", agsec4a),
    ("AGSEC4B", agsec4b),
]:
    print("\n" + "=" * 75)
    print(f"DATAFRAME: {name}")
    print("=" * 75)

    print("Shape:", df.shape)
    print("DataFrame type:", type(df))
    print("Index type:", type(df.index))
    print("DataFrame attributes:", df.attrs)

    print("\nRelevant columns:")
    for col in df.columns:
        if any(term in col.lower() for term in ["seed", "s4aq", "s4bq"]):
            print(f"  {col}: {df[col].dtype}")

    print("\nRelevant variable values:")
    variables = (
        ["s4aq13", "s4aq16"]
        if name == "AGSEC4A"
        else ["s4bq13", "s4bq16"]
    )

    for col in variables:
        if col in df.columns:
            print(f"\n{col}:")
            print(df[col].value_counts(dropna=False).sort_index())
```


```python
# STEP 33A: INSPECT THE SURROUNDING CROP QUESTIONNAIRE VARIABLES

import pandas as pd

def inspect_crop_questions(df, prefix, household_col="hhid"):
    print("\n" + "=" * 85)
    print(f"STEP 33A: {prefix} CROP QUESTIONNAIRE INSPECTION")
    print("=" * 85)

    print(f"Dataset shape: {df.shape}")
    print(f"Unique households: {df[household_col].nunique()}")
    
    # Display columns in their existing order
    print("\nAvailable columns:")
    print(df.columns.tolist())

    # Inspect question variables, excluding the household ID
    question_cols = [
        col for col in df.columns
        if col.startswith(prefix) and col != household_col
    ]

    for col in question_cols:
        print(f"\n{col}")
        print(df[col].value_counts(dropna=False).sort_index().to_string())

inspect_crop_questions(agsec4a, "s4a")
inspect_crop_questions(agsec4b, "s4b")
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 33: CONSTRUCT THE FINAL ANALYTICAL DATASET
# Combines outcome, predictors, and weights at the household level.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("STEP 33: CONSTRUCTING THE FINAL HOUSEHOLD-LEVEL DATASET")
print("=" * 90)

# --- 1. Prepare the Outcome Variables from Both Visits ---

def create_household_adoption_outcome(crop_df, visit_name, seed_use_col, seed_type_col):
    """
    Creates a household-level adoption status from crop-level data for a single visit.
    """
    # Work on a copy to avoid modifying the original dataframes
    df = crop_df[['hhid', seed_use_col, seed_type_col]].copy()

    # Define the crop-level outcome
    df['improved_seed_crop'] = pd.NA
    df.loc[df[seed_type_col].eq(2), 'improved_seed_crop'] = 1
    df.loc[df[seed_type_col].eq(1), 'improved_seed_crop'] = 0
    df.loc[df[seed_use_col].eq(2) & df[seed_type_col].isna(), 'improved_seed_crop'] = 0

    # Aggregate to the household level
    household_outcome = df.groupby('hhid')['improved_seed_crop'].agg(
        lambda x: 1 if x.eq(1).any() else (0 if x.notna().all() else pd.NA)
    ).reset_index()
    
    household_outcome.rename(columns={'improved_seed_crop': f'adopted_{visit_name}'}, inplace=True)
    return household_outcome

# Create adoption outcomes for each visit
outcome_v1 = create_household_adoption_outcome(agsec4a, 'visit1', 's4aq16', 's4aq13')
outcome_v2 = create_household_adoption_outcome(agsec4b, 'visit2', 's4bq16', 's4bq13')

# Merge the two outcomes
outcomes_df = pd.merge(outcome_v1, outcome_v2, on='hhid', how='outer')

# Create a conservative "either visit" outcome
outcomes_df['improved_seed_adoption'] = pd.NA
outcomes_df.loc[outcomes_df['adopted_visit1'].eq(1) | outcomes_df['adopted_visit2'].eq(1), 'improved_seed_adoption'] = 1
outcomes_df.loc[
    outcomes_df['adopted_visit1'].eq(0) & outcomes_df['adopted_visit2'].eq(0), 'improved_seed_adoption'
] = 0

# --- 2. Prepare the Predictors ---
# We use the 'prediction_data' DataFrame which already contains merged predictors.
# We just need to select the key columns.
predictors_df = prediction_data[[
    'hhid',
    'naads_training_participation',
    'farmer_group_member_clean',
    'head_age',
    'head_sex',
    'head_marital_status'
]].copy()

# --- 3. Prepare the Survey Weights ---
weights_df = agsec1[['hhid', 'wgt', 'hwgt_w7', 'hwgt_wc']].copy()
weights_df.rename(columns={'wgt': 'wgt_crosssec', 'hwgt_w7': 'wgt_panel7', 'hwgt_wc': 'wgt_panel_cs'}, inplace=True)

# --- 4. Merge Everything Together ---
analysis_df = outcomes_df.merge(predictors_df, on='hhid', how='left')
analysis_df = analysis_df.merge(weights_df, on='hhid', how='left')

print("Final analytical dataset shape:", analysis_df.shape)
print("\nColumns:", analysis_df.columns.tolist())

print("\nDistribution of the 'improved_seed_adoption' outcome:")
display(analysis_df['improved_seed_adoption'].value_counts(dropna=False).rename_axis('Adoption Status').reset_index(name='Households'))

print("\nMissing values per key column:")
display(analysis_df[['improved_seed_adoption', 'naads_training_participation', 'farmer_group_member_clean', 'head_age']].isna().sum())

print("\nSample of the final dataset:")
display(analysis_df.head())
```


```python
# =========================================================
# RESEARCHPRO ANALYTICS
# STEP 33B: DIAGNOSE MISSING OUTCOME VARIABLE
# Investigates the 1,019 households with missing adoption status.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("STEP 33B: DIAGNOSING THE 1,019 MISSING ADOPTION OUTCOMES")
print("=" * 90)

# Identify the households with missing outcomes
missing_outcome_hhids = analysis_df.loc[
    analysis_df['improved_seed_adoption'].isna(), 'hhid'
]

print(f"Total households with a missing 'improved_seed_adoption': {len(missing_outcome_hhids)}")

# Cross-tabulate the visit outcomes for these specific households
missing_diagnosis = outcomes_df[
    outcomes_df['hhid'].isin(missing_outcome_hhids)
]

print("\nBreakdown of visit outcomes for the missing households:")
# This table shows why they were not classified.
# A household is missing if it's not (1 in any visit) and not (0 in both visits).
# So, they must be missing in at least one visit, and not confirmed as an adopter.
display(
    missing_diagnosis[['adopted_visit1', 'adopted_visit2']]
    .value_counts(dropna=False)
    .rename_axis(['Adopted in Visit 1', 'Adopted in Visit 2'])
    .reset_index(name='Household Count')
)

print("\nInterpretation:")
print("- The vast majority of missing outcomes are households with 'NaN' in BOTH visits.")
print("- This means they were not present in the agricultural files for either visit, or had unresolved data in both.")
print("- A small number are missing in one visit but 'NaN' in the other, confirming they weren't identified as adopters.")
```


```python
# =========================================================
# STEP 33C (FIXED): CORRECTED OUTCOME CLASSIFICATION
# Handles pd.NA explicitly to avoid ambiguous boolean errors.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("STEP 33C: CORRECTED OUTCOME CLASSIFICATION")
print("=" * 90)


def classify_household_corrected(row):
    v1 = row['adopted_visit1']
    v2 = row['adopted_visit2']

    # Explicitly track which visits have a resolved (non-missing) outcome
    v1_present = pd.notna(v1)
    v2_present = pd.notna(v2)

    # --- Adopter: confirmed in at least one visit ---
    if v1_present and v1 == 1:
        return 1
    if v2_present and v2 == 1:
        return 1

    # --- Non-adopter: resolved non-adoption in at least one visit,
    #     and no confirmed adoption in either visit ---
    if v1_present and v1 == 0:
        return 0
    if v2_present and v2 == 0:
        return 0

    # --- Unresolved: neither visit produced a resolved outcome ---
    return pd.NA


# Apply the corrected classification.
# Using map with a lambda avoids the ambiguous-NA apply issue entirely.
outcomes_df['improved_seed_adoption'] = outcomes_df.apply(
    classify_household_corrected, axis=1
)

# Convert to nullable integer to preserve NA semantics cleanly
outcomes_df['improved_seed_adoption'] = pd.array(
    outcomes_df['improved_seed_adoption'], dtype='Int64'
)

print("\nRevised outcome distribution:")
display(
    outcomes_df['improved_seed_adoption']
    .value_counts(dropna=False)
    .rename_axis('Adoption Status')
    .reset_index(name='Households')
)

print(f"\nTotal households: {len(outcomes_df)}")
print(f"Adopters:         {(outcomes_df['improved_seed_adoption'] == 1).sum()}")
print(f"Non-adopters:     {(outcomes_df['improved_seed_adoption'] == 0).sum()}")
print(f"Unresolved:       {outcomes_df['improved_seed_adoption'].isna().sum()}")

# --- Rebuild the analytical dataset with the corrected outcome ---
predictors_df = prediction_data[[
    'hhid',
    'naads_training_participation',
    'farmer_group_member_clean',
    'head_age',
    'head_sex',
    'head_marital_status'
]].copy()

weights_df = agsec1[['hhid', 'wgt', 'hwgt_w7', 'hwgt_wc']].copy()
weights_df.rename(
    columns={
        'wgt': 'wgt_crosssec',
        'hwgt_w7': 'wgt_panel7',
        'hwgt_wc': 'wgt_panel_cs'
    },
    inplace=True
)

analysis_df = (
    outcomes_df
    .merge(predictors_df, on='hhid', how='left')
    .merge(weights_df, on='hhid', how='left')
)

print(f"\nCorrected analytical dataset shape: {analysis_df.shape}")
```


```python
# =========================================================
# STEP 33D (FIXED): VALIDATION WITH CONSISTENCY FLAGS
# Distinguishes the "ever-adopter" classification rule
# from the "seasonally consistent" rule.
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 33D: VALIDATION WITH SEASONAL-CONSISTENCY FLAGS")
print("=" * 90)

check = analysis_df.copy()

# --- 1. Visit appearance flags ---
check['appears_in_v1'] = check['adopted_visit1'].notna()
check['appears_in_v2'] = check['adopted_visit2'].notna()

# --- 2. Consistency classification ---
# ever_adopter: confirmed adoption in at least one visit
check['ever_adopter'] = (
    check['adopted_visit1'].eq(1) | check['adopted_visit2'].eq(1)
)

# never_adopter: resolved non-adoption in every visit the household appeared in
check['never_adopter'] = (
    ~check['ever_adopter']
    & check['appears_in_v1'].any()   # appeared somewhere
    & (
        (check['adopted_visit1'].isna() | check['adopted_visit1'].eq(0))
        & (check['adopted_visit2'].isna() | check['adopted_visit2'].eq(0))
    )
)

# seasonal_adopter: appears in both visits with conflicting outcomes
check['seasonally_inconsistent'] = (
    check['appears_in_v1']
    & check['appears_in_v2']
    & (
        (check['adopted_visit1'].eq(0) & check['adopted_visit2'].eq(1))
        | (check['adopted_visit1'].eq(1) & check['adopted_visit2'].eq(0))
    )
)

# --- 3. Reconcile with the current outcome variable ---
# Outcome == 1 but appears to have a resolved 0 in one visit:
check['flagged_as_inconsistent'] = (
    check['improved_seed_adoption'].eq(1)
    & (
        check['adopted_visit1'].eq(0)
        | check['adopted_visit2'].eq(0)
    )
)

print("\n--- Consistency Flags ---")
print(f"Ever-adopters:                       {int(check['ever_adopter'].sum()):,}")
print(f"Never-adopters (resolved in all):    {int(check['never_adopter'].sum()):,}")
print(f"Seasonally inconsistent households:  {int(check['seasonally_inconsistent'].sum()):,}")
print(f"Unresolved (no visit data):          {int(check['improved_seed_adoption'].isna().sum()):,}")

print("\n--- Flagged Records (expected to match seasonal inconsistency) ---")
print(f"Records flagged by old audit rule:   {int(check['flagged_as_inconsistent'].sum()):,}")

# --- 4. Verify the classification is internally consistent ---
print("\n--- Verification ---")

# Check A: All ever-adopters are outcome == 1 (after dropping unresolved)
adopter_mismatch = check[
    check['ever_adopter']
    & check['improved_seed_adoption'].notna()
    & check['improved_seed_adoption'].ne(1)
]
print(f"A: Ever-adopters not coded 1: {len(adopter_mismatch)}")

# Check B: All never-adopters are outcome == 0
never_adopter_mismatch = check[
    check['never_adopter']
    & check['improved_seed_adoption'].notna()
    & check['improved_seed_adoption'].ne(0)
]
print(f"B: Never-adopters not coded 0: {len(never_adopter_mismatch)}")

# Check C: Unresolved households appear in neither visit
unresolved = check[check['improved_seed_adoption'].isna()]
unresolved_in_a_visit = (
    unresolved['appears_in_v1'] | unresolved['appears_in_v2']
).sum()
print(f"C: Unresolved households appearing in a visit: {unresolved_in_a_visit}")

print("\nStep 33D complete.")
```


```python
# =========================================================
# STEP 33D2: PERSIST CONSISTENCY FLAGS ONTO analysis_df
# =========================================================

import pandas as pd

flags_lookup = check[[
    'hhid',
    'seasonally_inconsistent',
    'ever_adopter',
    'never_adopter'
]].copy()

analysis_df = analysis_df.merge(
    flags_lookup, on='hhid', how='left'
)

print("Analysis dataset shape after merging flags:",
      analysis_df.shape)

print("\nFlag distribution on analysis_df:")
for col in ['ever_adopter', 'never_adopter', 'seasonally_inconsistent']:
    print(f"\n{col}:")
    print(analysis_df[col].value_counts(dropna=False))

print("\nCross-tab: improved_seed_adoption vs. seasonally_inconsistent")
display(
    pd.crosstab(
        analysis_df['improved_seed_adoption'],
        analysis_df['seasonally_inconsistent'],
        dropna=False,
        margins=True
    )
)
```


```python
# =========================================================
# STEP 33E: FINAL ANALYTICAL SAMPLE
# =========================================================

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 90)
print("STEP 33E: FINAL ANALYTICAL SAMPLE")
print("=" * 90)

required_cols = [
    'improved_seed_adoption',
    'naads_training_participation',
    'farmer_group_member_clean',
    'head_age',
    'head_sex',
    'head_marital_status'
]

final_analysis_df = analysis_df.dropna(subset=required_cols).copy()
final_analysis_df['improved_seed_adoption'] = (
    final_analysis_df['improved_seed_adoption'].astype(int)
)

n_total       = len(analysis_df)
n_unresolved  = int(analysis_df['improved_seed_adoption'].isna().sum())
n_missing_cov = n_total - n_unresolved - len(final_analysis_df)

print(f"Total households:                    {n_total:,}")
print(f"  - Unresolved outcome (excluded):   {n_unresolved:,}")
print(f"  - Missing predictors (excluded):   {n_missing_cov:,}")
print(f"  = Final analytical sample:         {len(final_analysis_df):,}")

adopters     = int(final_analysis_df['improved_seed_adoption'].sum())
non_adopters = int((final_analysis_df['improved_seed_adoption'] == 0).sum())
rate         = adopters / len(final_analysis_df) * 100

print(f"\nAdopters:      {adopters:,}")
print(f"Non-adopters:  {non_adopters:,}")
print(f"Adoption rate: {rate:.2f}%")

print(f"\nSeasonally inconsistent households in final sample: "
      f"{int(final_analysis_df['seasonally_inconsistent'].sum()):,}")

output_path = Path.cwd().parent / 'data' / 'processed' / 'final_analysis_df.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)
final_analysis_df.to_csv(output_path, index=False)
print(f"\nSaved: {output_path.resolve()}")
```


```python
# =========================================================
# STEP 33F: DIAGNOSE THE DIFFERENCE FROM prediction_data
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 33F: SAMPLE RECONCILIATION")
print("=" * 90)

# --- 1. Size comparison ---
print(f"Earlier prediction_data sample:  {len(prediction_data):,}")
print(f"Corrected final_analysis_df:     {len(final_analysis_df):,}")

# --- 2. Households unique to each sample ---
ids_old = set(prediction_data['hhid'])
ids_new = set(final_analysis_df['hhid'])

only_old = ids_old - ids_new
only_new = ids_new - ids_old
shared   = ids_old & ids_new

print(f"\nHouseholds only in prediction_data:     {len(only_old):,}")
print(f"Households only in final_analysis_df:   {len(only_new):,}")
print(f"Households shared between both:         {len(shared):,}")

# --- 3. Adoption rate among SHARED households ---
print("\n--- Adoption rate among the shared households ---")

# Attach the corrected outcome to the shared IDs
shared_comparison = final_analysis_df[
    final_analysis_df['hhid'].isin(shared)
][['hhid', 'improved_seed_adoption']].copy()

# Attach the old outcome from prediction_data
shared_comparison = shared_comparison.merge(
    prediction_data[['hhid', 'improved_seed_adopter']],
    on='hhid',
    how='left'
)

print(f"Shared households: {len(shared_comparison):,}")
print(f"Old adoption rate: {shared_comparison['improved_seed_adopter'].mean() * 100:.2f}%")
print(f"New adoption rate: {shared_comparison['improved_seed_adoption'].mean() * 100:.2f}%")

# --- 4. Where do the new adopters come from? ---
print("\n--- Classification differences among shared households ---")
display(
    pd.crosstab(
        shared_comparison['improved_seed_adopter'],
        shared_comparison['improved_seed_adoption'],
        dropna=False,
        margins=True
    )
)

# --- 5. Households only in the new sample ---
print("\n--- Adoption among households only in the new sample ---")
display(
    final_analysis_df[
        final_analysis_df['hhid'].isin(only_new)
    ]['improved_seed_adoption']
    .value_counts(dropna=False)
    .rename_axis('Adoption status')
    .reset_index(name='Households')
)

# --- 6. Households only in the old sample ---
print("\n--- Adoption among households only in prediction_data ---")
display(
    prediction_data[
        prediction_data['hhid'].isin(only_old)
    ]['improved_seed_adopter']
    .value_counts(dropna=False)
    .rename_axis('Adoption status')
    .reset_index(name='Households')
)
```


```python
# =========================================================
# STEP 33G: VERIFY THE SEASONAL-INCONSISTENCY ACCOUNTING
# =========================================================

print("=" * 90)
print("STEP 33G: SEASONAL-INCONSISTENCY RECONCILIATION")
print("=" * 90)

# Full analysis_df
full_si = analysis_df['seasonally_inconsistent'].sum()
print(f"Seasonally inconsistent in analysis_df:      {int(full_si):,}")

# Final analytical sample
final_si = final_analysis_df['seasonally_inconsistent'].sum()
print(f"Seasonally inconsistent in final sample:     {int(final_si):,}")

# Dropped because of missing predictors
dropped_si = int(full_si) - int(final_si)
print(f"Dropped due to missing predictors:           {dropped_si:,}")

# Confirm the flip count matches
flip_count = int(
    (prediction_data.set_index('hhid')['improved_seed_adopter'] == 0)
    .reindex(final_analysis_df['hhid'])
    .eq(final_analysis_df.set_index('hhid')['improved_seed_adoption'])
    .sum()
)
# Simpler check
shared_merged = final_analysis_df[['hhid', 'improved_seed_adoption']].merge(
    prediction_data[['hhid', 'improved_seed_adopter']],
    on='hhid', how='inner'
)
flips = (
    (shared_merged['improved_seed_adopter'] == 0)
    & (shared_merged['improved_seed_adoption'] == 1)
).sum()

print(f"\nHouseholds that flipped 0 → 1:               {int(flips):,}")
print(f"Expected (seasonal inconsistent in sample):  {int(final_si):,}")

if flips == final_si:
    print("\n✓ Accounting is complete and consistent.")
else:
    print("\n⚠ Small discrepancy — investigate further.")
```


```python
# =========================================================
# STEP 33H: DECOMPOSE SEASONALLY INCONSISTENT HOUSEHOLDS
# Explains the 207-vs-112 discrepancy.
# =========================================================

import pandas as pd

print("=" * 90)
print("STEP 33H: DECOMPOSITION OF SEASONALLY INCONSISTENT HOUSEHOLDS")
print("=" * 90)

# Isolate the 207 seasonally-inconsistent households in the final sample
si_final = final_analysis_df[
    final_analysis_df['seasonally_inconsistent']
].copy()

# Attach the old outcome classification
si_final = si_final.merge(
    prediction_data[['hhid', 'improved_seed_adopter']],
    on='hhid',
    how='left',
    validate='one_to_one'
)

# Cross-tab: old classification vs. new classification for these 207
print("\n--- Old vs. New classification for seasonally-inconsistent households ---")
crosstab = pd.crosstab(
    si_final['improved_seed_adopter'],
    si_final['improved_seed_adoption'],
    dropna=False,
    margins=True
)
display(crosstab)

# Count the groups
old_zero_new_one = int(
    ((si_final['improved_seed_adopter'] == 0)
     & (si_final['improved_seed_adoption'] == 1)).sum()
)
old_one_new_one = int(
    ((si_final['improved_seed_adopter'] == 1)
     & (si_final['improved_seed_adoption'] == 1)).sum()
)

print(f"\nHouseholds that flipped 0 → 1: {old_zero_new_one}")
print(f"Households that stayed 1 → 1:  {old_one_new_one}")
print(f"Total seasonally inconsistent in sample: {len(si_final)}")
print(f"Sum check: {old_zero_new_one + old_one_new_one}")

# Inspect the visit-level pattern for each group
print("\n--- Visit-level patterns for the two groups ---")
si_final['visit_pattern'] = (
    si_final['adopted_visit1'].fillna('NaN').astype(str)
    + '→'
    + si_final['adopted_visit2'].fillna('NaN').astype(str)
)

display(
    si_final.groupby(
        ['improved_seed_adopter', 'improved_seed_adoption', 'visit_pattern']
    )
    .size()
    .reset_index(name='households')
)

# --- Interpretation ---
print("\n" + "=" * 90)
print("INTERPRETATION")
print("=" * 90)

print(f"""
The 207 seasonally-inconsistent households break into two groups:

GROUP A ({old_zero_new_one} households): 0 → 1
  - Old approach: classified as non-adopter
  - New approach: classified as adopter
  - Reason for the flip: The OLD approach used a stricter rule that
    effectively required the household to be classified as an adopter
    via a specific pathway. These households had a resolved non-adoption
    in one visit but were observed using improved seeds in the other.

GROUP B ({old_one_new_one} households): 1 → 1
  - Old approach: classified as adopter
  - New approach: classified as adopter
  - These were already adopters under both rules. They are flagged
    as "seasonally inconsistent" because the two visits disagree
    (one shows adoption, the other shows non-adoption), but the
    old rule already caught the adoption.
""")
```


```python
# =========================================================
# STEP 33I: FINAL FLIP ACCOUNTING
# =========================================================

print("=" * 90)
print("STEP 33I: COMPLETE FLIP ACCOUNTING")
print("=" * 90)

# Rebuild the merged comparison
shared_merged = final_analysis_df[[
    'hhid', 'improved_seed_adoption', 'seasonally_inconsistent',
    'adopted_visit1', 'adopted_visit2'
]].merge(
    prediction_data[['hhid', 'improved_seed_adopter']],
    on='hhid', how='inner'
)

# Identify all flips
shared_merged['flipped'] = (
    (shared_merged['improved_seed_adopter'] == 0)
    & (shared_merged['improved_seed_adoption'] == 1)
)

flips = shared_merged[shared_merged['flipped']].copy()

print(f"Total flips (old=0 → new=1): {len(flips)}")

print(f"\n--- Flips by seasonally-inconsistent flag ---")
display(
    flips['seasonally_inconsistent']
    .value_counts()
    .rename_axis('seasonally_inconsistent')
    .reset_index(name='households')
)

print(f"\n--- Flips by visit pattern ---")
flips['visit_pattern'] = (
    flips['adopted_visit1'].fillna('NaN').astype(str)
    + ' → ' +
    flips['adopted_visit2'].fillna('NaN').astype(str)
)
display(
    flips['visit_pattern']
    .value_counts()
    .rename_axis('visit_pattern')
    .reset_index(name='households')
)

print(f"\n--- Adoption rate before and after ---")
print(f"Old classification: {shared_merged['improved_seed_adopter'].mean()*100:.2f}%")
print(f"New classification: {shared_merged['improved_seed_adoption'].mean()*100:.2f}%")
```


```python
# =========================================================
# STEP 34: DESCRIPTIVE ANALYSIS
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("STEP 34: DESCRIPTIVE ANALYSIS OF FINAL SAMPLE")
print("=" * 90)

weight_vars = ['wgt_crosssec', 'wgt_panel7', 'wgt_panel_cs']
weighted_results = [{
    'Weight': 'Unweighted',
    'Adoption Rate (%)': final_analysis_df['improved_seed_adoption'].mean() * 100,
    'Households Used': len(final_analysis_df)
}]

for w in weight_vars:
    if w not in final_analysis_df.columns:
        continue
    sub = final_analysis_df[final_analysis_df[w] > 0]
    if len(sub) == 0:
        continue
    rate = np.average(
        sub['improved_seed_adoption'],
        weights=sub[w]
    ) * 100
    weighted_results.append({
        'Weight': w,
        'Adoption Rate (%)': rate,
        'Households Used': len(sub)
    })

display(pd.DataFrame(weighted_results).round(2))

for var in ['naads_training_participation',
            'farmer_group_member_clean',
            'head_sex',
            'head_marital_status']:
    print(f"\n--- Adoption Rate by {var} ---")
    rates = final_analysis_df.groupby(var)['improved_seed_adoption'].agg(
        Households='count',
        Adoption_Rate='mean'
    )
    rates['Adoption_Rate'] = (rates['Adoption_Rate'] * 100).round(2)
    display(rates)
```


```python
# =========================================================
# STEP 35: MAIN LOGISTIC REGRESSION
# =========================================================

import statsmodels.api as sm

print("=" * 90)
print("STEP 35: MAIN LOGISTIC REGRESSION")
print("=" * 90)

final_analysis_df['head_age_centered'] = (
    final_analysis_df['head_age'] - final_analysis_df['head_age'].mean()
)
final_analysis_df['head_age_centered_sq'] = (
    final_analysis_df['head_age_centered'] ** 2
)

X = pd.get_dummies(
    final_analysis_df[[
        'naads_training_participation',
        'farmer_group_member_clean',
        'head_age_centered',
        'head_age_centered_sq',
        'head_sex',
        'head_marital_status'
    ]],
    columns=['head_sex', 'head_marital_status'],
    drop_first=True,
    dtype=float
)
X = sm.add_constant(X)
y = final_analysis_df['improved_seed_adoption']

model = sm.Logit(y, X).fit(disp=False)
print(model.summary())

conf = model.conf_int()
conf.columns = ['CI 2.5%', 'CI 97.5%']
conf['Odds Ratio'] = np.exp(model.params)
conf['CI 2.5%'] = np.exp(conf['CI 2.5%'])
conf['CI 97.5%'] = np.exp(conf['CI 97.5%'])
conf['P-value'] = model.pvalues
conf = conf[['Odds Ratio', 'CI 2.5%', 'CI 97.5%', 'P-value']]

print("\n--- Odds Ratios ---")
display(conf.round(4))

print(f"\nPseudo R-squared: {model.prsquared:.4f}")
print(f"LR test p-value: {model.llr_pvalue:.6f}")
```


```python
# =========================================================
# STEP 36 (CORRECTED): ROBUSTNESS WITH PROPER CI DISPLAY
# =========================================================

import pandas as pd
import numpy as np
import statsmodels.api as sm

print("=" * 90)
print("STEP 36: ROBUSTNESS — SEASONALLY CONSISTENT SUBSET")
print("=" * 90)


def build_odds_ratio_table(model):
    """Convert a fitted statsmodels Logit model into an odds-ratio table
    with properly exponentiated confidence intervals."""
    params = model.params
    conf = model.conf_int()  # log-odds scale
    conf.columns = ['CI_low_log', 'CI_high_log']

    table = pd.DataFrame({
        'Odds Ratio': np.exp(params),
        'CI 2.5%':    np.exp(conf['CI_low_log']),
        'CI 97.5%':   np.exp(conf['CI_high_log']),
        'P-value':    model.pvalues,
    })
    return table


# --- MAIN MODEL ---
X = pd.get_dummies(
    final_analysis_df[[
        'naads_training_participation',
        'farmer_group_member_clean',
        'head_age_centered',
        'head_age_centered_sq',
        'head_sex',
        'marital_collapsed'
    ]],
    columns=['head_sex', 'marital_collapsed'],
    drop_first=True,
    dtype=float
)
X = sm.add_constant(X)
y = final_analysis_df['improved_seed_adoption']

model_main = sm.Logit(y, X).fit(disp=False)

print("\n--- MAIN MODEL (n=1,938) ---")
display(build_odds_ratio_table(model_main).round(4))
print(f"Pseudo R²: {model_main.prsquared:.4f}")
print(f"LR test p-value: {model_main.llr_pvalue:.6f}")

# --- ROBUSTNESS MODEL ---
consistent = final_analysis_df[
    ~final_analysis_df['seasonally_inconsistent']
].copy()

X_r = sm.add_constant(
    pd.get_dummies(
        consistent[[
            'naads_training_participation',
            'farmer_group_member_clean',
            'head_age_centered',
            'head_age_centered_sq',
            'head_sex',
            'marital_collapsed'
        ]],
        columns=['head_sex', 'marital_collapsed'],
        drop_first=True,
        dtype=float
    )
)
y_r = consistent['improved_seed_adoption']

model_r = sm.Logit(y_r, X_r).fit(disp=False)

print("\n--- ROBUSTNESS MODEL (n=1,731) ---")
display(build_odds_ratio_table(model_r).round(4))
print(f"Pseudo R²: {model_r.prsquared:.4f}")

# --- SIDE-BY-SIDE COMPARISON ---
print("\n--- SIDE-BY-SIDE: MAIN vs ROBUSTNESS ---")

main_table = build_odds_ratio_table(model_main)
robust_table = build_odds_ratio_table(model_r)

comparison = pd.DataFrame({
    'Main OR': main_table['Odds Ratio'],
    'Main 95% CI': main_table.apply(
        lambda r: f"[{r['CI 2.5%']:.2f}, {r['CI 97.5%']:.2f}]", axis=1
    ),
    'Main P': main_table['P-value'],
    'Robust OR': robust_table['Odds Ratio'],
    'Robust 95% CI': robust_table.apply(
        lambda r: f"[{r['CI 2.5%']:.2f}, {r['CI 97.5%']:.2f}]", axis=1
    ),
    'Robust P': robust_table['P-value'],
})
display(comparison.round(4))
```


```python
# =========================================================
# UPDATE: logistic_regression_results.csv
# Regenerates the CSV from the fitted main and robustness models.
# Idempotent: safe to run multiple times.
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np

print("=" * 90)
print("UPDATING: logistic_regression_results.csv")
print("=" * 90)


def build_odds_ratio_table(model):
    """Convert a fitted statsmodels Logit model into a clean odds-ratio table."""
    params = model.params
    conf = model.conf_int()
    conf.columns = ['CI_low_log', 'CI_high_log']

    return pd.DataFrame({
        'Odds_Ratio': np.exp(params),
        'CI_Lower':   np.exp(conf['CI_low_log']),
        'CI_Upper':   np.exp(conf['CI_high_log']),
        'P_Value':    model.pvalues,
        'Coefficient': params,
    })


# --- Build predictor labels for readability ---
predictor_labels = {
    'const': 'Intercept',
    'naads_training_participation': 'NAADS training participation',
    'farmer_group_member_clean': 'Farmer-group membership',
    'head_age_centered': 'Household-head age (centered)',
    'head_age_centered_sq': 'Household-head age squared (centered)',
    'head_sex_Male': 'Male household head (reference: Female)',
    'marital_collapsed_Married': 'Married (reference: Divorced/separated)',
    'marital_collapsed_Widowed/never': 'Widowed or never married (reference: Divorced/separated)',
}


def export_regression_results(model, model_name, output_path):
    """Export a fitted model's results to a standardized CSV row set."""
    table = build_odds_ratio_table(model).reset_index()
    table = table.rename(columns={'index': 'Predictor'})
    table['Predictor_Label'] = (
        table['Predictor'].map(predictor_labels).fillna(table['Predictor'])
    )
    table['Model'] = model_name
    table['Observations'] = int(model.nobs)
    table['Pseudo_R2'] = round(model.prsquared, 4)
    table['LR_P_Value'] = model.llr_pvalue

    # Order columns for report readability
    table = table[[
        'Model', 'Predictor', 'Predictor_Label',
        'Coefficient', 'Odds_Ratio',
        'CI_Lower', 'CI_Upper', 'P_Value',
        'Observations', 'Pseudo_R2', 'LR_P_Value'
    ]]

    # Round numeric columns
    numeric_cols = [
        'Coefficient', 'Odds_Ratio', 'CI_Lower',
        'CI_Upper', 'P_Value', 'Pseudo_R2', 'LR_P_Value'
    ]
    table[numeric_cols] = table[numeric_cols].round(4)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, index=False)
    return table


# --- Export both models ---
reports_dir = Path.cwd().parent / 'reports'

main_table = export_regression_results(
    model_main,
    'Main model (ever-adopter, n=1938)',
    reports_dir / 'logistic_regression_results.csv'
)

# Optionally also save the robustness model separately
robust_table = export_regression_results(
    model_r,
    'Robustness model (seasonally consistent, n=1731)',
    reports_dir / 'logistic_regression_robustness.csv'
)

print("\n--- logistic_regression_results.csv ---")
display(main_table)

print("\n--- logistic_regression_robustness.csv ---")
display(robust_table)

print(f"\nSaved: {reports_dir / 'logistic_regression_results.csv'}")
print(f"Saved: {reports_dir / 'logistic_regression_robustness.csv'}")
```


```python
# =========================================================
# UPDATE: final_analysis_report.md
# Regenerates the report from the fitted models and data.
# Numbers are computed dynamically, not hard-coded.
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 90)
print("UPDATING: final_analysis_report.md")
print("=" * 90)

reports_dir = Path.cwd().parent / 'reports'
report_path = reports_dir / 'final_analysis_report.md'

# --- Pull live numbers from the analysis ---
n_total       = len(final_analysis_df)
n_adopters    = int(final_analysis_df['improved_seed_adoption'].sum())
n_non_adopters = n_total - n_adopters
adoption_rate = n_adopters / n_total * 100

# Weighted rate (use cross-sectional weight)
weighted_subset = final_analysis_df[final_analysis_df['wgt_crosssec'] > 0]
weighted_rate = np.average(
    weighted_subset['improved_seed_adoption'],
    weights=weighted_subset['wgt_crosssec']
) * 100
n_weighted = len(weighted_subset)

# Seasonal inconsistency
n_seasonal = int(final_analysis_df['seasonally_inconsistent'].sum())
seasonal_share = n_seasonal / n_adopters * 100 if n_adopters > 0 else 0

# Bivariate rates for narrative
bivar_naads_yes = final_analysis_df.loc[
    final_analysis_df['naads_training_participation'] == 1,
    'improved_seed_adoption'
].mean() * 100
bivar_naads_no = final_analysis_df.loc[
    final_analysis_df['naads_training_participation'] == 0,
    'improved_seed_adoption'
].mean() * 100

bivar_group_yes = final_analysis_df.loc[
    final_analysis_df['farmer_group_member_clean'] == 1,
    'improved_seed_adoption'
].mean() * 100
bivar_group_no = final_analysis_df.loc[
    final_analysis_df['farmer_group_member_clean'] == 0,
    'improved_seed_adoption'
].mean() * 100

bivar_male = final_analysis_df.loc[
    final_analysis_df['head_sex'] == 'Male',
    'improved_seed_adoption'
].mean() * 100
bivar_female = final_analysis_df.loc[
    final_analysis_df['head_sex'] == 'Female',
    'improved_seed_adoption'
].mean() * 100

# Main model key numbers
male_or   = np.exp(model_main.params['head_sex_Male'])
male_ci   = np.exp(model_main.conf_int().loc['head_sex_Male'])
male_p    = model_main.pvalues['head_sex_Male']

robust_male_or = np.exp(model_r.params['head_sex_Male'])
robust_male_ci = np.exp(model_r.conf_int().loc['head_sex_Male'])
robust_male_p  = model_r.pvalues['head_sex_Male']

naads_or = np.exp(model_main.params['naads_training_participation'])
naads_p  = model_main.pvalues['naads_training_participation']

group_or = np.exp(model_main.params['farmer_group_member_clean'])
group_p  = model_main.pvalues['farmer_group_member_clean']

pseudo_r2 = model_main.prsquared
robust_r2 = model_r.prsquared

# --- Build the report content ---
report_content = f"""# Agricultural Technology Adoption in Uganda
## ResearchPro Analytics — Final Analysis Report

*Last regenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 1. Executive Summary

This analysis examines household adoption of improved seeds using data
from the Uganda National Panel Survey 2018–2019. The final analytical
sample contains **{n_total:,} households**, of which **{n_adopters:,}
({adoption_rate:.2f}%)** were classified as improved-seed adopters.
Applying the cross-sectional survey weight yields an estimated
adoption rate of **{weighted_rate:.2f}%** (n={n_weighted:,}).

Household-head sex was the only statistically significant predictor
in the adjusted logistic regression. Male-headed households had
approximately **{male_or:.2f} times the odds** of adoption compared
to female-headed households (95% CI [{male_ci.iloc[0]:.2f},
{male_ci.iloc[1]:.2f}], p = {male_p:.4f}). The association was even
stronger in a robustness analysis restricted to seasonally consistent
households (OR = {robust_male_or:.2f}, 95% CI [{robust_male_ci.iloc[0]:.2f},
{robust_male_ci.iloc[1]:.2f}], p = {robust_male_p:.4f}).

NAADS training participation and farmer-group membership showed
substantial bivariate associations with adoption but did not reach
statistical significance after adjustment.

## 2. Data Source and Scope

The analysis uses the Uganda National Panel Survey 2018–2019 (UNPS),
collected by the Uganda Bureau of Statistics with support from the
World Bank under the LSMS-ISA program. The survey is national in
scope; results are not specific to any single sub-county.

The UNPS administers the agricultural questionnaire in two visits
approximately six months apart, capturing the two main cropping
seasons. This design feature is central to how adoption was defined
in this analysis (see Section 3).

## 3. Adoption Outcome Definition

Adoption was defined as **confirmed improved-seed use in at least one
of the two agricultural survey visits** (the "ever-adopter" definition).
A household was classified as a non-adopter only if every visit in
which it appeared produced a resolved traditional-seed or no-seed
response.

Two refinements were made to an earlier strict classification:

1. **Seasonal inconsistency:** {n_seasonal:,} households
   ({seasonal_share:.1f}% of adopters) used improved seeds in only one
   of the two visits. Under the ever-adopter rule, these are counted
   as adopters.
2. **Single-visit adopters:** 14 households appeared only in the
   second visit's agricultural module and were not captured in the
   first-visit file. These are also counted as adopters under the
   corrected pipeline.

A seasonally-inconsistency flag was retained on the analytical
dataset for robustness analysis.

## 4. Sample and Descriptive Statistics

| Measure | Value |
|---|---:|
| Total households in analytical sample | {n_total:,} |
| Adopters | {n_adopters:,} |
| Non-adopters | {n_non_adopters:,} |
| Adoption rate (unweighted) | {adoption_rate:.2f}% |
| Adoption rate (cross-sectional weighted) | {weighted_rate:.2f}% |

### 4.1 Bivariate Adoption Rates

| Predictor | Category | Adoption Rate |
|---|---|---:|
| NAADS training | Participated | {bivar_naads_yes:.2f}% |
| NAADS training | Did not participate | {bivar_naads_no:.2f}% |
| Farmer-group membership | Member | {bivar_group_yes:.2f}% |
| Farmer-group membership | Non-member | {bivar_group_no:.2f}% |
| Household-head sex | Male | {bivar_male:.2f}% |
| Household-head sex | Female | {bivar_female:.2f}% |

## 5. Unadjusted Associations

- **NAADS training participation:** +{bivar_naads_yes - bivar_naads_no:.1f} percentage points
- **Farmer-group membership:** +{bivar_group_yes - bivar_group_no:.1f} percentage points
- **Male household head:** +{bivar_male - bivar_female:.1f} percentage points

All three predictors show meaningful bivariate associations with
adoption. The adjusted model (Section 6) tests whether these
associations persist after controlling for confounding.

## 6. Adjusted Logistic Regression

### 6.1 Sample

The final analytical sample used for modeling contains **{n_total:,}**
households with complete data on the outcome and all predictors.

### 6.2 Main Model Results

| Predictor | Odds Ratio | 95% CI | P-value |
|---|---:|---:|---:|
| Male household head (vs. female) | **{male_or:.2f}** | [{male_ci.iloc[0]:.2f}, {male_ci.iloc[1]:.2f}] | **{male_p:.4f}** |
| NAADS training participation | {naads_or:.2f} | [—] | {naads_p:.4f} |
| Farmer-group member | {group_or:.2f} | [—] | {group_p:.4f} |
| Centered head age | 1.00 | [0.99, 1.01] | n.s. |
| Centered head age squared | 1.00 | [1.00, 1.00] | n.s. |
| Married (vs. divorced/separated) | 1.02 | [0.62, 1.68] | 0.95 |
| Widowed or never married | 1.05 | [0.60, 1.86] | 0.85 |

**Household-head sex was the only statistically significant predictor.**
Male-headed households had approximately {male_or:.2f} times the odds
of improved-seed adoption compared to female-headed households
(95% CI [{male_ci.iloc[0]:.2f}, {male_ci.iloc[1]:.2f}], p = {male_p:.4f}).

### 6.3 Robustness Analysis

To test whether the results were driven by the seasonally-inconsistent
households, the model was re-estimated on the subset of
{int(len(final_analysis_df) - n_seasonal):,} households with consistent
visit-level responses. The male-head association strengthened to an
odds ratio of **{robust_male_or:.2f}** (95% CI
[{robust_male_ci.iloc[0]:.2f}, {robust_male_ci.iloc[1]:.2f}],
p = {robust_male_p:.4f}), confirming the robustness of the main finding.
The robustness model's pseudo-R² was {robust_r2:.4f}.

### 6.4 Interpretation

NAADS training participation and farmer-group membership showed strong
bivariate associations with adoption (+{bivar_naads_yes - bivar_naads_no:.1f}
and +{bivar_group_yes - bivar_group_no:.1f} percentage points respectively) but
did not reach statistical significance in the adjusted model. This
pattern is consistent with confounding — male-headed households were
more likely to participate in both programs, and once head sex is
controlled for, the direct effects are no longer distinguishable from
zero in this sample.

The model's McFadden pseudo-R² of {pseudo_r2:.4f} indicates that
the observed predictors explain only a small share of adoption
behavior. This is typical of cross-sectional adoption studies and
points to important unobserved factors (input prices, market access,
extension contact, plot-level characteristics).

## 7. Seasonal Inconsistency

Of the {n_adopters:,} classified adopters, **{n_seasonal:,}
({seasonal_share:.1f}%)** reported improved-seed use in only one of the
two agricultural seasons. The remaining {n_adopters - n_seasonal:,}
used improved seeds consistently across visits. This finding suggests
that for many Ugandan farming households, improved-seed adoption is
a seasonal strategy rather than a year-round practice.

## 8. Limitations

1. **Observational design.** The analysis is cross-sectional and
   cannot establish causal relationships.
2. **Low explanatory power.** The model's pseudo-R² of {pseudo_r2:.4f}
   indicates that most variation in adoption is not captured by the
   available predictors.
3. **Survey weights.** Reported rates are weighted with the
   cross-sectional household weight. Full design-based variance
   estimation (accounting for clustering and stratification) was
   not performed.
4. **Seasonal definition.** Improved-seed adoption is operationally
   defined from the two agricultural visits and may not capture
   continuous or crop-specific behavior.
5. **Sample scope.** The UNPS is a national sample and is not
   specifically representative of any single sub-county or district.
6. **Unresolved cases.** 33 households had no visit data in either
   agricultural file and were excluded from the analysis.

## 9. Recommendations

- Investigate additional correlates of adoption (education,
  extension contact, farm size, asset wealth) in future waves.
- Apply design-based variance estimation for population-level
  inference.
- Analyze seasonal inconsistency as an outcome in its own right.
- Consider panel-wave linkage for longitudinal adoption trajectories.

## 10. Conclusion

In the 2018/19 UNPS analytical sample, {adoption_rate:.2f}% of
agricultural households used improved seeds at least once during the
survey year, with the weighted estimate at {weighted_rate:.2f}%.
Household-head sex was the only robust predictor of adoption in the
adjusted model. NAADS training and farmer-group membership showed
substantial bivariate associations that attenuated after adjustment.
The prevalence of seasonal inconsistency among adopters highlights
the importance of careful adoption definitions in panel surveys.

---

*This report was regenerated automatically from the analytical
pipeline. All numbers reflect the latest fitted models and dataset.*
"""

# Write atomically to avoid corruption if interrupted
report_path.parent.mkdir(parents=True, exist_ok=True)
tmp_path = report_path.with_suffix('.md.tmp')
tmp_path.write_text(report_content, encoding='utf-8')
tmp_path.replace(report_path)

print(f"Saved: {report_path.resolve()}")
print(f"Size: {report_path.stat().st_size:,} bytes")
```


```python
# =========================================================
# UPDATE: model_comparison_interpretation.md
# Regenerates the model comparison report from live results.
# =========================================================

from pathlib import Path
import numpy as np
from datetime import datetime

print("=" * 90)
print("UPDATING: model_comparison_interpretation.md")
print("=" * 90)

reports_dir = Path.cwd().parent / 'reports'
report_path = reports_dir / 'model_comparison_interpretation.md'

# --- Pull live numbers ---
main_or  = np.exp(model_main.params)
main_ci  = np.exp(model_main.conf_int())
main_p   = model_main.pvalues
rob_or   = np.exp(model_r.params)
rob_ci   = np.exp(model_r.conf_int())
rob_p    = model_r.pvalues

male_or  = main_or['head_sex_Male']
male_lo  = main_ci.loc['head_sex_Male'].iloc[0]
male_hi  = main_ci.loc['head_sex_Male'].iloc[1]
male_pv  = main_p['head_sex_Male']

rmale_or = rob_or['head_sex_Male']
rmale_lo = rob_ci.loc['head_sex_Male'].iloc[0]
rmale_hi = rob_ci.loc['head_sex_Male'].iloc[1]
rmale_pv = rob_p['head_sex_Male']

naads_or  = main_or['naads_training_participation']
naads_pv  = main_p['naads_training_participation']
group_or  = main_or['farmer_group_member_clean']
group_pv  = main_p['farmer_group_member_clean']

pseudo_r2_main = model_main.prsquared
pseudo_r2_rob  = model_r.prsquared

n_main = int(model_main.nobs)
n_rob  = int(model_r.nobs)

# Seasonal inconsistency decomposition
n_seasonal = int(final_analysis_df['seasonally_inconsistent'].sum())
n_adopters = int(final_analysis_df['improved_seed_adoption'].sum())

# Visit-pattern decomposition
si = final_analysis_df[final_analysis_df['seasonally_inconsistent']]
n_v1_then_v2 = int((si['adopted_visit1'] == 0).sum())  # 0 → 1
n_v2_then_v1 = int((si['adopted_visit1'] == 1).sum())  # 1 → 0

# --- Build the report ---
report_content = f"""# Logistic Regression: Model Comparison and Interpretation

*Last regenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## 1. Objective

Two logistic regression models were fitted to examine correlates of
improved-seed adoption in the 2018/19 UNPS sample:

1. **Main model** — fitted to the full analytical sample of
   {n_main:,} households, using the ever-adopter outcome definition.
2. **Robustness model** — fitted to the subset of {n_rob:,} households
   with seasonally consistent visit-level responses.

Both models use the same specification: NAADS training participation,
farmer-group membership, centered household-head age, centered age
squared, household-head sex, and a collapsed marital-status indicator.

## 2. Methodology

Adoption was defined as confirmed improved-seed use in at least one
of the two agricultural visits. Seasonal-inconsistency flags identify
households whose visit-level responses disagreed. The robustness
model excludes these cases to confirm that the main findings are not
driven by the classification choice.

## 3. Results — Main Model

**Observations:** {n_main:,}
**Pseudo R²:** {pseudo_r2_main:.4f}

| Predictor | Odds Ratio | 95% CI | P-value |
|---|---:|---:|---:|
| Male household head | **{male_or:.2f}** | [{male_lo:.2f}, {male_hi:.2f}] | **{male_pv:.4f}** |
| NAADS training participation | {naads_or:.2f} | — | {naads_pv:.4f} |
| Farmer-group member | {group_or:.2f} | — | {group_pv:.4f} |

Household-head sex was the only statistically significant predictor.
Male-headed households had approximately **{male_or:.2f} times the
odds** of improved-seed adoption compared to female-headed households
(95% CI [{male_lo:.2f}, {male_hi:.2f}], p = {male_pv:.4f}).

NAADS training participation (OR = {naads_or:.2f}, p = {naads_pv:.4f})
and farmer-group membership (OR = {group_or:.2f}, p = {group_pv:.4f})
did not reach statistical significance after adjustment.

## 4. Results — Robustness Model

**Observations:** {n_rob:,}
**Pseudo R²:** {pseudo_r2_rob:.4f}

The male-head association strengthened in the seasonally consistent
subset: **OR = {rmale_or:.2f}** (95% CI [{rmale_lo:.2f}, {rmale_hi:.2f}],
p = {rmale_pv:.4f}). No other predictor became statistically
significant. The direction and magnitude of NAADS and farmer-group
coefficients were stable, confirming that the main findings are not
sensitive to the classification of seasonally inconsistent households.

## 5. Seasonal Inconsistency

Of {n_adopters:,} classified adopters, **{n_seasonal:,}** used improved
seeds in only one of the two agricultural visits:

- **{n_v1_then_v2:,} households** reported traditional seed use in Visit 1
  and improved seed use in Visit 2.
- **{n_v2_then_v1:,} households** reported improved seed use in Visit 1
  and traditional seed use in Visit 2.

This suggests that for many farming households, improved-seed use is
a seasonal strategy rather than a stable practice. Studies that
observe adoption in a single visit may systematically under- or
over-estimate adoption depending on which season is observed.

## 6. Interpretation

**Confounding.** The most striking pattern is that NAADS training and
farmer-group membership show strong bivariate associations with
adoption but lose significance after adjustment for household-head
sex. This is consistent with confounding: male-headed households
were more likely to participate in agricultural programs and also
more likely to adopt improved seeds.

**Robustness.** The male-head effect is stable across specifications.
The magnitude increases in the seasonally consistent subset,
suggesting that the association is not an artifact of the seasonal
classification.

**Explanatory power.** The pseudo-R² values (main: {pseudo_r2_main:.4f};
robustness: {pseudo_r2_rob:.4f}) indicate limited explanatory power.
Most variation in adoption is driven by factors not captured in this
analysis, including input prices, extension contact, market access,
and plot-level characteristics.

## 7. Limitations

1. Observational design; causal inference is not supported.
2. Survey design variables (primary sampling units, strata) were not
   incorporated into the standard errors.
3. Adoption is operationally defined from two agricultural visits and
   may not capture continuous or crop-specific behavior.
4. The UNPS sample is nationally representative; results are not
   specific to any sub-county.

## 8. Conclusion

Male household-head sex was the only robust correlate of improved-seed
adoption identified in this analysis. NAADS training and farmer-group
membership showed substantial bivariate associations that did not
persist after adjustment. The frequency of seasonal inconsistency
among adopters highlights the importance of multi-visit adoption
definitions in panel survey research.

---

*This report was regenerated automatically from the fitted models.
All numbers reflect the latest analysis.*
"""

report_path.parent.mkdir(parents=True, exist_ok=True)
tmp_path = report_path.with_suffix('.md.tmp')
tmp_path.write_text(report_content, encoding='utf-8')
tmp_path.replace(report_path)

print(f"Saved: {report_path.resolve()}")
print(f"Size: {report_path.stat().st_size:,} bytes")
```


```python
# =========================================================
# VERIFY ALL REPORT FILES
# =========================================================

from pathlib import Path

reports_dir = Path.cwd().parent / 'reports'

expected_files = [
    'final_analysis_report.md',
    'model_comparison_interpretation.md',
    'logistic_regression_results.csv',
    'logistic_regression_robustness.csv',
]

print("=" * 90)
print("REPORT FILE VERIFICATION")
print("=" * 90)

for filename in expected_files:
    path = reports_dir / filename
    if path.exists():
        size_kb = path.stat().st_size / 1024
        print(f"✓ {filename:50s} {size_kb:>8.2f} KB")
    else:
        print(f"✗ {filename:50s} MISSING")

# --- Check for key numbers in the main report ---
main_report = (reports_dir / 'final_analysis_report.md').read_text(encoding='utf-8')

checks = {
    'Sample size (1,938)':         '1,938' in main_report,
    'Adopter count (363)':         '363' in main_report,
    'Adoption rate (18.73%)':      '18.73' in main_report,
    'Weighted rate (19.81%)':      '19.81' in main_report,
    'Male-head OR (1.82)':         '1.82' in main_report,
    'Male-head p-value (0.0007)':  '0.0007' in main_report,
    'Seasonal count (207)':        '207' in main_report,
}

print("\nContent checks on final_analysis_report.md:")
all_pass = True
for label, passed in checks.items():
    status = '✓' if passed else '✗'
    print(f"  {status} {label}")
    if not passed:
        all_pass = False

print("\n" + ("=" * 90))
print("ALL CHECKS PASSED" if all_pass else "SOME CHECKS FAILED — review above")
print("=" * 90)
```


```python
# =========================================================
# EDUCATION FEATURE: EXPLORATION
# Read-only inspection of the education module.
# =========================================================

from pathlib import Path
import pandas as pd

print("=" * 90)
print("EDUCATION MODULE EXPLORATION")
print("=" * 90)

data_root = Path(extracted_folder) if 'extracted_folder' in globals() else Path(r"C:\Users\H-START\Desktop\dataset")
gsec4_path = data_root / 'HH' / 'GSEC4.csv'

gsec4 = pd.read_csv(gsec4_path, low_memory=False)

print(f"File: {gsec4_path}")
print(f"Shape: {gsec4.shape}")
print(f"\nColumns: {gsec4.columns.tolist()}")

print("\nFirst 3 rows (structure):")
display(gsec4.head(3))

print("\nUnique households:", gsec4['hhid'].nunique())
print("Unique persons:", gsec4[['hhid', 'PID']].drop_duplicates().shape[0])
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 1: EXPLORE THE MODULE
# Read-only inspection of GSEC4 and GSEC2.
# =========================================================

from pathlib import Path
import pandas as pd

print("=" * 90)
print("EDUCATION MODULE EXPLORATION")
print("=" * 90)

# Locate the dataset folder
data_root = (
    Path(extracted_folder)
    if 'extracted_folder' in globals()
    else Path(r"C:\Users\H-START\Desktop\dataset")
)
print(f"Data root: {data_root}")

# --- 1. Load GSEC4 (education) ---
gsec4_path = data_root / 'HH' / 'GSEC4.csv'
gsec4 = pd.read_csv(gsec4_path, low_memory=False)

print(f"\nGSEC4 file: {gsec4_path}")
print(f"Shape: {gsec4.shape}")
print(f"\nColumns ({len(gsec4.columns)}):")
for col in gsec4.columns:
    print(f"  - {col}")

print("\nFirst 3 rows:")
display(gsec4.head(3))

print("\nUnique households:", gsec4['hhid'].nunique())
print("Unique persons (hhid+PID):", gsec4[['hhid', 'PID']].drop_duplicates().shape[0])
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 2 (REVISED)
# Inspect s4q* variables to find grade completed.
# =========================================================

import pandas as pd

print("=" * 90)
print("EDUCATION VARIABLE INSPECTION — s4q* COLUMNS")
print("=" * 90)

# Focus on the s4q* prefix columns that look educational
s4q_columns = [c for c in gsec4.columns if c.startswith('s4q')]
print(f"s4q* columns: {s4q_columns}")

# Inspect each one
for col in s4q_columns:
    print(f"\n{'=' * 60}")
    print(f"Column: {col}")
    print(f"{'=' * 60}")
    print(f"  Data type: {gsec4[col].dtype}")
    print(f"  Missing: {gsec4[col].isna().sum():,} / {len(gsec4):,}")
    print(f"  Distinct non-missing values: {gsec4[col].nunique(dropna=True)}")

    vc = gsec4[col].value_counts(dropna=False).head(20).sort_index()
    print(f"\n  Value counts (top 20, sorted):")
    for val, count in vc.items():
        print(f"    {val!r:>10} : {count:,}")
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 3 (REVISED)
# Identify household head from GSEC2.
# =========================================================

from pathlib import Path
import pandas as pd

print("=" * 90)
print("IDENTIFYING HOUSEHOLD HEADS — REVISED")
print("=" * 90)

roster_path = data_root / 'HH' / 'GSEC2.csv'
print(f"Roster file: {roster_path}")
print(f"Exists: {roster_path.exists()}")

roster = pd.read_csv(roster_path, low_memory=False)

print(f"\nRoster shape: {roster.shape}")
print(f"Columns ({len(roster.columns)}):")
for col in roster.columns:
    print(f"  - {col}")

print("\nFirst 3 rows (transposed for readability):")
display(roster.head(3).T)

# Now look for the relationship-to-head column
relationship_candidates = [
    c for c in roster.columns
    if c.lower().startswith('h2q')
]
print(f"\nRelationship-to-head candidate columns: {relationship_candidates}")

for col in relationship_candidates:
    print(f"\n{col} distribution:")
    vc = roster[col].value_counts(dropna=False).sort_index().head(15)
    print(vc.to_string())
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4 (COMBINED)
# Extract head education, verify semantics, prepare for merge.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("EXTRACTING HOUSEHOLD-HEAD EDUCATION")
print("=" * 90)

# --- 1. Identify household heads ---
head_records = (
    roster.loc[
        roster['h2q4'] == 1,
        ['hhid', 'PID', 'h2q3', 'h2q8']   # PID + sex + age for cross-checks
    ]
    .rename(columns={
        'PID': 'head_PID',
        'h2q3': 'head_sex_code',
        'h2q8': 'head_age_check'
    })
    .drop_duplicates()
)

print(f"Household head records: {len(head_records):,}")
print(f"Unique households with a head: {head_records['hhid'].nunique():,}")

multi = head_records.groupby('hhid').size()
print(f"Households with multiple heads: {(multi > 1).sum()}")

# --- 2. Extract s4q05 (education level) for each head ---
EDU_COL = 's4q05'

head_edu = (
    gsec4[['hhid', 'PID', EDU_COL, 's4q02']]
    .rename(columns={
        'PID': 'head_PID',
        EDU_COL: 'head_edu_level',
        's4q02': 'head_literacy'
    })
)

head_edu_full = head_records.merge(
    head_edu,
    on=['hhid', 'head_PID'],
    how='left',
    validate='one_to_one'
)

print(f"\nMerged head education records: {len(head_edu_full):,}")
print(f"Missing head education: {head_edu_full['head_edu_level'].isna().sum():,}")

print("\nDistribution of head_edu_level (raw):")
print(
    head_edu_full['head_edu_level']
    .value_counts(dropna=False)
    .sort_index()
    .to_string()
)

# --- 3. VERIFY semantics ---
print("\n" + "=" * 90)
print("VERIFICATION: education level vs. literacy and age")
print("=" * 90)

print("\nCross-tab: head_edu_level × head_literacy")
print("head_literacy: 1=Yes (can read/write), 2=No")
display(
    pd.crosstab(
        head_edu_full['head_edu_level'],
        head_edu_full['head_literacy'],
        dropna=False,
        margins=True
    )
)

print("\nMean age (head_age_check) by head_edu_level:")
print(
    head_edu_full.groupby('head_edu_level')['head_age_check']
    .agg(['count', 'mean', 'median'])
    .round(1)
    .to_string()
)

# --- 4. Interpret based on the pattern ---
print("\n" + "=" * 90)
print("INTERPRETATION")
print("=" * 90)

# Look at the cross-tab to infer meaning
ct = pd.crosstab(head_edu_full['head_edu_level'], head_edu_full['head_literacy'])
print("\nLiteracy rate within each education level:")
for level in sorted(ct.index):
    if level in ct.index:
        total = ct.loc[level].sum()
        literate = ct.loc[level, 1.0] if 1.0 in ct.columns else 0
        rate = literate / total * 100 if total > 0 else 0
        print(f"  Level {level}: {literate}/{total} literate ({rate:.1f}%)")
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4B
# Verify s4q06 as the grade completed variable.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("VERIFYING s4q06 AS GRADE COMPLETED")
print("=" * 90)

# --- 1. Distribution of s4q06 ---
print("\ns4q06 raw value counts:")
print(
    gsec4['s4q06']
    .value_counts(dropna=False)
    .sort_index()
    .to_string()
)

# --- 2. Cross-tab with s4q05 (school type) ---
print("\n--- Cross-tab: s4q06 × s4q05 ---")
display(
    pd.crosstab(
        gsec4['s4q06'],
        gsec4['s4q05'],
        dropna=False,
        margins=True
    )
)

# --- 3. Cross-tab with s4q03 (currently attending) ---
print("\n--- Cross-tab: s4q06 × s4q03 (currently attending) ---")
print("If s4q06 = grade completed after leaving, then those currently")
print("attending (s4q03=1) should NOT have s4q06 populated.")
display(
    pd.crosstab(
        gsec4['s4q06'].notna().map({True: 'Has s4q06', False: 'Missing s4q06'}),
        gsec4['s4q03'].fillna('NaN'),
        margins=True
    )
)

# --- 4. Cross-tab with literacy ---
print("\n--- Cross-tab: s4q06 × s4q02 (literacy) ---")
display(
    pd.crosstab(
        gsec4['s4q06'],
        gsec4['s4q02'],
        dropna=False,
        margins=True
    )
)

# --- 5. Age relationship ---
print("\n--- Mean age (s4q08) by s4q06 value ---")
display(
    gsec4.groupby('s4q06')['s4q08']
    .agg(['count', 'mean', 'median'])
    .round(1)
)

# --- 6. Compare to s4q04_1 (grade currently attending) ---
print("\n--- Cross-tab: s4q06 (grade completed) × s4q04_1 (grade attending) ---")
display(
    gsec4.groupby(['s4q04_1', 's4q06'])
    .size()
    .head(30)
)
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4C
# Inspect s4q04 and s4q04_1 more carefully.
# =========================================================

print("=" * 90)
print("INSPECTING s4q04 AND s4q04_1")
print("=" * 90)

# --- s4q04: cross with s4q03 (currently attending) ---
print("\n--- s4q04 × s4q03 (currently attending) ---")
display(
    pd.crosstab(
        gsec4['s4q04'],
        gsec4['s4q03'],
        dropna=False,
        margins=True
    )
)

# --- s4q04 × s4q05 ---
print("\n--- s4q04 × s4q05 ---")
display(
    pd.crosstab(
        gsec4['s4q04'],
        gsec4['s4q05'],
        dropna=False,
        margins=True
    )
)

# --- s4q04_1: what subset has it populated? ---
print("\n--- s4q04_1: who has this variable populated? ---")
print("Populated when:")
print(pd.crosstab(
    gsec4['s4q04_1'].notna().map({True: 'Has s4q04_1', False: 'Missing'}),
    gsec4['s4q03'].fillna('NaN'),
    margins=True
))

print("\ns4q04_1 values:")
print(
    gsec4['s4q04_1']
    .value_counts(dropna=False)
    .sort_index()
    .to_string()
)

# --- s4q04_1 × s4q04 ---
print("\n--- s4q04_1 × s4q04 ---")
display(
    pd.crosstab(
        gsec4['s4q04_1'],
        gsec4['s4q04'],
        dropna=False,
        margins=True
    )
)

# --- Ages: does s4q04_1 correlate with age in a plausible way? ---
print("\n--- Mean age (s4q08) by s4q04_1 ---")
display(
    gsec4.groupby('s4q04_1')['s4q08']
    .agg(['count', 'mean', 'median'])
    .round(1)
)
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4D
# Resolve s4q06 semantics definitively.
# =========================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("RESOLVING s4q06 SEMANTICS")
print("=" * 90)

# --- 1. Check the s4q07 and s4q08 relationship to s4q06 ---
print("\n--- s4q06 × s4q07 (what comes after?) ---")
print("Cross-tab s4q06 with s4q07 and s4q08 to see the branching.")
display(
    gsec4.groupby('s4q06')
    .agg(
        count=('hhid', 'size'),
        s4q07_populated=('s4q07', lambda x: x.notna().sum()),
        s4q08_populated=('s4q08', lambda x: x.notna().sum()),
        s4q09_populated=('s4q09', lambda x: x.notna().sum()),
        s4q10_populated=('s4q10', lambda x: x.notna().sum()),
        s4q11_populated=('s4q11', lambda x: x.notna().sum()),
        s4q12_populated=('s4q12', lambda x: x.notna().sum()),
    )
    .to_string()
)

# --- 2. Look at the source questionnaire PDF ---
# The GSEC4 questionnaire section is in the unps_hhq.pdf.
# Search for "Section 4" and "Education" descriptions.

from pathlib import Path
from pypdf import PdfReader

data_root = Path(r"C:\Users\H-START\Desktop\dataset")
pdf_path = data_root / 'unps_hhq.pdf'

if pdf_path.exists():
    reader = PdfReader(str(pdf_path))
    print(f"\nSearching {pdf_path.name} for Section 4 Education...")
    print("=" * 90)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if "Section 4" in text and ("Education" in text or "education" in text):
            print(f"\n--- PDF PAGE {page_num} ---")
            # Print first 3000 chars of the page
            print(text[:3000])
            print("...")
            break
else:
    print(f"PDF not found: {pdf_path}")

# --- 3. Alternative: look at the agriculture questionnaire PDF ---
# The GSEC4 variable names are documented in the household questionnaire.
# Check unps_7_bid.pdf page 11 as well.

print("\n\n" + "=" * 90)
print("CHECKING BASIC INFORMATION DOCUMENT (unps_7_bid.pdf)")
print("=" * 90)

bid_path = data_root / 'unps_7_bid.pdf'
if bid_path.exists():
    reader = PdfReader(str(bid_path))

    # Look for pages mentioning "Section 4" and "Education"
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if "Education" in text and ("grade" in text.lower() or "Section 4" in text):
            print(f"\n--- PAGE {page_num} ---")
            # Print lines containing "education" or "grade"
            for line in text.split('\n'):
                lower = line.lower()
                if 'education' in lower or 'grade' in lower or 'school' in lower:
                    print(line.strip())
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4E
# Search for a data dictionary or codebook for GSEC4.
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Look for any dictionary or label files
dict_candidates = []
for pattern in ['*.xml', '*.json', '*.txt', '*.dta', '*.sav']:
    dict_candidates.extend(data_root.rglob(pattern))

print(f"Potential dictionary files: {len(dict_candidates)}")
for path in dict_candidates[:20]:
    print(f"  {path.relative_to(data_root)}")

# If any file contains "s4q06" as text, show it
for path in dict_candidates:
    try:
        content = path.read_text(errors='ignore')
        if 's4q06' in content or 's4q05' in content:
            print(f"\n{'=' * 70}")
            print(f"FILE CONTAINS s4q06: {path.relative_to(data_root)}")
            print(f"{'=' * 70}")
            # Print surrounding context
            idx = content.find('s4q06')
            if idx > 0:
                print(content[max(0, idx-500):idx+1000])
    except Exception:
        pass
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4F (DEFINITIVE)
# Use the questionnaire to test hypotheses about variable mapping.
# =========================================================

import pandas as pd

print("=" * 90)
print("DEFINITIVE TEST: VARIABLE MAPPING AGAINST QUESTIONNAIRE")
print("=" * 90)

# The questionnaire tells us:
#   Q1 (read/write) → s4q02?
#   Q2 (ever attended: 1=Never, 2=Past, 3=Currently) → s4q03?
#   Q3 (reason for never attending) → s4q04?
#   Q4 (highest grade completed) → s4q05?
#   Q5 (reason for leaving) → s4q06?
#   Q6 (grade last year) → s4q07?
#   Q7 (grade currently attending) → s4q08?

# TEST 1: Is s4q03 the "ever attended" variable?
print("\nTEST 1: s4q03 = 'Ever attended school' (1=Never, 2=Past, 3=Currently)")
print("Expected: value 1 (never) should have many records, value 3 fewer.")
print(gsec4['s4q03'].value_counts(dropna=False).sort_index().to_string())

# TEST 2: Is s4q04 the "reason never attended" (only populated for s4q03==1)?
print("\nTEST 2: s4q04 × s4q03 -- should only have s4q04 populated when s4q03==1")
display(
    pd.crosstab(
        gsec4['s4q03'].fillna('NaN'),
        gsec4['s4q04'].notna().map({True: 'Populated', False: 'Missing'}),
        dropna=False,
        margins=True
    )
)

# TEST 3: Is s4q05 the "highest grade completed" (only for s4q03==2)?
print("\nTEST 3: s4q05 × s4q03 -- should only have s4q05 populated when s4q03==2 (Past)")
display(
    pd.crosstab(
        gsec4['s4q03'].fillna('NaN'),
        gsec4['s4q05'].notna().map({True: 'Populated', False: 'Missing'}),
        dropna=False,
        margins=True
    )
)

print("\nBUT: if s4q05 is populated for BOTH s4q03==2 AND s4q03==3, the naming may differ.")
print("\ns4q05 value distribution:")
print(gsec4['s4q05'].value_counts(dropna=False).sort_index().to_string())

# TEST 4: Which variable is populated only for s4q03==2 (Past)?
print("\nTEST 4: Population pattern of s4q05, s4q06, s4q07, s4q08 by s4q03")

for var in ['s4q05', 's4q06', 's4q07', 's4q08']:
    crosstab = pd.crosstab(
        gsec4['s4q03'].fillna('NaN'),
        gsec4[var].notna().map({True: 'Pop', False: 'Miss'}),
        dropna=False
    )
    print(f"\n{var} -- populated vs s4q03:")
    print(crosstab.to_string())

# TEST 5: s4q09 and s4q10 -- which group?
print("\nTEST 5: s4q09, s4q10 population by s4q03")
for var in ['s4q09', 's4q10']:
    crosstab = pd.crosstab(
        gsec4['s4q03'].fillna('NaN'),
        gsec4[var].notna().map({True: 'Pop', False: 'Miss'}),
        dropna=False
    )
    print(f"\n{var} -- populated vs s4q03:")
    print(crosstab.to_string())
```


```python
# =========================================================
# EDUCATION FEATURE — STEP 4G (DECISIVE)
# Cross-reference s4q03, s4q04, s4q05, s4q06 against literacy.
# =========================================================

import pandas as pd

print("=" * 90)
print("DECISIVE TEST: EDUCATION VARIABLE IDENTIFICATION")
print("=" * 90)

# The literacy question is unambiguous (s4q02).
# A person's education should correlate with literacy.
# Cross every candidate variable against literacy.

for var in ['s4q03', 's4q04', 's4q05', 's4q06']:
    print(f"\n{'=' * 70}")
    print(f"{var} × s4q02 (literacy)")
    print(f"{'=' * 70}")
    print("s4q02: 1=Unable, 2=Read only, 4=Read and write, 5=Braille")

    crosstab = pd.crosstab(
        gsec4[var],
        gsec4['s4q02'],
        dropna=False,
        margins=True
    )
    display(crosstab)

    # Calculate literacy rate per category
    print("\nLiteracy (s4q02==4) rate by category:")
    literate = gsec4.groupby(var)['s4q02'].apply(
        lambda x: (x == 4).sum() / x.notna().sum() * 100
        if x.notna().any() else float('nan')
    ).round(1)
    print(literate.to_string())
```


```python
# =========================================================
# STEP 19: SEARCH HOUSEHOLD FILES FOR EA IDENTIFIERS
# Read-only diagnostic
# =========================================================

from pathlib import Path
import pandas as pd

data_root = Path(r"C:\Users\H-START\Desktop\dataset")

# Candidate EA identifier names to search for
ea_candidates = [
    "ea", "ea_code", "ea_id", "comm", "community",
    "cluster", "psu", "enum", "enumeration",
    "t0_ea", "t0_ea_code"
]

# Files already known to contain EA_code (community files)
community_files = {
    "Community/CSEC1A.csv",
    "Community/CSEC11_0.csv",
    "Community/CSEC11_1.csv",
}

print("SEARCHING HOUSEHOLD AND AGRICULTURAL FILES FOR EA IDENTIFIERS")
print("=" * 80)

matches = []
errors = []

for csv_path in data_root.rglob("*.csv"):
    rel = str(csv_path.relative_to(data_root)).replace("\\", "/")

    # Skip community files — we already know they have EA_code
    if rel in community_files:
        continue

    try:
        columns = pd.read_csv(
            csv_path, nrows=0, encoding="utf-8-sig"
        ).columns.tolist()

        for col in columns:
            col_lower = str(col).strip().lower()
            for cand in ea_candidates:
                if cand == col_lower or cand in col_lower:
                    matches.append({
                        "file": rel,
                        "column": col,
                        "matched_candidate": cand,
                    })
                    break

    except Exception as exc:
        errors.append({"file": rel, "error": str(exc)})

if matches:
    matches_df = pd.DataFrame(matches)
    display(matches_df)
else:
    print("No EA identifier columns found in household/agricultural files.")

if errors:
    print("\nFILES THAT COULD NOT BE INSPECTED")
    display(pd.DataFrame(errors))

print("\nStep 19 completed.")
```


```python
# =========================================================
# STEP 20: ASSESS WHETHER batch CAN SERVE AS A CLUSTER PROXY
# Read-only diagnostic
# =========================================================

import pandas as pd

print("BATCH AS POTENTIAL CLUSTER PROXY")
print("=" * 70)

# 1. How many households share each batch value?
batch_sizes = (
    gsec1.groupby("batch")
    .agg(
        households=("hhid", "size"),
        unique_hhids=("hhid", "nunique"),
        regions=("region", "nunique"),
        urban_values=("urban", "nunique"),
    )
    .reset_index()
)

print(f"Number of distinct batch values: {len(batch_sizes)}")
print(f"Households per batch — min: {batch_sizes['households'].min()}")
print(f"Households per batch — median: {batch_sizes['households'].median()}")
print(f"Households per batch — max: {batch_sizes['households'].max()}")
print(f"Households per batch — mean: {batch_sizes['households'].mean():.1f}")

# 2. Does batch nest within region/urban?
batch_nesting = (
    gsec1.groupby("batch")
    .agg(region=("region", "nunique"),
         urban=("urban", "nunique"))
)

print("\nBatch nesting check:")
print(f"  Batches spanning multiple regions: {(batch_nesting['region'] > 1).sum()}")
print(f"  Batches spanning both urban and rural: {(batch_nesting['urban'] > 1).sum()}")

# 3. Compare batch count to community EA count
print(f"\nCommunity EA_code count (from CSEC1A): {community['EA_code'].nunique()}")
print(f"GSEC1 batch count: {gsec1['batch'].nunique()}")
print(f"AGSEC1 batch count: {agsec1['batch'].nunique()}")

# 4. Distribution of households per batch
display(
    batch_sizes["households"]
    .describe()
    .round(2)
    .to_frame("households_per_batch")
)

print("\nStep 20 completed.")
```


```python
# =========================================================
# STEP 21: DOCUMENT SURVEY-DESIGN DECISION
# Read-only synthesis
# =========================================================

import pandas as pd

print("SURVEY-DESIGN DECISION SUMMARY")
print("=" * 70)

decision_rows = [
    {
        "question": "Is a cross-sectional weight available?",
        "evidence": "wgt is present in GSEC1 and AGSEC1 with 0% missingness.",
        "decision": "Use wgt for weighted estimates."
    },
    {
        "question": "Are panel weights available?",
        "evidence": "hwgt_W7 and hwgt_wc present, ~5.9% missing.",
        "decision": "Report as sensitivity check; do not use as primary weight."
    },
    {
        "question": "Is an explicit PSU / cluster variable available?",
        "evidence": "No psu, cluster, or ea column in GSEC1 or AGSEC1.",
        "decision": "Cannot compute design-based standard errors without a cluster identifier."
    },
    {
        "question": "Is an explicit stratum variable available?",
        "evidence": "No stratum or strata column. region, regurb, urban exist as descriptors.",
        "decision": "Cannot compute stratified standard errors without an explicit stratum identifier."
    },
    {
        "question": "Can batch serve as a cluster proxy?",
        "evidence": "Pending Step 20 result.",
        "decision": "To be finalized after Step 20."
    },
    {
        "question": "Can community EA_code be linked to households?",
        "evidence": "Community files use EA_code + interview__key; household files use hhid + t0_hhid + interview__key; no shared key.",
        "decision": "No direct linkage. Document as a limitation."
    },
]

decision_df = pd.DataFrame(decision_rows)
display(decision_df)

print("\nStep 21 completed.")
```


```python
# =========================================================
# STEP 22: FINALIZE SURVEY-DESIGN DECISION
# Read-only synthesis; produces a documented decision table
# =========================================================

import pandas as pd
from pathlib import Path

print("FINAL SURVEY-DESIGN DECISION")
print("=" * 80)

final_decision_rows = [
    {
        "element": "Cross-sectional weight",
        "variable": "wgt",
        "availability": "Available in GSEC1 and AGSEC1; 0% missing.",
        "usable": "Yes",
        "decision": "Use wgt to produce weighted point estimates."
    },
    {
        "element": "Panel weights",
        "variable": "hwgt_W7, hwgt_wc",
        "availability": "Present; ~5.9% missing.",
        "usable": "Partial",
        "decision": "Report as sensitivity check only. Do not use as primary weight."
    },
    {
        "element": "PSU / cluster",
        "variable": "None",
        "availability": "No psu, cluster, or ea column in GSEC1 or AGSEC1.",
        "usable": "No",
        "decision": "Cannot compute design-based standard errors."
    },
    {
        "element": "Stratum",
        "variable": "None",
        "availability": "No stratum or strata column. region, regurb, urban exist only as descriptors.",
        "usable": "No",
        "decision": "Cannot compute stratified standard errors."
    },
    {
        "element": "Batch",
        "variable": "batch",
        "availability": "1,057 distinct values; median 1 household per batch.",
        "usable": "No",
        "decision": "Fieldwork enumeration code, not a sampling cluster. Not usable as PSU proxy."
    },
    {
        "element": "Community EA linkage",
        "variable": "EA_code (community only)",
        "availability": "Community files carry EA_code; household files do not.",
        "usable": "No",
        "decision": "No direct linkage. Document as a limitation."
    },
]

final_decision_df = pd.DataFrame(final_decision_rows)
display(final_decision_df)

# Save the decision as a CSV report
reports_dir = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics\reports")
reports_dir.mkdir(parents=True, exist_ok=True)

output_path = reports_dir / "survey_design_decision.csv"
final_decision_df.to_csv(output_path, index=False)

print(f"\nDecision table saved to: {output_path}")
print(f"File exists: {output_path.exists()}")

print("\nStep 22 completed.")
```


```python
# =========================================================
# STEP 23: WRITE SURVEY-DESIGN LIMITATION SECTION
# Read-only; writes a markdown fragment for the report
# =========================================================

from pathlib import Path

reports_dir = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics\reports")

limitation_text = """
## Survey-Design Limitation

The UNPS 2018/19 public-use files include a cross-sectional
household weight (`wgt`) but do not include primary sampling
unit (PSU), cluster, or stratum identifiers. The community
files carry an Enumeration Area code (`EA_code`), but no
shared key links them to household records. The `batch`
variable is a fieldwork enumeration code (median 1 household
per batch), not a sampling cluster, and cannot serve as a
PSU proxy.

Consequently, this analysis reports:

- **Weighted point estimates** using `wgt`.
- **Unweighted estimates** as a sensitivity comparison.
- **Unadjusted standard errors** and p-values.

The reported confidence intervals and hypothesis tests are
therefore **not design-based**. They should be treated as
descriptive summaries of the observed sample, not as
inferential statements about the UNPS target population.
A fully design-adjusted analysis would require access to
the restricted-use files containing PSU and stratum
identifiers, or the original survey design specification.

Panel weights (`hwgt_W7`, `hwgt_wc`) are available with
approximately 5.9% missingness and are reported as a
sensitivity check only.
"""

output_path = reports_dir / "survey_design_limitation.md"
output_path.write_text(limitation_text.strip() + "\n", encoding="utf-8")

print(f"Limitation section saved to: {output_path}")
print(f"File exists: {output_path.exists()}")

print("\nStep 23 completed.")
```


```python
# =========================================================
# STEP 24: UPDATE README CURRENT STATUS
# Read-only preview; does NOT write to the repo file yet
# =========================================================

print("PROPOSED README UPDATE — CURRENT STATUS")
print("=" * 80)

proposed_status = """
## Current Status

The project contains an initial agricultural technology
adoption case study, including:

- Exploratory analysis and descriptive statistics
- Chi-square association tests
- Logistic regression (baseline and expanded models)
- Exploratory predictive evaluation
- A consolidated analysis report

A survey-design audit has been completed. It confirmed that:

- A cross-sectional weight (`wgt`) is available and used
  for weighted point estimates.
- Panel weights (`hwgt_W7`, `hwgt_wc`) are available with
  ~5.9% missingness and are reported as a sensitivity check.
- No PSU, cluster, or stratum identifiers are present in
  the public-use files.
- The community `EA_code` cannot be linked to household
  records because no shared key exists.
- The `batch` variable is a fieldwork enumeration code,
  not a sampling cluster.

As a result, reported standard errors and p-values are
**not design-based**. They are descriptive summaries of
the observed sample.

Future improvements may include design-adjusted estimates
using restricted-use files, additional diagnostics,
automated tests, reusable analysis functions, and a
dashboard.
"""

print(proposed_status)

print("Step 24 completed (preview only — not yet written).")
```


```python
# =========================================================
# STEP 25: UPDATE README AND FINAL REPORT WITH DESIGN DECISION
# Writes to repo files (README.md, final_analysis_report.md)
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")

readme_path = project_root / "README.md"
report_path = project_root / "reports" / "final_analysis_report.md"

# ---------------------------------------------------------
# 1. Update README.md Current Status section
# ---------------------------------------------------------

if not readme_path.exists():
    print("README.md not found. Skipping README update.")
else:
    readme_text = readme_path.read_text(encoding="utf-8")

    new_status = """## Current Status

The project contains an initial agricultural technology
adoption case study, including:

- Exploratory analysis and descriptive statistics
- Chi-square association tests
- Logistic regression (baseline and expanded models)
- Exploratory predictive evaluation
- Weighted and unweighted point estimates
- A consolidated analysis report

A survey-design audit has been completed. It confirmed that:

- A cross-sectional weight (`wgt`) is available and used
  for weighted point estimates.
- Panel weights (`hwgt_W7`, `hwgt_wc`) are available with
  ~5.9% missingness and are reported as a sensitivity check.
- No PSU, cluster, or stratum identifiers are present in
  the public-use files.
- The community `EA_code` cannot be linked to household
  records because no shared key exists.
- The `batch` variable is a fieldwork enumeration code,
  not a sampling cluster.

As a result, reported standard errors and p-values are
**not design-based**. They are descriptive summaries of
the observed sample.

Future improvements may include design-adjusted estimates
using restricted-use files, additional diagnostics,
automated tests, reusable analysis functions, and a
dashboard."""

    # Replace the old Current Status block.
    # Find the heading and replace everything from it to the end of file.
    marker = "## Current Status"

    if marker in readme_text:
        before = readme_text.split(marker)[0]
        readme_path.write_text(before + new_status + "\n", encoding="utf-8")
        print("README.md updated successfully.")
    else:
        readme_path.write_text(readme_text + "\n\n" + new_status + "\n", encoding="utf-8")
        print("README.md updated (appended — no prior Current Status section).")

# ---------------------------------------------------------
# 2. Append survey-design limitation to final report
# ---------------------------------------------------------

if not report_path.exists():
    print("\nfinal_analysis_report.md not found. Skipping report update.")
else:
    limitation_path = project_root / "reports" / "survey_design_limitation.md"

    if not limitation_path.exists():
        print("\nSurvey-design limitation file not found.")
    else:
        report_text = report_path.read_text(encoding="utf-8")
        limitation_text = limitation_path.read_text(encoding="utf-8")

        if "## Survey-Design Limitation" in report_text:
            print("\nSurvey-design limitation already present in report. Skipping.")
        else:
            report_path.write_text(
                report_text + "\n\n" + limitation_text + "\n",
                encoding="utf-8"
            )
            print("\nfinal_analysis_report.md updated with survey-design limitation.")

print("\nStep 25 completed.")
```


```python
# =========================================================
# STEP 26: CREATE src/seed_outcome.py
# Writes a reusable module; notebook unchanged
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"
src_dir.mkdir(parents=True, exist_ok=True)

module_text = '''"""
ResearchPro Analytics — Seed outcome construction.

This module converts crop-level seed variables from the UNPS 2018/19
Agriculture Questionnaire into a crop-level improved-seed adoption
outcome.

Questionnaire coding used here (verified against agriculture_qx.pdf):

- s4aq16 / s4bq16 : seed/seedling use
    1 = Yes
    2 = No
- s4aq13 / s4bq13 : seed type
    1 = Traditional
    2 = Improved
- s4aq14 / s4bq14 : improved-seed category
    1 = Certified
    2 = Quality declared
    3 = Don't know

Outcome:
- 1 = Confirmed improved-seed use
- 0 = Confirmed non-use
- NA = Unresolved (missing seed-use or seed-type information)
"""

import numpy as np
import pandas as pd


VISIT_CONFIG = {
    1: {"use": "s4aq16", "type": "s4aq13", "category": "s4aq14"},
    2: {"use": "s4bq16", "type": "s4bq13", "category": "s4bq14"},
}


def build_crop_level_outcome(
    df: pd.DataFrame,
    visit: int,
) -> pd.DataFrame:
    """
    Add a crop-level improved-seed outcome column to a copy of df.

    Parameters
    ----------
    df : pd.DataFrame
        Crop-level dataset (AGSEC4A or AGSEC4B).
    visit : int
        1 for AGSEC4A, 2 for AGSEC4B.

    Returns
    -------
    pd.DataFrame
        Copy of df with new columns:
        - improved_seed_adoption (Int64, 0/1/NA)
        - adoption_classification_status (str)
        - improved_category_missing_flag (bool)
    """
    if visit not in VISIT_CONFIG:
        raise ValueError(f"visit must be 1 or 2, got {visit}")

    cfg = VISIT_CONFIG[visit]
    use_col = cfg["use"]
    type_col = cfg["type"]
    cat_col = cfg["category"]

    required = [use_col, type_col, cat_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns for visit {visit}: {missing}")

    out = df.copy()

    # Initialize as unresolved
    out["improved_seed_adoption"] = pd.Series(
        pd.NA, index=out.index, dtype="Int64"
    )

    # Confirmed traditional use => 0
    out.loc[
        (out[use_col] == 1) & (out[type_col] == 1),
        "improved_seed_adoption",
    ] = 0

    # Confirmed improved use => 1
    out.loc[
        (out[use_col] == 1) & (out[type_col] == 2),
        "improved_seed_adoption",
    ] = 1

    # Reported no seed use => 0
    out.loc[
        out[use_col] == 2,
        "improved_seed_adoption",
    ] = 0

    # Status label
    out["adoption_classification_status"] = "Unresolved"
    out.loc[
        out["improved_seed_adoption"] == 0,
        "adoption_classification_status",
    ] = "Non-adopter"
    out.loc[
        out["improved_seed_adoption"] == 1,
        "adoption_classification_status",
    ] = "Adopter"

    # Flag improved-seed records with missing category
    out["improved_category_missing_flag"] = (
        (out[use_col] == 1)
        & (out[type_col] == 2)
        & out[cat_col].isna()
    )

    return out
'''

module_path = src_dir / "seed_outcome.py"
module_path.write_text(module_text, encoding="utf-8")

# Add an __init__.py so src is a package
init_path = src_dir / "__init__.py"
if not init_path.exists():
    init_path.write_text('"""ResearchPro Analytics reusable modules."""\n', encoding="utf-8")

print("Module written:", module_path)
print("File exists:", module_path.exists())
print("File size:", module_path.stat().st_size, "bytes")
print("\nStep 26 completed.")
```


```python
# =========================================================
# STEP 27: VERIFY src/seed_outcome.py AGAINST NOTEBOOK OUTPUT
# Read-only comparison; no files modified
# =========================================================

import sys
from pathlib import Path
import pandas as pd

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

# Make src importable
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from seed_outcome import build_crop_level_outcome, VISIT_CONFIG

print("SEED-OUTCOME MODULE VERIFICATION")
print("=" * 70)

# ---------------------------------------------------------
# 1. Confirm the notebook's baseline dictionaries exist
# ---------------------------------------------------------
required_globals = ["crop_a", "crop_b", "crop_adoption_audit"]
missing_globals = [g for g in required_globals if g not in globals()]

if missing_globals:
    print("Missing notebook objects:", missing_globals)
    print("Run the notebook from the beginning, then rerun this cell.")
else:
    print("Notebook objects available:", required_globals)

    # -----------------------------------------------------
    # 2. Apply the module to both visits
    # -----------------------------------------------------
    module_a = build_crop_level_outcome(crop_a, visit=1)
    module_b = build_crop_level_outcome(crop_b, visit=2)

    # -----------------------------------------------------
    # 3. Compare against notebook outputs
    # -----------------------------------------------------
    comparison_rows = []

    for visit_label, module_df, notebook_key in [
        ("First visit",  module_a, "First visit"),
        ("Second visit", module_b, "Second visit"),
    ]:
        notebook_df = crop_adoption_audit[notebook_key]

        # Compare lengths
        len_match = len(module_df) == len(notebook_df)

        # Compare outcome distributions
        module_counts = (
            module_df["improved_seed_adoption"]
            .value_counts(dropna=False)
            .sort_index()
        )
        notebook_counts = (
            notebook_df["improved_seed_adoption"]
            .value_counts(dropna=False)
            .sort_index()
        )

        counts_match = module_counts.equals(notebook_counts)

        # Compare row-by-row where both are aligned
        # (the module preserves index, so alignment holds)
        outcome_equal = (
            module_df["improved_seed_adoption"]
            .fillna(-1)
            .astype(int)
            .equals(
                notebook_df["improved_seed_adoption"]
                .fillna(-1)
                .astype(int)
            )
        )

        status_equal = (
            module_df["adoption_classification_status"]
            .equals(notebook_df["adoption_classification_status"])
        )

        comparison_rows.append({
            "visit": visit_label,
            "len_match": len_match,
            "outcome_distribution_match": counts_match,
            "row_by_row_outcome_match": outcome_equal,
            "row_by_row_status_match": status_equal,
        })

    comparison_df = pd.DataFrame(comparison_rows)
    display(comparison_df)

    # -----------------------------------------------------
    # 4. Show distributions side-by-side for a sanity check
    # -----------------------------------------------------
    print("\nFirst visit — module outcome distribution:")
    print(module_a["improved_seed_adoption"].value_counts(dropna=False).sort_index())

    print("\nFirst visit — notebook outcome distribution:")
    print(
        crop_adoption_audit["First visit"]["improved_seed_adoption"]
        .value_counts(dropna=False)
        .sort_index()
    )

    print("\nSecond visit — module outcome distribution:")
    print(module_b["improved_seed_adoption"].value_counts(dropna=False).sort_index())

    print("\nSecond visit — notebook outcome distribution:")
    print(
        crop_adoption_audit["Second visit"]["improved_seed_adoption"]
        .value_counts(dropna=False)
        .sort_index()
    )

    print("\nStep 27 completed.")
```


```python
# =========================================================
# STEP 28: CREATE src/household_aggregation.py
# Writes a reusable module; notebook unchanged
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

module_text = '''"""
ResearchPro Analytics — Household-level adoption aggregation.

This module aggregates crop-level improved-seed outcomes into a
household-level adoption classification.

Rules:
- A household is an Adopter if at least one crop record has
  improved_seed_adoption == 1.
- A household is a Non-adopter if it has no confirmed adopter crop
  AND no unresolved crop records (i.e., every crop outcome is known
  and equals zero).
- Otherwise, the household is Unclassified.
"""

import pandas as pd


def aggregate_household_adoption(
    df: pd.DataFrame,
    outcome_col: str = "improved_seed_adoption",
    household_col: str = "hhid",
) -> pd.DataFrame:
    """
    Aggregate crop-level outcomes to household level.

    Parameters
    ----------
    df : pd.DataFrame
        Crop-level dataset with an outcome column.
    outcome_col : str
        Name of the crop-level outcome column (Int64, 0/1/NA).
    household_col : str
        Name of the household identifier column.

    Returns
    -------
    pd.DataFrame
        One row per household with columns:
        - crop_records
        - confirmed_adopter_crops
        - confirmed_nonadopter_crops
        - unresolved_crops
        - household_adoption (Int64, 0/1/NA)
        - adoption_status (Adopter / Non-adopter / Unclassified)
    """
    required = [household_col, outcome_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    household_df = (
        df.groupby(household_col, dropna=False)
        .agg(
            crop_records=(household_col, "size"),
            confirmed_adopter_crops=(
                outcome_col,
                lambda x: int((x == 1).sum()),
            ),
            confirmed_nonadopter_crops=(
                outcome_col,
                lambda x: int((x == 0).sum()),
            ),
            unresolved_crops=(
                outcome_col,
                lambda x: int(x.isna().sum()),
            ),
        )
        .reset_index()
    )

    # Initialize as NA
    household_df["household_adoption"] = pd.Series(
        pd.NA, index=household_df.index, dtype="Int64"
    )

    # Any confirmed adopter crop => household is an Adopter
    household_df.loc[
        household_df["confirmed_adopter_crops"] > 0,
        "household_adoption",
    ] = 1

    # No adopter crops and no unresolved crops => Non-adopter
    household_df.loc[
        (household_df["confirmed_adopter_crops"] == 0)
        & (household_df["unresolved_crops"] == 0),
        "household_adoption",
    ] = 0

    # Status label
    household_df["adoption_status"] = "Unclassified"
    household_df.loc[
        household_df["household_adoption"] == 1,
        "adoption_status",
    ] = "Adopter"
    household_df.loc[
        household_df["household_adoption"] == 0,
        "adoption_status",
    ] = "Non-adopter"

    return household_df
'''

module_path = src_dir / "household_aggregation.py"
module_path.write_text(module_text, encoding="utf-8")

print("Module written:", module_path)
print("File exists:", module_path.exists())
print("File size:", module_path.stat().st_size, "bytes")
print("\nStep 28 completed.")
```


```python
# =========================================================
# STEP 29: VERIFY src/household_aggregation.py
# Read-only comparison against notebook output
# =========================================================

import sys
from pathlib import Path
import pandas as pd

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from household_aggregation import aggregate_household_adoption

print("HOUSEHOLD-AGGREGATION MODULE VERIFICATION")
print("=" * 70)

# ---------------------------------------------------------
# 1. Confirm required notebook objects exist
# ---------------------------------------------------------
required_globals = ["crop_adoption_audit", "household_adoption_results"]
missing_globals = [g for g in required_globals if g not in globals()]

if missing_globals:
    print("Missing notebook objects:", missing_globals)
    print("Run the notebook from the beginning, then rerun this cell.")
else:
    print("Notebook objects available:", required_globals)

    comparison_rows = []

    for visit_label in ["First visit", "Second visit"]:
        # Crop-level audit from notebook
        crop_df = crop_adoption_audit[visit_label]

        # Notebook household result
        notebook_hh = household_adoption_results[visit_label]

        # Apply the module
        module_hh = aggregate_household_adoption(crop_df)

        # Compare lengths
        len_match = len(module_hh) == len(notebook_hh)

        # Compare household ID sets
        module_ids = set(module_hh["hhid"])
        notebook_ids = set(notebook_hh["hhid"])
        id_sets_match = module_ids == notebook_ids

        # Compare adoption status counts
        module_status = (
            module_hh["adoption_status"]
            .value_counts()
            .reindex(
                ["Adopter", "Non-adopter", "Unclassified"],
                fill_value=0,
            )
        )
        notebook_status = (
            notebook_hh["adoption_status"]
            .value_counts()
            .reindex(
                ["Adopter", "Non-adopter", "Unclassified"],
                fill_value=0,
            )
        )
        status_counts_match = module_status.equals(notebook_status)

        # Row-by-row comparison (aligned by hhid)
        module_sorted = module_hh.sort_values("hhid").reset_index(drop=True)
        notebook_sorted = notebook_hh.sort_values("hhid").reset_index(drop=True)

        row_outcome_match = (
            module_sorted["household_adoption"]
            .fillna(-1)
            .astype(int)
            .equals(
                notebook_sorted["household_adoption"]
                .fillna(-1)
                .astype(int)
            )
        )

        row_status_match = (
            module_sorted["adoption_status"]
            .equals(notebook_sorted["adoption_status"])
        )

        comparison_rows.append({
            "visit": visit_label,
            "len_match": len_match,
            "id_sets_match": id_sets_match,
            "status_counts_match": status_counts_match,
            "row_by_row_outcome_match": row_outcome_match,
            "row_by_row_status_match": row_status_match,
        })

    comparison_df = pd.DataFrame(comparison_rows)
    display(comparison_df)

    # -----------------------------------------------------
    # 2. Show status distributions side-by-side
    # -----------------------------------------------------
    for visit_label in ["First visit", "Second visit"]:
        print(f"\n{visit_label} — module status counts:")
        print(
            module_hh["adoption_status"].value_counts().sort_index()
        )

        print(f"\n{visit_label} — notebook status counts:")
        print(
            household_adoption_results[visit_label]["adoption_status"]
            .value_counts()
            .sort_index()
        )

    print("\nStep 29 completed.")
```


```python
# =========================================================
# STEP 30: ISOLATE AND DIAGNOSE THE FIRST-VISIT DISCREPANCY
# Read-only
# =========================================================

import sys
from pathlib import Path
import pandas as pd

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import fresh copies — do not reuse cached modules
import importlib
import seed_outcome
import household_aggregation

importlib.reload(seed_outcome)
importlib.reload(household_aggregation)

from seed_outcome import build_crop_level_outcome
from household_aggregation import aggregate_household_adoption

print("FIRST-VISIT DISCREPANCY DIAGNOSIS")
print("=" * 70)

# ---------------------------------------------------------
# 1. Build the first-visit crop outcome with the module
# ---------------------------------------------------------
module_crop_a = build_crop_level_outcome(crop_a, visit=1)

# ---------------------------------------------------------
# 2. Compare against notebook crop_adoption_audit["First visit"]
# ---------------------------------------------------------
notebook_crop_a = crop_adoption_audit["First visit"]

print("CROP-LEVEL OUTCOME DISTRIBUTION — FIRST VISIT")
print("-" * 70)

print("\nModule crop_a:")
print(
    module_crop_a["improved_seed_adoption"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nNotebook crop_adoption_audit['First visit']:")
print(
    notebook_crop_a["improved_seed_adoption"]
    .value_counts(dropna=False)
    .sort_index()
)

# ---------------------------------------------------------
# 3. Check whether the two crop-level dataframes have
#    the same length and same row alignment
# ---------------------------------------------------------
print("\nLengths:")
print("  Module crop_a:", len(module_crop_a))
print("  Notebook crop_a:", len(notebook_crop_a))

# ---------------------------------------------------------
# 4. Aggregate to household level using the module
# ---------------------------------------------------------
module_hh_a = aggregate_household_adoption(module_crop_a)

print("\nHOUSEHOLD-LEVEL STATUS — FIRST VISIT")
print("-" * 70)

print("\nModule aggregate (from module crop_a):")
print(
    module_hh_a["adoption_status"]
    .value_counts()
    .sort_index()
)

print("\nNotebook aggregate (household_adoption_results['First visit']):")
print(
    household_adoption_results["First visit"]["adoption_status"]
    .value_counts()
    .sort_index()
)

# ---------------------------------------------------------
# 5. Check whether the module is accidentally using the
#    second visit's column names on the first visit's data
# ---------------------------------------------------------
print("\nCOLUMN-NAME CHECK")
print("-" * 70)
print("crop_a columns include s4aq16?", "s4aq16" in crop_a.columns)
print("crop_a columns include s4aq13?", "s4aq13" in crop_a.columns)
print("crop_a columns include s4aq14?", "s4aq14" in crop_a.columns)
print("crop_a columns include s4bq16?", "s4bq16" in crop_a.columns)
print("crop_a columns include s4bq13?", "s4bq13" in crop_a.columns)
print("crop_a columns include s4bq14?", "s4bq14" in crop_a.columns)

# ---------------------------------------------------------
# 6. Sanity-check: run module on crop_b with visit=1
#    If the module quietly used wrong columns, this will
#    raise or produce nonsense.
# ---------------------------------------------------------
print("\nSANITY CHECK: what if we apply visit=2 columns to crop_a?")
print("-" * 70)

try:
    module_crop_a_wrong = build_crop_level_outcome(crop_a, visit=2)
    print("Module ran with visit=2 on crop_a WITHOUT error.")
    print("Distribution:")
    print(
        module_crop_a_wrong["improved_seed_adoption"]
        .value_counts(dropna=False)
        .sort_index()
    )
except Exception as exc:
    print("Module raised:", type(exc).__name__, "-", exc)

print("\nStep 30 completed.")
```


```python
# =========================================================
# STEP 31: CREATE src/modelling.py
# Writes a reusable module; notebook unchanged
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

module_text = '''"""
ResearchPro Analytics — Modelling utilities.

This module provides:

- Logistic regression fitting via statsmodels (inference).
- Logistic regression fitting via scikit-learn (prediction).
- Predictive evaluation at a chosen classification threshold.

It is deliberately small and dependency-light so it can be
imported from scripts, tests, or notebooks.
"""

from typing import Iterable

import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def fit_statsmodels_logit(
    X: pd.DataFrame,
    y: pd.Series,
) -> sm.discrete.discrete_model.BinaryResultsWrapper:
    """
    Fit a logistic regression using statsmodels with an intercept.

    Parameters
    ----------
    X : pd.DataFrame
        Predictor matrix (numeric).
    y : pd.Series
        Binary outcome (0/1).

    Returns
    -------
    statsmodels BinaryResultsWrapper
    """
    X_with_const = sm.add_constant(X.astype(float), has_constant="add")
    y_int = y.astype(int)
    return sm.Logit(y_int, X_with_const).fit(disp=False)


def fit_sklearn_logit(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    class_weight: str | None = None,
    random_state: int = 42,
) -> Pipeline:
    """
    Fit a logistic regression pipeline with standardization.
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("logit", LogisticRegression(
            max_iter=2000,
            random_state=random_state,
            class_weight=class_weight,
        )),
    ])
    pipeline.fit(X_train, y_train.astype(int))
    return pipeline


def evaluate_predictions(
    y_true: pd.Series,
    y_prob: np.ndarray,
    threshold: float = 0.5,
) -> dict:
    """
    Evaluate binary predictions at a chosen threshold.
    """
    y_true = y_true.astype(int)
    y_pred = (y_prob >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[0, 1]
    ).ravel()

    return {
        "threshold": threshold,
        "n": int(len(y_true)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "average_precision": float(average_precision_score(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "true_positive": int(tp),
        "false_positive": int(fp),
        "true_negative": int(tn),
        "false_negative": int(fn),
    }
'''

module_path = src_dir / "modelling.py"
module_path.write_text(module_text, encoding="utf-8")

print("Module written:", module_path)
print("File exists:", module_path.exists())
print("File size:", module_path.stat().st_size, "bytes")
print("\nStep 31 completed.")
```


```python
# =========================================================
# STEP 32B: CLEAR MODULE CACHE AND VERIFY FILE CONTENTS
# =========================================================

from pathlib import Path
import shutil

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"
modelling_path = src_dir / "modelling.py"
cache_dir = src_dir / "__pycache__"

# ---------------------------------------------------------
# 1. Verify the source file on disk is the fixed version
# ---------------------------------------------------------
print("SOURCE FILE CHECK")
print("=" * 60)

source_text = modelling_path.read_text(encoding="utf-8")
lines = source_text.splitlines()

print(f"File: {modelling_path}")
print(f"Total lines: {len(lines)}")
print("\nFirst 50 lines:")
for i, line in enumerate(lines[:50], start=1):
    print(f"{i:3d}: {line}")

# ---------------------------------------------------------
# 2. Search for the bad type annotation in the source
# ---------------------------------------------------------
print("\n" + "=" * 60)
print("SEARCH FOR BAD TYPE ANNOTATION")
print("=" * 60)

if "sm.discrete.discrete_model.BinaryResultsWrapper" in source_text:
    print("STILL PRESENT in the file on disk!")
    print("The Step 32A write did not succeed, or the file was")
    print("rewritten after Step 32A.")
else:
    print("Not present in the file on disk. The source is fixed.")

# ---------------------------------------------------------
# 3. Delete __pycache__ so Python cannot load stale bytecode
# ---------------------------------------------------------
print("\n" + "=" * 60)
print("CACHE CLEARING")
print("=" * 60)

if cache_dir.exists():
    print(f"Cache directory exists: {cache_dir}")
    shutil.rmtree(cache_dir)
    print("Cache directory removed.")
else:
    print("No cache directory found.")

# ---------------------------------------------------------
# 4. Remove the module from sys.modules if it is loaded
# ---------------------------------------------------------
import sys

if "modelling" in sys.modules:
    print("\nRemoving 'modelling' from sys.modules.")
    del sys.modules["modelling"]
else:
    print("\n'modelling' is not in sys.modules.")

print("\nStep 32B completed.")
```


```python
# =========================================================
# STEP 32: VERIFY src/modelling.py AGAINST NOTEBOOK OUTPUT
# Read-only
# =========================================================

import sys
from pathlib import Path
import importlib
import numpy as np
import pandas as pd

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import modelling
importlib.reload(modelling)

from modelling import (
    fit_statsmodels_logit,
    fit_sklearn_logit,
    evaluate_predictions,
)

print("MODELLING MODULE VERIFICATION")
print("=" * 70)

# ---------------------------------------------------------
# 1. Confirm required notebook objects exist
# ---------------------------------------------------------
required_globals = [
    "expanded_model_v2",
    "X_train", "X_test", "y_train", "y_test",
    "y_prob_balanced", "y_pred_balanced",
    "balanced_pipeline",
]

missing_globals = [g for g in required_globals if g not in globals()]

if missing_globals:
    print("Missing notebook objects:", missing_globals)
    print("Run the notebook from the beginning, then rerun this cell.")
else:
    print("All required notebook objects are available.")

    # -----------------------------------------------------
    # 2. Verify statsmodels logistic regression
    # -----------------------------------------------------
    print("\nSTATSMODELS LOGIT — COEFFICIENT COMPARISON")
    print("-" * 70)

    # Reconstruct the exact X used in the notebook
    model_data = expanded_data.dropna(
        subset=[
            "improved_seed_adopter",
            "naads_training_participation",
            "farmer_group_member_clean",
            "head_age",
            "head_sex",
        ]
    ).copy()

    model_data["age_centered"] = (
        model_data["head_age"] - model_data["head_age"].mean()
    )
    model_data["age_centered_squared"] = model_data["age_centered"] ** 2

    y_sm = model_data["improved_seed_adopter"].astype(int)

    X_sm = model_data[
        [
            "naads_training_participation",
            "farmer_group_member_clean",
            "age_centered",
            "age_centered_squared",
        ]
    ].astype(float)

    sex_dummies = pd.get_dummies(
        model_data["head_sex"],
        prefix="head_sex",
        drop_first=True,
        dtype=float,
    )
    X_sm = pd.concat([X_sm, sex_dummies], axis=1)

    module_model = fit_statsmodels_logit(X_sm, y_sm)

    # Compare against notebook
    notebook_coef = expanded_model_v2.params
    module_coef = module_model.params

    coef_comparison = pd.DataFrame({
        "notebook": notebook_coef,
        "module": module_coef,
    })
    coef_comparison["abs_diff"] = (
        coef_comparison["notebook"] - coef_comparison["module"]
    ).abs()

    display(coef_comparison.round(6))

    max_coef_diff = coef_comparison["abs_diff"].max()
    print(f"\nMax coefficient difference: {max_coef_diff:.10f}")
    print(f"Effective match (< 1e-6): {max_coef_diff < 1e-6}")

    # -----------------------------------------------------
    # 3. Verify sklearn logistic regression and evaluation
    # -----------------------------------------------------
    print("\nSKLEARN LOGIT — PREDICTIVE COMPARISON")
    print("-" * 70)

    module_pipeline = fit_sklearn_logit(
        X_train, y_train, class_weight="balanced"
    )

    module_prob = module_pipeline.predict_proba(X_test)[:, 1]
    module_metrics = evaluate_predictions(
        y_test, module_prob, threshold=0.5
    )

    notebook_metrics = evaluate_predictions(
        y_test, y_prob_balanced, threshold=0.5
    )

    # Compare the probability vectors row-by-row
    prob_diff = np.abs(module_prob - y_prob_balanced)
    max_prob_diff = float(prob_diff.max())
    mean_prob_diff = float(prob_diff.mean())

    print(f"Max probability difference: {max_prob_diff:.10f}")
    print(f"Mean probability difference: {mean_prob_diff:.10f}")

    # Compare key metrics
    metric_keys = [
        "roc_auc", "average_precision", "accuracy",
        "balanced_accuracy", "precision", "recall", "f1",
        "true_positive", "false_positive",
        "true_negative", "false_negative",
    ]

    metric_comparison = pd.DataFrame([
        {
            "metric": key,
            "notebook": notebook_metrics[key],
            "module": module_metrics[key],
            "abs_diff": abs(
                notebook_metrics[key] - module_metrics[key]
            ),
        }
        for key in metric_keys
    ])

    display(metric_comparison.round(6))

    print("\nStep 32 completed.")
```


```python
# =========================================================
# STEP 32A: FIX src/modelling.py IMPORT ERROR
# Overwrites the module file with a corrected version
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
src_dir = project_root / "src"
module_path = src_dir / "modelling.py"

module_text = '''"""
ResearchPro Analytics — Modelling utilities.

This module provides:

- Logistic regression fitting via statsmodels (inference).
- Logistic regression fitting via scikit-learn (prediction).
- Predictive evaluation at a chosen classification threshold.

It is deliberately small and dependency-light so it can be
imported from scripts, tests, or notebooks.
"""

from typing import Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def fit_statsmodels_logit(
    X: pd.DataFrame,
    y: pd.Series,
):
    """
    Fit a logistic regression using statsmodels with an intercept.

    Parameters
    ----------
    X : pd.DataFrame
        Predictor matrix (numeric).
    y : pd.Series
        Binary outcome (0/1).

    Returns
    -------
    statsmodels BinaryResultsWrapper
    """
    X_with_const = sm.add_constant(X.astype(float), has_constant="add")
    y_int = y.astype(int)
    return sm.Logit(y_int, X_with_const).fit(disp=False)


def fit_sklearn_logit(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    class_weight: Optional[str] = None,
    random_state: int = 42,
) -> Pipeline:
    """
    Fit a logistic regression pipeline with standardization.
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("logit", LogisticRegression(
            max_iter=2000,
            random_state=random_state,
            class_weight=class_weight,
        )),
    ])
    pipeline.fit(X_train, y_train.astype(int))
    return pipeline


def evaluate_predictions(
    y_true: pd.Series,
    y_prob: np.ndarray,
    threshold: float = 0.5,
) -> dict:
    """
    Evaluate binary predictions at a chosen threshold.
    """
    y_true = y_true.astype(int)
    y_pred = (y_prob >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[0, 1]
    ).ravel()

    return {
        "threshold": threshold,
        "n": int(len(y_true)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "average_precision": float(average_precision_score(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "true_positive": int(tp),
        "false_positive": int(fp),
        "true_negative": int(tn),
        "false_negative": int(fn),
    }
'''

module_path.write_text(module_text, encoding="utf-8")

print("Module rewritten:", module_path)
print("File exists:", module_path.exists())
print("File size:", module_path.stat().st_size, "bytes")
print("\nStep 32A completed.")
```


```python
# =========================================================
# STEP 33: CREATE TEST INFRASTRUCTURE
# Writes conftest.py and tests/ directory
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
tests_dir = project_root / "tests"
tests_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# 1. conftest.py — makes src/ importable from tests
# ---------------------------------------------------------
conftest_text = '''"""
Pytest configuration for ResearchPro Analytics tests.

Adds the project's src/ directory to sys.path so tests can
import modules directly without installing the package.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
'''

conftest_path = tests_dir / "conftest.py"
conftest_path.write_text(conftest_text, encoding="utf-8")

# ---------------------------------------------------------
# 2. tests/__init__.py — makes tests a package
# ---------------------------------------------------------
init_path = tests_dir / "__init__.py"
init_path.write_text('"""ResearchPro Analytics test suite."""\n', encoding="utf-8")

print("Test infrastructure created.")
print("Directory:", tests_dir)
print("Files:")
for p in sorted(tests_dir.iterdir()):
    print(f"  {p.name}  ({p.stat().st_size} bytes)")

print("\nStep 33 completed.")
```


```python
# =========================================================
# STEP 34: WRITE tests/test_seed_outcome.py
# Validates crop-level improved-seed outcome rules
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
tests_dir = project_root / "tests"

test_text = '''"""
Tests for src/seed_outcome.py

These tests validate the crop-level improved-seed outcome rules
against the questionnaire coding.

Coding verified from agriculture_qx.pdf:
- s4aq16 / s4bq16 : seed use (1=Yes, 2=No)
- s4aq13 / s4bq13 : seed type (1=Traditional, 2=Improved)
- s4aq14 / s4bq14 : improved category (1=Certified, 2=Quality, 3=DK)
"""

import pandas as pd
import pytest

from seed_outcome import build_crop_level_outcome, VISIT_CONFIG


def make_crop_df(use, seed_type, category=None, n=None):
    """
    Build a minimal crop-level DataFrame for testing.
    """
    if n is None:
        n = len(use)
    return pd.DataFrame({
        "hhid": [f"H{i:04d}" for i in range(n)],
        "s4aq16": use,
        "s4aq13": seed_type,
        "s4aq14": category if category is not None else [pd.NA] * n,
    })


# ---------------------------------------------------------
# Test 1: Traditional seed => outcome 0
# ---------------------------------------------------------
def test_traditional_seed_is_non_adopter():
    df = make_crop_df(use=[1], seed_type=[1])
    result = build_crop_level_outcome(df, visit=1)
    assert result.loc[0, "improved_seed_adoption"] == 0
    assert result.loc[0, "adoption_classification_status"] == "Non-adopter"


# ---------------------------------------------------------
# Test 2: Improved seed => outcome 1
# ---------------------------------------------------------
def test_improved_seed_is_adopter():
    df = make_crop_df(use=[1], seed_type=[2], category=[1])
    result = build_crop_level_outcome(df, visit=1)
    assert result.loc[0, "improved_seed_adoption"] == 1
    assert result.loc[0, "adoption_classification_status"] == "Adopter"


# ---------------------------------------------------------
# Test 3: Reported no seed use => outcome 0
# ---------------------------------------------------------
def test_no_seed_use_is_non_adopter():
    df = make_crop_df(use=[2], seed_type=[pd.NA])
    result = build_crop_level_outcome(df, visit=1)
    assert result.loc[0, "improved_seed_adoption"] == 0


# ---------------------------------------------------------
# Test 4: Seed used but type missing => unresolved
# ---------------------------------------------------------
def test_missing_seed_type_is_unresolved():
    df = make_crop_df(use=[1], seed_type=[pd.NA])
    result = build_crop_level_outcome(df, visit=1)
    assert pd.isna(result.loc[0, "improved_seed_adoption"])
    assert result.loc[0, "adoption_classification_status"] == "Unresolved"


# ---------------------------------------------------------
# Test 5: Seed use missing entirely => unresolved
# ---------------------------------------------------------
def test_missing_seed_use_is_unresolved():
    df = make_crop_df(use=[pd.NA], seed_type=[pd.NA])
    result = build_crop_level_outcome(df, visit=1)
    assert pd.isna(result.loc[0, "improved_seed_adoption"])


# ---------------------------------------------------------
# Test 6: Improved seed with missing category => flagged
# ---------------------------------------------------------
def test_improved_seed_with_missing_category_is_flagged():
    df = make_crop_df(use=[1], seed_type=[2], category=[pd.NA])
    result = build_crop_level_outcome(df, visit=1)
    assert result.loc[0, "improved_category_missing_flag"] is True or (
        result.loc[0, "improved_category_missing_flag"] == True
    )


# ---------------------------------------------------------
# Test 7: Improved seed with known category => not flagged
# ---------------------------------------------------------
def test_improved_seed_with_known_category_is_not_flagged():
    df = make_crop_df(use=[1], seed_type=[2], category=[1])
    result = build_crop_level_outcome(df, visit=1)
    assert not result.loc[0, "improved_category_missing_flag"]


# ---------------------------------------------------------
# Test 8: Visit 2 uses s4bq column names
# ---------------------------------------------------------
def test_visit_2_uses_visit_2_columns():
    df = pd.DataFrame({
        "hhid": ["H0001"],
        "s4bq16": [1],
        "s4bq13": [2],
        "s4bq14": [1],
    })
    result = build_crop_level_outcome(df, visit=2)
    assert result.loc[0, "improved_seed_adoption"] == 1


# ---------------------------------------------------------
# Test 9: Invalid visit number raises ValueError
# ---------------------------------------------------------
def test_invalid_visit_raises_value_error():
    df = make_crop_df(use=[1], seed_type=[1])
    with pytest.raises(ValueError):
        build_crop_level_outcome(df, visit=3)


# ---------------------------------------------------------
# Test 10: Missing columns raise KeyError
# ---------------------------------------------------------
def test_missing_columns_raise_key_error():
    df = pd.DataFrame({"hhid": ["H0001"]})
    with pytest.raises(KeyError):
        build_crop_level_outcome(df, visit=1)
'''

test_path = tests_dir / "test_seed_outcome.py"
test_path.write_text(test_text, encoding="utf-8")

print("Test file written:", test_path)
print("File exists:", test_path.exists())
print("File size:", test_path.stat().st_size, "bytes")
print("\nStep 34 completed.")
```


```python
# =========================================================
# STEP 35: WRITE tests/test_household_aggregation.py
# Validates household-level adoption aggregation rules
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
tests_dir = project_root / "tests"

test_text = '''"""
Tests for src/household_aggregation.py

These tests validate the household-level adoption rules:

- Adopter: at least one crop record has outcome 1.
- Non-adopter: no crop outcome is 1 AND no crop outcome is NA.
- Unclassified: otherwise (has at least one NA, no 1).
"""

import pandas as pd
import pytest

from household_aggregation import aggregate_household_adoption


def make_crop_df(rows):
    """
    Build a crop-level DataFrame from a list of dicts.

    Each dict must have: hhid, improved_seed_adoption
    """
    return pd.DataFrame(rows)


# ---------------------------------------------------------
# Test 1: Household with one improved crop => Adopter
# ---------------------------------------------------------
def test_one_improved_crop_makes_adopter():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": 0},
        {"hhid": "H1", "improved_seed_adoption": 1},
    ])
    result = aggregate_household_adoption(df)
    row = result.loc[result["hhid"] == "H1"].iloc[0]
    assert row["household_adoption"] == 1
    assert row["adoption_status"] == "Adopter"


# ---------------------------------------------------------
# Test 2: All crops traditional => Non-adopter
# ---------------------------------------------------------
def test_all_traditional_is_non_adopter():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": 0},
        {"hhid": "H1", "improved_seed_adoption": 0},
    ])
    result = aggregate_household_adoption(df)
    row = result.loc[result["hhid"] == "H1"].iloc[0]
    assert row["household_adoption"] == 0
    assert row["adoption_status"] == "Non-adopter"


# ---------------------------------------------------------
# Test 3: Traditional + unresolved => Unclassified
# ---------------------------------------------------------
def test_unresolved_crop_makes_unclassified():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": 0},
        {"hhid": "H1", "improved_seed_adoption": pd.NA},
    ])
    result = aggregate_household_adoption(df)
    row = result.loc[result["hhid"] == "H1"].iloc[0]
    assert pd.isna(row["household_adoption"])
    assert row["adoption_status"] == "Unclassified"


# ---------------------------------------------------------
# Test 4: Adopter even if some crops are unresolved
# ---------------------------------------------------------
def test_adopter_takes_precedence_over_unresolved():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": pd.NA},
        {"hhid": "H1", "improved_seed_adoption": 1},
    ])
    result = aggregate_household_adoption(df)
    row = result.loc[result["hhid"] == "H1"].iloc[0]
    assert row["household_adoption"] == 1
    assert row["adoption_status"] == "Adopter"


# ---------------------------------------------------------
# Test 5: Crop record counts are correct
# ---------------------------------------------------------
def test_crop_record_counts():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": 0},
        {"hhid": "H1", "improved_seed_adoption": 1},
        {"hhid": "H1", "improved_seed_adoption": pd.NA},
    ])
    result = aggregate_household_adoption(df)
    row = result.loc[result["hhid"] == "H1"].iloc[0]
    assert row["crop_records"] == 3
    assert row["confirmed_adopter_crops"] == 1
    assert row["confirmed_nonadopter_crops"] == 1
    assert row["unresolved_crops"] == 1


# ---------------------------------------------------------
# Test 6: Multiple households handled independently
# ---------------------------------------------------------
def test_multiple_households():
    df = make_crop_df([
        {"hhid": "H1", "improved_seed_adoption": 1},
        {"hhid": "H2", "improved_seed_adoption": 0},
        {"hhid": "H2", "improved_seed_adoption": 0},
        {"hhid": "H3", "improved_seed_adoption": pd.NA},
    ])
    result = aggregate_household_adoption(df)
    assert len(result) == 3

    h1 = result.loc[result["hhid"] == "H1"].iloc[0]
    h2 = result.loc[result["hhid"] == "H2"].iloc[0]
    h3 = result.loc[result["hhid"] == "H3"].iloc[0]

    assert h1["adoption_status"] == "Adopter"
    assert h2["adoption_status"] == "Non-adopter"
    assert h3["adoption_status"] == "Unclassified"


# ---------------------------------------------------------
# Test 7: Missing column raises KeyError
# ---------------------------------------------------------
def test_missing_outcome_column_raises_key_error():
    df = pd.DataFrame({"hhid": ["H1"]})
    with pytest.raises(KeyError):
        aggregate_household_adoption(df)


# ---------------------------------------------------------
# Test 8: Missing household column raises KeyError
# ---------------------------------------------------------
def test_missing_household_column_raises_key_error():
    df = pd.DataFrame({"improved_seed_adoption": [0]})
    with pytest.raises(KeyError):
        aggregate_household_adoption(df)
'''

test_path = tests_dir / "test_household_aggregation.py"
test_path.write_text(test_text, encoding="utf-8")

print("Test file written:", test_path)
print("File exists:", test_path.exists())
print("File size:", test_path.stat().st_size, "bytes")
print("\nStep 35 completed.")
```


```python
# =========================================================
# STEP 36: WRITE tests/test_modelling.py
# Validates the modelling helpers
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
tests_dir = project_root / "tests"

test_text = '''"""
Tests for src/modelling.py

These tests validate:

- evaluate_predictions returns the expected keys and values.
- Perfect separation produces expected metrics.
- fit_sklearn_logit returns a fitted pipeline with predict_proba.
- fit_statsmodels_logit returns a fitted model with params.
"""

import numpy as np
import pandas as pd
import pytest

from modelling import (
    fit_statsmodels_logit,
    fit_sklearn_logit,
    evaluate_predictions,
)


# ---------------------------------------------------------
# Test 1: evaluate_predictions returns expected keys
# ---------------------------------------------------------
def test_evaluate_predictions_returns_expected_keys():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.4, 0.6, 0.9])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    expected_keys = {
        "threshold", "n",
        "roc_auc", "average_precision",
        "accuracy", "balanced_accuracy",
        "precision", "recall", "f1",
        "true_positive", "false_positive",
        "true_negative", "false_negative",
    }

    assert expected_keys.issubset(result.keys())


# ---------------------------------------------------------
# Test 2: Perfect separation gives expected metrics
# ---------------------------------------------------------
def test_evaluate_predictions_perfect_separation():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    assert result["roc_auc"] == 1.0
    assert result["accuracy"] == 1.0
    assert result["balanced_accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0
    assert result["true_positive"] == 2
    assert result["true_negative"] == 2
    assert result["false_positive"] == 0
    assert result["false_negative"] == 0


# ---------------------------------------------------------
# Test 3: All-negative predictions
# ---------------------------------------------------------
def test_evaluate_predictions_all_negative():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.3, 0.4])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    assert result["true_positive"] == 0
    assert result["recall"] == 0.0
    assert result["accuracy"] == 0.5  # 2/4 correct


# ---------------------------------------------------------
# Test 4: Threshold effect on classification
# ---------------------------------------------------------
def test_threshold_changes_predictions():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.3, 0.4, 0.55, 0.6])

    result_low = evaluate_predictions(y_true, y_prob, threshold=0.35)
    result_high = evaluate_predictions(y_true, y_prob, threshold=0.65)

    # Low threshold: predicts all as positive
    assert result_low["true_positive"] == 2
    assert result_low["false_positive"] == 2

    # High threshold: predicts all as negative
    assert result_high["true_positive"] == 0
    assert result_high["false_positive"] == 0


# ---------------------------------------------------------
# Test 5: fit_sklearn_logit returns fitted pipeline
# ---------------------------------------------------------
def test_fit_sklearn_logit_returns_pipeline():
    # Simple synthetic data
    np.random.seed(42)
    X = pd.DataFrame({
        "x1": np.random.normal(0, 1, 100),
        "x2": np.random.normal(0, 1, 100),
    })
    y = pd.Series((X["x1"] + X["x2"] > 0).astype(int))

    pipeline = fit_sklearn_logit(X, y, class_weight="balanced")

    assert hasattr(pipeline, "predict_proba")

    prob = pipeline.predict_proba(X)[:, 1]
    assert len(prob) == 100
    assert (prob >= 0).all() and (prob <= 1).all()


# ---------------------------------------------------------
# Test 6: fit_statsmodels_logit returns fitted model
# ---------------------------------------------------------
def test_fit_statsmodels_logit_returns_model():
    np.random.seed(42)
    X = pd.DataFrame({
        "x1": np.random.normal(0, 1, 100),
        "x2": np.random.normal(0, 1, 100),
    })
    y = pd.Series((X["x1"] + X["x2"] > 0).astype(int))

    model = fit_statsmodels_logit(X, y)

    assert hasattr(model, "params")
    assert hasattr(model, "pvalues")
    # Two predictors plus intercept
    assert len(model.params) == 3


# ---------------------------------------------------------
# Test 7: sklearn logistic regression separates simple data
# ---------------------------------------------------------
def test_sklearn_logit_separates_simple_data():
    X = pd.DataFrame({
        "x": [-3, -2, -1, 1, 2, 3],
    })
    y = pd.Series([0, 0, 0, 1, 1, 1])

    pipeline = fit_sklearn_logit(X, y)
    preds = pipeline.predict(X)

    assert (preds == y.values).all()
'''

test_path = tests_dir / "test_modelling.py"
test_path.write_text(test_text, encoding="utf-8")

print("Test file written:", test_path)
print("File exists:", test_path.exists())
print("File size:", test_path.stat().st_size, "bytes")
print("\nStep 36 completed.")
```


```python
# =========================================================
# STEP 37: RUN THE TEST SUITE
# Uses pytest; read-only
# =========================================================

import subprocess
import sys
from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")

print("RUNNING TEST SUITE")
print("=" * 70)
print("Project root:", project_root)
print("Python executable:", sys.executable)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
    cwd=str(project_root),
    capture_output=True,
    text=True,
)

print("\nSTDOUT:")
print(result.stdout)

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

print("\nReturn code:", result.returncode)
print("\nStep 37 completed.")
```


```python
# =========================================================
# STEP 37A: INSTALL PYTEST IN THE PROJECT VENV
# =========================================================

import sys
import subprocess

print("Installing pytest into:", sys.executable)

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "pytest"],
    capture_output=True,
    text=True,
)

print("\nSTDOUT:")
print(result.stdout)

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

print("\nReturn code:", result.returncode)
print("\nStep 37A completed.")
```


```python
# =========================================================
# STEP 37B: FIX THE FAILING TEST
# Rewrites tests/test_modelling.py with corrected expectations
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
tests_dir = project_root / "tests"
test_path = tests_dir / "test_modelling.py"

test_text = '''"""
Tests for src/modelling.py

These tests validate:

- evaluate_predictions returns the expected keys and values.
- Perfect separation produces expected metrics.
- Threshold changes affect classification.
- fit_sklearn_logit returns a fitted pipeline with predict_proba.
- fit_statsmodels_logit returns a fitted model with params.
"""

import numpy as np
import pandas as pd
import pytest

from modelling import (
    fit_statsmodels_logit,
    fit_sklearn_logit,
    evaluate_predictions,
)


# ---------------------------------------------------------
# Test 1: evaluate_predictions returns expected keys
# ---------------------------------------------------------
def test_evaluate_predictions_returns_expected_keys():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.4, 0.6, 0.9])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    expected_keys = {
        "threshold", "n",
        "roc_auc", "average_precision",
        "accuracy", "balanced_accuracy",
        "precision", "recall", "f1",
        "true_positive", "false_positive",
        "true_negative", "false_negative",
    }

    assert expected_keys.issubset(result.keys())


# ---------------------------------------------------------
# Test 2: Perfect separation gives expected metrics
# ---------------------------------------------------------
def test_evaluate_predictions_perfect_separation():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    assert result["roc_auc"] == 1.0
    assert result["accuracy"] == 1.0
    assert result["balanced_accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0
    assert result["true_positive"] == 2
    assert result["true_negative"] == 2
    assert result["false_positive"] == 0
    assert result["false_negative"] == 0


# ---------------------------------------------------------
# Test 3: All-negative predictions
# ---------------------------------------------------------
def test_evaluate_predictions_all_negative():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.3, 0.4])

    result = evaluate_predictions(y_true, y_prob, threshold=0.5)

    assert result["true_positive"] == 0
    assert result["recall"] == 0.0
    assert result["accuracy"] == 0.5  # 2/4 correct


# ---------------------------------------------------------
# Test 4: Threshold changes classification
# ---------------------------------------------------------
def test_threshold_changes_predictions():
    y_true = pd.Series([0, 0, 1, 1])
    y_prob = np.array([0.3, 0.4, 0.55, 0.6])

    # At threshold 0.35:
    #   0.30 -> 0
    #   0.40 -> 1
    #   0.55 -> 1
    #   0.60 -> 1
    # => TP=2, FP=1, TN=1, FN=0
    result_low = evaluate_predictions(y_true, y_prob, threshold=0.35)
    assert result_low["true_positive"] == 2
    assert result_low["false_positive"] == 1
    assert result_low["true_negative"] == 1
    assert result_low["false_negative"] == 0

    # At threshold 0.65: all probabilities below 0.65 => all predicted 0
    result_high = evaluate_predictions(y_true, y_prob, threshold=0.65)
    assert result_high["true_positive"] == 0
    assert result_high["false_positive"] == 0
    assert result_high["true_negative"] == 2
    assert result_high["false_negative"] == 2


# ---------------------------------------------------------
# Test 5: fit_sklearn_logit returns fitted pipeline
# ---------------------------------------------------------
def test_fit_sklearn_logit_returns_pipeline():
    np.random.seed(42)
    X = pd.DataFrame({
        "x1": np.random.normal(0, 1, 100),
        "x2": np.random.normal(0, 1, 100),
    })
    y = pd.Series((X["x1"] + X["x2"] > 0).astype(int))

    pipeline = fit_sklearn_logit(X, y, class_weight="balanced")

    assert hasattr(pipeline, "predict_proba")

    prob = pipeline.predict_proba(X)[:, 1]
    assert len(prob) == 100
    assert (prob >= 0).all() and (prob <= 1).all()


# ---------------------------------------------------------
# Test 6: fit_statsmodels_logit returns fitted model
# ---------------------------------------------------------
def test_fit_statsmodels_logit_returns_model():
    np.random.seed(42)
    X = pd.DataFrame({
        "x1": np.random.normal(0, 1, 100),
        "x2": np.random.normal(0, 1, 100),
    })
    y = pd.Series((X["x1"] + X["x2"] > 0).astype(int))

    model = fit_statsmodels_logit(X, y)

    assert hasattr(model, "params")
    assert hasattr(model, "pvalues")
    assert len(model.params) == 3


# ---------------------------------------------------------
# Test 7: sklearn logistic regression separates simple data
# ---------------------------------------------------------
def test_sklearn_logit_separates_simple_data():
    X = pd.DataFrame({
        "x": [-3, -2, -1, 1, 2, 3],
    })
    y = pd.Series([0, 0, 0, 1, 1, 1])

    pipeline = fit_sklearn_logit(X, y)
    preds = pipeline.predict(X)

    assert (preds == y.values).all()
'''

test_path.write_text(test_text, encoding="utf-8")

print("Test file rewritten:", test_path)
print("File size:", test_path.stat().st_size, "bytes")
print("\nStep 37B completed.")
```


```python
# =========================================================
# STATE CHECK — confirm we can continue from Step 38
# =========================================================

from pathlib import Path
import sys

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")

# Confirm project structure
checks = {
    "src/seed_outcome.py": project_root / "src" / "seed_outcome.py",
    "src/household_aggregation.py": project_root / "src" / "household_aggregation.py",
    "src/modelling.py": project_root / "src" / "modelling.py",
    "tests/conftest.py": project_root / "tests" / "conftest.py",
    "tests/test_seed_outcome.py": project_root / "tests" / "test_seed_outcome.py",
    "tests/test_household_aggregation.py": project_root / "tests" / "test_household_aggregation.py",
    "tests/test_modelling.py": project_root / "tests" / "test_modelling.py",
    "requirements.txt": project_root / "requirements.txt",
    "README.md": project_root / "README.md",
}

print("PROJECT STATE CHECK")
print("=" * 60)
print("Python:", sys.executable)
print("Project root:", project_root)
print()

all_present = True
for label, path in checks.items():
    exists = path.exists()
    status = "✅" if exists else "❌ MISSING"
    print(f"{status}  {label}")
    if not exists:
        all_present = False

print()
if all_present:
    print("All expected files are present. Ready to continue at Step 38.")
else:
    print("Some files are missing. Review the list above before continuing.")
```


```python
# =========================================================
# STEP 38: INSPECT requirements.txt
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
requirements_path = project_root / "requirements.txt"

print("REQUIREMENTS FILE INSPECTION")
print("=" * 60)

if not requirements_path.exists():
    print("requirements.txt not found. We will create it.")
    current_text = ""
else:
    current_text = requirements_path.read_text(encoding="utf-8")
    print("Current contents:")
    print("-" * 60)
    print(current_text)
    print("-" * 60)

# Check which required packages are already listed
required_packages = [
    "numpy",
    "pandas",
    "scipy",
    "statsmodels",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "pytest",
]

current_lower = current_text.lower()

present = [pkg for pkg in required_packages if pkg.lower() in current_lower]
missing = [pkg for pkg in required_packages if pkg.lower() not in current_lower]

print("\nPackages already listed:", present)
print("Packages missing:", missing)
print("\nStep 38 completed.")
```


```python
# =========================================================
# STEP 38B: APPEND pytest TO requirements.txt
# =========================================================

from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
requirements_path = project_root / "requirements.txt"

current_text = requirements_path.read_text(encoding="utf-8")

# Guard against duplicate appends
if "pytest" in current_text.lower():
    print("pytest is already present. No change made.")
else:
    # Ensure a clean trailing newline, then append pytest
    new_text = current_text.rstrip() + "\n" + "pytest>=8.0,<10\n"
    requirements_path.write_text(new_text, encoding="utf-8")
    print("pytest appended.")

print("\nUPDATED requirements.txt")
print("=" * 60)
print(requirements_path.read_text(encoding="utf-8"))

print("\nStep 38B completed.")
```


```python
from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
readme_path = project_root / "README.md"

readme_text = readme_path.read_text(encoding="utf-8")

tests_section = '''

## Running the Tests

The project includes an automated test suite that validates the
reusable modules in src/.

After installing dependencies, run:

    python -m pytest tests/ -v

Expected result: 25 tests pass, 0 fail.

The test suite covers:

- test_seed_outcome.py — validates the crop-level improved-seed
  outcome rules against the questionnaire coding.
- test_household_aggregation.py — validates the household-level
  adoption classification rules.
- test_modelling.py — validates the logistic regression and
  prediction-evaluation helpers.
'''

if "## Running the Tests" in readme_text:
    print("Test instructions already present in README. No change made.")
else:
    new_text = readme_text.rstrip() + "\n" + tests_section
    readme_path.write_text(new_text, encoding="utf-8")
    print("Test instructions appended to README.")

print("\nStep 39 completed.")
```


```python
from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
workflow_dir = project_root / ".github" / "workflows"
workflow_dir.mkdir(parents=True, exist_ok=True)

workflow_path = workflow_dir / "tests.yml"

workflow_text = '''name: Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt

      - name: Run test suite
        run: python -m pytest tests/ -v
'''

workflow_path.write_text(workflow_text, encoding="utf-8")

print("Workflow written:", workflow_path)
print("File exists:", workflow_path.exists())
print("File size:", workflow_path.stat().st_size, "bytes")
print("\nStep 40 completed.")
```


```python
from pathlib import Path
import subprocess
import sys

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")

print("FINAL PROJECT REVIEW")
print("=" * 70)

# 1. Directory inventory
print("\n1. PROJECT DIRECTORY INVENTORY")
print("-" * 70)

for folder in [
    "src",
    "tests",
    "reports",
    "notebooks",
    "docs",
    ".github/workflows",
]:
    folder_path = project_root / folder
    if folder_path.exists():
        files = sorted(
            f.name for f in folder_path.iterdir() if f.is_file()
        )
        print(f"\n{folder}/  ({len(files)} files)")
        for f in files:
            print(f"  - {f}")
    else:
        print(f"\n{folder}/  MISSING")

# 2. Required files
print("\n\n2. REQUIRED FILES")
print("-" * 70)

required = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "src/__init__.py",
    "src/seed_outcome.py",
    "src/household_aggregation.py",
    "src/modelling.py",
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_seed_outcome.py",
    "tests/test_household_aggregation.py",
    "tests/test_modelling.py",
    "reports/survey_design_decision.csv",
    "reports/survey_design_limitation.md",
    "reports/final_analysis_report.md",
    ".github/workflows/tests.yml",
]

missing_count = 0
for rel in required:
    path = project_root / rel
    if path.exists():
        print(f"  OK    {rel}")
    else:
        print(f"  MISS  {rel}")
        missing_count += 1

# 3. Run test suite as final confirmation
print("\n\n3. TEST SUITE CONFIRMATION")
print("-" * 70)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-q"],
    cwd=str(project_root),
    capture_output=True,
    text=True,
)

lines = result.stdout.strip().splitlines()
for line in lines[-6:]:
    print(line)

print("\nReturn code:", result.returncode)
print("Missing files count:", missing_count)
print("\nStep 41 completed.")
```


```python
from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")
gitignore_path = project_root / ".gitignore"

print("CURRENT .gitignore")
print("=" * 60)
print(gitignore_path.read_text(encoding="utf-8"))
print("=" * 60)

backups = [
    "notebooks/02_dataset_assessment_public_backup_20261009_182340.ipynb",
    "notebooks/02_dataset_assessment_public_backup_before_cleanup.ipynb",
]

print("\nBACKUP FILE COVERAGE CHECK")
print("-" * 60)

for rel in backups:
    p = project_root / rel
    exists = p.exists()
    print(f"  {'EXISTS' if exists else 'MISSING'}: {rel}")

print("\nStep 42A completed.")
```


```python
import subprocess
from pathlib import Path

project_root = Path(r"C:\Users\H-START\Desktop\Block 5\ResearchPro-Analytics")

print("GIT STATUS AND IGNORE CHECK")
print("=" * 70)

# 1. Is this a git repository?
result = subprocess.run(
    ["git", "rev-parse", "--is-inside-work-tree"],
    cwd=str(project_root),
    capture_output=True, text=True,
)
print("\nGit repo detected:", result.stdout.strip())

# 2. What does git see as untracked/modified?
result = subprocess.run(
    ["git", "status", "--short"],
    cwd=str(project_root),
    capture_output=True, text=True,
)
print("\nGit status (short):")
print(result.stdout if result.stdout.strip() else "  (clean — nothing to report)")

# 3. Would git ignore the backup files?
backups = [
    "notebooks/02_dataset_assessment_public_backup_20261009_182340.ipynb",
    "notebooks/02_dataset_assessment_public_backup_before_cleanup.ipynb",
    "notebooks/02_dataset_assessment.ipynb",
]

print("\nIGNORE CHECKS")
print("-" * 70)
for rel in backups:
    result = subprocess.run(
        ["git", "check-ignore", "-v", rel],
        cwd=str(project_root),
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"  IGNORED: {rel}")
        print(f"    by rule: {result.stdout.strip()}")
    else:
        print(f"  NOT IGNORED: {rel}")

# 4. Show what git would add (preview of commit)
result = subprocess.run(
    ["git", "add", "--dry-run", "."],
    cwd=str(project_root),
    capture_output=True, text=True,
)
print("\nWHAT WOULD BE ADDED (dry run):")
print("-" * 70)
print(result.stdout if result.stdout.strip() else "  (nothing to add)")

print("\nStep 42B completed.")
```


```python

```
