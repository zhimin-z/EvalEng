# Ragas - Stage 4 (EVALUATE) Evaluation

## Summary
Ragas provides a comprehensive metric computation framework with strong support for LLM-based evaluators, custom metrics, and per-sample scoring. The framework excels at evaluator model integration and has decent aggregate statistics support. However, it lacks built-in output validation, has limited traditional ML metrics, no multi-modal scoring capabilities, and minimal statistical comparison tools.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation features. Only basic data schema validation through Pydantic models (`src/ragas/dataset_schema.py`, `src/ragas/validation.py`). No format validation, policy compliance checks, or normalization utilities. Users must implement validation manually. Example from `src/ragas/validation.py` shows only schema validation, not malformed output detection or sanity checks. |
| S4F2: Metric Computation | 2 | ~15-20 metrics available but heavily skewed toward LLM-based metrics. Coverage includes LLM-judge metrics (`AspectCritic`, `faithfulness`, `answer_relevancy` in `src/ragas/metrics/`), some traditional metrics (`ChrF`, `RougeScore` from examples), but missing standard ML metrics (precision/recall/F1 for classification, NDCG for retrieval). Per-sample scoring works via `.single_turn_ascore()`. Custom metrics supported via decorators (`@numeric_metric`, `@discrete_metric` in examples). Extensible but limited coverage of traditional metrics. |
| S4F3: Evaluator Models | 3 | Excellent LLM-as-judge support. Pre-built judge metrics with configurable criteria (`DiscreteMetric`, `AspectCritic` in `src/ragas/metrics/`). Supports multiple LLM providers (OpenAI, Google, Anthropic via `src/ragas/llms/`). Rationale capture built-in (`MetricResult` includes `reason` field). Ensemble scoring possible by running multiple metrics. Examples show custom judge prompts in `examples/ragas_examples/workflow_eval/evals.py`: `DiscreteMetric(name="response_quality", prompt="...")`. Strong evaluator integration. |
| S4F4: Multi-Modal Scoring | 0 | Text-only framework. No vision-language metrics (no CLIP score, CIDEr, SPICE). No audio-text metrics (no WER). No video understanding. Repository structure and documentation show exclusively text-based evaluation. Multi-modal artifacts not supported. |
| S4F5: Aggregate Statistics | 2 | Basic statistics available through pandas DataFrames (experiments return DataFrames with results). Per documentation, results can be aggregated using standard pandas operations. No built-in significance testing, bootstrap CIs, or ranking systems (Elo/TrueSkill). Examples show manual aggregation in `examples/ragas_examples/*/evals.py` with basic mean calculations. No advanced statistical comparison tools. Weighted metrics not explicitly supported beyond manual implementation. |

## Evidence Details

### S4F1: Output Validation (1 point)
Evidence from repository:

1. Schema validation only - `src/ragas/validation.py`:
```python
from pydantic import BaseModel, ValidationError

# Basic schema validation through Pydantic models
# No format validation, policy checks, or normalization
```

2. Dataset schema - `src/ragas/dataset_schema.py`:
```python
# Defines SingleTurnSample, MultiTurnSample schemas
# Only validates structure, not content quality
```

3. No validation utilities - Searched for validation features:
- No JSON/XML format validators
- No policy compliance checkers (harmful content, length constraints)
- No sanity checks (anomaly detection, logical consistency)
- No normalization utilities (case, whitespace, structured extraction)

Rating justification: Framework provides only basic Pydantic schema validation. Users must implement all output validation, format checking, policy compliance, and normalization themselves. This is minimal functionality requiring significant manual work.

### S4F2: Metric Computation (2 points)
Evidence from repository:

1. Available metrics - `src/ragas/metrics/` directory shows:
   - LLM-based: `AspectCritic`, `faithfulness`, `answer_relevancy`, `context_precision`, `SimpleClassifier`
   - Traditional: `RougeScore`, `BleuScore`, `ChrF` (from examples)
   - Total: ~15-20 metrics estimated from codebase

2. Missing standard metrics:
   - No classification metrics (accuracy, precision, recall, F1, AUC-ROC) as built-ins
   - No retrieval metrics (P@k, R@k, NDCG, MRR, MAP)
   - No safety metrics (toxicity, bias scores)

3. Per-sample scoring - From quickstart example:
```python
from ragas.metrics import AspectCritic
metric = AspectCritic(name="summary_accuracy", llm=evaluator_llm, definition="...")
await metric.single_turn_ascore(SingleTurnSample(test_data))
# Returns per-sample score
```

4. Custom metrics - From examples:
```python
from ragas.metrics import discrete_metric, numeric_metric

@discrete_metric(name="accuracy", allowed_values=["pass", "fail"])
def my_metric(prediction: str, actual: str):
    return MetricResult(value="pass", reason="")

@numeric_metric(name="correctness")
def correctness_metric(prediction: float, actual: float):
    return MetricResult(value=1.0 if abs(prediction - actual) < 1e-5 else 0.0)
```

Rating justification: Framework has 15-20 metrics with good custom metric support, but coverage heavily skewed to LLM-based metrics. Missing many standard ML evaluation metrics. Per-sample scoring works well. Extensible architecture but requires building most traditional metrics yourself.

### S4F3: Evaluator Models (3 points)
Evidence from repository:

1. Pre-built judge prompts - `src/ragas/metrics/discrete.py`:
```python
class DiscreteMetric(Metric):
    """LLM-as-judge with configurable prompt"""
    prompt: str
    allowed_values: List[str]
```

2. Multi-aspect scoring - Example from quickstart:
```python
metric = AspectCritic(
    name="summary_accuracy",
    llm=evaluator_llm,
    definition="Verify if the summary is accurate."
)
```

3. Multiple LLM providers - `src/ragas/llms/` shows:
   - OpenAI (`langchain_openai.py`)
   - Google Gemini (`langchain_google.py`)  
   - Anthropic, Azure, Bedrock, etc.

4. Rationale capture - `src/ragas/metrics/result.py`:
```python
class MetricResult(BaseModel):
    value: Union[float, str]
    reason: str  # Captures evaluator reasoning
```

5. Ensemble example - From workflow tutorial:
```python
# Run multiple evaluators
score1 = metric1.score(llm=llm, response=response, ...)
score2 = metric2.score(llm=llm, response=response, ...)
# Can aggregate multiple scores
```

Rating justification: Excellent LLM-as-judge capabilities with pre-built metrics, configurable prompts, multi-aspect scoring, multiple LLM providers, automatic rationale capture, and ensemble support. All features work well out-of-box with clear documentation. Deserves full 3 points.

### S4F4: Multi-Modal Scoring (0 points)
Evidence from repository:

1. Text-only documentation - All tutorials in `docs/tutorials/` show text-only examples:
   - `prompt.md`: Text classification
   - `rag.md`: Text retrieval and generation
   - `agent.md`: Mathematical text expressions
   - `workflow.md`: Email text processing

2. No multi-modal metrics - Searched `src/ragas/metrics/`:
   - No vision-language metrics (CLIP, CIDEr, SPICE)
   - No audio metrics (WER, MOS)
   - No video metrics
   - No multi-modal artifact handling

3. Schema is text-only - `src/ragas/dataset_schema.py`:
```python
class SingleTurnSample(BaseModel):
    user_input: Optional[str]
    response: Optional[str]
    # No image, audio, video fields
```

Rating justification: Framework is exclusively text-based with no multi-modal evaluation capabilities. No metrics, schemas, or examples for image, audio, or video modalities.

### S4F5: Aggregate Statistics (2 points)
Evidence from repository:

1. Basic statistics via DataFrames - From experiment output:
```python
@experiment()
async def run_experiment(row):
    # Returns dict with results
    return {"score": score.value, ...}

# Results returned as DataFrame-like structure
# Can compute mean, std, etc. with pandas
```

2. Manual aggregation - `examples/ragas_examples/text2sql/evals.py`:
```python
# Calculate and display accuracy
accuracy_rate = sum(1 for r in results if r["execution_accuracy"] == "correct") / max(1, len(results))
```

3. Missing advanced stats:
   - No built-in significance testing (t-test, Wilcoxon)
   - No bootstrap confidence intervals
   - No permutation tests
   - No effect size computation
   - No ranking systems (Elo, TrueSkill)
   - No leaderboard generation

4. No comparison tools - Examples show manual comparison:
```python
# Users must manually compare across models
# No built-in pairwise comparison or statistical tests
```

Rating justification: Framework provides basic statistics through DataFrames (mean, median, std dev accessible via pandas). No built-in advanced statistical analysis, significance testing, or model comparison tools. Users must implement statistical comparisons manually. Deserves 2 points for basic statistics but lacks sophisticated comparison capabilities.

## Overall Assessment

Strengths:
- Excellent LLM-as-judge infrastructure (S4F3: 3/3)
- Good custom metric extensibility
- Per-sample scoring works well
- Strong rationale capture

Weaknesses:
- Minimal output validation (S4F1: 1/3)
- Limited traditional ML metrics (S4F2: 2/3)
- No multi-modal support (S4F4: 0/3)
- Basic statistics only, no advanced comparisons (S4F5: 2/3)

Total: 8/15 points

Ragas is purpose-built for LLM application evaluation with strong evaluator model support but lacks breadth in traditional metrics, validation utilities, multi-modal capabilities, and statistical comparison tools.