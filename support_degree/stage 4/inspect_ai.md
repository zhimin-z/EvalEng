# Inspect AI - Stage 4 (EVALUATE) Evaluation

## Summary
Inspect AI provides a comprehensive evaluation framework with strong built-in metric computation, model-based evaluation capabilities, and sophisticated statistical analysis tools. The framework excels in per-sample scoring, aggregate statistics, and multi-model comparison, though multi-modal scoring support is primarily text-focused with some vision capabilities.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Basic format validation exists but limited comprehensive policy checking. Evidence: The framework includes type validation through Pydantic models (e.g., `examples/structured.py` shows JSON schema validation with `ResponseSchema`), and tools include error handling (e.g., `ToolError` in `examples/tool_use.py`). However, there's no explicit comprehensive policy compliance system, sanity checks, or advanced normalization beyond basic type checking. The `structured.py` example shows `ValidationError` handling but this is primarily for JSON schema compliance rather than broader policy checks. |
| S4F2: Metric Computation | 3 | Extensive metric library with 15+ built-in scorers, per-sample scoring, and strong extensibility. Evidence: The framework provides numerous metrics including `match`, `includes`, `pattern`, `answer`, `choice`, `f1`, `exact`, `model_graded_qa`, `model_graded_fact` (docs/reference/filter/sidebar.py). The `examples/scorer.py` demonstrates custom scorer creation with `@scorer` decorator and shows per-sample scoring with `Score` objects. Metrics support `accuracy()`, `stderr()`, `mean()`, `std()`, `bootstrap_stderr()` reducers. The `TaskState` and scoring system clearly support granular per-sample evaluation with extensible custom metrics. |
| S4F3: Evaluator Models | 3 | Strong LLM-as-judge support with pre-built templates, custom evaluators, and rationale capture. Evidence: The framework includes `model_graded_qa()` and `model_graded_fact()` scorers (docs reference). The `examples/scorer.py` shows using `get_model().generate()` within custom scorers for equivalence checking, demonstrating flexible evaluator model integration. The `examples/theory_of_mind.py` uses `model_graded_fact()` with `self_critique()` showing multi-aspect evaluation. Scorers can capture explanations via `Score.explanation` field, and the system supports async model calls for evaluation. |
| S4F4: Multi-Modal Scoring | 1 | Limited to text-first with basic image support; no comprehensive multi-modal metrics. Evidence: The `examples/images/images.py` shows image input support through dataset samples, and `docs/multimodal.qmd` is mentioned in the structure. The framework supports `ContentImage`, `ContentAudio`, `ContentVideo` types (reference API shows these in model messages). However, there are no specialized multi-modal metrics like CLIP score, CIDEr, SPICE, WER, or cross-modal alignment metrics. The scoring examples focus entirely on text-based evaluation even when images are present. |
| S4F5: Aggregate Statistics | 3 | Comprehensive statistical suite with significance testing, multiple reducers, and rich comparison tools. Evidence: The framework provides multiple metric reducers: `accuracy()`, `mean()`, `std()`, `stderr()`, `bootstrap_stderr()`, `at_least()`, `pass_at()`, `max_score()`, `mean_score()`, `median_score()`, `mode_score()` (docs/reference/filter/sidebar.py). The `docs/dataframe.qmd` and analysis module (`inspect_ai.analysis`) provide DataFrame extraction with `evals_df()`, `samples_df()`, `messages_df()`, `events_df()` for sophisticated analysis. The log system captures detailed metrics (`EvalMetric`, `EvalStats`) and the `examples/evalset.py` shows eval set management with retries and aggregation across multiple tasks/models. |

## Detailed Evidence

### S4F1: Output Validation and Normalization

Format Validation (Partial):
```python
# From examples/structured.py - JSON schema validation
config=GenerateConfig(
    response_schema=ResponseSchema(name="color", json_schema=json_schema(Color))
)

try:
    color = Color.model_validate_json(state.output.completion)
except ValidationError as ex:
    return Score(
        value=INCORRECT,
        answer=state.output.completion,
        explanation=f"Error parsing response: {ex}",
    )
```

Limited Policy Compliance:
The framework doesn't show explicit policy violation checking, content safety validation, or systematic anomaly detection in the provided examples. Tool execution has error handling but not content-based policy checks.

Missing Comprehensive Features:
- No evidence of harmful content detection
- No systematic length constraint validation
- No logical consistency checkers beyond custom scorer logic
- Limited normalization beyond type coercion

### S4F2: Task-Specific Metric Computation

Extensive Coverage:
```python
# From docs/reference/filter/sidebar.py - Available scorers
scorers = [
    "match", "includes", "pattern", "answer", "choice", "f1", "exact",
    "model_graded_qa", "model_graded_fact", "multi_scorer"
]

# Metric reducers
metrics = [
    "accuracy", "mean", "std", "stderr", "bootstrap_stderr",
    "at_least", "pass_at", "max_score", "mean_score", 
    "median_score", "mode_score"
]
```

Per-Sample Scoring:
```python
# From examples/scorer.py
@scorer(metrics=[accuracy(), stderr()])
def expression_equivalence():
    async def score(state: TaskState, target: Target):
        # Per-sample scoring with detailed output
        return Score(
            value=CORRECT if correct else INCORRECT,
            answer=answer,
            explanation=state.output.completion,
        )
    return score
```

Extensibility:
```python
# Custom metric definition from examples/scorer.py
@scorer(metrics=[accuracy(), stderr()])
def score_json_color():
    async def score(state: TaskState, target: Target):
        # Custom scoring logic
        return Score(value=value, answer=state.output.completion)
    return score
```

### S4F3: Evaluator Model Integration

LLM-as-Judge Templates:
```python
# From examples/scorer.py - Model-graded evaluation
prompt = EQUIVALENCE_TEMPLATE % (
    {"expression1": target.text, "expression2": answer}
)
result = await get_model().generate(prompt)
correct = result.completion.lower() == "yes"
```

Pre-built Evaluators:
```python
# From examples/theory_of_mind.py
return Task(
    dataset=example_dataset("theory_of_mind"),
    solver=[chain_of_thought(), generate(), self_critique()],
    scorer=model_graded_fact(),
)
```

Rationale Capture:
```python
# Score objects support explanations
return Score(
    value=INCORRECT,
    explanation="Answer not found in model output: " + state.output.completion,
)
```

### S4F4: Multi-Modal Scoring Protocols

Image Input Support:
```python
# From examples/images/images.py
@task
def images():
    return Task(
        dataset=json_dataset("images.jsonl"),
        solver=[system_message(SYSTEM_MESSAGE), generate()],
        scorer=match(),  # Still text-based scoring
    )
```

Limited Multi-Modal Metrics:
The reference shows `ContentImage`, `ContentAudio`, `ContentVideo` types exist, but no specialized multi-modal scoring metrics are demonstrated:
- No CLIP score for image-text alignment
- No CIDEr/SPICE for image captioning
- No WER for speech recognition
- No temporal consistency metrics for video

Scoring remains primarily text-based even with multi-modal inputs.

### S4F5: Aggregate Statistics and Cross-Model Comparison

Comprehensive Statistics:
```python
# From docs - Available metric reducers
- accuracy() - mean correctness
- mean() - arithmetic mean
- std() - standard deviation  
- stderr() - standard error
- bootstrap_stderr() - bootstrap confidence intervals
- at_least(n) - threshold-based metrics
- pass_at(k) - pass@k metric
- max_score(), mean_score(), median_score(), mode_score() - aggregation methods
```

DataFrame Analysis:
```python
# From docs/dataframe.qmd reference
from inspect_ai.analysis import evals_df, samples_df, messages_df, events_df

# Extract structured data for analysis
evals = evals_df(logs)  # Cross-eval comparison
samples = samples_df(logs)  # Per-sample analysis
messages = messages_df(logs)  # Message-level analysis
events = events_df(logs)  # Event-level analysis
```

Eval Sets with Retries:
```python
# From examples/evalset.py
success, logs = eval_set(
    tasks=[security_guide(), popularity()],
    model=["openai/gpt-4o-mini", "anthropic/claude-3-5-haiku-latest"],
    log_dir=log_dir,
    max_tasks=max_tasks,
    retry_attempts=retry_attempts,
)
```

Statistical Comparison Support:
The framework provides extensive logging (`EvalLog`, `EvalStats`, `EvalMetric`) that enables comparison, though explicit significance testing (t-test, Wilcoxon) would need to be implemented using the DataFrame outputs and external libraries like scipy.

## Strengths
1. Rich Metric Library: 15+ built-in scorers covering text generation, classification, and QA tasks
2. Model-Graded Evaluation: Strong support for LLM-as-judge patterns with templates
3. Per-Sample Granularity: Excellent support for per-sample scoring with detailed explanations
4. Extensibility: Clean decorator-based API for custom metrics
5. Statistical Analysis: Comprehensive DataFrame extraction for analysis
6. Eval Management: Sophisticated eval set handling with retries and progress tracking

## Limitations
1. Multi-Modal Metrics: Lacks specialized metrics for vision, audio, and video evaluation
2. Policy Validation: No built-in content safety or policy compliance checking
3. Formal Testing: No explicit significance testing or effect size computation in core
4. Ranking Systems: No built-in Elo, TrueSkill, or tournament comparison systems