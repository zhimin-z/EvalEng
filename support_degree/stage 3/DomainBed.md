# DomainBed - Stage 3 (EXECUTE) Evaluation

## Summary
DomainBed is a PyTorch-based research benchmark for domain generalization, not an LLM evaluation framework. It focuses on training and evaluating computer vision models across different domains. Since it lacks fundamental LLM evaluation execution capabilities (no LLM inference, no prompt execution, no LLM-specific metrics), most Stage 3 features are not applicable. The framework does provide basic ML experiment execution features like training loops, checkpointing, and distributed execution, but these are designed for vision model training rather than LLM evaluation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No evaluation pipeline orchestration exists. The framework provides training scripts (`domainbed/scripts/train.py`, `domainbed/scripts/sweep.py`) for ML model training, not LLM evaluation workflows. There's no task routing, no DAG-based workflows, no protocol support (zero-shot, few-shot), and no conditional branching. Example from `train.py` shows it's a simple training loop for vision models with fixed data loading and forward passes, not a flexible evaluation orchestration system. |
| S3F2: Inference & Telemetry | 0 | No inference telemetry for LLM evaluation. The training scripts in `domainbed/scripts/train.py` log basic metrics like accuracy and loss (`env0_in_acc`, `env0_out_acc`, `loss`, `step_time`) but lack LLM-specific telemetry: no TTFT, no per-token latency, no throughput metrics (tokens/second), no cost tracking. The output format in test files (e.g., `domainbed/misc/test_sweep_data/*/out.txt`) shows only epoch-based training metrics, not inference performance monitoring. |
| S3F3: Test-Time Optimization | 0 | No test-time compute optimization features. The codebase has no caching mechanisms (no prompt caching, no KV cache management), no batching strategies beyond basic DataLoader batching, no speculative decoding, no quantization support. The `domainbed/lib/fast_data_loader.py` provides basic data loading utilities but nothing related to LLM inference optimization. |
| S3F4: Failure Handling | 0 | No robust failure handling mechanisms. There are no retry strategies, no exponential backoff, no circuit breakers, and no sophisticated error recovery. The command launchers in `domainbed/command_launchers.py` (local, multi_gpu) provide basic subprocess management but don't implement failure resilience patterns. No timeout management or request rescheduling evident in the codebase. |
| S3F5: Checkpointing | 1 | Minimal checkpointing support. The training script (`domainbed/scripts/train.py`) includes basic checkpoint saving with `--checkpoint_freq` parameter and `--save_model_every_checkpoint` flag. However, there's no evidence of automatic resumption from checkpoints, no incremental evaluation support, and no state persistence beyond model weights. The `--skip_model_save` flag suggests optional checkpoint saving but not a robust checkpoint/resume system for long-running evaluations. |
| S3F6: Distributed Execution | 1 | Single-node multi-GPU only. The `command_launchers.py` file shows a `multi_gpu_launcher` that distributes commands across GPUs using `CUDA_VISIBLE_DEVICES`, but this is limited to single-node execution. No multi-node cluster support (no Slurm, Kubernetes), no sophisticated load balancing, and crucially no budget enforcement (no cost limits, token quotas, or time budgets). The launcher simply cycles through available GPUs without resource management. |
| S3F7: Human Evaluation | 0 | No human evaluation features. The framework is entirely focused on automated metrics for vision models (accuracy on different domains). There's no crowdsourcing integration, no annotation interfaces, no quality control mechanisms, and no agreement metrics for human evaluators. The `model_selection.py` file shows only automated validation strategies (IID, LeaveOneOut, Oracle). |

## Evidence Details

### S3F1: Pipeline Orchestration (0 points)
Evidence from `domainbed/scripts/train.py`:
```python
# Simple training loop, not evaluation orchestration
for step in range(start_step, n_steps):
    step_start_time = time.time()
    minibatches_device = [(x.to(device), y.to(device))
        for x,y in next(train_minibatches_iterator)]
    step_vals = algorithm.update(minibatches_device, unlabeled=None)
```
This is a fixed training loop for vision models, not a flexible evaluation pipeline with task routing or protocol selection.

### S3F2: Inference & Telemetry (0 points)
Evidence from test output files:
```txt
# From domainbed/misc/test_sweep_data/8cfbf830754065d02f9723c57abc992e/out.txt
env0_in_acc   env0_out_acc  env1_in_acc   env1_out_acc  env2_in_acc   env2_out_acc  env3_in_acc   env3_out_acc  epoch         loss          step          step_time    
0.7544169611  0.7349823322  0.4640000000  0.4990583804  0.4185072353  0.4344512195  0.4439096631  0.4459259259  0.0000000000  1.6586600542  0             0.8204424381
```
Only basic training metrics (accuracy, loss, step time), no LLM inference telemetry.

### S3F3: Test-Time Optimization (0 points)
No relevant code found. The `domainbed/lib/fast_data_loader.py` only provides `FastDataLoader` and `InfiniteDataLoader` classes for training data iteration, not inference optimization.

### S3F4: Failure Handling (0 points)
Evidence from `domainbed/command_launchers.py`:
```python
def multi_gpu_launcher(commands):
    """Launch commands on the local machine, using all GPUs in parallel."""
    # ... simplified ...
    while len(commands) > 0:
        for idx, gpu_idx in enumerate(available_gpus):
            proc = procs_by_gpu[idx]
            if (proc is None) or (proc.poll() is not None):
                cmd = commands.pop(0)
                new_proc = subprocess.Popen(f'CUDA_VISIBLE_DEVICES={gpu_idx} {cmd}', shell=True)
                procs_by_gpu[idx] = new_proc
                break
        time.sleep(1)
```
Simple subprocess management with no retry logic, timeouts, or error handling.

### S3F5: Checkpointing (1 point)
Evidence from command-line arguments:
```python
# From domainbed/scripts/train.py (visible in README)
parser.add_argument('--checkpoint_freq', type=int, default=None)
parser.add_argument('--save_model_every_checkpoint', action='store_true')
parser.add_argument('--skip_model_save', action='store_true')
```
Basic checkpoint saving exists but no automatic resumption or incremental evaluation.

### S3F6: Distributed Execution (1 point)
Evidence from `domainbed/command_launchers.py`:
```python
def multi_gpu_launcher(commands):
    """Launch commands on the local machine, using all GPUs in parallel."""
    available_gpus = [x for x in os.environ['CUDA_VISIBLE_DEVICES'].split(',') if x != '']
    # ... distributes across GPUs but single-node only ...
```
Single-node multi-GPU support only, no cluster orchestration or budget enforcement.

### S3F7: Human Evaluation (0 points)
Evidence from `domainbed/model_selection.py`:
```python
# Only automated selection methods
class IIDAccuracySelectionMethod(SelectionMethod):
    """Picks argmax(mean(env_out_acc for env in train_envs))"""
    
class LeaveOneOutSelectionMethod(SelectionMethod):
    """Picks (hparams, step) by leave-one-out cross validation."""
    
class OracleSelectionMethod(SelectionMethod):
    """Like Selection method which picks argmax(test_out_acc)"""
```
No human evaluation infrastructure whatsoever.

## Critical Limitations for LLM Evaluation

1. Not an LLM Framework: DomainBed is fundamentally designed for computer vision domain generalization research, not LLM evaluation. It trains ResNets and CNNs on image classification tasks.

2. No LLM Inference: There's no code for loading LLMs, managing tokenization, generating text, or handling LLM APIs.

3. No Prompt Management: No prompt templates, no few-shot example selection, no chain-of-thought execution.

4. Vision-Specific Metrics: All metrics are vision-related (accuracy on PACS, VLCS, etc.), not NLP/LLM metrics.

5. Training-Focused: The entire pipeline is built around model training epochs, not evaluation runs across test sets.

## Conclusion

DomainBed receives very low scores across all Stage 3 features because it's a domain generalization research framework for computer vision, not an LLM evaluation harness. While it has some basic ML infrastructure (checkpointing, multi-GPU training), it lacks all the essential components needed for LLM evaluation: no inference orchestration, no LLM-specific telemetry, no prompt execution, and no evaluation protocols. This framework is fundamentally unsuitable for LLM evaluation tasks without a complete rewrite.