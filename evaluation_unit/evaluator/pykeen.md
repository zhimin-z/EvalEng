## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Rank-based evaluation metrics implementation
- File: `pykeen/evaluation/rank_based_evaluator.py` (implied from docs/source/reference/evaluation.rst)
- File: `pykeen/metrics/ranking.py` (implied from docs/source/reference/metrics.rst)
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference:
```python
# From tests/test_models.py
results.metric_results.get_metric("mr")
```
This repository implements a knowledge graph embedding evaluation harness that uses algorithmic rank-based metrics. For link prediction tasks, the system scores all candidate entities and ranks them, then calculates deterministic metrics including Mean Rank (MR), Hits@K (measuring if correct answer is in top-K), and Mean Reciprocal Rank (MRR). As documented: "Based on these individual ranks, which are obtained for each evaluation triple and each side of the prediction (left/right), there exist several aggregation measures to quantify the performance of a model in a single number."

Evidence 2: Deterministic metric assertions in test suite
- File: `tests/test_pipeline.py`
- Code Reference:
```python
# Line 467-471
assert results.metric_results.get_metric("mr") == 2, "The rank should equal 2"

# Line 486-487
assert results.metric_results.get_metric("mr") == 1, "The rank should equal 1"
```
The test files confirm the use of predefined, deterministic algorithmic metrics by checking specific metric values with exact assertions. These tests demonstrate that the evaluation produces reproducible, deterministic results that can be validated against expected values, which is characteristic of algorithmic evaluation approaches.

Evidence 3: Filtered evaluation and ranking variations
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Documentation describes filtered evaluation settings (Bordes et al. 2013) and multiple ranking types
The system implements filtering logic that removes known true triples from ranking, which is a rule-based algorithmic approach. The documentation describes optimistic, pessimistic, realistic, and non-deterministic ranking calculations—all algorithmic variations on how to handle ties in scores. This demonstrates the use of mathematical formulas and predefined computational rules to ensure consistent, reproducible evaluation through established computational measures.