## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: RAG Question Samples
- File: `giskard/rag/testset.py`
- Code Reference: `QuestionSample` class and `QATestset` class
```
@dataclass
class QuestionSample:
    id: str
    question: str
    reference_answer: str  # This is the explicit label/ground truth
    reference_context: str
    conversation_history: Sequence[Dict[str, str]]
    metadata: Dict[str, Any]
```
The `QuestionSample` dataclass stores reference answers that serve as ground truth for RAG evaluation tasks. These are static, predetermined correct answers stored in test sets that models are evaluated against.

Evidence 2: Evaluation Against Reference Answers
- File: `giskard/rag/evaluate.py`
- Code Reference: `evaluate()` function
```
for sample, answer in maybe_tqdm(...):
    metrics_results[sample["id"]].update(metric(sample, answer))
```
The evaluation compares model outputs against reference answers loaded from datasets. Each sample contains a reference answer that serves as the comparison target for assessing model response quality.

Evidence 3: RAGAS Metric Ground Truth
- File: `giskard/rag/metrics/ragas_metrics.py`
- Code Reference: `prepare_ragas_sample()` method
```
return {
    "user_input": question_sample["question"],
    "response": answer.message,
    "retrieved_contexts": answer.documents,
    "reference": question_sample["reference_answer"],  # Ground truth label
}
```
Reference answers are explicitly used as ground truth labels in RAGAS metric preparation. The reference field provides the comparison standard for evaluating generated responses against predetermined correct answers.

---

### Behavioral Specification

Evidence 1: Classification Score Metrics
- File: `giskard/scanner/performance/metrics.py`
- Code Reference: `F1Score` class in `PerformanceMetric` classes
```
class F1Score(SklearnClassificationScoreMixin, ClassificationPerformanceMetric):
    name = "F1 Score"
    greater_is_better = True
    
    def __call__(self, model: BaseModel, dataset: Dataset) -> MetricResult:
        # Executable specification that validates model performance
        y_true = np.asarray(dataset.df[dataset.target])
        y_pred = np.asarray(model.predict(dataset).prediction)
        value = self._calculate_metric(y_true, y_pred, model)
```
Implements dynamic validation mechanisms that define acceptable system behavior for evaluation tasks. These metrics execute against model outputs to verify functional correctness through performance specifications.

Evidence 2: RAGAS Metric Wrappers
- File: `giskard/rag/metrics/ragas_metrics.py`
- Code Reference: RAGAS metric wrappers
RAGAS metric wrappers provide behavioral specifications for RAG evaluation, defining executable validation criteria for retrieval and generation quality. These wrappers implement functional requirements that model outputs must satisfy.

---

### None

Evidence 1: Intrinsic Quality Metrics
- File: `giskard/core/test_result.py`
- Code Reference: `TestResult` class
```
@dataclass
class TestResult:
    passed: bool = False
    metric: Optional[float] = None  # Intrinsic quality measure
    # No reference to external ground truth needed
```
Test results include intrinsic quality measures that assess model properties without comparison to external standards. These metrics provide reference-free evaluation of model behavior.

Evidence 2: Metric Tool Assessment
- File: `giskard/llm/talk/tools/metric.py`
- Code Reference: `MetricTool` class
The metric tool provides reference-free assessment capabilities, computing intrinsic quality measures of model outputs without requiring external ground truth or baseline comparisons.