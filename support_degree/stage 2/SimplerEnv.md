# SimplerEnv - Stage 2 (PREPARE) Evaluation

## Summary
SimplerEnv is a robotics simulation evaluation framework focused on real-to-sim policy evaluation, not a general-purpose evaluation harness. It provides minimal preparation features primarily for loading pre-configured simulation environments and assets, not for dataset preprocessing, quality assessment, or data preparation workflows typical of LLM evaluation frameworks. The framework is specialized for robotics policy testing in SAPIEN simulator environments.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No dataset preprocessing pipelines; only loads pre-configured simulation assets and robot URDFs |
| S2F2: Quality Assessment | 0 | No dataset quality assessment, bias detection, or label validation features |
| S2F3: PII Detection | 0 | No PII detection or anonymization capabilities; focused on simulation environments |
| S2F4: Infrastructure Building | 1 | Minimal infrastructure for loading simulation environments and robots; no retrieval systems or databases |
| S2F5: Model Artifact Validation | 0 | No model validation, checksum verification, or corruption detection |
| S2F6: Scenario Generation | 1 | Basic environment configuration variations via kwargs; no templating or multi-turn dialogue support |
| S2F7: Red-Teaming | 0 | No adversarial testing, jailbreak attempts, or safety boundary testing |
| S2F8: Contamination Detection | 0 | No contamination detection or train/test overlap checking |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (0/3)

Rating: 0 points

SimplerEnv has no dataset preprocessing capabilities. The framework is designed to load pre-configured simulation environments, not to preprocess evaluation datasets.

Evidence:

1. Environment Loading Only: The main entry point shows environments are pre-configured, not preprocessed:

```python
# simpler_env/__init__.py
ENVIRONMENT_MAP = {
    "google_robot_pick_coke_can": ("GraspSingleOpenedCokeCanInScene-v0", {}),
    "google_robot_pick_horizontal_coke_can": (
        "GraspSingleOpenedCokeCanInScene-v0",
        {"lr_switch": True},
    ),
    # ...
}

def make(task_name, kwargs):
    """Creates simulated eval environment from task name."""
    env_name, env_kwargs = ENVIRONMENT_MAP[task_name]
    env_kwargs["obs_mode"] = "rgbd",
    env_kwargs["prepackaged_config"] = True
    env = gym.make(env_name, env_kwargs)
    return env
```

2. No Preprocessing Pipeline: The simple inference script shows direct environment loading without any preprocessing:

```python
# simpler_env/simple_inference_visual_matching_prepackaged_envs.py (from README)
env = simpler_env.make('google_robot_pick_coke_can')
obs, reset_info = env.reset()
# No preprocessing, caching, validation, or splitting
```

3. Asset Management, Not Dataset Preprocessing: The framework manages simulation assets (URDF files, meshes) but doesn't preprocess evaluation datasets:

```md
# ADDING_NEW_ENVS_ROBOTS.md
4. Add new object assets to `ManiSkill2_real2sim/data/custom`.
   - Example object assets are in `ManiSkill2_real2sim/data/custom`. Each object asset contains:
     - Visual mesh (a `textured.dae` file combined with its corresponding `.png` texture files)
     - Collision mesh (`collision.obj`). The collision mesh should be watertight and convex.
```

Missing Capabilities:
- No data loading from configs
- No caching mechanisms
- No preprocessing pipelines (tokenization, normalization)
- No validation (checksum, format checking)
- No train/val/test splitting
- No versioning of splits

### S2F2: Dataset Quality and Bias Assessment (0/3)

Rating: 0 points

SimplerEnv has no dataset quality assessment tools. It's a simulation framework, not a data quality evaluation tool.

Evidence:

1. No Quality Tools Found: Searching through the codebase reveals no quality assessment utilities:
   - No files in `simpler_env/utils/` related to quality checks
   - No label quality validation
   - No demographic analysis
   - No duplicate detection

2. Focus on Simulation Evaluation: The framework's purpose is policy evaluation in simulation:

```md
# README.md
Significant progress has been made in building generalist robot manipulation policies, yet their scalable and reproducible evaluation remains challenging, as real-world evaluation is operationally expensive and inefficient. We propose employing physical simulators as efficient, scalable, and informative complements to real-world evaluations.
```

3. System Identification, Not Quality Assessment: The closest thing to quality tools is system identification for robot parameter tuning:

```python
# tools/sysid/sysid.py (filename only, shows robotics focus)
```

Missing Capabilities:
- No label quality checks
- No inter-annotator agreement
- No demographic distribution analysis
- No duplicate detection
- No bias detection tools

### S2F3: PII Detection and Anonymization (0/3)

Rating: 0 points

SimplerEnv has no PII detection or anonymization features. As a robotics simulation framework, it doesn't handle text data requiring privacy protection.

Evidence:

1. No Privacy-Related Code: No files or functions related to PII:
   - No PII detection in any utility files
   - No anonymization functions
   - No privacy-related documentation

2. Simulation Environment Focus: The framework processes visual observations and robot states, not text requiring PII protection:

```python
# From README.md getting started example
image = get_image_from_maniskill2_obs_dict(env, obs)
action = env.action_space.sample()
obs, reward, done, truncated, info = env.step(action)
```

Missing Capabilities:
- No PII detection (names, emails, addresses)
- No anonymization strategies
- No audit trails
- No compliance reporting

### S2F4: Task-Specific Infrastructure Building (1/3)

Rating: 1 point

SimplerEnv provides minimal infrastructure support for loading simulation environments and robot configurations, but no retrieval systems, databases, or versioned artifacts.

Evidence:

1. Environment Loading Infrastructure: The framework provides basic environment building:

```python
# simpler_env/__init__.py
def make(task_name, kwargs):
    """Creates simulated eval environment from task name."""
    assert task_name in ENVIRONMENTS, f"Task {task_name} is not supported"
    env_name, env_kwargs = ENVIRONMENT_MAP[task_name]
    env_kwargs["obs_mode"] = "rgbd"
    env_kwargs["prepackaged_config"] = True
    for key, value in kwargs.items():
        env_kwargs[key] = value
    env = gym.make(env_name, env_kwargs)
    return env
```

2. Robot and Scene Configuration: Basic robot and scene loading:

```python
# simpler_env/evaluation/maniskill2_evaluator.py (from scripts)
# From scripts/rt1_pick_coke_can_visual_matching.sh
CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py \
  --robot google_robot_static \
  --env-name ${env_name} --scene-name ${scene_name} \
  --robot-init-x 0.35 0.35 1 --robot-init-y 0.20 0.20 1
```

3. No Advanced Infrastructure: No retrieval systems, databases, or versioning:
   - No FAISS, BM25, or vector database support
   - No index building or persistence
   - No database schema creation
   - No artifact versioning beyond file paths

Why only 1 point:
- ✓ Basic environment loading exists
- ✗ No retrieval systems
- ✗ No database support
- ✗ No artifact versioning or management
- ✗ Minimal infrastructure, mostly manual setup required

### S2F5: Model Artifact Validation (0/3)

Rating: 0 points

SimplerEnv has no model artifact validation. The framework loads pre-trained models (RT-1, Octo) without validation or integrity checks.

Evidence:

1. No Validation Code: Policy loading in scripts shows no validation:

```bash
# scripts/rt1_pick_coke_can_visual_matching.sh
declare -a arr=("./checkpoints/rt_1_tf_trained_for_000400120/" \
                "./checkpoints/rt_1_tf_trained_for_000058240/" \
                "./checkpoints/rt_1_x_tf_trained_for_002272480_step/")

for ckpt_path in "${arr[@]}";
do python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path}
done
```

2. Direct Model Loading: No checksum verification or corruption detection:

```python
# simpler_env/policies/rt1/__init__.py (assumed from usage)
# No validation, just path passing
```

3. Manual Checkpoint Download: Installation instructions show manual gsutil download without validation:

```bash
# README.md
gsutil -m cp -r gs://gdm-robotics-open-x-embodiment/open_x_embodiment_and_rt_x_oss/rt_1_x_tf_trained_for_002272480_step.zip .
unzip rt_1_x_tf_trained_for_002272480_step.zip
mv rt_1_x_tf_trained_for_002272480_step checkpoints
```

Missing Capabilities:
- No checksum validation
- No version compatibility checks
- No configuration validation
- No corruption detection
- No test inference for integrity

### S2F6: Evaluation Scenario Generation (1/3)

Rating: 1 point

SimplerEnv provides minimal scenario generation through environment configuration parameters, but no template instantiation, multi-turn dialogues, or structured variation generation.

Evidence:

1. Basic Parameter Variations: Environment configurations can be varied through kwargs:

```python
# simpler_env/__init__.py
ENVIRONMENT_MAP = {
    "google_robot_pick_horizontal_coke_can": (
        "GraspSingleOpenedCokeCanInScene-v0",
        {"lr_switch": True},
    ),
    "google_robot_pick_vertical_coke_can": (
        "GraspSingleOpenedCokeCanInScene-v0",
        {"laid_vertically": True},
    ),
    "google_robot_pick_standing_coke_can": (
        "GraspSingleOpenedCokeCanInScene-v0",
        {"upright": True},
    ),
}
```

2. Environment Variations in Scripts: Robot pose and object variations via command-line args:

```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
python simpler_env/main_inference.py \
  --robot-init-x 0.35 0.35 1 --robot-init-y 0.20 0.20 1 \
  --obj-init-x -0.35 -0.12 5 --obj-init-y -0.02 0.42 5 \
  --additional-env-build-kwargs ${coke_can_option}
```

3. No Structured Scenario Generation: No templating system or automatic variation generation:
   - No prompt templates with variables
   - No parameter sweeps (must be manually scripted)
   - No multi-turn dialogue generation
   - No edge case generators

Why only 1 point:
- ✓ Basic environment configuration variations exist
- ✗ No template instantiation
- ✗ No automatic parameter sweeps
- ✗ No multi-turn scenarios
- ✗ No edge case generation
- ✗ Manual scenario creation required

### S2F7: Red-Teaming and Adversarial Test Generation (0/3)

Rating: 0 points

SimplerEnv has no red-teaming or adversarial testing capabilities. It's a robotics simulation framework, not a safety testing tool.

Evidence:

1. No Red-Teaming Features: No files or code related to adversarial testing:
   - No jailbreak attempt library
   - No prompt injection testing
   - No bias probing
   - No safety boundary testing

2. Focus on Physical Simulation: The framework tests robot policies in physical manipulation tasks:

```md
# README.md - Current Environments
| Task Name | Description |
| google_robot_pick_coke_can | Pick up coke can |
| google_robot_open_drawer | Open drawer |
| widowx_spoon_on_towel | Place spoon on towel |
```

3. No Safety Testing Documentation: No mention of adversarial testing or safety evaluation in docs.

Missing Capabilities:
- No red-teaming framework
- No jailbreak generation
- No prompt injection tests
- No bias probing
- No safety boundary testing
- No attack taxonomy

### S2F8: Data Contamination Detection (0/3)

Rating: 0 points

SimplerEnv has no contamination detection capabilities. As a simulation framework, it doesn't compare evaluation data against training corpora.

Evidence:

1. No Contamination Detection Code: No files or utilities for contamination checking:
   - No corpus comparison tools
   - No n-gram overlap detection
   - No semantic similarity checking

2. Simulation-Based Evaluation: The framework evaluates policies in simulation environments, not on text datasets:

```python
# From README.md
env = simpler_env.make('google_robot_pick_coke_can')
obs, reset_info = env.reset()
action = env.action_space.sample()
obs, reward, done, truncated, info = env.step(action)
```

3. Real-to-Sim Gap Metrics: The closest thing to contamination detection is measuring real-to-sim correlation:

```python
# tools/calc_metrics.py
from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF

sim_eval_perf = [your_sim_eval(task="google_robot_move_near", policy=p)]
real_eval_perf = [REAL_PERF["google_robot_move_near"][p]]
mmrv = mean_maximum_rank_violation(real_eval_perf, sim_eval_perf)
pearson = pearson_correlation(real_eval_perf, sim_eval_perf)
```

This measures real-vs-sim performance correlation, not training data contamination.

Missing Capabilities:
- No training corpus comparison
- No n-gram overlap detection
- No semantic similarity checking
- No contamination severity scoring
- No mitigation recommendations

## Summary of Key Issues

1. Wrong Domain: SimplerEnv is a robotics simulation framework, not an LLM/NLP evaluation harness. The Stage 2 criteria assume text-based evaluation workflows.

2. No Data Preparation: The framework loads pre-configured simulation environments, not datasets requiring preprocessing, validation, or splitting.

3. No Privacy/Safety Features: As a simulation framework, it doesn't handle text data requiring PII detection, red-teaming, or contamination checking.

4. Minimal Infrastructure: Only basic environment loading; no retrieval systems, databases, or artifact management.

5. Manual Scenario Creation: Environment variations must be manually specified in scripts; no automatic generation or templating.

## Recommendations

For a robotics simulation evaluation framework like SimplerEnv, Stage 2 criteria should focus on:
- Robot/environment asset management and validation
- Simulation parameter calibration and system identification
- Real-to-sim visual matching and domain randomization
- Trajectory data loading and preprocessing (if applicable)
- Reproducibility through deterministic environment initialization

The current Stage 2 criteria are designed for text-based evaluation harnesses and don't apply well to this robotics simulation framework.