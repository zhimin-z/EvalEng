# JiWER - Stage 7 (VALIDATE) Evaluation

## Summary
JiWER is a specialized library for computing word error rate (WER) and character error rate (CER) for automatic speech recognition systems. It is not an evaluation framework in the sense of Stage 7 requirements - it's a metric computation library. It lacks quality gates, compliance validation, and ensemble decision-making capabilities entirely, as these concepts are outside its scope as a single-purpose metric library.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S7F1: Quality Gates | 0 | No quality gate features exist. JiWER computes metrics (WER, MER, CER, etc.) but provides no threshold checking, pass/fail decisions, or automated quality gates. The library returns metric values that users must manually evaluate. Evidence: The `measures.py` functions (`wer()`, `mer()`, etc.) only return float values with no threshold comparison capabilities. |
| S7F2: Compliance Validation | 0 | No compliance, fairness, explainability, or regulatory features exist. JiWER is purely a metric computation tool for ASR evaluation without any compliance checking, fairness testing, or model card generation capabilities. Evidence: Review of all source files shows only metric computation logic with no compliance-related functionality. |
| S7F3: Ensemble Decisions | 0 | No ensemble orchestration or multi-model comparison features exist. JiWER processes single reference-hypothesis pairs to compute error rates. It has no concept of multiple models, voting mechanisms, or deployment recommendations. Evidence: `process_words()` and `process_characters()` in `src/jiwer/process.py` only handle single hypothesis comparisons. |

## Detailed Analysis

### S7F1: Quality Gate Application (0 pts)

Evidence of absence:

1. No threshold configuration: Review of `src/jiwer/measures.py` shows all functions return raw float values:
```python
def wer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate the word error rate (WER) between one or more reference and
    hypothesis sentences.
    
    Returns:
        (float): The word error rate of the given reference and
                 hypothesis sentence(s).
    """
    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )
    return output.wer
```

2. No pass/fail logic: The library only computes metrics without any decision-making capability. Users must manually check if results meet their thresholds.

3. No safety checks: There are no automated harmful content detection, safety metrics, or red-team test requirements.

4. No regression testing: While the library computes error rates, it doesn't compare against baselines or detect regressions automatically.

5. CLI limitations: Even the CLI tool in `src/jiwer/cli.py` only outputs metric values without threshold checking:
```python
if show_alignment:
    print(jiwer.visualize_alignment(out, show_measures=True), end="")
else:
    if compute_cer:
        print(out.cer)
    else:
        print(out.wer)
```

### S7F2: Regulatory Compliance Validation (0 pts)

Evidence of absence:

1. No fairness testing: The library has no demographic parity, equalized odds, or any fairness metrics. It only computes alignment-based error rates.

2. No explainability: While JiWER provides alignment visualization (`visualize_alignment()` in `src/jiwer/alignment.py`), this shows word-level differences, not model explainability. No SHAP, LIME, or model card generation exists:
```python
def visualize_alignment(
    output: Union[WordOutput, CharacterOutput],
    show_measures: bool = True,
    skip_correct: bool = True,
    line_width: Optional[int] = None,
) -> str:
    """
    Visualize the output of [jiwer.process_words][process.process_words] and
    [jiwer.process_characters][process.process_characters]. The visualization
    shows the alignment between each processed reference and hypothesis pair.
    """
```

3. No privacy validation: No GDPR, CCPA, data minimization, or consent tracking features exist.

4. No certification support: No EU AI Act, NIST AI RMF, ISO/IEC standards, or audit trail generation capabilities.

The library is focused solely on computing alignment-based metrics for ASR evaluation, not on compliance or regulatory requirements.

### S7F3: Model Ensemble Decision-Making (0 pts)

Evidence of absence:

1. Single hypothesis only: The `process_words()` function in `src/jiwer/process.py` processes one reference and one hypothesis:
```python
def process_words(
    reference: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> WordOutput:
    """
    Compute the word-level levenshtein distance and alignment between one or more
    reference and hypothesis sentences.
    """
```

2. No multi-model support: The library has no concept of evaluating multiple models simultaneously or comparing them.

3. No voting mechanisms: There are no majority voting, weighted voting, or any ensemble strategies.

4. No deployment recommendations: The library outputs metrics but provides no recommendations about which model to deploy.

5. Architecture limitation: The core design is about comparing reference text to hypothesis text, not about orchestrating multiple models:
```python
@dataclass
class WordOutput:
    """
    The output of calculating the word-level levenshtein distance between one or
    more reference and hypothesis sentence(s).
    """
    references: List[List[str]]
    hypotheses: List[List[str]]
    alignments: List[List[AlignmentChunk]]
    wer: float
    mer: float
    # ...
```

## Conclusion

JiWER receives 0/9 points for Stage 7 because it is fundamentally a metric computation library rather than an evaluation framework with pre-deployment validation capabilities. It excels at its intended purpose (computing WER, CER, and related metrics for ASR systems) but has no features for:

- Automated quality gates or threshold-based decisions
- Compliance validation or fairness testing  
- Ensemble model orchestration or multi-model comparison

This is not a criticism of JiWER - it simply operates at a different level of abstraction. It's a building block that could be used *within* an evaluation framework, but it is not itself a framework for pre-deployment validation. Users would need to build quality gates, compliance checks, and ensemble logic on top of JiWER's metric computation capabilities.