# Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Multi-step agent evaluation with state evolution
- File: `testing/overcooked_test.py`, `testing/agent_test.py`, `testing/planners_test.py`
- Class/Function: `overcooked_ai_py.agents.benchmarking.AgentEvaluator`
- Code Reference:
```python
# From testing/overcooked_test.py
def test_run_agents(self):
    start_state = self.env.state
    self.env.run_agents(self.rnd_agent_pair)
    self.assertNotEqual(self.env.state, start_state)
```
The test files demonstrate the use of `AgentEvaluator` for simulating agent interactions over multiple timesteps, where agents interact with the environment and the state evolves based on their actions.

Evidence 2: Sequential multi-step environment interaction
- File: `testing/overcooked_test.py`
- Class/Function: `overcooked_ai_py.mdp.overcooked_env.OvercookedEnv.run_agents()`
- Code Reference:
```python
# From testing/overcooked_test.py
def test_one_player_env(self):
    mdp = OvercookedGridworld.from_layout_name("cramped_room_single")
    env = OvercookedEnv.from_mdp(mdp, horizon=12, info_level=0)
    a0 = FixedPlanAgent([stay, w, w, e, e, n, e, interact, w, n, interact])
    ag = AgentGroup(a0)
    env.run_agents(ag, display=False)
```
The `run_agents()` method enables sequential interaction where a `FixedPlanAgent` executes a series of actions over a defined horizon, with the environment responding to each action and maintaining state across the interaction sequence.

Evidence 3: Episode-based trajectory collection with feedback
- File: `testing/overcooked_test.py`
- Class/Function: `overcooked_ai_py.mdp.overcooked_env.OvercookedEnv.get_rollouts()`
- Code Reference:
```python
# From testing/overcooked_test.py
def test_rollouts(self):
    try:
        self.env.get_rollouts(self.rnd_agent_pair, 3, info=False)
    except Exception as e:
        print(e.with_traceback())
        self.fail("Failed to get rollouts from environment:\n{}".format(e))
```
The `get_rollouts()` method collects complete episode trajectories containing state-action sequences, enabling evaluation through feedback loops where agents observe the results of their actions over time.

Evidence 4: Multi-turn game simulation with state persistence
- File: `testing/planners_test.py`
- Code Reference:
```python
# From testing/planners_test.py
def test_mdp_dynamics(self):
    traj_path = os.path.join(TESTING_DATA_DIR, "test_mdp_dynamics", "expected.json")
    test_trajectory = AgentEvaluator.load_traj_from_json(traj_path)
    AgentEvaluator.check_trajectories(
        test_trajectory, from_json=True, verbose=False
    )
```
The environment maintains persistent state across multiple turns of the game, with trajectories capturing the full sequence of state transitions that result from agent decisions throughout the simulation.

Evidence 5: Agent evaluation with iterative action-state transitions
- File: `testing/agent_test.py`
- Code Reference:
```python
# From testing/agent_test.py
def test_human_model_pair(self):
    trajs = self.agent_eval.evaluate_human_model_pair()
    try:
        AgentEvaluator.check_trajectories(trajs, verbose=False)
    except AssertionError as e:
        self.fail(
            "Trajectories were not returned in standard format:\n{}".format(e)
        )
```
The evaluation process involves sequential decision-making where agents receive feedback from the environment after each action, enabling assessment of behavioral competence through extended interaction sequences with state evolution.

Evidence 6: Reinforcement learning environment with episodic interaction
- File: `src/human_aware_rl/ppo/ppo_rllib_test.py`
- Code Reference:
```python
# From src/human_aware_rl/ppo/ppo_rllib_test.py
def test_ppo_sp_no_phi(self):
    # Train a self play agent for 20 iterations
    results = ex.run(
        config_updates={
            "results_dir": self.temp_results_dir,
            "num_workers": 2,
            "train_batch_size": 800,
            "sgd_minibatch_size": 800,
            "num_training_iters": 30,
            "evaluation_interval": 10,
            "entropy_coeff_start": 0.0,
            "entropy_coeff_end": 0.0,
            "use_phi": False,
            "evaluation_display": False,
            "verbose": False,
        },
        options={"--loglevel": "ERROR"},
    ).result
```
PPO agents are trained through repeated interactions with the environment over 30 training iterations, learning from cumulative rewards and feedback across many episodes, demonstrating the harness's support for complex multi-step interaction with adaptive behavior.

Evidence 7: Multi-player cooperative game simulation
- File: `testing/overcooked_test.py`
- Code Reference:
```python
# From testing/overcooked_test.py
def test_four_player_env_fixed(self):
    mdp = OvercookedGridworld.from_layout_name("multiplayer_schelling")
    assert mdp.num_players == 4
    env = OvercookedEnv.from_mdp(mdp, horizon=16, info_level=0)
    a0 = FixedPlanAgent([stay, w, w])
    a1 = FixedPlanAgent([...])
    a2 = FixedPlanAgent([...])
    a3 = FixedPlanAgent([...])
    ag = AgentGroup(a0, a1, a2, a3)
    env.run_agents(ag, display=False)
```
The harness supports four-player cooperative scenarios where multiple agents interact simultaneously in a shared environment, requiring coordination and adaptation to each other's actions across the simulation.

Evidence 8: State evolution through MDP transitions
- File: `testing/overcooked_test.py`
- Code Reference:
```python
# From testing/overcooked_test.py
def test_transitions_and_environment(self):
    env = OvercookedEnv.from_mdp(self.base_mdp, info_level=0)
    
    def check_transition(action, expected_path, recompute=False):
        state = env.state
        pred_state, _ = self.base_mdp.get_state_transition(state, action)
        new_state, sparse_reward, _, _ = env.step(action)
```
The environment implements a Markov Decision Process where each state transition depends on the current state and joint actions, creating feedback loops essential for interactive simulation where future states depend on the history of interactions.