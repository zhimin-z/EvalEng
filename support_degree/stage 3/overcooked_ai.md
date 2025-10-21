# Overcooked AI - Stage 3 (EXECUTE) Evaluation

## Summary
Overcooked AI is a cooperative multi-agent reinforcement learning environment, not an LLM evaluation framework. It provides game simulation and agent interaction infrastructure but lacks most execution-stage evaluation capabilities expected of LLM testing frameworks. The codebase focuses on reinforcement learning agent training/deployment rather than systematic LLM evaluation with performance monitoring, resilience, and resource management.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No evaluation pipeline orchestration exists. The codebase provides game loop execution (`src/overcooked_demo/server/game.py:play_game()`) but no DAG workflows, task routing, or protocol support for evaluations. The `AgentEvaluator` class (`src/overcooked_ai_py/agents/benchmarking.py`) only runs sequential game episodes without dependency management or conditional branching. |
| S3F2: Inference & Telemetry | 1 | Minimal metrics exist. The game loop tracks basic timing (`time_left`, `time_elapsed` in `src/overcooked_demo/server/game.py:apply_actions()`) and sparse rewards, but lacks comprehensive telemetry like TTFT, throughput, percentiles, GPU utilization, or API cost tracking. No structured monitoring dashboard or real-time metrics collection framework is present. |
| S3F3: Test-Time Optimization | 0 | No caching, batching, or optimization features for evaluation. The code runs agent forward passes sequentially (`src/overcooked_demo/server/game.py:npc_policy_consumer()`) without any prompt caching, KV cache management, or batch processing. No support for speculative decoding, quantization, or model compilation. |
| S3F4: Failure Handling | 1 | Minimal error handling exists. The server has basic socket disconnect handling (`src/overcooked_demo/server/app.py:on_disconnect()`) and game cleanup on errors, but no retry logic, exponential backoff, circuit breakers, or intelligent failure recovery. Errors in agent loading are caught but not automatically retried (`src/overcooked_demo/server/game.py:get_policy()`). |
| S3F5: Checkpointing | 0 | No evaluation checkpointing or resumption capability. The game tracks trajectory data (`src/overcooked_demo/server/game.py:trajectory`) but this is for post-hoc analysis, not for resuming interrupted evaluations. No mechanism to save partial evaluation progress and continue from that point. |
| S3F6: Distributed Execution | 0 | No distributed execution infrastructure. The codebase mentions Ray (`src/overcooked_demo/server/game.py` imports Ray for agent loading) but doesn't use it for distributed evaluation. All game instances run on a single process with thread-based concurrency. No multi-GPU, multi-node, load balancing, or budget enforcement features. Config limits max games (`MAX_GAMES=10` in `src/overcooked_demo/server/config.json`) but this is capacity management, not distributed scheduling. |
| S3F7: Human Evaluation | 2 | Basic human-in-the-loop gameplay exists. The web interface (`src/overcooked_demo/server/templates/`) allows humans to play alongside AI agents, and trajectory data is collected (`src/overcooked_demo/server/game.py:apply_actions()` stores human actions). However, there's no crowdsourcing platform integration, annotation UI builder, quality control mechanisms (attention checks, gold standards), or agreement metrics (Cohen's kappa, etc). The README mentions human data collection was done via MTurk but provides no automation or tooling for this. |

## Detailed Analysis

### S3F1: Pipeline Orchestration (0 pts)
Evidence of absence:
- The `AgentEvaluator` class in `src/overcooked_ai_py/agents/benchmarking.py` only provides `evaluate_agent_pair()` which runs a simple loop:
```python
def evaluate_agent_pair(self, ap, num_games=1, game_length=None, ...):
    """Evaluate agent pair over num_games"""
    for _ in range(num_games):
        # Simple sequential execution
        state = self.env.reset()
        for t in range(horizon):
            joint_action = ap.joint_action(state)
            state, reward, done, info = self.env.step(joint_action)
```
- No support for DAG-based workflows, task dependencies, or conditional execution paths
- No protocol support for different evaluation types (zero-shot, few-shot, chain-of-thought)
- Game loop in `src/overcooked_demo/server/game.py:play_game()` is purely sequential with no branching logic

### S3F2: Inference & Telemetry (1 pt)
Evidence:
- Basic timing metrics in `src/overcooked_demo/server/game.py:apply_actions()`:
```python
transition = {
    "state": json.dumps(prev_state.to_dict()),
    "time_left": max(self.max_time - (time() - self.start_time), 0),
    "time_elapsed": time() - self.start_time,
    "cur_gameloop": self.curr_tick,
    "score": self.score,
}
```
- Only tracks wall-clock time, game ticks, and sparse reward
- No latency percentiles, throughput metrics, memory usage, GPU utilization, or cost tracking
- No real-time monitoring dashboard or structured logging framework

### S3F3: Test-Time Optimization (0 pts)
Evidence of absence:
- Agent actions are computed sequentially without batching in `src/overcooked_demo/server/game.py:npc_policy_consumer()`:
```python
def npc_policy_consumer(self, policy_id):
    while self._is_active:
        state = queue.get()  # Blocking, one at a time
        npc_action, _ = policy.action(state)  # No batching
        super(OvercookedGame, self).enqueue_action(policy_id, npc_action)
```
- No caching infrastructure mentioned in any file
- No optimization techniques like quantization, model compilation, or speculative decoding

### S3F4: Failure Handling (1 pt)
Evidence:
- Basic error handling in agent loading (`src/overcooked_demo/server/game.py:get_policy()`):
```python
def get_policy(self, npc_id, idx=0):
    try:
        agent = load_agent(fpath, agent_index=idx)
        return agent
    except Exception as e:
        raise IOError("Error loading Rllib Agent\n{}".format(e.__repr__()))
```
- Socket disconnect handling in `src/overcooked_demo/server/app.py:on_disconnect()`
- No retry logic, exponential backoff, circuit breakers, or failure categorization
- Errors terminate execution rather than attempting recovery

### S3F5: Checkpointing (0 pts)
Evidence of absence:
- Trajectory storage in `src/overcooked_demo/server/game.py` is for post-hoc analysis only:
```python
self.trajectory.append(transition)
# Later saved to file but not used for resumption
```
- No checkpoint creation during evaluation
- No mechanism to resume interrupted evaluations from saved state
- The `AgentEvaluator` always runs fresh evaluations from start

### S3F6: Distributed Execution (0 pts)
Evidence of absence:
- Single-process execution with threading in `src/overcooked_demo/server/app.py`
- Config shows capacity limits but no distribution: `"MAX_GAMES": 10` in `src/overcooked_demo/server/config.json`
- Ray is imported but only used for loading pre-trained agents, not for distributed execution:
```python
# src/overcooked_demo/server/game.py
agent = load_agent(fpath, agent_index=idx)
# Always kill ray after loading
if ray.is_initialized():
    ray.shutdown()
```
- No multi-GPU, multi-node, or budget enforcement features

### S3F7: Human Evaluation (2 pts)
Evidence:
- Web interface for human gameplay in `src/overcooked_demo/server/templates/index.html` and associated JavaScript
- Human action collection in `src/overcooked_demo/server/game.py:apply_actions()`:
```python
if self.players[i] in self.human_players:
    try:
        joint_action[i] = self.pending_actions[i].get(block=False)
```
- Trajectory data includes human/AI indicators:
```python
"player_0_is_human": self.players[0] in self.human_players,
"player_1_is_human": self.players[1] in self.human_players,
```
- README mentions MTurk data collection but no automation: "Data was collected through Mturk and is fully anonymized"
- No crowdsourcing platform integration, quality control (attention checks, gold standards), or agreement metrics
- No annotation UI builder or mobile support for raters

## Key Limitations

1. Not an LLM Evaluation Framework: This is a game simulation environment for RL, not designed for LLM evaluation
2. No Orchestration: Evaluations are simple loops without DAG support, conditional branching, or protocol management
3. Minimal Monitoring: Only basic game metrics tracked; no comprehensive telemetry or real-time monitoring
4. No Optimization: Sequential execution without caching, batching, or any test-time optimizations
5. No Resilience: Basic error handling but no retry logic, circuit breakers, or intelligent failure recovery
6. No Checkpointing: Cannot save/resume evaluation progress
7. Single-Node Only: No distributed execution capabilities despite Ray being available
8. Limited Human Eval: Basic human-in-the-loop gameplay but no crowdsourcing integration or quality control

## Conclusion

Overcooked AI scores 4/21 overall for Stage 3 execution capabilities. It provides a functional game environment with minimal metrics collection and basic human gameplay support, but lacks the sophisticated execution infrastructure expected of modern LLM evaluation frameworks. The codebase is purpose-built for reinforcement learning research rather than systematic LLM evaluation with performance monitoring, optimization, and resilience features.