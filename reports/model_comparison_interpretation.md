# Logistic Regression: Model Comparison and Interpretation

*Last regenerated: 2026-10-13 17:57*

## 1. Objective

Two logistic regression models were fitted to examine correlates of
improved-seed adoption in the 2018/19 UNPS sample:

1. **Main model** — fitted to the full analytical sample of
   1,938 households, using the ever-adopter outcome definition.
2. **Robustness model** — fitted to the subset of 1,731 households
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

**Observations:** 1,938
**Pseudo R²:** 0.0159

| Predictor | Odds Ratio | 95% CI | P-value |
|---|---:|---:|---:|
| Male household head | **1.82** | [1.29, 2.56] | **0.0007** |
| NAADS training participation | 1.41 | — | 0.2192 |
| Farmer-group member | 1.51 | — | 0.2447 |

Household-head sex was the only statistically significant predictor.
Male-headed households had approximately **1.82 times the
odds** of improved-seed adoption compared to female-headed households
(95% CI [1.29, 2.56], p = 0.0007).

NAADS training participation (OR = 1.41, p = 0.2192)
and farmer-group membership (OR = 1.51, p = 0.2447)
did not reach statistical significance after adjustment.

## 4. Results — Robustness Model

**Observations:** 1,731
**Pseudo R²:** 0.0317

The male-head association strengthened in the seasonally consistent
subset: **OR = 2.87** (95% CI [1.65, 5.00],
p = 0.0002). No other predictor became statistically
significant. The direction and magnitude of NAADS and farmer-group
coefficients were stable, confirming that the main findings are not
sensitive to the classification of seasonally inconsistent households.

## 5. Seasonal Inconsistency

Of 363 classified adopters, **207** used improved
seeds in only one of the two agricultural visits:

- **98 households** reported traditional seed use in Visit 1
  and improved seed use in Visit 2.
- **109 households** reported improved seed use in Visit 1
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

**Explanatory power.** The pseudo-R² values (main: 0.0159;
robustness: 0.0317) indicate limited explanatory power.
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
