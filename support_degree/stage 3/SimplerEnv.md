# SimplerEnv - Stage 3 (EXECUTE) Evaluation

## Summary
SimplerEnv is a simulation-based evaluation framework for robotic manipulation policies, not a general-purpose LLM evaluation framework. It focuses on executing robotic policies in simulated environments with emphasis on visual matching and variant aggregation evaluation. The framework has minimal execution orchestration capabilities, basic telemetry, and no test-time optimization or resilience features typical of LLM evaluation frameworks. It's designed for single-shot policy rollouts rather than comprehensive evaluation pipelines.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No orchestration features exist. The framework executes single policy rollouts sequentially through bash scripts without DAG support, task routing, or protocol management. Evidence: `scripts/*.sh` files show simple sequential execution with no workflow orchestration. |
| S3F2: Inference & Telemetry | 1 | Minimal metrics tracking. Basic episode statistics are logged (`episode_stats` in `simpler_env/__init__.py:42`), but there's no comprehensive telemetry for latency, throughput, resource consumption, or cost tracking. Only success/failure and basic environment metrics. |
| S3F3: Test-Time Optimization | 0 | No optimization features. The framework performs direct policy inference without caching, batching, or any computational optimization. All inference is done sequentially per episode. |
| S3F4: Failure Handling | 0 | No failure handling mechanisms. Scripts execute linearly with no retry logic, timeout management, circuit breakers, or error recovery. Failures would require manual intervention and re-execution. |
| S3F5: Checkpointing | 0 | No checkpointing support. Each evaluation run is independent with no ability to save progress or resume from interruptions. Episodes must be re-executed from scratch if interrupted. |
| S3F6: Distributed Execution | 0 | No distributed execution capabilities. All evaluations run on a single GPU/device specified by `CUDA_VISIBLE_DEVICES`. No multi-GPU, multi-node, or budget enforcement features exist. |
| S3F7: Human Evaluation | 0 | No human evaluation features. The framework is purely automated simulation-based evaluation with no crowdsourcing integration, annotation interfaces, or agreement metrics. |

Total Score: 1/21 (4.8%)

---

## Detailed Feature Analysis

### S3F1: Pipeline Orchestration (0/3 points)

Evidence:
```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
for coke_can_option in "${coke_can_options_arr[@]}";
do for ckpt_path in "${arr[@]}";
do CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path} \
  --robot google_robot_static \
  --control-freq 3 --sim-freq 513 --max-episode-steps 80 \
  --env-name ${env_name} --scene-name ${scene_name} \
  --robot-init-x 0.35 0.35 1 --robot-init-y 0.20 0.20 1 --obj-init-x -0.35 -0.12 5 --obj-init-y -0.02 0.42 5
```

Justification:
The framework uses simple bash scripts with nested loops for orchestration. There is no DAG-based workflow support, task routing, protocol selection, or dynamic workflows. Each evaluation is a sequential execution of independent policy rollouts with no dependencies or conditional branching at the framework level. The scripts merely iterate over parameter combinations without any intelligent orchestration.

Rating: 0 points - No orchestration features beyond basic sequential execution.

---

### S3F2: Model Inference with Performance Telemetry (1/3 points)

Evidence:
```python
# simpler_env/__init__.py
episode_stats = info.get('episode_stats', {})
print("Episode stats", episode_stats)
```

Justification:
The framework provides only basic episode-level statistics through the environment's info dict. There is no comprehensive telemetry for:
- Latency metrics (TTFT, per-token latency, percentiles)
- Throughput measurements (requests/sec, tokens/sec)
- Resource consumption (memory, GPU utilization)
- Cost tracking

The minimal logging captures success/failure and basic environment metrics, but lacks the detailed performance monitoring needed for optimization or analysis.

Rating: 1 point - Minimal metrics, mostly episode outcome tracking.

---

### S3F3: Test-Time Compute Optimization (0/3 points)

Evidence:
```python
# simpler_env/__init__.py
while not (done or truncated):
   image = get_image_from_maniskill2_obs_dict(env, obs)
   action = env.action_space.sample() # replace this with your policy inference
   obs, reward, done, truncated, info = env.step(action)
```

Justification:
The framework performs direct, sequential policy inference with no optimization techniques:
- No prompt/response caching
- No batching (dynamic or static)
- No speculative decoding or quantization
- No model compilation

Each step executes independently with fresh computation, suitable for simulation accuracy but lacking any performance optimization.

Rating: 0 points - No optimization features.

---

### S3F4: Failure Handling and Resilience (0/3 points)

Evidence:
Examining all scripts and main inference code reveals no error handling:
```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
do CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path} \
  --robot google_robot_static \
  # ... no error handling, retries, or fallback
done
```

Justification:
The framework has no failure handling mechanisms:
- No automatic retry logic or exponential backoff
- No timeout management
- No circuit breakers for failing services
- No graceful error recovery or request rescheduling

Failures in policy inference or environment execution would cause the script to exit or hang, requiring manual intervention.

Rating: 0 points - No failure handling.

---

### S3F5: Progress Checkpointing and Resumption (0/3 points)

Evidence:
No checkpointing code exists in the repository. Each evaluation is independent:
```python
# simpler_env/__init__.py
env = gym.make(env_name, env_kwargs)
return env
```

Justification:
The framework does not support:
- Automatic or manual checkpointing
- Resumption from partial evaluations
- Incremental evaluation avoiding re-computation
- State persistence beyond video outputs

If an evaluation run is interrupted, all progress is lost and episodes must be re-executed from the beginning.

Rating: 0 points - No checkpointing.

---

### S3F6: Distributed Execution and Resource Management (0/3 points)

Evidence:
```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
gpu_id=0
CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py
```

Justification:
The framework only supports single-device execution:
- No multi-GPU data/model parallelism
- No multi-node cluster support (Slurm, Kubernetes)
- No load balancing or dynamic task distribution
- No budget enforcement (cost, token, or time limits)

While users can manually run scripts on different GPUs, there's no framework-level support for distributed execution or resource management.

Rating: 0 points - Single-device only.

---

### S3F7: Human Evaluation Orchestration (0/3 points)

Evidence:
The README explicitly states it's simulation-based:
```markdown
# README.md
We propose employing physical simulators as efficient, scalable, and informative 
complements to real-world evaluations.
```

Justification:
The framework has no human evaluation features:
- No crowdsourcing platform integration (MTurk, Scale AI, etc.)
- No annotation interfaces or UI builders
- No quality control mechanisms
- No inter-rater agreement metrics

It's designed purely for automated simulation-based evaluation of robotic policies against ground truth.

Rating: 0 points - No human evaluation features.

---

## Overall Assessment

SimplerEnv is not designed as an LLM evaluation framework and should not be evaluated against these criteria. It's a specialized robotics simulation evaluation tool with a completely different purpose:

Actual Purpose:
- Simulate real-world robot manipulation tasks
- Evaluate vision-based robotic policies (RT-1, Octo)
- Provide visual matching and variant aggregation evaluation setups
- Validate sim-to-real transfer for robotics research

Why Low Scores Are Expected:
1. Domain mismatch: Evaluates robotic policies, not language models
2. Single-shot execution: Designed for episode rollouts, not batch evaluation
3. Simulation focus: Emphasizes physical accuracy over execution optimization
4. Research tool: Built for robotics researchers, not production ML evaluation

What It Does Well (outside these criteria):
- Comprehensive robot simulation environments
- Visual matching for real-to-sim evaluation
- System identification for robot parameter tuning
- Integration with real robot datasets (Bridge, RT-1)

This framework receives a score of 1/21 (4.8%) because it fundamentally serves a different purpose than general LLM evaluation frameworks. The single point comes from minimal episode-level logging, which is appropriate for its robotics simulation use case but insufficient for comprehensive LLM evaluation needs.