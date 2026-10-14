"""
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
