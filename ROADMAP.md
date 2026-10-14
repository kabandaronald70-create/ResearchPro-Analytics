Project: ResearchPro Analytics
Current state: MVP shipped (analysis + tests + CI + dashboard + README polish)
Goal: Reference-quality research repository (statistician + engineer approved)
Effort: ~5 hours/week × 12 weeks

Phase 1 — Software foundation (Weeks 1–3)
Week 1 — Packaging and modernization
□ Create pyproject.toml (PEP 621 layout)
□ Move src/*.py → src/researchpro/ package
□ Add __init__.py files
□ Create .pre-commit-config.yaml (nbstripout + leak-check)
□ Create Makefile (install, test, lint, dashboard, leak-check)
□ Verify: fresh venv → pip install -e ".[dev,dashboard]" → pytest tests/ (25 pass)
□ Commit and push
Considerations:

Use PEP 621, not legacy setup.py

Pin requires-python = ">=3.11"

Don't hardcode Windows paths anywhere

Update notebook sys.path calls if needed

Week 2 — CLI entry point
□ Install typer
□ Create src/researchpro/cli.py
□ Add researchpro run --data PATH --out PATH
□ Add researchpro dashboard
□ Add researchpro check-data --data PATH (stub for now)
□ Fix random seeds everywhere (random_state=42)
□ Sort all report outputs deterministically
□ Use logging, not print
□ Verify: researchpro run produces byte-identical reports to the notebook
□ Commit and push
Considerations:

Exit codes: 0 success, 1 user error, 2 data error, 3 unexpected

No silent fallbacks — raise if input missing

CLI calls functions in src/, doesn't duplicate logic

Week 3 — Notebook → pipeline refactor
□ Create src/researchpro/pipeline.py (run(config) -> None)
□ Create src/researchpro/data.py (loading + validation)
□ Create src/researchpro/reports.py (report generation)
□ Add PipelineConfig dataclass
□ Shrink notebook to: intro + from researchpro.pipeline import run + a few exploration cells
□ Add reports/pipeline_log.json (git SHA, file hashes, params, convergence)
□ Verify: pipeline output byte-matches old notebook output
□ Commit and push
Considerations:

Pure functions where possible

Cache expensive operations (functools.lru_cache)

Don't change results during refactor — move first, improve second

Phase 2 — Statistical depth (Weeks 4–7)
Week 4 — Missing-data analysis
□ Create reports/missingness_report.md
□ Visualize missingness (missingno matrix + heatmap)
□ Test MAR vs MCAR (missingness correlated with observed vars?)
□ Fit logistic model with multiple imputation (20 imputations)
□ Pool estimates using Rubin's rules
□ Build side-by-side table: complete-case vs MI estimates
□ Interpret: "conclusion is robust / sensitive"
□ Commit and push
Considerations:

Impute predictors only, never the outcome

Track random seeds per imputation

Include auxiliary variables (education, sex) in imputation model

Report CI widths, not just point estimates

Week 5 — Sensitivity analysis for seasonal classification
□ Parametrize outcome definition in config (ever | both | either)
□ Refit main model under all three definitions
□ Create reports/sensitivity_outcome_definitions.csv
□ Add comparison paragraph to final_analysis_report.md
□ Optionally: ordinal logistic on adoption intensity (0/1/2 visits)
□ Commit and push
Considerations:

Different outcomes = different sample sizes — report each N

Report OR, CI, p for each definition

Conclusion: "male-head OR is stable across definitions in range [X, Y]"

Week 6 — Predictive model calibration
□ Compute calibration curve (sklearn.calibration.calibration_curve)
□ Compute Brier score + bootstrap CI
□ Compute log loss
□ Run decision curve analysis (net benefit vs. threshold)
□ Add "Calibration" tab to Streamlit dashboard
□ Create reports/calibration_analysis.md
□ Commit and push
Considerations:

Use cross-validation for calibration (small test set)

Report Brier decomposition (reliability, resolution, uncertainty)

Cox calibration intercept/slope

Don't over-interpret with N=393 test set

Week 7 — Subgroup and interaction analyses
□ Pre-specify subgroups before looking at data
□ Subgroups: urban/rural, NAADS yes/no, farmer group yes/no, age <40/≥40
□ Fit model with interaction terms
□ Apply Holm-Bonferroni correction for 4 tests
□ Create forest plots (subgroup ORs with CIs)
□ Create reports/subgroup_analysis.md
□ Add forest plot to dashboard
□ Commit and push
Considerations:

Interaction term (formal test) > stratified models

Every subgroup needs N + CI

No data dredging — pre-specify

Format: | Subgroup | N | OR (95% CI) | p-interaction |

Phase 3 — Documentation and reproducibility (Weeks 8–10)
Week 8 — Documentation site
□ Install mkdocs + mkdocs-material + mkdocstrings
□ Create mkdocs.yml
□ Create docs/ pages: Home, Methodology, Data, Findings, Limitations, API, Reproducibility
□ Write Methodology page (why logistic, outcome choice, missing-data handling, survey-design limitation)
□ Add STROBE-style checklist
□ Add "What this analysis cannot tell you" section
□ Add GitHub Action to deploy on push
□ Link from README
□ Commit and push
Considerations:

Use absolute or repo-root-relative links

Don't commit site/ build output

Deploy from CI, not from your machine

Week 9 — Data validation with Pandera
□ Install pandera
□ Create src/researchpro/schemas.py
□ Define schemas for AGSEC1, AGSEC4A, AGSEC4B, GSEC1
□ Encode questionnaire coding (s4aq16 ∈ {1, 2, NA}, etc.)
□ Add range checks (age, weights, districts)
□ Add cross-variable checks (seed use implies seed type)
□ Wire into pipeline start
□ Fill in researchpro check-data command
□ Commit and push
Considerations:

Start lenient, tighten as you find real problems

Log every failed check with row indices

Exit code 2 on failures

Fail fast — run before expensive computation

Week 10 — Reproducibility guarantees
□ Generate requirements.lock (use uv or pip-tools)
□ Create Dockerfile (python:3.11-slim)
□ Create data/README.md (which UNPS files, where to get them)
□ Create REPRODUCIBILITY.md (step-by-step rerun guide)
□ Record package versions in pipeline_log.json
□ Verify: docker run produces byte-identical output
□ Commit and push
Considerations:

Don't bake raw data into Docker image — mount at runtime

Document all random seeds

Test the Docker build on a fresh machine (or CI)

Phase 4 — Deep extension + release (Weeks 11–12)
Week 11 — Pick ONE deep statistical extension
Choose one of:

□ Option A — Longitudinal / pseudo-panel analysis (fixed effects, first differences)
□ Option B — Heterogeneous treatment effects (causal forest via econml or grf)
□ Option C — Bayesian logistic regression (pymc or bambi)
□ Option D — Design-effect simulation (Monte Carlo with ρ = 0.05, 0.10, 0.20)
Whichever you pick:

□ Create src/researchpro/extension_x.py
□ Create notebooks/05_extension_x.ipynb (exploration)
□ Create reports/extension_x_findings.md
□ Add methods + sensitivity section
□ Add to docs site
□ Commit and push
Considerations:

Depth beats breadth — don't try all four

Pick the one aligned with your career target (academic → A or D, industry → B, Bayesian → C)

Justify method choice explicitly

Week 12 — Release v1.0 + narrative
□ Tag v1.0.0 (git tag -a v1.0.0 -m "Initial public release")
□ Push tag (git push origin v1.0.0)
□ Create GitHub Release with notes
□ Create CHANGELOG.md (Keep a Changelog format)
□ Create CITATION.cff
□ Create LICENSE (MIT or Apache 2.0 for code)
□ Write portfolio blog post in docs/blog/
□ Update README with:
□ Repo structure diagram
□ Installation one-liner
□ Usage examples
□ Citation block
□ Publish blog post (LinkedIn, personal site, Medium)
□ Final "10-second test": stranger understands what/how/what for in 10 seconds
Considerations:

Write executive summary for non-statisticians

Include a limitations box

Cite UNPS properly (Uganda Bureau of Statistics via World Bank LSMS-ISA)