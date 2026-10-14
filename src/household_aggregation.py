"""
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
