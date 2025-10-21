# Quantus - Stage 8 (MONITOR) Evaluation

## Summary
Quantus is an XAI evaluation metrics library focused on offline evaluation of explanation methods. It has no production drift monitoring, online evaluation, feedback loop integration, or automated improvement recommendation capabilities. The framework is designed for research and development contexts where explanations are evaluated in batch mode against pre-defined metrics, not for production deployment scenarios.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring features exist. The library is purely for offline evaluation of XAI methods. |
| S8F2: Online Evaluation | 0 | No online/streaming evaluation capabilities. All evaluation is batch-based with no A/B testing or shadow deployment support. |
| S8F3: Feedback Integration | 0 | No feedback loop integration. The library operates independently without production data ingestion capabilities. |
| S8F4: Improvement Planning | 0 | No automated improvement recommendations. The library provides evaluation scores but no root cause analysis or optimization suggestions. |

### Detailed Analysis

#### S8F1: Production Drift Monitoring (0/3 points)

Evidence:

1. Core Design: The framework is explicitly designed for offline evaluation:
```python
# From quantus/metrics/base.py lines 210-221
def __call__(
    self,
    model: Union[keras.Model, nn.Module, None],
    x_batch: np.ndarray,
    y_batch: np.ndarray,
    a_batch: Optional[np.ndarray],
    ...
) -> R:
    """
    This implementation represents the main logic of the metric and makes the class object callable.
    It completes batch-wise evaluation of explanations (a_batch) with respect to input data (x_batch),
    output labels (y_batch) and a torch or tensorflow model (model).
    """
```

2. Batch-Based Processing: All metrics process data in batches:
```python
# From quantus/metrics/base.py lines 285-292
batch_generator = self.generate_batches(
    data=data,
    batch_size=batch_size,
)

self.evaluation_scores = []
for d_ix, data_batch in enumerate(batch_generator):
    data_batch = self.batch_preprocess(data_batch)
    result = self.evaluate_batch(data_batch)
```

3. No Streaming or Time-Series Support: The library focuses on static evaluation without temporal tracking of distribution shifts or performance degradation.

4. Documentation Confirms Offline Focus: 
```markdown
# From docs/source/getting_started/getting_started_example.md
This notebook shows how to get started with Quantus using tabular data...
Quantus implements methods for the quantitative evaluation of XAI methods.
Generally, in order to apply these, you will need:
* A model (`model`), inputs (`x_batch`) and labels (`y_batch`)
* Some explanations you want to evaluate (`a_batch`)
```

Justification: Quantus is entirely focused on offline evaluation with no infrastructure for:
- Distribution shift detection (no statistical tests for drift)
- Performance degradation tracking over time
- Behavioral monitoring in production
- Alerting capabilities
- Production integration

#### S8F2: Online and Streaming Evaluation (0/3 points)

Evidence:

1. Batch-Only Architecture: The evaluation is strictly batch-based:
```python
# From quantus/evaluation.py (referenced in __init__.py)
from quantus.evaluation import evaluate

# From tutorials/Tutorial_Getting_Started.ipynb
results = quantus.evaluate(
    metrics=metrics,
    xai_methods=xai_methods,
    agg_func=np.mean,
    model=model,
    x_batch=x_batch,
    y_batch=y_batch,
    call_kwargs={"0": {"softmax": False,},}
)
```

2. No Real-Time Processing: All metrics inherit from base `Metric` class with batch processing:
```python
# From quantus/metrics/base.py lines 456-480
@final
def generate_batches(
    self,
    data: D,
    batch_size: int,
) -> Generator[D, None, None]:
    """
    Creates iterator to iterate over all batched instances in data dictionary.
    """
```

3. No A/B Testing Framework: The library provides no infrastructure for:
- Traffic splitting
- Multi-variant testing
- Gradual rollouts
- Automated rollback

4. Evaluation Returns Static Scores:
```python
# From quantus/metrics/base.py lines 320-323
if self.return_aggregate:
    if self.aggregate_func:
        try:
            self.evaluation_scores = [
                self.aggregate_func(self.evaluation_scores)
            ]
```

Justification: Quantus is designed for research and development contexts where:
- Explanations are evaluated offline against pre-collected datasets
- No streaming data support exists
- No A/B testing or shadow deployment capabilities
- All evaluation is retrospective, not real-time

#### S8F3: Feedback Loop Integration (0/3 points)

Evidence:

1. No Data Ingestion: The library has no capabilities for:
- Production log parsing
- User feedback collection
- Operational metric ingestion

2. Standalone Evaluation: From the documentation:
```markdown
# From docs/source/getting_started/getting_started_example.md
Quantus implements XAI evaluation metrics from different categories...
To apply a metric to your setting...it first needs to be instantiated:

metric = quantus.MaxSensitivity()

and then applied to your model, data, and (pre-computed) explanations
```

3. No Production Integration: The tutorials show purely offline workflows:
```python
# From tutorials/Tutorial_Getting_Started_with_Tabular_Data.ipynb
# Load datasets
df = pd.read_csv("assets/titanic3.csv")
...
# Generate explanations
ig = IntegratedGradients(net)
...
# Evaluate
scores_intgrad = quantus.ModelParameterRandomisation(...)
```

4. No Closed-Loop Automation: The library provides scores but no automation for:
- Re-evaluation triggers
- Feedback accumulation
- Integration with retraining pipelines

Justification: Quantus is a metrics library without:
- Production data collection capabilities
- Failure mining from production logs
- Automatic incorporation into evaluation datasets
- Any feedback loop infrastructure

#### S8F4: Iteration Planning and Improvement Recommendations (0/3 points)

Evidence:

1. Metrics Return Only Scores: From the base class:
```python
# From quantus/metrics/base.py lines 318-332
self.evaluation_scores = []
for d_ix, data_batch in enumerate(batch_generator):
    data_batch = self.batch_preprocess(data_batch)
    result = self.evaluate_batch(data_batch)
    self.evaluation_scores.extend(result)

# Call post-processing.
self.custom_postprocess(data)

if self.return_aggregate:
    if self.aggregate_func:
        try:
            self.evaluation_scores = [
                self.aggregate_func(self.evaluation_scores)
            ]
```

2. No Root Cause Analysis: Metrics provide quantitative scores without diagnostic information:
```python
# From quantus/metrics/faithfulness/pixel_flipping.py (example metric)
def evaluate_batch(...) -> np.ndarray:
    """Returns evaluation scores for a batch."""
    # Returns numeric scores only, no analysis
```

3. Manual Interpretation Required: The library offers interpretation text but no automated recommendations:
```python
# From quantus/metrics/base.py lines 631-633
def interpret_scores(self):
    """Get an interpretation of the scores."""
    print(self.__init__.__doc__.split(".")[1].split("References")[0])
```

4. No Optimization Suggestions: The README shows metrics evaluate methods but don't suggest improvements:
```markdown
# From README.md
With Quantus, we can obtain richer insights on how the methods compare e.g., 
b) by holistic quantification on several evaluation criteria and 
c) by providing sensitivity analysis of how a single parameter e.g. 
the pixel replacement strategy of a faithfulness test influences the ranking of the XAI methods.
```

5. No Roadmap Generation: Tutorials show manual analysis:
```python
# From tutorials/Tutorial_Metric_Parameterisation_Analysis.ipynb
# Manual comparison of metrics with different hyperparameters
# No automated recommendations generated
```

Justification: Quantus provides:
- Raw evaluation scores across multiple metrics
- Basic plotting for visualization
- Manual interpretation guidance

But lacks:
- Automated root cause analysis
- Hyperparameter optimization recommendations
- Prompt/explanation improvement suggestions
- Dataset gap analysis
- Structured experiment planning
- Impact vs. effort estimates

---

## Overall Stage 8 Assessment

Total Score: 0/12 points

Quantus is fundamentally not designed for production monitoring or continuous improvement. It is an offline evaluation toolkit for research and development of XAI methods. The framework:

- Strengths: Comprehensive offline evaluation metrics (35+ metrics across 6 categories), excellent documentation for research use, supports multiple frameworks (PyTorch, TensorFlow)

- Scope Limitations: Entirely focused on offline evaluation without any:
  - Production deployment considerations
  - Real-time monitoring capabilities
  - Feedback loop integration
  - Automated improvement recommendations

- Use Case: Quantus is designed for researchers and developers to evaluate explanation methods during development, not for monitoring explanations in production systems.

The framework would require substantial architectural changes to support Stage 8 (MONITOR) capabilities, as this is fundamentally outside its intended scope.