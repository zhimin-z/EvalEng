## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Core evaluation logic with static comparison
- File: `beir/retrieval/evaluation.py`
- Class/Function: `EvaluateRetrieval.evaluate()`
- Code Reference:
```python
@staticmethod
def evaluate(
    qrels: dict[str, dict[str, int]],
    results: dict[str, dict[str, float]],
    k_values: list[int],
    ignore_identical_ids: bool = True,
) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]]:
```
This method performs direct comparison and scoring of retrieval results against reference judgments using metrics like NDCG, MAP, Recall, and Precision. The evaluation harness evaluates information retrieval systems by comparing retrieved document rankings against ground truth relevance judgments (qrels) without executing any model-generated code or engaging in multi-step interactions. This represents examination of retrieval model outputs (ranked document lists) through similarity scoring and statistical metric computation.

Evidence 2: Custom metric functions for static analysis
- File: `beir/retrieval/custom_metrics.py`
- Functions: `mrr()`, `recall_cap()`, `hole()`, `top_k_accuracy()`
- Code Reference:
```python
# Functions include:
# - mrr() - Computes Mean Reciprocal Rank by analyzing ranking positions
# - recall_cap() - Calculates capped recall scores
# - hole() - Identifies documents not in annotated corpus
# - top_k_accuracy() - Measures top-k accuracy
```
All these functions perform statistical analysis and scoring of retrieved results without any execution. They focus on pattern matching to identify relevant documents in rankings and computing information retrieval metrics through direct analysis of output structure, rather than executing model-generated code or running simulations.

Evidence 3: PyTrec evaluation integration
- File: `beir/retrieval/evaluation.py`
- Code Reference:
```python
evaluator = pytrec_eval.RelevanceEvaluator(qrels, {map_string, ndcg_string, recall_string, precision_string})
scores = evaluator.evaluate(results)
```
The harness uses the `pytrec_eval` library to compute standard IR metrics through direct comparison of results and qrels. This demonstrates the static analysis approach where pre-computed retrieval results are analyzed against ground truth judgments without any dynamic execution or interactive simulation components.

Evidence 4: Example evaluation workflow
- File: `examples/retrieval/evaluation/dense/evaluate_sbert.py`
- Code Reference:
```python
#### Retrieve dense results (format of results is identical to qrels)
results = retriever.retrieve(corpus, queries)

#### Evaluate your retrieval using NDCG@k, MAP@K ...
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
```
The evaluation flow follows a clear static analysis pattern: (1) Retrieve ranked documents to produce output, (2) Compare output rankings against ground truth, (3) Calculate metrics through direct analysis. This workflow confirms the harness operates through static comparison and metric computation rather than executing generated artifacts, running multi-step interactions, or analyzing the harness codebase itself with tools like linters. The harness evaluates the quality of information retrieval through static comparison, making it a clear example of the Static Analysis category for benchmark task evaluation.