# Evidently - Stage 4 (EVALUATE) Evaluation

## Summary
Evidently is a comprehensive ML/LLM evaluation framework with strong data quality and drift detection capabilities, excellent metric coverage for traditional ML tasks, and emerging LLM evaluation features. The framework excels at computing metrics from per-sample to aggregate levels with robust statistical analysis, though some features like output validation and multi-modal scoring are still developing.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Evidence-based reasoning: The framework has basic validation capabilities but lacks comprehensive format validation and policy compliance. From the codebase structure, I can see data quality metrics (`src/evidently/metrics/`) that check for missing values, duplicates, and data quality issues, but no dedicated output format validators. The `examples/cookbook/metrics.ipynb` shows data quality checks like `DuplicatedRowCount`, `EmptyRowsCount`, `DatasetMissingValueCount` but these are dataset-level, not output validation-specific. The LLM features (`src/evidently/llm/`) exist but documentation doesn't show robust output schema validation or policy checking systems. Basic sanity checks exist through metrics but require manual setup. |
| S4F2: Metric Computation | 3 | Evidence-based reasoning: Excellent metric library with 100+ built-in metrics. From `examples/cookbook/metrics.ipynb`, the framework covers: Data Quality (`MinValue`, `MaxValue`, `MeanValue`, `MedianValue`, `StdValue`, `QuantileValue`, `CategoryCount`, `UniqueValueCount`, `MissingValueCount`, `InRangeValueCount`, `OutRangeValueCount`, `InListValueCount`, `OutListValueCount`), Classification (`F1Score`, `Accuracy`, `Precision`, `Recall`, `TPR`, `TNR`, `FPR`, `FNR`, `LogLoss`, `RocAuc`, `F1ByLabel`, `PrecisionByLabel`, `RecallByLabel`), Regression (`MeanError`, `MAE`, `MAPE`, `RMSE`, `R2Score`, `AbsMaxError`), Drift Detection (`DriftedColumnsCount`, `ValueDrift` with 20+ statistical tests), and RecSys metrics (`PrecisionTopK`, `RecallTopK`, `FBetaTopK`, `MAP`, `MRR`, `NDCG`, `HitRate`, `ScoreDistribution`). The `examples/cookbook/recsys_metrics.ipynb` confirms per-sample scoring with DataframeValue results. Custom metrics are straightforward via inheritance as shown in metrics.ipynb. |
| S4F3: Evaluator Models | 2 | Evidence-based reasoning: Basic LLM-as-judge support exists but limited evaluator ecosystem. From `src/evidently/descriptors/` and `examples/cookbook/prompt_optimization_*.ipynb`, the framework has `LLMEval` and `LLMJudge` descriptors with configurable templates (`BinaryClassificationPromptTemplate`, `MulticlassClassificationPromptTemplate`). The `PromptOptimizer` in prompt optimization examples shows judge capabilities with reasoning capture (`include_reasoning=True`). However, there's no evidence of specialized evaluator models like RAGAS or G-Eval integration. Ensemble scoring isn't shown in documentation. The guardrails (`src/evidently/guardrails/`) provide validation but aren't true evaluator models. Rationale capture exists through `include_reasoning` but no calibration mechanisms shown. |
| S4F4: Multi-Modal Scoring | 1 | Evidence-based reasoning: Primarily text-focused with minimal multi-modal support. The `DataDefinition` in examples shows `text_columns`, `numerical_columns`, `categorical_columns` but no image, audio, or video handling. The `src/evidently/llm/` directory focuses on text-based LLM evaluation. The `examples/cookbook/` examples only demonstrate text data analysis. No evidence of vision-language metrics (CIDEr, SPICE, CLIP score), audio-text metrics (WER), or video understanding capabilities. The framework handles tabular data well but lacks dedicated multi-modal artifact handling or cross-modal retrieval metrics. |
| S4F5: Aggregate Statistics | 3 | Evidence-based reasoning: Comprehensive statistical analysis and comparison features. From `examples/cookbook/metrics.ipynb`, the framework computes basic statistics (mean, median, std dev) via `MeanValue`, `MedianValue`, `StdValue`, `QuantileValue` metrics. The drift detection shows distribution analysis with 20+ statistical tests: `'anderson', 'chisquare', 'cramer_von_mises', 'ed', 'es', 'fisher_exact', 'g_test', 'hellinger', 'jensenshannon', 'kl_div', 'ks', 'mannw', 'empirical_mmd', 'psi', 't_test', 'perc_text_content_drift', 'abs_text_content_drift', 'TVD', 'wasserstein', 'z'`. Model comparison via reference datasets is core functionality: `report.run(current_dataset, reference_dataset)` pattern throughout examples. The `GroupBy` metric enables stratified statistics. Test framework (`evidently.tests`) with conditions (`lte, gte, lt, gt, eq, not_eq, Reference`) provides threshold-based comparisons. No explicit Elo/TrueSkill ranking systems, but strong statistical foundation. |

## Detailed Analysis

### S4F1: Output Validation and Normalization - Rating: 2

Strengths:
- Data quality metrics exist for dataset-level validation
- Basic sanity checks through metrics like `MissingValueCount`, `InRangeValueCount`, `OutRangeValueCount`
- Text content analysis for LLM outputs

Weaknesses:
- No dedicated format validators (JSON, XML schema validation)
- No policy compliance checks (harmful content, length constraints) as built-in features
- Limited output normalization capabilities beyond basic data cleaning
- No structured data extraction from free text shown in documentation

Evidence:
```python
# From examples/cookbook/metrics.ipynb - basic validation metrics
quality_report = Report([
    InListValueCount(column="Feedback", values=["Positive"]),
    OutListValueCount(column="Feedback", values=["Positive"]),
    InRangeValueCount(column="Predicted Probas", left=0.5, right=1.),
    OutRangeValueCount(column="Predicted Probas", left=0.5, right=1.)
])
```

### S4F2: Task-Specific Metric Computation - Rating: 3

Strengths:
- 100+ built-in metrics covering multiple domains
- Per-sample scoring with DataframeValue results
- Custom metric creation well-documented
- Efficient batch processing

Weaknesses:
- Some metrics require manual configuration
- LLM-specific metrics still developing

Evidence:
```python
# From examples/cookbook/metrics.ipynb - comprehensive metric coverage
data_report = Report([
    ColumnCount(), RowCount(), EmptyRowsCount(), EmptyColumnsCount(),
    DuplicatedRowCount(), DuplicatedColumnsCount(), DatasetMissingValueCount()
])

classification_report = Report([
    F1Score(), Accuracy(), Precision(), Recall(),
    TPR(), TNR(), FPR(), FNR(), LogLoss(), RocAuc()
])

regression_report = Report([
    MeanError(), MAE(), MAPE(), RMSE(), R2Score(), AbsMaxError()
])

# Custom metric example
class MyMaxMetric(SingleValueMetric):
    column: str
    def _default_tests(self, context: Context) -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]
```

### S4F3: Evaluator Model Integration - Rating: 2

Strengths:
- LLM-as-judge implementation with template system
- Configurable judging criteria via prompt templates
- Reasoning/explanation capture
- Prompt optimization framework

Weaknesses:
- No pre-built specialized evaluator models (RAGAS, G-Eval, Prometheus)
- No ensemble scoring or disagreement handling
- Limited calibration mechanisms

Evidence:
```python
# From examples/cookbook/prompt_optimization_code_review_example.ipynb
feedback_quality = BinaryClassificationPromptTemplate(
    pre_messages=[("system", "You are evaluating quality of code reviews")],
    criteria=criteria,
    target_category="bad",
    non_target_category="good",
    uncertainty="unknown",
    include_reasoning=True,
)

judge = LLMEval(
    alias="Code Review Judge",
    provider="openai",
    model="gpt-4o-mini",
    column_name="Generated review",
    template=feedback_quality
)

# Prompt optimization for judge improvement
optimizer = PromptOptimizer("code_review_example", strategy="feedback", verbose=True)
await optimizer.arun(executor=judge, scorer="accuracy", dataset=dataset, repetitions=5)
```

### S4F4: Multi-Modal Scoring Protocols - Rating: 1

Strengths:
- Strong text data analysis
- Tabular data support

Weaknesses:
- No vision-language metrics
- No audio-text capabilities
- No video understanding
- No cross-modal retrieval support

Evidence:
```python
# From examples/cookbook/metrics.ipynb - only text and tabular data
data_definition=DataDefinition(
    text_columns=["Question", "Answer"],
    numerical_columns=["Score", "Predicted Score"],
    categorical_columns=["Feedback", "Predicted Feedback"]
)
# No image_columns, audio_columns, video_columns, or cross-modal metrics
```

### S4F5: Aggregate Statistics and Cross-Model Comparison - Rating: 3

Strengths:
- Full statistical suite with basic and advanced statistics
- 20+ drift detection statistical tests
- Built-in reference comparison
- Stratified analysis via GroupBy
- Test framework with flexible conditions

Weaknesses:
- No explicit ranking systems (Elo, TrueSkill)
- No tournament-style comparisons shown

Evidence:
```python
# From examples/cookbook/metrics.ipynb - comprehensive statistics
quality_report = Report([
    MinValue(column="Rating"),
    MaxValue(column="Rating"),
    MeanValue(column="Rating"),
    MedianValue(column="Rating"),
    QuantileValue(column="Rating"),
    StdValue(column="Rating"),
])

# Statistical drift detection with 20+ tests
drift_report = Report([
    DriftedColumnsCount(cat_stattest="psi", num_stattest="wasserstein"),
    ValueDrift(column="Feedback", method="psi", threshold=0.05),
    ValueDrift(column="Rating", method="chisquare"),
])

# Reference comparison pattern
report.run(current_dataset, reference_dataset)

# Stratified analysis
groupby_report = Report(metrics=[
    GroupBy(UniqueValueCount(column="Rating"), "Feedback"),
])

# Test framework with conditions
from evidently.tests import lte, gte, lt, gt, eq, not_eq, Reference
# Tests can use Reference() for relative comparisons
```

## Key Observations

1. Strong Core Evaluation: Excellent metric computation for traditional ML tasks with per-sample scoring and comprehensive statistical analysis

2. Emerging LLM Features: LLM evaluation capabilities exist but are still developing, particularly around output validation and specialized evaluators

3. Limited Multi-Modal: Framework is primarily text and tabular data focused, lacking dedicated multi-modal evaluation capabilities

4. Excellent Extensibility: Custom metrics are straightforward to create, and the framework provides good building blocks for extending functionality

5. Robust Comparison: Strong reference dataset comparison and statistical testing make it excellent for monitoring and regression detection