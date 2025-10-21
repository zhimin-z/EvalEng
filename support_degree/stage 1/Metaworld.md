# Metaworld - Stage 1 (CONFIGURE) Evaluation

## Summary
Metaworld is a robotics simulation benchmark for multi-task and meta-reinforcement learning, not an LLM evaluation framework. It focuses on robotic manipulation tasks rather than language model evaluation. The repository is fundamentally misaligned with the evaluation criteria, which target LLM evaluation frameworks.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | Not Applicable - Wrong Domain: Metaworld is a robotics RL benchmark, not an LLM evaluation framework. It provides 50 robotic manipulation environments (e.g., `reach-v3`, `push-v3`, `pick-place-v3`) as shown in `metaworld/env_dict.py`. There is no concept of "datasets" in the LLM evaluation sense (JSON, CSV, HuggingFace datasets). The "tasks" are physical simulation environments with goal positions and object states, not text/data samples for LLM evaluation. Evidence: `metaworld/__init__.py` lines 66-184 show task generation via `_make_tasks()` which creates simulated robotic scenarios with randomized object positions (`rand_vecs`), not evaluation datasets. |
| S1F2: Model Configuration | 0 | Not Applicable - Wrong Domain: This is a robotics environment, not an LLM evaluation framework. There is no model configuration for language models or LLM backends. The framework expects RL agents/policies to interact with gymnasium environments. Evidence: `README.md` shows usage like `env = gym.make("Meta-World/MT1", env_name="reach-v3")` followed by `action = env.action_space.sample()` and `env.step(action)` - this is standard RL environment interaction, not LLM API configuration. The `policies/` directory contains scripted robotic manipulation policies (e.g., `SawyerReachV3Policy`), not LLM configuration. |
| S1F3: Prompt Configuration | 0 | Not Applicable - Wrong Domain: No prompt templating, parameter configuration, or LLM-related features exist. This is a robotic simulation benchmark where "actions" are 4D continuous vectors representing gripper movements `(dx, dy, dz, gripper)` as documented in `docs/benchmark/action_space.md`. There are no prompts, templates, or text generation parameters. The only "configuration" relates to environment parameters like `reward_function_version`, `render_mode`, `camera_name`, etc., as shown in `metaworld/__init__.py` lines 345-376. |
| S1F4: Environment Setup | 2 | Partial Credit for RL Setup: While not an LLM framework, it does provide decent environment setup for its intended purpose. Evidence: `pyproject.toml` shows pinned dependencies including `gymnasium>=1.1`, `mujoco>=3.0.0`, `numpy>=1.18`. Docker support exists in `docker/` directory with `Dockerfile` and setup instructions in `docker/README.md`. Installation is straightforward: `pip install metaworld` or `pip install -e .` for development. However, no GPU/TPU configuration for LLMs exists (only MuJoCo physics simulation GPU support). Pre-commit hooks are documented in `CONTRIBUTING.md`. Loses a point because it's solving the wrong problem (RL environment setup, not LLM evaluation setup). |
| S1F5: Security & Access Control | 0 | No Security Features: The repository shows no security infrastructure. No credential management, RBAC, audit logging, SSO, or enterprise integration features. Evidence: Grep for "vault", "credentials", "auth", "rbac" yields no results. `CONTRIBUTING.md` discusses code contribution workflows but no security mechanisms. The framework is designed for local research use with physics simulation, not production LLM evaluation with sensitive API keys or multi-user access control. |
| S1F6: Cost Estimation | 0 | No Cost Features: This is a simulation environment with no API calls or cloud resource costs to estimate. Evidence: No cost-related code found in codebase. The "cost" in RL research is computational (GPU hours for training agents), not API token costs. `docs/benchmark/reward_functions.md` discusses reward shaping for RL training, not financial cost estimation. No token counting, budget limits, or cost optimization suggestions exist. |

## Overall Assessment

Total Score: 2/18

### Critical Issues

1. Fundamental Domain Mismatch: Metaworld is a robotics reinforcement learning benchmark, not an LLM evaluation framework. The evaluation criteria assume an LLM evaluation harness with concepts like:
   - Text datasets (JSON/CSV/HuggingFace)
   - LLM model backends (OpenAI, Anthropic, etc.)
   - Prompt templates with variable substitution
   - Token counting and API cost estimation
   
   None of these concepts exist in Metaworld because it's solving a completely different problem.

2. What Metaworld Actually Does (from `README.md` and documentation):
   - Provides 50 simulated robotic manipulation tasks (reach, push, pick-place, door-open, etc.)
   - Organizes tasks into benchmarks: MT1/MT10/MT50 (multi-task RL) and ML1/ML10/ML45 (meta-RL)
   - Uses Gymnasium API for environment interaction
   - Supports rendering with MuJoCo physics engine
   - Provides scripted expert policies for each task
   - Evaluates RL agents via success rate on physical manipulation tasks

3. Evidence of Domain:
   ```python
   # From metaworld/__init__.py
   env = gym.make("Meta-World/MT1", env_name="reach-v3")
   observation, info = env.reset()
   for _ in range(500):
       action = env.action_space.sample()  # 4D continuous action space
       observation, reward, terminated, truncated, info = env.step(action)
   ```
   
   Compare to what an LLM evaluation framework would look like:
   ```python
   # Hypothetical LLM eval framework
   eval_suite = EvalFramework.load_dataset("gsm8k")
   model = EvalFramework.load_model("gpt-4", api_key=...)
   results = eval_suite.evaluate(model, prompt_template="...")
   ```

4. Configuration Exists, But Wrong Type:
   - `metaworld/__init__.py` shows environment configuration parameters: `seed`, `max_episode_steps`, `render_mode`, `camera_name`, `reward_function_version`
   - These configure physics simulation environments, not LLM evaluation pipelines
   - No dataset discovery, model backends, prompt templates, or cost estimation

### Why 2 Points Awarded

The 2 points for S1F4 (Environment Setup) recognize that Metaworld does provide:
- Clear dependency management (`pyproject.toml`)
- Docker containerization (`docker/Dockerfile`)
- Installation scripts and documentation
- Development tooling (pre-commit hooks)

However, this is environment setup for RL research, not LLM evaluation. The framework would need to be completely redesigned to serve as an LLM evaluation harness.

### Recommendation

This repository should not be evaluated against LLM evaluation framework criteria. It is a well-designed robotics RL benchmark serving its intended purpose (cited 100+ times for meta-RL research per the paper reference). Forcing it into the LLM evaluation rubric is like evaluating a car using airplane criteria - the domains are fundamentally different.

If you need to evaluate LLM frameworks, consider repositories like:
- EleutherAI/lm-evaluation-harness
- bigcode-project/bigcode-evaluation-harness
- OpenCompass
- HELM (Holistic Evaluation of Language Models)