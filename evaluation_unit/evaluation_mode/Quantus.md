## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Main evaluation orchestrator
- File: `quantus/evaluation.py`
- Function: `evaluate()`
- Code Reference:
```python
def evaluate(
    metrics: Dict,
    xai_methods: Union[Dict[str, Callable], Dict[str, Dict], Dict[str, np.ndarray]],
    model: ModelInterface,
    x_batch: np.ndarray,
    y_batch: np.ndarray,
    s_batch: Union[np.ndarray, None] = None,
    ...
) -> Optional[dict]:
```
This function evaluates explanation methods (XAI methods like Gradient, Saliency, IntegratedGradients) by generating attributions/explanations from model outputs and comparing these attributions using various metrics without executing the attributions themselves. The metrics analyze properties like faithfulness, robustness, complexity, and localization of the explanations through structural analysis, similarity comparison, and property checking.

Evidence 2: Similarity and comparison functions
- File: `quantus/functions/similarity_func.py`
- Code Reference:
```python
def correlation_spearman(a: np.ndarray, b: np.ndarray) -> float
def correlation_pearson(a: np.ndarray, b: np.ndarray) -> float
def correlation_kendall_tau(a: np.ndarray, b: np.ndarray) -> float
def distance_euclidean(a: np.ndarray, b: np.ndarray) -> float
def distance_manhattan(a: np.ndarray, b: np.ndarray) -> float
def cosine(a: np.ndarray, b: np.ndarray) -> float
def ssim(a: np.ndarray, b: np.ndarray) -> float
```
These functions perform static analysis by computing correlation metrics between attribution arrays, calculating distance metrics between explanations, computing structural similarity between outputs, with all operations being inspection-based without executing any model-generated code.

Evidence 3: Normalization functions for output analysis
- File: `quantus/functions/normalise_func.py`
- Code Reference:
```python
def normalise_by_max(a: np.ndarray, normalise_axes: Optional[Sequence[int]] = None) -> np.ndarray
def normalise_by_negative(a: np.ndarray, normalise_axes: Optional[Sequence[int]] = None) -> np.ndarray
def normalise_by_average_second_moment_estimate(a: np.ndarray, normalise_axes: Optional[Sequence[int]] = None) -> np.ndarray
```
These functions perform syntactic transformations and structural analysis on attribution outputs for comparison and evaluation purposes.

Evidence 4: Evaluation test suite patterns
- File: `tests/test_evaluation.py`
- Function: `test_evaluate_func()`
- Code Reference:
```python
def test_evaluate_func(model, data: np.ndarray, params: dict, expected: Union[float, dict, bool]):
    x_batch, y_batch = data["x_batch"], data["y_batch"]
    
    # Generate explanations
    a_batch = explain(model=model, inputs=x_batch, targets=y_batch, **explain_func_kwargs)
    
    # Evaluate using metrics (static analysis)
    results = evaluate(
        metrics=eval(params["eval_metrics"]),
        xai_methods=eval(params["eval_xai_methods"]),
        model=model,
        x_batch=x_batch,
        y_batch=y_batch,
        agg_func=np.mean,
        ...
    )
```
The tests confirm that evaluation involves generating attributions/explanations from models, analyzing these attributions through various metrics (Sparseness, MaxSensitivity, Complexity), comparing attribution properties without executing the attributions as code, and validating output shapes, value ranges, and structural properties.

Evidence 5: Complexity measurement functions
- File: `quantus/functions/complexity_func.py`
- Code Reference:
```python
def entropy(a: np.ndarray, x: np.ndarray) -> float
def gini_coeffiient(a: np.ndarray, x: np.ndarray) -> float
def discrete_entropy(a: np.ndarray, x: np.ndarray, n_bins: int) -> float
```
These functions perform static analysis by computing complexity measures on attribution arrays without executing any generated artifacts.

Evidence 6: Metric categories for property analysis
- File: `docs/source/docs_api/`
- Code Reference:
```
quantus.metrics.faithfulness.*
quantus.metrics.robustness.*
quantus.metrics.complexity.*
quantus.metrics.localisation.*
quantus.metrics.axiomatic.*
```
All these metric categories analyze properties of model-generated explanations through inspection and comparison. They evaluate faithfulness of explanations, check robustness properties of attributions, measure complexity of explanations, evaluate localization properties, and validate axiomatic properties, which is characteristic of static analysis evaluation.