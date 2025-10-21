## Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Multi-step environment interactions with feedback loops
- File: `metaworld/evaluation.py`
- Function: `evaluation()` and `metalearning_evaluation()`
- Code Reference:
```python
def evaluation(
    agent: Agent,
    eval_envs: gym.vector.SyncVectorEnv | gym.vector.AsyncVectorEnv,
    num_episodes: int = 50,
) -> tuple[float, float, dict[str, float], dict[str, list[float]]]:
    # ... setup code ...
    
    while not eval_done(episodic_returns):
        actions = agent.eval_action(obs)
        obs, _, terminations, truncations, infos = eval_envs.step(actions)  # Environment interaction
        
        dones = np.logical_or(terminations, truncations)
        agent.reset(dones)  # Agent state management based on environment feedback
        
        for i, env_ended in enumerate(dones):
            if env_ended:
                episodic_returns[task_names[i]].append(
                    float(infos["final_info"]["episode"]["r"][i])
                )
                if len(episodic_returns[task_names[i]]) <= num_episodes:
                    successes[task_names[i]] += int(infos["final_info"]["success"][i])
```
The evaluation harness implements multi-step environment interactions where the agent repeatedly interacts with the environment via `eval_envs.step(actions)`. This creates feedback loops as the agent receives observations and info from the environment, adjusting behavior accordingly. Environment state changes based on agent actions, tracked through `terminations`, `truncations`, and `infos`. The iterative evaluation continues until evaluation criteria are met via `eval_done()`.

Evidence 2: Multi-phase interaction pattern with adaptation
- File: `metaworld/evaluation.py`
- Function: `metalearning_evaluation()`
- Code Reference:
```python
def metalearning_evaluation(
    agent: MetaLearningAgent,
    eval_envs: gym.vector.SyncVectorEnv | gym.vector.AsyncVectorEnv,
    num_evals: int = 10,
    adaptation_steps: int = 1,
    adaptation_episodes: int = 10,
    evaluation_episodes: int = 3,
) -> tuple[float, float, dict[str, float]]:
    # ... setup code ...
    
    for i in range(num_evals):
        eval_envs.call("sample_tasks")  # Environment reconfiguration
        agent.init()  # Agent initialization
        
        for _ in range(adaptation_steps):  # Adaptation phase
            obs, _ = eval_envs.reset()
            episodes_elapsed = np.zeros((eval_envs.num_envs,), dtype=np.uint16)
            
            while not (episodes_elapsed >= adaptation_episodes).all():
                actions, aux_policy_outs = agent.adapt_action(obs)
                next_obs, rewards, terminations, truncations, _ = eval_envs.step(actions)
                agent.step(
                    Timestep(obs, actions, rewards, terminations, truncations, aux_policy_outs)
                )  # Agent receives feedback and updates internal state
                episodes_elapsed += np.logical_or(terminations, truncations)
                obs = next_obs
            
            agent.adapt()  # Agent adaptation based on collected experience
        
        # Evaluation phase with adapted agent
        mean_success_rate, mean_return, _success_rate_per_task, _ = evaluation(
            agent, eval_envs, evaluation_episodes
        )
```
The meta-learning evaluation implements complex multi-step processes with separate adaptation and evaluation phases. The agent iteratively refines through `agent.step()` and `agent.adapt()` based on environment feedback. Environment and agent states evolve through multiple episodes, with the agent's actions informed by previous timesteps captured in `Timestep` objects, demonstrating feedback-driven behavior.

Evidence 3: Rich feedback and state transitions from environment
- File: `metaworld/sawyer_xyz_env.py`
- Class/Function: `SawyerXYZEnv.step()`
- Code Reference:
```python
def step(
    self, action: npt.NDArray[np.float32]
) -> tuple[npt.NDArray[np.float64], SupportsFloat, bool, bool, dict[str, Any]]:
    assert len(action) == 4, f"Actions should be size 4, got {len(action)}"
    self.set_xyz_action(action[:3])
    if self.curr_path_length >= self.max_path_length:
        raise ValueError("You must reset the env manually once truncate==True")
    self.do_simulation([action[-1], -action[-1]], n_frames=self.frame_skip)
    self.curr_path_length += 1
    
    # Running the simulator can sometimes mess up site positions, so
    # re-position them here to make sure they're accurate
    for site in self._target_site_config:
        self._set_pos_site(*site)
    
    # ... exception handling ...
    
    mujoco.mj_forward(self.model, self.data)
    self._last_stable_obs = self._get_obs()
    
    # ... observation clipping ...
    
    reward, info = self.evaluate_state(self._last_stable_obs, action)
    # step will never return a terminate==True if there is a success
    # but we can return truncate=True if the current path length == max path length
    truncate = False
    if self.curr_path_length == self.max_path_length:
        truncate = True
    return (
        np.array(self._last_stable_obs, dtype=np.float64),
        reward,
        False,
        truncate,
        info,
    )
```
The environment provides state evolution through physics simulation via `do_simulation()` and `mujoco.mj_forward()`. It returns rich feedback including observations, rewards, termination flags, and info dict with success metrics. The environment maintains persistent state by tracking `curr_path_length` and updating internal state across steps, with dynamic evaluation computing reward based on current state via `evaluate_state()`.

Evidence 4: Agent-environment interaction testing
- File: `tests/metaworld/test_evaluation.py`
- Function: `test_evaluation()`
- Code Reference:
```python
def test_evaluation():
    SEED = 42
    max_episode_steps = 300  # To speed up the test
    num_episodes = 50
    
    random.seed(SEED)
    np.random.seed(SEED)
    envs = gym.make_vec(
        "Meta-World/MT50",
        seed=SEED,
        max_episode_steps=max_episode_steps,
        vector_strategy="async",
    )
    agent = ScriptedPolicyAgent(envs)
    mean_success_rate, mean_returns, success_rate_per_task, _ = evaluation.evaluation(
        agent, envs, num_episodes=num_episodes
    )
    assert isinstance(mean_returns, float)
    assert mean_success_rate >= 0.80
    assert len(success_rate_per_task) == envs.num_envs
    assert np.all(np.array(list(success_rate_per_task.values())) >= 0.80)
```
This test confirms agent-environment interaction through actual environment simulation. The agent policies are evaluated through multi-episode evaluation to gather statistics, collecting performance metrics including success rates and returns across tasks.

Evidence 5: Evaluation methodology with adaptation phases
- File: `docs/evaluation/evaluation.md`
- Code Reference:
```markdown
### Multi-Task Reinforcement Learning (MT1, MT10, MT50)

The agent, trained on the set of training tasks and training goal positions from the benchmark, is evaluated for one episode per training goal position, per training task. Meaning it is in practice evaluated for 50 episodes (one for each of the 50 goals) for each training task, and these goal positions are the same ones seen during training. During this episode, the agent is considered to have succeeded if the success flag is `1` *at any point during the episode*, not just at the end of the episode.

### Meta-Reinforcement Learning (ML1, ML10, ML45)

However, since meta-RL is all about adaptation, additionally the evaluation procedure also allows the agent to adapt. Specifically, one would collect `adaptation_steps * adaptation_episodes` number of episodes per testing task, per testing goal, and give them back to the network to adapt from, before computing the final post-adaptation evaluation metric (in three episodes) for that testing goal / task, in a similar fashion to the multi-task reinforcement learning setting.
```
The documentation confirms multi-step interaction through episodes involving repeated agent-environment interactions. Meta-RL agents demonstrate feedback-driven adaptation based on collected experience, with sequential decision-making where agents make decisions at each timestep based on observations.