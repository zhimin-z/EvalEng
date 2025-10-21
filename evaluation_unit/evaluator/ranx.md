## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Core metric implementations in ranx/metrics directory
- File: `ranx/metrics/` directory
- Related Files: `tests/unit/ranx/metrics_test.py`
- Code Reference:
```python
def test_precision():
    y_true = List()
    y_true.append(np.array([[1, 1], [2, 1], [3, 1]]))
    # ... calculates precision as count/k
```
The `ranx/metrics/` directory implements standard Information Retrieval metrics including precision, recall, F1, MRR, MAP, NDCG, DCG, bpref, hits, hit_rate, and rank-biased precision. These are deterministic algorithmic functions that follow defined mathematical formulas. Test files confirm their algorithmic nature by validating calculations like precision computed as count/k. The metrics are reproducible - same inputs always produce same outputs - and follow established IR evaluation formulas without using machine learning models.

Evidence 2: Dynamic metric evaluation function
- File: `ranx/meta/evaluate.py`
- Function: `evaluate()` and `metric_switch()`
- Code Reference:
```python
def evaluate(qrels, run, metrics, ...):
    # Extract metric and params
    m, k, rel_lvl = extract_metric_and_params(metric)
    # Apply algorithmic metric
    metric_scores_dict[metric] = metric_switch(m)(_qrels, _run, k, rel_lvl)
```
The `evaluate()` function serves as the central evaluation mechanism that takes qrels (relevance judgments) and runs (system outputs), then applies metric functions based on string names. The `metric_switch()` function dynamically selects the appropriate algorithmic metric function. This architecture demonstrates rule-based, deterministic evaluation where performance scores are computed using predefined mathematical operations rather than learned models or human judgment.

Evidence 3: Statistical test implementations
- File: `ranx/statistical_tests/` directory
- Functions: `fisher_randomization_test.py`, `paired_student_t_test.py`, `tukey_hsd_test.py`
- Code Reference:
```python
# Fisher's Randomization Test using permutations
# Paired Student's t-Test using scipy
# Tukey's HSD test using scipy
```
The statistical tests directory contains implementations of algorithmic statistical functions used for comparing runs: Fisher's Randomization Test (using permutations), paired Student's t-Test (using scipy), and Tukey's HSD test (using scipy). These are established statistical algorithms that provide deterministic, reproducible analysis of evaluation results without requiring machine learning models, external environment interaction, or human annotation.

Evidence 4: Comprehensive metric documentation with mathematical definitions
- File: `docs/metrics.md`
- Code Reference:
```
Algorithmic metrics: Hits, Hit Rate, Precision, Recall, F1, R-Precision, 
Bpref, RBP, MRR, MAP, DCG, NDCG
Each metric has mathematical formula definitions (e.g., Precision = r/n)
```
The documentation provides a comprehensive list of algorithmic metrics with their mathematical formula definitions. For example, Precision is defined as r/n (relevant items divided by total items). This documentation confirms that all metrics follow established IR evaluation formulas and are purely computational, ensuring consistent and reproducible evaluation through predefined mathematical operations rather than learned representations or subjective judgment.