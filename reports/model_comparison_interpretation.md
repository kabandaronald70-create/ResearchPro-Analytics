# Logistic Regression Model Comparison

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
