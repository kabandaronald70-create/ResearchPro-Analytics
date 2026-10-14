"""
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
