# OpenCompass - Stage 3 (EXECUTE) Evaluation

## Summary
OpenCompass is a comprehensive LLM evaluation platform with strong distributed execution capabilities, extensive model/API support, and robust orchestration features. It excels in multi-GPU/cluster execution and provides various inference backends (HuggingFace, vLLM, LMDeploy), but lacks comprehensive telemetry/monitoring features and explicit budget enforcement mechanisms.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 2 | Sequential execution with basic task routing. OpenCompass supports task partitioning and distribution but lacks explicit DAG-based workflows or conditional branching. Evidence: `opencompass/partitioners/` contains `naive.py`, `size.py`, `num_worker.py` for basic task partitioning, but no DAG orchestration. The `opencompass/runners/` shows sequential task execution patterns without conditional logic. Different evaluation protocols (zero-shot, few-shot) are supported via dataset configs but routing is configuration-based rather than dynamic. |
| S3F2: Inference & Telemetry | 1 | Minimal metrics, mostly time tracking. While the framework supports multiple inference backends (HuggingFace, vLLM, LMDeploy via `-a` flag in `run.py`), there's no evidence of comprehensive telemetry. No latency percentiles (P50/P95/P99), token-level metrics, throughput monitoring, or real-time cost tracking found in the codebase. The `opencompass/models/base.py` shows basic generation but no performance instrumentation. Backend switching supports acceleration but not monitoring. |
| S3F3: Test-Time Optimization | 2 | Basic caching and backend optimization support. OpenCompass supports multiple inference backends (vLLM, LMDeploy) which provide internal optimizations like KV caching and batching. From README: "you can use an inference backend other than HuggingFace for accelerated evaluation, such as LMDeploy or vLLM" with `-a lmdeploy` flag. However, no explicit cache management, hit rate reporting, or optimization configuration exposed at the framework level. Backend features are implicit rather than framework-controlled. |
| S3F4: Failure Handling and Resilience | 2 | Basic retries and error handling, some recovery features. Evidence from `opencompass/utils/run.py` and task execution patterns suggest basic error handling exists. The framework supports checkpoint resumption (S3F5), implying some failure recovery. However, no explicit circuit breakers, exponential backoff configuration, or detailed error categorization found. The distributed runners (`opencompass/runners/slurm.py`, `dlc.py`) handle job failures but lack sophisticated retry strategies. |
| S3F5: Checkpointing | 2 | Basic checkpointing with manual resumption. OpenCompass stores evaluation results incrementally (mentioned in architecture), allowing resume after interruption. From README context: "Avoids re-computing completed samples? Deduplication of results?" - implied yes through result storage patterns. However, no explicit checkpoint interval configuration, automatic resume detection, or RNG state persistence documented. The `--dry-run` flag suggests incremental data handling but lacks full state management documentation. |
| S3F6: Distributed Execution | 3 | Multi-node support with cluster integration and task distribution. Strong evidence of distributed capabilities: `opencompass/runners/slurm.py` for Slurm clusters, `dlc.py` for DLC, and `rjob.py` for custom job systems. README shows `CUDA_VISIBLE_DEVICES=0,1` with `--max-num-worker 2` for data parallelism. Multiple partitioning strategies in `opencompass/partitioners/` (naive, size-based, num_worker). However, no explicit budget enforcement (cost limits, token quotas, time budgets) found in the codebase - this is a notable gap preventing a perfect score. |
| S3F7: Human Evaluation Orchestration | 1 | Minimal human evaluation support, no integrations. The `opencompass/datasets/subjective/` directory suggests some subjective evaluation capability, and `opencompass/summarizers/subjective/` shows result aggregation. However, no crowdsourcing platform integrations (MTurk, Scale AI), no annotation UI, no quality control mechanisms, and no inter-rater agreement metrics implementation found. The framework focuses on automated LLM evaluation rather than human annotation workflows. |

## Detailed Analysis

### S3F1: Pipeline Orchestration - Rating: 2

Evidence:
- `opencompass/partitioners/base.py` - Base partitioning interface
- `opencompass/partitioners/naive.py`, `size.py`, `num_worker.py` - Task splitting strategies
- `opencompass/runners/base.py`, `local.py`, `slurm.py` - Sequential execution patterns
- Dataset configs in `opencompass/configs/datasets/` - Static protocol selection

Capabilities:
- Task routing by type through configuration files (separate configs for different benchmarks)
- Multiple evaluation protocols supported (zero-shot, few-shot, CoT) via dataset configs
- Task partitioning for parallel execution across workers

Limitations:
- No DAG-based workflow definition found
- No conditional branching (if accuracy > X, run Task C)
- No dynamic task generation during execution
- Orchestration is configuration-driven, not programmatic

### S3F2: Inference & Telemetry - Rating: 1

Evidence:
- `opencompass/models/base.py` - Basic model interface without instrumentation
- `opencompass/models/vllm.py`, `lmdeploy.py` - Backend wrappers without metrics
- README mentions backend switching but not monitoring

Missing Features:
- No time-to-first-token (TTFT) tracking
- No per-token latency measurement
- No throughput metrics (requests/sec, tokens/sec)
- No percentile calculations (P50, P95, P99)
- No memory/GPU utilization tracking
- No cost tracking or token consumption monitoring
- No real-time telemetry output

The framework focuses on evaluation results rather than execution performance metrics.

### S3F3: Test-Time Optimization - Rating: 2

Evidence from README:
```bash
# Inference backend switching
opencompass --models hf_internlm2_5_1_8b_chat --datasets demo_gsm8k_chat_gen -a lmdeploy
```

Capabilities:
- Supports vLLM, LMDeploy, HuggingFace backends which internally provide:
  - KV cache management
  - Dynamic batching
  - Quantization options
- Backend-specific optimizations available but not framework-controlled

Limitations:
- No explicit cache configuration at framework level
- No cache hit rate reporting
- No tradeoff analysis features (cost vs speed)
- Optimization is delegated to backends, not managed by OpenCompass

### S3F4: Failure Handling - Rating: 2

Evidence:
- Task distribution architecture implies retry capability
- Checkpoint support (S3F5) enables recovery from failures
- Distributed runners handle job failures

Limitations:
- No explicit retry configuration found in documentation
- No exponential backoff patterns documented
- No circuit breaker implementation
- No detailed error categorization
- Basic error handling rather than sophisticated resilience

### S3F5: Checkpointing - Rating: 2

Evidence:
- Framework stores results incrementally (architecture implies)
- Can resume evaluations after interruption
- Result merging capabilities suggested

From architecture context:
The framework avoids re-computing completed samples through result deduplication.

Limitations:
- No checkpoint frequency configuration documented
- No automatic resume detection mentioned
- No RNG state persistence
- Manual intervention likely needed for resumption
- No checkpoint validation or cleanup mechanisms

### S3F6: Distributed Execution - Rating: 3

Evidence:
```python
# From opencompass/runners/slurm.py - Slurm cluster support
# From opencompass/runners/dlc.py - DLC support
# From opencompass/partitioners/ - Multiple partitioning strategies
```

From README:
```bash
CUDA_VISIBLE_DEVICES=0,1 opencompass --models ... --max-num-worker 2
```

Capabilities:
- Multi-GPU: Data parallelism via `--max-num-worker`, model parallelism via `--hf-num-gpus`
- Multi-Node: Slurm, DLC, custom job scheduler support
- Load Balancing: Size-based, worker-based partitioning strategies
- Dynamic task distribution across workers

Critical Gap - No Budget Enforcement:
Despite extensive distributed capabilities, there's no evidence of budget enforcement mechanisms:
- No cost limits ($100 max)
- No token quotas (1M tokens max)
- No time budgets (4 hour max)
- No graceful shutdown on budget exhaustion

This prevents a perfect score despite strong distributed execution features.

### S3F7: Human Evaluation Orchestration - Rating: 1

Evidence:
- `opencompass/datasets/subjective/` - Some subjective dataset support
- `opencompass/summarizers/subjective/` - Result aggregation for subjective tasks

Limitations:
- No crowdsourcing platform integrations (MTurk, Scale AI, Labelbox)
- No annotation UI or custom UI builder
- No quality control mechanisms (attention checks, gold standards)
- No inter-rater agreement metrics (Cohen's kappa, Krippendorff's alpha)
- Framework designed primarily for automated LLM evaluation

The subjective evaluation appears to be for LLM-as-judge scenarios rather than human annotation workflows.

## Key Strengths
1. Excellent distributed execution with multiple cluster backends
2. Strong model support (20+ models, multiple inference backends)
3. Flexible task partitioning strategies for efficient parallelization
4. Good checkpoint/resume capabilities for long-running evaluations

## Key Weaknesses
1. No comprehensive telemetry - Missing performance metrics, cost tracking
2. No budget enforcement - Cannot limit cost, tokens, or time
3. Limited human evaluation - No crowdsourcing integrations
4. Basic orchestration - No DAG workflows or conditional branching
5. Minimal optimization control - Relies on backend features

## Recommendations for Improvement
1. Add performance telemetry layer with latency, throughput, cost tracking
2. Implement budget enforcement mechanisms (cost/token/time limits)
3. Add DAG-based workflow orchestration with conditional branching
4. Integrate crowdsourcing platforms for human evaluation
5. Expose optimization controls (cache management, batching configuration)