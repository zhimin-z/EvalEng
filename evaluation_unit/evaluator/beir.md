## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Standard IR metrics implementation
- File: `beir/retrieval/evaluation.py`
- Class/Function: `EvaluateRetrieval.evaluate()`
- Code Reference:
```python
map_string = "map_cut." + ",".join([str(k) for k in k_values])
ndcg_string = "ndcg_cut." + ",".join([str(k) for k in k_values])
recall_string = "recall." + ",".join([str(k) for k in k_values])
precision_string = "P." + ",".join([str(k) for k in k_values])
evaluator = pytrec_eval.RelevanceEvaluator(qrels, {map_string, ndcg_string, recall_string, precision_string})
scores = evaluator.evaluate(results)
```
The harness implements standard information retrieval metrics using the `pytrec_eval` library to evaluate retrieval results. This method computes deterministic, rule-based mathematical formulas including NDCG@k (Normalized Discounted Cumulative Gain), MAP@k (Mean Average Precision), Recall@k, and Precision@k by comparing retrieved documents against ground truth relevance judgments (qrels).

Evidence 2: Custom algorithmic metrics
- File: `beir/retrieval/custom_metrics.py`
- Functions: `mrr()`, `recall_cap()`, `hole()`, `top_k_accuracy()`
- Code Reference:
```python
# Custom metrics implementations including:
# - MRR@k (Mean Reciprocal Rank)
# - Recall_cap@k (capped recall metric)
# - Hole@k (measures retrieval of unannotated documents)
# - Top_k_accuracy (measures if any relevant document appears in top-k)
```
This module implements additional custom algorithmic metrics that extend the standard IR evaluation suite. MRR computes the reciprocal rank of the first relevant document, Recall_cap implements a capped recall metric, Hole measures retrieval of unannotated documents, and Top_k_accuracy measures whether any relevant document appears in the top-k results. These are all deterministic scoring formulas applied to retrieval results.

Evidence 3: Integration in example evaluation scripts
- Files: Multiple example files (e.g., `examples/retrieval/evaluation/dense/evaluate_sbert.py`)
- Usage: Algorithmic evaluation methods applied across retrieval models
- Code Reference:
```python
# Examples demonstrate usage of evaluation methods across
# different retrieval approaches, all using the same
# algorithmic metrics for consistent evaluation
```
The algorithmic evaluation metrics are consistently applied across all retrieval model examples in the harness, demonstrating their role as the primary scoring mechanism for comparing different retrieval approaches using standardized, rule-based measurements.

---

### ML-based

Evidence 1: Neural rerankers (Cross-Encoders)
- File: `examples/retrieval/evaluation/reranking/evaluate_bm25_ce_reranking.py`
- Model: CrossEncoder
- Code Reference:
```python
cross_encoder_model = CrossEncoder("cross-encoder/ms-marco-electra-base")
reranker = Rerank(cross_encoder_model, batch_size=128)
rerank_results = reranker.rerank(corpus, queries, results, top_k=100)
```
Cross-encoder models score query-document pairs jointly through a neural network architecture. These models take the concatenated query and document as input and produce relevance scores, functioning as learned evaluators that rerank initial retrieval results based on neural predictions of document relevance.

Evidence 2: MonoT5 rerankers
- File: `examples/retrieval/evaluation/reranking/evaluate_bm25_monot5_reranking.py`
- Model: MonoT5
- Code Reference:
```python
cross_encoder_model = MonoT5("castorini/monot5-base-msmarco", token_false="▁false", token_true="▁true")
reranker = Rerank(cross_encoder_model, batch_size=128)
rerank_results = reranker.rerank(corpus, queries, results, top_k=100)
```
T5-based sequence-to-sequence models adapted as rerankers for document ranking. MonoT5 frames the ranking task as text generation, using the language model's learned representations to produce relevance judgments that serve as evaluation scores for retrieved documents.

Evidence 3: Dense retrieval models
- File: `examples/retrieval/evaluation/dense/evaluate_sbert.py`
- Model: SentenceBERT
- Code Reference:
```python
dense_model = models.SentenceBERT(
    model_name_or_path,
    max_length=max_length,
    prompt_names={"query": query_prompt_name, "passage": None},
    trust_remote_code=True,
)
model = DRES(dense_model, batch_size=128, corpus_chunk_size=50000)
retriever = EvaluateRetrieval(model, score_function="cos_sim")
results = retriever.retrieve(corpus, queries)
```
Neural embedding models based on BERT and sentence transformers encode queries and documents into dense vector representations. These models use learned parameters to compute semantic similarity scores between queries and documents through vector operations (typically cosine similarity), functioning as ML-based evaluators of document relevance.

Evidence 4: Sparse neural models
- File: `examples/retrieval/evaluation/sparse/evaluate_splade.py`
- Model: SPLADE
- Code Reference:
```python
model = DRES(models.SPLADE(model_path), batch_size=128)
retriever = EvaluateRetrieval(model, score_function="dot")
results = retriever.retrieve(corpus, queries)
```
Neural models that produce sparse representations with learned term weights. SPLADE uses a neural architecture to learn importance weights for vocabulary terms, combining the interpretability of sparse retrieval with the learning capability of neural networks to score document relevance.

Evidence 5: Large language model embedders
- Files: `examples/retrieval/evaluation/dense/evaluate_llm2vec.py`, `examples/retrieval/evaluation/dense/evaluate_nvembed.py`
- Models: LLM2Vec, NVEmbed
- Code Reference:
```python
dense_model = models.LLM2Vec(
    model_name_or_path=model_name_or_path,
    peft_model_path=peft_model_name_or_path,
    ...
)
```
Large language models (Llama, Mistral) adapted for generating document and query embeddings. These models leverage the rich semantic understanding from pre-trained LLMs to produce high-quality representations for retrieval evaluation, using learned neural parameters to assess document relevance.

Evidence 6: Additional dense retrieval models
- Files: `examples/retrieval/evaluation/dense/evaluate_dpr.py`, `examples/retrieval/evaluation/dense/evaluate_huggingface.py`
- Models: Dense Passage Retriever (DPR), E5, Tevatron
- Code Reference:
```python
# DPR, E5, Tevatron and other HuggingFace models
# used as neural evaluators for retrieval tasks
```
The harness supports additional neural retrieval models including DPR (Dense Passage Retriever) and various HuggingFace models like E5 and Tevatron. These are all neural network architectures with learned parameters that evaluate retrieval performance by scoring documents for queries, serving as ML-based evaluation models applied to benchmark tasks.