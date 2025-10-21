## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification]

## Detailed Analysis

### Explicit Labels

Evidence 1: Demonstration Storage and Loading
- File: `rlbench/utils.py`
- Code Reference: `get_stored_demos()` function (lines 24-212)
```python
with open(join(example_path, LOW_DIM_PICKLE), 'rb') as f:
    obs = pickle.load(f)
```
The harness loads pre-recorded demonstrations from disk that serve as reference trajectories. These demonstrations contain ground truth observations and actions that were successfully executed to complete tasks, representing explicit labels in the form of reference demonstrations used to evaluate or bootstrap learning algorithms.

Evidence 2: Task Success Conditions
- File: `rlbench/tasks/reach_target.py`
- Code Reference: `init_task()` and `init_episode()` methods (lines 12-14, 16-28)
```python
self.register_success_conditions(
    [DetectedCondition(self.robot.arm.get_tip(), success_sensor)])
```
Tasks define explicit success conditions that serve as ground truth labels for task completion. These success conditions are predetermined correct states that the system evaluates against to determine task success.

Evidence 3: Task Variation Descriptions
- File: `rlbench/dataset_generator.py`
- Code Reference: `save_demo()` function (lines 77-79)
```python
with open(os.path.join(
        variation_path, VARIATION_DESCRIPTIONS), 'wb') as f:
    pickle.dump(descriptions, f)
```
Task variations are stored with explicit text descriptions that serve as ground truth labels. These descriptions are reference labels for task understanding and provide predetermined specifications for task variations.

Evidence 4: Ground Truth Observation Trajectories
- File: `rlbench/demo.py`
- Code Reference: `Demo` class (lines 5-17)
```python
def __init__(self, observations: List[Observation], random_seed=None, num_reset_attempts=None):
    self._observations = observations
```
Demo objects contain lists of Observation objects that represent ground truth state trajectories. These observations serve as explicit reference outputs for the benchmark tasks, providing predetermined correct sequences of states.

---

### Behavioral Specification

Evidence 1: Executable Success Conditions
- File: `rlbench/tasks/take_lid_off_saucepan.py`
- Code Reference: Success condition registration (lines 14-18)
```python
cond_set = ConditionSet([
    GraspedCondition(self.robot.gripper, self.lid),
    DetectedCondition(self.lid, self.success_detector)
])
self.register_success_conditions([cond_set])
```
Tasks register executable validation conditions that dynamically check if model outputs achieve task goals. These are executable specifications that verify functional correctness of agent behavior on benchmark tasks through runtime validation.

Evidence 2: Joint State Validation
- File: `rlbench/tasks/open_drawer.py`
- Code Reference: `init_episode()` method (lines 16-17)
```python
self.register_success_conditions(
    [JointCondition(self._joints[index], 0.15)])
```
Tasks use joint state conditions as executable validators. This behavioral specification validates whether the robot achieved the correct joint configuration through dynamic state checking.

Evidence 3: Detection and Proximity Validators
- File: `rlbench/tasks/sweep_to_dustpan.py`
- Code Reference: `init_task()` method (lines 10-13)
```python
conditions = [DetectedCondition(dirt, success_sensor) for dirt in dirts]
self.register_graspable_objects([broom])
self.register_success_conditions(conditions)
```
Tasks use proximity sensors as executable validators for object placement. These are runtime-executable specifications that verify task completion through sensor-based detection.

Evidence 4: Custom Behavioral Validators
- File: `rlbench/tasks/stack_chairs.py`
- Code Reference: `ChairsOrientedCondition` class (lines 15-23)
```python
class ChairsOrientedCondition(Condition):
    def condition_met(self):
        for obj in self.objs[:-1]:
            x, y, z = obj.get_orientation(self.objs[-1])
            if abs(x) > self.error or abs(y) > self.error or abs(z) > self.error:
                return False, False
        return True, False
```
Custom condition classes implement executable behavioral specifications. This programmatic validation function checks behavioral correctness through orientation comparison, providing dynamic functional validation.

Evidence 5: Sequential Behavior Requirements
- File: `rlbench/tasks/hit_ball_with_queue.py`
- Code Reference: `init_task()` method (lines 13-17)
```python
cond_set = ConditionSet([
    GraspedCondition(self.robot.gripper, queue),
    DetectedCondition(ball, success_sensor)
], order_matters=True)
```
Tasks specify sequential behavioral requirements validating that actions are performed in the correct sequence. This ordered condition set provides executable specification for temporal correctness of agent behavior.