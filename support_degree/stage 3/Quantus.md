# Quantus - Stage 3 (EXECUTE) Evaluation

## Summary
Quantus is an XAI (Explainable AI) evaluation toolkit that operates in a batch-wise evaluation paradigm. The framework has minimal execution orchestration capabilities as it's designed for offline metric computation rather than production inference pipelines. It provides basic batch processing and progress tracking but lacks distributed execution, comprehensive telemetry, test-time optimization, and human evaluation features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 1 | Basic sequential batch processing only. No DAG support, task routing, or workflow management. Only simple iteration over batches. |
| S3F2: Inference & Telemetry | 0 | No performance telemetry. Only basic tqdm progress bars exist. No latency, throughput, resource usage, or cost tracking. |
| S3F3: Test-Time Optimization | 0 | No caching, batching optimization, or compute optimization features. Basic numpy operations only. |
| S3F4: Failure Handling | 1 | Minimal error handling with basic Python exceptions. No retry logic, circuit breakers, or intelligent recovery. |
| S3F5: Checkpointing | 0 | No checkpointing or resumption capabilities. Evaluations must complete in single run or restart from beginning. |
| S3F6: Distributed Execution | 0 | Single-process execution only. No multi-GPU, multi-node, or resource management features. |
| S3F7: Human Evaluation | 0 | No human evaluation features, crowdsourcing integration, or annotation interfaces. |

Total Score: 2/21 (9.5%)

---

## Detailed Analysis

### S3F1: Pipeline Orchestration (1/3)

Evidence of Basic Sequential Processing:

From `quantus/metrics/base.py`:
```python
def __call__(self, model, x_batch, y_batch, a_batch, ...):
    """Main evaluation logic."""
    data = self.general_preprocess(...)
    
    # Create generator for generating batches
    batch_generator = self.generate_batches(data=data, batch_size=batch_size)
    
    self.evaluation_scores = []
    for d_ix, data_batch in enumerate(batch_generator):
        data_batch = self.batch_preprocess(data_batch)
        result = self.evaluate_batch(data_batch)
        self.evaluation_scores.extend(result)
```

From `quantus/evaluation.py`:
```python
def evaluate(metrics, xai_methods, model, x_batch, y_batch, ...):
    """High-level evaluation function."""
    results = {}
    for xai_method_key, xai_method_value in xai_methods.items():
        results[xai_method_key] = {}
        for metric_key, metric_value in metrics.items():
            scores = metric_value(
                model=model,
                x_batch=x_batch,
                y_batch=y_batch,
                a_batch=xai_method_value if isinstance(...) else None,
                ...
            )
```

Limitations:
- No DAG support: Simple sequential iteration, no dependency management
- No task routing: All samples processed identically through same metric
- No conditional branching: Linear execution path only
- No protocol support: Fixed evaluation pattern per metric
- Manual orchestration through nested loops required for multiple metrics/methods

Rating: 1/3 - Single pipeline with basic batch iteration. Manual orchestration needed for multiple metrics. No workflow management.

---

### S3F2: Inference & Telemetry (0/3)

Evidence of Minimal Progress Tracking:

From `quantus/metrics/base.py`:
```python
def generate_batches(self, data, batch_size):
    """Creates iterator to iterate over all batched instances."""
    n_batches = np.ceil(n_instances / batch_size)
    
    with tqdm(total=n_batches, disable=not self.display_progressbar) as pbar:
        for batch_idx in gen_batches(n_instances, batch_size):
            # ... batch processing ...
            pbar.update(batch_idx.stop - batch_idx.start)
```

Complete Absence of Telemetry:
- No latency measurement (TTFT, per-token, end-to-end, percentiles)
- No throughput tracking (requests/sec, tokens/sec)
- No resource monitoring (memory, GPU utilization, API calls)
- No cost tracking or token consumption
- Only basic tqdm progress bar for batch iteration count

Rating: 0/3 - No telemetry beyond basic progress bars. No latency, throughput, resource, or cost tracking.

---

### S3F3: Test-Time Optimization (0/3)

Evidence of No Optimization Features:

From `quantus/metrics/base.py`:
```python
def explain_batch(self, model, x_batch, y_batch):
    """Compute explanations for batch."""
    a_batch = self.explain_func(
        model=model, 
        inputs=x_batch, 
        targets=y_batch, 
        self.explain_func_kwargs
    )
    # Direct computation, no caching
    return a_batch
```

Absence of Optimizations:
- No caching: Explanations recomputed every time, no prompt/response caching
- No batching optimization: Fixed batch sizes, no dynamic batching
- No model optimization: No quantization, compilation, or speculative decoding
- Basic numpy operations only, no GPU kernel optimization

From tutorials showing repeated computation:
```python
# Tutorial_Getting_Started.ipynb shows manual re-computation
for epoch in range(num_epochs):
    output = net(input_tensor)  # No caching of results
```

Rating: 0/3 - No caching, batching optimization, or test-time compute features.

---

### S3F4: Failure Handling (1/3)

Evidence of Basic Error Handling:

From `quantus/metrics/base.py`:
```python
def __call__(self, ...):
    if self.return_aggregate:
        if self.aggregate_func:
            try:
                self.evaluation_scores = [
                    self.aggregate_func(self.evaluation_scores)
                ]
            except Exception as ex:
                log.error(
                    f"The aggregation of evaluation scores failed with {ex}..."
                )
```

From `quantus/helpers/asserts.py` (implied from imports):
```python
# Basic assertions but no recovery mechanisms
asserts.assert_attributions(x_batch=x_batch, a_batch=a_batch)
asserts.assert_plot_func(plot_func=plot_func)
```

Limitations:
- No retry logic: Failures cause immediate exception propagation
- No exponential backoff: No retry strategies for transient failures
- No circuit breakers: No protection against cascading failures
- No timeout management: No configurable timeouts per operation
- No fallback strategies: Failures terminate entire evaluation
- Basic try-except blocks only for logging, no recovery

Rating: 1/3 - Minimal error handling with basic exceptions and logging. No retry logic, timeouts, circuit breakers, or intelligent recovery.

---

### S3F5: Checkpointing (0/3)

Evidence of No Checkpointing:

From `quantus/metrics/base.py`:
```python
def __call__(self, ...):
    """Evaluation must complete in single call."""
    self.evaluation_scores = []
    for d_ix, data_batch in enumerate(batch_generator):
        result = self.evaluate_batch(data_batch)
        self.evaluation_scores.extend(result)
    # No checkpoint saving
    return self.evaluation_scores
```

From `README.md`:
```markdown
## Getting started
# Shows one-shot evaluation with no resumption capability
scores = metric(
    model=model,
    x_batch=x_batch,
    y_batch=y_batch,
    device=device
)
```

Complete Absence:
- No checkpoint creation: No intermediate state saving
- No resumption: Cannot resume interrupted evaluations
- No incremental evaluation: Must reprocess all samples on failure
- No state persistence: RNG state, progress not saved
- Users must implement their own checkpointing externally

Rating: 0/3 - No checkpointing or resumption capabilities. Evaluations must complete or restart.

---

### S3F6: Distributed Execution (0/3)

Evidence of Single-Process Only:

From `quantus/metrics/base.py`:
```python
# Single-threaded batch processing
for d_ix, data_batch in enumerate(batch_generator):
    data_batch = self.batch_preprocess(data_batch)
    result = self.evaluate_batch(data_batch)
    self.evaluation_scores.extend(result)
```

From `README.md` and tutorials showing single device usage:
```python
# Tutorial_Getting_Started.ipynb
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Single GPU/CPU only
```

From `pyproject.toml` dependencies:
```toml
# No distributed computing dependencies
dependencies = [
    "numpy>=1.19.5",
    "pandas>=1.5.3",
    # No ray, dask, horovod, or distributed frameworks
]
```

Complete Absence:
- No multi-GPU support: Single device execution only
- No multi-node: No cluster support (Slurm, Kubernetes)
- No parallelization: Sequential batch processing
- No load balancing: No dynamic task distribution
- No budget enforcement: No cost, token, or time limits
- Users must implement external parallelization wrapper

Rating: 0/3 - Single-process, single-device execution only. No distributed capabilities.

---

### S3F7: Human Evaluation (0/3)

Evidence of No Human Evaluation Features:

From repository search:
- No files related to crowdsourcing (MTurk, Scale AI, Labelbox)
- No annotation interface code
- No quality control mechanisms
- No inter-rater agreement metrics

From `quantus/metrics/` directory structure:
```
metrics/
├── axiomatic/
├── complexity/
├── faithfulness/
├── localisation/
├── randomisation/
└── robustness/
# No human_evaluation/ directory
```

From `quantus/__init__.py`:
```python
# No human evaluation exports
from quantus.metrics import *
# Only automated metrics exposed
```

Complete Absence:
- No crowdsourcing integration: No platform connectors
- No annotation UI: No interface for human raters
- No quality control: No attention checks or gold standards
- No agreement metrics: No Cohen's kappa, Krippendorff's alpha
- Framework is purely automated metric computation

Rating: 0/3 - No human evaluation features, integrations, or quality control mechanisms.

---

## Key Strengths

1. Clean batch processing abstraction: Well-structured generator-based batching
2. Educational examples: Comprehensive tutorials showing evaluation workflows
3. Extensible metric framework: Clear base class for custom metrics

## Critical Weaknesses

1. No execution infrastructure: Designed for notebook-style offline evaluation
2. No production features: Missing all telemetry, optimization, and resilience features
3. No scalability: Single-process only, manual parallelization required
4. No checkpointing: Long evaluations at risk of total loss on failure
5. No observability: Cannot monitor performance or debug issues

## Recommendations

For users needing Stage 3 execution capabilities:
1. Implement external orchestration: Use Airflow/Prefect for workflow management
2. Add observability layer: Wrap metric calls with timing/resource tracking
3. Build checkpointing: Save intermediate results to disk manually
4. Use distributed frameworks: Wrap Quantus in Ray/Dask for parallelization
5. Consider alternative frameworks: For production evaluation pipelines, look at frameworks designed for inference monitoring

## Summary

Quantus scores 2/21 (9.5%) on Stage 3 execution criteria. It is fundamentally a research/development toolkit for offline XAI metric computation, not a production evaluation harness. The framework provides basic batch iteration and progress tracking but completely lacks:
- Performance monitoring and telemetry
- Test-time optimization
- Failure resilience and recovery
- Checkpoint/resume capabilities  
- Distributed execution
- Human evaluation orchestration

The design is appropriate for exploratory analysis and metric development but would require significant external infrastructure for production deployment or large-scale evaluation campaigns.