# Melting Pot - Stage 5 (INTERPRET) Evaluation

## Summary

Melting Pot is a multi-agent reinforcement learning test suite framework, not an evaluation framework in the traditional sense. It provides test scenarios and substrates for evaluating multi-agent RL algorithms but has minimal built-in capabilities for insight extraction, pattern analysis, or interactive exploration of evaluation results. The repository focuses on environment creation and scenario design rather than comprehensive result analysis.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S5F1: Stratified Analysis | 0 | No stratification or performance tradeoff analysis capabilities exist. The framework focuses on creating test environments, not analyzing results. |
| S5F2: Failure Analysis | 0 | No automated failure pattern detection, error clustering, or bias identification features. Analysis must be done manually outside the framework. |
| S5F3: A/B Test Analysis | 0 | No statistical testing capabilities for comparing model variants. The framework provides test scenarios but no analysis tools. |
| S5F4: Interactive Exploration | 1 | Basic human player interface exists for substrate visualization, but no interactive analysis of evaluation results. |

## Detailed Analysis

### S5F1: Stratified Analysis and Performance Tradeoff Analysis
Rating: 0/3

Evidence:

The framework provides no stratification or tradeoff analysis capabilities. The evaluation module (`meltingpot/utils/evaluation/evaluation.py`) exists but focuses on running evaluations, not analyzing results:

From `examples/rllib/self_play_train.py`:
```python
def get_config(
    substrate_name: str = "bach_or_stravinsky_in_the_matrix__repeated",
    num_rollout_workers: int = 2,
    rollout_fragment_length: int = 100,
    train_batch_size: int = 6400,
    # ... configuration parameters only
):
  """Get the configuration for running an agent on a substrate using RLLib."""
```

The notebook `notebooks/evaluation_results.ipynb` is mentioned in the README but not included in the provided files. Even if it existed, the code shows no programmatic API for stratification.

No evidence found for:
- Slicing results by metadata fields
- Hierarchical stratification
- Disparity analysis across subgroups
- Pareto frontier computation
- Multi-objective tradeoff analysis

The framework is designed for creating test environments, not analyzing performance across dimensions.

### S5F2: Failure Pattern and Bias Identification with Recommendations
Rating: 0/3

Evidence:

No failure analysis or bias detection capabilities exist in the codebase. The testing infrastructure focuses on functional tests of the framework itself, not analysis of agent behavior:

From `meltingpot/configs/bots/bot_configs_test.py`:
```python
class BotConfigTest(parameterized.TestCase):

  @parameterized.named_parameters(BOT_CONFIGS.items())
  def test_has_valid_substrate(self, bot):
    self.assertIn(bot.substrate, AVAILABLE_SUBSTRATES)

  @parameterized.named_parameters(BOT_CONFIGS.items())
  def test_model_exists(self, bot):
    self.assertTrue(
        os.path.isdir(bot.model_path), f'Missing model {bot.model_path!r}.')
```

These are unit tests for configuration validity, not analysis tools for agent failures.

From `examples/rllib/self_play_train.py`:
```python
def train(config, num_iterations=1):
  """Trains a model.

  Args:
    config: model config
    num_iterations: number of iterations ot train for.

  Returns:
    Training results.
  """
  # ... just returns raw training results
  return tune.Tuner(
      "PPO",
      param_space=config.to_dict(),
      run_config=air.RunConfig(stop=stop, verbose=1),
  ).fit()
```

No evidence found for:
- Error clustering or categorization
- Bias detection across demographics
- Outlier detection
- Automated recommendations for improvement

### S5F3: A/B Test Statistical Analysis
Rating: 0/3

Evidence:

The framework provides no statistical analysis capabilities. The evaluation module appears to be a basic runner, not an analyzer:

From `examples/rllib/utils.py`:
```python
class MeltingPotEnv(multi_agent_env.MultiAgentEnv):
  """An adapter between the Melting Pot substrates and RLLib MultiAgentEnv."""

  def step(self, action_dict):
    """See base class."""
    actions = [action_dict[agent_id] for agent_id in self._ordered_agent_ids]
    timestep = self._env.step(actions)
    rewards = {
        agent_id: timestep.reward[index]
        for index, agent_id in enumerate(self._ordered_agent_ids)
    }
    # ... returns raw rewards, no analysis
    return observations, rewards, done, done, info
```

The README mentions an evaluation notebook (`notebooks/evaluation_results.ipynb`), but it's not included in the repository:

From `README.md`:
```md
Evaluation results from the [Melting Pot 2.0 Tech Report](https://arxiv.org/abs/2211.13746)
can be viewed in the [Evaluation Notebook](https://github.com/google-deepmind/meltingpot/blob/main/notebooks/evaluation_results.ipynb).
```

No evidence found for:
- Significance testing (t-test, chi-square, etc.)
- Effect size computation
- Power analysis
- Sequential testing
- Multiple comparison corrections

### S5F4: Interactive Exploratory Analysis
Rating: 1/3

Evidence:

The framework provides basic human player interfaces for interacting with substrates, but no interactive analysis of evaluation results:

From `examples/tutorial/harvest/play_harvest.py`:
```python
_ACTION_MAP = {
    'move': level_playing_utils.get_direction_pressed,
    'turn': level_playing_utils.get_turn_pressed,
}

def main(argv):
  del argv  # Unused.
  level_playing_utils.run_episode(
      FLAGS.observation,
      {},  # Settings overrides
      _ACTION_MAP,
      game.get_config(),
      level_playing_utils.RenderType.PYGAME,
      FLAGS.screen_width, FLAGS.screen_height, FLAGS.frames_per_second,
      verbose_fn if FLAGS.verbose else None,
      text_display_fn if FLAGS.display_text else None)
```

This allows visual inspection of environments but not analysis of results. From `meltingpot/human_players/play_clean_up.py`:
```python
def verbose_fn(timestep, unused_player_index: int) -> None:
  """Logs selected data about the current step."""
  # Only log every 100 steps to avoid spam.
  if timestep.step_type != dm_env.StepType.FIRST:
    if _EPISODES[0] % 100 == 0:
      logging.info('TIMESTEP %s', _EPISODES[0])
      logging.info('reward: %s', timestep.reward)
      logging.info('discount: %s', timestep.discount)
```

This is basic logging during gameplay, not interactive analysis.

From `examples/rllib/view_models.py`:
```python
def main():
  # ... loads trained model and renders substrate
  for _ in range(config["horizon"]):
    obs = timestep.observation[0]["WORLD.RGB"]
    obs = np.transpose(obs, (1, 0, 2))
    surface = pygame.surfarray.make_surface(obs)
    # ... renders to pygame window
```

Partial credit (1 point) for:
- Basic visualization of substrates via pygame
- Human player interface for manual testing
- Ability to render trained models

Missing features:
- No sample browser for evaluation results
- No drill-down from metrics to individual episodes
- No interactive filtering or aggregation
- No programmatic exploration API beyond basic environment stepping
- No collaborative annotation

The interactive capabilities are limited to environment visualization, not result analysis. Users must implement their own analysis tools outside the framework.

## Overall Assessment

Melting Pot is fundamentally a test suite creation framework, not an evaluation analytics framework. It excels at providing diverse multi-agent scenarios and substrates but offers virtually no built-in capabilities for analyzing the results of running those tests. Users would need to:

1. Export results to external tools for any statistical analysis
2. Build their own stratification and comparison logic
3. Manually inspect failures without automated clustering
4. Use external statistical packages for any hypothesis testing

The framework's value lies in environment diversity and scenario design, not in insight extraction from evaluation results. For Stage 5 (INTERPRET) capabilities, users must integrate external analysis tools.