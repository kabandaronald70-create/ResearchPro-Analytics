"""
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
