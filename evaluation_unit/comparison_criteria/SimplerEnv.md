## Comparison Criteria Categories

[Comparative Baseline]

## Detailed Analysis

### Comparative Baseline

Evidence 1: Real Robot Performance Baseline
- File: `simpler_env/utils/metrics.py`
- Code Reference: `REAL_PERF` dictionary
```python
REAL_PERF = {    # Real robot eval performance --> extract via: REAL_PERF[task][policy]
    "google_robot_pick_coke_can": {
        "rt-2-x": 0.907,
        "rt-1-converged": 0.853,
        "rt-1-15pct": 0.920,
        "rt-1-x": 0.760,
        "rt-1-begin": 0.133,
        "octo-base": 0.293,
    },
    "google_robot_move_near": {
        "rt-2-x": 0.733,
        "rt-1-converged": 0.633,
        ...
    },
    ...
}
```
Stores real-world robot evaluation performance data as baseline reference metrics. These aggregate performance values from physical robot experiments serve as comparison standards for evaluating simulated policy performance across multiple tasks.

Evidence 2: Simulated Performance Storage
- File: `simpler_env/utils/metrics.py`
- Code Reference: `SIMPLER_PERF` dictionary
```python
SIMPLER_PERF = {    # SIMPLER simulated eval performance --> extract via: SIMPLER_PERF[task][policy]
    "google_robot_pick_coke_can": {
        "rt-2-x": 0.787,
        "rt-1-converged": 0.857,
        "rt-1-15pct": 0.710,
        ...
    },
    ...
}
```
Stores simulated evaluation performance for comparison against real robot baselines. These simulation results are evaluated relative to real-world performance rather than against explicit correctness labels.

Evidence 3: Ranking Comparison Metrics
- File: `simpler_env/utils/metrics.py`
- Code Reference: Comparative metrics functions
```python
def mean_maximum_rank_violation(
    perf_sim: Sequence[float], perf_real: Sequence[float]
) -> float:
    # Compares ranking of policies between sim and real
    ...

def pearson_correlation(perf_sim: Sequence[float], perf_real: Sequence[float]) -> float:
    # Computes correlation between sim and real performance
    ...
```
Implements ranking-based and correlation metrics for comparing simulated performance against real-world baseline performance. These functions evaluate how well simulation reproduces the relative ordering of policies observed in physical robot experiments.

Evidence 4: Baseline Comparison Execution
- File: `tools/calc_metrics.py`
- Code Reference: Metric calculation against baselines
```python
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF

if __name__ == "__main__":
    print("======= SIMPLER Evaluation =======\n")

    for k in SIMPLER_PERF.keys():
        print(f"{k}:")
        mmrv = mean_maximum_rank_violation(
            list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
        )
        pearson = pearson_correlation(
            list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
        )
        print(f"MMRV: {mmrv}, Pearson: {pearson}\n")
```
Executes comparative evaluation by computing metrics between simulated and real robot performance. The evaluation measures correlation and ranking agreement rather than correctness against ground truth labels.

Evidence 5: Task-Specific Baseline Usage
- File: `tools/calc_metrics_evaluation_videos.py`
- Code Reference: Real evaluation baseline comparison
```python
def calc_pick_coke_can_stats(root_result_dir):
    print("*Pick coke can results*")
    # If you use a new checkpoint, please update the real evaluation results here
    coke_can_real_success = {
        "horizontal": {
            "rt-2-x": 0.92,
            "rt-1-converged": 0.96,
            "rt-1-15pct": 1.0,
            ...
        },
        ...
    }
    ...
    # Compare simulation results against real baseline
    print(
        f"{coke_can_orientation} MMRV",
        mean_maximum_rank_violation(
            list(coke_can_sim_variant_success[coke_can_orientation].values()),
            list(coke_can_real_success[coke_can_orientation].values()),
        ),
    )
```
Compares task-specific simulation results against real robot baseline performance. The evaluation focuses on relative quality assessment through ranking comparison rather than absolute correctness validation.

Evidence 6: Framework Documentation
- File: `README.md`
- Code Reference: Baseline comparison methodology
```python
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF

sim_eval_perf = [
    your_sim_eval(task="google_robot_move_near", policy=p) 
    for p in ["rt-1-x", "octo", ...]
]
real_eval_perf = [
    REAL_PERF["google_robot_move_near"][p] for p in ["rt-1-x", "octo", ...]
]
mmrv = mean_maximum_rank_violation(real_eval_perf, sim_eval_perf)
pearson = pearson_correlation(real_eval_perf, sim_eval_perf)
```
Documentation explicitly describes the comparative baseline evaluation approach. The framework evaluates simulation quality by measuring how well simulated policy rankings correlate with real-world robot performance rankings, establishing real robot results as the comparison standard.