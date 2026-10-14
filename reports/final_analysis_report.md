# Agricultural Technology Adoption in Uganda
## ResearchPro Analytics — Final Analysis Report

*Last regenerated: 2026-10-13 17:57*

---

## 1. Executive Summary

This analysis examines household adoption of improved seeds using data
from the Uganda National Panel Survey 2018–2019. The final analytical
sample contains **1,938 households**, of which **363
(18.73%)** were classified as improved-seed adopters.
Applying the cross-sectional survey weight yields an estimated
adoption rate of **19.81%** (n=1,910).

Household-head sex was the only statistically significant predictor
in the adjusted logistic regression. Male-headed households had
approximately **1.82 times the odds** of adoption compared
to female-headed households (95% CI [1.29,
2.56], p = 0.0007). The association was even
stronger in a robustness analysis restricted to seasonally consistent
households (OR = 2.87, 95% CI [1.65,
5.00], p = 0.0002).

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

1. **Seasonal inconsistency:** 207 households
   (57.0% of adopters) used improved seeds in only one
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
| Total households in analytical sample | 1,938 |
| Adopters | 363 |
| Non-adopters | 1,575 |
| Adoption rate (unweighted) | 18.73% |
| Adoption rate (cross-sectional weighted) | 19.81% |

### 4.1 Bivariate Adoption Rates

| Predictor | Category | Adoption Rate |
|---|---|---:|
| NAADS training | Participated | 28.44% |
| NAADS training | Did not participate | 18.15% |
| Farmer-group membership | Member | 30.65% |
| Farmer-group membership | Non-member | 18.34% |
| Household-head sex | Male | 21.40% |
| Household-head sex | Female | 13.06% |

### 4.2 Sample Reconciliation

Several household counts appear across this analysis. They are
not contradictions; each reflects a different stage of the
analytical pipeline.

| Stage | Households | Reason for exclusion |
|---|---:|---|
| AGSEC1 agricultural households | 2,191 | — |
| − No valid seed-type record in either visit | −213 | Outcome could not be resolved as 0/1 |
| = Households with a known adoption outcome | 1,978 | — |
| − Missing data on one or more predictors | −40 | Complete-case analysis |
| = Final analytical sample | 1,938 | — |

An earlier draft of this analysis reported a sample of 1,962,
using a stricter classification rule that required a household
to appear in both agricultural visits to be classified as an
adopter. The current analysis uses an *ever-adopter* rule:
a household is counted as an adopter if at least one visit
confirms improved-seed use. This reclassifies 207 seasonally
inconsistent households as adopters (see Section 7) and adds
14 households that appeared only in the second visit's
agricultural module. The final sample of 1,938 reflects these
changes plus complete-case filtering on the predictors.

## 5. Unadjusted Associations

- **NAADS training participation:** +10.3 percentage points
- **Farmer-group membership:** +12.3 percentage points
- **Male household head:** +8.3 percentage points

All three predictors show meaningful bivariate associations with
adoption. The adjusted model (Section 6) tests whether these
associations persist after controlling for confounding.

## 6. Adjusted Logistic Regression

### 6.1 Sample

The final analytical sample used for modeling contains **1,938**
households with complete data on the outcome and all predictors.

### 6.2 Main Model Results

| Predictor | Odds Ratio | 95% CI | P-value |
|---|---:|---:|---:|
| Male household head (vs. female) | **1.82** | [1.29, 2.56] | **0.0007** |
| NAADS training participation | 1.41 | [—] | 0.2192 |
| Farmer-group member | 1.51 | [—] | 0.2447 |
| Centered head age | 1.00 | [0.99, 1.01] | n.s. |
| Centered head age squared | 1.00 | [1.00, 1.00] | n.s. |
| Married (vs. divorced/separated) | 1.02 | [0.62, 1.68] | 0.95 |
| Widowed or never married | 1.05 | [0.60, 1.86] | 0.85 |

**Household-head sex was the only statistically significant predictor.**
Male-headed households had approximately 1.82 times the odds
of improved-seed adoption compared to female-headed households
(95% CI [1.29, 2.56], p = 0.0007).

### 6.3 Robustness Analysis

To test whether the results were driven by the seasonally-inconsistent
households, the model was re-estimated on the subset of
1,731 households with consistent
visit-level responses. The male-head association strengthened to an
odds ratio of **2.87** (95% CI
[1.65, 5.00],
p = 0.0002), confirming the robustness of the main finding.
The robustness model's pseudo-R² was 0.0317.

### 6.4 Interpretation

NAADS training participation and farmer-group membership showed strong
bivariate associations with adoption (+10.3
and +12.3 percentage points respectively) but
did not reach statistical significance in the adjusted model. This
pattern is consistent with confounding — male-headed households were
more likely to participate in both programs, and once head sex is
controlled for, the direct effects are no longer distinguishable from
zero in this sample.

The model's McFadden pseudo-R² of 0.0159 indicates that
the observed predictors explain only a small share of adoption
behavior. This is typical of cross-sectional adoption studies and
points to important unobserved factors (input prices, market access,
extension contact, plot-level characteristics).

## 7. Seasonal Inconsistency

Of the 363 classified adopters, **207
(57.0%)** reported improved-seed use in only one of the
two agricultural seasons. The remaining 156
used improved seeds consistently across visits. This finding suggests
that for many Ugandan farming households, improved-seed adoption is
a seasonal strategy rather than a year-round practice.

## 8. Limitations

1. **Observational design.** The analysis is cross-sectional and
   cannot establish causal relationships.
2. **Low explanatory power.** The model's pseudo-R² of 0.0159
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

In the 2018/19 UNPS analytical sample, 18.73% of
agricultural households used improved seeds at least once during the
survey year, with the weighted estimate at 19.81%.
Household-head sex was the only robust predictor of adoption in the
adjusted model. NAADS training and farmer-group membership showed
substantial bivariate associations that attenuated after adjustment.
The prevalence of seasonal inconsistency among adopters highlights
the importance of careful adoption definitions in panel surveys.

---

*This report was regenerated automatically from the analytical
pipeline. All numbers reflect the latest fitted models and dataset.*


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

