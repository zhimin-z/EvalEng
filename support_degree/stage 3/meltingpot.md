# Melting Pot (google-deepmind__meltingpot) - Stage 3 (EXECUTE) Evaluation

## Summary

Melting Pot is a multi-agent reinforcement learning research environment/benchmark, NOT an evaluation framework for LLMs. It provides game environments (substrates) for training and evaluating multi-agent RL algorithms, with pre-trained bots and scenarios for testing generalization. The framework has minimal execution orchestration focused on RL episodes rather than LLM evaluation pipelines. It lacks LLM-specific features like prompt caching, API cost tracking, or checkpoint-based resumption.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No evaluation pipeline orchestration exists. Melting Pot is a multi-agent RL environment framework, not an LLM evaluation harness. The "evaluation" in `meltingpot/utils/evaluation/evaluation.py` refers to running RL agents in game scenarios, not orchestrating LLM evaluation workflows. There is no support for routing tasks, DAG-based workflows, or conditional branching for LLM evaluations. Evidence: The README states it's "A suite of test scenarios for multi-agent reinforcement learning" and examples show RL training (`examples/rllib/self_play_train.py`), not LLM evaluation pipelines. |
| S3F2: Inference & Telemetry | 0 | No LLM inference telemetry. The framework tracks RL episode metrics (rewards, episode length) but has no latency tracking (TTFT, TPS), throughput measurement, GPU utilization monitoring, or API cost tracking for LLM inference. The `evaluation.py` module returns scenario outcomes for RL bots, not inference performance metrics. Evidence: `meltingpot/utils/evaluation/evaluation.py` contains functions like `scenario_sample()` that return episode data, but no telemetry for model inference. The RLlib integration (`examples/rllib/`) uses Ray's metrics, not LLM-specific telemetry. |
| S3F3: Test-Time Optimization | 0 | No test-time compute optimization for LLMs. The framework has no prompt caching, KV cache management, dynamic batching, or other LLM inference optimizations. It's designed for RL agent execution in game environments, which operates on a fundamentally different paradigm (discrete actions in episodes) than LLM generation. Evidence: No caching logic found in codebase. The `substrate.py` and `scenario.py` modules manage game state, not LLM inference optimization. |
| S3F4: Failure Handling | 1 | Minimal failure handling, not designed for long-running evaluations. The framework has basic episode timeout (`maxEpisodeLengthFrames` in configs like `fruit_market.py`) and can handle agent failures within episodes, but lacks retry logic, exponential backoff, circuit breakers, or sophisticated error recovery for evaluation runs. The focus is on single-episode execution rather than robust multi-hour evaluation campaigns. Evidence: Config files show `maxEpisodeLengthFrames` parameter (e.g., `fruit_market.py:1083`), but no retry/recovery mechanisms in evaluation code. The `bin/test.sh` script is for unit tests, not evaluation resilience. |
| S3F5: Checkpointing | 0 | No evaluation checkpointing. While RL training with RLlib supports model checkpointing (`examples/rllib/view_models.py` loads checkpoints), there is no mechanism to checkpoint and resume evaluation progress across scenarios. The evaluation module runs scenarios independently without state persistence between runs. Evidence: `meltingpot/utils/evaluation/evaluation.py` has no checkpoint saving/loading. Each `scenario_sample()` call is independent. The RLlib checkpoint logic is for model weights, not evaluation state. |
| S3F6: Distributed Execution | 1 | Limited distributed support via RLlib, not evaluation-focused. The RLlib integration supports multi-worker rollouts for RL training (`num_rollout_workers` in `self_play_train.py:30`), but this is for parallel game episode collection, not distributed LLM evaluation. There's no budget enforcement (cost/token limits) or evaluation-specific job scheduling. Evidence: `examples/rllib/self_play_train.py` shows `num_rollout_workers=2` for parallel RL rollouts, but no evaluation-specific distributed execution. No budget tracking code found. GitHub Actions CI (`test-examples.yml`) runs tests sequentially. |
| S3F7: Human Evaluation | 1 | Human playable demos only, no crowdsourcing integration. The framework provides interactive human player scripts (`meltingpot/human_players/play_*.py`) for manual playtesting of substrates, but has no integration with crowdsourcing platforms (MTurk, Scale AI), annotation interfaces, quality control mechanisms, or inter-rater agreement metrics. Evidence: `meltingpot/human_players/play_clean_up.py` shows a pygame-based manual play interface, but no crowdsourcing API. The `level_playing_utils.py` module handles keyboard input for local play only. No annotation workflow found. |

## Key Observations

Critical Misalignment: This repository is fundamentally a multi-agent RL research environment, not an LLM evaluation framework. It provides:

1. Game Substrates: Complex multi-agent environments like "Fruit Market" and "Commons Harvest" (see `meltingpot/configs/substrates/`)
2. Bot Training: Integration with RLlib for training RL policies (`examples/rllib/self_play_train.py`)
3. Generalization Testing: Pre-trained bots and scenarios to test agent generalization (`meltingpot/configs/bots/`, `meltingpot/configs/scenarios/`)

What's Missing for LLM Evaluation:
- No support for LLM APIs (OpenAI, Anthropic, etc.)
- No prompt/response handling
- No dataset loading for NLP benchmarks
- No evaluation metrics for language tasks (accuracy, BLEU, F1, etc.)
- No cost tracking or rate limiting for API calls
- No checkpoint-based evaluation resumption

Evidence of RL Focus:
- README states: "Melting Pot assesses generalization to novel social situations involving both familiar and unfamiliar individuals" (line 28)
- Documentation references "substrates" (game levels) and "scenarios" (bot configurations), not LLM tasks
- Core modules are `substrate.py` and `scenario.py` for game environments
- Examples show RL training loops with RLlib, not LLM evaluation scripts

Potential Confusion: The term "evaluation" appears in `meltingpot/utils/evaluation/`, but this refers to evaluating RL agent performance in game scenarios, not evaluating LLMs on language benchmarks. The `evaluation.py` module runs pre-trained SavedModel policies in substrates and collects episode metrics.

## Conclusion

Melting Pot scores 3/21 total points across Stage 3 features. It is not suitable for LLM evaluation and should not be compared to frameworks like lm-evaluation-harness or HELM. The repository's purpose is to provide challenging multi-agent environments for RL research, similar to OpenAI Gym or PettingZoo, but with a focus on social generalization scenarios.

If the goal is to evaluate LLMs on tasks, this framework is the wrong tool. If the goal is to test multi-agent RL algorithms in social dilemma games, Melting Pot is well-designed for that purpose (but outside the scope of this LLM evaluation rubric).