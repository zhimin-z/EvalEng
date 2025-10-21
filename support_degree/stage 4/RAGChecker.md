# RAGChecker - Stage 4 (EVALUATE) Evaluation

## Summary
RAGChecker is a specialized RAG evaluation framework with a unique claim-level checking approach. It provides fine-grained metrics for assessing retrieval and generation components separately, plus overall RAG quality. The framework is narrow but deep, focusing specifically on entailment-based evaluation rather than providing a broad metric library. It has minimal validation features and limited statistical capabilities but excels at its core claim-checking methodology.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation. Only basic format checks exist in the code for JSON structure (`container.py` uses dataclasses with type hints). No policy compliance, sanity checks, or normalization features. Evidence: No dedicated validation module; outputs are simply stored as strings in `RAGResult.response`. |
| S4F2: Metric Computation | 2 | Limited but specialized metric set (~11 metrics). Covers overall (precision/recall/F1), retrieval (claim_recall, context_precision), and generation (faithfulness, hallucination, etc.). All metrics are claim-based, not diverse task types. Per-sample scoring supported (`result.metrics` dict per `RAGResult`). No extensibility - adding custom metrics requires forking. Evidence: `metrics.py` defines all metrics, `computation.py` implements ~11 metric functions. Example metrics in `examples/checking_outputs.json` show per-sample scores. |
| S4F3: Evaluator Models | 2 | Basic LLM-as-judge support via RefChecker integration. Uses LLM for claim extraction and entailment checking (`evaluator.py:LLMExtractor`, `LLMChecker`). No pre-built judge prompts - relies on RefChecker's implementation. No ensemble or rationale capture beyond basic extraction/checking. Alternative checkers exist (NLI, AlignScore) but limited. Evidence: `evaluator.py` lines 43-78 show `LLMExtractor` and `LLMChecker` initialization; no custom evaluator framework beyond RefChecker wrapper. |
| S4F4: Multi-Modal Scoring | 0 | Text-only. No support for vision, audio, or video modalities. All examples use text documents and responses. Evidence: `container.py:RetrievedDoc` only has `text` field; tutorial examples (`tutorial/ragchecker_tutorial_en.md`) only discuss text-based QA. |
| S4F5: Aggregate Statistics | 1 | Very basic aggregation. Only computes mean across samples (`computation.py` uses `np.mean()`). Outputs simple averages in `results.metrics` dict with overall/retriever/generator groupings. No distribution analysis, significance testing, ranking, or weighted metrics. Evidence: `evaluator.py` lines 252-258 show simple `np.mean()` aggregation; `examples/checking_outputs.json` shows only mean values (e.g., `"precision": 76.4`). No statistical tests or confidence intervals in codebase. |

---

## Detailed Feature Analysis

### S4F1: Output Validation and Normalization (1 pt)

Evidence:

1. Format Validation: Minimal. Uses dataclasses with basic type checking:
```python
# ragchecker/container.py
@dataclass_json
@dataclass
class RAGResult:
    query_id: str
    query: str
    gt_answer: str
    response: str  # No validation on response content
    retrieved_context: List[RetrievedDoc] | None = None
```
No schema validation, malformed output detection, or partial output handling.

2. Policy Compliance: None. No checks for harmful content, length constraints, or required fields beyond basic type hints.

3. Sanity Checks: None. No logical consistency checks or anomaly detection.

4. Normalization: None. Responses stored as-is with no standardization. Example from `examples/checking_inputs.json` shows raw response text is accepted verbatim.

Rating Justification: Barely exists (1 pt). Only basic dataclass type hints; no actual validation logic.

---

### S4F2: Task-Specific Metric Computation (2 pts)

Evidence:

1. Coverage (~11 metrics):
```python
# ragchecker/metrics.py
# Overall metrics
precision = "precision"
recall = "recall"
f1 = "f1"

# Retriever metrics
claim_recall = "claim_recall"
context_precision = "context_precision"

# Generator metrics
context_utilization = "context_utilization"
noise_sensitivity_in_relevant = "noise_sensitivity_in_relevant"
noise_sensitivity_in_irrelevant = "noise_sensitivity_in_irrelevant"
hallucination = "hallucination"
self_knowledge = "self_knowledge"
faithfulness = "faithfulness"
```

All metrics are RAG-specific (entailment-based), not general-purpose. No BLEU/ROUGE, classification metrics, or retrieval metrics like NDCG.

2. Implementation Quality: Uses NumPy for vectorized computation:
```python
# ragchecker/computation.py:92-98
retrieved2answer = to_bool(result.retrieved2answer)
if len(retrieved2answer) > 0 and len(retrieved2answer[0]) > 0:
    claim_recalled = np.max(retrieved2answer, axis=1)
    result.metrics[metrics.claim_recall] = np.mean(claim_recalled)
```

Edge cases handled (empty checks), but implementation is simple boolean operations, not reference implementations from established libraries.

3. Granularity: Per-sample scoring supported:
```json
// examples/checking_outputs.json (line 120-131)
"metrics": {
    "precision": 0.7272727272727273,
    "recall": 0.5,
    "claim_recall": 0.22727272727272727,
    // ... per-sample metrics
}
```

Batch processing via `batch_size_extractor` and `batch_size_checker` parameters.

4. Extensibility: No custom metric support. All metrics hardcoded in `computation.py`. Adding metrics requires modifying framework code. No plugin system or metric composition features.

Rating Justification: 10-20 metrics (11 total), mostly standard for RAG, per-sample supported, but no extensibility caps at 2 pts.

---

### S4F3: Evaluator Model Integration (2 pts)

Evidence:

1. LLM-as-Judge: Basic support via RefChecker:
```python
# ragchecker/evaluator.py:51-65
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

Uses LiteLLM for LLM invocation (supports OpenAI, Bedrock, etc.). Judging criteria are fixed (claim extraction + entailment checking), not configurable.

2. Specialized Models: Supports NLI and AlignScore as alternative checkers, but these are still entailment-focused. No RAGAS, G-Eval, or Prometheus integration.

3. Ensemble Scoring: None. Only one evaluator runs at a time (either LLM, NLI, or AlignScore).

4. Rationale Capture: None. Only saves entailment labels (Entailment/Neutral/Contradiction), not reasoning:
```json
// examples/checking_outputs.json (line 48-51)
"answer2response": [
    "Neutral",
    "Entailment",
    "Entailment",
    // ... only labels, no explanations
]
```

Rating Justification: Basic LLM judge with limited evaluator types (2 pts). No ensemble, no rationale capture, not evaluation-specific beyond claim checking.

---

### S4F4: Multi-Modal Scoring Protocols (0 pts)

Evidence:

1. Text-Only: All data structures are text-based:
```python
# ragchecker/container.py:16-18
@dataclass
class RetrievedDoc:
    doc_id: str | None = None
    text: str = ""  # Only text field
```

2. No Multi-Modal Metrics: Examples (`examples/checking_inputs.json`) only show text queries/responses. Tutorial (`tutorial/ragchecker_tutorial_en.md`) focuses entirely on text QA.

3. No Infrastructure: No image/audio/video artifact handling. No cross-modal retrieval support.

Rating Justification: 0 pts. Completely text-focused, no multi-modal features.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (1 pt)

Evidence:

1. Basic Statistics: Only mean:
```python
# ragchecker/evaluator.py:252-258
for group, group_metrics in METRIC_GROUP_MAP.items():
    if group == all_metrics:
        continue
    for metric in group_metrics:
        if metric in ret_metrics:
            results.metrics[group][metric] = round(np.mean(
                [result.metrics[metric] for result in results.results]
            ) * 100, 1)  # Only computes mean
```

Output example:
```json
// examples/checking_outputs.json:182-194
"metrics": {
    "overall": {
      "precision": 76.4,  // Mean only
      "recall": 62.5,
      "f1": 68.3
    },
    // ... no std dev, percentiles, or confidence intervals
}
```

2. Distribution Analysis: None. No histograms, outlier detection, or measurement reliability.

3. Model Comparison: None. No significance testing, bootstrap, or permutation tests. Meta-evaluation script (`data/meta_evaluation/meta_eval.py`) computes Pearson/Spearman correlation but is separate from main framework:
```python
# data/meta_evaluation/meta_eval.py:34-37
def correlation(a, b):
    pearson = round(stats.pearsonr(a, b)[0] * 100, 2)
    spearman = round(stats.spearmanr(a, b)[0] * 100, 2)
    return pearson, spearman
```

This is for evaluating RAGChecker itself, not for comparing models in user evaluations.

4. Ranking Systems: None. No Elo, TrueSkill, or leaderboards.

5. Weighted Metrics: None. No class imbalance handling or sample importance weighting.

Rating Justification: 1 pt. Only mean/median; no distribution analysis or statistical tests in the user-facing evaluation pipeline.

---

## Key Strengths

1. Specialized Approach: Claim-level checking provides fine-grained, interpretable evaluation for RAG systems.
2. Per-Sample Scoring: All metrics computed at sample level before aggregation.
3. Dual Evaluation: Separates retriever and generator metrics for targeted diagnosis.
4. LLM Flexibility: Supports multiple LLM providers via LiteLLM and custom API functions.

## Key Limitations

1. Narrow Metric Set: Only ~11 RAG-specific metrics; not suitable for general NLP evaluation.
2. No Extensibility: Adding custom metrics requires modifying framework code.
3. Minimal Validation: No output format checking, policy compliance, or normalization.
4. Basic Statistics: Only mean aggregation; no distribution analysis or significance testing.
5. No Multi-Modal Support: Text-only evaluation.
6. No Model Comparison Tools: Users must manually compare results from different RAG systems.

## Comparison to Rubric

- 3-Point Features: None. All features fall short of "comprehensive," "extensible," or "full statistical suite" requirements.
- 2-Point Features: S4F2 (specialized but limited metric set), S4F3 (basic LLM judge).
- 1-Point Features: S4F1 (minimal validation), S4F5 (mean-only aggregation).
- 0-Point Features: S4F4 (no multi-modal support).

---

## Final Checklist

- [x] All 5 features rated (S4F1 through S4F5)
- [x] Every rating has evidence (file paths, code snippets, JSON examples)
- [x] Justifications concise (2-4 sentences)
- [x] Consistent rating standards across features

---

Total Stage 4 Score: 6/15 points

RAGChecker is a specialized RAG evaluation tool with a unique claim-based methodology, but it lacks the breadth (diverse metrics, multi-modal support), depth (validation, statistical analysis), and extensibility expected of a comprehensive evaluation framework. It works well for its intended narrow use case but is not suitable for general-purpose evaluation tasks.