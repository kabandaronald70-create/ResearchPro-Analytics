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
