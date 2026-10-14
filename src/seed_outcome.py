"""
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
