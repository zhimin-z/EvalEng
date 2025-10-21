# Melting Pot - Stage 1 (CONFIGURE) Evaluation

## Summary
Melting Pot is a multi-agent reinforcement learning evaluation suite focused on test scenarios (substrates and scenarios) rather than a general evaluation framework. It does not provide systematic configuration for datasets, models, prompts, or traditional LLM evaluation workflows. It's designed for RL experiments with pre-configured game environments, not for configuring/running LLM evaluations with customizable parameters.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No dataset abstraction exists. The framework works with pre-built game substrates (environments) defined in Lua/Python configs, not datasets with rows/samples. No support for JSON, CSV, HuggingFace, databases, or APIs. Evidence: `meltingpot/configs/substrates/` contains game definitions, not data loading (e.g., `fruit_market.py` defines game objects and maps). |
| S1F2: Model Configuration | 0 | No model/backend configuration system for LLM evaluation. The framework uses pre-trained RL bots (SavedModels) stored in assets, not configurable inference endpoints. Evidence: `meltingpot/configs/bots/__init__.py` references static model paths like `os.path.join(MODELS_ROOT, 'substrate_name', 'model_name')` with no provider abstraction (OpenAI, Anthropic, etc.). |
| S1F3: Prompt Configuration | 0 | No prompt templating, parameter sweeps, or metric configuration. This is an RL framework for gridworld games, not LLM evaluation. Evidence: Action specifications in configs like `fruit_market.py` define discrete actions (`"move": {"default": 0, "min": 0, "max": 5}`) with no text generation parameters (temperature, top_p, etc.). |
| S1F4: Environment Setup | 2 | Good dependency management with pinned requirements and Docker support, but manual setup required. Evidence: `requirements.txt` has hashed dependencies, `setup.py` handles installation, `.devcontainer/devcontainer.json` provides container config. However, `bin/install.sh` shows manual steps needed, and `.github/actions/install/action.yml` reveals complex caching logic for assets, indicating non-trivial setup. |
| S1F5: Security & Access | 0 | No credential management, access control, or audit logging for evaluation workloads. The framework is designed for local/research use. Evidence: No vault integration, RBAC, or SSO mentioned in codebase. `examples/rllib/utils.py` shows direct environment instantiation with no auth checks. |
| S1F6: Cost Estimation | 0 | No cost estimation or budgeting features. This is an RL simulation framework with no concept of API costs. Evidence: Configs like `predator_prey__random_forest.py` specify `maxEpisodeLengthFrames=1000` for simulation length, but no token counting, pricing data, or budget limits exist in the codebase. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (0 points)

Evidence of absence:
- No dataset abstraction: The framework works with "substrates" (game environments) defined via ASCII maps and game object configs, not traditional datasets. From `docs/substrates.md`:
  ```markdown
  Substrates are built with DeepMind Lab2D... we provide an abstraction layer 
  that enables the use of modular components to build the functionality needed.
  ```

- File-based game definitions: `meltingpot/configs/substrates/fruit_market.py` shows configuration is about game objects, not data sources:
  ```python
  ASCII_MAP = """
  /;___________________,/
  ;]XAXXXXXXXAXXXXXXXAX[,
  !XXXXXXXXXXXXXXXXXXXXX|
  ```

- No data loading utilities: Search through `meltingpot/utils/` shows no dataset connectors. Files like `meltingpot/utils/substrates/builder.py` build game environments, not data pipelines.

Why not 1 point: Even basic file loading for evaluation data doesn't exist. This is fundamentally not an evaluation framework for models on datasets.

### S1F2: Model and Backend Configuration (0 points)

Evidence of absence:
- Bot-based, not model-based: From `meltingpot/configs/bots/__init__.py`:
  ```python
  def _saved_model(substrate: str, model: str) -> BotConfig:
    """Creates a saved model bot."""
    return BotConfig(
        substrate=substrate,
        model_path=os.path.join(MODELS_ROOT, substrate, model),
    )
  ```
  These are pre-trained RL agents, not configurable LLM inference endpoints.

- No provider support: No mentions of OpenAI, Anthropic, HuggingFace APIs, vLLM, etc. The framework uses TensorFlow SavedModels stored locally in `meltingpot/assets/saved_models/`.

- Example integration: `examples/rllib/self_play_train.py` shows RLlib training integration:
  ```python
  config = ppo.PPOConfig()
  config.num_rollout_workers = num_rollout_workers
  ```
  This is for training RL agents, not configuring LLM inference.

Why not 1 point: There's no concept of model provider configuration. The framework is for multi-agent RL simulation, not LLM evaluation.

### S1F3: Evaluation Parameters and Prompt Configuration (0 points)

Evidence of absence:
- Action-based, not text-based: From `fruit_market.py`:
  ```python
  NOOP = {"move": 0, "turn": 0, "eat_apple": 0, "eat_banana": 0, ...}
  FORWARD = {"move": 1, "turn": 0, "eat_apple": 0, "eat_banana": 0, ...}
  ACTION_SET = (NOOP, FORWARD, BACKWARD, ...)
  ```
  These are discrete gridworld actions, not LLM generation parameters.

- No templating: No Jinja2, prompt versioning, or variable substitution. The substrates use Lua scripts for game logic, not prompts.

- Configuration format: From `predator_prey__random_forest.py`:
  ```python
  config.timestep_spec = specs.timestep({
      "RGB": specs.OBSERVATION["RGB"],
      "STAMINA": specs.float64(),
      "WORLD.RGB": specs.rgb(152, 184),
  })
  ```
  This defines observation spaces for RL, not evaluation metrics for LLMs.

Why not 1 point: This is a fundamental mismatch—Melting Pot evaluates RL agents in game environments, not LLMs with prompts.

### S1F4: Environment Setup and Dependency Management (2 points)

Positive evidence:
- Pinned dependencies: `requirements.txt` uses hashed requirements:
  ```
  absl-py==2.1.0 \
      --hash=sha256:... \
      --hash=sha256:...
  ```

- Container support: `.devcontainer/devcontainer.json` exists with:
  ```json
  {
    "name": "Melting Pot Dev Container",
    "build": {"dockerfile": "Dockerfile"},
    "customizations": {...}
  }
  ```

- Setup automation: `bin/install.sh` provides installation:
  ```bash
  pip install --no-deps --require-hashes --requirement requirements.txt
  pip install --no-deps --no-index --no-build-isolation --editable .
  ```

Negative evidence (why not 3 points):
- Manual steps required: From `README.md`:
  ```markdown
  1. Clone Melting Pot
  2. (Optional) Activate a virtual environment
  3. Install Melting Pot: pip install --editable .[dev]
  4. (Optional) Test the installation
  ```

- Complex asset handling: `setup.py` shows non-trivial asset download:
  ```python
  class BuildPy(build_py.build_py):
    def download_and_extract_assets(self):
      tar_file_path = os.path.join(...)
      urllib.request.urlretrieve(ASSETS_URL, filename=tmp_path)
  ```

- Platform limitations: From README:
  ```markdown
  NOTE: This Devcontainer only works for x86 platforms. For arm64 (newer M1 Macs)
  users will have to follow the manual installation steps.
  ```

Justification for 2 points: Good dependency management and container support exist, but setup requires manual intervention, has platform-specific issues, and involves downloading 100+ MB of assets.

### S1F5: Security and Access Control (0 points)

Evidence of absence:
- No authentication: `examples/rllib/utils.py` shows direct instantiation:
  ```python
  def env_creator(env_config):
    env = substrate.build(env_config['substrate'], roles=env_config['roles'])
    env = MeltingPotEnv(env)
    return env
  ```

- No access control mentions: Searching for "RBAC", "auth", "credentials", "vault" yields no results in core framework files.

- Research/local use focus: From `README.md`:
  ```markdown
  We hope Melting Pot will become a standard benchmark for multi-agent
  reinforcement learning. We plan to maintain it...
  ```
  This positions it as a research tool, not enterprise software.

Why not 1 point: No security features exist at all. This is appropriate for a research simulation framework but means 0 points for evaluation security.

### S1F6: Cost Estimation and Budget Planning (0 points)

Evidence of absence:
- Simulation-based, not API-based: Configs specify simulation parameters, not API costs. From `fruit_market.py`:
  ```python
  substrate_definition = dict(
      maxEpisodeLengthFrames=1000,
      topology="BOUNDED",
      simulation={...}
  )
  ```

- No cost modeling: No references to tokens, pricing, budgets, or cost optimization in any config or utility file.

- No resource projection: The framework tracks simulation steps (frames), not inference tokens. From `predator_prey__random_forest.py`:
  ```python
  config.timestep_spec = specs.timestep({...})
  ```

Why not 1 point: Cost estimation is not applicable to this framework. It simulates RL environments locally, not API-based LLM inference.

## Final Checklist

- [x] All 6 features rated (S1F1 through S1F6)
- [x] Every rating has evidence (code snippets, file paths)
- [x] Justifications are concise (2-4 sentences)
- [x] Consistent rating standards across features

## Key Takeaway

Melting Pot is not an LLM evaluation framework. It's a multi-agent reinforcement learning benchmark suite for evaluating RL agents in game-like substrates. The Stage 1 evaluation criteria assume a framework for configuring datasets, models, prompts, and metrics for LLM evaluation—concepts that don't apply here. The framework excels at what it's designed for (RL simulation environments) but scores 0 on 5/6 Stage 1 features because it serves a fundamentally different purpose. Only environment setup (S1F4) receives partial credit for general software engineering practices.