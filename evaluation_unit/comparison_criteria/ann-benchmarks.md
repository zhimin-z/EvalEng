## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: `ann_benchmarks/datasets.py` - `write_output()` and `write_sparse_output()` functions

```
def write_output(train: numpy.ndarray, test: numpy.ndarray, fn: str, distance: str, point_type: str = "float", count: int = 100) -> None:
    """
    Writes the provided training and testing data to an HDF5 file. It also computes 
    and stores the nearest neighbors and their distances for the test set using a 
    brute-force approach.
    """
    from ann_benchmarks.algorithms.bruteforce.module import BruteForceBLAS

    with h5py.File(fn, "w") as f:
        # ... dataset creation ...
        
        # Create datasets for neighbors and distances
        neighbors_ds = f.create_dataset("neighbors", (len(test), count), dtype=int)
        distances_ds = f.create_dataset("distances", (len(test), count), dtype=float)

        # Fit the brute-force k-NN model
        bf = BruteForceBLAS(distance, precision=train.dtype)
        bf.fit(train)

        for i, x in enumerate(test):
            # Query the model and sort results by distance
            res = list(bf.query_with_distances(x, count))
            res.sort(key=lambda t: t[-1])

            # Save neighbors indices and distances
            neighbors_ds[i] = [idx for idx, _ in res]
            distances_ds[i] = [dist for _, dist in res]
```
This code clearly demonstrates the creation of ground truth labels for benchmark evaluation. The function computes the true k-nearest neighbors using a brute-force approach and stores them as "neighbors" and "distances" in the HDF5 dataset files. These are explicit reference answers that model outputs will be compared against during evaluation.

Evidence 2: `ann_benchmarks/datasets.py` - `get_dataset()` function

```
def get_dataset(dataset_name: str) -> Tuple[h5py.File, int]:
    """
    Fetches a dataset by downloading it from a known URL or creating it locally
    if it's not already present. The dataset file is then opened for reading, 
    and the file handle and the dimension of the dataset are returned.
    """
    hdf5_filename = get_dataset_fn(dataset_name)
    # ... download or create dataset ...
    
    hdf5_file = h5py.File(hdf5_filename, "r")
    return hdf5_file, dimension
```
The function loads datasets that contain pre-computed ground truth nearest neighbors. These datasets (downloaded from URLs like "https://ann-benchmarks.com/{dataset_name}.hdf5") contain the explicit labels that algorithms are evaluated against.

Evidence 3: `ann_benchmarks/plotting/metrics.py` - Recall computation functions

```
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

def knn(dataset_distances, run_distances, count, metrics, epsilon=1e-3):
    # ...
    mean, std, recalls = get_recall_values(dataset_distances, run_distances, count, knn_threshold, epsilon)
    knn_metrics.attrs["mean"] = mean
    knn_metrics.attrs["std"] = std
    knn_metrics["recalls"] = recalls
```
These functions compute recall by comparing algorithm outputs (`run_distances`) against ground truth distances (`dataset_distances`). The `dataset_distances` parameter represents the explicit labels (true nearest neighbors) that serve as the comparison criteria for evaluating model performance.

Evidence 4: `ann_benchmarks/runner.py` - `run_individual_query()` function

```
def run_individual_query(algo: BaseANN, X_train: numpy.array, X_test: numpy.array, distance: str, count: int, 
                         run_count: int, batch: bool) -> Tuple[dict, list]:
    """Run a search query using the provided algorithm and report the results."""
    # ...
    candidates = [
        (int(idx), float(metrics[distance].distance(v, X_train[idx]))) for idx in candidates
    ]
```
The code computes distances between query results and the actual training data points, which are then compared against the ground truth neighbors stored in the dataset. The true neighbors serve as explicit labels for evaluation.

### None

Evidence 1: `ann_benchmarks/plotting/metrics.py` - Performance metrics

```
def queries_per_second(queries, attrs):
    return 1.0 / attrs["best_search_time"]

def percentile_50(times):
    return np.percentile(times, 50.0) * 1000.0

def percentile_95(times):
    return np.percentile(times, 95.0) * 1000.0

def percentile_99(times):
    return np.percentile(times, 99.0) * 1000.0

def build_time(queries, attrs):
    return attrs["build_time"]

def index_size(queries, attrs):
    return attrs.get("index_size", 0)

def dist_computations(queries, attrs):
    return attrs.get("dist_comps", 0) / (attrs["run_count"] * len(queries))
```
These metrics measure intrinsic properties of algorithm performance without comparing to external references:
- Queries per second (QPS): Throughput measurement based on execution time
- Latency percentiles: Distribution of query response times
- Build time: Time taken to construct the index
- Index size: Memory footprint of the algorithm
- Distance computations: Internal computational efficiency

These are all reference-free evaluations that assess the algorithm's computational characteristics without comparing to ground truth or external standards.

Evidence 2: `ann_benchmarks/runner.py` - Timing and resource measurements

```
def run_individual_query(...):
    best_search_time = float("inf")
    for i in range(run_count):
        # ...
        start = time.time()
        candidates = algo.query(v, count)
        total = time.time() - start
        # ...
        search_time = total_time / len(X_test)
        best_search_time = min(best_search_time, search_time)
    
    attrs = {
        "best_search_time": best_search_time,
        "candidates": avg_candidates,
        # ...
    }
```
The code directly measures algorithm execution time and computes throughput metrics without any external reference. These are intrinsic quality measures based solely on the algorithm's performance characteristics.

Evidence 3: `ann_benchmarks/runner.py` - Index building metrics

```
def build_index(algo: BaseANN, X_train: numpy.ndarray) -> Tuple:
    """Builds the ANN index for a given ANN algorithm on the training data."""
    t0 = time.time()
    memory_usage_before = algo.get_memory_usage()
    algo.fit(X_train)
    build_time = time.time() - t0
    index_size = algo.get_memory_usage() - memory_usage_before

    print("Built index in", build_time)
    print("Index size: ", index_size)

    return build_time, index_size
```
This function measures build time and memory usage without comparing to any external standard. These are self-contained metrics that evaluate the computational efficiency of the indexing process.