# Overcooked AI - Stage 6 (SHIP) Evaluation

## Summary

The Overcooked AI repository is a research environment for cooperative human-AI gameplay, not a traditional LLM evaluation framework. It has minimal to no support for Stage 6 communication features. The repository focuses on game mechanics, agent training, and data collection rather than result packaging, versioning, and distribution of evaluation artifacts. Some basic data collection exists but lacks sophisticated artifact management, versioning, or reporting capabilities.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 0 | No systematic artifact management, capture, or querying capabilities |
| S6F2: Version Control | 0 | No git integration, dependency tracking, or reproducibility manifests |
| S6F3: Report Generation | 0 | No automated report generation, stakeholder templates, or rich visualizations |
| S6F4: Distribution Channels | 0 | No CI/CD integration, MLOps platform connections, or notification systems |

---

## Detailed Analysis

### S6F1: Evaluation Artifact Management

Rating: 0/3

Evidence:

1. No Runtime Capture System: The repository lacks automatic metadata capture during execution. The only data collection occurs in game trajectories:

```python
# src/overcooked_demo/server/game.py, lines 393-410
transition = {
    "state": json.dumps(prev_state.to_dict()),
    "joint_action": json.dumps(joint_action),
    "reward": curr_reward,
    "time_left": max(self.max_time - (time() - self.start_time), 0),
    "score": self.score,
    "time_elapsed": time() - self.start_time,
    "cur_gameloop": self.curr_tick,
    "layout": json.dumps(self.mdp.terrain_mtx),
    "layout_name": self.curr_layout,
    "trial_id": str(self.start_time),
    "player_0_id": self.players[0],
    "player_1_id": self.players[1],
    "player_0_is_human": self.players[0] in self.human_players,
    "player_1_is_human": self.players[1] in self.human_players,
}
self.trajectory.append(transition)
```

This is minimal game state tracking, not comprehensive artifact management.

2. No Querying Capabilities: There's no API or interface for querying past runs. Data is simply pickled:

```python
# src/overcooked_demo/server/game.py, lines 594-603
def get_data(self):
    """
    Returns and then clears the accumulated trajectory
    """
    data = {
        "uid": str(time()),
        "trajectory": self.trajectory,
    }
    self.trajectory = []
    # if we want to store the data and there is data to store
    if self.write_data and len(data["trajectory"]) > 0:
```

No search, filtering, or comparison tools exist.

3. No Packaging System: Data is saved as raw pickle files with no bundling, compression, or structured archiving:

```python
# src/overcooked_demo/server/game.py, lines 604-609
configs = self.write_config
# create necessary dirs
data_path = create_dirs(configs, self.curr_layout)
# the 3-layer-directory structure should be able to uniquely define any experiment
with open(os.path.join(data_path, "result.pkl"), "wb") as f:
    pickle.dump(data, f)
```

4. Basic Directory Structure Only: The only organization is through directory structure:

```python
# src/overcooked_demo/server/utils.py, lines 73-88
def create_dirs(config: dict, cur_layout: str):
    """
    config has 3 keys:
     {"time": datetime.today().strftime("%Y-%m-%d_%H-%M-%S"),
      "type": gameType/a str of either "HH","HA","AH","AA",
      "layout": a layout string}
    We group the data by layout/type/time
    """
    path = os.path.join(
        DOCKER_VOLUME,
        cur_layout,
        config["old_dynamics"],
        config["type"],
        config["time"],
    )
    if not os.path.exists(path):
        os.makedirs(path)
    return path
```

Justification: No artifact management system exists. Basic trajectory logging with manual directory organization doesn't constitute an artifact management system.

---

### S6F2: Archival Version Control and Reproducibility Manifests

Rating: 0/3

Evidence:

1. No Git Integration: No automatic commit tracking or git operations:

```bash
# No .git hooks or tracking code found in repository
# Only manual version tracking through directory names
```

2. No Dependency Pinning: While there are requirements files, they're not captured per-run:

```txt
# src/overcooked_demo/server/requirements.txt
certifi==2020.6.20
click==8.0
dnspython==1.16.0
# ... etc
```

But these are static, not captured at runtime per experiment.

3. No Environment Capture: No recording of Python version, CUDA, OS, or environment variables during runs. The only configuration is manual:

```json
# src/overcooked_demo/server/config.json
{
    "logfile" : "app.log",
    "layouts" : ["cramped_room", ...],
    "MAX_GAMES" : 10,
    "MAX_GAME_LENGTH" : 120,
    ...
}
```

4. No Reproducibility Manifests: No manifest generation. The only documentation is in README:

```md
# README.md
## Installation
You can install the pre-compiled wheel file using pip.
```

No automated capture of reproduction requirements.

5. No Container Packaging: While Docker is used for deployment, there's no automatic containerization of experiments:

```yml
# src/overcooked_demo/docker-compose.yml
version : '3.7'
services:
    app:
        build:
            context: ./server
            args:
                BUILD_ENV: "${BUILD_ENV:-production}"
```

This is for server deployment, not experiment reproduction.

Justification: No versioning or reproducibility features exist. The repository has standard development dependencies but no experiment-level tracking.

---

### S6F3: Stakeholder-Specific Report and Visualization Generation

Rating: 0/3

Evidence:

1. No Report Generation: No automated reporting system. The only visualization is a basic interactive widget in a notebook:

```python
# Overcooked Tutorial.ipynb, cell output
StateVisualizer().display_rendered_trajectory(trajs, ipython_display=True)
```

This is a manual, one-off visualization, not an automated report.

2. No Format Support: No HTML, PDF, JSON exports for results. Only raw pickle files:

```python
# src/overcooked_demo/server/game.py
with open(os.path.join(data_path, "result.pkl"), "wb") as f:
    pickle.dump(data, f)
```

3. No Stakeholder Templates: No templates for different audiences. The only example is a manual plotting script:

```python
# src/human_aware_rl/ppo/plot_example_experiments.py, lines 56-80
def plot_statistics(dict):
    names = []
    stds = []
    means = []
    for env in dict:
        names.append(env)
        stds.append(dict[env]["std"])
        means.append(dict[env]["mean"])

    x_pos = np.arange(len(names))
    matplotlib.rc("xtick", labelsize=7)
    fig, ax = plt.subplots()
    ax.bar(
        x_pos,
        means,
        yerr=stds,
        align="center",
        alpha=0.5,
        ecolor="black",
        capsize=10,
    )
```

This is a single-purpose script, not a flexible reporting system.

4. Basic Visualization Only: The StateVisualizer is minimal:

```python
# From tutorial notebook
StateVisualizer().display_rendered_trajectory(trajs, ipython_display=True)
```

No confusion matrices, ROC curves, calibration plots, or comprehensive visualizations.

5. No Automation: All visualization is manual. No scheduled reports, no automatic generation on run completion.

Justification: No reporting infrastructure exists. Only manual, ad-hoc visualization through notebooks and custom scripts.

---

### S6F4: Publication to Distribution Channels

Rating: 0/3

Evidence:

1. No CI/CD Integration: The repository has GitHub Actions tests but no integration with evaluation results:

```yaml
# .github/workflows/pythontests.yml (referenced in README badges but file not shown)
# Only basic unit tests, no evaluation pipeline
```

The README shows test badges but no evaluation automation:

```md
![MDP python tests](https://github.com/HumanCompatibleAI/overcooked_ai/workflows/.github/workflows/pythontests.yml/badge.svg)
```

2. No MLOps Platform Integration: No code for MLflow, W&B, Neptune, Comet, or any experiment tracking platforms. Agent training uses deprecated RLlib:

```md
# src/human_aware_rl/README.md
NOTE + LOOKING FOR CONTRIBUTORS: DRL and BC implementations are now deprecated.
```

3. No Leaderboard Support: No HuggingFace Hub, Papers with Code, or custom leaderboard integration. The demo server is for gameplay only:

```python
# src/overcooked_demo/server/app.py
# Only game hosting code, no leaderboard submission
@app.route("/")
def index():
    agent_names = get_agent_names()
    return render_template(
        "index.html", agent_names=agent_names, layouts=LAYOUTS
    )
```

4. No Notification System: No Slack, email, webhook support. The only "notifications" are socket.io messages for game state:

```python
# src/overcooked_demo/server/app.py, lines 666-671
socketio.emit(
    "state_pong", {"state": game.get_state()}, room=game.id
)
```

This is for real-time gameplay, not evaluation alerts.

5. Manual Agent Distribution: Agents must be manually copied:

```python
# src/overcooked_demo/server/move_agents.py, lines 35-52
# Manual script to copy agent checkpoints
parser.add_argument(
    "checkpoint",
    help="The path to the checkpoint directory, e.g. ~/ray_results/run_xyz/checkpoint_000500",
)
parser.add_argument(
    "agent_name",
    help="The name you want for this agent; remember to follow the naming conventions: the name must start with 'Rllib'",
)
```

No automated publishing.

Justification: No distribution infrastructure exists. The repository is self-contained with manual processes for sharing agents and results.

---

## Overall Assessment

Total Score: 0/12

This repository is fundamentally not an evaluation framework. It's a cooperative game environment for studying human-AI interaction. The absence of Stage 6 features is expected given its purpose:

### What Exists:
- Game state trajectory logging (basic)
- Manual data export to pickle files
- Directory-based organization
- Ad-hoc visualization scripts
- Docker deployment for game server

### What's Missing:
- All artifact management features
- All versioning and reproducibility features
- All automated reporting features
- All distribution and integration features

### Why This Makes Sense:
The repository serves a different purpose than typical evaluation frameworks. It focuses on:
1. Providing a game environment
2. Collecting human gameplay data
3. Training cooperative agents
4. Running interactive demos

The "evaluation" in this context means testing agents in gameplay, not comprehensive ML model evaluation with artifact management and reporting.

### Recommendation:
This repository should not be evaluated as a Stage 6-capable framework. It lacks even basic features in all four categories. If one needed to add Stage 6 capabilities, it would require building an entirely new system on top of or alongside the existing game infrastructure.