# Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Recall computation functions
- File: `ann_benchmarks/plotting/metrics.py`
- Functions: `knn()`, `epsilon()`, `rel()`, and `get_recall_values()`
- Code Reference:
```python
def get_recall_values(dataset_distances, run_distances, count, threshold, epsilon=1e-3):
    recalls = np.zeros(len(run_distances))
    for i in range(len(run_distances)):
        t = threshold(dataset_distances[i], count, epsilon)
        actual = 0
        for d in run_distances[i][:count]:
            if d <= t:
                actual += 1
        recalls[i] = actual
    return (np.mean(recalls) / float(count), np.std(recalls) / float(count), recalls)
```
The functions compute metrics by comparing algorithm-generated nearest neighbor results against ground truth without executing any code. The `get_recall_values()` function specifically compares distances returned by algorithms to ground truth distances using threshold functions, demonstrating static analysis of pre-computed results.

Evidence 2: Performance metric calculations
- File: `ann_benchmarks/plotting/metrics.py`
- Functions: `queries_per_second()`, `percentile_50()`, `percentile_95()`
- Code Reference:
```python
def queries_per_second(queries, attrs):
    return 1.0 / attrs["best_search_time"]

def percentile_50(times):
    return np.percentile(times, 50.0) * 1000.0
```
These functions analyze timing data from algorithm runs without executing the algorithms themselves. They compute performance characteristics such as throughput and latency percentiles from stored execution metadata, exemplifying static analysis of runtime behavior.

Evidence 3: Metrics computation from stored results
- File: `ann_benchmarks/plotting/utils.py`
- Function: `compute_metrics()`
- Code Reference:
```python
# Called in plot.py line 98:
runs = compute_metrics(np.array(dataset["distances"]), results, args.x_axis, args.y_axis, args.recompute)
```
This function computes various performance metrics by analyzing stored results without executing algorithms. It processes pre-computed distance data and results to derive evaluation metrics, demonstrating the harness's static analysis approach.

Evidence 4: Result storage and loading mechanism
- File: `ann_benchmarks/results.py`
- Function: `store_results()`
- Code Reference:
```python
def store_results(dataset_name: str, count: int, definition: Definition, query_arguments:Any, attrs, results, batch):
    # ...
    with h5py.File(filename, "w") as f:
        for k, v in attrs.items():
            f.attrs[k] = v
        times = f.create_dataset("times", (len(results),), "f")
        neighbors = f.create_dataset("neighbors", (len(results), count), "i")
        distances = f.create_dataset("distances", (len(results), count), "f")
```
The function saves algorithm outputs (neighbors, distances, times) to HDF5 files for later analysis. This storage mechanism enables subsequent static analysis of results without re-executing algorithms, separating the execution phase from the evaluation phase.

Evidence 5: Output validation through distance comparison
- File: `ann_benchmarks/runner.py`
- Function: `run_individual_query()`
- Code Reference:
```python
candidates = [
    (int(idx), float(metrics[distance].distance(v, X_train[idx]))) for idx in candidates
]
```
After running queries, results are compared to ground truth by computing distances between query vectors and returned candidates. This validates algorithm outputs by checking distances, demonstrating static analysis verification of correctness without interactive execution.