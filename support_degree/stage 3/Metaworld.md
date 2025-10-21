# Metaworld - Stage 3 (EXECUTE) Evaluation

## Summary
Metaworld is a robotic manipulation benchmark environment, not an LLM evaluation framework. It provides simulated environments for training/evaluating RL agents on 50 manipulation tasks. It has no execution orchestration, model inference telemetry, test-time optimization, distributed execution, or human evaluation features relevant to LLM evaluation frameworks. This is fundamentally the wrong type of tool for LLM evaluation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No evaluation pipeline orchestration exists. Metaworld provides RL environments (`SawyerXYZEnv` in `metaworld/sawyer_xyz_env.py`), not evaluation pipelines. The benchmarks (MT1, MT10, ML1, etc. in `metaworld/__init__.py`) simply group environments, they don't orchestrate evaluation workflows, DAGs, or protocols. No routing logic, dependency management, or conditional branching for evaluations exists. |
| S3F2: Inference & Telemetry | 0 | No model inference or telemetry infrastructure. Metaworld environments return observations/rewards (standard RL interface) but provide zero LLM inference telemetry. No latency tracking (TTFT, token latency), throughput metrics, resource consumption monitoring, or cost tracking exists. The `RecordEpisodeStatistics` wrapper (`metaworld/wrappers.py`) only tracks RL episode stats (returns, lengths), not inference metrics. |
| S3F3: Test-Time Optimization | 0 | No test-time compute optimization features. Metaworld has no caching (prompt caching, KV cache), batching (dynamic/static), or optimization techniques (speculative decoding, quantization). It's a physics simulator using MuJoCo, not an LLM inference system. The environments simply step through physics simulations with no concept of prompt processing or generation optimization. |
| S3F4: Failure Handling | 0 | No failure handling for model inference. While Gymnasium environments have basic error handling, there's no retry logic, exponential backoff, circuit breakers, or request rescheduling for LLM inference failures. The `CheckpointWrapper` in `metaworld/wrappers.py:367-393` provides checkpointing for *environment state*, not for handling inference failures during evaluation. |
| S3F5: Checkpointing | 1 | Minimal environment checkpointing, not evaluation checkpointing. The `CheckpointWrapper` (`metaworld/wrappers.py:367-393`) and `RandomTaskSelectWrapper.get_checkpoint()` (`metaworld/wrappers.py:119-127`) save RNG state and task lists, but this is for *RL training reproducibility*, not for resuming interrupted LLM evaluation runs. No automatic checkpointing intervals, no detection of failures to resume from, no incremental evaluation of samples. The checkpointing is manual and environment-focused. |
| S3F6: Distributed Execution | 0 | No distributed execution infrastructure. Metaworld uses Gymnasium's `SyncVectorEnv`/`AsyncVectorEnv` (`metaworld/__init__.py:378-389, 470-481`) for parallel environment rollouts on a single machine, not distributed LLM evaluation. No multi-GPU/multi-node support, no cluster integration (Slurm/K8s), no load balancing, and critically no budget enforcement (cost limits, token quotas, time budgets). The vectorization is for environment parallelism, not model inference distribution. |
| S3F7: Human Evaluation | 0 | No human evaluation features whatsoever. Metaworld provides scripted expert policies (`metaworld/policies/`) and reward functions for automated RL evaluation. Zero crowdsourcing integration (MTurk, Scale AI), no annotation interfaces, no quality control mechanisms (attention checks, gold standards), and no agreement metrics (Cohen's kappa, etc.). The `docs/evaluation/evaluation.md` discusses *success rate* metrics for RL agents, not human annotation workflows. |

## Key Evidence

### Not an Evaluation Framework
File: `README.md:1-5`
```markdown
Meta-World is an open source benchmark for developing and evaluating multi-task 
and meta reinforcement learning algorithms for continuous control robotic 
manipulation environments, with various benchmarks to evaluate different aspects 
of reinforcement learning algorithms.
```
This explicitly states Metaworld evaluates RL algorithms on robotic tasks, not LLMs on language tasks.

File: `metaworld/__init__.py:29-42`
```python
class MetaWorldEnv(abc.ABC):
    """Environment that requires a task before use.
    Takes no arguments to its constructor, and raises an exception if used
    before `set_task` is called.
    """
    @abc.abstractmethod
    def set_task(self, task: Task) -> None:
        """Sets the task.
        Args:
            task: The task to set.
        Raises:
            ValueError: If `task.env_name` is different from the current task.
        """
```
The core abstraction is a simulation environment, not an evaluation pipeline.

### Benchmarks Are Environment Collections
File: `metaworld/__init__.py:250-264`
```python
class MT10(Benchmark):
    """
    The MT10 benchmark.
    Contains 10 tasks in its train set.
    Has an empty test set.
    """
    def __init__(self, seed=None):
        super().__init__()
        self._train_classes = _env_dict.MT10_V3
        self._test_classes = OrderedDict()
        train_kwargs = _env_dict.MT10_V3_ARGS_KWARGS
        self._train_tasks = _make_tasks(
            self._train_classes, train_kwargs, _MT_OVERRIDE, seed=seed
        )
```
MT10 is a collection of 10 RL environments, not an evaluation orchestration system.

### No Inference Infrastructure
File: `metaworld/sawyer_xyz_env.py` (not shown due to length, but referenced in imports)
The base `SawyerXYZEnv` class implements `step(action) -> (obs, reward, done, info)`, the standard RL interface. No `generate()`, `batch_inference()`, or LLM-specific methods exist.

File: `docs/evaluation/evaluation.md:13-15`
```markdown
Each environment computes a success flag which is available through the `info` 
dictionary's `"success"` key, which is `0` when the task has not yet been 
accomplished, and `1` when success has been achieved.
```
Evaluation is based on RL task success flags, not LLM output quality metrics.

### Checkpointing for Environment State Only
File: `metaworld/wrappers.py:367-393`
```python
class CheckpointWrapper(gym.Wrapper):
    env_id: str
    def __init__(self, env: gym.Env, env_id: str):
        super().__init__(env)
        assert hasattr(self.env, "get_checkpoint") and callable(self.env.get_checkpoint)
        assert hasattr(self.env, "load_checkpoint") and callable(
            self.env.load_checkpoint
        )
        self.env_id = env_id

    def get_checkpoint(self) -> tuple[str, dict]:
        ckpt: dict = self.env.get_checkpoint()
        return (self.env_id, ckpt)

    def load_checkpoint(self, ckpts: list[tuple[str, dict]]) -> None:
        my_ckpt = None
        for env_id, ckpt in ckpts:
            if env_id == self.env_id:
                my_ckpt = ckpt
                break
```
This checkpoints RNG states and environment parameters, not evaluation progress through datasets.

### Environment Vectorization, Not Distributed Inference
File: `metaworld/__init__.py:378-389`
```python
vectorizer: type[gym.vector.VectorEnv] = getattr(
    gym.vector, f"{vector_strategy.capitalize()}VectorEnv"
)
return vectorizer(  # type: ignore
    [
        partial(
            _init_each_env,
            env_cls=env_cls,
            tasks=[task for task in benchmark.train_tasks if task.env_name == name],
            seed=seed,
            env_id=env_id,
            num_tasks=num_tasks or default_num_tasks,
            kwargs,
        )
        for env_id, (name, env_cls) in enumerate(benchmark.train_classes.items())
    ],
    autoreset_mode=autoreset_mode,
)
```
Uses Gymnasium's vector environments for parallel RL rollouts, not distributed LLM inference across GPUs/nodes.

### No Human Evaluation Infrastructure
File: `metaworld/policies/__init__.py:1-5`
```python
from metaworld.policies.sawyer_assembly_v3_policy import SawyerAssemblyV3Policy
from metaworld.policies.sawyer_basketball_v3_policy import SawyerBasketballV3Policy
from metaworld.policies.sawyer_bin_picking_v3_policy import SawyerBinPickingV3Policy
from metaworld.policies.sawyer_box_close_v3_policy import SawyerBoxCloseV3Policy
from metaworld.policies.sawyer_button_press_topdown_v3_policy import (
    SawyerButtonPressTopdownV3Policy,
)
```
These are scripted expert RL policies for generating demonstrations, not human annotators or crowdsourcing workers.

## Overall Assessment

Total Score: 1/21

Metaworld is a high-quality reinforcement learning benchmark for robotic manipulation, but it has zero relevance to LLM evaluation. It:
- Provides physics-simulated RL environments, not evaluation pipelines
- Has no model inference, telemetry, or optimization infrastructure
- Uses environment checkpointing for reproducibility, not evaluation resumption
- Implements RL environment parallelism, not distributed LLM inference
- Evaluates RL agents with success rates, not LLMs with human/automated metrics

The single point for S3F5 reflects minimal checkpoint functionality that could theoretically be adapted for evaluation resumption, but this would require building an entirely new system on top of Metaworld.

This repository should not be evaluated as an LLM evaluation framework. It belongs to a completely different domain (robotics/RL) and attempting to use it for LLM evaluation would require rebuilding all Stage 3 features from scratch.