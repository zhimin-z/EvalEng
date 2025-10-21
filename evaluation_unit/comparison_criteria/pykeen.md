## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Rank-Based Evaluation Protocol
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference: Link prediction evaluation description
```rst
In the rank-based evaluation protocol, the scores are used to sort the list of possible choices by decreasing score,
and determine the *rank* of the true choice, i.e. the index in the sorted list.
```
The evaluation harness compares model predictions against ground truth triples in test/validation sets. Models predict missing entities in triples, and their predictions are ranked against the true correct entity.

Evidence 2: Pipeline Test Triple Evaluation
- File: `tests/test_pipeline.py`
- Code Reference: Pipeline evaluation with test triples
```python
results = pipeline(
    training=self.training,
    testing=self.testing,
    validation=self.validation,
    model="TransE",
    training_kwargs=dict(num_epochs=1, use_tqdm=False),
    evaluation_kwargs=dict(use_tqdm=False),
)
```
Test triples serve as explicit labels for evaluation. The pipeline uses predetermined test sets containing ground truth triples for assessing model predictions on knowledge graph completion.

Evidence 3: Explicit Test Triple Creation
- File: `tests/test_model_mode.py`
- Code Reference: Test triple specification
```python
# The test triples are created to yield the third highest score on both head and tail prediction
cls.dataset.testing.mapped_triples = torch.tensor([[max_score - 2, 0, max_score - 2]])
```
Test triples are explicitly created with known correct answers. These predetermined triples serve as ground truth labels for evaluating model predictions.

Evidence 4: Entity Prediction Evaluation
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference: Known triple filtering
```rst
During evaluation time, we now evaluate head and tail prediction, i.e., whether we can predict the correct
head/tail entity from the remainder of a triple. The first triple in the test split of this dataset is
`['belgium', 'locatedin', 'europe']`. Thus, for tail prediction, we aim to answer `['belgium', 'locatedin', ?]`.
```
Evaluation compares model-predicted entities against explicit ground truth triples. The correct answer (e.g., 'europe') is the predetermined label used to compute ranking metrics for knowledge graph completion tasks.

---

### None

Evidence 1: Rank Aggregation Metrics
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference: Ranking metric aggregation
```rst
Given the set of individual rank scores for each head/tail entity from evaluation triples, there are various
aggregation metrics which summarize different aspects of the set of ranks into a single-figure number.
```
Computes intrinsic quality metrics from ranking positions without requiring external references beyond test triples. These self-contained aggregation metrics assess model performance through internal ranking properties.

Evidence 2: Mean Rank Computation
- File: `tests/test_pipeline.py`
- Code Reference: Metric result extraction
```python
assert results.metric_results.get_metric("mr") == 2, "The rank should equal 2"
```
Metrics like Mean Rank (MR), Mean Reciprocal Rank (MRR), and Hits@K are computed purely from ranking positions. These intrinsic measures assess quality without additional references beyond the test triples themselves.

Evidence 3: Ranking Type Variations
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference: Ranking type definitions
```rst
Ranking Types
~~~~~~~~~~~~~
* The *optimistic* rank assumes that the true choice is on the first position of all those with equal score.
* The *pessimistic* rank assumes that the true choice is on the last position of all those with equal score.
* The *realistic* rank is the mean of the optimistic and the pessimistic rank
```
Various rank-based aggregation metrics are computed as intrinsic quality measures from model scores and rankings. These metrics assess model performance based solely on ranking positions without requiring external baselines, additional corpora, or comparison to other systems.