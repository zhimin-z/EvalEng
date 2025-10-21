# ranx - Stage 7 (VALIDATE) Evaluation

## Summary
ranx is a Python library for ranking evaluation and comparison in Information Retrieval systems. It focuses on metric computation, statistical testing, and run fusion/comparison but does not implement pre-deployment quality gates, compliance validation, or ensemble decision-making features as defined by Stage 7 criteria. The framework is designed for post-hoc evaluation rather than pre-deployment validation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S7F1: Quality Gates | 0 | No quality gate features exist. The library provides evaluation metrics but no threshold-based gates, safety checks, regression detection, or go/no-go recommendations. |
| S7F2: Compliance Validation | 0 | No compliance features found. No fairness testing, explainability tools, privacy validation, or certification support. |
| S7F3: Ensemble Decisions | 1 | Basic multi-model comparison exists through `compare()` but lacks voting mechanisms, cascade strategies, or deployment recommendations. |

## Detailed Analysis

### S7F1: Quality Gate Application (Rating: 0/3)

Evidence of Absence:

1. No Threshold Configuration: The `evaluate` function (docs/evaluate.md, ranx/meta/evaluate.py) only computes metrics without any threshold checking:
```python
# From docs/index.md
evaluate(qrels, run, "ndcg@5")
>>> 0.7861

evaluate(qrels, run, ["map@5", "mrr"])
>>> {"map@5": 0.6416, "mrr": 0.75}
```

2. No Safety Checks: No harmful content detection, safety thresholds, or red-team testing found in the codebase.

3. No Regression Testing: The `compare` function (ranx/meta/compare.py) performs statistical tests but doesn't detect regressions or recommend against deployment:
```python
# From docs/compare.md
report = compare(
    qrels=qrels,
    runs=[run_1, run_2, run_3, run_4, run_5],
    metrics=["map@100", "mrr@100", "ndcg@10"],
    max_p=0.01  # P-value threshold for statistical significance only
)
```

4. No Decision Output: The library produces reports showing metric comparisons but no go/no-go recommendations:
```python
# From docs/index.md - output shows comparison, not decisions
#    Model    MAP@100    MRR@100    NDCG@10
---  -------  --------   --------   ---------
a    model_1  0.320ᵇ     0.320ᵇ     0.368ᵇᶜ
b    model_2  0.233      0.234      0.239
```

Rating Justification: 0 points - No quality gate features exist. The framework is purely evaluative, not prescriptive.

### S7F2: Regulatory Compliance Validation (Rating: 0/3)

Evidence of Absence:

1. No Fairness Testing: The metrics (docs/metrics.md) include only retrieval metrics (NDCG, MAP, MRR, etc.) with no demographic parity, equalized odds, or calibration metrics:
```md
# From docs/metrics.md
* [Hits](...)
* [Hit Rate](...)
* [Precision](...)
* [Recall](...)
* [F1](...)
* [r-Precision](...)
* [Bpref](...)
* [Rank-biased Precision (RBP)](...)
* [Mean Reciprocal Rank (MRR)](...)
* [Mean Average Precision (MAP)](...)
* [DCG](...)
* [NDCG](...)
```

2. No Explainability: No model card generation, SHAP/LIME integration, or decision documentation:
```python
# From ranx/data_structures/run.py - only stores scores, no explanations
class Run:
    def __init__(self, run_dict: Dict[str, Dict[str, float]] = None, name: str = None):
        self.run = {}
        self.name = name
        self.scores = {}
        self.mean_scores = {}
```

3. No Privacy Validation: No GDPR, CCPA, or consent tracking features in the codebase.

4. No Certification Support: The library doesn't generate compliance reports for EU AI Act, NIST AI RMF, or ISO standards.

Rating Justification: 0 points - No compliance features exist. The framework focuses solely on retrieval effectiveness metrics.

### S7F3: Model Ensemble Decision-Making (Rating: 1/3)

Evidence of Limited Support:

1. Multi-Model Comparison: The `compare` function supports evaluating multiple models:
```python
# From notebooks/4_comparison_and_report.ipynb
report = compare(
    qrels,
    runs=[run_1, run_2, run_3, run_4, run_5],
    metrics=["map@100", "mrr@100", "ndcg@10"],
    max_p=0.01,  # P-value threshold
)
```

2. Statistical Comparison: Provides statistical tests (Fisher's, Student's t-test, Tukey HSD) but no voting or decision logic:
```python
# From ranx/statistical_tests/__init__.py
def compute_statistical_significance(
    model_names: List[str],
    metric_scores: Dict[str, Dict[str, np.ndarray]],
    stat_test: str = "fisher",  # or "student" or "tukey"
    n_permutations: int = 1000,
    max_p: float = 0.01,
    random_seed: int = 42,
):
```

3. Fusion Algorithms: Extensive fusion support (docs/fusion.md) for combining runs:
```python
# From docs/fusion.md - 26 fusion algorithms available
| CombMIN | CombMNZ | RRF | MAPFuse | BordaFuse |
| CombMED | CombGMNZ | RBC | PosFuse | Weighted BordaFuse |
| CombANZ | ISR | WMNZ | ProbFuse | Condorcet |
...
```

However, fusion is for combining retrieval results, not for ensemble decision-making about deployment.

Missing Features:

1. No Voting Mechanisms: Fusion algorithms combine scores but don't provide voting for deployment decisions:
```python
# From ranx/fusion/comb_sum.py - combines scores, not deployment votes
def comb_sum(runs: List[Run], name: str = "comb_sum") -> Run:
    run = Run()
    run.name = name
    run.run = _comb_sum_parallel(TypedList([run.run for run in runs]))
    run.sort()
    return run
```

2. No Cascade Strategies: No cost-based routing or confidence-based escalation.

3. No Deployment Recommendations: Reports show metric comparisons but don't recommend which model(s) to deploy:
```python
# From ranx/data_structures/report.py
class Report:
    def __str__(self):
        return tabulate(...)  # Just formats comparison table
```

Rating Justification: 1 point - Basic multi-model comparison exists but lacks ensemble decision logic, voting mechanisms, or deployment recommendations. The fusion functionality is for combining retrieval results, not for making deployment decisions.

## Key Evidence Summary

### Strengths:
1. Comprehensive Evaluation: 12+ metrics with statistical testing
2. Fusion Algorithms: 26 algorithms for combining retrieval results
3. Multi-Run Comparison: Can evaluate multiple models simultaneously

### Critical Gaps:
1. No Quality Gates: Missing threshold configuration, safety checks, and go/no-go logic
2. No Compliance Features: No fairness testing, explainability, or privacy validation
3. Evaluation-Only: Designed for post-hoc analysis, not pre-deployment validation

### Example of Evaluation-Only Design:
```python
# From notebooks/1_overview.ipynb
# Library computes metrics but provides no deployment guidance
score = evaluate(qrels, run, "ndcg@5")
print(score)  # Just prints 0.7861, no threshold check or recommendation

report = compare(qrels, runs, metrics, max_p=0.01)
print(report)  # Shows statistical differences, not deployment decisions
```

## Conclusion

ranx is a post-deployment evaluation framework, not a pre-deployment validation system. It excels at computing retrieval metrics and comparing models but provides no quality gates, compliance validation, or ensemble decision-making for deployment. The framework assumes humans will interpret evaluation results and make deployment decisions manually.