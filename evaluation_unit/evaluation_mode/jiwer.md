## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Error Rate Calculation Functions
- File: `src/jiwer/measures.py`
- Functions: `wer()`, `mer()`, `wip()`, `wil()`, `cer()`
- Code Reference:
```python
# Functions compute error rates by comparing text strings
wer()  # Word Error Rate
mer()  # Match Error Rate
cer()  # Character Error Rate
```
These functions compute error rates by comparing reference and hypothesis text strings. They calculate metrics like Word Error Rate (WER), Match Error Rate (MER), Character Error Rate (CER), etc. by analyzing the textual differences between reference and hypothesis outputs without executing any code. The comparison is purely syntactic/structural analysis of text strings.

Evidence 2: Text Processing and Alignment
- File: `src/jiwer/process.py`
- Functions: `process_words()`, `process_characters()`
- Classes: `WordOutput`, `CharacterOutput`, `AlignmentChunk`
- Code Reference:
```python
process_words()      # Word-level alignment
process_characters() # Character-level alignment
rapidfuzz.distance.Levenshtein.opcodes()  # Edit distance operations
```
These functions perform Levenshtein distance calculations to align reference and hypothesis sentences at word or character level. They count substitutions, insertions, deletions, and hits through string comparison and pattern matching. The code uses `rapidfuzz.distance.Levenshtein.opcodes()` to compute edit distance operations, which is a static analysis technique that inspects string structure without execution.

Evidence 3: Alignment Visualization
- File: `src/jiwer/alignment.py`
- Functions: `visualize_alignment()`, `visualize_error_counts()`, `collect_error_counts()`
- Code Reference:
```python
visualize_alignment()    # Visual representation of alignment
visualize_error_counts() # Error frequency visualization
collect_error_counts()   # Build frequency dictionaries
```
These functions visualize and count errors by inspecting the alignment chunks between reference and hypothesis text. They perform frequency analysis of substitutions, insertions, and deletions, which is static pattern matching and counting on text outputs. For example, `collect_error_counts()` builds frequency dictionaries by iterating through alignment chunks without executing any model-generated code.

Evidence 4: Validation Tests
- File: `tests/test_measures.py`
- Functions: `test_input_ref_string_hyp_string()`, `test_known_values()`
- Code Reference:
```python
assert output.wer == 0.5  # checking calculated WER matches expected
assert output.hits == 50  # verifying hit count
```
The test suite validates the error rate calculations by comparing computed metrics against expected values. These assertions demonstrate static comparison of numerical results from text analysis.

Evidence 5: Text Transformations
- File: `src/jiwer/transforms.py`
- Classes: `RemovePunctuation`, `ToLowerCase`, `RemoveWhiteSpace`, `SubstituteWords`
- Code Reference:
```python
class RemovePunctuation(BaseRemoveTransform):
    # Filters out punctuation characters through string manipulation
```
These transformation classes perform syntactic preprocessing on text strings before comparison. They use regex patterns, string operations, and character filtering to normalize text. This is pure text structure manipulation without execution.

Evidence 6: Alignment Testing
- File: `tests/test_alignment.py`
- Functions: Test cases verifying alignment output format
- Code Reference:
```python
correct_alignment = """=== SENTENCE 1 ===
REF: this is a 
HYP: this is a test
              I
"""
alignment = jiwer.visualize_alignment(...)
self.assertEqual(alignment, correct_alignment)
```
Tests validate the alignment visualization output by comparing generated strings against expected patterns. This validates output structure through string comparison.