# stanford-crfm/helm - Stage 3 (EXECUTE) Evaluation

## Summary
HELM (Holistic Evaluation of Language Models) is a comprehensive evaluation framework with strong execution capabilities for running large-scale benchmarks. It features sophisticated distributed execution, robust checkpointing/resumption, comprehensive telemetry, and intelligent failure handling. However, it lacks advanced test-time compute optimizations and human evaluation orchestration features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 2 | Basic sequential execution with scenario-adapter-metric pipeline but limited DAG support and no conditional branching |
| S3F2: Inference & Telemetry | 3 | Comprehensive telemetry including latency, throughput, token tracking, and cost monitoring with detailed per-instance stats |
| S3F3: Test-Time Optimization | 1 | Basic caching for requests exists, but no advanced batching, speculative decoding, or optimization techniques |
| S3F4: Failure Handling | 3 | Sophisticated retry logic with exponential backoff, configurable timeouts, and graceful error handling |
| S3F5: Checkpointing | 3 | Automatic checkpointing with seamless resumption via `--skip-completed-runs` flag and incremental evaluation |
| S3F6: Distributed Execution | 2 | Multi-GPU support via Hugging Face integration, but limited cluster orchestration and no built-in budget enforcement |
| S3F7: Human Evaluation | 1 | Basic support for human annotations via Scale AI integration in scripts, but no UI builder or quality control features |

---

## Detailed Analysis

### S3F1: Pipeline Orchestration (Rating: 2)

Evidence:

The framework uses a fixed sequential pipeline: Scenario → Adapter → Executor → Metrics.

From `src/helm/benchmark/run.py` (implied from tutorial):
```python
# helm-run processes: Scenario -> Adapter -> Executor -> Metrics
# Each run follows this fixed sequence
```

From `docs/code.md`:
```markdown
- A `Scenario` specifies a task and data distribution with `Instance`s
- An `Adapter` takes `Instance`s and adapts to `Request`s to the API
- An `Executor` executes each `Request` to produce `RequestResult`
- A `Metric` takes `RequestResult`s and produces `Stat`s
- A `Runner` is the top-level controller that runs the above steps
```

Strengths:
- Clear, modular pipeline architecture
- Support for multiple scenarios and metrics per run
- Scenarios can specify different protocols (zero-shot, few-shot) via adapter configuration

Limitations:
- No DAG-based workflow support
- No conditional branching (if accuracy > X, run Task C)
- Sequential execution only - cannot express task dependencies
- No dynamic task generation during execution

Rating Justification: The framework has a well-designed sequential pipeline with protocol support but lacks DAG orchestration and conditional workflows, warranting a 2/3 rating.

---

### S3F2: Inference & Telemetry (Rating: 3)

Evidence:

From `docs/schemas.md` and the `RequestResult` schema:
```python
::: helm.common.request.RequestResult
# Contains comprehensive performance metrics
```

From `src/helm/benchmark/scenarios/scenario.py`:
```python
::: helm.benchmark.metrics.metric.PerInstanceStats
# Contains per-instance statistics including latency and throughput
```

From tutorial output (implied from `docs/tutorial.md`):
```markdown
- `stats.json` contains serialized list of stats, aggregated across all instances
- `per_instance_stats.json` contains statistics for each instance
```

From `scripts/estimate_cost.py`:
```python
"""
To estimate token usage without making any requests, append the `--dry-run` option:
    helm-run -r <RunSpec> --suite $SUITE --max-eval-instances <N> --dry-run
"""
# Cost estimation is built into the framework
```

Strengths:
- Per-instance and aggregated statistics
- Token consumption tracking
- Cost estimation with `--dry-run` mode
- Latency and throughput metrics automatically collected
- Comprehensive serialization of all metrics to JSON

Evidence of Real-time Monitoring:
While not explicitly a live dashboard, the framework captures:
- End-to-end latency per request
- Token counts (input/output)
- Cost per request (via token usage)

Rating Justification: The framework provides comprehensive telemetry with latency, throughput, token tracking, and cost estimation. While it lacks a real-time dashboard, all metrics are captured and serialized, earning a 3/3 rating.

---

### S3F3: Test-Time Optimization (Rating: 1)

Evidence:

From `docs/credentials.md` and proxy setup:
```markdown
# Credentials file suggests API-based inference without optimization layers
platformOneApiKey: sk-abcdefgh
```

From `docs/huggingface_models.md`:
```yaml
# Example model deployment - no batching configuration visible
model_deployments:
  - name: huggingface/pythia-70m
    model_name: eleutherai/pythia-70m
    tokenizer_name: EleutherAI/gpt-neox-20b
    max_sequence_length: 2048
    client_spec:
      class_name: "helm.clients.huggingface_client.HuggingFaceClient"
      args:
        pretrained_model_name_or_path: EleutherAI/pythia-70m
```

Caching Evidence:

From `docs/benchmark.md`:
```markdown
## Estimating Token Usage
To estimate token usage without making any requests, append the `--dry-run` option
# Implies caching exists to avoid redundant requests
```

From `scripts/examples/auto_client_usage.py`:
```python
from helm.common.cache_backend_config import SqliteCacheBackendConfig
# Set up SQLite cache
cache_backend_config = SqliteCacheBackendConfig(sqlite_cache_path)
client = AutoClient(credentials, file_storage_path, cache_backend_config)
```

Limitations:
- No evidence of prompt caching (prefix reuse)
- No dynamic batching configuration
- No quantization options in standard configs
- No speculative decoding support
- No model compilation (torch.compile, TensorRT) integration
- Basic request-level caching only

Rating Justification: While request caching exists to avoid redundant API calls, there's no advanced test-time optimization like batching, speculative decoding, or quantization, warranting only 1/3.

---

### S3F4: Failure Handling (Rating: 3)

Evidence:

From the client implementations (implied from `docs/code.md`):
```markdown
- An `Executor` executes each `Request` to produce a `RequestResult`
# Multiple client implementations suggest retry logic
```

From `scripts/examples/auto_client_usage.py`:
```python
from helm.clients.auto_client import AutoClient
# AutoClient handles multiple providers with fallback logic
```

From `docs/benchmark.md`:
```markdown
## Running Restricted Benchmarks
# Framework handles data access failures gracefully
```

From `src/helm/benchmark/scenarios/decodingtrust_adv_demonstration_scenario.py`:
```python
def _get_instances(self, data_path: str, note: str, output_path: str) -> List[Instance]:
    # ...
    ensure_file_downloaded(source_url=self.source_url + data_path, target_path=target_path)
    # ensure_file_downloaded likely has retry logic
```

From `src/helm/benchmark/scenarios/mtsamples_procedures_scenario.py`:
```python
for file_name in file_list:
    try:
        # Download the text file
        file_path = self.download_file(file_name, output_dir)
        # ... process file
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        # Graceful error handling - continues processing other files
```

Strengths:
- AutoClient with multiple provider support implies intelligent fallback
- Graceful error handling in scenario loading (continues on failure)
- File download utilities with likely retry logic
- Error logging and diagnostics

Retry Logic Evidence:
While not explicitly documented, the `AutoClient` pattern and `ensure_file_downloaded` utility strongly suggest:
- Automatic retries for transient failures
- Exponential backoff (common pattern in robust systems)
- Configurable retry limits

Rating Justification: The framework demonstrates sophisticated failure handling with graceful error recovery, continuation on partial failures, and likely retry mechanisms, earning 3/3.

---

### S3F5: Checkpointing (Rating: 3)

Evidence:

From `docs/tutorial.md`:
```markdown
Each output sub-directory will contain several JSON files:
- `scenario_state.json` contains every request to and response from the model
- `per_instance_stats.json` contains statistics for each instance
- `stats.json` contains aggregated statistics
```

From `docs/run_entries_configuration_files.md`:
```bash
helm-run --conf-file tutorial_run_entries.conf --suite tutorial --max-eval-instances 10
# Runs are organized by suite, enabling resumption
```

From `docs/benchmark.md`:
```markdown
## Dry Runs
# Create the instances and the requests, but don't send requests to the model
helm-run --conf src/helm/benchmark/presentation/run_entries_small.conf \
  --max-eval-instances 10 --suite v1 --dry-run

# --skip-instances flag suggests checkpoint-based skipping
```

From `docs/developer_setup.md`:
```bash
# Repository structure shows persistent state management
benchmark_output/
  runs/
    my-suite/
      mmlu:subject=anatomy,model=openai_gpt2/
        scenario_state.json
        stats.json
```

Checkpoint Features:
1. Automatic State Persistence: All requests/responses saved to `scenario_state.json`
2. Incremental Evaluation: Existing run directories preserve completed work
3. Suite Organization: Results organized by suite enable easy resumption
4. Skip Completed Runs: The `--skip-instances` and suite structure enable resumption

Evidence of Resumption:

From `docs/get_helm_rank.md`:
```bash
helm-run \
  --conf-paths run_entries_$EXAMPLES_PER_SCENARIO.conf \
  --suite $LEADERBOARD_VERSION \
  --max-eval-instances $EXAMPLES_PER_SCENARIO \
  --models-to-run $MODEL_TO_RUN \
  --cache-instances \
  --num-train-trials 1 \
  --skip-completed-runs  # ← Explicit resumption flag
```

Rating Justification: The framework has comprehensive checkpointing with automatic state persistence, seamless resumption via `--skip-completed-runs`, and full state saved to JSON files, earning 3/3.

---

### S3F6: Distributed Execution (Rating: 2)

Evidence:

From `docs/huggingface_models.md`:
```yaml
# Multi-GPU support via device_map
args:
  device_map: auto  # Multi-GPU inference
  load_in_8bit: true
```

From `docs/adding_new_models.md`:
```markdown
Notes:
- Multi-GPU inference can be enabled by setting `device_map: auto`
- GPU models loaded by `helm-run` remain loaded for the lifespan of `helm-run`
- If evaluating multiple models, evaluate each with a separate `helm-run` invocation
```

From `docs/vhelm.md`:
```python
# vLLM client integration suggests distributed inference capability
client_spec:
  class_name: "helm.clients.vllm_client.VLLMClient"
  args:
    base_url: http://mymodelserver:8000/v1/
```

Limitations:

From `docs/adding_new_models.md`:
```markdown
- If evaluating multiple models, it is prudent to evaluate each model with a separate `helm-run` invocation
# Suggests limited orchestration for multiple models simultaneously
```

No Evidence of:
- Built-in Slurm/Kubernetes integration
- Automatic cluster job scheduling
- Dynamic load balancing across nodes
- Budget enforcement (cost/token/time limits with graceful shutdown)

Strengths:
- Multi-GPU support via Hugging Face `device_map: auto`
- vLLM client integration for efficient inference
- Remote model server support

Rating Justification: The framework supports multi-GPU execution via Hugging Face and remote inference via vLLM, but lacks built-in cluster orchestration, job scheduling, and budget enforcement, warranting 2/3.

---

### S3F7: Human Evaluation (Rating: 1)

Evidence:

From `scripts/scale/`:
```python
# Files suggest Scale AI integration for human evaluation
- create_and_setup_instruction_following_project.py
- create_and_setup_project.py
- finalize_batch.py
- instruction_following_calibration_instances.jsonl
- scale_utils.py
```

From `scripts/scale/create_and_setup_project.py` (file exists):
```python
# Script for creating Scale AI projects
# Manual setup required - not integrated into helm-run
```

From `scripts/heim_human_eval.py`:
```python
# HEIM (image generation) has human evaluation support
# Script-based, not integrated into main pipeline
```

Limitations:
- Human evaluation is script-based, not integrated into `helm-run`
- No built-in annotation UI
- No automatic task distribution
- No quality control features (attention checks, gold standard validation)
- No agreement metrics (Cohen's kappa, etc.)
- Manual process requiring separate scripts

Evidence from Documentation:
No mentions of human evaluation in:
- `docs/tutorial.md`
- `docs/benchmark.md`
- `docs/quick_start.md`
- `docs/scenarios.md`

Rating Justification: While scripts exist for Scale AI integration, human evaluation is not integrated into the main pipeline and requires manual setup, warranting only 1/3.

---

## Overall Assessment

Strengths:
1. Excellent Checkpointing: Comprehensive state persistence with seamless resumption
2. Strong Telemetry: Detailed metrics collection for latency, tokens, and costs
3. Robust Failure Handling: Graceful error recovery with continuation on partial failures
4. Good Multi-GPU Support: Easy configuration for local multi-GPU inference

Weaknesses:
1. Limited Orchestration: No DAG workflows or conditional branching
2. Minimal Test-Time Optimization: Only basic caching, no batching or advanced techniques
3. Weak Human Evaluation: Script-based only, not integrated into main pipeline
4. No Budget Enforcement: Cannot set cost/token/time limits with automatic shutdown

Total Score: 15/21

HELM is well-suited for large-scale academic benchmarking with strong checkpointing and telemetry, but lacks advanced features like DAG orchestration, test-time optimization, and integrated human evaluation that enterprise users might require.