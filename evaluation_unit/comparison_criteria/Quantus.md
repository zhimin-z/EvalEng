## Comparison Criteria Categories

[None]

## Detailed Analysis

### None

Evidence 1: Intrinsic Attribution Quality Metrics
- File: `quantus/metrics/complexity/sparseness.py`, `quantus/metrics/complexity/complexity.py`, `quantus/metrics/complexity/effective_complexity.py`
- Code Reference: Complexity metric implementations
These metrics evaluate intrinsic properties of explanations (attributions) without external references. Metrics like `Sparseness` and `Complexity` measure properties of the explanation itself, such as how sparse an attribution map is, rather than comparing against ground truth labels or baseline outputs.

Evidence 2: Robustness Metrics
- File: `quantus/metrics/robustness/max_sensitivity.py`, `quantus/metrics/robustness/avg_sensitivity.py`, `quantus/metrics/robustness/continuity.py`, `quantus/metrics/robustness/consistency.py`, `quantus/metrics/robustness/local_lipschitz_estimate.py`
- Code Reference: Sensitivity evaluation
```python
"eval_metrics": "{'max-Sensitivity': MaxSensitivity(**{'disable_warnings': True,})}"
```
Metrics like `MaxSensitivity` evaluate explanation robustness by measuring how explanations change under perturbations without requiring external reference answers. These assess intrinsic stability properties of attribution maps.

Evidence 3: Faithfulness Through Perturbation
- File: `quantus/metrics/faithfulness/pixel_flipping.py`, `quantus/metrics/faithfulness/monotonicity.py`, `quantus/metrics/faithfulness/selectivity.py`, `quantus/metrics/faithfulness/sensitivity_n.py`
- Code Reference: Perturbation-based evaluation
These metrics evaluate explanation quality by measuring how model predictions change when inputs are perturbed according to attributions. No external ground truth explanations are needed—evaluation is based on analyzing the relationship between attribution importance and prediction changes.

Evidence 4: Reference-Free Evaluation Function
- File: `quantus/evaluation.py`
- Code Reference: `evaluate()` function (Lines 40-242)
```python
evaluate(
    metrics: Dict,
    xai_methods: Union[Dict[str, Callable], Dict[str, Dict], Dict[str, np.ndarray]],
    model: ModelInterface,
    x_batch: np.ndarray,
    y_batch: np.ndarray,
    ...
)
```
The evaluation function evaluates explanation methods against metrics without requiring external reference attributions. While `y_batch` is provided, these are model predictions used for generating explanations, not comparison criteria for evaluation. Metrics assess explanations using intrinsic quality measures.

Evidence 5: Self-Contained Metric Computation
- File: `tests/test_evaluation.py`
- Code Reference: Metric instantiation (Lines 17-207)
```python
"eval_metrics": "{'Sparseness': Sparseness(**{'disable_warnings': True,'normalise': True,})}"
```
Test cases demonstrate that metrics like `Sparseness`, `Complexity`, and `MaxSensitivity` are computed without loading any external reference data. Metrics are instantiated and computed purely from the model, input, and generated explanation, with no external comparison targets.

Evidence 6: Axiomatic Property Evaluation
- File: `quantus/metrics/axiomatic/completeness.py`, `quantus/metrics/axiomatic/input_invariance.py`, `quantus/metrics/axiomatic/non_sensitivity.py`
- Code Reference: Axiomatic metric implementations
These metrics evaluate whether explanations satisfy certain axiomatic properties (theoretical requirements for good explanations) without comparing to reference explanations. They assess intrinsic qualities like completeness and invariance properties through self-contained evaluation.

Evidence 7: Localisation Property Assessment
- File: `quantus/metrics/localisation/pointing_game.py`, `quantus/metrics/localisation/attribution_localisation.py`, `quantus/metrics/localisation/auc.py`
- Code Reference: Localisation metric implementations
While these metrics evaluate where explanations focus, they do so by analyzing the attribution maps' internal properties and their relationship to model behavior, not by comparing to ground truth explanation labels. Assessment is based on intrinsic localization characteristics.

Evidence 8: No Reference Data Loading
- File: `tests/conftest.py` and test files
- Code Reference: Test fixtures
Throughout the test fixtures, data loading occurs for inputs (`load_mnist_images`, `load_cifar10_images`) and models (`load_mnist_model`), but no loading of reference explanations, ground truth attribution maps, or baseline comparison outputs. The only data loaded are inputs (x_batch) and labels (y_batch), which are used for generating explanations, not as evaluation criteria. All metrics assess properties of the explanations themselves without external references.