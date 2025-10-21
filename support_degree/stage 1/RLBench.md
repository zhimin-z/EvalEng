# RLBench (stepjam__RLBench) - Stage 1 (CONFIGURE) Evaluation

## Summary
RLBench is a robot learning benchmark and simulation environment built on CoppeliaSim/V-REP, not an LLM evaluation framework. It provides a collection of robotic manipulation tasks for training and evaluating reinforcement learning, imitation learning, and other robotic learning algorithms. This repository is fundamentally incompatible with the Stage 1 (CONFIGURE) evaluation criteria, which assumes an LLM evaluation framework with datasets, models, prompts, and metrics configuration.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | RLBench generates robotic demonstration datasets (trajectories, observations, actions) rather than text/QA datasets for LLM evaluation. The `dataset_generator.py` creates simulation-based demos with camera images and robot states, not evaluation datasets with inputs/outputs/references. Example from `dataset_generator.py`: `demo, = task_env.get_demos(amount=1, live_demos=True)` - this collects robot trajectories, not eval data. |
| S1F2: Model Configuration | 0 | RLBench configures robot arms and grippers (Panda, Mico, Jaco, Sawyer, UR5), not LLM models. From `environment.py` lines 43-44: `robot_setup: str = 'panda'` and `SUPPORTED_ROBOTS` dictionary. No API providers (OpenAI, Anthropic, etc.) or LLM configuration exists. The "models" here are physics-based robot models in simulation. |
| S1F3: Prompt Configuration | 0 | RLBench has task descriptions for language-conditioned robotics (e.g., "slide the red block to target"), but these are fixed strings returned by tasks, not configurable prompts/templates for LLM evaluation. From `tasks/slide_block_to_target.py` lines 60-64: returns hardcoded task descriptions. No templating engine, no prompt versioning, no few-shot configuration. |
| S1F4: Environment Setup | 2 | Strong simulation environment setup but for robotics, not LLM evaluation. Provides `setup.py` with dependencies, Docker support mentioned in README. From `setup.py`: core requirements include `pyrep`, `numpy`, etc. Environment setup via `Environment.launch()` initializes CoppeliaSim simulator. However, this is for 3D robot simulation, not LLM evaluation infrastructure. Rated 2 for having good dependency management within its domain. |
| S1F5: Security & Access | 0 | No security features relevant to LLM evaluation. No API key management for LLM providers, no RBAC for experiments, no credential vaults. The framework runs locally in simulation without external API authentication needs. |
| S1F6: Cost Estimation | 0 | No cost estimation for LLM API calls. The only "cost" concept is computational cost of running physics simulations, which is measured in FPS/steps-per-second (see `examples/rlbench_gym.py` line 21: `fps = benchmark_step(env, target_duration=10)`), not monetary cost of model inference. |

## Evidence Analysis

### Why RLBench is Not an LLM Evaluation Framework

1. Domain Mismatch - Robotics vs. NLP:
- From `README.md` lines 1-8: "RLBench is an ambitious large-scale benchmark and learning environment designed to facilitate research in...vision-guided manipulation research areas, including: reinforcement learning, imitation learning, multi-task learning, geometric computer vision"
- The framework evaluates robot policies (controllers that map observations to robot actions), not LLM outputs

2. "Dataset" Concept:
- RLBench datasets contain robot demonstrations with:
  - Camera images (RGB, depth, masks) from multiple views
  - Joint positions, velocities, forces
  - Gripper states and poses
  - From `dataset_generator.py` lines 105-134: Saves images and pickled low-dimensional robot states
- No text inputs, model outputs, or reference answers for comparison

3. "Model" Concept:
- Models in RLBench are robot arm configurations: `'panda'`, `'jaco'`, `'sawyer'`, `'mico'`, `'ur5'` (from `const.py`)
- From `environment.py` lines 72-91: Robot setup involves importing physical robot models into simulation
- No LLM APIs, no inference endpoints, no model serving infrastructure

4. "Task" Concept:
- Tasks are robotic manipulation challenges like:
  - `ReachTarget`, `OpenDoor`, `StackBlocks`, `EmptyDishwasher`
  - From `tasks/__init__.py`: 100+ robotic manipulation tasks
- Each task defines success conditions based on object positions/states in simulation
- Not NLP tasks with text inputs/outputs

5. Evaluation Metrics:
- Success rate of completing robotic tasks (did the robot open the door?)
- From `examples/single_task_rl.py` line 30: `obs, reward, terminate = task.step(action)`
- Not accuracy, F1, BLEU, or other NLP metrics

### What RLBench Actually Provides

Configuration for Robotics:
```python
# From environment.py - configures robot simulation, not LLMs
env = Environment(
    action_mode=action_mode,
    obs_config=obs_config,
    headless=False,
    robot_setup='panda',  # Robot type, not LLM provider
    arm_max_velocity=1.0,
    arm_max_acceleration=4.0
)
```

Task Descriptions (not prompts):
```python
# From tasks/phone_on_base.py - fixed strings, not configurable templates
def init_episode(self, index: int) -> List[str]:
    return ['put the phone on the base',
            'put the phone on the stand',
            'grasp the phone and put it on the base']
```

Observation Configuration (not model parameters):
```python
# From observation_config.py - configures sensors, not LLM settings
obs_config = ObservationConfig()
obs_config.left_shoulder_camera.image_size = (128, 128)
obs_config.joint_velocities = True
obs_config.gripper_pose = True
```

### Gymnasium Integration

RLBench does provide a Gym wrapper (`rlbench/gym.py`), but this is for reinforcement learning integration, not LLM evaluation:
```python
# From gym.py lines 13-16
env = gym.make('rlbench/reach_target-vision-v0', render_mode="rgb_array")
# Action space is robot joint commands, not text generation
self.action_space = spaces.Box(low=action_low, high=action_high, ...)
```

## Conclusion

RLBench scores 0 or near-0 on all Stage 1 (CONFIGURE) features because it operates in a fundamentally different domain. It is an excellent framework for robotics research but has no applicability to LLM evaluation. The concepts of "dataset", "model", "task", and "evaluation" in RLBench refer to robotic simulation entities, not NLP/LLM evaluation components.

Total Stage 1 Score: 2/18 (only partial credit for general dependency management in S1F4)

The framework would require a complete architectural redesign to support LLM evaluation - it cannot be adapted through configuration alone. For LLM evaluation needs, researchers should use frameworks explicitly designed for that purpose (e.g., lm-evaluation-harness, HELM, etc.).