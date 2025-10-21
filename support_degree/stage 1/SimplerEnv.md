# SimplerEnv - Stage 1 (CONFIGURE) Evaluation

## Summary
SimplerEnv is a robotics simulation evaluation framework built on SAPIEN/ManiSkill2, not an LLM evaluation framework. It is designed for evaluating robot manipulation policies (RT-1, Octo) in simulated environments that match real-world setups. The framework has zero configuration capabilities for LLM evaluation tasks as understood in the 8-stage framework. This is a fundamental category mismatch - evaluating this robotics simulator against LLM evaluation criteria is inappropriate.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No LLM dataset configuration. The framework uses robotics trajectory datasets (Bridge, Fractal) via tensorflow_datasets. No schema definition, versioning, or split strategies for evaluation datasets. |
| S1F2: Model Configuration | 0 | Configures robot policies (RT-1, Octo), not LLM models. No support for LLM providers (OpenAI, Anthropic, etc.). The `simpler_env/__init__.py` only maps task names to simulation environments. |
| S1F3: Prompt Configuration | 0 | No prompt templating system. Language instructions are hardcoded in environments (e.g., `get_language_instruction()` returns fixed strings). No parameter sweeps, few-shot support, or prompt versioning. |
| S1F4: Environment Setup | 2 | Has `requirements_full_install.txt`, `setup.py`, and `pyproject.toml`. Dependencies specified but focused on robotics simulation (SAPIEN, ManiSkill2). No containerization provided. Manual setup required with multiple conda/pip install steps. |
| S1F5: Security & Access | 0 | No credential management, RBAC, audit logging, or enterprise integration features. Framework expects local execution with manual API key management for robot policies. |
| S1F6: Cost Estimation | 0 | No cost estimation capabilities for API calls or token usage. Framework is designed for local simulation execution, not cloud LLM inference. |

Total Stage 1 Score: 2/18 (11%)

---

## Detailed Feature Analysis

### S1F1: Dataset Discovery and Logical Configuration (0/3 points)

Evidence of Mismatch:

The framework uses robotics trajectory datasets, not text evaluation datasets:

```python
# tools/visualize_dataset.py
DATASETS = ["fractal20220817_data", "bridge"]

def dataset2path(dataset_name):
    if dataset_name == "robo_net":
        version = "1.0.0"
    elif dataset_name == "language_table":
        version = "0.0.1"
    else:
        version = "0.1.0"
    return f"gs://gresearch/robotics/{dataset_name}/{version}"
```

What exists instead:
- Environment configuration through task names (`simpler_env/__init__.py`):
```python
ENVIRONMENT_MAP = {
    "google_robot_pick_coke_can": ("GraspSingleOpenedCokeCanInScene-v0", {}),
    "google_robot_move_near": ("MoveNearGoogleBakedTexInScene-v1", {}),
    # ... more robotics tasks
}
```

Missing for LLM evaluation:
- No JSON/CSV/HuggingFace dataset registration
- No schema definition for text inputs/outputs
- No train/val/test split strategies
- No dataset versioning system

Rating: 0 points - Framework is for robotics simulation, not LLM dataset management.

---

### S1F2: Model and Backend Configuration (0/3 points)

Evidence of Mismatch:

The framework configures robot policies, not LLMs:

```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
declare -a arr=("./checkpoints/rt_1_x_tf_trained_for_002272480_step/" \
                "./checkpoints/rt_1_tf_trained_for_000400120/")

python simpler_env/main_inference.py --policy-model rt1 --ckpt-path ${ckpt_path}
```

```bash
# scripts/octo_bridge.sh
declare -a policy_models=("octo-small" "octo-base")
python simpler_env/main_inference.py --policy-model ${policy_model}
```

What exists instead:
- Robot policy configuration (RT-1, Octo models)
- Simulation environment parameters (control frequency, sim frequency)
- No LLM provider abstractions

Missing for LLM evaluation:
- No OpenAI/Anthropic/HuggingFace provider support
- No API key management for LLM services
- No LLM-specific parameters (temperature, top_p, max_tokens)

Rating: 0 points - Configures robot controllers, not language models.

---

### S1F3: Evaluation Parameters and Prompt Configuration (0/3 points)

Evidence:

Language instructions are hardcoded in environment code, not templated:

```python
# simpler_env/__init__.py - example usage
env = simpler_env.make('google_robot_pick_coke_can')
instruction = env.get_language_instruction()  # Returns fixed string
```

The framework has no prompt templating:
- No Jinja2 or similar template engine
- No variable substitution mechanisms
- No few-shot example injection
- No prompt versioning

What exists instead:
- Robot control parameters: `--control-freq 3 --sim-freq 513`
- Environment variation configs: `--robot-init-x 0.35 --robot-init-y 0.20`

Missing for LLM evaluation:
- No prompt template system
- No parameter sweeps for temperature/top_p
- No metric configuration for text generation
- No success criteria thresholds

Rating: 0 points - No prompt configuration infrastructure.

---

### S1F4: Environment Setup and Dependency Management (2/3 points)

Evidence of what exists:

1. Dependency Specification:
```txt
# requirements_full_install.txt (partial)
numpy<2.0
tensorflow[and-cuda]==2.15.1
matplotlib
transformers
scipy==1.12.0
```

```python
# setup.py
setup(
    name="simpler_env",
    version="0.0.1",
    packages=find_packages(include=["simpler_env*"]),
    python_requires=">=3.10",
)
```

2. Installation Steps (from README.md):
```bash
conda create -n simpler_env python=3.10
pip install numpy==1.24.4
cd ManiSkill2_real2sim && pip install -e .
cd .. && pip install -e .
```

Strengths:
- Clear requirements file with pinned versions
- setup.py provided
- Multi-step installation documented

Weaknesses:
- No Docker/container support mentioned
- No automated setup scripts
- Complex multi-repo installation (submodule ManiSkill2_real2sim)
- CUDA version dependencies complex (requires >=11.8 or 12.2+)

Rating: 2 points - Has requirements and setup.py, but manual installation with multiple steps required. No containerization.

---

### S1F5: Security and Access Control (0/3 points)

Evidence:

No security infrastructure found:
- No credential management code in `simpler_env/`
- No RBAC, audit logging, or access control
- No enterprise integration features

From README.md, the framework expects local execution:
```markdown
Prerequisites:
- CUDA version >=11.8
- An NVIDIA GPU
```

What exists:
- Manual checkpoint management: `gsutil -m cp -r gs://...` (in README)
- No API key handling visible in codebase

Missing:
- No vault integration
- No SSO/SAML support
- No audit logging
- No RBAC for experiments

Rating: 0 points - No security features for evaluation infrastructure.

---

### S1F6: Cost Estimation and Budget Planning (0/3 points)

Evidence:

No cost estimation code found. The framework is designed for local GPU simulation, not cloud API usage:

```python
# simpler_env/__init__.py
def make(task_name, kwargs):
    env = gym.make(env_name, env_kwargs)  # Local simulation
    return env
```

Evaluation scripts run simulations locally:
```bash
# scripts/rt1_pick_coke_can_variant_agg.sh
CUDA_VISIBLE_DEVICES=${gpu_id} python simpler_env/main_inference.py
```

What exists:
- GPU resource allocation via CUDA_VISIBLE_DEVICES
- Simulation step budgets: `--max-episode-steps 80`

Missing for LLM evaluation:
- No token counting
- No API pricing models
- No cost estimation before runs
- No budget limits or alerts

Rating: 0 points - Framework for local simulation, not API cost management.

---

## Why This Evaluation is Inappropriate

SimplerEnv is fundamentally a robotics simulation framework:

1. Purpose Statement (README.md):
   > "Simulated Manipulation Policy Evaluation Environments for Real Robot Setups"

2. Core Functionality:
   - Evaluates robot manipulation policies (RT-1, Octo)
   - Uses SAPIEN physics simulator
   - Compares sim-to-real transfer
   - No LLM inference or text generation

3. Evaluation Metrics (tools/calc_metrics.py):
```python
# Compares robot policy success rates
mmrv = mean_maximum_rank_violation(real_eval_perf, sim_eval_perf)
pearson = pearson_correlation(real_eval_perf, sim_eval_perf)
```

4. Task Examples:
   - `google_robot_pick_coke_can`
   - `widowx_stack_cube`
   - `google_robot_open_drawer`

These are robot manipulation tasks, not LLM evaluation benchmarks.

---

## Recommendations

This repository should NOT be evaluated as an LLM evaluation framework. It is:
- ✅ A robotics simulation framework
- ✅ A real-to-sim evaluation tool for robot policies
- ❌ NOT an LLM evaluation harness
- ❌ NOT related to language model benchmarking

Appropriate evaluation would assess:
- Physics simulation accuracy
- Real-to-sim visual matching quality
- Robot policy evaluation workflows
- Environment configuration for robotics tasks

For LLM evaluation frameworks, consider:
- lm-evaluation-harness (EleutherAI)
- HELM (Stanford)
- OpenAI Evals
- BigBench

---

## Final Assessment

Stage 1 Score: 2/18 (11%)

The only points awarded are for basic Python package setup (S1F4), which is a general software engineering practice, not specific to evaluation framework configuration.

Critical Finding: This repository is categorically mismatched with the evaluation criteria. It is a specialized robotics simulation tool, not a language model evaluation framework. The 8-stage evaluation guidelines assume LLM evaluation infrastructure (datasets, prompts, model APIs) which are completely absent here.