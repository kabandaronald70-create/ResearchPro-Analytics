# Agricultural Technology Adoption in Uganda
## ResearchPro Analytics — Final Analysis Report

## 1. Executive Summary

This exploratory analysis examined household adoption of improved
seeds using data from the Uganda National Panel Survey 2018–2019.
The analysis considered seed-use patterns, NAADS training participation,
farmer-group membership, household-head age and sex.

Among the 1,978 households with known adoption outcomes, 252 were
classified as adopters, giving an observed adoption rate of 12.74%.
A further 213 household records had unknown adoption outcomes and
were excluded from analyses requiring a known outcome.

The adjusted logistic regression used 1,962 complete observations.
The expanded model improved fit over the baseline model
(likelihood-ratio chi-square(3) = 16.92, p = .000733).
Household-head sex was significantly associated with adoption,
while training participation, farmer-group membership and age terms
were not statistically significant after adjustment.

Predictive performance was weak. The class-weighted model achieved
a test-set ROC AUC of 0.5524 and recall of 64%, but precision was
13.97%. These findings suggest that the current predictor set does
not reliably distinguish adopters from non-adopters.

The results are exploratory and should not be interpreted causally
or as estimates specific to Kibalinga Sub-County.

## 2. Data Source and Scope

The analysis used agricultural and household information from the
Uganda National Panel Survey 2018–2019, collected by the Uganda
Bureau of Statistics with support from the World Bank.

The survey is national in scope. This analysis does not establish
that the sample is representative of Kibalinga Sub-County.

The principal analytical unit for the adoption and modelling
analyses was the household interview record. Agricultural seed
information originated from crop-level records and was aggregated
to the household level for the adoption outcome.

## 3. Adoption Outcome Definition

Households were classified using observed improved-seed information
from their crop records:

- Adopter: at least one crop record indicated improved-seed use.
- Non-adopter: at least one valid seed-type record was available,
  and no improved-seed crop record was observed.
- Unknown: no valid seed-type record was available to establish
  adoption status.

The resulting household classification contained:

| Adoption status | Households |
|---|---:|
| Adopter | 252 |
| Non-adopter | 1,726 |
| Unknown | 213 |
| Total | 2,191 |

Among the 1,978 households with known outcomes, the observed
adoption rate was 12.74% (252/1,978).

This operational definition measures adoption as observed in the
available crop records. It should not be assumed to capture every
possible form of agricultural technology adoption.

## 4. Crop-Level Seed-Use Patterns

Crop-record summaries showed variation in the observed use of
improved seeds across crops.

Among the five crops examined in the exploratory comparison,
improved-seed use among records with valid seed-type responses was:

| Crop | Improved-seed records | Valid seed-type records | Percentage |
|---|---:|---:|---:|
| Banana food | 2 | 99 | 2.02% |
| Beans | 13 | 1,377 | 0.94% |
| Cassava | 35 | 495 | 7.07% |
| Maize | 132 | 1,342 | 9.84% |
| Sweet potatoes | 2 | 314 | 0.64% |

The five-crop chi-square comparison found an association between
crop category and seed type, chi-square(4) = 130.82, p < .001,
Cramer's V = 0.190.

The effect size indicates a relatively weak association. The
observations are crop records rather than independent households,
so this unadjusted test does not account for multiple crop records
from the same household or the complex survey design.

Percentages in this table are based on valid seed-type records
for each crop, not on the number of farmers growing that crop.

## 5. Unadjusted Associations with Adoption

### 5.1 NAADS Training Participation

Among households with valid values for the relevant variables,
the observed adoption rate was 22.32% for households reporting
NAADS training participation and 12.22% for those not reporting
participation.

The association was statistically significant:
chi-square(1) = 9.67, p = .002, Cramer's V = 0.070.

The effect size was small. This unadjusted association does not
establish that training caused adoption.

### 5.2 Farmer-Group Membership

The observed adoption rate was 25.40% among farmer-group members
and 12.37% among non-members.

The association was statistically significant:
chi-square(1) = 9.27, p = .002, Cramer's V = 0.069.

The effect size was small, and the result is unadjusted for
other household characteristics or survey design.

### 5.3 Household-Head Sex

The observed adoption rate was 14.85% for male-headed households
and 8.43% for female-headed households.

The association was statistically significant:
chi-square(1) = 15.83, p < .001, Cramer's V = 0.090.

The effect size was small. This result is an unadjusted association
and should not be interpreted causally.

### 5.4 Household-Head Age

The age distributions of adopters and non-adopters did not differ
significantly in the Mann–Whitney U test:
U = 204,690, p = .231.

The age-group comparison also did not identify a statistically
significant association:
chi-square(6) = 5.87, p = .437, Cramer's V = 0.055.

These findings do not provide strong evidence of an association
between household-head age and adoption in this sample.

## 6. Adjusted Logistic Regression

The adjusted logistic regression used 1,962 complete household
observations. The outcome was binary improved-seed adoption.

The model included NAADS training participation, farmer-group
membership, centered household-head age, centered age squared,
and a male household-head indicator.

### 6.1 Model Comparison

The baseline model included training participation and farmer-group
membership. The expanded model added age, age squared and sex.

| Measure | Baseline | Expanded |
|---|---:|---:|
| Observations | 1,962 | 1,962 |
| Log-likelihood | -745.3417 | -736.8809 |
| McFadden pseudo-R-squared | 0.0067 | 0.0179 |

The likelihood-ratio test indicated improved fit:
chi-square(3) = 16.92, p = .000733.

Although the expanded model fitted better than the baseline,
its explanatory power remained limited.

### 6.2 Adjusted Predictor Results

| Predictor | Coefficient | P-value | Interpretation |
|---|---:|---:|---|
| NAADS training participation | 0.4113 | .178 | Not statistically significant |
| Farmer-group membership | 0.5651 | .138 | Not statistically significant |
| Centered household-head age | -0.0017 | .721 | Not statistically significant |
| Centered age squared | -0.0002 | .505 | Not statistically significant |
| Male household head | 0.6167 | .0002 | Statistically significant positive association |

The estimated odds ratio for male-headed households was approximately
1.85, with an approximate 95% confidence interval of 1.34 to 2.56.
Conditional on the other variables in the model, male-headed
households had higher estimated odds of adoption than female-headed
households.

This is an observational association and does not establish a
causal effect. The model does not account for all potential
confounding factors.

## 7. Predictive Modelling

Predictive evaluation used 1,962 complete observations, split into
1,569 training records and 393 test records. The test set contained
50 adopters and 343 non-adopters.

Predictors included NAADS training participation, farmer-group
membership, household-head age and sex.

### 7.1 Test-Set Performance

| Metric | Standard logistic model | Class-weighted model |
|---|---:|---:|
| ROC AUC | 0.5394 | 0.5524 |
| Accuracy | 87.28% | 45.29% |
| Balanced accuracy | 50.00% | 53.28% |
| Precision | 0.00% | 13.97% |
| Recall | 0.00% | 64.00% |
| F1-score | 0.0000 | 0.2294 |

The standard model classified all test observations as non-adopters
at the default threshold of 0.50. Its high accuracy therefore
concealed its failure to identify adopters.

The class-weighted model identified 32 of the 50 adopters but
incorrectly classified 197 non-adopters as adopters. Its ROC AUC
of 0.5524 indicates weak discrimination.

The models should be treated as exploratory baselines, not as
deployment-ready prediction systems. Threshold selection should
be based on validation data and the intended practical objective.

## 8. Limitations

1. The analysis is observational and does not establish causation.
2. Survey sampling weights, strata and clustering were not
   incorporated into the reported statistical tests or regression.
3. The data are from a national Ugandan survey and are not
   specifically representative of Kibalinga Sub-County.
4. Adoption was operationalized using improved-seed crop records;
   it is not a comprehensive measure of every agricultural technology.
5. Missing and skipped responses may affect the available analysis
   samples. Unknown outcomes were not treated as non-adopters.
6. The complete-case models use 1,962 households, fewer than the
   1,978 households with known adoption outcomes.
7. Crop-level records from the same household are not independent.
8. The predictive models use a limited set of predictors and show
   weak test-set discrimination.
9. Predictive performance was assessed using one train-test split,
   so results may vary across different samples.

## 9. Recommendations

- Incorporate the survey's weights, strata and clustering when
  conducting population-level inference, using appropriate methods.
- Investigate additional predictors supported by the survey and
  relevant agricultural theory.
- Assess missing-data patterns and explain complete-case exclusions.
- Evaluate predictive stability with an appropriate validation
  strategy and compare models against simple baselines.
- Examine probability calibration and class-specific performance.
- Select classification thresholds using validation data and a
  clearly stated decision objective.
- Avoid making claims about Kibalinga Sub-County without data and
  a sampling design suitable for that population.

## 10. Conclusion

In this exploratory analysis, improved-seed adoption was observed
in 12.74% of households with known adoption outcomes. Unadjusted
tests found small associations between adoption and NAADS training,
farmer-group membership, and household-head sex. In the adjusted
model, household-head sex remained statistically significant, while
training participation, group membership and age terms did not.

The expanded logistic regression improved fit over the baseline
model, but explanatory power remained limited. Predictive evaluation
also showed weak discrimination, even with class weighting.

These findings provide a starting point for further analysis.
Survey-design-aware inference, stronger predictor selection and
additional validation are necessary before drawing population-level
or operational conclusions.
