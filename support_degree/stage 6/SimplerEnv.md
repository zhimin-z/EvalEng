# SimplerEnv - Stage 6 (COMMUNICATE) Evaluation

## Summary
SimplerEnv is a robotics simulation evaluation framework built on ManiSkill2/SAPIEN. It focuses on sim-to-real policy evaluation but has minimal artifact management and no systematic result communication features. Results are saved as videos and pickles, but there's no querying, comparison, versioning, reporting, or distribution infrastructure.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 1 | Minimal logging exists (videos + pickles), but no querying, comparison, or packaging capabilities |
| S6F2: Version Control | 0 | No git integration, dependency tracking, or reproducibility manifests |
| S6F3: Report Generation | 1 | Simple metrics calculation script exists, but no stakeholder-specific reports or visualizations |
| S6F4: Distribution Channels | 0 | No CI/CD integration, MLOps platform support, or automated publishing |

---

## S6F1: Evaluation Artifact Management (Rating: 1)

Evidence:

### Runtime Capture - Basic
The framework saves videos and pickle files during evaluation:

```python
# simpler_env/evaluation/maniskill2_evaluator.py (not provided but referenced)
# From example.ipynb and scripts, results are saved to directories like:
# results/rt_1_tf_trained_for_000400120/google_pick_coke_can_1_v4/.../*.mp4
```

From `tools/merge_videos.py`:
```python
def merge_videos(input_dir: Path, output_path: str = None, no_text_on_video: bool = False):
    video_paths = []
    for video_path in input_dir.glob("/*.mp4"):
        video_paths.append(video_path)
    # Basic text overlay with success/failure info
    put_text_on_image(
        lines=[
            "success: " + success,
            video_clip_additional_info if video_clip_additional_info is not None else "",
        ],
    )
```

Issues:
- No structured metadata capture (timestamps, configs, model IDs)
- No execution logs or traces beyond videos
- File naming encodes some info but no database/index

### Querying - None
Evidence:
- No API or tools for filtering/searching runs
- Manual filesystem navigation required
- From `tools/merge_videos.py`, extraction of metadata from filenames is hardcoded:
```python
dirname_elems = dirname.name.split("_")
rob_idx = dirname_elems.index("rob")
robot_init_x = round(float(dirname_elems[rob_idx + 1]), 3)
```

### Comparison - Manual Only
Evidence:
From `tools/calc_metrics.py`:
```python
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF, SIMPLER_PERF

# Manual comparison by importing hardcoded data
for k in SIMPLER_PERF.keys():
    mmrv = mean_maximum_rank_violation(
        list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
    )
```

- No automated run comparison
- No diff tools for configs
- Requires manual data aggregation

### Packaging - None
Evidence:
- No bundling of results, logs, configs into archives
- Results scattered in filesystem
- No compression or efficient storage mechanisms
- Directory structure is implicit, not preserved

Rating Justification: 1 pt - Minimal logging (videos) exists but no querying, comparison tools, or proper packaging. All artifact management is manual.

---

## S6F2: Archival Version Control and Reproducibility Manifests (Rating: 0)

Evidence:

### Git Integration - None
- No automatic commit tracking in code
- No links between runs and git commits
- No detection of uncommitted changes

### Dependency Pinning - Minimal
From `requirements_full_install.txt`:
```txt
numpy<2.0
tensorflow[and-cuda]
tensorflow_datasets==4.9.4
# ... other deps with versions
```

Issues:
- Requirements file exists but not auto-captured per run
- No runtime capture of actual installed versions
- No system library version tracking

### Environment Capture - None
- No recording of Python/CUDA/OS versions per run
- No environment variable capture
- No random seed tracking in evaluation code

### Manifest Generation - None
Evidence:
- No reproducibility manifests generated
- No machine-executable reproduction scripts
- Config details embedded in shell scripts (e.g., `scripts/rt1_pick_coke_can_visual_matching.sh`):
```bash
CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py \
  --policy-model rt1 --ckpt-path ${ckpt_path} \
  --robot google_robot_static \
  --control-freq 3 --sim-freq 513 --max-episode-steps 80 \
  --env-name ${env_name} --scene-name ${scene_name}
```

But no automatic manifest generation from runs.

### Container Packaging - None
- No Docker image export
- No containerized reproducibility mentioned in docs

Rating Justification: 0 pts - No git integration, no automated dependency/environment capture, no reproducibility manifests. Users must manually track all versioning.

---

## S6F3: Stakeholder-Specific Report and Visualization Generation (Rating: 1)

Evidence:

### Format Support - Videos Only
From codebase:
- Videos: `.mp4` files saved by default
- No HTML, PDF, CSV, Parquet export
- No interactive dashboards
- No notebooks for results

### Stakeholder Templates - None
- No executive summary templates
- No technical deep-dive reports
- No compliance/audit reports
- All results are raw videos + metrics in stdout

### Visualization - Basic
From `tools/merge_videos.py`:
```python
def put_text_on_image(
    image: np.ndarray,
    lines: List[str],
    font_size=1,
    font_thickness=1,
    color=(255, 255, 255),
):
    # Basic text overlay on videos
    cv2.putText(image, line, (x, y), font, font_size, color, ...)
```

From `tools/calc_metrics.py`:
```python
# Simple metrics calculation
mmrv = mean_maximum_rank_violation(...)
pearson = pearson_correlation(...)
print(f"MMRV: {mmrv}, Pearson: {pearson}\n")
```

Issues:
- No confusion matrices, ROC curves, calibration plots
- No performance comparison charts
- Just simple print statements for metrics

### Automation - None
- No automated report generation after runs
- No template customization
- No scheduled reporting

Rating Justification: 1 pt - Single format (video), generic output (print statements), very basic text overlay visualization. No stakeholder-specific reports or rich visualizations.

---

## S6F4: Publication to Distribution Channels (Rating: 0)

Evidence:

### CI/CD Integration - None
- No GitHub Actions, GitLab CI, or Jenkins integration
- No pass/fail gates based on metrics
- Shell scripts (e.g., `scripts/*.sh`) are for manual execution

### MLOps Platforms - None
From `requirements_full_install.txt`:
```txt
wandb
```

Wandb is listed as a dependency, but:
- No usage in main inference scripts
- No MLflow, Neptune, Comet integration examples
- No model registry publishing code

### Public Leaderboards - None
- No HuggingFace Hub publishing code
- No Papers with Code integration
- From README: comparison instructions are manual
```python
# README.md example is manual:
sim_eval_perf = [your_sim_eval(task=..., policy=p) for p in policies]
real_eval_perf = [REAL_PERF["task"][p] for p in policies]
```

### Notifications - None
- No Slack, email, or webhook notifications
- No configurable notification rules
- No alert on metric degradation

Rating Justification: 0 pts - No CI/CD integration, no MLOps platform connections (despite wandb in deps), no leaderboard publishing, no notifications. All distribution is manual.

---

## Overall Assessment

Total Score: 2/12

SimplerEnv is a research evaluation framework focused on sim-to-real robotics, not a production evaluation harness. It has:

### Strengths:
- Comprehensive simulation environments
- Good policy inference examples
- Detailed environment building documentation

### Critical Gaps for COMMUNICATE Stage:
1. No Artifact Management: Results are videos + filenames, no structured metadata
2. No Versioning: Zero reproducibility infrastructure
3. No Reporting: Just videos and print statements
4. No Distribution: Fully manual sharing/publishing

### Use Case:
- Suitable for: Academic experiments, manual comparison studies
- Not suitable for: Production evaluation, automated benchmarking, team collaboration, compliance/audit needs

### To Improve:
1. Add structured result storage (JSON/database)
2. Implement git/dependency tracking
3. Create HTML/PDF report generators
4. Integrate with MLOps platforms (wandb is already a dep)
5. Add CI/CD examples

The framework is well-designed for its intended robotics research use case, but has essentially no infrastructure for professional result communication and distribution.