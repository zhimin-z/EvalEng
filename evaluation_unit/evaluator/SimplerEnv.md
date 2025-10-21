## Evaluator Categories

[Algorithmic, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Statistical correlation and rank violation metrics
- File: `simpler_env/utils/metrics.py`
- Function: `pearson_correlation()`, `mean_maximum_rank_violation()`
- Code Reference:
```python
def pearson_correlation(perf_sim: Sequence[float], perf_real: Sequence[float]) -> float:
    perf_sim, perf_real = np.array(perf_sim), np.array(perf_real)
    assert perf_sim.shape == perf_real.shape
    perf_sim = perf_sim - np.mean(perf_sim)
    perf_real = perf_real - np.mean(perf_real)
    if np.all(perf_sim == perf_real):
        pearson = 1
    else:
        pearson = np.sum(perf_sim * perf_real) / (
            np.sqrt(np.sum(perf_sim**2) * np.sum(perf_real**2)) + 1e-8
        )
    return pearson

def mean_maximum_rank_violation(
    perf_sim: Sequence[float], perf_real: Sequence[float]
) -> float:
    perf_sim, perf_real = np.array(perf_sim), np.array(perf_real)
    assert perf_sim.shape == perf_real.shape
    rank_violations = []
    for i in range(len(perf_sim)):
        rank_violation = 0.0
        for j in range(len(perf_sim)):
            if (perf_sim[i] > perf_sim[j]) != (perf_real[i] > perf_real[j]):
                rank_violation = max(
                    rank_violation, np.abs(perf_real[i] - perf_real[j])
                )
        rank_violations.append(rank_violation)
    rank_violation = np.mean(rank_violations)
    return rank_violation
```
These are deterministic statistical functions that compute correlation and rank violation metrics to evaluate the quality of simulated policy evaluations against real-world performance. They use mathematical formulas (Pearson correlation coefficient, rank violation calculations) to score the alignment between simulated and real evaluation results.

Evidence 2: Non-parametric statistical testing
- File: `simpler_env/utils/metrics.py`
- Function: `print_all_kruskal_results()`
- Code Reference:
```python
def print_all_kruskal_results(
    sim: Sequence[Sequence[float]], real: Sequence[Sequence[float]], title: str
) -> None:
    from scipy.stats import kruskal
    sim, real = np.array(sim), np.array(real)
    assert sim.shape == real.shape
    print(title)
    print(" " * 6, "each checkpoint kruskal:")
    for i in range(sim.shape[0]):
        if np.all(sim[i] == real[i]):
            print(" " * 12, "all same, 1.0")
        else:
            print(" " * 12, kruskal(sim[i], real[i]))
```
This function applies the Kruskal-Wallis H-test, a non-parametric statistical test, to compare distributions of simulation vs. real evaluation results. It's a predefined statistical metric used to assess significance of performance differences.

Evidence 3: Aggregated statistical metric calculations
- File: `tools/calc_metrics.py` and `tools/calc_metrics_evaluation_videos.py`
- Code Reference:
```python
mmrv = mean_maximum_rank_violation(
    list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
)
pearson = pearson_correlation(
    list(SIMPLER_PERF[k].values()), list(REAL_PERF[k].values())
)
```
These scripts aggregate success rates and calculate statistical correlation metrics (MMRV, Pearson correlation) to evaluate how well simulation results match real-world performance across different tasks and policies.

---

### Environmental

Evidence 1: Physics simulator feedback for manipulation tasks
- File: `simpler_env/evaluation/maniskill2_evaluator.py`
- Function: `run_maniskill2_eval_single_episode()`
- Code Reference:
```python
def run_maniskill2_eval_single_episode(
    model,
    ckpt_path,
    robot_name,
    env_name,
    ...
):
    env = build_maniskill2_env(
        env_name,
        **additional_env_build_kwargs,
        **kwargs,
    )
    
    obs, _ = env.reset(options=env_reset_options)
    
    while not (predicted_terminated or truncated):
        raw_action, action = model.step(image, task_description)
        predicted_terminated = bool(action["terminate_episode"][0] > 0)
        
        obs, reward, done, truncated, info = env.step(
            np.concatenate([action["world_vector"], action["rot_axangle"], action["gripper"]]),
        )
        
        success = "success" if done else "failure"
```
This function executes model-generated actions in a physics simulation environment (ManiSkill2/SAPIEN) and receives feedback (`done`, `reward`, `info`) from the simulator to evaluate task success. The simulator provides environmental feedback on whether the robot successfully completed manipulation tasks (e.g., grasping, drawer opening).

Evidence 2: Simulated environment task completion signals
- File: `simpler_env/simple_inference_visual_matching_prepackaged_envs.py`
- Code Reference:
```python
env = simpler_env.make(args.task)

for ep_id in range(args.n_trajs):
    obs, reset_info = env.reset()
    
    while not (predicted_terminated or truncated):
        raw_action, action = model.step(image, instruction)
        
        obs, reward, success, truncated, info = env.step(
            np.concatenate([action["world_vector"], action["rot_axangle"], action["gripper"]]),
        )
        
    success_arr.append(success)
```
The script evaluates robot manipulation policies by executing their actions in simulated environments and collecting success/failure feedback from the simulator. The `env.step()` returns task completion signals (`success`, `truncated`) based on the simulation state.

Evidence 3: Main evaluation pipeline with simulator feedback
- File: `simpler_env/main_inference.py`
- Function: `maniskill2_evaluator()` call
- Code Reference:
```python
success_arr = maniskill2_evaluator(model, args)
print(" " * 10, "Average success", np.mean(success_arr))
```
This is the main evaluation pipeline that runs policies in simulated robot environments and aggregates success metrics based on simulator feedback about task completion.

Evidence 4: Environment-specific task success detection
- File: `simpler_env/__init__.py` and environment implementations in `ManiSkill2_real2sim/`
- Code Reference:
```python
ENVIRONMENTS = [
    "google_robot_pick_coke_can",
    "google_robot_move_near",
    "google_robot_open_drawer",
    "widowx_spoon_on_towel",
    ...
]
```
The harness defines various manipulation tasks where success is determined by the simulation environment checking physical conditions (e.g., whether an object was grasped, whether a drawer opened sufficiently). The simulator acts as an oracle providing task-specific success/failure signals.