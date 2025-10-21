## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: `docs/source/evaluate_metrics/retrieval.md`
This documentation clearly describes how AutoRAG uses ground truth labels for retrieval evaluation. The document states: "retrieval_gt" is used to validate retrieval outputs, and examples show `retrieval_gt = [['test-1', 'test-2'], ['test-3']]` as static reference answers for benchmarks.

Evidence 2: `docs/source/test_your_rag.md`
- Code Reference: `MetricInput` dataclass definition
```
MetricInput(
    query=x[1]["query"],
    retrieval_gt=x[1]["retrieval_gt"],  # Ground truth passage IDs
)
```
This shows explicit ground truth labels (`retrieval_gt`) loaded from QA datasets for evaluating retrieval performance. The `generation_gt` field stores ground truth answers for generation evaluation.

### None

Evidence 1: `docs/source/evaluate_metrics/retrieval_contents.md`
This documentation clearly describes token-level metrics (Token Precision, Token Recall, Token F1) that measure intrinsic properties of retrieved passages by comparing token overlap without requiring external ground truth passages. These are self-contained quality measures.

Evidence 2: From `docs/source/evaluate_metrics/retrieval_contents.md`
- Code Reference:
```
## 1. Token Precision
Number of overlapping tokens / token length in result

## 2. Token Recall  
Number of overlapping tokens / token length in gt

## 3. Token F1
F1 score is the harmonic mean of Precision and Recall
```
While these metrics compare to answer_gt, they measure intrinsic token-level properties (overlap, length) rather than relying on external corpus references. The measurement is self-contained within the retrieved content.