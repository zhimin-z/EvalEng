## Evaluator Categories

[Environmental, Algorithmic]

## Detailed Analysis

### Environmental

Evidence 1: Simulation environment feedback for task completion
- File: `metaworld/evaluation.py`
- Function: `evaluation()`
- Code Reference:
```python
def evaluation(
    agent: Agent,
    eval_envs: gym.vector.SyncVectorEnv | gym.vector.AsyncVectorEnv,
    num_episodes: int = 50,
) -> tuple[float, float, dict[str, float], dict[str, list[float]]]:
    # ...
    while not eval_done(episodic_returns):
        actions = agent.eval_action(obs)
        obs, _, terminations, truncations, infos = eval_envs.step(actions)
        # ...
        for i, env_ended in enumerate(dones):
            if env_ended:
                episodic_returns[task_names[i]].append(
                    float(infos["final_info"]["episode"]["r"][i])
                )
                if len(episodic_returns[task_names[i]]) <= num_episodes:
                    successes[task_names[i]] += int(infos["final_info"]["success"][i])
```
The evaluation function executes agent actions in robotic manipulation simulation environments (Metaworld tasks) and captures feedback directly from the simulator. The `success` flag from `infos["final_info"]["success"]` is a binary signal provided by the environment indicating whether the agent successfully completed the manipulation task (e.g., reached a target, opened a door). This environmental feedback mechanism assesses performance through direct interaction with the target system, where the simulator itself determines task completion based on predefined success criteria embedded in the environment's logic.

Evidence 2: Physics simulation execution and state evaluation
- File: `metaworld/sawyer_xyz_env.py`
- Function: `step()`
- Code Reference:
```python
def step(
    self, action: npt.NDArray[np.float32]
) -> tuple[npt.NDArray[np.float64], SupportsFloat, bool, bool, dict[str, Any]]:
    # ...
    self.do_simulation([action[-1], -action[-1]], n_frames=self.frame_skip)
    # ...
    reward, info = self.evaluate_state(self._last_stable_obs, action)
    return (
        np.array(self._last_stable_obs, dtype=np.float64),
        reward,
        False,
        truncate,
        info,  # Contains 'success' key
    )
```
The base environment class executes the MuJoCo physics simulation for robotic manipulation tasks and provides system-generated success signals. The `do_simulation()` call runs the physics engine with the agent's action, and the environment validates whether manipulation goals are achieved through `evaluate_state()`, returning success/failure feedback in the `info` dictionary. This represents execution-based assessment where the simulator acts as the evaluator by enforcing physical constraints and task objectives.

Evidence 3: Runtime policy validation through environment interaction
- File: `tests/metaworld/envs/mujoco/sawyer_xyz/test_scripted_policies.py`
- Code Reference:
```python
def test_policy(env_name):
    # ...
    completed = 0
    for task in mt1.train_tasks:
        env.set_task(task)
        obs, info = env.reset()
        done = False
        count = 0
        while count < 500 and not done:
            count += 1
            a = p.get_action(obs)
            next_obs, _, trunc, termn, info = env.step(a)
            done = trunc or termn
            obs = next_obs
            if int(info["success"]) == 1:
                completed += 1
                break
    assert (float(completed) / 50) >= 0.80
```
This test validates scripted policies by executing them in the simulation environment and checking task completion via the environment-provided `info["success"]` flag. The environment simulation provides runtime validation of model-generated actions against task objectives, where success is determined by the simulator's internal evaluation logic. This demonstrates environmental evaluation where the system itself judges whether the agent's behavior meets the task requirements through actual execution rather than external metrics.

---

### Algorithmic

Evidence 1: Statistical aggregation of success metrics
- File: `metaworld/evaluation.py`
- Function: `evaluation()`
- Code Reference:
```python
success_rate_per_task = {
    task_name: task_successes / num_episodes
    for task_name, task_successes in successes.items()
}
mean_success_rate = np.mean(list(success_rate_per_task.values()))
mean_returns = np.mean(list(episodic_returns.values()))
```
These are algorithmic metrics that apply deterministic mathematical functions to compute success rates and mean returns. The success rate calculation uses division to normalize success counts by the number of episodes, while mean calculations use averaging functions. These predefined statistical operations provide consistent, reproducible evaluation measures independent of the specific environment or task, representing the algorithmic processing layer that transforms raw environmental signals into standardized performance metrics.

Evidence 2: Deterministic episode tracking and counting
- File: `metaworld/evaluation.py`
- Function: `evaluation()`
- Code Reference:
```python
for i, env_ended in enumerate(dones):
    if env_ended:
        episodic_returns[task_names[i]].append(
            float(infos["final_info"]["episode"]["r"][i])
        )
        if len(episodic_returns[task_names[i]]) <= num_episodes:
            successes[task_names[i]] += int(infos["final_info"]["success"][i])
```
The evaluation harness uses algorithmic counting and accumulation operations to track episodic returns and success counts. These are deterministic arithmetic operations (counting successes with `+=`, accumulating rewards with `.append()`) that systematically aggregate performance data. This represents algorithmic evaluation where predefined computational procedures process the raw environmental feedback into structured performance statistics.

Evidence 3: Mathematical reward function computations
- File: `metaworld/sawyer_xyz_env.py` and `metaworld/utils/reward_utils.py`
- Code Reference:
```python
from metaworld.utils import reward_utils
```
The codebase employs algorithmic reward functions (e.g., `_gripper_caging_reward` in `sawyer_xyz_env.py` lines 548-645) that compute rewards using mathematical formulas involving distance calculations, tolerance functions, and Hamacher products. These are predefined computational measures that deterministically evaluate agent behavior based on geometric and physical relationships. The reward functions serve as algorithmic evaluators that provide consistent, formula-based assessment of manipulation quality.

Evidence 4: Documented success rate as primary metric
- File: `docs/evaluation/evaluation.md`
- Documentation Reference:
```markdown
# Evaluation

In Metaworld, agents are to be evaluated using their **success rate** on a set of tasks and goal positions, not the episodic reward achieved during training.

Each environment computes a success flag which is available through the `info` dictionary's `"success"` key, which is `0` when the task has not yet been accomplished, and `1` when success has been achieved.
```
The documentation explicitly defines success rate as the primary evaluation metric, which is computed algorithmically by averaging binary success values across episodes. While the success flag originates from environmental feedback, the calculation of success rate (dividing total successes by number of episodes) is a deterministic algorithmic metric. This demonstrates how the harness combines environmental signals with algorithmic processing to produce standardized evaluation measures.