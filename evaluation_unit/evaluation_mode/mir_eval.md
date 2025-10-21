## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text/Label Comparison
- File: `mir_eval/key.py`
- Function: `weighted_score()`
- Code Reference:
```python
def weighted_score(reference_key, estimated_key, allow_descending_fifths=False):
    """Compute a heuristic score which is weighted according to the
    relationship of the reference and estimated key..."""
    validate(reference_key, estimated_key)
    reference_key, reference_mode = split_key_string(reference_key)
    estimated_key, estimated_mode = split_key_string(estimated_key)
    # If keys are the same, return 1.
    if reference_key == estimated_key and reference_mode == estimated_mode:
        return 1.0
    # ... further string comparisons
```
This function compares two key strings (e.g., "C# major") by parsing and comparing their components without any execution. It performs pattern matching and string-based validation to compute a similarity score.

Evidence 2: Interval/Event Validation
- File: `mir_eval/util.py`
- Function: `validate_intervals()`
- Code Reference:
```python
def test_validate_intervals(intervals):
    mir_eval.util.validate_intervals(intervals)
```
The validation functions check structural properties of model outputs (intervals, events, frequencies) through inspection - checking array shapes, value ranges, sortedness - without executing any generated code.

Evidence 3: Chord Label Format Validation
- File: `mir_eval/chord.py`
- Function: `validate_chord_label()`
- Code Reference:
```python
def validate_chord_label(label):
    """Check that a key is well-formatted, e.g. in the form ``'C# major'``.
    The Key can be 'X' if it is not possible to categorize the Key and mode
    can be 'other' if it can't be categorized as major or minor."""
    if len(key.split()) != 2 and not (len(key.split()) and key.lower() == 'x'):
        raise ValueError("'{}' is not in the form '(key) (mode)' or 'X'".format(key))
```
This validates the syntactic structure of chord labels by parsing and checking format compliance without execution.

Evidence 4: Frequency/Pitch Comparison
- File: `mir_eval/melody.py`
- Functions: `hz2cents()`, `freq_to_voicing()`
- Code Reference:
```python
def test_hz2cents():
    # Unit test some simple values
    hz = np.array([0.0, 10.0, 5.0, 320.0, 1420.31238974231])
    # Expected cent conversion
    expected_cent = np.array([0.0, 0.0, -1200.0, 6000.0, 8580.0773605])
    assert np.allclose(mir_eval.melody.hz2cents(hz), expected_cent)
```
These functions perform mathematical transformations and comparisons on model-generated frequency values through inspection and calculation, not execution.

Evidence 5: Interval Overlap Calculation
- File: `mir_eval/segment.py`
- Code Reference:
```python
def test_segment_boundary_detection_perfect():
    correct_intervals = np.array([[0, 1], [1, 2]])
    assert np.allclose(
        mir_eval.segment.detection(correct_intervals, correct_intervals), 1
    )
```
The detection function analyzes the temporal structure of segment intervals by computing overlaps and boundaries without executing generated content.

Evidence 6: Bipartite Matching for Alignment
- File: `mir_eval/util.py`
- Function: `_bipartite_match()`
- Code Reference:
```python
def test_bipartite_match():
    # This test constructs a graph as follows:
    #   v9 -- (u0)
    #   v8 -- (u0, u1)
    #   v7 -- (u0, u1, u2)
    # ...
    matching = util._bipartite_match(G)
```
This function performs graph matching on model outputs to find optimal alignments through algorithmic analysis, not execution.

Evidence 7: Note/Event Matching
- File: `mir_eval/transcription.py`
- Functions: `match_notes()`, `match_note_onsets()`
- Code Reference:
```python
def test_match_notes():
    ref_int, ref_pitch = REF[:, :2], REF[:, 2]
    est_int, est_pitch = EST[:, :2], EST[:, 2]
    
    matching = mir_eval.transcription.match_notes(
        ref_int, ref_pitch, est_int, est_pitch
    )
    
    assert matching == [(0, 0), (3, 3)]
```
These functions compare note intervals and pitches from model outputs by analyzing their temporal and frequency properties, without executing any code.

Evidence 8: Pattern Matching in Patterns
- File: `mir_eval/pattern.py`
- Code Reference:
```python
@pytest.mark.parametrize(
    "metric",
    [
        mir_eval.pattern.standard_FPR,
        mir_eval.pattern.establishment_FPR,
        mir_eval.pattern.occurrence_FPR,
        mir_eval.pattern.three_layer_FPR,
    ],
)
def test_pattern_perfect(metric):
    # Valid patterns which are the same produce a score of 1 for all metrics
    patterns = [[[(100, 20), (200, 30)]]]
    assert np.allclose(metric(patterns, patterns), 1)
```
Pattern discovery metrics analyze sequences of (onset, pitch) tuples by comparing their structural properties through inspection.

Evidence 9: Chord Quality Bitmap Conversion
- File: `mir_eval/chord.py`
- Function: `quality_to_bitmap()`
- Code Reference:
```python
def test_quality_to_bitmap():
    # Test simple case
    assert np.all(
        mir_eval.chord.quality_to_bitmap("maj")
        == np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    )
```
This function converts chord quality strings to binary representations through parsing and lookup, performing syntactic analysis on model outputs.

Evidence 10: Hierarchy Comparison
- File: `mir_eval/hierarchy.py`
- Code Reference:
```python
@pytest.mark.parametrize("window", [5, 10, 15, 30, 90, None])
@pytest.mark.parametrize("frame_size", [0.1, 0.5, 1.0])
def test_tmeasure_pass(window, frame_size):
    ref = [[[0, 30]], [[0, 15], [15, 30]]]
    ref = [np.asarray(_) for _ in ref]
    est = ref[:1]
    
    scores = mir_eval.hierarchy.tmeasure(ref, est, window=window, frame_size=frame_size)
```
Hierarchy metrics analyze the structure of nested interval annotations by comparing their alignment and overlap without execution.