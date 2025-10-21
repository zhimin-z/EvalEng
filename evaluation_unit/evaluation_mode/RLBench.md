## Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Step-based interaction with observation-reward-termination feedback
- File: `rlbench/task_environment.py`
- Function: `step()`
- Code Reference:
```python
def step(self, action) -> (Observation, int, bool):
    # returns observation, reward, done, info
    if not self._reset_called:
        raise RuntimeError(
            "Call 'reset' before calling 'step' on a task.")
    self._action_mode.action(self._scene, action)
    success, terminate = self._task.success()
    reward = float(success)
    if self._shaped_rewards:
        reward = self._task.reward()
        if reward is None:
            raise RuntimeError(
                'User requested shaped rewards, but task %s does not have '
                'a defined reward() function.' % self._task.get_name())
    return self._scene.get_observation(), reward, terminate
```
The `step()` method processes agent actions and returns observations, rewards, and termination flags, enabling sequential decision-making over multiple timesteps. Each action causes the simulation state to evolve via `self._action_mode.action(self._scene, action)`, and the environment provides feedback through rewards and new observations.

Evidence 2: Environment infrastructure with configurable simulation parameters
- File: `rlbench/environment.py`
- Class: `Environment`
- Code Reference:
```python
class Environment(object):
    """Each environment has a scene."""

    def __init__(self,
                 action_mode: ActionMode,
                 dataset_root: str = '',
                 obs_config: ObservationConfig = ObservationConfig(),
                 headless: bool = False,
                 static_positions: bool = False,
                 robot_setup: str = 'panda',
                 randomize_every: RandomizeEvery = None,
                 frequency: int = 1,
                 visual_randomization_config: VisualRandomizationConfig = None,
                 dynamics_randomization_config: DynamicsRandomizationConfig = None,
                 attach_grasped_objects: bool = True,
                 shaped_rewards: bool = False,
                 arm_max_velocity: float = 1.0,
                 arm_max_acceleration: float = 4.0,
                 ):
```
The Environment class maintains persistent state across steps and supports domain randomization through visual and dynamics randomization configurations, demonstrating that environment state can vary between episodes to test model adaptation.

Evidence 3: Gymnasium interface for standardized interaction loops
- File: `rlbench/gym.py`
- Class: `RLBenchEnv`
- Code Reference:
```python
class RLBenchEnv(gym.Env):
    """An gym wrapper for RLBench."""
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        np.random.seed(seed=seed)
        reset_to_demo = None
        if options is not None:
            reset_to_demo = options.get("reset_to_demo", None)
        if reset_to_demo is None:
            descriptions, obs = self.rlbench_task_env.reset()
        else:
            descriptions, obs = self.rlbench_task_env.reset(reset_to_demo=reset_to_demo)
        return self._extract_obs(obs), {"text_descriptions": descriptions}

    def step(self, action):
        obs, reward, terminated = self.rlbench_task_env.step(action)
        return self._extract_obs(obs), reward, terminated, False, {}
```
The Gymnasium wrapper implements the classic reinforcement learning interaction loop: reset environment → take action → receive observation/reward/done → repeat. This standardizes the multi-step interaction pattern with feedback loops.

Evidence 4: Multi-step interaction validation through unit tests
- File: `tests/unit/test_environment.py`
- Function: `test_step()`
- Code Reference:
```python
def test_step(self):
    task = self.get_task(
        ReachTarget, JointVelocity())
    task.reset()
    obs, reward, term = task.step(np.random.uniform(size=8))
    self.assertIsNotNone(obs.right_shoulder_rgb)
    self.assertIsNone(obs.left_shoulder_rgb)
    self.assertEqual(reward, 0)
    self.assertFalse(term)
```
Test cases demonstrate the sequential decision-making process over multiple timesteps, validating that observations, rewards, and termination signals are correctly returned after each action.

Evidence 5: Complete RL loop example showing interaction pattern
- File: `examples/single_task_rl.py` (referenced in README.md)
- Code Reference:
```python
# From README.md
action_mode = MoveArmThenGripper(
  arm_action_mode=JointVelocity(),
  gripper_action_mode=Discrete()
)
env = Environment(action_mode)
env.launch()

task = env.get_task(ReachTarget)
descriptions, obs = task.reset()
obs, reward, terminate = task.step(np.random.normal(size=env.action_shape))
```
The example demonstrates the complete environment-model interaction loop, showing how agents interact with the simulation through repeated action-observation cycles to evaluate robotic manipulation capabilities.

Evidence 6: State restoration capabilities for episodic evaluation
- File: `rlbench/task_environment.py`
- Function: `reset_to_demo()`
- Code Reference:
```python
def reset_to_demo(self, demo: Demo) -> (List[str], Observation):
    demo.restore_state()
    variation_index = demo._observations[0].misc["variation_index"]
    self.set_variation(variation_index)
    return self.reset(demo)
```
The `reset_to_demo()` function demonstrates state restoration capabilities, allowing the environment to be initialized to specific configurations. This supports consistent evaluation across different starting states while maintaining persistent state management.

Evidence 7: Continuous feedback through shaped reward functions
- File: `rlbench/tasks/reach_target.py`
- Function: `reward()`
- Code Reference:
```python
def reward(self) -> float:
    return -np.linalg.norm(self.target.get_position() -
                           self.robot.arm.get_tip().get_position())
```
Support for shaped rewards provides continuous feedback signals beyond binary success/failure, enabling evaluation of agent behavior through dense reward functions that guide learning and assessment of progressive task completion.