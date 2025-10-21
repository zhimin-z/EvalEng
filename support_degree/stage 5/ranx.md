# ranx - Stage 5 (INTERPRET) Evaluation

## Summary
ranx is a Python library for ranking evaluation and comparison in Information Retrieval. It provides basic statistical comparison capabilities through hypothesis testing and tabular reporting, but lacks sophisticated stratification, failure analysis, and interactive exploration features typical of comprehensive evaluation frameworks.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S5F1: Stratified Analysis | 0 | No stratification or slicing capabilities found. The framework evaluates runs globally across all queries but provides no mechanism to slice results by metadata fields, difficulty levels, topics, or demographics. Evidence: No stratification features in `ranx/meta/evaluate.py` or `ranx/meta/compare.py`. The only grouping is by query ID for per-query scores. |
| S5F2: Failure Analysis | 0 | No failure pattern analysis, error clustering, or bias detection features. The framework computes aggregate metrics and per-query scores but provides no tools to identify failure patterns, cluster errors, or detect systematic biases. Evidence: No relevant code in `ranx/meta/`, `ranx/metrics/`, or documentation (`docs/*.md`). |
| S5F3: A/B Test Analysis | 2 | Basic statistical significance testing with three test options (Student's t-test, Fisher's randomization, Tukey's HSD), confidence in differences via superscripts in reports, but no power analysis, effect sizes (Cohen's d), sequential testing, or multiple comparison corrections beyond simple p-value thresholds. Evidence: `ranx/statistical_tests/__init__.py` (lines 11-91), `ranx/meta/compare.py` (lines 34-36: `stat_test` parameter), `docs/stat_tests.md`. Reports show significance via superscripts but no effect size metrics or power calculations. |
| S5F4: Interactive Exploration | 0 | No interactive UI, sample browser, or drill-down capabilities. All outputs are static (text reports, LaTeX tables, JSON files). While notebooks demonstrate usage, there's no programmatic or UI-based interactive exploration of individual samples, filtering, or dynamic visualization. Evidence: `ranx/data_structures/report.py` shows only static `__str__`, `to_latex`, `to_dict` methods. No interactive tools in codebase or documentation (`docs/report.md`). |

---

## Detailed Analysis

### S5F1: Stratified Analysis and Performance Tradeoff Analysis
Rating: 0 points

Evidence:
1. No Stratification Features: The core evaluation functions (`ranx/meta/evaluate.py`) only compute metrics globally or per-query:
   ```python
   # ranx/meta/evaluate.py lines 13-89
   def evaluate(
       qrels: Qrels,
       run: Run,
       metrics: Union[str, List[str]],
       # ... no parameters for stratification, metadata slicing, or subgroup analysis
   ```

2. No Metadata Support: The `Run` and `Qrels` classes (`ranx/data_structures/run.py`, `ranx/data_structures/qrels.py`) store only query-document-score triplets with no metadata fields for topics, difficulty, demographics, etc.

3. No Disparity Analysis: No code for identifying performance gaps across subgroups, intersectional analysis, or statistical tests for disparities.

4. No Multi-Objective Tradeoffs: While the framework supports fusion of multiple runs (`ranx/fusion/`), there's no Pareto frontier computation, efficiency curves (performance vs cost/latency), or resource analysis features.

5. Documentation Confirmation: None of the documentation files (`docs/evaluate.md`, `docs/compare.md`, `docs/metrics.md`) mention stratification, slicing, or subgroup analysis capabilities.

Conclusion: The framework operates at the query-level only, with no provisions for hierarchical or metadata-based stratification, making sophisticated analysis of subgroup performance impossible.

---

### S5F2: Failure Pattern and Bias Identification with Recommendations
Rating: 0 points

Evidence:
1. No Error Clustering: The framework computes per-query metric scores but provides no tools to cluster failures or categorize error types:
   ```python
   # ranx/meta/evaluate.py lines 62-74
   # Returns only numeric scores, no error analysis
   if return_mean:
       return mean_scores
   else:
       return scores  # Just arrays of per-query metrics
   ```

2. No Bias Detection: No statistical tests for systematic bias across demographics, fairness metrics, or intersectional analysis. The only bias-related capability is basic statistical significance testing between runs.

3. No Outlier Detection: While per-query scores are available, there's no automatic outlier detection, anomalous prediction flagging, or severity scoring.

4. No Recommendations: The framework provides no hyperparameter tuning suggestions, prompt optimization recommendations, or dataset expansion priorities based on evaluation results. The fusion optimization (`ranx/fusion_optimization/`) is for combining runs, not for improving individual models.

5. Documentation Confirmation: No mention of failure analysis, error patterns, or recommendations in any documentation file.

Conclusion: ranx is purely a metrics computation and comparison framework with no analytical capabilities for understanding failures or generating actionable recommendations.

---

### S5F3: A/B Test Statistical Analysis
Rating: 2 points

Evidence:
1. Multiple Statistical Tests Available:
   ```python
   # ranx/statistical_tests/__init__.py lines 11-91
   def compute_statistical_significance(
       model_names: List[str],
       metric_scores: Dict[str, Dict[str, np.ndarray]],
       stat_test: str = "fisher",  # Default is Fisher's randomization test
       # ...
   ):
       # Supports 'fisher', 'student', 'tukey'
   ```
   - Fisher's Randomization Test (`ranx/statistical_tests/fisher_randomization_test.py`)
   - Paired Student's t-Test (`ranx/statistical_tests/paired_student_t_test.py`)
   - Tukey's HSD Test (`ranx/statistical_tests/tukey_hsd_test.py`)

2. Significance Reporting: Results include p-values and statistical significance indicators via superscripts in reports:
   ```python
   # ranx/data_structures/report.py lines 134-160
   # Superscripts (ᵃᵇᶜ) indicate which models a given model significantly outperforms
   ```
   Documentation example (`docs/compare.md`):
   ```
   #    Model    MAP@100    MRR@100    NDCG@10
   ---  -------  --------   --------   ---------
   a    model_1  0.320ᵇ     0.320ᵇ     0.368ᵇᶜ
   ```

3. Missing Advanced Features:
   - No Effect Sizes: No Cohen's d, relative improvement percentages, or practical significance assessment reported
   - No Confidence Intervals: Only p-values, no confidence intervals around differences
   - No Power Analysis: No sample size calculators, power computation, or minimum detectable effect calculations
   - No Sequential Testing: No early stopping support or sequential confidence intervals
   - No Multiple Comparison Corrections: The `max_p` parameter (`ranx/meta/compare.py` line 36) is a simple threshold, not a proper correction method like Bonferroni or Benjamini-Hochberg

4. Documentation: `docs/stat_tests.md` confirms only basic test availability without advanced analysis features.

Conclusion: Basic significance testing exists with three test options, but lacks effect sizes, power analysis, sequential testing, and proper multiple comparison corrections. Manual calculations would be needed for these advanced features.

---

### S5F4: Interactive Exploratory Analysis
Rating: 0 points

Evidence:
1. Static Outputs Only: The `Report` class (`ranx/data_structures/report.py`) provides only static outputs:
   ```python
   # ranx/data_structures/report.py lines 103-225
   def __str__(self) -> str:  # Static table
   def to_latex(self) -> str:  # Static LaTeX
   def to_dict(self) -> Dict:  # Static dictionary
   def save(self, path: str):  # Save JSON
   ```

2. No Sample Browser: No functionality to browse individual query-document pairs, filter by scores, or search through results. The framework operates at the query-level aggregation only.

3. No Drill-Down: While per-query scores are available (`run.scores`), there's no interactive drill-down from aggregate metrics to individual samples, no side-by-side comparison UI, or multi-level navigation.

4. No On-the-Fly Analysis: All metric computation happens via the `evaluate` function with no interactive UI for custom metric computation, real-time filtering, or dynamic visualization updates.

5. Jupyter Integration: The notebooks (`notebooks/*.ipynb`) demonstrate API usage but are standard code cells, not interactive widgets or specialized exploratory tools:
   ```python
   # notebooks/4_comparison_and_report.ipynb
   # Just standard print statements and function calls, no interactive UI
   report = compare(...)
   print(report)
   print(report.to_latex())
   ```

6. Plotting: The `ranx/meta/plot.py` file provides only static Interpolated Precision-Recall curves via seaborn, not interactive visualizations:
   ```python
   # ranx/meta/plot.py lines 27-66
   def plot(...) -> Union[DataFrame, None]:
       # Returns static seaborn plot or DataFrame
       sns.lineplot(...)
   ```

7. Documentation: No mention of interactive features in `docs/report.md`, `docs/evaluate.md`, or any other documentation file.

Conclusion: ranx is purely a command-line/script-based evaluation framework with static outputs. All exploration must be done manually through code, with no interactive UI, sample browser, or drill-down capabilities.

---

## Overall Assessment

Total Score: 2/12 points

ranx is a lightweight, fast evaluation library focused on efficient metrics computation and basic statistical comparison for Information Retrieval. Its strengths lie in:
- Speed (leverages Numba for parallelization)
- Comprehensive metric coverage (12 ranking metrics)
- Multi-run fusion algorithms (25+ fusion methods)
- Integration with ir-datasets for qrels and ranxhub for pre-computed runs
- Clean API and good documentation

However, it completely lacks the sophisticated analysis and interpretation features expected in Stage 5:
- No stratification or metadata-based slicing
- No failure analysis or error clustering
- No bias detection or fairness metrics
- No interactive exploration tools
- Basic statistical testing without effect sizes or power analysis
- No actionable recommendations generation

ranx is best suited for researchers who need fast, accurate metric computation and basic statistical comparison, but who are comfortable writing custom code for deeper analysis. For comprehensive evaluation with built-in interpretation features, a more full-featured framework would be needed.