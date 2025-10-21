# ann-benchmarks - Stage 4 (EVALUATE) Evaluation

## Summary
Ann-benchmarks is a specialized benchmarking framework for approximate nearest neighbor (ANN) algorithms. It focuses on performance evaluation (query speed, recall) for similarity search algorithms rather than LLM evaluation. The framework computes distance/similarity metrics, measures query performance, and generates comparative visualizations. While it has strong metric computation capabilities for its domain, it lacks the LLM-specific evaluation features described in the rubric (output validation, LLM-as-judge, multi-modal scoring).

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No output validation, normalization, policy compliance, or sanity checks exist. The framework directly evaluates algorithm results without validation steps. Evidence: No validation code found in `ann_benchmarks/runner.py` or other modules. |
| S4F2: Metric Computation | 2 | Has 5-6 specialized retrieval metrics (recall, queries-per-second, index size) with per-sample scoring capability. Evidence: `ann_benchmarks/plotting/metrics.py` defines metrics like "k-nn" (recall), "qps" (throughput), "build" (build time). Limited compared to comprehensive evaluation frameworks. |
| S4F3: Evaluator Models | 0 | No LLM-as-judge, specialized evaluator models, or rationale capture. The framework evaluates based on ground-truth distance computations only. Evidence: No evaluator model integration found in codebase. |
| S4F4: Multi-Modal Scoring | 0 | Text-only framework for vector similarity search. No vision-language, audio-text, or cross-modal evaluation capabilities. Evidence: All datasets in `ann_benchmarks/datasets.py` are single-modality float/bit vectors. |
| S4F5: Aggregate Statistics | 2 | Basic statistics (mean from multiple runs), comparison plots, and Pareto frontier analysis. No significance testing, confidence intervals, or ranking systems. Evidence: `ann_benchmarks/runner.py` line 114-119 shows best-of-N selection; `plot.py` generates comparison visualizations. |

---

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 0)

Evidence of absence:

The framework directly consumes algorithm outputs without validation:

```python
# ann_benchmarks/runner.py, lines 63-70
def run_individual_query(algo, X_train, X_test, distance, count, run_count, batch_mode):
    prepared_queries = prepare_batch_queries(X_test, count, distance, batch_mode)
    
    result = []
    for i in range(run_count):
        # ... timing code ...
        result.append({
            "run": i,
            "results": candidates,  # Direct usage without validation
            # ...
        })
```

No format validation: The code assumes algorithms return valid neighbor indices without checking for:
- Malformed output structures
- Out-of-bounds indices
- Duplicate neighbors
- Incorrect result counts

No policy compliance: No checks for harmful content, length constraints, or required fields beyond basic structure.

No sanity checks: Missing anomaly detection like:
- All results identical across queries
- Degenerate distance values
- Logical consistency of retrieved neighbors

Justification: 0 points - No validation features exist in the evaluation pipeline.

---

### S4F2: Task-Specific Metric Computation (Rating: 2)

Coverage - Specialized for retrieval:

```python
# ann_benchmarks/plotting/metrics.py, lines 1-50
all_metrics = {
    "k-nn": {
        "description": "Recall",
        "function": lambda true_distances, run: knn(true_distances, run),
        # ...
    },
    "qps": {
        "description": "Queries per second (1/s)",
        "function": lambda true_distances, run: qps(true_distances, run),
        # ...
    },
    "indexsize": {
        "description": "Index size (kB)",
        "function": lambda true_distances, run: index_size(true_distances, run),
        # ...
    },
    # ... 5-6 total metrics
}
```

Metric types available:
1. Recall (k-nn)
2. Queries per second (qps)
3. Index build time
4. Index size
5. Distance computations
6. Candidates retrieved

Per-sample scoring capability:

```python
# ann_benchmarks/plotting/utils.py, lines 145-160
def compute_all_metrics(true_distances, run, properties, recompute=False):
    """Compute metrics for each query in a run."""
    algo = properties["algo"]
    # ... 
    results = {}
    for name, metric in metrics.items():
        v = metric["function"](true_distances, run)
        results[name] = v  # Per-query metric
    # ...
    return results
```

Limitations:
- Only ~6 metrics (vs 20+ in rubric for 3 points)
- No text generation metrics (BLEU, ROUGE, BERTScore)
- No classification metrics (precision, F1, AUC-ROC)
- No safety/bias metrics
- Domain-specific to vector similarity

Extensibility:
Custom metrics can be added by modifying the `all_metrics` dictionary, but no plugin system exists.

Justification: 2 points - Has 5-6 specialized metrics with per-sample scoring, but limited coverage compared to comprehensive LLM evaluation frameworks. No standard NLP/classification metrics.

---

### S4F3: Evaluator Model Integration (Rating: 0)

Evidence of absence:

The evaluation is purely algorithmic, comparing retrieved neighbors against ground truth:

```python
# ann_benchmarks/plotting/metrics.py, lines 20-35
def knn(true_distances, run):
    """Compute recall by comparing to ground truth."""
    total = len(run)
    actual = 0
    for q, results in enumerate(run):
        # Compare retrieved neighbors to true nearest neighbors
        actual += len(
            set(results["results"]).intersection(
                set(true_distances[q][:len(results["results"])])
            )
        )
    return float(actual) / float(total)
```

No LLM-as-judge: The framework doesn't use language models to evaluate outputs.

No specialized evaluator models: No RAGAS, G-Eval, Prometheus, or similar integrations.

No rationale capture: Evaluation is numerical comparison only, no explanations generated.

Justification: 0 points - This is a vector similarity benchmarking tool, not an LLM evaluation framework. No evaluator model support.

---

### S4F4: Multi-Modal Scoring Protocols (Rating: 0)

Evidence from dataset definitions:

```python
# ann_benchmarks/datasets.py, lines 1-100
DATASETS = {
    'fashion-mnist-784-euclidean': { ... },
    'glove-25-angular': { ... },
    'sift-128-euclidean': { ... },
    # All datasets are single-modality vectors
}
```

Dataset structure:

```python
# create_dataset.py, lines 10-20
def write_output(train, test, fn, ...):
    with h5py.File(fn, 'w') as f:
        f.attrs['dimension'] = len(train[0])
        f.attrs['distance'] = distance
        f.create_dataset('train', data=train)  # Float vectors only
        f.create_dataset('test', data=test)
        f.create_dataset('neighbors', data=neighbors)
        f.create_dataset('distances', data=true_distances)
```

No multi-modal support:
- Only float/bit vector embeddings
- No image captioning metrics (CIDEr, SPICE)
- No VQA accuracy
- No text-to-image alignment (CLIP score)
- No audio-text metrics (WER, MOS)
- No video understanding metrics

Justification: 0 points - Single-modality framework focused on vector similarity. No multi-modal evaluation capabilities.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 2)

Basic statistics - Best of N runs:

```python
# ann_benchmarks/runner.py, lines 114-119
results = run_individual_query(algo, X_train, X_test, distance, count, run_count, batch_mode)

best_search_time = min([result["best_search_time"] for result in results])
# Takes minimum time across runs
```

Visualization and comparison:

```python
# plot.py, lines 20-60
def create_plot(all_data, raw, x_scale, y_scale, xn, yn, fn_out, linestyles, batch):
    """Create comparison plots with multiple algorithms."""
    for algo in sorted(all_data.keys(), key=mean_y):
        xs, ys, ls, axs, ays, als = create_pointset(all_data[algo], xn, yn)
        # Plot Pareto frontier
        plt.plot(xs, ys, "-", label=algo, ...)
    # Generate comparative visualization
```

Pareto frontier analysis:

```python
# ann_benchmarks/plotting/utils.py, lines 50-80
def create_pointset(data, xn, yn):
    """Extract Pareto frontier points."""
    # ... filtering logic ...
    data.sort(key=lambda t: (t[2], t[3]))
    # Return best performance points
```

What's available:
- Mean/best performance selection
- Comparison plots across algorithms
- Pareto frontier extraction
- Multiple run handling

What's missing (for 3 points):
- No significance testing (t-test, Wilcoxon)
- No confidence intervals
- No bootstrap methods
- No effect size computation
- No ranking systems (Elo, TrueSkill)
- No stratified statistics
- No class imbalance handling

Evidence of limitations:

```python
# data_export.py, lines 10-30
def export_results():
    """Export results to CSV."""
    for res in results:
        # Exports raw metrics without statistical analysis
        writer.writerow(res)
```

Justification: 2 points - Has basic statistics (min time selection), comparison visualizations, and Pareto frontier analysis. Missing advanced statistical testing, confidence intervals, and ranking systems needed for 3 points.

---

## Summary of Limitations

This framework is purpose-built for ANN algorithm benchmarking, not LLM evaluation:

1. Domain mismatch: Evaluates vector similarity algorithms, not language model outputs
2. No validation layer: Trusts algorithm outputs without checks
3. Specialized metrics: Only similarity search metrics (recall, QPS, index size)
4. No LLM integration: No judge models, no rationale generation
5. Single modality: Vector embeddings only
6. Basic statistics: Simple aggregation without significance testing

For ANN benchmarking, it's well-designed. For LLM evaluation per this rubric, it lacks most required features.

---

## Key Evidence Files

- `ann_benchmarks/runner.py`: Core evaluation loop (no validation)
- `ann_benchmarks/plotting/metrics.py`: Metric definitions (~6 specialized metrics)
- `ann_benchmarks/plotting/utils.py`: Metric computation and Pareto frontier
- `plot.py`: Visualization and comparison generation
- `ann_benchmarks/datasets.py`: Dataset handling (vectors only)
- `requirements.txt`: Dependencies (no LLM libraries like transformers, openai)