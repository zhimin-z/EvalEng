# Quantus - Stage 7 (VALIDATE) Evaluation

## Summary
Quantus is an XAI (Explainable AI) evaluation toolkit that focuses on assessing explanation quality for neural networks. It does not implement pre-deployment quality gates, compliance validation, or ensemble decision-making systems. The framework is designed purely for post-hoc evaluation of explanations, not for deployment validation or go/no-go decisions.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S7F1: Quality Gates | 0 | No quality gate features exist. The framework provides metrics that output scores (e.g., faithfulness, robustness) but has no built-in threshold checking, pass/fail logic, or deployment decision capabilities. From `quantus/metrics/base.py`, metrics only compute and return evaluation scores without any decision logic. |
| S7F2: Compliance Validation | 0 | No compliance features exist. The framework does not test for fairness, generate model cards, validate privacy compliance, or produce certification reports. It only evaluates explanation quality using metrics like MPRT and Complexity, as seen in the tutorials. |
| S7F3: Ensemble Decisions | 0 | No ensemble orchestration or multi-model comparison features. While `quantus.evaluate()` in `quantus/evaluation.py` can compare multiple explanation methods on a single model, it cannot evaluate multiple models simultaneously, provide voting mechanisms, or make deployment recommendations between model candidates. |

---

## Detailed Analysis

### S7F1: Quality Gate Application (Rating: 0)

Evidence of Missing Features:

1. No Threshold Configuration: The base metric class in `quantus/metrics/base.py` shows metrics only compute scores:
```python
def __call__(
    self,
    model: Union[keras.Model, nn.Module, None],
    x_batch: np.ndarray,
    y_batch: np.ndarray,
    a_batch: Optional[np.ndarray],
    ...
) -> R:
    """
    ...
    Returns
    -------
    evaluation_scores: list
        a list of Any with the evaluation scores of the concerned batch.
    """
```

2. No Decision Logic: Searching through the codebase reveals no pass/fail logic, threshold comparisons, or go/no-go recommendations. The framework only aggregates scores:
```python
if self.return_aggregate:
    if self.aggregate_func:
        try:
            self.evaluation_scores = [
                self.aggregate_func(self.evaluation_scores)
            ]
```

3. Tutorial Example (`tutorials/Tutorial_Getting_Started.ipynb`) shows only score computation:
```python
scores_intgrad = quantus.ModelParameterRandomisation(
    similarity_func=quantus.similarity_func.correlation_spearman,
    return_sample_correlation=True,
    return_aggregate=True,
    aggregate_func=np.mean,
    ...
)(...)
print(f"ModelParameterRandomisation scores = ", scores_intgrad)
```

Missing Capabilities:
- No configurable thresholds (e.g., accuracy > 0.9)
- No composite conditions (AND/OR logic)
- No safety checks or red-team requirements
- No regression detection against baselines
- No go/no-go recommendations

---

### S7F2: Regulatory Compliance Validation (Rating: 0)

Evidence of Missing Features:

1. No Fairness Testing: The framework focuses on explanation quality, not model fairness. From `README.md`:
```
Quantus implements methods for the quantitative evaluation of XAI methods.
```

The metric categories listed are:
- Faithfulness
- Robustness  
- Localisation
- Complexity
- Randomisation
- Axiomatic

None relate to demographic parity, equalized odds, or fairness metrics.

2. No Model Card Generation: No functionality for generating model cards or documentation. The framework only evaluates explanations.

3. No Privacy Validation: No GDPR, CCPA, or data minimization checks. The framework operates on provided data without privacy compliance features.

4. Guidelines Document (`docs/source/guidelines/guidelines_and_disclaimers.md`) discusses evaluation methodology but has no compliance features:
```markdown
## User guidelines

Just 'throwing' some metrics at your explanations and considering the job done 
is not a very productive approach.
```

Missing Capabilities:
- No fairness testing (demographic parity, equalized odds, calibration)
- No explainability compliance (model cards, SHAP/LIME integration for compliance)
- No privacy validation (GDPR, CCPA)
- No certification reports (EU AI Act, NIST AI RMF)

---

### S7F3: Model Ensemble Decision-Making (Rating: 0)

Evidence of Missing Features:

1. Multi-XAI Method Comparison Only: From `quantus/evaluation.py`, the `evaluate()` function compares explanation methods, not models:
```python
def evaluate(
    metrics: Dict[str, Metric],
    xai_methods: Union[Dict[str, np.ndarray], Dict[str, Callable], Dict[str, dict]],
    ...
) -> Dict[str, Dict[str, List[float]]]:
    """
    ...
    xai_methods: dict[str, Any]
        A dictionary with a string key for the method and a np.ndarray,
        a callable or dictionary as value for the explanation method.
    """
```

2. Example Usage (`tutorials/Tutorial_Getting_Started.ipynb`) shows evaluation of different explanation methods on a single model:
```python
results = quantus.evaluate(
    metrics={
        "max-sensitivity-10": quantus.MaxSensitivity(nr_samples=10),
        "max-sensitivity-20": quantus.MaxSensitivity(nr_samples=20),
    },
    xai_methods={
        "Saliency": a_batch_saliency,
        "IntegratedGradients": a_batch_intgrad
    },
    model=model,  # Single model
    ...
)
```

3. No Ensemble Orchestration: The codebase has no functionality for:
   - Parallel model evaluation
   - Voting mechanisms between models
   - Cascade strategies (cheaper model first)
   - Mixture-of-experts routing

Missing Capabilities:
- No multi-model orchestration
- No voting mechanisms (majority, weighted, ranked)
- No cascade strategies (confidence-based routing)
- No mixture-of-experts support
- No deployment recommendations between model candidates

---

## Conclusion

Quantus is a specialized XAI evaluation toolkit that provides no Stage 7 (VALIDATE) functionality. It is designed to evaluate the quality of explanations after they are generated, not to apply pre-deployment quality gates, validate compliance, or make ensemble deployment decisions. The framework would require substantial new development to support any Stage 7 features, as the current architecture is fundamentally oriented toward explanation quality assessment rather than deployment validation.