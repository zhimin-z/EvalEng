# Overcooked-AI - Stage 1 (CONFIGURE) Evaluation

## Summary
Overcooked-AI is a multi-agent reinforcement learning research environment simulating a cooperative cooking game. It is NOT an evaluation framework - it's a research environment/simulator for training and testing cooperative AI agents. The repository provides game environments, agent implementations, and demo interfaces, but lacks the systematic configuration management, dataset handling, and evaluation infrastructure expected of a proper evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No dataset configuration system exists. Human gameplay data is stored as static pickled dataframes with no registration, versioning, or schema APIs. See `src/human_aware_rl/static/human_data/README.md` - data is just raw CSV/pickle files with manual processing scripts. |
| S1F2: Model Configuration | 1 | Minimal agent loading via hardcoded paths. `src/overcooked_demo/server/game.py:415-430` shows basic pickle loading with no provider abstraction, no YAML/JSON config system, and hardcoded directory structures (`AGENT_DIR`). Authentication and resource allocation completely absent. |
| S1F3: Prompt Configuration | 0 | Not applicable - this is an RL environment, not an LLM evaluation framework. No prompt templates, parameter sweeps, or metric configuration exists. The "evaluation" is game score, not LLM outputs. |
| S1F4: Environment Setup | 2 | Has `setup.py`, `pyproject.toml`, and `uv.lock` for dependencies. Docker support exists (`src/overcooked_demo/docker-compose.yml`). However, no automated setup scripts, unclear hardware requirements, and dependencies not well-documented. From `README.md:69-75`: only basic pip/uv install instructions. |
| S1F5: Security & Access | 0 | No security features whatsoever. No credential management, access control, audit logging, or enterprise integration. The demo server (`src/overcooked_demo/server/app.py`) has no authentication - anyone can join games. |
| S1F6: Cost Estimation | 0 | No cost modeling exists. This is a local simulation environment with no API calls or cloud resources to estimate. The concept doesn't apply to this type of research tool. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (0/3)

Evidence of absence:

The repository contains human gameplay data but no dataset configuration system:

```python
# From src/human_aware_rl/static/human_data/README.md
# Data is just stored as static files with manual processing
raw/  # Raw CSV files
cleaned/  # Processed pickle files
dummy/  # Test subset
```

The data processing is entirely manual:
```python
# From src/human_aware_rl/human/process_dataframes.py:30
def csv_to_df_pickle(path, layouts, check_trajectories=True):
    """
    Loads, processes, and filters raw CSV data and saves as pickled DataFrame
    """
    # Manual file loading with hardcoded paths, no registration system
```

Why this fails:
- No dataset registration API
- No schema definition capabilities
- No declarative split strategies
- No versioning system beyond manual directory names
- Data must be manually processed with custom scripts

Rating: 0 points - No dataset abstraction layer exists.

### S1F2: Model and Backend Configuration (1/3)

Evidence of minimal functionality:

```python
# From src/overcooked_demo/server/game.py:415-430
def get_policy(self, npc_id, idx=0):
    if npc_id.lower().startswith("rllib"):
        try:
            fpath = os.path.join(AGENT_DIR, npc_id, "agent")
            fix_bc_path(fpath)  # Manual path fixing
            agent = load_agent(fpath, agent_index=idx)
            return agent
        except Exception as e:
            raise IOError("Error loading Rllib Agent\n{}".format(e.__repr__()))
    else:
        try:
            fpath = os.path.join(AGENT_DIR, npc_id, "agent.pickle")
            with open(fpath, "rb") as f:
                return pickle.load(f)
```

Configuration is hardcoded:
```python
# From src/overcooked_demo/server/config.json
{
    "AGENT_DIR" : "./static/assets/agents",
    "MAX_GAME_LENGTH" : 120,
    "MAX_GAMES" : 10
}
```

Why this gets only 1 point:
- Only 2 "providers": RLlib checkpoints and pickle files
- No unified configuration API - just hardcoded paths
- No authentication system
- No resource allocation
- Manual path management with brittle string matching

Rating: 1 point - Bare minimum agent loading exists but requires manual file management.

### S1F3: Prompt Configuration (0/3)

Not Applicable - This is a reinforcement learning game environment, not an LLM evaluation framework. There are no:
- Prompts or templates
- Language model interactions
- Parameter configurations for text generation
- Metric computations beyond game scores

```python
# From src/overcooked_ai_py/mdp/overcooked_env.py
# The "evaluation" is just game simulation
class OvercookedEnv:
    def step(self, joint_action):
        """Apply action and return standard gym tuple"""
        next_state, sparse_reward, dense_reward, info = self.mdp.get_state_transition(
            prev_state, joint_action, display_phi, motion_planner
        )
```

Rating: 0 points - Feature category doesn't apply to this type of system.

### S1F4: Environment Setup (2/3)

Evidence of partial support:

Dependency specification exists:
```toml
# From pyproject.toml:11-34
[project]
name = "overcooked-ai"
dependencies = [
    "numpy>=1.24.0,<2.0.0",
    "scipy>=1.10.0",
    "tqdm>=4.66.0",
    "gym>=0.21.0",
    "matplotlib>=3.7.0",
    # ... more dependencies
]
```

Docker support:
```yaml
# From src/overcooked_demo/docker-compose.yml
services:
    app:
        build:
            context: ./server
            args:
                BUILD_ENV: "${BUILD_ENV:-production}"
```

Installation instructions:
```bash
# From README.md:69-75
# Installing from PyPI
pip install overcooked-ai

# Building from source
git clone https://github.com/HumanCompatibleAI/overcooked_ai.git
uv venv
uv sync
```

Why this gets 2 points:
- ✅ Has requirements files (pyproject.toml, uv.lock)
- ✅ Docker support exists
- ✅ Basic setup instructions provided
- ❌ No automated setup scripts (just manual commands)
- ❌ Hardware requirements not documented
- ❌ No environment validation on startup
- ❌ GPU/CPU configuration not addressed

Rating: 2 points - Basic dependency management and containerization exist, but setup is manual.

### S1F5: Security and Access Control (0/3)

Evidence of complete absence:

The demo server has no authentication:
```python
# From src/overcooked_demo/server/app.py:229-237
@socketio.on("connect")
def on_connect():
    user_id = request.sid  # Just uses session ID, no auth
    if user_id in USERS:
        return
    USERS[user_id] = Lock()
```

No credential management:
```python
# From src/overcooked_demo/server/game.py:15-20
# Agent directory is just a global path string
AGENT_DIR = None
def _configure(max_game_time, agent_dir):
    global AGENT_DIR, MAX_GAME_TIME
    MAX_GAME_TIME = max_game_time
    AGENT_DIR = agent_dir  # No encryption, no vault, no security
```

Why this gets 0 points:
- No authentication system
- No credential management (not even env vars)
- No access control or RBAC
- No audit logging
- No enterprise integrations
- Anyone can connect to the demo server

Rating: 0 points - Zero security features.

### S1F6: Cost Estimation (0/3)

Not Applicable - This is a local simulation environment. There are no:
- API calls to track
- Cloud resources to monitor
- Token usage to count
- Cost models to compute

```python
# From src/overcooked_ai_py/mdp/overcooked_mdp.py
# All computation is local simulation
class OvercookedGridworld:
    def get_state_transition(self, state, joint_action):
        """Pure simulation - no external costs"""
        # Local game logic only
```

Rating: 0 points - Feature doesn't apply to this type of system.

## Critical Issues

### 1. Fundamental Misalignment
This repository is a research environment for multi-agent RL, not an evaluation framework. It would be like evaluating a gym as a fitness tracking app - wrong category entirely.

### 2. No Evaluation Infrastructure
The repository lacks:
- No evaluation campaign management
- No experiment tracking beyond manual directories
- No metric aggregation or reporting
- No comparison tools between agents

### 3. Deprecated Core Functionality
```markdown
# From README.md:21-22
NOTE + LOOKING FOR CONTRIBUTORS: DRL and BC implementations are now deprecated.
```
The training code that would enable evaluation is explicitly deprecated.

### 4. Manual Everything
- Dataset processing requires custom scripts
- Agent loading requires hardcoded paths
- Results must be manually collected
- No automation anywhere

## Strengths

1. Clear Documentation - The README and tutorial notebook are well-written
2. Research Purpose - Excellent for its intended use (RL research environment)
3. Docker Support - Demo can be containerized
4. Active Maintenance - Code is actively used in research

## Final Assessment

Total Score: 3/18 (16.7%)

Recommendation: This repository should NOT be evaluated as an LLM evaluation framework. It's a multi-agent reinforcement learning research environment with a completely different purpose. The low score reflects category mismatch, not poor quality - Overcooked-AI is well-designed for its actual purpose (cooperative AI research in game environments).

If you need to evaluate RL environments specifically, a different rubric focused on:
- Environment configuration
- Agent interfaces
- Episode management
- Reward shaping
- Multi-agent coordination

Would be more appropriate.