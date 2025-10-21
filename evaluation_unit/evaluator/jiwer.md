## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Multiple metric functions for ASR evaluation
- File: `src/jiwer/measures.py`
- Functions: `wer()`, `mer()`, `wil()`, `wip()`, `cer()`
- Code Reference:
```python
# Lines implementing WER calculation in src/jiwer/process.py
wer = float(subs + dels + ins) / float(hits + subs + dels)
mer = float(subs + dels + ins) / float(hits + subs + dels + ins)
wip = (float(hits) / num_rf_words) * (float(hits) / num_hp_words)
wil = 1 - wip
```
This evidence demonstrates algorithmic evaluation through deterministic, formula-based metrics. Word Error Rate (WER) is computed using the formula `(substitutions + deletions + insertions) / total_reference_words`, while Match Error Rate (MER), Word Information Lost (WIL), and Word Information Preserved (WIP) follow similar mathematical formulas. These metrics are purely computational, producing consistent results for identical inputs, which aligns with the algorithmic evaluator's goal of ensuring reproducible evaluation through established computational measures.

Evidence 2: Levenshtein distance computation for edit operations
- File: `src/jiwer/process.py`
- Functions: `process_words()` and `process_characters()`
- Code Reference:
```python
opcodes = rapidfuzz.distance.Levenshtein.opcodes(
    reference_sentence, hypothesis_sentence
)
```
These functions employ the Levenshtein distance algorithm via the RapidFuzz library to compute minimum edit operations (substitutions, deletions, insertions, hits) between reference and hypothesis texts. This algorithmic approach is deterministic and rule-based, deriving error rates directly from edit operation counts. The use of established computational algorithms for string comparison exemplifies predefined metrics that provide consistent assessment across evaluations, fulfilling the algorithmic evaluator definition.

Evidence 3: Comprehensive test suite validating algorithmic behavior
- File: `tests/test_measures.py` - Tests for WER, MER, WIL, WIP calculations with known values
- File: `tests/test_cer.py` - Tests for CER (Character Error Rate) calculations
- File: `tests/test_empty_ref.py` - Tests for edge cases in metric calculations
- Code Reference: Test files demonstrating algorithmic evaluation
The test suite validates that all metrics behave deterministically with known expected values, confirming the algorithmic nature of the evaluators. Tests verify that Character Error Rate (CER) applies the same edit distance principles at the character level, and edge case tests ensure consistent behavior across various input conditions. This comprehensive testing framework demonstrates that the evaluation metrics are reproducible, deterministic, and based on predefined statistical functions—core characteristics of algorithmic evaluators designed to ensure consistent assessment through established computational measures.