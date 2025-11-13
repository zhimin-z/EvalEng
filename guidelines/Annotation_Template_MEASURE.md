# Stage 3: MEASURE - Evaluation Harness Assessment Template
## Structured Evaluation Format with Coverage Analysis

---

## Evaluation Format

For each feature, you will complete this structure:

```
S3FX: [Feature Name]
Grade: [Absent/Partial/Present] (XX% coverage)
Supports: [Sub-capability 1] ✓/✗, [Sub-capability 2] ✓/✗, ...
Documentation: [Quality assessment: Minimal/Moderate/Comprehensive]
Evidence: [Specific links, code examples, or behavioral observations supporting each ✓/✗]
```

**Coverage calculation:** `number of ✓ / (number of ✓ + number of ✗)`

**Grade mapping:**
- **Absent (0-30%)**: Feature missing, non-functional, or <2 sub-capabilities present
- **Partial (30-80%)**: Feature functional for common cases with significant gaps; 2-4 sub-capabilities present
- **Present (80-100%)**: Production-ready with comprehensive support; 5+ sub-capabilities present and well-integrated

---

## Feature 1: Output Format Validation

**Purpose:** Validate model outputs $O = \{o_i\}$ conform to benchmark-specified format requirements before measurement. Schema validation for structured outputs (JSON structure correctness, XML well-formedness, required fields present, type constraints satisfied), format consistency checks across outputs (uniform structure maintained), range validation (numerical values within expected bounds, categorical values from valid set). Systematically test whether parsing/validation process introduces measurement bias independent of model capability: does strict parsing penalize capable models with minor format deviations? Are format requirements capturing construct or formatting compliance? Flag parsing failures that prevent measurement with detailed diagnostics. Distinguish format compliance failures (model produced meaningful response in wrong format) from construct measurement failures (model doesn't understand task). If format constraints systematically affect performance across models, document as potential validity limitation. Ensures measurement captures target phenomenon rather than formatting compliance capability.

**Essential Capabilities:**
1. **JSON schema validation** - Validates JSON structure correctness, required fields present, nested objects correct, array constraints
2. **XML/structured format validation** - Well-formedness checking, schema conformance, element/attribute validation
3. **Format consistency checking** - Verifies uniform structure maintained across all outputs; detects schema violations
4. **Range/bound validation** - Validates numerical values within expected ranges, categorical values from valid set, constraints satisfied
5. **Parsing failure detection** - Identifies outputs that cannot be parsed; distinguishes format failures from construct failures
6. **Bias assessment** - Tests whether format validation introduces systematic bias (do format-strict models penalize capable models?)
7. **Fallback mechanism** - Handles format non-compliance gracefully (attempt recovery, partial parsing, or manual review pathways)
8. **Diagnostic reporting** - Detailed error messages identifying format violations, parse failures, constraint violations

**Look for:**
- JSON schema specifications or validation code
- XML/structured format validation implementation
- Schema consistency checking logic
- Range validation code with bounds/constraints
- Parsing error handling and recovery code
- Test cases showing format validation failures and successes
- Bias analysis code or documentation (does format strictness penalize capable models?)
- Format validation statistics (% parsing success, common failures)
- Documentation distinguishing format failures from construct failures
- Fallback or recovery mechanisms for format non-compliance
- Integration with measurement protocol (validation before scoring)

**Report template:**
```
S3F1: Output Format Validation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - JSON schema validation ✓/✗
  - XML/structured format validation ✓/✗
  - Format consistency checking ✓/✗
  - Range/bound validation ✓/✗
  - Parsing failure detection ✓/✗
  - Bias assessment ✓/✗
  - Fallback mechanism ✓/✗
  - Diagnostic reporting ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to schema validation code, format checks, bias assessment, error handling examples]
```

---

## Feature 2: Measurement Protocol Execution

**Purpose:** Execute measurement protocol $\mu$ specified in CONFIGURE with pluggable implementations supporting diverse measurement modalities. Human judgment implementation: integrate crowdsourcing platforms (Amazon MTurk, Prolific, Scale AI), rater qualification systems (screening tests, quality gates, training modules), attention checks (gold standard questions, timing analysis, logical consistency), inter-rater reliability computation (Krippendorff's $\alpha$, Fleiss' $\kappa$, ICC), demographic documentation for bias analysis. LLM-as-judge implementation: model selection (specify judge model), prompt design with structured rubrics (criteria, scale, examples), chain-of-thought reasoning prompts (explain before scoring), confidence calibration (probability calibration, uncertainty quantification), bias mitigation strategies (blinding, randomization, multiple judges). Algorithmic metrics: automated scoring functions (BLEU, ROUGE, BERTScore, semantic similarity), parameter configuration, threshold optimization. Ensemble combinations: voting schemes (majority vote, weighted vote), confidence weighting, disagreement resolution protocols. Return standardized measurement schema: score $s_i$, uncertainty estimate $u_i$, rationale/explanation $r_i$, scorer metadata $m_i$. Aggregate scores respecting inherent variability in subjective judgments without forcing single-point estimates.

**Essential Capabilities:**
1. **Human judgment execution** - Crowdsourcing integration (MTurk, Prolific, Scale AI), rater qualification, attention checks, IRR computation (Krippendorff's α, Fleiss' κ, ICC)
2. **LLM-as-judge implementation** - Judge model selection, rubric design, chain-of-thought prompts, confidence calibration, bias mitigation (blinding, randomization)
3. **Algorithmic metrics computation** - BLEU, ROUGE, BERTScore, semantic similarity, custom scoring functions with parameter configuration
4. **Ensemble measurement** - Voting schemes (majority, weighted), confidence weighting, disagreement resolution
5. **Standardized output schema** - All modalities return (score, uncertainty, rationale, metadata) structure
6. **Subjective judgment aggregation** - Preserves judgment variability (distributions, disagreement patterns) rather than forcing single-point estimates
7. **Metadata capture** - Records rater IDs (for demographic analysis), rater confidence, reasoning traces, timing data
8. **Pluggable measurement interface** - Can swap measurement implementations without harness modification; clean abstraction

**Look for:**
- Crowdsourcing platform integration code or documentation (MTurk, Prolific examples)
- Rater qualification implementation (screening, training, quality gates)
- Attention check implementation (gold standards, timing analysis)
- Inter-rater reliability computation code (Krippendorff's α, Fleiss' κ, ICC implementations)
- LLM judge model selection and configuration examples
- Rubric design and prompt examples for LLM judges
- Chain-of-thought prompt examples
- Confidence calibration code or methodology
- Algorithmic metrics library or function documentation (BLEU, ROUGE, BERTScore)
- Ensemble voting and weighting code
- Measurement output schema examples (score, uncertainty, rationale, metadata)
- Subjective judgment aggregation code (distribution preservation)
- Test cases showing measurement across multiple modalities
- Plugin/interface examples for custom measurement protocols

**Report template:**
```
S3F2: Measurement Protocol Execution
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Human judgment execution ✓/✗
  - LLM-as-judge implementation ✓/✗
  - Algorithmic metrics computation ✓/✗
  - Ensemble measurement ✓/✗
  - Standardized output schema ✓/✗
  - Subjective judgment aggregation ✓/✗
  - Metadata capture ✓/✗
  - Pluggable measurement interface ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to crowdsourcing integration, LLM judge examples, metrics library, ensemble code, schema definition]
```

---

## Feature 3: Baseline Comparison

**Purpose:** Execute identical measurement protocol $\mu$ on baseline systems specified in CONFIGURE ensuring fair comparison conditions: same data splits (identical train/validation/test partitions), same measurement protocol (same scoring function, same raters/judges, same aggregation), same hyperparameter tuning budget (equal optimization effort), same computational resources (comparable batch sizes, timeouts). Compare target system $M$ against baselines: random baseline (uniform random predictions, majority class baseline), majority baseline (most frequent class predictor), well-tuned classical methods (logistic regression with grid search, SVM with kernel tuning, gradient boosting with early stopping), state-of-the-art models (current best performers from published literature), human performance (expert annotations, crowd consensus). Enable convergent validity evidence: does target outperform simpler alternatives as expected? Enable discriminant validity assessment: is performance appropriate relative to human capability? Comparative context essential for interpreting absolute scores—score of 0.85 meaningless without knowing random baseline is 0.50 and human performance is 0.95. Prevent implausible comparative claims.

**Essential Capabilities:**
1. **Fair comparison enforcement** - Identical data splits, measurement protocol, hyperparameter budget, computational resources for all systems
2. **Random baseline execution** - Uniform random predictions and majority-class baseline with proper implementation
3. **Classical method baselines** - Logistic regression, SVM, decision trees with controlled hyperparameter tuning
4. **State-of-the-art integration** - Can incorporate published SOTA results or pre-trained models for comparison
5. **Human performance baseline** - Expert annotations or crowd consensus for ceiling/reference
6. **Protocol consistency** - Same measurement protocol applied to all systems (same raters/judges, scoring function, aggregation)
7. **Data partition equity** - All systems evaluated on identical train/validation/test splits
8. **Comparative result presentation** - Results clearly show target vs baselines with difference quantification

**Look for:**
- Fair comparison specification and enforcement code
- Random baseline implementation (uniform random, majority class)
- Classical method baseline configurations (logistic regression, SVM, decision tree examples)
- SOTA baseline integration examples (published models, results)
- Human performance baseline examples
- Code ensuring identical data splits and measurement protocol across all systems
- Hyperparameter tuning budget specification and tracking
- Comparative result tables showing baseline performance
- Validity evidence interpretation (convergent/discriminant validity discussion)
- Test cases showing fair comparison across multiple system types
- Documentation of comparison methodology and equity assurance

**Report template:**
```
S3F3: Baseline Comparison
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Fair comparison enforcement ✓/✗
  - Random baseline execution ✓/✗
  - Classical method baselines ✓/✗
  - State-of-the-art integration ✓/✗
  - Human performance baseline ✓/✗
  - Protocol consistency ✓/✗
  - Data partition equity ✓/✗
  - Comparative result presentation ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to fair comparison code, baseline implementations, protocol consistency checks, result table examples]
```

---

## Feature 4: Statistical Validation

**Purpose:** Compute uncertainty estimates for all primary scores per pre-specified analysis plan $\Sigma$ enabling robust model comparisons: confidence interval construction via bootstrap resampling (percentile method, bias-corrected accelerated BCa, specify resampling iterations typically 1000-10000) or parametric methods when distributional assumptions justified (t-distribution for normally distributed metrics, specify assumption verification tests). Statistical significance testing: permutation tests (for non-parametric comparison, exact p-values), t-tests (paired for within-subject design, independent for between-subject), Wilcoxon signed-rank (non-parametric alternative), apply pre-specified multiple comparison corrections (Bonferroni: $\alpha' = \alpha/k$ for $k$ comparisons, Benjamini-Hochberg FDR for less conservative control). Effect size computation: Cohen's $d$ (standardized mean difference), Hedges' $g$ (bias-corrected $d$ for small samples), confidence intervals on effect sizes. Evaluate metrics across multiple random seeds capturing run-to-run variability from stochastic processes. Report sample size with statistical power justification: achieved power for observed effect sizes. Enable robust model comparisons preventing spurious claims of differences arising from noise. All comparative claims accompanied by statistical evidence.

**Essential Capabilities:**
1. **Bootstrap confidence intervals** - Percentile method, BCa (bias-corrected accelerated), configurable iterations (1000-10000+)
2. **Parametric confidence intervals** - t-distribution CIs with assumption verification (normality tests); Wilson score interval for proportions
3. **Permutation testing** - Non-parametric significance testing with exact p-values
4. **T-tests implementation** - Paired t-tests (within-subject), independent t-tests (between-subject), assumes verification
5. **Wilcoxon signed-rank tests** - Non-parametric alternative to paired t-tests
6. **Multiple comparison correction** - Bonferroni correction, Benjamini-Hochberg FDR, Holm-Bonferroni method
7. **Effect size computation** - Cohen's d, Hedges' g (bias-corrected), confidence intervals on effect sizes
8. **Multi-seed evaluation** - Runs across multiple random seeds; captures stochastic variability; reports aggregated statistics

**Look for:**
- Bootstrap CI implementation with percentile and BCa methods
- Parametric CI code with assumption testing (normality verification)
- Permutation test implementation
- T-test implementations (paired and independent)
- Wilcoxon signed-rank test code
- Multiple comparison correction implementations
- Effect size computation functions (Cohen's d, Hedges' g)
- CI computation on effect sizes
- Multi-seed evaluation code
- Statistical testing result examples with p-values, effect sizes, CIs
- Power analysis and achieved power reporting
- Assumption verification tests (normality, homoscedasticity)
- Test cases showing statistical comparison workflow
- Documentation of statistical methods and assumptions

**Report template:**
```
S3F4: Statistical Validation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Bootstrap confidence intervals ✓/✗
  - Parametric confidence intervals ✓/✗
  - Permutation testing ✓/✗
  - T-tests implementation ✓/✗
  - Wilcoxon signed-rank tests ✓/✗
  - Multiple comparison correction ✓/✗
  - Effect size computation ✓/✗
  - Multi-seed evaluation ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to CI implementation, statistical test code, effect size functions, multi-seed examples, assumption verification]
```

---

## Feature 5: Fairness & Subgroup Analysis

**Purpose:** Assess measurement consistency across demographic groups and protected attributes to detect potential bias: compute performance metrics per subgroup (gender, race/ethnicity, age, language, geographic region, socioeconomic indicators), test for fairness criteria violations—demographic parity (equal selection rates: $P(\hat{Y}=1|A=a) = P(\hat{Y}=1|A=b)$), equalized odds (equal TPR/FPR across groups: $P(\hat{Y}=1|Y=1,A=a) = P(\hat{Y}=1|Y=1,A=b)$), predictive parity (equal precision across groups: $P(Y=1|\hat{Y}=1,A=a) = P(Y=1|\hat{Y}=1,A=b)$). Perform intersectional fairness assessment across attribute combinations (e.g., race $\times$ gender) as marginal analysis insufficient. Statistical significance testing within subgroups accounting for multiple comparisons and reduced sample sizes. If using human raters: document rater demographics, analyze rater agreement patterns for demographic bias (do certain demographics receive systematically different scores?), examine rater-ratee demographic concordance effects. Critical for understanding whether performance differences reflect construct measurement (model capability variation) or measurement bias (scorer bias). Informs model deployment decisions and fairness interventions.

**Essential Capabilities:**
1. **Subgroup performance computation** - Calculates metrics separately for each demographic group (gender, race, age, language, geography, SES)
2. **Demographic parity testing** - Tests equal selection/acceptance rates across groups ($P(\hat{Y}=1|A=a) = P(\hat{Y}=1|A=b)$)
3. **Equalized odds testing** - Tests equal TPR and FPR across groups ($P(\hat{Y}=1|Y=1,A=a) = P(\hat{Y}=1|Y=1,A=b)$ and FPR)
4. **Predictive parity testing** - Tests equal precision across groups ($P(Y=1|\hat{Y}=1,A=a) = P(Y=1|\hat{Y}=1,A=b)$)
5. **Intersectional analysis** - Fairness assessment across multiple attributes simultaneously (race × gender, not just marginal)
6. **Statistical significance in subgroups** - Tests with sample size adjustment and multiple comparison correction
7. **Rater demographic analysis** - If human raters: demographics documented, agreement patterns by rater demographics, rater-ratee concordance effects
8. **Bias detection and reporting** - Identifies fairness violations; flags systematic biases; reports disparities with magnitudes

**Look for:**
- Demographic subgroup tracking in data (gender, race, age, language, geography markers)
- Subgroup performance computation code with per-group metric calculation
- Fairness criterion implementation (demographic parity, equalized odds, predictive parity)
- Equalized odds computation (TPR and FPR per group)
- Intersectional analysis code (multi-attribute combinations)
- Statistical testing within subgroups (chi-square, t-tests, adjusted for multiple comparisons)
- Sample size adjustment for smaller subgroups
- Rater demographic tracking (if human evaluation)
- Rater agreement analysis by demographic (inter-rater reliability per group)
- Rater-ratee concordance analysis
- Fairness violation detection and flagging
- Bias reporting with disparities quantified (e.g., 15% gap between groups)
- Test cases showing fairness analysis across multiple protected attributes
- Documentation of fairness criteria and methodology

**Report template:**
```
S3F5: Fairness & Subgroup Analysis
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Subgroup performance computation ✓/✗
  - Demographic parity testing ✓/✗
  - Equalized odds testing ✓/✗
  - Predictive parity testing ✓/✗
  - Intersectional analysis ✓/✗
  - Statistical significance in subgroups ✓/✗
  - Rater demographic analysis ✓/✗
  - Bias detection and reporting ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to subgroup computation, fairness test implementations, intersectional analysis code, rater analysis, bias detection]
```

---

## Feature 6: Statistics Aggregation

**Purpose:** Summarize performance through comprehensive descriptive statistics providing distributional understanding beyond individual metric scores: central tendency measures (mean, median, mode), dispersion measures (standard deviation, variance, interquartile range), percentiles (quartiles, deciles, full distribution), full score distributions via histograms and kernel density estimates. Capture complete distributional properties: skewness and kurtosis revealing distributional shape, modality detection identifying multi-modal score distributions (e.g., bimodal indicating subsets of samples substantially easier/harder), tail behavior analysis (outlier prevalence, extreme performance instances). Compute aggregate uncertainty across all samples: population standard error, confidence intervals on mean score, credible intervals on full distribution parameters. Temporal aggregation for tracking evaluation evolution: aggregation by checkpoint, run, or date. Aggregation respects statistical properties, propagates uncertainties through calculations, avoids information loss from premature single-point summarization.

**Essential Capabilities:**
1. **Central tendency computation** - Mean, median, mode with proper handling of distributions
2. **Dispersion measures** - Standard deviation, variance, interquartile range, MAD (median absolute deviation)
3. **Percentile computation** - Quartiles, deciles, arbitrary percentiles, full quantile function
4. **Distribution visualization** - Histograms, kernel density estimation (KDE), empirical CDF plots
5. **Distributional shape analysis** - Skewness computation (asymmetry), kurtosis (tail weight), normality indicators
6. **Modality detection** - Identifies multi-modal distributions; detects easy vs hard subsets
7. **Tail behavior analysis** - Outlier detection and prevalence, extreme value analysis, tail risk quantification
8. **Uncertainty propagation** - Confidence intervals on Statistics Aggregation (mean, quantiles); credible intervals on distribution parameters

**Look for:**
- Statistical computation functions (mean, median, std dev, quantiles)
- Distribution visualization code (histograms, KDE, ECDF)
- Skewness and kurtosis computation
- Modality detection algorithm (peak detection, multimodality testing)
- Outlier detection and reporting (IQR method, z-score, isolation forest)
- Uncertainty quantification on aggregates (bootstrap CIs on mean, quantile CIs)
- Temporal aggregation code (by checkpoint, run date)
- Distribution summary examples (tables and figures)
- Handling of edge cases (single value, all identical, empty samples)
- Test cases showing comprehensive statistical summaries
- Documentation of statistical definitions and methods

**Report template:**
```
S3F6: Statistics Aggregation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Central tendency computation ✓/✗
  - Dispersion measures ✓/✗
  - Percentile computation ✓/✗
  - Distribution visualization ✓/✗
  - Distributional shape analysis ✓/✗
  - Modality detection ✓/✗
  - Tail behavior analysis ✓/✗
  - Uncertainty propagation ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to statistical computation, distribution visualization, shape analysis code, outlier detection, aggregation examples]
```

---

## Feature 7: Uncertainty Quantification

**Purpose:** Report uncertainties for all metrics enabling confidence in comparative claims and distinguishing statistical significance from practical significance: confidence interval construction with coverage guarantees (95% CI typical, 99% for high-stakes decisions), bootstrapped CIs (percentile bootstrap, BCa bootstrap with bias correction), parametric CIs when assumptions verified (t-distribution for sample means, Wilson score interval for proportions). Quantify multiple uncertainty sources and decompose total uncertainty: sampling variability (finite dataset size, estimated via bootstrap or analytical formulas), measurement variability (rater disagreement for human judgments, stochastic sampling for LLM judges, estimated via repeated measurements), model variability (random seed differences, weight initialization, estimated via multiple training runs). Propagate uncertainties through aggregations and transformations using Taylor approximation or Monte Carlo methods. Report point estimates with uncertainties: $\text{metric} = 0.85 \pm 0.03$ or $[0.82, 0.88]_{95\%}$. Distinguish statistical significance (p-value $< \alpha$) from practical significance (effect size $> \delta_{min}$). Support evidence-based decision making under uncertainty.

**Essential Capabilities:**
1. **Bootstrap confidence intervals** - Percentile method, BCa with bias correction, configurable coverage levels
2. **Parametric confidence intervals** - t-distribution CIs, Wilson score interval for proportions, assumption verification
3. **Sampling uncertainty quantification** - Estimated from finite sample size; bootstrap or analytical formulas
4. **Measurement uncertainty quantification** - Rater disagreement (human judgment), stochastic sampling (LLM judge), repeated measurement estimates
5. **Model variability quantification** - Random seed effects, initialization variability, estimated via multiple runs
6. **Uncertainty decomposition** - Separates sampling, measurement, and model variability; reports components
7. **Uncertainty propagation** - Through aggregations and transformations (Taylor approximation or Monte Carlo)
8. **Significance vs practical significance** - Distinguishes statistical significance (p < α) from practical significance (effect size > threshold)

**Look for:**
- Bootstrap CI implementation with multiple methods (percentile, BCa)
- Parametric CI code with assumption checking
- Sampling variance estimation code
- Measurement variability estimation (rater disagreement metrics, repeated measurement analysis)
- Model variability quantification (multi-seed experiment analysis)
- Uncertainty decomposition examples showing variance components
- Uncertainty propagation code (Taylor approximation or Monte Carlo)
- Reporting format examples (mean ± std, confidence intervals, credible intervals)
- Statistical vs practical significance explanation and computation
- Test cases showing uncertainty quantification across multiple sources
- Visualization of uncertainties (error bars, CIs, distributions)
- Documentation of uncertainty quantification methodology

**Report template:**
```
S3F7: Uncertainty Quantification
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Bootstrap confidence intervals ✓/✗
  - Parametric confidence intervals ✓/✗
  - Sampling uncertainty quantification ✓/✗
  - Measurement uncertainty quantification ✓/✗
  - Model variability quantification ✓/✗
  - Uncertainty decomposition ✓/✗
  - Uncertainty propagation ✓/✗
  - Significance vs practical significance ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to CI implementation, uncertainty estimation code, decomposition examples, propagation methodology, reporting format]
```

---

## Feature 8: Result Validation

**Purpose:** Perform comprehensive sanity checks on evaluation results before reporting preventing dissemination of invalid findings: verify baseline orderings make intuitive sense (random baseline should be worst, strong baselines competitive, human performance near ceiling), check for unexpected metric patterns suggesting bugs (zero variance indicating all predictions identical, perfect scores suggesting data leakage, inverse correlations between metrics that should agree), validate score ranges match expectations (probabilities in [0,1], counts non-negative, bounded metrics within bounds), confirm statistical test assumptions (normality tests for parametric methods, independence checks for correlation tests, homoscedasticity for ANOVA). Cross-validate results against prior work: are performance levels consistent with published benchmarks? Do ranking orders match expectations from related tasks? Flag implausible results requiring investigation: superhuman performance on difficult tasks, dramatic performance drops on similar tasks, inconsistent relative performance across metrics. Catch implementation bugs (incorrect metric computation, wrong aggregation, label mismatches), data quality issues (corrupted labels, distribution shift, contamination), measurement failures (scorer errors, parsing bugs) before propagation to reports. Final quality gate maintaining result integrity.

**Essential Capabilities:**
1. **Baseline ordering validation** - Checks random baseline worst, strong baselines competitive, human near ceiling
2. **Metric pattern checking** - Detects zero variance (uniform predictions), perfect scores (potential leakage), inverse correlations (metric disagreement)
3. **Score range validation** - Verifies probabilities in [0,1], counts non-negative, bounded metrics within bounds
4. **Statistical assumption verification** - Normality tests, independence checks, homoscedasticity tests (Levene's test)
5. **Prior work comparison** - Validates results against published benchmarks; checks consistency with expected performance levels
6. **Ranking consistency** - Verifies ranking order makes sense; checks consistency across metrics and related tasks
7. **Implausible result detection** - Flags superhuman performance, dramatic performance drops, metric disagreement
8. **Bug and data quality detection** - Identifies implementation bugs, corrupted labels, distribution shifts, contamination evidence

**Look for:**
- Baseline ordering validation code (random < strong < human comparisons)
- Metric pattern detection code (zero variance, perfect scores, correlation checks)
- Range validation code with bounds checking
- Statistical assumption testing (normality: Shapiro-Wilk, K-S; homoscedasticity: Levene's test)
- Prior work comparison utilities (lookup published results, compare performance levels)
- Ranking validation and consistency checks
- Outlier/implausible result detection (z-score, domain-specific rules)
- Bug detection patterns (label mismatches, metric computation errors, aggregation issues)
- Data quality checks (corrupted samples, distribution shift indicators, contamination signals)
- Sanity check report generation
- Test cases showing validation workflows
- Documentation of validation rules and thresholds
- Examples of caught bugs/issues and alerts

**Report template:**
```
S3F8: Result Validation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Baseline ordering validation ✓/✗
  - Metric pattern checking ✓/✗
  - Score range validation ✓/✗
  - Statistical assumption verification ✓/✗
  - Prior work comparison ✓/✗
  - Ranking consistency ✓/✗
  - Implausible result detection ✓/✗
  - Bug and data quality detection ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to validation code, baseline checking, metric pattern detection, assumption testing, implausible result examples]
```

