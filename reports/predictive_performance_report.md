# Predictive Performance Evaluation

## 1. Objective

This evaluation examines whether a logistic regression model can
distinguish households that adopted improved seeds from those that
did not, using selected household characteristics and agricultural
participation indicators from the Uganda National Panel Survey
2018–2019.

## 2. Data and methodology

The analysis used 1,962 complete household observations.

The data were divided into:
- Training set: 1,569 households (80%).
- Test set: 393 households (20%).

The split used random_state=42 and stratification by the outcome.
The outcome was improved-seed adoption. Predictors included NAADS
training participation, farmer-group membership, household-head age
and household-head sex.

Age-centering was calculated using the training set only and then
applied to both datasets. The model was fitted using a pipeline with
standardization and logistic regression.

The test set contained 50 adopters and 343 non-adopters.

## 3. Results

| Metric | Threshold 0.50 | Threshold 0.10 |
|---|---:|---:|
| ROC AUC | 0.5394 | 0.5394 |
| Average precision | 0.1697 | 0.1697 |
| Accuracy | 0.8728 | 0.3766 |
| Balanced accuracy | 0.5000 | 0.5403 |
| Precision | 0.0000 | 0.1402 |
| Recall | 0.0000 | 0.7600 |
| F1-score | 0.0000 | 0.2368 |

The threshold of 0.50 classified every test observation as a
non-adopter. Although accuracy was 87.28%, the model failed to
identify any of the 50 actual adopters. This illustrates why
accuracy alone is misleading when the outcome classes are imbalanced.

At a threshold of 0.10, the model identified 38 of the 50 adopters
and missed 12. However, it also incorrectly classified 233
non-adopters as adopters. Of the 271 households predicted to adopt,
only 38 actually adopted.

The ROC AUC of 0.5394 indicates weak discrimination. Average
precision was 0.1697, only modestly above the test-set adopter
prevalence of approximately 0.1272.

## 4. Interpretation

The model has limited predictive value in its current form.
Reducing the classification threshold improves recall but produces
many false positives. The default threshold produces high accuracy
only because non-adopters form the majority class.

The threshold of 0.10 is an exploratory comparison, not a final
operational threshold. Threshold selection should reflect the
intended use and be conducted using validation data rather than
optimizing against the test set.

## 5. Limitations

1. The analysis is exploratory and uses an unweighted test set.
2. The survey's sampling weights, strata and clustering have not
   been incorporated into this predictive evaluation.
3. The outcome represents household improved-seed adoption as
   operationally defined from crop records.
4. The model uses a limited set of predictors and may omit important
   factors related to adoption.
5. One train-test split provides only one estimate of predictive
   performance.
6. Associations in observational data do not establish causation.
7. The findings should not be generalized specifically to Kibalinga
   Sub-County because the dataset is from a national survey.

## 6. Recommendations

- Establish a simple baseline for comparison.
- Evaluate stability using cross-validation, with appropriate care
  for the survey's household and sampling design.
- Explore additional well-justified predictors.
- Check probability calibration and class-specific performance.
- Select a threshold using validation data and a clearly defined
  practical objective.
- Consider survey design and weighting before making population-level
  statistical claims.

## 7. Conclusion

The current logistic regression model does not reliably distinguish
improved-seed adopters from non-adopters. Its performance should be
treated as a baseline for further investigation rather than a
deployment-ready prediction system.

The results demonstrate the importance of evaluating multiple
metrics, examining confusion matrices and accounting for class
imbalance when assessing classification models.
