"""
ResearchPro Analytics — Interactive Dashboard.

Reads from reports/*.csv that are already committed to the
repository. No raw data is used or displayed.

Run locally:
    streamlit run dashboard/app.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = PROJECT_ROOT / "reports"

st.set_page_config(
    page_title="ResearchPro Analytics — Improved-Seed Adoption",
    page_icon="🌱",
    layout="wide",
)

# ---------------------------------------------------------------
# Data loaders (cached)
# ---------------------------------------------------------------

@st.cache_data
def load_main_model() -> pd.DataFrame:
    return pd.read_csv(REPORTS / "logistic_regression_results.csv")


@st.cache_data
def load_robust_model() -> pd.DataFrame:
    return pd.read_csv(REPORTS / "logistic_regression_robustness.csv")


@st.cache_data
def load_crop_summary() -> pd.DataFrame:
    return pd.read_csv(REPORTS / "top_five_crop_seed_summary.csv")


@st.cache_data
def load_predictive_performance() -> pd.DataFrame:
    return pd.read_csv(REPORTS / "predictive_performance.csv")


# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------

st.title("🌱 Improved-Seed Adoption in Uganda")
st.caption(
    "Uganda National Panel Survey 2018/19 — ResearchPro Analytics. "
    "Public-use files; no raw micro-data is displayed."
)

# ---------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)
col1.metric("Analytical sample", "1,938 households")
col2.metric("Adoption rate (unweighted)", "18.73%")
col3.metric("Adoption rate (weighted)", "19.81%")
col4.metric("Seasonally inconsistent", "207 households")

st.markdown("---")

# ---------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------

tab_desc, tab_model, tab_robust, tab_crops, tab_pred = st.tabs([
    "📊 Descriptive",
    "📈 Main model",
    "🔁 Robustness",
    "🌾 By crop",
    "🎯 Prediction",
])

with tab_desc:
    st.subheader("Adoption rate by predictor")
    breakdown = pd.DataFrame({
        "Predictor": [
            "NAADS training: Yes",
            "NAADS training: No",
            "Farmer group: Member",
            "Farmer group: Non-member",
            "Male household head",
            "Female household head",
        ],
        "Adoption rate (%)": [28.44, 18.15, 30.65, 18.34, 21.40, 13.06],
    })
    fig = px.bar(
        breakdown,
        x="Adoption rate (%)",
        y="Predictor",
        orientation="h",
        text="Adoption rate (%)",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_range=[0, 35],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info(
        "Bivariate rates. Adjusted odds ratios are in the "
        "'Main model' tab. The gap between bivariate and adjusted "
        "associations is consistent with confounding."
    )

with tab_model:
    st.subheader("Adjusted logistic regression — main model")
    main = load_main_model()
    main = main[main["Predictor"] != "const"].copy()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=main["Odds_Ratio"],
        y=main["Predictor_Label"],
        mode="markers",
        marker=dict(size=10),
        error_x=dict(
            type="data",
            symmetric=False,
            array=main["CI_Upper"] - main["Odds_Ratio"],
            arrayminus=main["Odds_Ratio"] - main["CI_Lower"],
        ),
        name="Odds ratio (95% CI)",
    ))
    fig.add_vline(x=1.0, line_dash="dash", line_color="grey")
    fig.update_layout(
        xaxis_title="Odds ratio (log scale)",
        xaxis_type="log",
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        main[["Predictor_Label", "Odds_Ratio", "CI_Lower", "CI_Upper", "P_Value"]]
        .round(4),
        use_container_width=True,
        hide_index=True,
    )


with tab_robust:
    st.subheader("Robustness — seasonally consistent households only")
    robust = load_robust_model()
    robust = robust[robust["Predictor"] != "const"].copy()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=robust["Odds_Ratio"],
        y=robust["Predictor_Label"],
        mode="markers",
        marker=dict(size=10, color="darkgreen"),
        error_x=dict(
            type="data",
            symmetric=False,
            array=robust["CI_Upper"] - robust["Odds_Ratio"],
            arrayminus=robust["Odds_Ratio"] - robust["CI_Lower"],
        ),
        name="Robustness OR (95% CI)",
    ))
    fig.add_vline(x=1.0, line_dash="dash", line_color="grey")
    fig.update_layout(
        xaxis_title="Odds ratio (log scale)",
        xaxis_type="log",
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        robust[["Predictor_Label", "Odds_Ratio", "CI_Lower", "CI_Upper", "P_Value"]]
        .round(4),
        use_container_width=True,
        hide_index=True,
    )

with tab_crops:
    st.subheader("Improved-seed use across the five most common crops")
    crops = load_crop_summary()

    fig = px.bar(
        crops.sort_values("improved_seed_percentage", ascending=False),
        x="crop_name",
        y="improved_seed_percentage",
        text="improved_seed_percentage",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        xaxis_title="Crop",
        yaxis_title="Improved-seed records (%)",
        height=450,
        yaxis_range=[0, 15],
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(crops.round(2), use_container_width=True, hide_index=True)

with tab_pred:
    st.subheader("Predictive performance at multiple thresholds")
    perf = load_predictive_performance()

    fig = go.Figure()
    for metric in ["Precision", "Recall", "F1_Score"]:
        fig.add_trace(go.Scatter(
            x=perf["Threshold"],
            y=perf[metric],
            mode="lines+markers",
            name=metric,
        ))
    fig.update_layout(
        xaxis_title="Classification threshold",
        yaxis_title="Score",
        yaxis_range=[0, 1],
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(perf.round(4), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------
# Footer
# ---------------------------------------------------------------

st.markdown("---")
st.caption(
    "Source: Uganda National Panel Survey 2018/19 (Uganda Bureau of "
    "Statistics, LSMS-ISA). Public-use files. Survey-design limitation "
    "documented in reports/survey_design_limitation.md."
)
