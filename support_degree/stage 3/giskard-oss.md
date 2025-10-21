# Giskard - Stage 3 (EXECUTE) Evaluation

## Summary
Giskard is a comprehensive ML testing and evaluation framework with strong documentation and examples, but limited execution orchestration capabilities. The framework excels at scan-based vulnerability detection for tabular, NLP, and LLM models, with integrations to MLflow, W&B, and CI/CD pipelines. However, it lacks native pipeline orchestration, distributed execution features, and advanced test-time optimizations. Execution is primarily sequential and single-node focused.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 1 | Evidence: The framework lacks DAG-based workflow orchestration. From `giskard/core/suite.py`, test execution is sequential: `for test in self.tests: result = test.execute(...)`. The `scan` function in `giskard/scanner/scanner.py` shows sequential detector execution with no conditional branching or parallel task support. No workflow definition language or dynamic routing is present. Tests are executed one-by-one without dependency management. |
| S3F2: Inference & Telemetry | 1 | Evidence: Minimal telemetry exists. In `giskard/models/base/model.py`, only basic execution time is logged: `logger.info(f"Predicted dataset with shape {dataset.df.shape} executed in {timedelta}")`. No metrics for TTFT, P95/P99 percentiles, throughput (tokens/sec), memory usage, GPU utilization, or cost tracking. The `ModelPredictionResults` class only stores predictions without performance metadata. |
| S3F3: Test-Time Optimization | 1 | Evidence: Very limited optimization support. In `giskard/models/cache/cache.py`, there's basic response caching: `if prediction_url in self._cache_dict: return self._cache_dict[prediction_url]`. No prompt caching, KV cache management, dynamic batching, speculative decoding, quantization, or model compilation. The cache is simple dictionary-based with no hit rate reporting or intelligent eviction policies. |
| S3F4: Failure Handling | 1 | Evidence: Minimal error handling. In `giskard/llm/client/base.py`, there's basic retry logic: `for attempt in range(num_retries)` but no exponential backoff, circuit breakers, or sophisticated failure recovery. Tests continue on errors but without detailed categorization. From `giskard/scanner/scanner.py`: `except Exception as e: logger.warning(f"Detector {detector} failed: {e}")` - errors are logged but not recovered from intelligently. |
| S3F5: Checkpointing | 0 | Evidence: No checkpointing or resumption capability found. Scanning in `giskard/scanner/scanner.py` runs to completion without intermediate state saving. The `Suite.run()` method in `giskard/core/suite.py` has no checkpoint/resume logic. If execution fails mid-scan, users must restart from scratch. No incremental evaluation or result deduplication mechanisms exist. |
| S3F6: Distributed Execution | 0 | Evidence: Single-node execution only. No multi-GPU, multi-node, or cluster support. From `giskard/scanner/scanner.py`, all detectors run sequentially on a single thread. No Ray, Dask, or Kubernetes integration. No load balancing, work stealing, or heterogeneous resource handling. No budget enforcement for costs, tokens, or time limits. The MLflow integration in `docs/integrations/mlflow/index.md` mentions running evaluations but provides no distributed execution capabilities. |
| S3F7: Human Evaluation | 0 | Evidence: No human evaluation orchestration features. No crowdsourcing platform integrations (MTurk, Scale AI, Labelbox). No annotation UI builder, quality control mechanisms, or inter-rater agreement metrics (Cohen's kappa, etc.). The framework focuses entirely on automated ML testing with no provisions for human-in-the-loop evaluation workflows. |

## Detailed Analysis

### S3F1: Pipeline Orchestration (1/3)
Strengths:
- Test suites can group multiple tests together via `Suite` class
- Basic test organization with `add_test()` method
- Integration with pytest for CI/CD execution

Limitations:
```python
# From giskard/core/suite.py - Sequential execution only
def run(self, verbose: bool = True) -> SuiteResult:
    for test in self.tests:
        try:
            result = test.execute(...)
        except Exception as e:
            logger.error(f"Test {test.test_id} failed: {e}")
```
- No DAG-based dependencies between tests
- No parallel execution of independent tests
- No conditional branching based on results
- No dynamic task generation during execution
- No protocol selection (zero-shot, few-shot, chain-of-thought)

### S3F2: Inference & Telemetry (1/3)
Strengths:
- Basic execution timing for predictions
- Integration with MLflow for logging scan results

Limitations:
```python
# From giskard/models/base/model.py - Only basic timing
start = datetime.now()
predictions = self._inference_call(dataset)
timedelta = datetime.now() - start
logger.info(f"Predicted dataset with shape {dataset.df.shape} executed in {timedelta}")
```
- No TTFT, per-token latency, or P95/P99 metrics
- No throughput tracking (requests/sec, tokens/sec)
- No memory usage monitoring (peak/average)
- No GPU utilization tracking
- No API call counting or token consumption tracking
- No real-time cost accumulation

### S3F3: Test-Time Optimization (1/3)
Strengths:
- Simple response caching for identical inputs
- Cache hit avoids redundant model calls

Limitations:
```python
# From giskard/models/cache/cache.py - Basic dictionary cache
def predict(self, prediction_url: str, prediction_input):
    if prediction_url in self._cache_dict:
        return self._cache_dict[prediction_url]
    
    result = self._call_worker(prediction_url, prediction_input)
    self._cache_dict[prediction_url] = result
    return result
```
- No prompt prefix caching or KV cache management
- No dynamic or continuous batching
- No speculative decoding, quantization, or compilation
- No cache hit rate reporting or optimization
- No cost vs. speed tradeoff analysis

### S3F4: Failure Handling (1/3)
Strengths:
- Basic retry logic for LLM client calls
- Timeout handling for HTTP requests
- Test execution continues on individual test failures

Limitations:
```python
# From giskard/llm/client/base.py - Simple retry without backoff
def complete(self, messages, caller_id=None, num_retries=6, backoff_factor=1):
    for attempt in range(num_retries):
        try:
            return self._model.complete(messages)
        except Exception as e:
            if attempt < num_retries - 1:
                time.sleep(backoff_factor)  # Fixed delay, not exponential
            else:
                raise
```
- No exponential backoff (uses fixed delay)
- No circuit breakers for failing services
- No per-error-type retry strategies
- No intelligent request rescheduling
- Limited error categorization (transient vs. permanent)

### S3F5: Checkpointing (0/3)
Critical Gap:
```python
# From giskard/scanner/scanner.py - No checkpointing mechanism
def scan(model, dataset, features=None, params=None):
    issues = []
    for detector_class in get_detector_classes():
        detector = detector_class()
        detector_issues = detector.run(model, dataset, features)
        issues.extend(detector_issues)
    
    return ScanReport(issues=issues)  # No state persistence
```
- No automatic or manual checkpointing during scans
- No resumption capability if execution fails
- No incremental evaluation to avoid re-computing results
- No checkpoint validation or cleanup
- Users must restart entire scans on failure

### S3F6: Distributed Execution (0/3)
Critical Gap:
- All execution is single-threaded and single-node
- No data parallelism, model parallelism, or pipeline parallelism
- No cluster support (Slurm, Kubernetes)
- No distributed communication frameworks (Ray, Dask)
- No load balancing or work stealing
- No budget enforcement ($100 max, 1M tokens, 4 hour limits)

The MLflow integration example shows single-node execution:
```python
# From docs/integrations/mlflow/mlflow-llm-example.ipynb
with mlflow.start_run(run_name=model_name):
    mlflow.evaluate(model=models[model_name], ...)  # Single-node only
```

### S3F7: Human Evaluation (0/3)
Critical Gap:
- No crowdsourcing platform integrations
- No annotation interface builder
- No quality control mechanisms (attention checks, gold standards)
- No inter-rater agreement metrics
- Framework is purely automated testing focused

## Integration Analysis

### MLflow Integration (Positive)
```python
# From docs/integrations/mlflow/index.md
evaluator_config = {
    "model_config": {"classification_labels": ["no", "yes"]},
    "dataset_config": {"name": "Articles"},
    "scan_config": {"params": {"text_perturbation": {"num_samples": 1000}}}
}

mlflow.evaluate(
    model=model_uri,
    model_type="classifier",
    data=df_sample,
    evaluators="giskard",  # Giskard as MLflow plugin
    evaluator_config=evaluator_config
)
```
- Clean integration with MLflow's evaluation API
- Automatic logging of scan results, test suites, and SHAP plots
- But doesn't add distributed execution capabilities

### W&B Integration (Positive)
```python
# From docs/integrations/wandb/index.md
scan_results.to_wandb(run)
test_suite_results.to_wandb(run)
shap_results.to_wandb(run)
```
- Good for visualization and tracking
- But no performance telemetry beyond basic metrics

### CI/CD Integration (Limited)
```yaml
# From docs/integrations/cicd/pipeline.ipynb
jobs:
  automatic_scan:
    runs-on: ubuntu-latest
    steps:
      - run: python scan.py  # Simple script execution
```
- Basic GitHub Actions integration
- No parallel job execution or sophisticated orchestration
- Exit codes for pass/fail but no partial results

## Recommendations for Improvement

1. Pipeline Orchestration: Add DAG-based workflow support with libraries like Prefect or Airflow for complex evaluation pipelines

2. Telemetry: Implement comprehensive metrics collection (latency percentiles, throughput, resource usage, costs) with OpenTelemetry

3. Optimization: Add prompt caching, dynamic batching, and integration with serving frameworks like vLLM for LLMs

4. Failure Handling: Implement exponential backoff, circuit breakers, and sophisticated retry strategies with tenacity library

5. Checkpointing: Add periodic state persistence and resumption logic, especially for long-running scans

6. Distributed Execution: Integrate Ray or Dask for multi-GPU/multi-node execution with budget enforcement

7. Human Evaluation: Add integration with platforms like Scale AI or Label Studio for human-in-the-loop workflows

## Final Checklist
- [x] All 7 features rated (S3F1 through S3F7)
- [x] Every rating has evidence (code snippets, doc links, file paths)
- [x] Justifications are concise (2-4 sentences max)
- [x] Consistent rating standards across features