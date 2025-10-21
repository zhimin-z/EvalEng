# Lighteval - Stage 4 (EVALUATE) Evaluation

## Summary
Lighteval provides a comprehensive evaluation framework with strong metric computation capabilities, extensive built-in metrics library, and flexible custom metric support. It excels in per-sample evaluation, aggregate statistics, and multi-modal scoring through custom implementations, though it lacks native multi-modal metrics and some advanced validation features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Evidence: No built-in validation features found. The codebase shows direct metric computation without format validation, schema checks, or policy compliance features. In `src/lighteval/metrics/metrics_sample.py`, metrics directly process model outputs without validation layers. No examples of validation rules in docs or configs. |
| S4F2: Metric Computation | 3 | Evidence: Extensive metric library with 50+ metrics. From `docs/source/metric-list.mdx`: includes BLEU, ROUGE, METEOR, BERTScore (text generation), accuracy, F1, precision, recall (classification), exact match variants, math normalization, perplexity. Per-sample scoring clearly supported via `SampleLevelMetric` class in examples. Custom metrics fully supported via `SampleLevelMetric` and `SampleLevelMetricGrouping` classes. Example: `examples/custom_tasks_templates/custom_yourbench_task.py` shows complete custom metric implementation with sample-level functions and corpus aggregation. |
| S4F3: Evaluator Models | 2 | Evidence: LLM-as-judge supported but limited. `src/lighteval/metrics/metrics_sample.py` shows `JudgeLLM` class with template support. Example in `examples/custom_tasks_templates/custom_yourbench_task.py` shows custom judge implementation with system/user prompts and response processing. No pre-built judge prompts or ensemble support found. Rationale capture exists via judge responses but not standardized. Limited to basic single-evaluator setup requiring custom implementation. |
| S4F4: Multi-Modal Scoring | 1 | Evidence: Minimal multi-modal support. Vision-language model loading exists (`examples/model_configs/transformers_vlm_model.yaml` shows VLM config), but no specialized multi-modal metrics found in metric list or codebase. No CLIP score, CIDEr, SPICE, or other multi-modal metrics in `docs/source/metric-list.mdx`. Multi-modal evaluation would require full custom metric implementation. Infrastructure supports multi-modal inputs but lacks evaluation metrics. |
| S4F5: Aggregate Statistics | 2 | Evidence: Basic aggregation with some advanced features. Corpus-level functions clearly supported: `corpus_level_fn=np.mean` pattern throughout examples. `src/lighteval/metrics/utils/metric_utils.py` shows `SampleLevelMetric` and `CorpusLevelMetric` with aggregation support. Basic stats (mean) prevalent but no evidence of percentiles, confidence intervals, or significance testing in docs or examples. No built-in model comparison tools, ranking systems (Elo, TrueSkill), or stratified statistics found. Weighted metrics possible via custom corpus functions but not built-in. |

## Detailed Analysis

### S4F1: Output Validation and Normalization - 1/3 points

Strengths:
- Normalization support exists via `normalize_gold` and `normalize_pred` parameters in metrics
- Examples show `helm_normalizer` and `math_normalizer` functions (`examples/nanotron/custom_evaluation_tasks.py`)

Weaknesses:
- No format validation (JSON, XML schema checking)
- No policy compliance checks (toxicity, harmful content)
- No sanity checks (duplicate outputs, logical consistency)
- No validation rules or error handling for malformed outputs

Evidence:
```python
# From examples/nanotron/custom_evaluation_tasks.py
Metrics.exact_match(sample_params={"normalize_gold": helm_normalizer, "normalize_pred": helm_normalizer})
```

This shows normalization but no validation framework.

### S4F2: Task-Specific Metric Computation - 3/3 points

Strengths:
- 50+ metrics covering text generation, classification, reasoning, math
- Reference implementations used (likely through external libraries)
- Per-sample scoring fully supported via `SampleLevelMetric`
- Excellent extensibility with custom metric creation

Evidence:
From `docs/source/metric-list.mdx`, extensive metrics including:
- Text: BLEU variants, ROUGE, METEOR, BERTScore, exact_match
- Classification: accuracy, F1, precision, recall
- Math: perfect_exact_match, math_normalizer
- Perplexity: target_perplexity, kl_divergence

Per-sample capability:
```python
# From examples/custom_tasks_templates/custom_yourbench_task.py
class JudgeLLMYourBench(JudgeLLM):
    def compute(self, sample_ids: list[str], responses: list, formatted_docs: list[Doc]) -> list[dict[str, float]]:
        # Returns list of per-sample metrics
        for i in range(len(sample_ids)):
            metrics.append({"accuracy": score[i]})
        return metrics
```

Custom metric example:
```python
# From docs/source/adding-a-new-metric.mdx
my_custom_metric = SampleLevelMetric(
    metric_name="custom_accuracy",
    sample_level_fn=custom_metric,
    corpus_level_fn=agg_function,
)
```

### S4F3: Evaluator Model Integration - 2/3 points

Strengths:
- LLM-as-judge framework exists with `JudgeLLM` class
- Template-based judge prompts supported
- Rationale capture through judge responses

Weaknesses:
- No pre-built judge prompts library
- No ensemble support or disagreement handling
- No specialized evaluator model integrations (RAGAS, G-Eval, Prometheus)
- Requires significant custom implementation

Evidence:
```python
# From examples/custom_tasks_templates/custom_yourbench_task.py
JUDGE_ANSWER_SYSTEM_PROMPT = """You will be provided with the summary of a document..."""

class JudgeLLMYourBench(JudgeLLM):
    def __init__(self):
        super().__init__(
            judge_model_name="gpt-4o-2024-08-06",
            template=get_judge_prompt,
            process_judge_response=process_judge_response_yourbench,
        )
```

Shows custom implementation required for judges.

### S4F4: Multi-Modal Scoring Protocols - 1/3 points

Strengths:
- Infrastructure supports VLMs (vision-language models)
- Can load multi-modal models

Weaknesses:
- No specialized multi-modal metrics in library
- No CLIP score, CIDEr, SPICE, VQA metrics
- No audio-text or video understanding metrics
- Would require full custom metric implementation

Evidence:
```yaml
# From examples/model_configs/transformers_vlm_model.yaml
model_parameters:
  model_name: "Qwen/Qwen2.5-VL-3B-Instruct"
  use_fast_image_processor: true
```

Shows VLM loading capability but metric list in `docs/source/metric-list.mdx` contains only text metrics.

### S4F5: Aggregate Statistics and Cross-Model Comparison - 2/3 points

Strengths:
- Corpus-level aggregation well-supported
- Custom aggregation functions possible
- Sample-to-corpus pipeline clear

Weaknesses:
- Only basic statistics (mean) in examples
- No built-in percentiles, confidence intervals
- No significance testing (t-test, Wilcoxon)
- No ranking systems (Elo, TrueSkill)
- No model comparison tools

Evidence:
```python
# From examples/nanotron/custom_evaluation_tasks.py
yourbench_metrics = CorpusLevelMetricGrouping(
    sample_level_fn=JudgeLLMYourBench(),
    corpus_level_fn={"accuracy": np.mean},  # Only mean aggregation
)
```

```python
# From docs/source/adding-a-new-metric.mdx
def agg_function(items):
    flat_items = [item for sublist in items for item in sublist]
    score = sum(flat_items) / len(flat_items)  # Basic mean only
    return score
```

No evidence of advanced statistics in documentation or examples.

## Overall Assessment

Total Score: 9/15 points

Lighteval excels at core metric computation with an extensive library and excellent extensibility. The per-sample to corpus aggregation pipeline is well-designed. However, it lacks native validation features, multi-modal metrics, and advanced statistical analysis tools. The LLM-as-judge support exists but requires custom implementation for each use case. For text-based evaluation with custom metrics, it's highly capable (3 points). For comprehensive evaluation needs including validation, multi-modal, and statistical comparison, significant custom development is required (1-2 points per feature).