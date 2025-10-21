## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Multiple similarity and distance metrics
- File: `quantus/functions/similarity_func.py`
- Functions: `correlation_spearman()`, `correlation_pearson()`, `correlation_kendall_tau()`, `distance_euclidean()`, `distance_manhattan()`, `distance_chebyshev()`, `cosine()`, `ssim()`, `lipschitz_constant()`, `abs_difference()`, `squared_difference()`
- Code Reference:
```python
# Statistical correlation metrics
correlation_spearman()
correlation_pearson()
correlation_kendall_tau()

# Distance computation functions
distance_euclidean()
distance_manhattan()
distance_chebyshev()

# Similarity metrics
cosine()
ssim()  # Structural Similarity Index Measure
lipschitz_constant()

# Mathematical difference functions
abs_difference()
squared_difference()
```
This module provides a comprehensive suite of algorithmic similarity and distance metrics that serve as deterministic evaluators. The statistical correlation metrics (Spearman, Pearson, Kendall-Tau) compute reproducible correlation coefficients, while the distance functions (Euclidean, Manhattan, Chebyshev) calculate mathematical distances between data points. Additional metrics include cosine similarity for vector comparisons, SSIM for structural similarity assessment, and Lipschitz constants for function continuity evaluation. These are all predefined mathematical functions that provide consistent, rule-based assessment.

Evidence 2: Mean Squared Error calculation
- File: `quantus/functions/loss_func.py`
- Function: `mse()`
- Code Reference:
```python
mse()  # Mean Squared Error calculation
```
The MSE function implements a fundamental algorithmic metric for comparing model outputs through deterministic mathematical computation. This loss function provides reproducible quantitative assessment of prediction accuracy without requiring learned models or human judgment.

Evidence 3: Complexity measurement metrics
- File: `quantus/functions/complexity_func.py`
- Functions: `entropy()`, `discrete_entropy()`, `gini_coeffiient()`
- Code Reference:
```python
entropy()           # Entropy-based complexity measure
discrete_entropy()  # Discrete entropy calculation
gini_coeffiient()   # Gini coefficient calculation
```
These algorithmic functions compute complexity metrics using established mathematical formulas. Entropy measures quantify information-theoretic complexity, while the Gini coefficient assesses distribution inequality. All calculations are deterministic and based on predefined statistical principles.

Evidence 4: Mathematical norm calculations
- File: `quantus/functions/norm_func.py`
- Functions: `fro_norm()`, `linf_norm()`, `l2_norm()`
- Code Reference:
```python
fro_norm()   # Frobenius norm
linf_norm()  # L-infinity norm
l2_norm()    # L2 norm
```
This module implements standard mathematical norm functions that provide deterministic magnitude calculations. These norms are fundamental algorithmic evaluators used throughout the library for measuring vector and matrix magnitudes in a reproducible manner.

Evidence 5: Comprehensive metric categories
- File: `quantus/metrics/` directory
- Metric Categories: `faithfulness`, `robustness`, `localisation`, `complexity`, `axiomatic`, `randomisation`
- Code Reference:
```python
# Documented metric categories
quantus.metrics.faithfulness      # pixel_flipping, sufficiency, monotonicity, etc.
quantus.metrics.robustness        # max_sensitivity, avg_sensitivity, continuity, etc.
quantus.metrics.localisation      # pointing_game, relevance_rank_accuracy, auc, etc.
quantus.metrics.complexity        # sparseness, complexity, effective_complexity
quantus.metrics.axiomatic         # completeness, input_invariance, non_sensitivity
quantus.metrics.randomisation     # model_parameter_randomisation, random_logit
```
The metrics directory structure reveals an extensive taxonomy of domain-specific algorithmic evaluators for XAI (explainable AI) assessment. These categories encompass faithfulness metrics that measure explanation fidelity, robustness metrics for sensitivity analysis, localisation metrics for spatial accuracy, complexity metrics for explanation simplicity, axiomatic metrics for theoretical properties, and randomisation metrics for stability testing. Each metric within these categories implements deterministic computational functions for evaluating explanation quality.

Evidence 6: Similarity function test suite
- File: `tests/functions/test_similarity_func.py`
- Tested Functions: `correlation_spearman`, `correlation_pearson`, `correlation_kendall_tau`, `distance_euclidean`, `distance_manhattan`, `distance_chebyshev`, `cosine`, `ssim`, `mse`, `lipschitz_constant`
- Code Reference:
```python
# Test cases for algorithmic evaluators
tests for correlation_spearman
tests for correlation_pearson
tests for correlation_kendall_tau
tests for distance_euclidean
tests for distance_manhattan
tests for distance_chebyshev
tests for cosine
tests for ssim
tests for mse
tests for lipschitz_constant
```
The comprehensive test suite validates the deterministic nature of these algorithmic evaluators. Each test verifies that the functions produce exact mathematical outputs given specific inputs, confirming their reproducible and rule-based assessment capabilities. The tests ensure these metrics behave as predefined computational functions rather than learned or adaptive systems.

Evidence 7: Complexity metric validation
- File: `tests/functions/test_complexity_func.py`
- Tested Functions: `entropy()`, `gini_coeffiient()`, `discrete_entropy()`
- Code Reference:
```python
# Tests for complexity metrics
tests for entropy()
tests for gini_coeffiient()
tests for discrete_entropy()
```
These tests validate that complexity metrics produce float outputs within valid ranges and behave deterministically. The test suite confirms that entropy and Gini coefficient calculations follow established mathematical formulas and provide consistent results.

Evidence 8: Norm function validation
- File: `tests/functions/test_norm_func.py`
- Tested Functions: `fro_norm()`, `linf_norm()`, `l2_norm()`
- Code Reference:
```python
# Tests for norm functions
tests for fro_norm()
tests for linf_norm()
tests for l2_norm()
```
The norm function tests verify exact mathematical outputs, confirming these functions implement standard mathematical definitions. The deterministic nature of these tests demonstrates that the norms serve as algorithmic evaluators with reproducible assessment characteristics.