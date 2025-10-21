# ranx - Stage 3 (EXECUTE) Evaluation

## Summary
ranx is a Python library for ranking evaluation metrics optimized with Numba. It focuses on metric computation rather than full evaluation pipeline execution. The framework has minimal execution orchestration features, no built-in telemetry, test-time optimization, or distributed execution. It's designed for post-hoc evaluation of pre-computed retrieval results, not for managing the evaluation execution process itself.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No DAG, routing, or workflow orchestration features exist. The library only computes metrics on pre-existing qrels and runs. |
| S3F2: Inference & Telemetry | 0 | No inference capabilities or performance telemetry. The library evaluates pre-computed results only. |
| S3F3: Test-Time Optimization | 0 | No caching, batching, or optimization features for model inference (library doesn't perform inference). |
| S3F4: Failure Handling | 0 | No retry logic, timeouts, circuit breakers, or failure recovery mechanisms present. |
| S3F5: Checkpointing | 0 | No checkpointing or resumption capabilities. All operations are single-shot computations. |
| S3F6: Distributed Execution | 1 | Basic multi-threading via Numba parallelization, but no multi-GPU, multi-node, or budget enforcement. |
| S3F7: Human Evaluation | 0 | No human evaluation orchestration, crowdsourcing integration, or annotation interfaces. |

## Detailed Analysis

### S3F1: Pipeline Orchestration (0/3)

Evidence:
ranx has no pipeline orchestration capabilities. It's a metric computation library, not an evaluation orchestration framework.

```python
# From ranx/__init__.py
from .meta import compare, evaluate, fuse, normalize, optimize_fusion, plot
```

The core functionality is exposed through simple functions:

```python
# From docs/evaluate.md and examples
from ranx import Qrels, Run, evaluate

qrels = Qrels(qrels_dict)
run = Run(run_dict)

# Single metric evaluation
evaluate(qrels, run, "ndcg@5")

# Multiple metrics
evaluate(qrels, run, ["map@5", "mrr"])
```

Missing features:
- No DAG-based workflow support
- No task routing or dependency management
- No protocol support (zero-shot, few-shot, etc.)
- No conditional branching or dynamic workflows
- Operations are single-function calls on pre-computed results

Rating: 0 points - No orchestration features present. The library expects all retrieval results to be pre-computed.

---

### S3F2: Model Inference with Performance Telemetry (0/3)

Evidence:
ranx does not perform model inference. It only evaluates pre-computed retrieval results.

```python
# From docs/qrels.md and docs/run.md
# Users must provide pre-computed results
qrels_dict = {"q_1": {"d_12": 5, "d_25": 3}}
run_dict = {"q_1": {"d_12": 0.9, "d_23": 0.8}}

qrels = Qrels(qrels_dict)
run = Run(run_dict)
```

The `Run` class stores pre-computed relevance scores, not inference results:

```python
# From ranx/data_structures/run.py (inferred from usage)
# Run stores document rankings with pre-assigned scores
# No inference or telemetry collection
```

Missing features:
- No latency metrics (TTFT, per-token, end-to-end)
- No throughput tracking
- No resource consumption monitoring (memory, GPU, API calls)
- No cost tracking
- Library doesn't call models at all

Rating: 0 points - No inference or telemetry capabilities. This is a post-hoc evaluation library.

---

### S3F3: Test-Time Compute Optimization (0/3)

Evidence:
Since ranx doesn't perform inference, it has no test-time optimization features.

```python
# From ranx/meta/evaluate.py (inferred structure)
# Only metric computation, no caching or batching of inference
def evaluate(qrels, run, metrics, ...):
    # Computes metrics on pre-existing run results
    # No optimization of inference process
```

The only optimization is in metric computation itself via Numba:

```python
# From ranx/__init__.py
from numba import config
config.THREADING_LAYER = "workqueue"
```

This optimizes metric calculation, not model inference.

Missing features:
- No prompt caching (no prompts)
- No KV cache management (no inference)
- No response caching (no API calls)
- No batching (no inference requests)
- No quantization or model compilation

Rating: 0 points - No test-time optimization features. Library doesn't perform inference that could be optimized.

---

### S3F4: Failure Handling and Resilience (0/3)

Evidence:
ranx has no failure handling mechanisms. Metric computation is deterministic and single-shot.

```python
# From notebooks/3_evaluation.ipynb
# No retry logic, timeouts, or error recovery shown
evaluate(qrels, run, ["map@100", "mrr@10", "ndcg@10"])
```

Error handling is minimal and relies on Python exceptions:

```python
# From ranx/metrics/__init__.py
def metric_switch(metric):
    # ...
    else:
        raise ValueError(
            f"Metric {metric} not supported. Supported metrics are ..."
        )
```

Missing features:
- No retry logic or exponential backoff
- No timeout management
- No circuit breakers
- No failure recovery or rescheduling
- No error categorization (transient vs permanent)

Rating: 0 points - No failure handling beyond basic exception raising. Operations are deterministic metric computations.

---

### S3F5: Progress Checkpointing and Resumption (0/3)

Evidence:
ranx has no checkpointing capabilities. All operations are in-memory computations.

```python
# From notebooks/3_evaluation.ipynb
# Single evaluation call with no checkpointing
scores = evaluate(qrels, run, ["map@100", "mrr@10", "ndcg@10"])
```

The only persistence is manual saving of results:

```python
# From docs/run.md
# Manual save/load, not automatic checkpointing
run.save("path/to/run.json")
run = Run.from_file("path/to/run.json")
```

This is file I/O for results, not checkpoint/resume functionality.

Missing features:
- No automatic checkpointing intervals
- No resumption from checkpoints
- No incremental evaluation (recomputes all metrics)
- No state persistence beyond manual save
- No deduplication of results across runs

Rating: 0 points - No checkpointing features. Metric computation is fast enough to not require it.

---

### S3F6: Distributed Execution and Resource Management (1/3)

Evidence:
ranx has basic multi-threading via Numba parallelization but no advanced distributed features.

```python
# From ranx/__init__.py
from numba import config
config.THREADING_LAYER = "workqueue"
```

Parallel execution for metric computation:

```python
# From ranx/fusion/comb_sum.py
@njit(cache=True, parallel=True)
def _comb_sum_parallel(runs):
    q_ids = TypedList(runs[0].keys())
    combined_results = create_empty_results_dict_list(len(q_ids))
    
    for i in prange(len(q_ids)):  # Parallel loop
        q_id = q_ids[i]
        combined_results[i] = _comb_sum([run[q_id] for run in runs])
```

Thread control in evaluation:

```python
# From notebooks/3_evaluation.ipynb
# User can set thread count
evaluate(qrels, run, ["map@100", "mrr@10", "ndcg@10"], threads=1)
# threads=0 uses all available threads (default)
```

Present features:
- Multi-threading via Numba `prange`
- Thread count configuration via `threads` parameter
- Automatic parallelization for metric computation

Missing features:
- No multi-GPU support (no GPU usage at all)
- No multi-node/cluster support
- No dynamic load balancing
- No budget enforcement (cost, token, time limits)
- No heterogeneous resource handling

Rating: 1 point - Basic multi-threading for single-node computation, but no distributed execution or resource management.

---

### S3F7: Human Evaluation Orchestration (0/3)

Evidence:
ranx has no human evaluation capabilities. It only computes metrics on existing annotations.

```python
# From docs/qrels.md
# Qrels contain human judgments, but library doesn't collect them
qrels_dict = {"q_1": {"d_12": 5, "d_25": 3}}
qrels = Qrels(qrels_dict)
```

The library uses pre-existing qrels (query relevance judgments):

```python
# From docs/qrels.md
# Can load from ir-datasets (existing human annotations)
qrels = Qrels.from_ir_datasets("msmarco-document/dev")
```

Missing features:
- No crowdsourcing integration (MTurk, Scale AI, etc.)
- No annotation interfaces or UI builder
- No quality control mechanisms
- No inter-rater agreement metrics
- Library assumes human judgments already exist

Rating: 0 points - No human evaluation orchestration. Library uses pre-existing annotations only.

---

## Overall Assessment

ranx scores 1/21 points on Stage 3 (EXECUTE) criteria.

### Key Limitations:

1. Not an Execution Framework: ranx is a metric computation library, not an evaluation execution framework
2. No Model Inference: Expects pre-computed retrieval results as input
3. No Pipeline Orchestration: Single-shot metric computation only
4. No Monitoring: No telemetry, logging, or performance tracking
5. No Distributed Features: Basic multi-threading only
6. Post-hoc Analysis Only: Designed for analyzing results, not running evaluations

### What ranx Does Well:

- Fast metric computation via Numba optimization
- Statistical significance testing for comparisons
- Result fusion algorithms for combining multiple retrieval systems
- Simple, clean API for metric evaluation

### Use Case Fit:

ranx is excellent for Stage 5 (ANALYZE) - comparing and reporting evaluation results. It's not designed for Stage 3 (EXECUTE) capabilities like pipeline orchestration, inference management, or distributed execution. Users must handle evaluation execution separately and use ranx for post-hoc analysis.

### Architecture:

```
┌─────────────────────────────────────────┐
│  External Evaluation System             │
│  (Users run models separately)          │
└──────────────────┬──────────────────────┘
                   │ Pre-computed results
                   ▼
┌─────────────────────────────────────────┐
│  ranx (Post-hoc Analysis)               │
│  • Load qrels and runs                  │
│  • Compute metrics (parallel)           │
│  • Statistical significance tests       │
│  • Result fusion                        │
│  • Report generation                    │
└─────────────────────────────────────────┘
```

The single point awarded is for basic multi-threading in metric computation, which shows some awareness of performance optimization, but this is far from the distributed execution and orchestration features expected in Stage 3.