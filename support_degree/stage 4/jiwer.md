# jiwer - Stage 4 (EVALUATE) Evaluation

## Summary
JiWER is a specialized library for computing speech recognition metrics (WER, CER, MER, WIL, WIP) with alignment visualization. It focuses narrowly on ASR evaluation with strong per-sample scoring and basic aggregation, but lacks output validation, multi-modal support, and evaluator model integration features expected in a general evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation or normalization features exist. The library expects pre-processed text inputs and provides no format validation, policy compliance checks, or sanity checking mechanisms. |
| S4F2: Metric Computation | 2 | Implements 5 ASR-specific metrics (WER, CER, MER, WIL, WIP) with per-sample scoring and efficient computation using RapidFuzz. Lacks broader metric coverage and extensibility for custom metrics beyond ASR. |
| S4F3: Evaluator Models | 0 | No support for LLM-as-judge, evaluator models, or ensemble scoring. This is purely a string distance-based metric library without any model-based evaluation capabilities. |
| S4F4: Multi-Modal Scoring | 0 | Text-only library with no multi-modal evaluation support. Focused exclusively on text-based ASR evaluation. |
| S4F5: Aggregate Statistics | 1 | Provides basic aggregation (total hits, substitutions, insertions, deletions) and simple derived metrics. No statistical analysis, confidence intervals, significance testing, or ranking systems. |

---

## Detailed Feature Analysis

### S4F1: Output Validation and Normalization (0/3)

Evidence:

The library provides no output validation features. It operates on raw text strings with optional transformations but performs no validation:

From `src/jiwer/measures.py`:
```python
def wer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
```

The only "validation" is basic type checking in `src/jiwer/process.py`:
```python
# validate input type
if isinstance(reference, str):
    reference = [reference]
if isinstance(hypothesis, str):
    hypothesis = [hypothesis]
```

Normalization exists but not validation:
- The library provides text transformations (lowercase, punctuation removal, etc.) in `src/jiwer/transforms.py`
- These are normalization operations, not validation
- No format validation (JSON, XML), schema checking, or sanity checks
- No policy compliance checks for harmful content or constraints
- No detection of malformed, partial, or truncated outputs

Why 0 points: The library expects users to provide clean text inputs and performs no validation of output quality, format, or policy compliance.

---

### S4F2: Task-Specific Metric Computation (2/3)

Evidence:

JiWER implements 5 metrics for ASR evaluation, documented in `src/jiwer/measures.py`:

```python
__all__ = [
    "cer",  # Character Error Rate
    "mer",  # Match Error Rate
    "wer",  # Word Error Rate
    "wil",  # Word Information Lost
    "wip",  # Word Information Preserved
]
```

Strengths:

1. Per-sample scoring available via `process_words()` and `process_characters()`:
```python
output = jiwer.process_words(reference, hypothesis)
# Access per-sentence alignments
for idx, chunks in enumerate(output.alignments):
    # Per-sentence analysis available
```

2. Efficient implementation using RapidFuzz (C++ backed):
```python
# From src/jiwer/process.py
opcodes = rapidfuzz.distance.Levenshtein.opcodes(
    reference_sentence, hypothesis_sentence
)
```

3. Edge case handling for empty references (from `tests/test_empty_ref.py`):
```python
def test_empty_ref_empty_hyp():
    out = jiwer.process_words(reference="", hypothesis="")
    assert out.wer == 0  # Correctly handles edge case
```

Limitations:

1. Limited scope: Only ASR metrics, no classification, retrieval, or safety metrics
2. No custom metric API: Users cannot define new metrics without modifying the library
3. No metric composition: Cannot combine metrics or create weighted combinations
4. No external integration: No support for integrating metrics from other libraries

From the README:
```markdown
It supports the following measures:
1. word error rate (WER)
2. match error rate (MER)
3. word information lost (WIL) 
4. word information preserved (WIP) 
5. character error rate (CER)
```

Why 2 points: Strong implementation of a narrow set of metrics with per-sample scoring, but lacks extensibility and broader metric coverage (10-20 metrics would get 2 points, this has 5 specialized ones with excellent implementation quality).

---

### S4F3: Evaluator Model Integration (0/3)

Evidence:

Complete absence of any evaluator model features:

- No LLM-as-judge capabilities
- No pre-built judge prompts
- No support for specialized evaluator models (RAGAS, G-Eval, Prometheus)
- No ensemble scoring mechanisms
- No rationale capture

The library is purely algorithmic (string distance based), not model-based. All metrics are computed via edit distance operations:

```python
# From src/jiwer/process.py - only uses algorithmic distance
opcodes = rapidfuzz.distance.Levenshtein.opcodes(
    reference_sentence, hypothesis_sentence
)
```

No model inference, API calls, or judge prompts anywhere in the codebase.

Why 0 points: This is a string metric library, not an LLM evaluation framework. No evaluator model support exists or is planned.

---

### S4F4: Multi-Modal Scoring Protocols (0/3)

Evidence:

The library is text-only with no multi-modal capabilities:

From the documentation (`docs/index.md`):
```markdown
JiWER is a simple and fast python package to evaluate an automatic speech recognition system.
```

Despite being for "speech recognition," it only processes text transcriptions, not audio:

```python
# From docs/usage.md
reference = "hello world"
hypothesis = "hello duck"
error = wer(reference, hypothesis)
```

No support for:
- Audio processing (WER for speech, despite the name)
- Image captioning metrics
- Video understanding
- Cross-modal retrieval
- Any modality-specific validators

The library assumes users have already transcribed audio to text externally.

Why 0 points: Pure text processing with no multi-modal evaluation capabilities.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (1/3)

Evidence:

Basic aggregation only:

From `src/jiwer/process.py`, the `WordOutput` class provides:
```python
@dataclass
class WordOutput:
    # Basic counts
    hits: int
    substitutions: int
    insertions: int
    deletions: int
    
    # Simple derived metrics
    wer: float
    mer: float
    wil: float
    wip: float
```

What exists:
1. Total counts across all samples:
```python
# From src/jiwer/process.py
num_hits, num_substitutions, num_deletions, num_insertions = 0, 0, 0, 0
for reference_sentence, hypothesis_sentence in zip(ref_as_ints, hyp_as_ints):
    # ... accumulate counts
```

2. Simple averages via aggregated metrics (WER is total errors / total words)

3. Error frequency counting via `visualize_error_counts()`:
```python
# From src/jiwer/alignment.py
def collect_error_counts(output: Union[WordOutput, CharacterOutput]):
    """
    Retrieve three dictionaries, which count the frequency of how often
    each word or character was substituted, inserted, or deleted.
    """
    substitutions = defaultdict(lambda: 0)
    insertions = defaultdict(lambda: 0)
    deletions = defaultdict(lambda: 0)
```

What's missing:
- No percentiles (P25, P50, P75, P95, P99)
- No standard deviation, variance, or confidence intervals
- No distribution analysis or histograms
- No outlier detection
- No model comparison features (no t-tests, bootstrap, permutation tests)
- No ranking systems (Elo, TrueSkill)
- No significance testing
- No stratified statistics or sample weighting

From the tests, we can see no statistical functions beyond basic counts:
```python
# tests/test_measures.py - only checks exact metric values
test_case.assertAlmostEqual(a[k], b[k], places=places, msg=msg, delta=delta)
```

Why 1 point: Only provides basic counts and simple derived metrics. No statistical analysis, distribution analysis, or model comparison capabilities. Users would need to export data and use external tools for any statistical analysis.

---

## Scoring Summary

Total Score: 3/15

- S4F1 (Validation): 0/3 - No validation features
- S4F2 (Metrics): 2/3 - Strong ASR metrics but narrow scope
- S4F3 (Evaluators): 0/3 - No model-based evaluation
- S4F4 (Multi-modal): 0/3 - Text-only
- S4F5 (Statistics): 1/3 - Basic aggregation only

## Key Findings

Strengths:
1. Excellent implementation of ASR-specific metrics with per-sample alignment
2. Efficient computation using RapidFuzz (C++ backend)
3. Good edge case handling (empty references)
4. Clear visualization of alignments and error patterns

Limitations:
1. Not a general evaluation framework - highly specialized for ASR
2. No validation, policy checking, or output sanitization
3. No model-based evaluation or LLM-as-judge support
4. No statistical analysis or model comparison tools
5. Text-only with no multi-modal support

Use Case: JiWER is a focused tool for computing ASR metrics efficiently, not a comprehensive evaluation framework. It excels at its narrow domain but lacks the breadth expected in Stage 4 of the 8-stage evaluation framework.