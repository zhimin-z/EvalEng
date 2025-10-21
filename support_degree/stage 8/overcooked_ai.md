# Overcooked-AI - Stage 8 (MONITOR) Evaluation

## Summary
Overcooked-AI is a cooperative multi-agent RL research environment, not an evaluation framework. It provides game logic, training infrastructure, and human-AI interaction tools, but lacks any production monitoring, drift detection, feedback loops, or continuous improvement features typical of Stage 8 evaluation frameworks. The repository is designed for training and offline evaluation of RL agents, not for monitoring deployed models.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities exist. The codebase is purely for training/offline evaluation with no production monitoring infrastructure. |
| S8F2: Online Evaluation | 0 | No online or streaming evaluation. Only offline trajectory evaluation via `AgentEvaluator.evaluate_agent_pair()`. No A/B testing, shadow deployment, or automated rollback. |
| S8F3: Feedback Integration | 0 | No feedback loop integration. Human data collection exists (`src/human_aware_rl/static/human_data/`) but is static/offline only, not for continuous feedback ingestion. |
| S8F4: Improvement Planning | 0 | No automated improvement recommendations, root cause analysis, or roadmap generation. Only raw trajectory data and manual analysis via notebooks. |

## Detailed Analysis

### S8F1: Production Drift Monitoring (0/3 points)

Evidence of absence:

The repository contains no drift monitoring capabilities whatsoever:

1. No statistical tests: Searching through the codebase reveals no KS tests, chi-square tests, MMD, or any distribution shift detection. The evaluation code in `src/overcooked_ai_py/agents/benchmarking.py` only computes basic metrics:

```python
def evaluate_agent_pair(self, ap, num_games=1, game_length=None, info=True):
    # ... trajectory collection only
    return trajs
```

2. No performance tracking: The `AgentEvaluator` class only stores raw trajectories without any time-series analysis, anomaly detection, or performance degradation tracking:

```python
# From src/overcooked_ai_py/agents/benchmarking.py
class AgentEvaluator:
    def evaluate_agent_pair(self, ap, num_games=1, game_length=None, info=True):
        # Only returns raw trajectory data
        trajs = {
            "ep_states": [],
            "ep_actions": [],
            "ep_rewards": [],
            # ... no drift metrics
        }
```

3. No alerting infrastructure: No configuration files, alert systems, or monitoring integrations exist. The demo server (`src/overcooked_demo/server/app.py`) is purely for game hosting, not monitoring.

4. Static data collection only: The human data directory (`src/human_aware_rl/static/human_data/`) contains historical data for training, not live production monitoring:

```python
# From src/human_aware_rl/static/human_data/README.md
# Data was collected through Mturk and is fully anonymized
# This is STATIC historical data, not live monitoring
```

### S8F2: Online and Streaming Evaluation (0/3 points)

Evidence of absence:

1. Only offline evaluation: The tutorial notebook (`Overcooked Tutorial.ipynb`) shows the evaluation pattern:

```python
# From Overcooked Tutorial.ipynb
ae = AgentEvaluator.from_layout_name(mdp_params={...})
trajs = ae.evaluate_agent_pair(ap, 10)  # Offline batch evaluation only
```

2. No A/B testing framework: The demo server supports human-AI gameplay but not experimentation:

```python
# From src/overcooked_demo/server/app.py
# Only supports basic game creation, no traffic splitting:
def _create_game(user_id, game_name, params={}):
    game, err = try_create_game(game_name, params)
    # No variant testing, traffic splitting, or gradual rollout
```

3. No shadow deployment: Games run in isolation with no side-by-side comparison or production impact measurement.

4. No automated rollback: The game server has basic error handling but no metric-based rollback triggers:

```python
# From src/overcooked_demo/server/game.py
def play_game(game: OvercookedGame, fps=6):
    status = Game.Status.ACTIVE
    while status != Game.Status.DONE:
        # Simple game loop, no rollback logic
        with game.lock:
            status = game.tick()
```

5. No streaming support: All evaluation is batch-based with complete trajectories:

```python
# From src/overcooked_ai_py/agents/benchmarking.py
# Collects full episodes, no sliding windows or real-time metrics
for _ in tqdm.trange(num_games):
    trajectory = self.env.run_agents(agents, include_final_state=True)
```

### S8F3: Feedback Loop Integration (0/3 points)

Evidence of absence:

1. Static data collection only: The data processing utilities show this is for offline analysis:

```python
# From src/human_aware_rl/human/process_dataframes.py
def csv_to_df_pickle(csv_path, processed_path):
    """
    Loads, processes, and filters raw CSV data and saves as pickled DataFrame
    """
    # This is offline batch processing, not real-time feedback ingestion
```

2. No production log parsing: The demo server saves game data but doesn't feed it back:

```python
# From src/overcooked_demo/server/game.py
def get_data(self):
    """Returns and then clears the accumulated trajectory"""
    data = {"uid": str(time()), "trajectory": self.trajectory}
    # Saves to file but no integration back into evaluation
    if self.write_data and len(data["trajectory"]) > 0:
        with open(os.path.join(data_path, "result.pkl"), "wb") as f:
            pickle.dump(data, f)
    return data
```

3. No failure mining: Trajectories contain errors but no automatic extraction:

```python
# From README.md for human data
# Schema includes 'state', 'joint_action', 'reward' but no failure categorization
NEW_SCHEMA = set(['state', 'joint_action', 'reward', ...])
# Manual analysis required, no automated failure detection
```

4. No metric updates: Metrics are hardcoded in the MDP definition with no dynamic updating:

```python
# From config.json
"layout_globals" : {
    "onion_value" : 21,
    "tomato_value" : 13,
    # Static values, no production-based updates
}
```

5. No closed-loop automation: The human aware RL training is completely separate from any deployment:

```python
# From src/human_aware_rl/README.md
# Training is separate from deployment:
# 1. Train BC/PPO agents offline
# 2. Load into demo server
# No automatic retraining based on production data
```

### S8F4: Iteration Planning and Improvement Recommendations (0/3 points)

Evidence of absence:

1. No root cause analysis: The evaluation returns raw game statistics without interpretation:

```python
# From src/overcooked_ai_py/mdp/overcooked_env.py
# Episode info contains raw counts, no analysis:
'ep_game_stats': {
    'tomato_pickup': [[], []],
    'onion_pickup': [[5, 78, ...], [6, 28, ...]],
    # Just raw timesteps, no pattern analysis or bottleneck identification
}
```

2. No hyperparameter recommendations: Training scripts use fixed configs:

```python
# From src/human_aware_rl/ppo/run_experiments.sh
# Fixed hyperparameters, no sensitivity analysis or recommendations
python ppo_rllib_client.py with lr=1e-3 layout_name=cramped_room
```

3. No prompt optimization: This is an RL environment, not an LLM framework, so N/A, but indicative of no optimization features.

4. No dataset expansion guidance: While the tutorial mentions data collection:

```python
# From src/overcooked_demo/README.md
# Data collection exists but no gap analysis or prioritization:
if params["dataCollection"] == "on":
    params["collection_config"] = {"time": ..., "type": gameType}
    # Just saves data, doesn't identify underrepresented scenarios
```

5. No roadmap generation: The plotting script only visualizes results:

```python
# From src/human_aware_rl/ppo/plot_example_experiments.py
def plot_statistics(dict):
    # Only plots final results, no experiment planning or impact estimates
    ax.bar(x_pos, means, yerr=stds, ...)
    plt.savefig("example_rewards.png")
```

6. Manual analysis required: The tutorial notebook shows all analysis is manual:

```python
# From Overcooked Tutorial.ipynb
trajs = ae.evaluate_agent_pair(ap_bc, 10)
trajs["ep_returns"]  # User must manually inspect results
StateVisualizer().display_rendered_trajectory(trajs)  # Manual visualization
```

## Conclusion

Overcooked-AI receives 0/12 points for Stage 8 (MONITOR) because it is fundamentally a training/research environment, not a production evaluation framework. It lacks:

- Any drift detection or monitoring capabilities
- Online evaluation, A/B testing, or streaming support  
- Feedback loop integration or closed-loop automation
- Automated improvement recommendations or root cause analysis

The repository is designed for offline research on human-AI cooperation in multi-agent RL, not for monitoring deployed models in production. While it has sophisticated training infrastructure and can collect human gameplay data, all evaluation is batch-based and requires manual analysis. There is no pathway from this codebase to production monitoring without building an entirely separate system.