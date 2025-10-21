## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Metric names and requirements definition
- File: `ragchecker/metrics.py`
- Code Reference:
```python
# Defines metrics like precision, recall, f1, claim_recall, context_precision, etc.
# These are metric identifiers used in computations
```
This file establishes the foundational metric identifiers that are referenced throughout the computation pipeline, providing the naming schema for all algorithmic evaluations.

Evidence 2: Algorithmic metric computation functions
- File: `ragchecker/computation.py`
- Functions: `evaluate_precision()`, `evaluate_recall()`, `evaluate_f1()`, `evaluate_claim_recall()`, `evaluate_context_precision()`, `evaluate_context_utilization()`, `evaluate_noise_sensitivity()`, `evaluate_unfaithfulness()`, `evaluate_faithfulness()`
- Code Reference:
```python
# evaluate_precision()
result.metrics[metrics.precision] = np.mean(answer2response)

# evaluate_recall()
result.metrics[metrics.recall] = np.mean(response2answer)

# evaluate_f1()
result.metrics[metrics.f1] = 2 * precision * recall / (precision + recall)

# evaluate_claim_recall()
claim_recalled = np.max(retrieved2answer, axis=1)
result.metrics[metrics.claim_recall] = np.mean(claim_recalled)

# evaluate_context_precision()
psg_useful = np.max(retrieved2answer, axis=0)
result.metrics[metrics.context_precision] = np.mean(psg_useful)

# evaluate_context_utilization()
claim_used = claim_recalled & response2answer
result.metrics[metrics.context_utilization] = np.sum(claim_used) / np.sum(claim_recalled)

# evaluate_unfaithfulness()
unfaithful = ~np.max(retrieved2response, axis=1)

# evaluate_faithfulness()
result.metrics[metrics.faithfulness] = np.mean(faithful)
```
These are pure mathematical functions that take intermediate boolean checking results (entailment/contradiction labels) and compute statistical metrics using numpy operations. The computations involve means, boolean logic (AND, OR, NOT via `&`, `|`, `~`), max operations, and arithmetic formulas. These are deterministic, rule-based calculations that score RAG system outputs based on mathematical formulas, ensuring consistent and reproducible evaluation through established computational measures.

---

### ML-based

Evidence 1: ML model initialization
- File: `ragchecker/evaluator.py`
- Class: `RAGChecker.__init__()`
- Code Reference:
```python
# Lines 43-95: Initializes LLMExtractor and LLMChecker (or NLIChecker, AlignScoreChecker)
self.extractor = LLMExtractor(
    model=extractor_name, 
    batch_size=batch_size_extractor,
    api_base=extractor_api_base
)
if checker_name == "nli":
    self.checker = NLIChecker(batch_size=batch_size_checker)
elif checker_name == "alignscore":
    self.checker = AlignScoreChecker(batch_size=batch_size_checker)
else:
    self.checker = LLMChecker(
        model=checker_name, 
        batch_size=batch_size_checker,
        api_base=checker_api_base
    )
```
The RAGChecker class initializes ML-based components that serve as the primary evaluators. These learned models with neural network architectures perform inference on benchmark task outputs (RAG system responses) to assess quality through learned representations.

Evidence 2: LLM-based claim extraction
- File: `ragchecker/evaluator.py`
- Function: `RAGChecker.extract_claims()`
- Code Reference:
```python
# Lines 97-126: Uses LLM extractor to extract claims from text
extraction_results = self.extractor.extract(
    batch_responses=texts,
    batch_questions=questions,
    max_new_tokens=self.extractor_max_new_tokens,
    ...
)
claims = [[c.content for c in res.claims] for res in extraction_results]
```
The LLM extractor decomposes responses into atomic claims using a large language model, leveraging learned representations to understand and segment the semantic content of RAG system outputs for granular evaluation.

Evidence 3: ML-based claim verification
- File: `ragchecker/evaluator.py`
- Function: `RAGChecker.check_claims()`
- Code Reference:
```python
# Lines 128-176: Uses LLM/ML checker to verify claim entailment
checking_results = self.checker.check(
    batch_claims=claims,
    batch_references=references,
    batch_questions=[ret.query for ret in results],
    ...
)
```
The ML checker (LLMChecker, NLIChecker, or AlignScoreChecker) uses machine learning models to verify whether claims are entailed by reference texts. These models generate entailment judgments (like "Entailment" or "Contradiction") which are then converted to boolean values (`to_bool()` function in `computation.py`) and used in the algorithmic metric computations, capturing semantic and contextual quality through learned patterns.

Evidence 4: ML model specification in configuration
- File: `ragchecker/cli.py` and `README.md`
- Code Reference:
```python
# CLI arguments specify models like:
--extractor_name=bedrock/meta.llama3-70b-instruct-v1:0
--checker_name=bedrock/meta.llama3-70b-instruct-v1:0

# README documentation:
--extractor_name=bedrock/meta.llama3-1-70b-instruct-v1:0
--checker_name=bedrock/meta.llama3-1-70b-instruct-v1:0
```
The documentation explicitly identifies the use of large language models as evaluators. The tutorial mentions "RAGChecker uses a large language model (LLM) as an extractor" and "Another LLM acts as a checker," confirming that ML-based models are the primary evaluation mechanism for assessing RAG system quality.

Evidence 5: Comparative ML-based evaluation systems
- File: `data/meta_evaluation/meta_eval.py`
- Code Reference:
```python
# Lines 18-40: Compares RAGChecker against other ML-based evaluation systems
evaluation_metrics = {
    "trulens": [...],
    "ares": [...],
    "ragas": [...],
    ...
}
```
The meta-evaluation framework references other ML-based evaluators including NLI-based systems and AlignScore, positioning RAGChecker within an ecosystem of machine learning approaches to RAG evaluation. These ML models are evaluating the quality of RAG-generated responses, not used for harness development or testing, demonstrating the prevalence of ML-based evaluation in this domain.