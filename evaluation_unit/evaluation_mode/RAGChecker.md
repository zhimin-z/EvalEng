## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Claim extraction and checking
- File: `ragchecker/evaluator.py`
- Class/Function: `RAGChecker.extract_claims()` and `RAGChecker.check_claims()`
- Code Reference:
```python
def extract_claims(self, results: List[RAGResult], extract_type="gt_answer"):
    """
    Extract claims from the response and ground truth answer.
    """
    # Extracts claims from text using LLM as extractor
    extraction_results = self.extractor.extract(
        batch_responses=texts,
        batch_questions=questions,
        max_new_tokens=self.extractor_max_new_tokens,
        ...
    )
    claims = [[c.content for c in res.claims] for res in extraction_results]
```

```python
def check_claims(self, results: RAGResults, check_type="answer2response"):
    """
    Check the claims extracted from the response and ground truth answer.
    """
    # Performs entailment checking between claims and references
    checking_results = self.checker.check(
        batch_claims=claims,
        batch_references=references,
        batch_questions=[ret.query for ret in results],
        ...
    )
```
The evaluation harness extracts claims from RAG system responses and ground truth answers, then performs entailment checking to verify if claims are factually supported. This is purely text comparison and structural validation without executing any generated code or artifacts.

Evidence 2: Metric computation through boolean operations
- File: `ragchecker/computation.py`
- Function: `to_bool()`, `evaluate_precision()`, `evaluate_retrieval()`
- Code Reference:
```python
def to_bool(checking_results):
    if isinstance(checking_results, str):
        return checking_results == "Entailment"
    return np.array([to_bool(res) for res in checking_results])

def evaluate_precision(result: RAGResult):
    assert result.answer2response is not None
    answer2response = to_bool(result.answer2response)
    if len(answer2response) > 0:
        result.metrics[metrics.precision] = np.mean(answer2response)
```

```python
def evaluate_retrieval(result: RAGResult):
    assert result.retrieved2answer is not None
    retrieved2answer = to_bool(result.retrieved2answer)
    if len(retrieved2answer) > 0 and len(retrieved2answer[0]) > 0:
        claim_recalled = np.max(retrieved2answer, axis=1)
        result.metrics[metrics.claim_recall] = np.mean(claim_recalled)
        psg_useful = np.max(retrieved2answer, axis=0)
        result.metrics[metrics.context_precision] = np.mean(psg_useful)
```
The computation module performs statistical analysis on entailment results (converting to boolean values and computing means, maxes, etc.) to calculate various metrics. This is pattern matching and mathematical operations on model outputs, not execution of generated artifacts.

Evidence 3: Metric definitions and dependencies
- File: `ragchecker/metrics.py`
- Code Reference:
```python
METRIC_REQUIREMENTS = {
    # overall metrics
    precision: ["answer2response"],
    recall: ["response2answer"],
    f1: ["answer2response", "response2answer"],
    # retriever metrics
    claim_recall: ["retrieved2answer"],
    context_precision: ["retrieved2answer"],
    # generator metrics
    context_utilization: ["retrieved2answer", "response2answer"],
    noise_sensitivity_in_relevant: ["retrieved2response", "answer2response", "retrieved2answer"],
    # ...
}
```
The metrics are based on different types of textual entailment checks between RAG components (response, answer, retrieved context). These represent structural relationships validated through text comparison, not execution.

Evidence 4: Data structures for textual evaluation
- File: `ragchecker/container.py`
- Class: `RAGResult`
- Code Reference:
```python
@dataclass
class RAGResult:
    query_id: str
    query: str
    gt_answer: str
    response: str
    retrieved_context: List[RetrievedDoc] | None = None
    response_claims: List[List[str]] | None = None
    gt_answer_claims: List[List[str]] | None = None
    answer2response: List[str] | None = None  # entailment results
    response2answer: List[str] | None = None  # entailment results
    retrieved2response: List[List[str]] | None = None  # entailment results
    retrieved2answer: List[List[str]] | None = None  # entailment results
    metrics: dict[str, float] = field(default_factory=dict)
```
The data structures store text-based claims and entailment results as strings. The evaluation operates on these textual representations through comparison and validation, confirming the static analysis approach.

Evidence 5: Correlation analysis for meta-evaluation
- File: `data/meta_evaluation/meta_eval.py`
- Function: `correlation()`
- Code Reference:
```python
def correlation(a, b):
    pearson = round(stats.pearsonr(a, b)[0] * 100, 2)
    spearman = round(stats.spearmanr(a, b)[0] * 100, 2)
    return pearson, spearman

# Comparing different evaluation metrics
x = np.array(list(baseline_data.values()))
eval_result[baseline][metric] = correlation(x, human_label)
```
The meta-evaluation compares RAGChecker's outputs with human judgments and other baselines using statistical correlation measures. This is similarity scoring between outputs and references, a form of static analysis.