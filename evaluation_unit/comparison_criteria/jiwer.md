## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Metric Value Test Cases
- File: `tests/test_measures.py`
- Code Reference: Test functions with expected metric values
```python
def test_input_ref_string_hyp_string(self):
    cases = [
        ("This is a test", "This is a test", all_m(0, 0, 0)),
        ("This is a test", "", all_m(1, 1, 1)),
        ("This is a test", "This test", all_m(0.5, 0.5, 0.5)),
    ]
```
Each test case specifies exact expected metric values (WER, MER, WIP, WIL) that the system's output must match. The third element in each tuple represents predetermined correct measures serving as ground truth for validation.

Evidence 2: Academic Reference Values
- File: `tests/test_measures.py`
- Code Reference: Known values from academic papers
```python
def test_known_values(self):
    # Taken from the "From WER and RIL to MER and WIL" paper
    cases = [
        ("X", "X", all_m(0, 0, 0)),
        ("X", "X X Y Y", all_m(3, 0.75, 0.75)),
        ("X Y X", "X Z", all_m(2 / 3, 2 / 3, 5 / 6)),
    ]
```
Test cases derived from academic papers provide mathematically verified reference values. These gold standard answers from published research serve as explicit labels for validating metric computations.

Evidence 3: Character Error Rate Cases
- File: `tests/test_cer.py`
- Code Reference: CER test cases with expected values
```python
def test_input_ref_string_hyp_string(self):
    cases = [
        ("This is a test", "This is a test", 0 / 14),
        ("This is a test", "", 14 / 14),
        ("This is a test", "This test", 5 / 14),
    ]
```
Hardcoded expected character error rates serve as explicit labels for validation. Each test pair includes predetermined correct CER values that computed metrics must match exactly.

Evidence 4: Alignment Visualization References
- File: `tests/test_alignment.py`
- Code Reference: Expected alignment string outputs
```python
def test_insertion(self):
    correct_alignment = """=== SENTENCE 1 ===

REF: this is a ****
HYP: this is a test
                  I
"""
    alignment = jiwer.visualize_alignment(
        jiwer.process_words("this is a", "this is a test"), show_measures=False
    )
    self.assertEqual(alignment, correct_alignment)
```
Static reference strings define expected alignment visualizations. These predetermined correct outputs serve as explicit labels for validating alignment computation and formatting.

Evidence 5: Error Count Visualizations
- File: `tests/test_count_errors.py`
- Code Reference: Expected error count visualizations
```python
def test_count_word_errors():
    correct = """=== SUBSTITUTIONS ===
sub --> bus = 3x
sub --> usb = 1x
sub --> bsu = 1x

=== INSERTIONS ===
ins = 1x

=== DELETIONS ===
del = 1x"""
    actual = jiwer.visualize_error_counts(jiwer.process_words(ref, hyp))
    assert correct == actual
```
Hardcoded correct error count summaries provide explicit reference standards. These static expected outputs serve as ground truth for validating error analysis computations.

Evidence 6: Edge Case Expected Values
- File: `tests/test_empty_ref.py`
- Code Reference: Edge case tests with explicit expected metrics
```python
def test_empty_ref_empty_hyp():
    out = jiwer.process_words(reference=ref, hypothesis=hyp)
    assert out.hits == 0
    assert out.deletions == 0
    assert out.insertions == 0
    assert out.substitutions == 0
    assert out.wer == 0
    assert out.mer == 0
    assert out.wip == 1
    assert out.wil == 0
```
Comprehensive explicit metric values for edge cases serve as ground truth labels. Tests validate that specific input conditions produce exact predetermined metric values through direct equality assertions.