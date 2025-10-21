# Quantus - Stage 4 (EVALUATE) Evaluation

## Summary
Quantus is a comprehensive XAI (Explainable AI) evaluation toolkit focused on evaluating neural network explanations. It provides 35+ metrics across 6 categories but is specifically designed for evaluating explanation methods rather than LLM outputs. The framework's evaluation capabilities are sophisticated for attribution-based explanations (saliency maps, feature importance) but fundamentally misaligned with Stage 4's focus on LLM output validation, task-specific metrics, and multi-modal scoring.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation for LLM outputs. Framework validates attribution shapes (quantus/helpers/asserts.py) and model predictions, but lacks JSON/XML parsing, schema validation, policy compliance checks, or text normalization capabilities. |
| S4F2: Metric Computation | 1 | 35+ metrics exist (quantus/metrics/) but for XAI evaluation (faithfulness, robustness, localisation), not LLM task metrics. No BLEU, ROUGE, accuracy, precision/recall for classification, or retrieval metrics. Per-sample scoring exists (base.py:evaluate_batch) but for wrong domain. |
| S4F3: Evaluator Models | 0 | No LLM-as-judge, no evaluator model integration. Framework expects pre-computed explanations or uses XAI methods (Integrated Gradients, Saliency) via quantus/functions/explanation_func.py. No judge prompts, rationale capture, or ensemble scoring. |
| S4F4: Multi-Modal Scoring | 0 | Handles image, tabular, time-series data as inputs (tutorials show MNIST images, Titanic tabular data) but evaluates explanations of those inputs, not multi-modal outputs. No CLIP score, image captioning metrics, WER, or cross-modal evaluation. |
| S4F5: Aggregate Statistics | 2 | Basic aggregation exists: mean/median via aggregate_func (base.py:236-237), custom aggregation functions supported. No built-in confidence intervals, significance testing, Elo ratings, or stratified statistics. Evaluation stores per-sample scores (evaluation_scores) but limited statistical analysis tools. |

---

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 0)

Evidence of absence:

1. No text output validation - Search through codebase shows no JSON/XML parsers:
```python
# quantus/helpers/asserts.py focuses on ML model validation
def assert_attributions(x_batch: np.ndarray, a_batch: np.ndarray):
    """Validates that attributions match input shape."""
    # Shape validation only, no text/format validation
```

2. No policy compliance - No toxicity detection, content filtering, or safety checks in any files.

3. No text normalization - The normalise_func in base.py normalizes numerical attributions:
```python
# quantus/functions/normalise_func.py
def normalise_by_max(a: np.ndarray) -> np.ndarray:
    """Normalise attributions by their maximum absolute value."""
    return np.divide(a, np.max(np.abs(a)))
```
This is for saliency maps, not text output normalization.

Conclusion: Framework designed for XAI explanation evaluation, not LLM output validation. Zero relevant functionality.

---

### S4F2: Task-Specific Metric Computation (Rating: 1)

What exists (but wrong domain):

1. 35+ XAI metrics organized in 6 categories:
```python
# quantus/metrics/__init__.py
from quantus.metrics.faithfulness import *  # 12 metrics
from quantus.metrics.robustness import *    # 8 metrics
from quantus.metrics.localisation import *  # 7 metrics
from quantus.metrics.complexity import *    # 3 metrics
from quantus.metrics.randomisation import * # 4 metrics
from quantus.metrics.axiomatic import *     # 3 metrics
```

2. Per-sample scoring exists:
```python
# quantus/metrics/base.py:356
def evaluate_batch(self, model, x_batch, y_batch, a_batch, s_batch, kwargs):
    """Evaluates model and attributes on a single data batch."""
    # Returns batched evaluation results
```

What's missing (for LLM evaluation):
- No BLEU, ROUGE, METEOR (text generation)
- No accuracy, precision, recall, F1 (classification) for text outputs
- No P@k, NDCG, MRR (retrieval)
- No perplexity, toxicity scores

Example of existing metric (wrong purpose):
```python
# quantus/metrics/complexity/sparseness.py
class Sparseness(Metric):
    """Measures if only highly attributed features are predictive (for explanations)."""
    # Uses Gini Index on attribution values, not text complexity
```

Extensibility exists but requires domain shift:
```python
# quantus/evaluation.py:16
def evaluate(metrics, xai_methods, model, x_batch, y_batch, kwargs):
    """High-level evaluation function."""
    # Could theoretically be extended but fundamentally expects explanations not text
```

Conclusion: Strong metric infrastructure but completely wrong domain. Giving 1 point for per-sample scoring capability that could theoretically be adapted.

---

### S4F3: Evaluator Model Integration (Rating: 0)

No LLM-as-judge anywhere:

1. Explanation functions are for XAI methods:
```python
# quantus/functions/explanation_func.py:153
def explain(model, inputs, targets, method: str, kwargs):
    """Generate explanations using Captum, Zennit, or tf-explain."""
    if method == "IntegratedGradients":
        return captum_instance.attribute(inputs, target=targets)
```

2. No judge prompt templates - Searched docs/ and quantus/ for "judge", "prompt", "evaluator" - only found model prediction code.

3. No rationale capture - Metrics return numerical scores:
```python
# quantus/metrics/faithfulness/pixel_flipping.py:94
def evaluate_instance(self, model, x, y, a, s):
    """Returns float score for pixel flipping metric."""
    return float(correlation_score)
```

Conclusion: Zero evaluator model support. Framework evaluates explanations, not generates or uses LLM judges.

---

### S4F4: Multi-Modal Scoring Protocols (Rating: 0)

Handles multi-modal inputs, not outputs:

1. Image inputs evaluated:
```python
# tutorials/Tutorial_Getting_Started.ipynb
# Load MNIST images
test_set = torchvision.datasets.MNIST(root='./sample_data')
# Evaluate explanations of image classifications
metric(model=model, x_batch=x_batch, y_batch=y_batch, a_batch=a_batch_saliency)
```

2. Tabular inputs evaluated:
```python
# tutorials/Tutorial_Getting_Started_with_Tabular_Data.ipynb
# Load Titanic dataset
df = pd.read_csv("assets/titanic3.csv")
# Evaluate explanations of tabular predictions
metric(model=net, x_batch=test_features, a_batch=attr)
```

3. Time-series inputs evaluated:
```python
# tutorials/Tutorial_Getting_Started_with_Time_Series_Data.ipynb
# Load MNIST1D time series
mnist1d_data = pickle.load(urllib.request.urlopen(mnist_url))
# Evaluate explanations
```

No output modality scoring:
- No image captioning metrics (CIDEr, SPICE)
- No VQA accuracy
- No CLIP score for text-to-image alignment
- No WER for speech

Conclusion: Multi-modal data handling exists for inputs to be explained, not for evaluating multi-modal outputs.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 2)

What exists:

1. Basic aggregation:
```python
# quantus/metrics/base.py:236-242
if self.return_aggregate:
    if self.aggregate_func:
        try:
            self.evaluation_scores = [self.aggregate_func(self.evaluation_scores)]
        except Exception:
            log.error("The aggregation of evaluation scores failed")
```

2. Flexible aggregation function:
```python
# README.md:369
results = quantus.evaluate(
    metrics=metrics,
    xai_methods=xai_methods,
    agg_func=np.mean,  # User can pass any callable
)
```

3. Per-sample storage:
```python
# quantus/metrics/base.py:141
self.evaluation_scores = []  # Stores batch results
self.all_evaluation_scores = []  # Stores all results across calls
```

4. Batch-level processing with progress tracking:
```python
# quantus/metrics/base.py:630
for d_ix, data_batch in enumerate(batch_generator):
    result = self.evaluate_batch(data_batch)
    self.evaluation_scores.extend(result)
```

What's missing:
- No percentiles (P25, P75, P95, P99)
- No confidence intervals
- No significance testing (t-test, Wilcoxon)
- No effect size computation
- No ranking systems (Elo, TrueSkill)
- No stratified statistics
- No built-in model comparison tools

Evidence from tutorials:
```python
# tutorials/Tutorial_Metric_Parameterisation_Analysis.ipynb
# Shows manual comparison across metrics but no statistical tests
scores_dict = {
    "Faithfulness Correlation": [],
    "Monotonicity": [],
}
# User must implement own significance tests
```

Conclusion: Basic aggregation works (mean/median/custom), per-sample scores accessible, but no advanced statistical analysis. Rating 2 for working basics with notable gaps.

---

## Overall Assessment

Total Stage 4 Score: 3/15 (20%)

Quantus is a well-engineered framework with strong capabilities in its intended domain (XAI evaluation), but fundamentally misaligned with Stage 4's LLM evaluation requirements:

Strengths:
- Robust metric computation infrastructure (wrong domain)
- Per-sample and aggregate scoring works reliably
- Good extensibility architecture
- Handles multiple input modalities for explanation evaluation

Critical Gaps:
- Zero LLM output validation (JSON, schema, policy)
- No text generation metrics (BLEU, ROUGE)
- No classification metrics for text (accuracy, F1)
- No LLM-as-judge or evaluator models
- No multi-modal output evaluation (only input evaluation)
- Limited statistical analysis tools

Verdict: This is an XAI evaluation toolkit, not an LLM evaluation framework. It would require a complete architectural overhaul to support Stage 4 capabilities. The repository name includes "machine-intelligence" but focuses exclusively on explaining predictions, not evaluating generative outputs.