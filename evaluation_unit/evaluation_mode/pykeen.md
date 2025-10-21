## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Core evaluation loop architecture
- File: `pykeen/evaluation/evaluation_loop.py`
- Class/Function: `LCWAEvaluationLoop`
- Code Reference:
```python
evaluation_loop = LCWAEvaluationLoop(
    model=model,
    triples_factory=dataset.testing,
)
results = evaluation_loop.evaluate()
```
The evaluation process computes scores for triples and compares them without executing generated code. The framework evaluates knowledge graph embedding models by computing scores for triples and analyzing these scores through ranking metrics, with no execution of model-generated code, scripts, or programs.

Evidence 2: Rank-based evaluation metrics
- File: `pykeen/evaluation/rank_based_evaluator.py`
- Class/Function: `RankBasedEvaluator`
- Code Reference:
```rst
Evaluation
==========

.. automodapi:: pykeen.evaluation
```
Evaluates model predictions by computing ranking metrics (MR, MRR, Hits@K) through direct score comparison. The core evaluation mechanism involves computing scores for candidate triples using the embedding model, sorting scores to determine rankings, calculating ranking-based metrics, and filtering known triples from evaluation sets.

Evidence 3: Ranking metrics computation
- File: `pykeen/metrics/ranking.py`
- Code Reference:
```rst
Metrics
=======

.. automodapi:: pykeen.metrics
    :no-heading:
    :inherited-members:
    :headings: --

.. automodapi:: pykeen.metrics.ranking
```
Computes metrics like Mean Rank (MR), Mean Reciprocal Rank (MRR), Hits@K by analyzing scores. The evaluation involves format validation of triples, structural checks on tensor dimensions, score comparison and ranking computation, and pattern matching for relation types and entity restrictions.

Evidence 4: Link prediction evaluation protocol
- File: `docs/source/tutorial/understanding_evaluation.rst`
- Code Reference:
```rst
Understanding the Evaluation
============================
This part of the tutorial is aimed to help you understand the evaluation of knowledge graph embeddings.
In particular it explains rank-based evaluation metrics reported in :class:`pykeen.evaluation.RankBasedMetricResults`.

Knowledge graph embedding are usually evaluated on the task of link prediction. To this end, an evaluation set of
triples is provided, and for each triple, two tasks are solved:

* Right-Side In the *right-side* prediction task, a pair of head entity and relation are given and aim to predict
  the tail, i.e. (h, r, ?). To this end, the knowledge graph embedding model is used to *score* each of the
  possible choices (h, r, e) for e ∈ E. Higher scores indicate higher plausibility.
* Left-Side Analogously, in the *left-side* prediction task, a pair of relation and tail entity are provided and
  aim to predict the head, i.e. (?, r, t). Again, each possible choice (e, r, t) for e ∈ E is scored according to 
  the knowledge graph embedding model.
```
All evaluation is centered on the link prediction task for knowledge graph embeddings: head prediction (?, r, t), tail prediction (h, r, ?), and relation prediction (h, ?, t). There are no multi-step feedback loops or state evolution; evaluation is a single-pass process where scores are computed once and then analyzed.

Evidence 5: Triple filtering during evaluation
- File: `tests/test_pipeline.py`
- Class/Function: `TestPipelineEvaluationFiltering.test_pipeline_evaluation_filtering_without_validation_triples()`
- Code Reference:
```python
class TestPipelineEvaluationFiltering(unittest.TestCase):
    """Test filtering of triples during evaluation using the pipeline."""
    
    def test_pipeline_evaluation_filtering_without_validation_triples(self):
        """Test if the evaluator's triple filtering works as expected using the pipeline."""
        results = pipeline(
            model=self.model,
            dataset=self.dataset,
            evaluator_kwargs=dict(filtered=True),
            evaluation_kwargs=dict(use_tqdm=False),
        )
        assert results.metric_results.get_metric("mr") == 2
```
The evaluation follows a standard static pattern: load test triples, compute scores for all candidate completions, rank candidates by scores, calculate metrics from rankings, and report aggregated results. The harness is purely focused on analyzing the numerical outputs of knowledge graph embedding models through direct inspection and mathematical operations, without any execution of generated artifacts or interactive processes.