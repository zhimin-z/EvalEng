# SimplerEnv - Stage 4 (EVALUATE) Evaluation

## Summary
SimplerEnv is a robotics simulation framework focused on real-to-sim policy evaluation, not a general evaluation framework. It lacks traditional evaluation infrastructure (metric computation, LLM judges, aggregation) and instead provides robotics-specific success detection and trajectory analysis for manipulation policies in simulated environments.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation and Normalization | 1 | Minimal validation - only success/failure checks in environment episodes; no format validation, policy compliance, or normalization features |
| S4F2: Task-Specific Metric Computation | 1 | Only provides success rate and basic statistical comparisons (MMRV, Pearson correlation); lacks standard metric library or per-sample scoring |
| S4F3: Evaluator Model Integration | 0 | No LLM-as-judge, specialized evaluators, or model-based scoring; only rule-based success detection |
| S4F4: Multi-Modal Scoring Protocols | 0 | Visual matching is for environment rendering, not evaluation; no multi-modal metrics or scoring |
| S4F5: Aggregate Statistics and Cross-Model Comparison | 2 | Basic statistics via custom metrics module; provides MMRV and Pearson correlation for model comparison but lacks comprehensive statistical suite |

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 1)

Evidence:

The framework only validates episode success/failure in environments:

From `simpler_env/simple_inference_visual_matching_prepackaged_envs.py`:
```python
done, truncated = False, False
while not (done or truncated):
   action = env.action_space.sample() # replace this with your policy inference
   obs, reward, done, truncated, info = env.step(action)
```

Episode tracking in `simpler_env/__init__.py`:
```python
def make(task_name, kwargs):
    env = gym.make(env_name, env_kwargs)
    return env
```

Missing capabilities:
- No format validation for policy outputs
- No schema validation against expected formats
- No policy compliance checks (harmful content, length constraints)
- No sanity checks for logical consistency
- No normalization of different output formats

Rating: 1 pt - Minimal validation exists (done/truncated episode status), mostly manual through environment step returns.

### S4F2: Task-Specific Metric Computation (Rating: 1)

Evidence:

Limited metrics in `simpler_env/utils/metrics.py`:
```python
def mean_maximum_rank_violation(real_eval_perf, sim_eval_perf):
    # Custom metric for comparing real vs sim performance
    
def pearson_correlation(real_eval_perf, sim_eval_perf):
    # Correlation metric
```

Usage in `tools/calc_metrics.py`:
```python
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF, SIMPLER_PERF

for k in SIMPLER_PERF.keys():
    mmrv = mean_maximum_rank_violation(
        list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
    )
    pearson = pearson_correlation(
        list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
    )
```

Coverage analysis:
- Only 2 custom metrics: MMRV and Pearson correlation
- Success rate computation (implied from episode results)
- No standard metrics: BLEU, ROUGE, METEOR, BERTScore, accuracy, precision, recall, F1, etc.
- No retrieval metrics: P@k, R@k, NDCG, MRR, MAP
- No safety metrics: toxicity, bias scores

Granularity:
- Episode-level success tracking (per sample)
- No batch processing support documented
- Limited extensibility for custom metrics

Rating: 1 pt - <10 metrics, limited coverage, lacks standard metric implementations.

### S4F3: Evaluator Model Integration (Rating: 0)

Evidence:

Policy inference scripts only use rule-based environment checks, not LLM judges:

From `scripts/rt1_pick_coke_can_visual_matching.sh`:
```bash
do CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path} \
  --robot google_robot_static \
  --control-freq 3 --sim-freq 513 --max-episode-steps 80 \
  --env-name ${env_name} --scene-name ${scene_name}
```

Missing capabilities:
- No LLM-as-judge support
- No pre-built judge prompts
- No multi-aspect scoring (fluency, relevance, etc.)
- No specialized evaluator models (RAGAS, G-Eval, Prometheus)
- No ensemble scoring mechanisms
- No rationale capture or chain-of-thought evaluation

Rating: 0 pts - No evaluator model support; only rule-based environment success detection.

### S4F4: Multi-Modal Scoring Protocols (Rating: 0)

Evidence:

While the framework handles multi-modal robotics data (RGB, depth), "visual matching" is for environment rendering, not evaluation:

From `README.md`:
```md
This repository encompasses 2 real-to-sim evaluation setups:
- `Visual Matching` evaluation: Matching real & sim visual appearances for policy evaluation by overlaying real-world images onto simulation backgrounds
```

From environment building in `simpler_env/utils/env/env_builder.py` (implied from structure):
```python
env_kwargs["obs_mode"] = "rgbd"  # from simpler_env/__init__.py
```

Missing capabilities:
- No vision-language metrics (CIDEr, SPICE, CLIP score)
- No VQA accuracy computation
- No text-to-image alignment metrics
- No audio-text metrics (WER, MOS)
- No video understanding metrics
- Visual matching is for sim environment setup, not evaluation scoring

Rating: 0 pts - Text-only evaluation (success/failure), no multi-modal evaluation metrics.

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 2)

Evidence:

Basic statistics via custom metrics module in `simpler_env/utils/metrics.py`:

From `tools/calc_metrics.py`:
```python
REAL_PERF = {
    "google_robot_move_near": {...},  # Performance data
}

SIMPLER_PERF = {
    "google_robot_move_near": {...},  # Performance data
}

for k in SIMPLER_PERF.keys():
    mmrv = mean_maximum_rank_violation(
        list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
    )
    pearson = pearson_correlation(
        list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
    )
```

From `README.md` documentation:
```python
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF

sim_eval_perf = [your_sim_eval(task="google_robot_move_near", policy=p) for p in ["rt-1-x", "octo"]]
real_eval_perf = [REAL_PERF["google_robot_move_near"][p] for p in ["rt-1-x", "octo"]]
mmrv = mean_maximum_rank_violation(real_eval_perf, sim_eval_perf)
pearson = pearson_correlation(real_eval_perf, sim_eval_perf)
```

Basic statistics:
- Custom MMRV (Mean Maximum Rank Violation) metric
- Pearson correlation for model comparison
- Success rates (computed from episode results)

Missing capabilities:
- No mean, median, std dev, variance
- No percentiles (P25, P50, P75, P95, P99)
- No confidence intervals
- No distribution analysis (histograms, outlier detection)
- No significance testing (t-test, Wilcoxon, bootstrap)
- No effect size computation
- No ranking systems (Elo, TrueSkill)
- No weighted metrics or stratified statistics

Rating: 2 pts - Basic statistics with simple comparisons (MMRV and Pearson correlation); lacks comprehensive statistical suite and significance testing.

## Key Observations

1. Not a General Evaluation Framework: SimplerEnv is purpose-built for robotics policy evaluation in simulation, not for general LLM/model evaluation.

2. Robotics-Specific Design: Focus is on real-to-sim gap analysis and manipulation task success, not on text generation quality or traditional ML metrics.

3. Minimal Evaluation Infrastructure: The framework provides environment simulation and policy execution but lacks comprehensive metric computation, validation, and aggregation features expected in evaluation frameworks.

4. Limited Metric Library: Only 2-3 custom metrics (MMRV, Pearson correlation, success rate) for comparing real vs. simulated performance.

5. No LLM Integration: No support for LLM-as-judge, model-based evaluation, or natural language scoring.

6. Basic Aggregation: Provides simple statistical comparisons between policies but lacks comprehensive statistical analysis tools.

## Recommendations

If adapting SimplerEnv for general evaluation tasks:
1. Add comprehensive metric library with standard text generation, classification, and retrieval metrics
2. Implement LLM-as-judge infrastructure for subjective evaluations
3. Add output validation and normalization capabilities
4. Expand statistical analysis with significance testing and confidence intervals
5. Support multi-modal evaluation beyond robotics-specific visual matching

However, this framework is well-suited for its intended purpose (robotics policy evaluation) and should not be expected to function as a general-purpose evaluation harness.