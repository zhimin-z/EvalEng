## Evaluator Categories

[Algorithmic, ML-based, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Predefined statistical and mathematical metric classes
- File: `giskard/scanner/performance/metrics.py`
- Classes: `Accuracy`, `F1Score`, `Precision`, `Recall`, `AUC`, `MeanSquaredError`, `MeanAbsoluteError`, `BalancedAccuracy`, `Brier`
- Code Reference:
```python
# Examples of metric implementations:
# Accuracy uses sklearn.metrics.accuracy_score
# F1Score uses sklearn.metrics.f1_score
# Precision uses sklearn.metrics.precision_score
# Recall uses sklearn.metrics.recall_score
# AUC uses sklearn.metrics.roc_auc_score
# MeanSquaredError uses sklearn.metrics.mean_squared_error
# MeanAbsoluteError uses sklearn.metrics.mean_absolute_error
```
These are predefined statistical and mathematical metrics used to evaluate model outputs through algorithmic computation. The implementation demonstrates clear algorithmic evaluation by leveraging scikit-learn's deterministic metric functions. These metrics are reproducible and based on mathematical formulas for scoring model predictions against ground truth labels, making them purely algorithmic evaluators.

Evidence 2: Performance test function wrappers
- File: `giskard/testing/tests/performance.py`
- Functions: `test_f1()`, `test_auc()`, `test_precision()`, `test_recall()`, `test_accuracy()`, `test_rmse()`, `test_mse()`, `test_mae()`, `test_r2()`, `test_brier()`
- Code Reference:
```python
# Test functions wrapping algorithmic metrics
test_f1()
test_auc()
test_precision()
test_recall()
test_accuracy()
```
These test functions wrap the algorithmic metrics from the metrics module and apply them to evaluate model performance on datasets. They compute scores based on algorithmic rules, providing a structured interface for algorithmic evaluation. The deterministic nature of these functions confirms their classification as algorithmic evaluators.

Evidence 3: Statistical evaluation functions
- File: `giskard/testing/tests/statistic.py`
- Functions: `test_right_label()`, `test_output_in_range()`, `test_disparate_impact()`, `test_nominal_association()`, `test_theil_u()`
- Code Reference:
```python
test_right_label()
test_output_in_range()
test_disparate_impact()
test_nominal_association()
test_theil_u()
```
These are statistical evaluation functions that use mathematical formulas and rule-based logic to assess model behavior. They perform checks such as verifying if outputs fall within specified ranges or measuring statistical associations, demonstrating algorithmic evaluation through mathematical computation rather than learned or environmental feedback.

Evidence 4: Validation tests with expected metric values
- File: `tests/test_performance.py`
- Code Reference:
```python
# Test cases with expected algorithmic outputs
expected_metric=0.85
expected_metric=0.83
```
These test cases validate that algorithmic metrics produce expected numerical results with specific tolerance levels. The presence of predetermined expected values confirms the deterministic nature of the metrics, as algorithmic evaluators should consistently produce the same outputs for the same inputs.

---

### ML-based

Evidence 1: RAGAS metrics using LLM and embedding models as evaluators
- File: `giskard/rag/metrics/ragas_metrics.py`
- Class: `RagasMetric`
- Metrics: `ragas_context_precision`, `ragas_faithfulness`, `ragas_answer_relevancy`, `ragas_context_recall`
- Code Reference:
```python
# RagasLLMWrapper wrapping an LLM client for evaluation
self.llm_client.complete([ChatMessage(...)])

# RagasEmbeddingsWrapper wrapping an embedding model
self.embedding_model.embed(texts)

# Metrics initialization with ML models
if hasattr(self.metric, "llm"):
    self.metric.llm = self.ragas_llm
if hasattr(self.metric, "embeddings"):
    self.metric.embeddings = self.ragas_embeddings
```
These metrics use ML models (LLMs and embeddings) as evaluators, making them ML-based rather than algorithmic. The code explicitly shows LLM clients being used to complete evaluation prompts and embedding models being used to compute semantic similarity. The initialization code confirms that these metrics depend on trained neural network models to score RAG outputs, representing a clear example of ML-as-evaluator.

Evidence 2: LLM-as-judge for correctness evaluation
- File: `giskard/rag/evaluate.py`
- Class: `CorrectnessMetric`
- Code Reference:
```python
CorrectnessMetric(
    name="correctness",
    llm_client=llm_client,
    agent_description=agent_description
)
```
The evaluation function uses an LLM client as a judge to evaluate correctness, implementing the LLM-as-judge pattern. This represents ML-based evaluation where a language model provides judgments about output quality rather than using predefined algorithmic rules. The LLM client parameter indicates that the metric relies on a trained model's capabilities to assess correctness.

Evidence 3: LLM-based test case generation for evaluation
- File: `giskard/llm/testcase.py`
- Class: `TestcaseRequirementsGenerator`
- Code Reference:
```python
self.llm_client.complete(
    messages=messages,
    format="json_object",
    ...
)
```
This class uses an LLM client for evaluation-related generation, demonstrating ML-based evaluation support in the framework. While primarily focused on test case generation, it shows how the framework integrates ML models into the evaluation pipeline. The structured JSON output format and message-based interaction pattern indicate that the LLM is being used to generate evaluation criteria through learned capabilities rather than hardcoded rules.

---

### Environmental

Evidence 1: Model scanning with environmental execution
- File: `giskard/integrations/mlflow/giskard_evaluator.py`
- Class: `GiskardEvaluator`
- Function: `_perform_scan()`
- Code Reference:
```python
# Method that executes scans on models and datasets
setup_scan(giskard_model, giskard_dataset, self.evaluator_config)
```
This evaluator runs scans on models and datasets by executing model predictions in an evaluation environment and generating scan results. The `_perform_scan()` method orchestrates the execution of the model on test data and collects environmental feedback. This represents environmental evaluation where the execution context provides insights into model performance through actual runtime behavior rather than static metrics.

Evidence 2: Scan report aggregation from environmental execution
- File: `giskard/scanner/report.py`
- Class: `ScanReport`
- Functions: `generate_tests()`, `generate_test_suite()`
- Code Reference:
```python
# Methods that create tests based on environmental execution
generate_tests()
generate_test_suite()
```
The scan report aggregates results from executing models in an evaluation environment, synthesizing environmental feedback into actionable test suites. These methods create tests based on observed runtime behavior rather than predetermined criteria, demonstrating how environmental execution informs the evaluation process. The aggregation of execution results into reports shows environmental evaluation in action.

Evidence 3: Test execution result capture
- File: `giskard/core/test_result.py`
- Classes: `TestResult`, `TestResultDetails`
- Code Reference:
```python
# Result structure capturing environmental execution data
inputs      # Model input data
outputs     # Model predictions
results     # Test execution results
metadata    # Additional execution metadata
```
These classes capture comprehensive results from test execution in the evaluation environment, including model inputs, predictions, execution outcomes, and contextual metadata. This structured capture of runtime information represents environmental feedback, as the results depend on actual model execution rather than theoretical analysis. The inclusion of metadata indicates awareness of execution context.

Evidence 4: Test execution with environmental tracking
- File: `giskard/registry/giskard_test.py`
- Class: `GiskardTest`
- Function: `execute()`
- Code Reference:
```python
# Test execution with analytics tracking
analytics.track("test:execute", {"test_name": self.meta.full_name})
```
The `execute()` method runs tests in an execution environment and returns `TestResult` objects with full execution details. The analytics tracking confirms that tests are being executed in a real environment rather than simulated, capturing environmental feedback about model behavior. This demonstrates environmental evaluation through actual runtime execution.

Evidence 5: Suite execution validation tests
- File: `tests/test_suite.py`
- Code Reference:
```python
# Environmental execution and result validation
result = suite.run()
assert result.passed
_, test_result, _ = result.results[0]
assert not test_result.is_error
```
These tests demonstrate that the harness executes tests in an environment and collects pass/fail results and error information as environmental feedback. The verification of execution state (passed, is_error) confirms that evaluation depends on actual runtime behavior. This shows environmental evaluation where the execution environment provides concrete feedback about model behavior through real test execution.