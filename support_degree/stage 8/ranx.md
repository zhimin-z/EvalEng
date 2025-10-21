# ranx - Stage 8 (MONITOR) Evaluation

## Summary
ranx is a Python library for ranking evaluation in Information Retrieval and Recommender Systems. It focuses on offline evaluation with statistical testing and fusion algorithms. The library does not provide production monitoring capabilities and is designed purely for experimental evaluation of ranking systems.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities. Library is designed for offline evaluation only. |
| S8F2: Online Evaluation | 0 | No online/streaming evaluation support. All evaluation is batch-based on static qrels/runs. |
| S8F3: Feedback Integration | 0 | No feedback loop integration. Library operates on pre-computed results files. |
| S8F4: Improvement Planning | 1 | Basic error analysis via comparison reports, but no automated recommendations or roadmap generation. |

---

## Detailed Analysis

### S8F1: Production Drift Monitoring
Rating: 0/3

Evidence:
ranx has no drift monitoring capabilities. The library is designed exclusively for offline evaluation.

1. No Distribution Shift Detection: No statistical drift tests found in codebase.
   - `ranx/statistical_tests/` only contains Fisher's test and t-test for comparing models, not detecting drift
   - From `ranx/statistical_tests/__init__.py`:
   ```python
   __all__ = [
       "fisher_randomization_test",
       "paired_student_t_test",
       "compute_statistical_significance",
   ]
   ```
   - These are for significance testing between runs, not production drift monitoring

2. No Performance Degradation Tracking: No online metric computation.
   - All evaluation is batch-based through `evaluate()` function
   - From `docs/evaluate.md` and `ranx/meta/evaluate.py`: operates on static `Qrels` and `Run` objects

3. No Behavioral Monitoring: No production data integration.
   - Library works with pre-computed result files (`.trec`, `.json`, `.lz4` formats)
   - From `docs/run.md`:
   ```python
   run = Run.from_file("path/to/run.json")  # JSON file
   run = Run.from_file("path/to/run.trec")  # TREC-Style file
   ```

4. No Alerting System: No alerting infrastructure.
   - No alert configuration, thresholds, or routing found in codebase

5. No Production Integration: Designed for offline analysis.
   - FAQ states explicitly this is for ranking tasks, not classification
   - From `docs/faq.md`: "ranx is meant for ranking tasks"

Conclusion: ranx is purely an offline evaluation harness with no production monitoring capabilities.

---

### S8F2: Online and Streaming Evaluation
Rating: 0/3

Evidence:
ranx has no online or streaming evaluation capabilities. All evaluation is batch-based.

1. No Streaming Support: All data loaded into memory at once.
   - From `ranx/data_structures/run.py`: Runs are represented as nested dictionaries loaded entirely in memory
   - No streaming data structures or windowed analysis

2. No A/B Testing: No traffic splitting or gradual rollout.
   - The `compare()` function compares pre-computed runs, not live traffic
   - From `docs/compare.md`:
   ```python
   report = compare(
       qrels=qrels,
       runs=[run_1, run_2, run_3, run_4, run_5],
       metrics=["map@100", "mrr@100", "ndcg@10"],
   )
   ```
   - This compares static result files, not live systems

3. No Shadow Deployment: No side-by-side production comparison.
   - Library operates on pre-computed results from offline experiments

4. No Automated Rollback: No production deployment features.
   - Library has no concept of deployment or rollback

5. No Online Metrics: All metrics computed in batch.
   - From `ranx/metrics/` directory: all metrics are batch computations using Numba JIT compilation
   - Example from `ranx/metrics/ndcg.py`:
   ```python
   @njit(cache=True, parallel=True)
   def ndcg(qrels, run, k=0, idcg=None):
       # Batch computation on entire dataset
   ```

Conclusion: ranx is designed for offline batch evaluation only. No online/streaming capabilities.

---

### S8F3: Feedback Loop Integration
Rating: 0/3

Evidence:
ranx has no feedback loop integration. It operates on static datasets with no production data ingestion.

1. No Data Ingestion: No production log parsing or real-time ingestion.
   - Library works with pre-existing files in standard formats (TREC, JSON)
   - From `docs/qrels.md`:
   ```python
   qrels = Qrels.from_file("path/to/qrels.json")
   qrels = Qrels.from_file("path/to/qrels.trec")
   ```

2. No Failure Mining: No automatic extraction of production failures.
   - Library provides comparison reports but requires manual analysis
   - From `notebooks/4_comparison_and_report.ipynb`: reports show statistical significance but don't automatically extract failure cases

3. No Metric Updates: No dynamic metric adjustment based on production.
   - Metrics are fixed implementations
   - From `docs/metrics.md`: 12 standard IR metrics (MAP, NDCG, MRR, etc.) with no mechanism for updating

4. No Closed-Loop Automation: No integration with retraining pipelines.
   - Library is standalone evaluation tool
   - No pipeline orchestration capabilities

Integration with External Systems:
ranx can load qrels from `ir-datasets`:
```python
# From docs/qrels.md
qrels = Qrels.from_ir_datasets("msmarco-document/dev")
```
However, this is static data loading, not feedback loop integration.

Conclusion: ranx is a static evaluation tool with no production feedback integration.

---

### S8F4: Iteration Planning and Improvement Recommendations
Rating: 1/3

Evidence:
ranx provides basic comparison reports showing statistical significance between models, but no automated recommendations or improvement planning.

What EXISTS (basic error analysis):

1. Comparison Reports: Shows which models are significantly better/worse.
   - From `docs/compare.md`:
   ```python
   report = compare(
       qrels=qrels,
       runs=[run_1, run_2, run_3, run_4, run_5],
       metrics=["map@100", "mrr@100", "ndcg@10"],
       max_p=0.01
   )
   ```
   - Output shows superscripts indicating statistical significance:
   ```
   #    Model    MAP@100    MRR@100    NDCG@10
   ---  -------  --------   --------   ---------
   a    model_1  0.320ᵇ     0.320ᵇ     0.368ᵇᶜ
   b    model_2  0.233      0.234      0.239
   ```

2. Win/Tie/Loss Tracking: Shows pairwise comparison outcomes.
   - From `notebooks/4_comparison_and_report.ipynb`:
   ```python
   report.win_tie_loss[(("model_1", "model_2")]
   ```

3. Export to LaTeX: For publication-ready tables.
   - From `docs/report.md`:
   ```python
   print(report.to_latex())
   ```

What DOES NOT EXIST:

1. No Root Cause Analysis: No automated bottleneck identification.
   - Reports show which model is better but not why
   - No error pattern analysis beyond aggregate metrics

2. No Hyperparameter Recommendations: Only for fusion algorithms.
   - Fusion optimization exists (e.g., `optimize_fusion()` in `ranx/meta/optimize_fusion.py`)
   - But this is only for combining existing runs, not for improving individual models
   - From `notebooks/5_fusion.ipynb`:
   ```python
   best_params = optimize_fusion(
       qrels=qrels,
       runs=[run_4, run_5],
       method="wsum",
       metric="ndcg@100"
   )
   ```

3. No Prompt Optimization: Not applicable (IR library, not LLM).

4. No Dataset Expansion: No gap analysis or data collection recommendations.
   - Library works with existing datasets
   - No analysis of underrepresented scenarios

5. No Roadmap Generation: No experiment planning or prioritization.
   - Reports are purely retrospective
   - No forward-looking recommendations

Conclusion: ranx provides basic comparison reports with statistical testing, which offers minimal insight into improvement directions. No automated recommendations, root cause analysis, or roadmap generation. Caps at 1 point for basic error analysis.

---

## Overall Assessment

ranx is a high-quality offline evaluation library but has zero production monitoring capabilities:

- Strengths: Fast evaluation with Numba, statistical testing, fusion algorithms, export to LaTeX
- Stage 8 Limitations: No drift monitoring, no online evaluation, no feedback loops, minimal improvement recommendations

Total Stage 8 Score: 1/12

The library explicitly positions itself as an evaluation tool for research and offline experiments:
- From `README.md`: "A Blazing-Fast Python Library for Ranking Evaluation and Comparison"
- All documentation focuses on comparing pre-computed results from offline experiments
- No production deployment or monitoring features

ranx excels at its intended purpose (offline evaluation) but is not designed for Stage 8 (MONITOR) capabilities. Users needing production monitoring would need to integrate ranx with external systems for logging, alerting, and continuous evaluation.