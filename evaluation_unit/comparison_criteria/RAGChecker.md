## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Ground Truth Answer Structure
- File: `ragchecker/container.py`
- Code Reference: `RAGResult` dataclass
```python
gt_answer: str  # field
```
The `RAGResult` dataclass includes a `gt_answer` field storing ground truth answers. These predetermined correct responses serve as explicit reference targets for evaluating model-generated outputs.

Evidence 2: Claim-Level Reference Checking
- File: `ragchecker/evaluator.py`
- Code Reference: `check_claims()` method
```python
case "response2answer":
    self.extract_claims(results, extract_type="gt_answer")
    claims = [ret.gt_answer_claims for ret in results]
    references = [ret.response for ret in results]
```
The evaluator extracts claims from ground truth answers and uses them as references for checking model responses. This implements claim-level entailment checking between RAG system responses and explicit ground truth answers.

Evidence 3: Precision Evaluation with Ground Truth
- File: `ragchecker/computation.py`
- Code Reference: Metrics computed using ground truth
```python
def evaluate_precision(result: RAGResult):
    assert result.answer2response is not None
    answer2response = to_bool(result.answer2response)
```
Computes precision metrics by comparing model responses against ground truth answers. The evaluation relies on explicit reference answers to determine correctness of generated claims.

Evidence 4: Benchmark Dataset Processing
- File: `data/benchmark/process_*.py` files
- Code Reference: Ground truth answer loading
```python
# From process_fiqa.py
queries.append({
    'query_id': str(q['_id']),
    'query': q['text'],
    'gt_answer': q2gt[q['_id']]['gt_answer'],
})
```
Multiple benchmark processing scripts load and format ground truth answers from datasets. Each query includes a `gt_answer` field containing static, predetermined correct responses used as reference targets for evaluation.

---

### None

Evidence 1: Faithfulness Metric Definition
- File: `ragchecker/metrics.py`
- Code Reference: Reference-free metric specification
```python
generator_metrics = "generator_metrics"
faithfulness = "faithfulness"
```
Defines faithfulness as a reference-free metric that evaluates response quality without requiring ground truth answers or external references.

Evidence 2: Faithfulness Computation
- File: `ragchecker/computation.py`
- Code Reference: `evaluate_faithfulness()` function
```python
def evaluate_faithfulness(result: RAGResult):
    assert result.retrieved2response is not None
    retrieved2response = to_bool(result.retrieved2response)
    if len(retrieved2response) > 0 and len(retrieved2response[0]) > 0:
        faithful = np.max(retrieved2response, axis=1)
        result.metrics[metrics.faithfulness] = np.mean(faithful)
```
Evaluates faithfulness by checking whether response claims are supported by retrieved context, without requiring ground truth answers. This intrinsic metric measures self-contained quality of generated responses.

Evidence 3: Retrieved Context Verification
- File: `ragchecker/evaluator.py`
- Code Reference: Faithfulness checking without ground truth
```python
case "retrieved2response":
    results = [ret for ret in results.results if ret.retrieved2response is None]
    self.extract_claims(results, extract_type="response")
    claims = [ret.response_claims for ret in results]
    references = [[doc.text for doc in ret.retrieved_context] for ret in results]
```
Checks whether response claims are grounded in retrieved documents without external references. The evaluation uses only the retrieved context and generated response, measuring intrinsic properties of output quality.

Evidence 4: Production Monitoring Capability
- File: README.md
- Code Reference: Reference-free metric documentation
```md
Q: Is RAGChecker suitable for production monitoring?
A: For production monitoring, use the reference-free metric of `faithfulness` 
as it doesn't require ground truth answers.
```
Documentation explicitly describes faithfulness as a reference-free metric suitable for production use where ground truth answers are unavailable. This confirms the metric evaluates intrinsic quality without external comparison targets.