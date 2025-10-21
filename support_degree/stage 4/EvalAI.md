# EvalAI - Stage 4 (EVALUATE) Evaluation

## Summary
EvalAI is a platform for hosting AI challenges where participants submit predictions/code that are evaluated against test annotations. The framework provides basic metric computation through custom Python evaluation scripts, supports custom metrics per challenge, and includes aggregation statistics. However, it lacks built-in validation, pre-built evaluator models, multi-modal scoring infrastructure, and statistical comparison tools.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation exists. Evaluation scripts must implement their own validation logic. No framework-level format validation, policy checks, or normalization. Evidence: `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md` shows evaluation scripts only receive file paths and must handle all validation manually. The only error detection is checking if `'result'` key exists in output (from `docs/source/submission.md`): "Currently, the only way to check for the occurrence of an error is to check if the key `result` exists in `submission_output`". |
| S4F2: Metric Computation | 2 | Custom metrics supported per challenge but no built-in metric library. Each challenge defines its own metrics in evaluation scripts. Per-sample scores possible but not standardized. Evidence: `docs/source/configuration.md` shows metrics are defined in leaderboard schema (`"labels": ["Metric1", "Metric2", "Metric3", "Total"]`) but computation is entirely custom. From `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md`: hosts write their own `evaluate()` function with arbitrary metric logic. No reference implementations of BLEU, ROUGE, F1, etc. provided. |
| S4F3: Evaluator Models | 1 | No LLM-as-judge or evaluator model integration. Evaluation is purely code-based through custom scripts. Evidence: The entire evaluation pipeline described in `docs/source/submission.md` shows worker calling `EVALUATION_SCRIPTS[challenge_id].evaluate(*params)` - a custom Python function. No mention of evaluator models, judge prompts, or ensemble scoring in any documentation. The `evaluate()` function signature in `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md` only accepts annotation files, not evaluator model configs. |
| S4F4: Multi-Modal Scoring | 0 | Text-only evaluation infrastructure. No multi-modal metrics, validators, or artifact handling mentioned. Evidence: All examples in `examples/` directories use `.txt` and `.json` annotation files. Configuration in `docs/source/configuration.md` and `docs/source/02-for-challenge-hosts/templates/example-challenges.md` shows only generic file uploads (`allowed_submission_file_types: ".json, .zip, .txt, .tsv, .gz, .csv, .h5, .npy"`). No vision, audio, or video evaluation capabilities documented anywhere. |
| S4F5: Aggregate Statistics | 1 | Basic aggregation through custom code only. No built-in statistical tools, significance testing, or model comparison features. Evidence: `docs/source/configuration.md` shows leaderboard displays metrics with `"sort_ascending"` and `"default_order_by"` but these are just display settings. From submission worker description in `docs/source/submission.md`: "LeaderBoardData objects are also created (in bulk) with the required parameters" - just stores individual scores. No percentiles, confidence intervals, t-tests, or ranking systems provided. Hosts must implement all statistical analysis externally. |

## Detailed Analysis

### S4F1: Output Validation and Normalization (1/3)

Evidence of minimal validation:

From `docs/source/submission.md`:
```
The output from the `evaluate` function is stored in a variable called `submission_output`. 
Currently, the only way to check for the occurrence of an error is to check if the key 
`result` exists in `submission_output`.

* If the key does not exist, then the submission is marked as __FAILED__.
* If the key exists, then the variable `submission_output` is parsed
```

This shows validation is limited to checking if a single key exists. No:
- Format validation (JSON/XML schema checking)
- Policy compliance checks (harmful content, length constraints)
- Sanity checks (anomaly detection, consistency checks)
- Normalization capabilities (standardizing formats, case/whitespace handling)

Why not 0 points: The framework does capture stderr/stdout and marks submissions as FAILED if they don't return the expected format, providing minimal error handling.

### S4F2: Task-Specific Metric Computation (2/3)

Evidence of custom-only metrics:

From `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md`:
```python
output = {}
output['result'] = [
            {
                'train_split': {
                    'Metric1': 123,
                    'Metric2': 123,
                    'Metric3': 123,
                    'Total': 123,
                }
            },
```

The framework allows arbitrary metric names but provides:
- ❌ No built-in metrics (BLEU, ROUGE, F1, etc.)
- ❌ No reference implementations
- ✅ Per-sample scoring possible (though not demonstrated)
- ✅ Custom metric definitions supported
- ✅ Multiple metrics per challenge

From `docs/source/configuration.md`:
```yaml
leaderboard:
  - id: 1
    schema: {
      "labels": ["Metric1", "Metric2", "Metric3", "Total"],
      "default_order_by": "Total",
```

Why not 3 points: No metric library exists. Every challenge must implement metrics from scratch, without reference implementations or edge case handling.

Why not 1 point: The framework does support multiple custom metrics, per-phase metrics, and extensibility through Python code.

### S4F3: Evaluator Model Integration (1/3)

Evidence of absence:

The evaluation architecture from `docs/source/submission.md` shows:
```python
EVALUATION_SCRIPTS = {
    <challenge_pk> : <evalutaion_script_loaded_as_module>,
    ....
}
```

```
The `evaluate` function of `EVALUATION_SCRIPTS` map with key of the challenge id is called.
```

No mention of:
- LLM-as-judge capabilities
- Evaluator model configurations
- Pre-built judge prompts
- Specialized evaluator models (RAGAS, G-Eval, Prometheus)
- Ensemble scoring
- Rationale capture

The evaluation function signature only accepts annotation files:
```python
def evaluate(test_annotation_file, user_annotation_file, phase_codename, kwargs):
```

Why not 0 points: The `kwargs` mechanism does support passing submission metadata which could theoretically be used to call external evaluators, though this is not documented or encouraged.

### S4F4: Multi-Modal Scoring Protocols (0/3)

Evidence of text-only support:

From `docs/source/configuration.md`:
```yaml
allowed_submission_file_types: ".json, .zip, .txt, .tsv, .gz, .csv, .h5, .npy"
```

Example annotation files in `examples/example1/test_annotation.txt`:
```txt
1
2
3
4
5
```

No documentation exists for:
- Image captioning metrics (CIDEr, SPICE)
- Vision-language evaluation
- Audio/video metrics
- Cross-modal retrieval
- Multi-modal artifact handling

Why 0 points: The platform is designed exclusively for prediction file-based challenges with no multi-modal infrastructure.

### S4F5: Aggregate Statistics and Cross-Model Comparison (1/3)

Evidence of minimal aggregation:

From `docs/source/configuration.md`, leaderboard only supports:
```yaml
"sort_ascending": false,
"description": "Metric Description"
```

And:
```yaml
leaderboard_decimal_precision: 2
is_leaderboard_order_descending: True
```

This provides:
- ❌ No percentiles (P25, P50, P75, P95, P99)
- ❌ No confidence intervals
- ❌ No distribution analysis
- ❌ No significance testing (t-test, Wilcoxon)
- ❌ No bootstrap methods
- ❌ No Elo/TrueSkill ranking systems
- ✅ Basic sorting/ordering
- ✅ Decimal precision control

From `docs/source/submission.md`:
```
LeaderBoardData objects are also created (in bulk) with the required parameters.
```

This shows the system stores individual submission scores but provides no statistical analysis tools.

Why not 0 points: The framework does compute and display aggregate scores (mean across test set) and supports weighted metrics implicitly through custom evaluation scripts.

Why not 2 points: No built-in statistical functions, comparison tools, or analytical capabilities exist beyond basic mean computation and sorting.

## Key Strengths
1. Flexible metric definition: Arbitrary metrics can be defined per challenge
2. Per-phase customization: Different metrics/evaluation logic per challenge phase
3. Extensible evaluation: Python-based evaluation scripts allow complex logic
4. Metadata capture: Submission metadata available for custom processing

## Key Weaknesses
1. No validation framework: Each challenge must implement format/policy validation manually
2. No metric library: No reference implementations of standard metrics
3. No evaluator models: Cannot use LLMs or specialized models as judges
4. Text-only: No multi-modal evaluation infrastructure
5. No statistical tools: No significance testing, confidence intervals, or comparison utilities
6. Manual everything: Most evaluation logic must be built from scratch per challenge

## Recommendations for Improvement
1. Add format validation layer before evaluation (JSON schema, file structure checks)
2. Build metric library with reference implementations (BLEU, ROUGE, F1, etc.)
3. Add LLM-as-judge integration for subjective evaluation
4. Implement statistical comparison utilities (t-tests, bootstrap CIs)
5. Add multi-modal artifact handling for vision/audio challenges
6. Provide per-sample score extraction and analysis tools