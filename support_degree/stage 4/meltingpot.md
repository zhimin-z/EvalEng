# Melting Pot (google-deepmind/meltingpot) - Stage 4 (EVALUATE) Evaluation

## Summary

Melting Pot is a multi-agent reinforcement learning evaluation suite focused on creating diverse social scenarios rather than being a general-purpose evaluation framework. It has very limited metric computation capabilities by design—it's primarily a substrate (environment) builder. While it provides basic evaluation utilities for its scenarios, it lacks the comprehensive metric computation, aggregation, and comparison features expected from a full evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation framework exists. The system focuses on environment simulation rather than output validation. No schema validation, policy compliance checks, or normalization features found in codebase. |
| S4F2: Metric Computation | 1 | Minimal metrics exist only for specific evaluation scenarios. `meltingpot/utils/evaluation/evaluation.py` contains basic per-episode metrics but no comprehensive metric library. No standard NLP/ML metrics (BLEU, ROUGE, F1, etc.). Only environment-specific reward tracking. |
| S4F3: Evaluator Models | 0 | No LLM-as-judge or evaluator model integration. The framework is for training RL agents in multi-agent environments, not for evaluating model outputs. No judge prompts, ensemble scoring, or rationale capture. |
| S4F4: Multi-Modal Scoring | 0 | Text-only observations with no multi-modal evaluation metrics. While environments have RGB observations (`"RGB": specs.OBSERVATION["RGB"]`), these are for agent input, not for multi-modal metric computation. No image captioning, VQA, or cross-modal metrics. |
| S4F5: Aggregate Statistics | 1 | Basic aggregation exists in evaluation utilities. `meltingpot/utils/evaluation/evaluation.py` computes means across episodes but lacks statistical testing, confidence intervals, ranking systems, or sophisticated comparison tools. No pairwise significance testing or effect size computation. |

## Detailed Evidence

### S4F1: Output Validation and Normalization (0 points)

Evidence of absence:

The codebase is an RL environment suite, not an output evaluation framework. Searching through the repository:

1. No validation utilities: No files match patterns for validation, schema checking, or normalization
2. Environment-focused: From `meltingpot/substrate.py`:
```python
def build(substrate_name: str, roles: Optional[Sequence[str]] = None) -> dmlab2d.Environment:
  """Builds the specified substrate with players in the specified roles."""
```
The system builds environments, not validates outputs.

3. No policy compliance: No content moderation, safety checks, or constraint validation in any configuration files or utilities.

Rating: 0/3 - No validation features exist as this is not an output evaluation framework.

### S4F2: Task-Specific Metric Computation (1 point)

Evidence of minimal metrics:

From `meltingpot/utils/evaluation/evaluation.py` (referenced in README):
```python
"""The evaluation library can be used to evaluate SavedModels trained on Melting Pot substrates."""
```

However, examining the actual metric computation:

1. Limited scope: Only environment-specific metrics exist. From scenario configs in `meltingpot/configs/scenarios/__init__.py`:
```python
Scenario(
    description='...',
    tags=frozenset({...}),
    substrate='substrate_name',
    num_focal_agents=4,
    num_background_bots=3,
    bots=frozenset({...}),
)
```
No metric specifications or computation logic.

2. Basic per-sample scoring: The evaluation notebook `notebooks/evaluation_results.ipynb` mentioned in README shows basic episode-level results but lacks comprehensive metric APIs.

3. No standard metrics: No implementations of BLEU, ROUGE, F1, accuracy, precision, recall, AUC-ROC, or other standard ML metrics. This is an RL framework focused on multi-agent scenarios.

4. No extensibility: No clear API for custom metric definitions or metric composition.

Rating: 1/3 - Minimal environment-specific metrics exist but no comprehensive metric library.

### S4F3: Evaluator Model Integration (0 points)

Complete absence of evaluator models:

1. No LLM-as-judge: The framework evaluates RL policies, not uses LLMs to judge outputs. From `examples/rllib/self_play_train.py`:
```python
def train(config, num_iterations=1):
  """Trains a model."""
  tune.register_env("meltingpot", utils.env_creator)
```
This is for training RL agents, not evaluating with LLMs.

2. No specialized evaluators: No integration with RAGAS, G-Eval, Prometheus, or similar evaluation models.

3. Policy evaluation only: From `meltingpot/utils/policies/policy.py`:
```python
class Policy(abc.ABC, Generic[State]):
  """Policy interface for bots."""
  @abc.abstractmethod
  def step(self, timestep: dm_env.TimeStep, prev_state: State) -> Tuple[int, State]:
```
Policies are actors in environments, not evaluators of outputs.

Rating: 0/3 - No evaluator model support as this is an environment simulation framework.

### S4F4: Multi-Modal Scoring Protocols (0 points)

Text-only with no multi-modal metrics:

1. RGB observations exist but not for evaluation: From substrate configs like `meltingpot/configs/substrates/predator_prey__random_forest.py`:
```python
config.timestep_spec = specs.timestep({
    "RGB": specs.OBSERVATION["RGB"],
    "STAMINA": specs.float64(),
    "WORLD.RGB": specs.rgb(152, 184),
})
```
These RGB observations are inputs to agents, not evaluation targets.

2. No image/video metrics: No CIDEr, SPICE, CLIP score, or any vision-language metrics in the codebase.

3. No audio/video support: The framework is purely for 2D grid-world simulations with sprite-based rendering.

4. Environment rendering only: From `examples/rllib/utils.py`:
```python
def render(self) -> np.ndarray:
  """Render the environment."""
  observation = self._env.observation()
  world_rgb = observation[0]['WORLD.RGB']
  return world_rgb
```
Rendering is for visualization, not evaluation.

Rating: 0/3 - No multi-modal evaluation metrics exist.

### S4F5: Aggregate Statistics and Cross-Model Comparison (1 point)

Basic aggregation only:

1. Episode-level aggregation: From the evaluation notebook reference in README:
```markdown
Evaluation results from the [Melting Pot 2.0 Tech Report](https://arxiv.org/abs/2211.13746)
can be viewed in the [Evaluation Notebook](notebooks/evaluation_results.ipynb).
```
This suggests basic result aggregation exists.

2. No statistical testing: No code found for:
   - t-tests or Wilcoxon tests
   - Bootstrap confidence intervals
   - Permutation tests
   - Effect size computation

3. No ranking systems: No Elo, TrueSkill, or leaderboard generation utilities found in the codebase.

4. Basic scenario evaluation: From bot configs in `meltingpot/configs/bots/__init__.py`:
```python
BOT_CONFIGS = immutabledict.immutabledict({
    'bot_name': _saved_model(substrate='substrate_name', model='model_name'),
    ...
})
```
Bots can be evaluated on scenarios but without sophisticated comparison tools.

5. No confidence intervals or distributions: The evaluation utilities appear to compute basic means without uncertainty quantification.

Rating: 1/3 - Basic aggregation exists (likely mean/median) but lacks statistical comparison tools.

## Key Observations

1. Purpose mismatch: Melting Pot is a multi-agent RL environment suite, not a general evaluation framework. Its focus is on creating diverse social scenarios for training and testing RL agents, not on computing metrics for model outputs.

2. Evaluation exists but is limited: From README:
```markdown
The [evaluation](meltingpot/utils/evaluation/evaluation.py) library can be used
to evaluate SavedModels trained on Melting Pot substrates.
```
This evaluation is environment-specific and minimal.

3. No metric library: Unlike frameworks like PromptBench or LangChain which include or integrate with metric libraries, Melting Pot has no such features.

4. Agent evaluation vs output evaluation: The framework evaluates agent policies in interactive environments, not model outputs against reference data.

5. Not an evaluation harness: This is fundamentally a substrate/environment builder with basic evaluation utilities, not a comprehensive evaluation harness like the ones described in the Stage 4 guidelines.

## Conclusion

Total Indicative Score: 2/15

Melting Pot receives low scores across all Stage 4 features because it is not designed as an evaluation framework. It's a multi-agent RL environment suite focused on creating diverse social interaction scenarios. While it has minimal evaluation utilities for comparing trained policies on scenarios, it lacks:

- Any output validation or normalization
- A comprehensive metric library
- Evaluator model integration
- Multi-modal scoring capabilities
- Statistical comparison and ranking tools

This framework should not be compared against evaluation-focused tools as it serves a fundamentally different purpose: providing rich multi-agent environments for RL research rather than computing metrics on model outputs.