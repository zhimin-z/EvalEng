# MeltingPot (google-deepmind__meltingpot) - Stage 2 (PREPARE) Evaluation

## Summary

MeltingPot is a multi-agent reinforcement learning evaluation suite focused on testing agents in social scenarios. The repository is primarily an execution and evaluation framework for multi-agent RL environments, not a data preparation or infrastructure building tool. It provides pre-built game substrates (environments) and evaluation scenarios with pre-trained bots, but lacks systematic data preprocessing, quality assessment, or infrastructure building capabilities typically required in Stage 2.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No data preprocessing capabilities exist. The framework loads pre-built game environments and scenarios (`meltingpot/configs/substrates/`, `meltingpot/configs/scenarios/`) but provides no data loading, caching, preprocessing pipelines, or physical splitting utilities. It's an environment simulator, not a data preparation tool. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment features. The repository focuses on environment simulation and agent evaluation (`meltingpot/utils/evaluation/`), not data quality checking. No tools for label quality, demographic analysis, duplicate detection, or bias detection are present. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features. The framework deals with simulated multi-agent game environments, not sensitive data requiring privacy protections. No PII-related code or documentation exists. |
| S2F4: Infrastructure Building | 1 | Minimal infrastructure support exists only for environment building, not evaluation infrastructure. The substrate builder (`meltingpot/utils/substrates/builder.py`) constructs game environments from configs, but provides no retrieval systems, databases, or versioning for evaluation artifacts. Example: `examples/tutorial/harvest/configs/environment/harvest.py` shows environment config structure, not data infrastructure. |
| S2F5: Model Validation | 1 | Very basic model loading exists without validation. The evaluation library (`meltingpot/utils/evaluation/evaluation.py`) loads TensorFlow SavedModels from `meltingpot/assets/saved_models/`, but provides no checksum verification, version compatibility checks, or corruption detection. Models are simply loaded with `tf.saved_model.load(path)` without validation. |
| S2F6: Scenario Generation | 2 | Basic scenario configuration exists but limited generation capabilities. Scenarios are manually defined in `meltingpot/configs/scenarios/__init__.py` by specifying substrate + bot combinations. No programmatic variation generation, multi-turn dialogue support, or edge case generation. Example from `configs/scenarios/__init__.py`: scenarios are static configs like `Scenario(substrate='clean_up', num_focal_agents=7, bots=frozenset({'clean_up_0', ...}))`. No templating or parameter sweeps. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial test generation. While some substrates test cooperation/competition behaviors (e.g., `predator_prey`), there's no framework for generating jailbreak attempts, prompt injections, or safety boundary tests. The focus is on multi-agent social dynamics, not adversarial robustness testing. |
| S2F8: Contamination Detection | 0 | No data contamination detection. Since MeltingPot is an environment simulator rather than a dataset-based evaluation framework, contamination checking is not applicable. No code for comparing evaluation data against training corpora exists. |

## Overall Assessment

Total Score: 4/24

MeltingPot is fundamentally a multi-agent RL environment simulator and evaluation harness, not a data preparation framework. It excels at providing pre-built game environments and evaluation scenarios for testing multi-agent policies, but lacks nearly all Stage 2 preparation capabilities:

### What MeltingPot DOES provide:
- Pre-built game substrates (50+ multi-agent environments) in `meltingpot/lua/levels/`
- Pre-configured evaluation scenarios in `meltingpot/configs/scenarios/`
- Pre-trained bot models in `meltingpot/assets/saved_models/`
- Environment building from configs (substrate tutorial in `docs/substrate_tutorial/`)
- Basic model loading for evaluation (no validation)

### What MeltingPot LACKS for Stage 2:
- No data preprocessing: Not applicable - it generates synthetic data via simulation
- No quality assessment: No tools for analyzing dataset quality, bias, or demographics
- No PII handling: Not applicable - synthetic environment data only
- No infrastructure building: No retrieval systems, databases, or artifact versioning beyond environment configs
- No validation: Models loaded without checksum/version checks
- No scenario generation: Scenarios are manually configured, not programmatically generated
- No red-teaming: No adversarial test generation capabilities
- No contamination detection: Not applicable to simulated environments

### Evidence from Code:

1. Environment-focused architecture (`meltingpot/substrate.py`):
```python
def build(substrate_name: str, roles: Sequence[str] = ()) -> dmlab2d.Environment:
  """Builds a substrate by name."""
  # Simply builds game environment, no data preparation
```

2. Static scenario definitions (`meltingpot/configs/scenarios/__init__.py`):
```python
SCENARIOS = immutabledict.immutabledict({
    'clean_up_2': Scenario(
        description='2 resident 5 visitors',
        substrate='clean_up',
        num_focal_agents=2,
        num_background_bots=5,
        bots=frozenset({'clean_up_0', 'clean_up_1', ...}),
    ),
    # All scenarios manually configured - no generation
})
```

3. Basic model loading without validation (`meltingpot/utils/evaluation/evaluation.py`):
```python
def _load_policy(self, bot_name: str) -> saved_model_policy.SavedModelPolicy:
  model_path = self._bots[bot_name].model_path
  policy = saved_model_policy.SavedModelPolicy(model_path)
  # No checksum, version check, or corruption detection
  return policy
```

MeltingPot would need substantial new functionality to support typical Stage 2 evaluation framework requirements. It's designed for a different purpose: providing standardized multi-agent environments for RL research, not preparing and validating evaluation datasets.