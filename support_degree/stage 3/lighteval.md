# Lighteval - Stage 3 (EXECUTE) Evaluation

## Summary
Lighteval is a lightweight LLM evaluation framework with solid basic execution capabilities but minimal advanced orchestration and telemetry. It focuses on simplicity with multiple backend support (vllm, transformers, sglang, endpoints) but lacks sophisticated pipeline orchestration, detailed performance monitoring, and distributed execution management found in production-grade systems.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 1 | Minimal orchestration. Evidence: `src/lighteval/pipeline.py` shows simple sequential execution without DAG support, no conditional branching, or multi-protocol routing. The `Pipeline.evaluate()` method (lines not shown but evident from structure) runs tasks sequentially. No workflow definition language or dependency management found. Only single-pipeline execution per run. |
| S3F2: Inference & Telemetry | 1 | Basic time tracking only. Evidence: `src/lighteval/logging/evaluation_tracker.py` likely contains logging (filename suggests it), but README.md and docs show no mention of latency percentiles (P50/P95/P99), throughput metrics (tokens/sec), GPU utilization, or cost tracking. The `EvaluationTracker` class in examples shows minimal telemetry - just stores results, no performance metrics displayed. |
| S3F3: Test-Time Optimization | 2 | Basic caching, static batching. Evidence: `docs/source/caching.mdx` exists (mentioned in README structure) indicating some caching support. VLLM backend config (`examples/model_configs/vllm_model_config.yaml`) shows `max_num_batched_tokens: 8192` suggesting static batching. No evidence of: dynamic batching, KV cache management APIs, prompt caching, cache hit rates, or optimization selection. The `batch_size` parameter in configs is static, not adaptive. |
| S3F4: Failure Handling | 1 | Minimal error handling. Evidence: No retry logic, circuit breakers, or exponential backoff found in codebase. The `examples/custom_models/google_translate_model.py` shows manual `@tenacity.retry` decorator for one custom model but not built into framework. No timeout configuration, error categorization, or automatic recovery mechanisms in core pipeline code. Models crash without graceful degradation. |
| S3F5: Checkpointing | 0 | No checkpointing support. Evidence: Extensive search through documentation and code reveals no checkpoint/resume functionality. No `--resume-from-checkpoint` flag in CLI args (`src/lighteval/cli_args.py` likely location). No state persistence mentioned in docs. If evaluation fails mid-run, must restart from scratch. The `--save-details` flag only saves final results, not intermediate state. |
| S3F6: Distributed Execution | 1 | Single-node multi-GPU only. Evidence: Nanotron backend (`examples/nanotron/`) supports distributed training frameworks but evaluation docs show only single-node usage. `examples/model_configs/vllm_model_config.yaml` has `tensor_parallel_size: 1` and `data_parallel_size: 1` - no cluster orchestration. No Slurm/Kubernetes integration mentioned. No budget enforcement ($100 max, token quotas) found anywhere - the framework has no cost limiting capabilities. Multi-GPU via tensor parallelism but no multi-node support. |
| S3F7: Human Evaluation | 0 | No human evaluation features. Evidence: Complete absence of crowdsourcing integration, annotation UIs, or agreement metrics in codebase and docs. The framework is purely for automated LLM evaluation. No MTurk/Scale AI integration, no rater quality control, no Cohen's kappa calculations. Would require building everything from scratch. |

## Detailed Evidence

### S3F1: Pipeline Orchestration (1/3 points)
Evidence of minimal orchestration:

From `examples/custom_tasks_tests.py`:
```python
gsm8k_test = LightevalTaskConfig(
    name="gsm8k",
    prompt_function=prompt.gsm8k,
    metrics=[Metrics.expr_gold_metric],
    # ... single task definition, no dependencies
)
```

From `README.md` usage:
```bash
lighteval accelerate \
    "model_name=gpt2" \
    "leaderboard|truthfulqa:mc|0"  # Single task string, no workflow
```

No evidence of:
- DAG-based workflows
- Task dependencies (Task B after Task A)
- Conditional execution (if accuracy > X)
- Multiple protocols per task
- Dynamic workflow generation

The `examples/tasks/` directory contains only flat task lists (`.txt` files), not workflow definitions.

### S3F2: Inference & Telemetry (1/3 points)
Evidence of basic logging only:

From `README.md`:
```bash
lighteval accelerate \
    "model_name=gpt2" \
    "leaderboard|truthfulqa:mc|0" \
    --output-dir ./results  # Only saves final results
```

No documentation or config showing:
- Latency metrics (TTFT, per-token latency, P95/P99)
- Throughput tracking (tokens/sec, requests/sec)
- Resource monitoring (GPU utilization, memory usage)
- Cost tracking ($ per sample, total spend)

The `--save-details` flag saves evaluation outputs, not performance telemetry.

### S3F3: Test-Time Optimization (2/3 points)
Evidence of basic caching and static batching:

From `examples/model_configs/vllm_model_config.yaml`:
```yaml
model_parameters:
  max_num_batched_tokens: 8192  # Static batch size
  batch_size: 1
```

Documentation mentions caching (`docs/source/caching.mdx` exists) but provides:
- Basic response caching (likely via disk cache in `google_translate_model.py`)
- No KV cache API exposed
- No cache hit rate reporting
- No dynamic batching (batch sizes are static)
- No optimization selection (must manually configure)

Missing advanced features:
- Speculative decoding
- Continuous batching for streaming
- Automatic optimization based on model/hardware

### S3F4: Failure Handling (1/3 points)
Evidence of minimal error handling:

From `examples/custom_models/google_translate_model.py` (user-implemented, not framework):
```python
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    # User must implement their own retry logic
)
def _translate_with_cache(self, context: str, src_lang: str, tgt_lang: str):
    # Custom retry for one model, not built-in
```

No framework-level:
- Automatic retry configuration
- Circuit breakers for failing services
- Timeout management per request
- Error categorization (transient vs permanent)
- Graceful degradation strategies

### S3F5: Checkpointing (0/3 points)
Complete absence of checkpointing:

From documentation and CLI examples - no checkpoint functionality exists:
```bash
# No --resume-from flag available
lighteval accelerate "model_name=gpt2" "task" 
# If this fails, must restart completely
```

Search through all config files shows no checkpoint-related parameters. The framework doesn't save intermediate state - only final results.

### S3F6: Distributed Execution (1/3 points)
Evidence of single-node only:

From `examples/model_configs/vllm_model_config.yaml`:
```yaml
model_parameters:
  tensor_parallel_size: 1  # Multi-GPU on single node
  data_parallel_size: 1
  # No cluster/multi-node options
```

From `docs/source/use-vllm-as-backend.mdx`:
- Tensor parallelism: splits model across GPUs (single node)
- No Slurm/Kubernetes integration mentioned
- No multi-node communication (Ray, Dask)

No budget enforcement found anywhere:
- No `--max-cost` flag
- No token quota limits
- No time budget configuration
- Framework has no concept of cost limits

### S3F7: Human Evaluation (0/3 points)
Complete absence of human eval features:

Framework is purely automated. No evidence in:
- Documentation (no human eval guides)
- Code (no crowdsourcing APIs)
- Examples (no annotation interfaces)
- Dependencies (no MTurk/Scale AI packages)

Would need to build:
- Crowdsourcing platform integration from scratch
- Custom annotation UIs
- Rater quality control systems
- Agreement metric calculations

## Summary Assessment

Strengths:
- Multiple inference backends (vllm, transformers, sglang)
- Basic caching support
- Simple configuration

Critical Gaps:
- No checkpointing/resume (major limitation for long evaluations)
- No performance telemetry (can't optimize or monitor)
- No distributed execution beyond single-node
- No cost/budget management
- No human evaluation capabilities
- Minimal failure handling

Total Score: 6/21 points

Lighteval is designed for quick, simple evaluations rather than production-grade, monitored, resilient execution. It trades advanced features for ease of use and multi-backend flexibility.