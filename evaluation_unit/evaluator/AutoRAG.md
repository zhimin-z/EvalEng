## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Standard information retrieval metrics implementation
- File: `autorag/evaluation/metric/retrieval.py`
- Related Files: `autorag/evaluation/metric/generation.py`, `autorag/evaluation/metric/retrieval_contents.py`
- Code Reference:
```yaml
strategy:
  metrics: [retrieval_f1, retrieval_recall, retrieval_precision]
```
The evaluation harness extensively uses predefined algorithmic metrics for evaluating RAG system outputs. The system implements standard IR metrics including Precision, Recall, F1 Score (standard classification metrics), MRR (Mean Reciprocal Rank), MAP (Mean Average Precision), and NDCG (Normalized Discounted Cumulative Gain) as documented in `docs/source/evaluate_metrics/retrieval.md`.

Evidence 2: Natural language generation metrics
- Documentation: `docs/source/test_your_rag.md`
- Metrics: BLEU, ROUGE, METEOR, and semantic similarity metrics
These are standard NLG metrics that use deterministic, mathematical formulas to score outputs based on statistical calculations and string/token matching algorithms.

Evidence 3: Token-level overlap evaluation
- Documentation: `docs/source/evaluate_metrics/retrieval_contents.md`
- Metrics: Token Precision, Token Recall, Token F1
Token-level overlap metrics that provide granular evaluation of retrieval quality through algorithmic comparison of token sequences.

Evidence 4: Test implementation verification
- File: `tests/autorag/test_evaluator.py`
- Code Reference:
```python
assert node.strategy["metrics"] == ["retrieval_f1", "retrieval_recall"]
```
Test evidence demonstrates metrics like `retrieval_f1`, `retrieval_recall`, and `retrieval_precision` being used throughout the harness, confirming the algorithmic evaluation approach.

---

### ML-based

Evidence 1: LLM-as-Judge evaluation paradigm
- File: `autorag/nodes/passagereranker/rankgpt.py`
- Test File: `tests/autorag/nodes/passagereranker/test_rankgpt.py`
- Code Reference:
```python
from autorag.nodes.passagereranker import RankGPT
result_df = RankGPT.run_evaluator(
    project_dir=project_dir,
    previous_result=previous_result,
    top_k=top_k,
    llm="openai",
    model="gpt-3.5-turbo"
)
```
RankGPT uses GPT models to evaluate and rank passage relevance, implementing the LLM-as-Judge pattern where language models serve as evaluators for assessing retrieval quality.

Evidence 2: Neural reranking models as evaluators
- Files: `autorag/nodes/passagereranker/sentence_transformer.py`, `autorag/nodes/passagereranker/cohere_reranker.py`, `autorag/nodes/passagereranker/jina_reranker.py`
- Test Files: `test_sentence_transformer.py`, `test_cohere_reranker.py`, `test_jina_reranker.py`
Multiple ML-based reranking models are used for evaluation purposes, including SentenceTransformerReranker (using cross-encoder models), CohereReranker (using Cohere's reranking API), JinaReranker (using Jina AI reranking), as well as FlagEmbeddingReranker, MonoT5, and ColbertReranker. These models evaluate passage relevance using learned neural network representations.

Evidence 3: Embedding-based semantic evaluation
- Documentation: `docs/source/test_your_rag.md`
- Code Reference:
```python
@evaluate_generation(
    metric_inputs=metric_inputs,
    metrics=[
        {"metric_name": "sem_score", "embedding_model": "openai_embed_3_small"}
    ]
)
```
The harness uses embedding models to compute semantic similarity scores for generation evaluation, leveraging learned vector representations to assess output quality beyond surface-level text matching.

Evidence 4: Deepeval integration for ML-based metrics
- API Documentation: `docs/source/api_spec/autorag.evaluation.metric.rst`
- Module: `autorag.evaluation.metric.deepeval_prompt`
- Code Reference:
```rst
autorag.evaluation.metric.deepeval_prompt module
```
References ML-based evaluation from the deepeval library, integrating external ML-powered evaluation capabilities into the harness.

Evidence 5: ML model usage in passage evaluation tests
- File: `tests/autorag/nodes/passagereranker/test_passage_reranker_base.py`
Multiple test files demonstrate ML models being used to score and rank passages for evaluation purposes, not just as retrieval components but as evaluators of retrieval quality. These ML models evaluate benchmark task outputs such as passage relevance and generation quality using learned representations and neural network inference.