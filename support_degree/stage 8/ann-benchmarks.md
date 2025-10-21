# ann-benchmarks - Stage 8 (MONITOR) Evaluation

## Summary
Ann-benchmarks is a comprehensive benchmarking framework for approximate nearest neighbor (ANN) algorithms. It focuses on offline batch evaluation and comparison of different ANN implementations across standardized datasets. The framework has minimal monitoring and continuous improvement capabilities, as it's designed primarily for reproducible offline benchmarking rather than production deployment monitoring.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities. The framework is purely offline evaluation-focused with no statistical tests, drift scores, or production monitoring integration. All evaluations are on fixed test sets. |
| S8F2: Online Evaluation | 0 | No online or streaming evaluation support. The framework runs batch evaluations on static datasets. No A/B testing, shadow deployment, or automated rollback features exist. See `ann_benchmarks/runner.py` - all evaluations are offline single-run or batch-mode. |
| S8F3: Feedback Integration | 0 | No feedback loop integration. Results are stored as static HDF5 files (see `ann_benchmarks/results.py`). No mechanism for production log parsing, failure mining, or automatic dataset updates based on production data. |
| S8F4: Improvement Planning | 1 | Minimal analysis capabilities. The framework provides comparative metrics (recall, QPS, build time) and generates plots showing Pareto frontiers (see `plot.py`, `create_website.py`), but no automated root cause analysis, hyperparameter recommendations, or structured improvement roadmaps. Users must manually interpret plots to identify improvements. |

## Detailed Analysis

### S8F1: Production Drift Monitoring (0/3)

Evidence of absence:

1. No distribution shift detection: The framework only evaluates on fixed test sets loaded from HDF5 files:
```python
# ann_benchmarks/datasets.py
def get_dataset(which='glove-100-angular'):
    hdf5_filename = get_dataset_fn(which)
    try:
        with h5py.File(hdf5_filename, "r") as f:
            # ... loads static test/train splits
            return f, dimension
```

2. No performance degradation tracking: Results are stored per-run with no temporal tracking:
```python
# ann_benchmarks/results.py
def store_results(dataset, count, definition, query_argument_group, attrs, results, batch):
    fn = build_result_filepath(dataset, count, definition, query_argument_group, batch)
    with h5py.File(fn, "w") as f:
        # Stores single run results, no time-series analysis
```

3. No alerting infrastructure: No configuration or code for alerts. The framework is designed for researcher-driven analysis, not automated monitoring.

4. No production integration: All evaluations run in isolated Docker containers with synthetic datasets, no connection to production systems:
```python
# ann_benchmarks/runner.py
def run_docker(definition, dataset, count, runs, timeout, batch, cpu_limit, mem_limit):
    client = docker.from_env()
    # Runs in isolated container with local data
```

### S8F2: Online and Streaming Evaluation (0/3)

Evidence of absence:

1. Batch-only processing: The framework has a "batch mode" but this means passing all queries at once to the algorithm, not streaming evaluation:
```python
# ann_benchmarks/runner.py
def run(definition, dataset, count, runs, batch_mode=False):
    if batch_mode:
        results = algo.batch_query(X_test, k)  # All queries at once
    else:
        for q in X_test:
            results.append(algo.query(q, k))  # Sequential, not streaming
```

2. No A/B testing: No traffic splitting or multi-variant testing. Each algorithm is evaluated independently:
```python
# run.py - main evaluation loop
for definition in definitions:
    run_worker(cpu, mem_limit, args, queue)  # Sequential execution
```

3. No shadow deployment: Algorithms run in complete isolation with no production comparison capability.

4. No automated rollback: Results are purely informational with no deployment automation:
```python
# ann_benchmarks/results.py
def store_results(...):
    # Just stores metrics, no rollback logic
    f.create_dataset("buildtime", data=[attrs["build_time"]])
```

### S8F3: Feedback Loop Integration (0/3)

Evidence of absence:

1. Static datasets only: All datasets are pre-generated and stored as HDF5 files:
```python
# create_dataset.py
if __name__ == "__main__":
    fn = get_dataset_fn(args.dataset)
    DATASETS[args.dataset](fn)  # Creates static HDF5 file
```

2. No production data ingestion: The framework only loads from local HDF5 files:
```python
# ann_benchmarks/datasets.py
DATASETS = {
    'glove-100-angular': lambda f: download(...),  # Downloads static dataset
    'sift-128-euclidean': lambda f: download(...),
    # ... all predefined datasets
}
```

3. No failure mining: Results storage is write-only with no analysis of failure patterns:
```python
# ann_benchmarks/results.py
def store_results(...):
    f.create_dataset("neighbors", data=results["neighbors"])
    f.create_dataset("distances", data=results["distances"])
    # No failure analysis or categorization
```

4. No closed-loop automation: Manual workflow only - user must run `run.py`, then `plot.py`, then interpret results themselves.

### S8F4: Iteration Planning and Improvement Recommendations (1/3)

Limited capabilities:

1. Basic comparative analysis: The framework generates Pareto frontier plots showing recall vs QPS tradeoffs:
```python
# ann_benchmarks/plotting/utils.py
def create_pointset(data, xn, yn):
    # ... extracts metrics
    ps = [(x, y) for (algo, algo_name, x, y) in data]
    # Computes Pareto frontier
    frontier = []
    for i, (x, y) in enumerate(ps):
        if pareto_frontier(i, ps, xn, yn):
            frontier.append(i)
```

2. Multiple metrics tracked: Provides various performance metrics:
```python
# ann_benchmarks/plotting/metrics.py
all_metrics = {
    "k-nn": {...},
    "qps": {"description": "Queries per second (1/s)", ...},
    "build": {"description": "Build time (s)", ...},
    "candidates": {"description": "Candidates generated", ...},
    # ... more metrics
}
```

3. Visual comparison only: Website generation shows comparisons but no automated insights:
```python
# create_website.py
def build_detail_site(data, label_func, j2_env, linestyles, batch=False):
    for plottype in args.plottype:
        data["normal"].append(create_plot(runs, xn, yn, ...))
    # Just creates plots, no analysis
```

Missing capabilities:

- No root cause analysis: No automated identification of why algorithms perform poorly on specific queries
- No hyperparameter recommendations: Users must manually configure parameter sweeps in `config.yml`:
```yaml
# ann_benchmarks/algorithms/hnswlib/config.yml
run_groups:
  M-12:
    arg_groups: [{M: 12, efConstruction: 500}]
    query_args: [[10, 20, 40, 80, 120, 200, 400, 600, 800]]
```

- No dataset gap analysis: No identification of underrepresented scenarios or data collection needs
- No impact estimates: Plots show performance but don't estimate improvement impact from changes
- No roadmap generation: Users must manually interpret comparative plots and decide next steps

Evidence of manual workflow:
```python
# README.md workflow
"""
1. Run `python run.py` (can take days)
2. Run `python plot.py` to plot results
3. Run `create_website.py` to create a website with lots of plots
"""
```

All analysis requires manual interpretation - there's no automated recommendation system.

## Conclusion

Ann-benchmarks is an excellent offline benchmarking harness for comparing ANN algorithms, but it has virtually no production monitoring or continuous improvement automation. It's designed for researchers to run reproducible experiments and compare algorithms, not for monitoring deployed systems or providing automated improvement guidance. The framework assumes human experts will interpret the comparative plots and make informed decisions about algorithm selection and tuning.