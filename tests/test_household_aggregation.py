"""
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
