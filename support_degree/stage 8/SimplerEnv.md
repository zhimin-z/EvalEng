# SimplerEnv - Stage 8 (MONITOR) Evaluation

## Summary
SimplerEnv is a robotics simulation evaluation framework designed to assess manipulation policies in simulated environments that closely match real-world robot setups. The repository focuses on offline evaluation of pre-trained policies (RT-1, Octo) in simulation environments, but provides no post-deployment monitoring or continuous improvement capabilities. This is fundamentally a research evaluation toolkit, not a production monitoring system.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift detection, distribution shift analysis, or performance degradation tracking exists |
| S8F2: Online Evaluation | 0 | Framework is entirely offline; no streaming support, A/B testing, or shadow deployment capabilities |
| S8F3: Feedback Integration | 0 | No production feedback loops, failure mining, or automatic dataset updates |
| S8F4: Improvement Planning | 1 | Basic comparative metrics exist for ranking policies, but no automated root cause analysis or recommendations |

## Detailed Analysis

### S8F1: Production Drift Monitoring (0/3)

Rating: 0 points - No drift monitoring capabilities exist.

Evidence:

1. No Distribution Shift Detection: The codebase contains no statistical tests for drift. Search through `simpler_env/utils/` reveals only basic metric utilities:

```python
# simpler_env/utils/metrics.py (entire file focused on offline comparison)
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF
```

2. No Performance Monitoring Infrastructure: The evaluation runs are one-off batch processes with no ongoing monitoring:

```python
# simpler_env/main_inference.py - Single-shot evaluation
# No evidence of:
# - Continuous metric tracking
# - Time-series performance analysis
# - Anomaly detection
```

3. No Alerting System: Scripts in `scripts/` are all batch evaluation scripts with no alert mechanisms:

```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
# Runs evaluations but has no alerting, monitoring, or drift detection
do CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path} \
  --robot google_robot_static \
  --control-freq 3 --sim-freq 513 --max-episode-steps 80 \
  --env-name ${env_name} --scene-name ${scene_name} \
  # ... just runs evaluation once
done
```

4. Static Evaluation Only: The framework evaluates policies against fixed test scenarios without monitoring deployment behavior:

```python
# simpler_env/__init__.py - Pre-defined static environments
ENVIRONMENTS = [
    "google_robot_pick_coke_can",
    "google_robot_pick_horizontal_coke_can",
    # ... fixed test environments
]
```

Conclusion: SimplerEnv is designed for offline research evaluation, not production monitoring. There are no drift detection features, performance tracking over time, or alerting mechanisms.

---

### S8F2: Online and Streaming Evaluation (0/3)

Rating: 0 points - Framework is entirely offline with no online evaluation capabilities.

Evidence:

1. No Streaming Support: All evaluations run as batch processes with pre-determined episode counts:

```python
# From scripts/rt1_pick_coke_can_variant_agg.sh
--max-episode-steps 80 \
--obj-init-x -0.35 -0.12 5 --obj-init-y -0.02 0.42 5 \
# Runs fixed number of episodes offline
```

2. No A/B Testing Infrastructure: The framework can compare policies, but only through separate offline runs:

```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
# Runs different checkpoints sequentially, not in parallel A/B fashion
declare -a arr=("./checkpoints/rt_1_x_tf_trained_for_002272480_step/" \
                "./checkpoints/rt_1_tf_trained_for_000400120/" \
                "./checkpoints/rt_1_tf_trained_for_000058240/" \
                "./checkpoints/rt_1_tf_trained_for_000001120/")
for ckpt_path in "${arr[@]}"; do
  # Each runs separately, no traffic splitting
done
```

3. No Shadow Deployment: No capability to run candidate policies alongside production:

```python
# simpler_env/main_inference.py
# Single policy evaluation at a time
# No side-by-side comparison in production
```

4. No Automated Rollback: Evaluations are manual research experiments with no automatic decision-making:

```python
# tools/calc_metrics.py - Manual metric computation after the fact
if __name__ == "__main__":
    print("======= SIMPLER Evaluation =======\n")
    for k in SIMPLER_PERF.keys():
        print(f"{k}:")
        mmrv = mean_maximum_rank_violation(...)
        pearson = pearson_correlation(...)
```

5. Batch Processing Architecture: The framework processes episodes sequentially:

```python
# From README.md example
done, truncated = False, False
while not (done or truncated):
    image = get_image_from_maniskill2_obs_dict(env, obs)
    action = env.action_space.sample() # offline policy inference
    obs, reward, done, truncated, info = env.step(action)
# No streaming, no online adaptation
```

Conclusion: SimplerEnv is a research evaluation toolkit for offline policy comparison, not an online evaluation system. It has no streaming capabilities, A/B testing, or production deployment features.

---

### S8F3: Feedback Loop Integration (0/3)

Rating: 0 points - No feedback integration or closed-loop systems.

Evidence:

1. No Production Data Ingestion: The framework uses pre-defined static test scenarios:

```python
# simpler_env/evaluation/maniskill2_evaluator.py
# No evidence of production log parsing or feedback collection
# Only evaluates on synthetic simulation environments
```

2. No Failure Mining: While evaluation results are logged, there's no automatic extraction or incorporation into datasets:

```python
# Tools for manual analysis only
# tools/merge_videos.py - Manual video merging
# tools/calc_metrics.py - Manual metric calculation
# No automated failure mining or dataset updates
```

3. Static Datasets: The framework uses fixed environments and test scenarios:

```python
# From ADDING_NEW_ENVS_ROBOTS.md
# Adding new environments requires manual code changes:
# 1. Add new object assets to ManiSkill2_real2sim/data/custom
# 2. Add custom simulation scene backgrounds
# 3. Add new environments to ManiSkill2_real2sim/mani_skill2_real2sim/envs/custom_scenes
# No automatic dataset expansion from production data
```

4. No Closed-Loop Automation: Evaluation is entirely manual:

```bash
# scripts/rt1_pick_coke_can_visual_matching.sh
# User must manually run evaluation scripts
# No automatic triggering based on feedback
for urdf_version in "${urdf_version_arr[@]}"; do
  for coke_can_option in "${coke_can_options_arr[@]}"; do
    for ckpt_path in "${arr[@]}"; do
      CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py ...
    done
  done
done
```

5. Research-Focused Metrics: The metrics compare simulation to real-world baselines, not production feedback:

```python
# simpler_env/utils/metrics.py
def mean_maximum_rank_violation(real_eval_perf, sim_eval_perf):
    # Compares pre-collected real-world results to simulation
    # Not designed for production feedback integration
```

Conclusion: SimplerEnv has no feedback loop capabilities. It's designed for academic comparison between simulation and real-world evaluation, not for production monitoring or continuous improvement.

---

### S8F4: Iteration Planning and Improvement Recommendations (1/3)

Rating: 1 point - Raw comparative metrics exist but no automated recommendations.

Evidence:

1. Basic Comparative Metrics: The framework provides MMRV and Pearson correlation for ranking:

```python
# simpler_env/utils/metrics.py
def mean_maximum_rank_violation(real_eval_perf, sim_eval_perf):
    """
    Computes the mean maximum rank violation (MMRV) between real and sim evaluation.
    Lower is better.
    """
    # Basic ranking metric, no root cause analysis

def pearson_correlation(real_eval_perf, sim_eval_perf):
    """
    Computes Pearson correlation between real and sim evaluation.
    """
    # Correlation metric only
```

Usage example:

```python
# tools/calc_metrics.py
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

2. No Root Cause Analysis: The framework logs success/failure but provides no automated analysis:

```python
# tools/merge_videos.py - Manual video inspection
text_fn = partial(
    put_text_on_image,
    lines=[
        "success: " + success,  # Just labels success/failure
        video_clip_additional_info if video_clip_additional_info is not None else "",
    ],
    color=(255, 0, 0) if success != "success" else (0, 255, 0),
)
# No automated error pattern analysis
```

3. No Hyperparameter Recommendations: System identification is manual:

```python
# From ADDING_NEW_ENVS_ROBOTS.md
# Manual system identification process:
# "perform system identification using the dataset. You can modify the existing 
# system identification script tools/sysid/sysid.py. The script uses simulated 
# annealing algorithm to find better stiffness and damping parameters"
# No automated suggestions
```

4. No Dataset Expansion Guidance: Adding new environments requires extensive manual work:

```markdown
# ADDING_NEW_ENVS_ROBOTS.md
4. Add new object assets to ManiSkill2_real2sim/data/custom
5. Add custom simulation scene backgrounds
6. If you adopt our visual-matching evaluation setup, add the overlay background image
7. Add new environments to ManiSkill2_real2sim/mani_skill2_real2sim/envs/custom_scenes
# No automated gap analysis or prioritization
```

5. No Roadmap Generation: Researchers must manually interpret results:

```python
# README.md guidance for using metrics
# "We make it easy to compare your offline robot policy evaluation approach to SIMPLER"
# Comparison only - no automated experiment planning
```

6. Manual Variant Testing: Users must manually configure evaluation variants:

```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
# Manual specification of variations to test:
declare -a coke_can_options_arr=("lr_switch=True" "upright=True" "laid_vertically=True")
declare -a scene_arr=("Baked_sc1_staging_objaverse_cabinet1_h870" \
                      "Baked_sc1_staging_objaverse_cabinet2_h870")
# No automated recommendation of what to test next
```

Why 1 point instead of 0: The framework does provide basic ranking metrics (MMRV, Pearson correlation) that can inform manual iteration planning. However, this is minimal - researchers still need to manually interpret results and plan improvements.

Conclusion: SimplerEnv provides basic comparative metrics but no automated root cause analysis, hyperparameter recommendations, or iteration planning. All improvement decisions require manual interpretation by researchers.

---

## Overall Assessment

SimplerEnv is a research evaluation framework for offline policy comparison in simulation, not a production monitoring or continuous improvement system. It excels at:

- Providing high-fidelity simulation environments that match real robot setups
- Enabling reproducible offline evaluation of policies
- Comparing simulation results to real-world baselines

However, it completely lacks:

- Drift monitoring and performance tracking over time
- Online/streaming evaluation capabilities
- Production feedback integration
- Automated improvement recommendations

Stage 8 Total: 1/12 points

This is appropriate for the repository's purpose as a research tool, but it means SimplerEnv cannot serve as a production monitoring or continuous improvement system. Users would need to build entirely new infrastructure on top of SimplerEnv to support post-deployment monitoring use cases.