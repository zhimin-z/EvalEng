## Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Multi-agent environment with state evolution
- File: `meltingpot/utils/scenarios/scenario.py`
- Class: `Scenario`
- Description: The `Scenario` class manages multi-step interactions between agents and environments with persistent state.

Evidence 2: Multi-agent environment substrate wrapper
- File: `meltingpot/utils/substrates/substrate.py`
- Class: `Substrate`
- Description: The `Substrate` class wraps environments that maintain state across timesteps, enabling continuous interaction.

Evidence 3: Episode execution with feedback loops
- File: `meltingpot/utils/evaluation/evaluation.py`
- Function: `run_episode()`
- Code Reference:
```python
def run_episode(
    population: population_lib.Population,
    substrate: substrate_lib.Substrate,
) -> None:
  """Runs a population on a substrate for one episode."""
  population.reset()
  timestep = substrate.reset()
  population.send_timestep(timestep)
  actions = population.await_action()
  while not timestep.step_type.last():
    timestep = substrate.step(actions)
    population.send_timestep(timestep)
    actions = population.await_action()
```
This implements a clear feedback loop where agents receive timesteps, take actions, and the environment responds with new timesteps based on those actions. The system demonstrates multi-step environment interaction where each action affects the environment state.

Evidence 4: Multi-turn interaction with observation tracking
- File: `meltingpot/utils/evaluation/evaluation.py`
- Function: `run_and_observe_episodes()`
- Code Reference:
```python
def run_and_observe_episodes(
    population: population_lib.Population,
    substrate: substrate_lib.Substrate,
    num_episodes: int,
    video_root: Optional[str] = None,
) -> pd.DataFrame:
  """Runs a population on a substrate and returns results."""
  # ... observation setup ...
  for n in range(num_episodes):
    run_episode(population, substrate)
```
This function runs multiple episodes with observation tracking, demonstrating extended interaction sequences with state evolution across episodes.

Evidence 5: Policy-based agent behavior with state management
- File: `meltingpot/utils/policies/saved_model_policy.py`
- Description: Agents maintain internal state across interactions, enabling adaptive behavior throughout episodes.

Evidence 6: Population management with persistent state
- File: `meltingpot/utils/scenarios/population.py`
- Class: `Population`
- Description: The `Population` class manages multiple agents with persistent state, coordinating multi-agent interactions in the simulation.

Evidence 7: Game/simulation environment configurations
- File: `meltingpot/configs/substrates/`
- Description: Multiple substrate configurations define different multi-agent game scenarios (e.g., `clean_up`, `collaborative_cooking__asymmetric`, `coins`). Each substrate represents a different social simulation environment with specific rules and interactions designed to evaluate multi-agent RL policies in social situations.

Evidence 8: Reinforcement learning task evaluation
- File: `meltingpot/scenario_test.py`
- Function: `test_scenario()`
- Code Reference:
```python
def test_scenario(self, name):
  factory = scenario.get_factory(name)
  num_players = factory.num_focal_players()
  # ... setup specs ...
  with factory.build() as env:
    with self.subTest('step'):
      self.assert_step_matches_specs(env)
```
Tests scenarios which are essentially RL evaluation environments, validating that the interactive simulation framework properly evaluates agent behavior in complex scenarios.

Evidence 9: Environment state transitions
- File: `meltingpot/utils/substrates/wrappers/multiplayer_wrapper_test.py`
- Function: `test_step()`
- Code Reference:
```python
def test_step(self):
  env.step.return_value = dm_env.transition(1, {
      '1.RGB': RGB_VALUE * 1,
      # ... observations ...
      '1.REWARD': REWARD_VALUE * 10,
      '2.REWARD': REWARD_VALUE * 20,
      '3.REWARD': REWARD_VALUE * 30,
      'WORLD.RGB': RGB_VALUE,
  })
```
This demonstrates how environment state evolves based on agent actions, with each agent receiving different observations and rewards based on their interactions within the shared environment.

Evidence 10: Interactive test scenarios with bot policies
- File: `meltingpot/bot_test.py`
- Function: `test_step_without_error()`
- Code Reference:
```python
def test_step_without_error(self, name):
  factory = bot.get_factory(name)
  with factory.build() as policy:
    self.assert_compatible(
        policy,
        timestep_spec=factory.timestep_spec(),
        action_spec=factory.action_spec())
```
Tests bot policies interacting with environments, verifying that agents can successfully engage in multi-step interactive behavior within the simulation framework.