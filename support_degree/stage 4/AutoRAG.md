# AutoRAG - Stage 4 (EVALUATE) Evaluation

## Summary
AutoRAG provides comprehensive metric computation capabilities with strong support for retrieval and generation evaluation. The framework offers 20+ built-in metrics, LLM-as-judge evaluation, statistical analysis, and some basic multi-modal support. However, output validation features are minimal, and advanced statistical comparison tools are limited.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation infrastructure. Evidence: The codebase shows basic schema validation in `autorag/schema/` but lacks comprehensive format validation, policy checks, or normalization. The `autorag/nodes/util.py` and validation modules don't show robust output validation patterns. No dedicated validation for malformed outputs, policy compliance checks, or sanity checks are evident in the documentation or code structure. |
| S4F2: Metric Computation | 3 | Extensive metric library with 20+ metrics and per-sample scoring. Evidence from `docs/source/evaluate_metrics/`: <br>- Retrieval metrics (retrieval.md): Precision, Recall, F1, MRR, MAP, NDCG with detailed per-sample computation<br>- Generation metrics (generation.md): BLEU, ROUGE, METEOR, SemScore, G-Eval (coherence, consistency, fluency, relevance), BERTScore<br>- Token metrics (retrieval_contents.md): Token Precision, Recall, F1<br>- Custom metrics supported via `autorag.evaluation.metric/` modules with extensibility<br>- Per-sample scoring clearly documented: "All attempts and evaluation metric results are recorded" (folder_structure.md) |
| S4F3: Evaluator Models | 2 | LLM-as-judge supported but limited evaluator types. Evidence:<br>- G-Eval implementation in `docs/source/evaluate_metrics/generation.md`: "G-Eval with GPT-4 as the backbone model" with chain-of-thought evaluation<br>- Four evaluation aspects: coherence, consistency, fluency, relevance<br>- Configuration example: `{metric_name: g_eval, metrics: [consistency]}`<br>- No evidence of ensemble scoring, multiple evaluator aggregation, or specialized models like RAGAS/Prometheus integration in evaluation<br>- Limited rationale capture beyond G-Eval's chain-of-thought |
| S4F4: Multi-Modal Scoring | 1 | Text-only with planned multi-modal support. Evidence from `docs/source/data_creation/data_format.md`: "It will support multi-modal, like images, videos, etc. in the future. But from an early version of AutoRAG, it only supports text." No vision-language, audio-text, or video understanding metrics are implemented. The corpus dataset only supports text contents with metadata. |
| S4F5: Aggregate Statistics | 2 | Basic statistics with limited comparison tools. Evidence:<br>- Summary CSVs show aggregated results across trials (folder_structure.md)<br>- Strategy options include mean, rank, normalize_mean (strategies.md): "mean: calculates the mean value of all specified metrics", "rank: ranks each module's results per metric, calculates the reciprocal rank"<br>- Node summary shows "evaluation metric results" per experiment<br>- Missing: No significance testing (t-test, Wilcoxon), bootstrap confidence intervals, Elo ratings, or advanced statistical comparison tools mentioned in documentation or API |

## Detailed Evidence

### S4F1: Output Validation (Rating: 1)
File: autorag/schema/base.py, autorag/validator.py
```python
# Limited schema validation exists but no comprehensive output validation
# From docs/source/troubleshooting.md:
"When you face error like `ValueError: doc_id: 0eec7e3a-e1c0-4d33-8cc5-7e604b30339b not found in corpus_data.`"
```
The framework validates corpus ID existence but lacks:
- Format validation for JSON/XML outputs
- Policy compliance checks for harmful content
- Normalization for different output formats
- Anomaly detection for identical outputs

### S4F2: Metric Computation (Rating: 3)
Files: docs/source/evaluate_metrics/*.md

Retrieval metrics (`retrieval.md`):
```yaml
strategy:
  metrics: [retrieval_f1, retrieval_recall, retrieval_ndcg, retrieval_mrr]
```

Generation metrics (`generation.md`):
```yaml
metrics:
  - metric_name: sem_score
    embedding_model: openai_embed_3_small
  - metric_name: bleu
  - metric_name: g_eval
    metrics: [consistency]
```

Per-sample computation (`test_your_rag.md`):
```python
@evaluate_retrieval(
    metric_inputs=metric_inputs,
    metrics=["retrieval_f1", "retrieval_recall", "retrieval_precision",
             "retrieval_ndcg", "retrieval_map", "retrieval_mrr"]
)
def custom_retrieval(queries):
    return retrieved_contents, retrieved_ids, retrieve_scores
```

### S4F3: Evaluator Models (Rating: 2)
File: docs/source/evaluate_metrics/generation.md
```yaml
# G-Eval with chain-of-thoughts
- metric_name: g_eval
  metrics: [coherence, consistency, fluency, relevance]
```

Documentation states: "G-Eval with GPT-4 as the backbone model achieves a Spearman correlation of 0.514 with human on a summarization task"

Missing features:
- No ensemble evaluator support
- No RAGAS/Prometheus integration for evaluation (only for data generation)
- Limited rationale capture beyond G-Eval

### S4F4: Multi-Modal Scoring (Rating: 1)
File: docs/source/data_creation/data_format.md
```python
# Explicit limitation documented:
"It will support multi-modal, like images, videos, etc. in the future.
But from an early version of AutoRAG, it only supports text."
```

Corpus only supports text:
```yaml
contents: "The actual contents. Type must be a string."
```

### S4F5: Aggregate Statistics (Rating: 2)
File: docs/source/optimization/strategies.md
```yaml
strategy:
  metrics: [retrieval_precision, retrieval_recall]
  speed_threshold: 5
  strategy: normalize_mean  # or mean, rank
```

Available aggregation methods:
- `mean`: "calculates the mean value of all specified metrics"
- `rank`: "ranks each module's results per metric, calculates the reciprocal rank"  
- `normalize_mean`: "normalizes each metric value across modules to a common scale"

Missing advanced features:
- No significance testing (t-test, Wilcoxon, permutation tests)
- No confidence intervals or bootstrap methods
- No ranking systems (Elo, TrueSkill)
- No effect size computation
- Limited to basic mean/rank comparisons

Evidence of basic statistics:
From `folder_structure.md`: "summary.csv file that summarizes the evaluation results" with per-module metrics, but no advanced statistical analysis tools are documented or evident in the API reference.