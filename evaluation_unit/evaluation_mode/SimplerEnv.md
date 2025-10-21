## Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Core evaluation loop with multi-step interaction
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
    # Create environment
    env = build_maniskill2_env(env_name, additional_env_build_kwargs, kwargs)
    
    # Initialize environment with specific poses
    obs, _ = env.reset(options=env_reset_options)
    
    # Initialize model
    model.reset(task_description)
    
    timestep = 0
    success = "failure"
    
    # Step the environment in a loop with feedback
    while not (predicted_terminated or truncated):
        # Get action from model based on current observation
        raw_action, action = model.step(image, task_description)
        
        # Execute action in environment
        obs, reward, done, truncated, info = env.step(
            np.concatenate([action["world_vector"], action["rot_axangle"], action["gripper"]]),
        )
        
        # Update state for next iteration
        image = get_image_from_maniskill2_obs_dict(env, obs)
        timestep += 1
```
This function implements a classic interactive simulation loop with multi-step interaction where the policy interacts with the environment over multiple timesteps. It demonstrates feedback loops through iterative observation-action cycles: each iteration takes an observation from the environment, feeds it to the policy to get an action, executes the action, and receives new observations and rewards. The environment state evolves based on policy actions via `env.step()`, enabling the policy to adapt its actions based on environment feedback including observations and task descriptions.

Evidence 2: Episode-based evaluation with sequential decision-making
- File: `simpler_env/simple_inference_visual_matching_prepackaged_envs.py`
- Code Reference:
```python
# run inference
success_arr = []
for ep_id in range(args.n_trajs):
    obs, reset_info = env.reset()
    instruction = env.get_language_instruction()
    is_final_subtask = env.is_final_subtask() 
    
    model.reset(instruction)
    
    predicted_terminated, success, truncated = False, False, False
    timestep = 0
    while not (predicted_terminated or truncated):
        # step the model based on observation
        raw_action, action = model.step(image, instruction)
        
        # Execute action and get new observation
        obs, reward, success, truncated, info = env.step(
            np.concatenate([action["world_vector"], action["rot_axangle"], action["gripper"]]),
        )
        
        # Handle subtask transitions for long-horizon tasks
        new_instruction = env.get_language_instruction()
        if new_instruction != instruction:
            instruction = new_instruction
        
        is_final_subtask = env.is_final_subtask()
        image = get_image_from_maniskill2_obs_dict(env, obs)
        timestep += 1
```
This demonstrates episode-based evaluation where multiple episodes are evaluated across trajectories. It implements sequential decision-making where actions are taken sequentially based on observations, with support for long-horizon tasks through subtask transitions with state persistence. The feedback-driven execution ensures policy actions are based on visual observations and language instructions received from the environment.

Evidence 3: Simulation environment creation infrastructure
- File: `simpler_env/__init__.py`
- Function: `make()`
- Code Reference:
```python
def make(task_name, **kwargs):
    """Creates simulated eval environment from task name."""
    assert task_name in ENVIRONMENTS, f"Task {task_name} is not supported."
    env_name, env_kwargs = ENVIRONMENT_MAP[task_name]
    
    env_kwargs["obs_mode"] = "rgbd"
    env_kwargs["prepackaged_config"] = True
    
    env = gym.make(env_name, **env_kwargs)
    return env
```
The harness creates simulation environments using ManiSkill2/SAPIEN for robot manipulation tasks. Policies interact with simulated physics environments that provide RGBD observations and support multi-step rollouts. Tasks include complex manipulation scenarios like picking, placing, and drawer opening/closing operations.

Evidence 4: Long-horizon task support with subtask composition
- File: `simpler_env/__init__.py`
- Code Reference:
```python
ENVIRONMENTS = [
    "google_robot_pick_coke_can",
    "google_robot_open_drawer",
    "google_robot_place_in_closed_drawer",  # Long-horizon task
    "widowx_stack_cube",
    ...
]
```
Long-horizon tasks like `google_robot_place_apple_in_closed_top_drawer` require multiple subtasks with state transitions across sequential phases: first opening the drawer, then picking the object, and finally placing the object in the drawer.

Evidence 5: Sequential action execution with state evolution
- File: `simpler_env/utils/debug/google_robot_test_dataset_inference_rollout_gt_traj_in_sim.py`
- Code Reference:
```python
for i in range(len(episode_steps) - 1):
    # Get ground truth action from dataset
    gt_action_world_vector = episode_step["action"]["world_vector"]
    gt_action_rotation_delta = np.asarray(episode_step["action"]["rotation_delta"])
    
    action = np.concatenate([
        gt_action_world_vector * action_scale,
        gt_action_rotation_axangle * action_scale,
        gt_action_gripper_closedness_action,
    ])
    
    # Step environment with action
    obs, *_ = env.step(action)
    images.append(obs["image"]["overhead_camera"]["rgb"])
    ee_poses_at_base.append(env.agent.robot.pose.inv() * env.tcp.pose)
```
This debugging script demonstrates open-loop trajectory rollout in simulation, showing how actions are executed sequentially in the environment with continuous state evolution and observation updates at each timestep.