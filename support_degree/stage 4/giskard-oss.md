# Giskard - Stage 4 (EVALUATE) Evaluation

## Summary
Giskard is a comprehensive testing framework for ML models (tabular to LLMs) with extensive metric computation capabilities. It provides robust validation, a rich metric library covering multiple modalities, evaluator model integration (especially for LLMs), and strong statistical aggregation features. The framework excels at automated vulnerability detection and test generation across different model types.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Basic validation exists but limited automation. In `giskard/core/validation.py` there are validation utilities, but no comprehensive schema validation or policy compliance checks are evident. The framework focuses more on post-hoc testing than real-time output validation. No explicit normalization pipeline for different output formats found in codebase. |
| S4F2: Metric Computation | 3 | Extensive metric library with 20+ metrics across domains. Evidence: `giskard/testing/tests/performance.py` contains `test_accuracy`, `test_precision`, `test_recall`, `test_f1`, `test_auc` for classification; `test_rmse`, `test_mae`, `test_r2` for regression. `giskard/rag/metrics/` contains RAG-specific metrics (correctness, coherency, etc.). Per-sample scoring supported via `ExampleExtractor` in `giskard/scanner/common/examples.py`. Custom metrics supported via decorator pattern in `giskard/registry/decorators.py`. |
| S4F3: Evaluator Models | 3 | Strong LLM-as-judge support with multiple evaluator types. Evidence: `giskard/llm/evaluators/` contains `base.py`, `correctness.py`, `coherency.py` for specialized evaluators. `giskard/llm/client/` supports OpenAI, Claude, Mistral clients. Ensemble scoring via RAGET in `giskard/rag/evaluate.py` which aggregates multiple evaluator results. Rationale capture visible in evaluator outputs with explanations. |
| S4F4: Multi-Modal Scoring | 2 | Limited multi-modal support beyond text. `docs/reference/notebooks/vision_landmark_detection.ipynb` and `vision_object_detection.ipynb` show some vision support, but the core framework in `giskard/models/base/` focuses primarily on text and tabular. No explicit CLIP score, CIDEr, or audio metrics found. The vision support appears more for wrapping models than comprehensive metric computation. |
| S4F5: Aggregate Statistics | 3 | Comprehensive statistical aggregation and comparison features. Evidence: `giskard/scanner/report.py` contains `ScanReport` class with statistical summaries. `giskard/core/test_result.py` shows test results with pass/fail metrics. MLflow integration in `docs/integrations/mlflow/` shows model comparison capabilities with significance testing mentioned. `giskard/scanner/issues.py` contains issue aggregation and ranking. W&B integration shows distribution analysis and leaderboard generation capabilities. |

## Detailed Analysis

### S4F1: Output Validation and Normalization
Rating: 2/3

Evidence:
- `giskard/core/validation.py` contains basic validation:
```python
def validate_model_and_dataset(model: BaseModel, dataset: Dataset, ...):
    # Basic compatibility checks
```
- No comprehensive format validation (JSON/XML schema) found
- No policy compliance checks in core framework
- Limited normalization features; mostly data type casting in `giskard/datasets/base/__init__.py`:
```python
def _cast_column_to_dtypes(self, df, column_dtypes):
    # Basic type casting
```

Missing:
- Structured output validators for LLM responses
- Malformed output detection
- Policy violation checks (harmful content) as a validation layer
- Standardization of different output formats

Present:
- Basic dataset validation and type checking
- Model-dataset compatibility validation
- Some sanity checks in test execution

### S4F2: Task-Specific Metric Computation
Rating: 3/3

Evidence:
1. Coverage - Extensive metric library:
```python
# From giskard/testing/tests/performance.py
@test()
def test_accuracy(model: BaseModel, dataset: Dataset, threshold: float = 1.0):
    """Test if model accuracy is above threshold"""

@test()
def test_f1(model: BaseModel, dataset: Dataset, threshold: float = 1.0):
    """Test if model F1 score is above threshold"""
```

2. RAG-specific metrics in `giskard/rag/metrics/`:
   - Correctness, coherency, groundedness
   - RAGAS integration shown in docs

3. Per-sample scoring:
```python
# From giskard/scanner/common/examples.py
class ExampleExtractor:
    def get_examples_dataframe(self, n=3, with_prediction=True):
        # Returns per-sample predictions
```

4. Extensibility:
```python
# From giskard/registry/decorators.py
@test(name="My Custom Test", tags=["custom"])
def my_test(model, dataset):
    # Custom test definition
```

Strengths:
- 20+ built-in metrics across classification, regression, RAG
- Standard implementations (sklearn-based)
- Per-sample and batch support
- Strong extensibility via decorator pattern

### S4F3: Evaluator Model Integration
Rating: 3/3

Evidence:
1. LLM-as-Judge infrastructure:
```python
# From giskard/llm/evaluators/base.py
class BaseEvaluator:
    def evaluate(self, inputs, outputs):
        # Evaluator interface
```

2. Multiple evaluator types in `giskard/llm/evaluators/`:
   - `correctness.py` - Answer correctness evaluation
   - `coherency.py` - Response coherency
   - `groundedness.py` - Factual grounding

3. RAGET ensemble scoring:
```python
# From giskard/rag/evaluate.py
def evaluate(testset, model, knowledge_base=None):
    # Aggregates multiple evaluator results
```

4. Rationale capture:
```python
# Evaluators return detailed explanations
result = evaluator.evaluate(...)
result.explanation  # Contains reasoning
```

5. Client support in `giskard/llm/client/`:
   - OpenAI, Anthropic, Mistral
   - Custom client support

Strengths:
- Multiple specialized evaluators
- Ensemble aggregation
- Rationale/explanation capture
- Flexible client integration

### S4F4: Multi-Modal Scoring Protocols
Rating: 2/3

Evidence:
1. Vision support exists but limited:
   - `docs/reference/notebooks/vision_landmark_detection.ipynb`
   - `docs/reference/notebooks/vision_object_detection.ipynb`

2. Model wrapping in `giskard/models/base/`:
```python
# Model types supported
model_type: Literal["classification", "regression", "text_generation"]
```
- No explicit "vision" or "audio" model types

3. No specialized multi-modal metrics:
   - No CLIP score implementation found
   - No CIDEr, SPICE for image captioning
   - No WER for speech
   - No video temporal consistency metrics

Present:
- Text-heavy focus (classification, regression, text generation)
- Some vision model wrapping capability
- Cross-modal support appears minimal

Missing:
- Dedicated multi-modal metric implementations
- Audio-text metrics
- Video understanding metrics
- Standard multi-modal evaluation protocols

### S4F5: Aggregate Statistics and Cross-Model Comparison
Rating: 3/3

Evidence:
1. Statistical aggregation in `giskard/scanner/report.py`:
```python
class ScanReport:
    def get_issue_summary(self):
        # Aggregates issues by type, severity
```

2. MLflow integration for comparison:
```python
# From docs/integrations/mlflow/mlflow-llm-example.ipynb
with mlflow.start_run(run_name=model_name):
    mlflow.evaluate(model=models[model_name], 
                   evaluators="giskard")
# Enables cross-model comparison in MLflow UI
```

3. W&B integration shows distribution analysis:
```python
# From docs/integrations/wandb/wandb-tabular-example.ipynb
scan_results.to_wandb()
test_suite.run().to_wandb()
# Logs distributions, histograms, metrics
```

4. Test suite results in `giskard/core/test_result.py`:
```python
class TestResult:
    metric: float
    passed: bool
    # Statistical information per test
```

5. Ranking and comparison:
   - Issue severity ranking in scanner
   - Test suite pass/fail aggregation
   - Cross-run comparison via integrations

Strengths:
- Comprehensive statistical summaries
- Integration with MLflow for significance testing
- Distribution analysis via W&B
- Issue ranking by severity
- Test suite aggregation

Minor gaps:
- No explicit bootstrap CI implementation found in core
- Permutation tests not evident
- Elo/TrueSkill ranking not present (but not critical)

## Overall Assessment

Total Score: 13/15

### Strengths:
1. Excellent metric library with 20+ metrics and strong extensibility
2. Best-in-class LLM evaluation with multiple evaluators, ensemble scoring, and rationale capture
3. Strong statistical aggregation with excellent integration ecosystem (MLflow, W&B)
4. Per-sample and aggregate scoring well-supported
5. Good extensibility via decorator pattern for custom metrics

### Weaknesses:
1. Limited output validation - no comprehensive schema/policy checking layer
2. Multi-modal support is basic - primarily text/tabular focused
3. No explicit audio/video metrics - limited to vision with basic support

### Recommendations:
1. Add structured output validators for LLM responses (JSON schema validation)
2. Expand multi-modal metrics (CLIP, CIDEr, WER)
3. Add explicit policy compliance checks as validation layer
4. Consider adding bootstrap confidence intervals to core framework

### Positioning:
Giskard is a strong evaluation framework particularly for LLMs and tabular models, with excellent metric computation and aggregation capabilities. It's more focused on post-hoc testing and vulnerability detection than real-time validation, which is appropriate for its use case as a testing framework rather than a production monitoring tool.