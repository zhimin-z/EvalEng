# beir-cellar__beir - Stage 4 (EVALUATE) Evaluation

## Summary
BEIR is a benchmark repository focused on information retrieval evaluation, providing comprehensive retrieval evaluation capabilities with multiple metrics (NDCG, MAP, Recall, Precision, MRR). The framework computes per-sample and aggregate statistics for retrieval tasks, but lacks validation features, evaluator model integration, and multi-modal scoring beyond text retrieval.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation infrastructure found. The codebase focuses entirely on retrieval evaluation without any output validation, format checking, or policy compliance features. Files like `beir/retrieval/evaluation.py` compute metrics directly on results without validating format or content. No schema validation, sanity checks, or normalization utilities exist. |
| S4F2: Metric Computation | 3 | Excellent retrieval metric library. The framework provides comprehensive retrieval metrics including NDCG@k, MAP@k, Recall@k, Precision@k, MRR (in `beir/retrieval/evaluation.py` lines showing `evaluate()` and `evaluate_custom()` methods). Custom metrics are supported via `custom_metrics.py` including hole@k, recall_cap@k, and top_k_accuracy. Per-sample scoring is available through the results dictionary format `{query_id: {doc_id: score}}`. All metrics use standard information retrieval formulations. Example from README: "Evaluate your retrieval using NDCG@k, MAP@K, Recall@K and Precision@K where k = [1,3,5,10,100,1000]". |
| S4F3: Evaluator Models | 0 | No LLM-as-judge or evaluator model integration. The repository is purely focused on metric-based evaluation for retrieval. There are no judge prompts, specialized evaluator models, or ensemble scoring mechanisms. Reranking examples exist (e.g., `examples/retrieval/evaluation/reranking/evaluate_bm25_ce_reranking.py`) but these are for re-scoring retrieved documents, not for evaluation. No rationale capture or calibration mechanisms present. |
| S4F4: Multi-Modal Scoring | 0 | Text-only retrieval framework. All examples and evaluation code focus exclusively on text retrieval (corpus with "title" and "text" fields). No vision-language metrics, audio-text evaluation, or video understanding capabilities. The data loader in `beir/datasets/data_loader.py` only handles text corpus and queries in JSON format. No cross-modal retrieval support exists. |
| S4F5: Aggregate Statistics | 2 | Basic statistics with limited comparison features. The framework computes mean scores across queries (evident in `evaluate()` method returning aggregate NDCG, MAP, etc.). The `evaluate_custom()` method supports MRR, recall_cap, hole, and top_k_accuracy metrics. Results can be saved via `util.save_results()` and `util.save_runfile()` for reranking. However, there's no built-in statistical significance testing, confidence intervals, distribution analysis, or ranking systems like Elo. The evaluation is limited to averaging per-query scores without advanced statistical comparisons. Example from `examples/retrieval/evaluation/custom/evaluate_custom_metrics.py` shows basic aggregation but no significance tests. |

## Strengths
- Comprehensive retrieval metrics: Extensive coverage of standard IR metrics (NDCG, MAP, Recall, Precision, MRR) with custom metric support
- Per-sample granularity: Results format enables per-query-document score analysis
- Extensible architecture: Custom metrics can be added via `evaluate_custom()` method
- Multiple retrieval paradigms: Supports dense, sparse, and lexical retrieval evaluation

## Weaknesses
- No output validation: Missing format validation, schema checks, or normalization
- No evaluator models: No LLM-as-judge or specialized evaluation models
- Text-only: No multi-modal evaluation capabilities
- Limited statistical analysis: No significance testing, confidence intervals, or advanced comparison tools
- No distribution analysis: Missing outlier detection, histogram generation, or reliability metrics

## Evidence for Ratings

### S4F2 Evidence (3 points):
From `beir/retrieval/evaluation.py`:
```python
def evaluate(self, qrels: dict[str, dict[str, int]], 
             results: dict[str, dict[str, float]], 
             k_values: list[int]) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]]:
```

From README.md:
```python
#### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
```

### S4F5 Evidence (2 points):
From `examples/retrieval/evaluation/custom/evaluate_custom_metrics.py`:
```python
#### Evaluate your retreival using MRR@K, Recall_cap@K, Hole@K
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
recall_cap = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="recall_cap")
hole = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="hole")
```

The metrics are aggregated but without statistical significance testing or confidence intervals, limiting the comparison capabilities.