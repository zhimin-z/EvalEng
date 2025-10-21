# Overcooked-AI - Stage 4 (EVALUATE) Evaluation

## Summary
Overcooked-AI is a cooperative multi-agent game environment for research, not an evaluation framework. It lacks the metric computation, validation, and statistical analysis capabilities required for a Stage 4 evaluation framework. The repository focuses on game logic, agent training (deprecated), and human-AI interaction rather than systematic output evaluation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation features exist. The codebase focuses on game state transitions and MDP logic without any output validation, normalization, or policy compliance checking mechanisms. |
| S4F2: Metric Computation | 0 | No metric library exists. Only basic game scoring (soup deliveries) is tracked. No standard NLP/ML metrics (BLEU, ROUGE, F1, etc.) are implemented or referenced. |
| S4F3: Evaluator Models | 0 | No evaluator model integration exists. While the code references AI agents (BC, PPO), these are game-playing agents, not evaluation models. No LLM-as-judge or specialized evaluators are present. |
| S4F4: Multi-Modal Scoring | 0 | Text-only environment with no multi-modal capabilities. The game operates on discrete grid states without image, audio, or video evaluation components. |
| S4F5: Aggregate Statistics | 0 | No statistical analysis framework. Only basic episode returns are tracked. No significance testing, distribution analysis, or model comparison capabilities exist. |

## Detailed Analysis

### S4F1: Output Validation and Normalization

Rating: 0/3

Evidence:

The repository contains game logic for state transitions but no output validation mechanisms:

```python
# From src/overcooked_demo/server/game.py
def apply_actions(self):
    # Default joint action, as NPC policies and clients probably don't enqueue actions fast
    # enough to produce one at every tick
    joint_action = [Action.STAY] * len(self.players)
    
    # Apply overcooked game logic to get state transition
    prev_state = self.state
    self.state, info = self.mdp.get_state_transition(
        prev_state, joint_action
    )
```

The code applies actions directly to the MDP without any validation of:
- Action format correctness
- Policy compliance checks
- Sanity checks on outputs
- Normalization of different formats

No validation features exist - actions are simply mapped and applied:

```python
# From src/overcooked_demo/server/game.py
self.action_to_overcooked_action = {
    "STAY": Action.STAY,
    "UP": Direction.NORTH,
    "DOWN": Direction.SOUTH,
    "LEFT": Direction.WEST,
    "RIGHT": Direction.EAST,
    "SPACE": Action.INTERACT,
}
```

This is a simple dictionary mapping with no validation logic.

### S4F2: Task-Specific Metric Computation

Rating: 0/3

Evidence:

The only "metric" is the game score (soup deliveries):

```python
# From src/overcooked_demo/server/game.py
def apply_actions(self):
    # ... state transition ...
    
    # Update score based on soup deliveries that might have occured
    curr_reward = sum(info["sparse_reward_by_agent"])
    self.score += curr_reward
```

No metric library exists. The evaluation notebook shows only basic trajectory collection:

```python
# From Overcooked Tutorial.ipynb
trajs = ae.evaluate_agent_pair(ap, 10)
trajs["ep_returns"]  # array([80, 40, 80, 40, 80, 80, 20, 60, 80, 20])
```

No standard metrics like:
- BLEU, ROUGE, METEOR (text generation)
- Precision, Recall, F1 (classification)
- P@k, NDCG (retrieval)
- Custom metric definitions

The data collection only tracks game events:

```python
# From src/overcooked_demo/server/game.py
transition = {
    "state": json.dumps(prev_state.to_dict()),
    "joint_action": json.dumps(joint_action),
    "reward": curr_reward,
    "time_left": max(self.max_time - (time() - self.start_time), 0),
    "score": self.score,
    # ... basic game stats only
}
```

### S4F3: Evaluator Model Integration

Rating: 0/3

Evidence:

While the codebase references AI agents, these are game-playing agents, not evaluation models:

```python
# From src/overcooked_demo/server/game.py
def get_policy(self, npc_id, idx=0):
    if npc_id.lower().startswith("rllib"):
        try:
            # Loading rllib agents requires additional helpers
            fpath = os.path.join(AGENT_DIR, npc_id, "agent")
            fix_bc_path(fpath)
            agent = load_agent(fpath, agent_index=idx)
            return agent
```

These agents play the game, they don't evaluate outputs. No evidence of:
- LLM-as-judge implementations
- Pre-built judge prompts
- Evaluator rationale capture
- Ensemble scoring strategies

The README mentions deprecated training code:

```markdown
# From README.md
NOTE + LOOKING FOR CONTRIBUTORS: DRL and BC implementations are now deprecated.
```

Even when training was supported, it was for game-playing, not evaluation.

### S4F4: Multi-Modal Scoring Protocols

Rating: 0/3

Evidence:

The environment is purely text/symbolic based on grid states:

```python
# From README.md
## Introduction 🥘
Overcooked-AI is a benchmark environment for fully cooperative human-AI task performance
```

The state representation is discrete grid-based:

```python
# From src/overcooked_demo/server/game.py
def get_state(self):
    state_dict = {}
    state_dict["potential"] = self.phi if self.show_potential else None
    state_dict["state"] = self.state.to_dict()
    state_dict["score"] = self.score
    state_dict["time_left"] = max(
        self.max_time - (time() - self.start_time), 0
    )
    return state_dict
```

No multi-modal capabilities:
- No image processing (only 2D grid visualization)
- No audio/video evaluation
- No cross-modal metrics
- Text-only state representation

### S4F5: Aggregate Statistics and Cross-Model Comparison

Rating: 0/3

Evidence:

The only aggregation is averaging episode returns:

```python
# From src/human_aware_rl/ppo/plot_example_experiments.py
def get_statistics(dict):
    for env in dict:
        rewards = [
            get_last_episode_rewards(file + "/result.json")[
                "sparse_reward_mean"
            ]
            for file in dict[env]["files"]
        ]
        dict[env]["rewards"] = rewards
        dict[env]["std"] = np.std(rewards)  # Only std
        dict[env]["mean"] = np.mean(rewards)  # Only mean
    return dict
```

No statistical analysis framework:
- No confidence intervals
- No significance testing (t-test, Wilcoxon)
- No distribution analysis
- No ranking systems (Elo, TrueSkill)
- No model comparison utilities

The evaluation code only collects trajectories:

```python
# From Overcooked Tutorial.ipynb
trajs = ae.evaluate_agent_pair(ap_bc, 10)
# Returns raw trajectory data, no statistics
```

The plotting code creates simple bar charts with error bars:

```python
# From src/human_aware_rl/ppo/plot_example_experiments.py
def plot_statistics(dict):
    # ... 
    ax.bar(
        x_pos,
        means,
        yerr=stds,  # Only mean and std, no CI or tests
        align="center",
        alpha=0.5,
        ecolor="black",
        capsize=10,
    )
```

## Conclusion

Total Score: 0/15

Overcooked-AI is fundamentally not an evaluation framework - it is a game environment for multi-agent RL research. It lacks all Stage 4 evaluation capabilities:

1. No validation infrastructure - actions are applied directly without checks
2. No metric library - only game scores are tracked
3. No evaluator models - agents play the game, they don't evaluate
4. No multi-modal support - discrete grid states only
5. No statistical analysis - only basic mean/std computation

The repository would need to be completely restructured with new modules for metric computation, validation, and statistical analysis to function as an evaluation framework. The current codebase serves an entirely different purpose - providing a cooperative game environment for studying human-AI coordination.