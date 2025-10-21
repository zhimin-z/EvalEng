# Quantus - Stage 5 (INTERPRET) Evaluation

## Summary
Quantus is a comprehensive XAI evaluation toolkit that primarily focuses on metric computation and aggregation. It lacks dedicated interpretation and pattern analysis features, as it's fundamentally a metrics library rather than a full evaluation framework with built-in analytical capabilities. Users must perform their own post-hoc analysis of metric results.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S5F1: Stratified Analysis | 0 | No stratification capabilities exist. The framework computes metrics across batches uniformly without any native support for slicing by metadata, hierarchical stratification, disparity analysis, or Pareto frontiers. Users receive flat arrays of scores with no grouping mechanism. Evidence: `quantus/metrics/base.py` shows `evaluate_batch()` returns simple lists/arrays with no stratification support. |
| S5F2: Failure Analysis | 0 | No failure pattern detection or recommendation system exists. The framework only computes numerical scores without identifying failure modes, clustering errors, detecting biases, or providing actionable recommendations. Evidence: All metric implementations (e.g., `quantus/metrics/faithfulness/`) return scalar values or arrays without any analysis of failure patterns or improvement suggestions. |
| S5F3: A/B Test Analysis | 0 | No statistical testing capabilities for comparing methods. While users can evaluate multiple XAI methods via `quantus.evaluate()` (`quantus/evaluation.py`), the framework provides no significance testing, effect sizes, power analysis, or multiple comparison corrections. Users must manually perform statistical tests on returned score arrays. |
| S5F4: Interactive Exploration | 0 | No interactive tools whatsoever. The framework is purely programmatic with no UI, sample browser, drill-down capabilities, or visualization beyond basic matplotlib plotting functions. Evidence: `quantus/helpers/plotting.py` only contains static plotting utilities. The `plot()` method in `quantus/metrics/base.py` (lines 581-624) requires users to provide their own plotting functions. |

## Detailed Analysis

### S5F1: Stratified Analysis and Performance Tradeoff Analysis (0 points)

Evidence of absence:

1. No metadata support: The framework's data model (`quantus/metrics/base.py`, lines 215-285) only accepts:
   ```python
   def __call__(
       self,
       model: Union[keras.Model, nn.Module, None],
       x_batch: np.ndarray,
       y_batch: np.ndarray,
       a_batch: Optional[np.ndarray],
       s_batch: Optional[np.ndarray],  # Only segmentation masks
       # ... no metadata fields
   )
   ```
   There's no mechanism to pass or track metadata like difficulty, topic, or demographic information.

2. Simple aggregation only: The `quantus/evaluation.py` module shows the evaluation returns raw scores:
   ```python
   results = quantus.evaluate(
       metrics=metrics,
       xai_methods=xai_methods,
       agg_func=np.mean,  # Only simple aggregation
       # ... no stratification parameters
   )
   ```

3. No statistical testing: Searching the codebase reveals no chi-square tests, significance testing, or disparity detection. The `quantus/helpers/` directory contains utility functions but nothing for statistical analysis of subgroups.

4. No Pareto analysis: There's no code for multi-objective tradeoff analysis, efficiency curves, or Pareto frontier computation anywhere in the repository.

### S5F2: Failure Pattern and Bias Identification (0 points)

Evidence of absence:

1. No clustering capabilities: The codebase has no clustering algorithms (k-means, HDBSCAN) or error categorization. Metrics only return numerical scores:
   ```python
   # From quantus/metrics/base.py
   self.evaluation_scores = []
   # Just appends numerical results, no categorization
   ```

2. No bias detection: While there are robustness and faithfulness metrics, none perform systematic bias detection across demographics. The metrics documentation (e.g., `docs/source/docs_api/quantus.metrics.*.rst`) shows all metrics return scalar values or arrays without bias analysis.

3. No recommendations: The framework is purely evaluative. For example, looking at `tutorials/Tutorial_Getting_Started.ipynb`, users get scores like:
   ```python
   scores_intgrad = quantus.MaxSensitivity(...)
   # Returns: array of floats
   # No recommendations, just numbers
   ```

4. No outlier detection: There's no code for identifying anomalous predictions or population-level outliers in explanations.

### S5F3: A/B Test Statistical Analysis (0 points)

Evidence of absence:

1. No statistical testing: Searching for "t-test", "chi-square", "p-value", "confidence interval" in the codebase yields no results. The only scipy usage is in `quantus/functions/similarity_func.py` for correlation metrics, not hypothesis testing.

2. Manual comparison required: The tutorial `tutorials/Tutorial_Metric_Parameterisation_Analysis.ipynb` shows users must manually compare results:
   ```python
   # Users get raw scores and must do their own analysis
   scores_method_a = metric(...)
   scores_method_b = metric(...)
   # Framework provides no comparison statistics
   ```

3. No power analysis: The `quantus/` directory has no sample size calculators or power computation utilities.

4. No multiple comparison corrections: Since there's no hypothesis testing, there are also no Bonferroni or Benjamini-Hochberg corrections.

### S5F4: Interactive Exploratory Analysis (0 points)

Evidence of absence:

1. No UI components: The entire framework is Python library-based with no web interface or GUI. The tutorials all run in Jupyter notebooks with programmatic calls.

2. No sample browser: There's no functionality to interactively browse, filter, or search through evaluation results. Users work directly with numpy arrays.

3. No drill-down: The metric results are flat structures. From `quantus/metrics/base.py`:
   ```python
   self.evaluation_scores = []
   # Just a list - no hierarchical structure for drill-down
   ```

4. Limited visualization: The `quantus/helpers/plotting.py` file (if it exists based on imports) only provides basic plotting utilities. The base metric class shows:
   ```python
   def plot(
       self,
       plot_func: Optional[Callable] = None,  # User must provide
       show: bool = True,
       path_to_save: Optional[str] = None,
       *args,
       kwargs,
   ) -> None:
   ```
   Users must implement their own plotting logic.

5. No real-time analysis: All computation is batch-based and offline. There's no interactive filtering or on-the-fly metric computation.

## Supporting Evidence from Documentation

The README.md clearly positions Quantus as a metrics toolkit:
> "Quantus is an eXplainable AI toolkit for responsible evaluation of neural network explanations."

The "Getting Started" documentation (`docs/source/getting_started/getting_started_example.md`) shows the workflow:
1. Load data and model
2. Generate explanations  
3. Compute metric scores
4. User performs own analysis

There's no mention of interpretation features, stratification, or statistical comparison tools in any documentation.

## Conclusion

Quantus is a well-designed metrics computation library but provides zero built-in interpretation or analysis capabilities. It outputs numerical scores that users must analyze themselves using external tools. The framework's scope is intentionally limited to metric calculation rather than providing a comprehensive evaluation platform with analytical features.