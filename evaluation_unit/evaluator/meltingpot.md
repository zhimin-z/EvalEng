## Evaluator Categories

[Environmental]

## Detailed Analysis

### Environmental

Evidence 1: Core environment interaction loop
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
This function executes model interactions with simulation environments (substrates), implementing the core evaluation loop where agents perform actions and receive environmental feedback. The substrate acts as a game environment that provides timesteps and rewards based on model actions, making it a pure environmental evaluator where the simulator itself determines assessment through its state transitions and reward signals.

Evidence 2: Episode execution with environmental metrics collection
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
  """Runs a population on a substrate and returns results.
  
  Returns:
    A dataframe of results. One row for each episode with columns:
      background_player_names: the names of each background player.
      background_player_returns: the episode returns for each background player.
      focal_player_names: the names of each focal player.
      focal_player_returns: the episode returns for each focal player.
      video_path: a path to a video of the episode.
  """
```
This function runs multiple episodes and collects evaluation metrics including player returns (cumulative rewards) derived directly from environmental feedback during substrate execution. The key metrics `focal_player_returns` and `background_player_returns` are computed from rewards provided by the simulation environment itself, demonstrating pure environmental evaluation where the simulator generates all assessment signals without external judgment.

Evidence 3: Environmental reward accumulation
- File: `meltingpot/utils/evaluation/return_subject.py`
- Class: `ReturnSubject`
- Code Reference:
```python
class ReturnSubject(Subject):
  """Subject that computes episode returns from timesteps."""
  
  def on_next(self, timestep):
    # Accumulates rewards from environment timesteps
    # and emits episode returns when episode terminates
```
This evaluator accumulates rewards from environment timesteps to compute episode returns, processing simulator-provided feedback rather than applying external judgment. The rewards originate from the substrate (game environment) execution, making this a clear example of environmental evaluation where assessment comes from direct interaction with the target system.

Evidence 4: Multi-agent game substrates as evaluation environments
- File: `meltingpot/substrate_test.py` and `README.md`
- Code Reference:
```python
@parameterized.named_parameters((name, name) for name in substrate.SUBSTRATES)
class PerSubstrateTestCase(test_utils.SubstrateTestCase):

  def test_substrate(self, name):
    factory = substrate.get_factory(name)
    roles = factory.default_player_roles()
    # ... builds environment
    with factory.build(roles) as env:
      with self.subTest('step'):
        self.assert_step_matches_specs(env)
```
The substrates are multi-agent reinforcement learning game environments that provide rewards, observations, and termination signals based on agent actions. As stated in the documentation, "Melting Pot offers researchers a set of over 50 multi-agent reinforcement learning substrates (multi-agent games) on which to train agents, and over 256 unique test scenarios." These are classic RL simulation environments that evaluate agent performance through environmental feedback (game scores, rewards from interactions), representing the fundamental environmental evaluator pattern where the system itself determines success.

Evidence 5: Scenario-based environmental evaluation
- File: `meltingpot/scenario_test.py`
- Function: `test_scenario()`
- Code Reference:
```python
def test_scenario(self, name):
    factory = scenario.get_factory(name)
    num_players = factory.num_focal_players()
    # ... 
    with factory.build() as env:
      with self.subTest('step'):
        self.assert_step_matches_specs(env)
```
Scenarios are evaluation configurations that wrap substrates to test agents in specific social situations within the game environments. The evaluation happens through environment execution where the simulator provides rewards and feedback based on agent performance, extending the environmental evaluation approach to structured test cases while maintaining the core principle of simulator-provided assessment.

Evidence 6: Task-based environmental objectives
- File: `meltingpot/configs/substrates/collaborative_cooking__asymmetric.py`
- Code Reference:
```python
"""Configuration for Collaborative Cooking: Asymmetric.

The recipe they must follow is for tomato soup:
1.   Add three tomatoes to the cooking pot.
2.   Wait for the soup to cook (status bar completion).
3.   Bring a bowl to the pot and pour the soup from the pot into the bowl.
4.   Deliver the bowl of soup at the goal location.

This substrate is a pure common interest game. All players share all rewards.
"""
```
This describes a task-based evaluation environment where agents must accomplish specific procedural goals, with success measured entirely by the environment (completing the recipe steps, delivering soup). Rewards are provided by the simulator based on task completion, demonstrating how environmental evaluators can encode complex objective functions directly into the simulation mechanics rather than requiring external assessment of outcomes.