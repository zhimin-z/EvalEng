## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Core Evaluation Function
- File: `ranx/meta/evaluate.py`
- Code Reference: `evaluate()` function (Lines 63-106)
```python
def evaluate(
    qrels: Union[Qrels, Dict[str, Dict[str, Number]], ...],
    run: Union[Run, Dict[str, Dict[str, Number]], ...],
    metrics: Union[List[str], str],
    ...
)
```
The `evaluate()` function takes `qrels` (query relevance labels) and `run` (model outputs) as parameters. The evaluation process compares runs against ground truth qrels, establishing explicit labels as the primary comparison criterion.

Evidence 2: Qrels Data Structure
- File: `ranx/data_structures/qrels.py`
- Code Reference: Qrels structure (Referenced in `tests/unit/ranx/data_structures/qrels_test.py`)
```python
qrels_dict = {
    "q1": {"d1": 1, "d2": 2, "d3": 3},
    "q2": {"d1": 1, "d2": 2},
}
```
Stores gold standard relevance judgments for queries with structure `{"query_id": {"doc_id": relevance_score}}`. These predetermined relevance scores serve as explicit ground truth labels for evaluation.

Evidence 3: Run Data Structure
- File: `ranx/data_structures/run.py`
- Code Reference: Run structure (Referenced in `tests/unit/ranx/data_structures/run_test.py`)
```python
run_dict = {
    "q1": {"d1": 0.1, "d2": 0.2, "d3": 0.3},
    "q2": {"d1": 0.1, "d2": 0.2},
}
```
Stores model predictions/outputs to be evaluated. These runs are compared against qrels for metric computation, demonstrating the explicit label comparison pattern.

Evidence 4: Explicit Comparison Pattern
- File: `tests/unit/ranx/meta/evaluate_test.py`
- Code Reference: `test_hits_single()` (Lines 8-16)
```python
def test_hits_single():
    y_true = np.array([[[1, 1], [4, 1], [5, 1], [6, 1]]])  # Ground truth
    y_pred = np.array([[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [7, 1]]])  # Predictions
    k = 5
    assert evaluate(y_true, y_pred, f"hits@{k}") == 3
```
Demonstrates ground truth labels (y_true/qrels) versus predictions (y_pred/run) comparison pattern. The evaluation directly compares model outputs against predetermined correct relevance judgments.

Evidence 5: Metric Implementations
- File: `ranx/metrics/` directory
- Code Reference: Various metric implementations (Referenced in `tests/unit/ranx/metrics/bpref_test.py`)
```python
qrels_dict = {
    "q1": {"d2": 1, "d5": 1, "d1": 0, "d4": 0},  # Explicit relevance labels
    "q2": {"d2": 1, "d5": 1, "d1": 0, "d6": 0},
}
```
Contains implementations for various IR metrics (precision, recall, MAP, NDCG, etc.). All metrics require qrels with explicit relevance labels for computation, demonstrating systematic use of ground truth annotations.

Evidence 6: Metric Documentation
- File: `docs/metrics.md`
- Code Reference: Metric definitions (Lines 23-59)
```
"Precision is the proportion of the retrieved documents that are relevant"
```
Documents metrics like Precision, Recall, F1, MAP, NDCG that compare model outputs against explicit relevance labels. All documented metrics require predetermined ground truth for evaluation.

Evidence 7: Multi-Run Comparison
- File: `ranx/meta/compare.py`
- Code Reference: `compare()` function (Lines 21-48)
```python
def compare(
    qrels: Qrels,
    runs: List[Run],
    metrics: Union[List[str], str],
    ...
) -> Report:
```
The `compare()` function evaluates multiple runs against qrels. All comparisons require explicit qrels as ground truth, reinforcing the framework's reliance on predetermined relevance labels for assessment.