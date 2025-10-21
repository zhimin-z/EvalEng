# HELM (stanford-crfm/helm) - Stage 5 (INTERPRET) Evaluation

## Summary

HELM is a comprehensive language model benchmarking framework with minimal built-in support for advanced interpretation and insight extraction. The framework focuses heavily on execution and basic metric computation, but lacks native stratification, failure analysis, A/B testing, and interactive exploration tools. Most interpretation functionality would need to be built externally using the raw output files.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S5F1: Stratified Analysis | 1 | Limited to manual subsplit filtering. No built-in stratification engine, no statistical significance tests, no Pareto analysis. Evidence: `Instance` supports `sub_split` field but no analysis tools. |
| S5F2: Failure Analysis | 1 | Raw failure data available in output files but no automated clustering, bias detection, or recommendations. Evidence: `scenario_state.json` contains requests/responses but no analysis tools. |
| S5F3: A/B Test Analysis | 0 | No built-in A/B testing framework, statistical tests, or comparison tools. Evidence: No statistical test implementations found in codebase. |
| S5F4: Interactive Exploration | 2 | Basic web UI (`helm-server`) for browsing results but limited drill-down and no on-the-fly analysis. Evidence: React frontend exists but focuses on display, not interactive analysis. |

---

## Detailed Analysis

### S5F1: Stratified Analysis and Performance Tradeoff Analysis

Rating: 1/3

Evidence:

1. Basic Subsplit Support (Manual Only)
   - From `src/helm/benchmark/scenarios/scenario.py`:
     ```python
     @dataclass(frozen=True)
     class Instance:
         input: Input
         references: List[Reference]
         split: str
         sub_split: Optional[str] = None
     ```
   - Instances can have `sub_split` tags, but there's no automated stratification engine

2. No Statistical Analysis
   - Examined `src/helm/benchmark/metrics/` - no statistical significance testing found
   - No chi-square, t-tests, or disparity analysis implementations
   - Example from `docs/tutorial.md` shows only basic aggregation:
     ```
     stats.json contains a serialized list of `PerInstanceStats`, which contains 
     the statistics produced for the metrics, aggregated across all instances
     ```

3. No Multi-Objective Tradeoff Analysis
   - No Pareto frontier computation found in metrics
   - No efficiency curves (performance vs cost)
   - File `scripts/estimate_cost.py` exists but only for pre-run estimation, not post-hoc analysis

4. Limited Grouping
   - From `docs/tutorial.md`:
     ```
     groups.json contains a serialized list of `Table`, each containing 
     information about groups in a group category
     ```
   - Groups are taxonomy-based, not dynamic stratification

Why not 0: The framework does support `sub_split` on instances and can produce per-instance statistics, allowing manual stratification by post-processing the JSON output files.

Why not 2: No built-in stratification tools, no statistical tests, no automated disparity analysis, and no tradeoff visualizations.

### S5F2: Failure Pattern and Bias Identification with Recommendations

Rating: 1/3

Evidence:

1. Raw Failure Data Available
   - From `docs/tutorial.md`:
     ```
     scenario_state.json contains a serialized `ScenarioState`, which contains 
     every request to and response from the model
     per_instance_stats.json contains a serialized list of `PerInstanceStats`
     ```
   - All request/response data is preserved but not analyzed

2. No Error Clustering
   - Searched for clustering algorithms - none found
   - No automatic failure categorization
   - No error taxonomy generation

3. Basic Bias Metrics Only
   - Found `bias_metrics.py` but it only computes basic demographic representation
   - No statistical bias tests (chi-square, permutation tests)
   - No intersectional analysis tools
   - Example from `src/helm/benchmark/scenarios/image_generation/demographic_stereotypes_scenario.py`:
     ```python
     # Simple prompts for bias detection, but no analysis tools
     Instance(Input(text=f"a photo of the face of {person}"), references=[], split=TEST_SPLIT)
     ```

4. No Automated Recommendations
   - No hyperparameter tuning suggestions
   - No prompt optimization recommendations
   - No dataset expansion priorities
   - The framework only collects data, doesn't provide actionable insights

Why not 0: The framework does preserve all failure data in structured JSON format (`scenario_state.json`), making external analysis possible.

Why not 2: No automated analysis, no clustering, no statistical bias detection, and no recommendations engine.

### S5F3: A/B Test Statistical Analysis

Rating: 0/3

Evidence:

1. No Statistical Testing Framework
   - Searched entire `src/helm/benchmark/metrics/` directory
   - No implementations of t-tests, chi-square, Mann-Whitney U
   - No confidence interval computation
   - No p-value calculations

2. No Comparison Tools
   - While multiple runs can be executed, there's no built-in comparison framework
   - From `docs/run_entries_configuration_files.md`:
     ```
     entries: [
       {description: "mmlu:subject=anatomy,model=openai/gpt2", priority: 1},
       {description: "mmlu:subject=philosophy,model=openai/gpt2", priority: 1},
     ]
     ```
   - Multiple runs are possible but comparison is manual

3. No Power Analysis
   - No sample size calculators
   - No minimum detectable effect computation
   - File `scripts/estimate_cost.py` only estimates token usage, not statistical power

4. No Sequential Testing
   - No early stopping support
   - No sequential confidence intervals
   - No always-valid p-values

5. No Multiple Comparison Correction
   - No Bonferroni correction
   - No Benjamini-Hochberg FDR control
   - No family-wise error rate control

Why 0: Complete absence of statistical testing infrastructure. The framework would require forking or building an entirely separate analysis pipeline to add these features.

### S5F4: Interactive Exploratory Analysis

Rating: 2/3

Evidence:

1. Basic Web UI Exists
   - From `docs/tutorial.md`:
     ```sh
     helm-server --suite my-suite
     # Then go to http://localhost:8000/
     ```
   - React frontend exists in `helm-frontend/` directory
   - From `helm-frontend/README.md`:
     ```
     This app makes use of React + TypeScript and built with vite. 
     Tailwindcss is used for CSS
     ```

2. Limited Sample Browsing
   - UI shows results but browsing capabilities are limited
   - From frontend structure:
     ```
     helm-frontend/src/
     ├── components
     ├── routes
     └── services
     ```
   - Routes suggest display-focused rather than analysis-focused

3. No Advanced Drill-Down
   - Can view aggregate metrics and individual runs
   - From `docs/tutorial.md`:
     ```
     - Leaderboards contains the leaderboards with aggregate metrics.
     - Predictions contains a searchable list of runs.
     ```
   - No multi-level drill-down from dataset → stratum → sample

4. No On-the-Fly Analysis
   - Cannot compute custom metrics in UI
   - No real-time filtering beyond basic search
   - No dynamic visualization updates
   - All metrics must be computed during `helm-run` or `helm-summarize`

5. Some Programmatic Access
   - From `scripts/examples/auto_client_usage.py`:
     ```python
     from helm.clients.auto_client import AutoClient
     client = AutoClient(credentials, file_storage_path, cache_backend_config)
     response = client.make_request(request)
     ```
   - Can access results programmatically but no interactive exploration API

6. No Collaborative Features
   - No annotation support
   - No shared sessions
   - Static server only

Why not 1: A functional web UI exists with basic browsing and visualization capabilities.

Why not 3: No drill-down, no on-the-fly analysis, limited interactivity, no collaborative features. The UI is primarily for displaying pre-computed results, not interactive exploration.

---

## Key Strengths

1. Comprehensive Data Preservation: All requests, responses, and per-instance stats are saved in structured JSON format
2. Basic Web Visualization: A working React-based frontend for viewing results
3. Extensible Architecture: Well-documented object specs make external analysis tools feasible
4. Rich Scenario Support: 100+ scenarios with diverse metrics provide substantial data for external analysis

## Key Limitations

1. No Built-in Statistical Analysis: Users must implement their own significance tests, confidence intervals, etc.
2. Manual Interpretation Required: No automated failure analysis, clustering, or recommendation engine
3. Static Results: Once `helm-summarize` runs, results are fixed—no interactive re-aggregation
4. Limited Stratification: While `sub_split` exists, there's no flexible slicing or hierarchical grouping
5. No A/B Testing Support: Complete absence of statistical comparison tools

## Recommendations for Users

If you need Stage 5 features with HELM:

1. For Stratification: Post-process `per_instance_stats.json` with pandas/numpy to implement custom slicing and statistical tests
2. For Failure Analysis: Build external tools using `scenario_state.json` to cluster errors and identify patterns
3. For A/B Testing: Export metrics to R or Python's scipy.stats for statistical comparison
4. For Interactive Exploration: Consider building custom Jupyter notebooks that read the JSON outputs

Example Post-Processing Workflow:
```python
import json
import pandas as pd
from scipy import stats

# Load results
with open("benchmark_output/runs/my-suite/run1/per_instance_stats.json") as f:
    stats_data = json.load(f)

# Convert to DataFrame for stratified analysis
df = pd.DataFrame(stats_data)

# Manual stratification by sub_split
for split in df['sub_split'].unique():
    split_data = df[df['sub_split'] == split]
    print(f"{split}: accuracy = {split_data['accuracy'].mean():.3f}")

# Statistical comparison (manual A/B test)
model_a_scores = df[df['model'] == 'gpt-3.5']['accuracy']
model_b_scores = df[df['model'] == 'gpt-4']['accuracy']
t_stat, p_value = stats.ttest_ind(model_a_scores, model_b_scores)
```

## Overall Assessment

HELM is a data collection and execution framework rather than an interpretation framework. It excels at systematically running evaluations and preserving detailed results, but provides minimal tools for extracting insights from those results. Users seeking Stage 5 capabilities will need to build their own analysis pipeline on top of HELM's output files.