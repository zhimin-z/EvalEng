## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Tempo Reference Data Loading
- File: `tests/test_tempo.py`
- Code Reference: Test data file loading (Lines 19-28)
```python
REF_GLOB = "data/tempo/ref*.lab"
EST_GLOB = "data/tempo/est*.lab"
SCORES_GLOB = "data/tempo/output*.json"

ref_files = sorted(glob.glob(REF_GLOB))
est_files = sorted(glob.glob(EST_GLOB))
sco_files = sorted(glob.glob(SCORES_GLOB))
```
Loads reference labels (`ref*.lab`) and expected scores (`output*.json`) as ground truth for tempo evaluation. These files contain predetermined annotations serving as explicit comparison standards.

Evidence 2: Melody Reference Annotations
- File: `tests/test_melody.py`
- Code Reference: Reference data loading pattern (Lines 18-24)
```python
REF_GLOB = "data/melody/ref*.txt"
EST_GLOB = "data/melody/est*.txt"
SCORES_GLOB = "data/melody/output*.json"

ref_files = sorted(glob.glob(REF_GLOB))
est_files = sorted(glob.glob(EST_GLOB))
sco_files = sorted(glob.glob(SCORES_GLOB))
```
Pattern of loading reference annotations for melody evaluation. The reference files contain gold standard melody annotations used for comparing against model outputs.

Evidence 3: Key Detection Ground Truth
- File: `tests/test_key.py`
- Code Reference: Ground truth comparison in tests (Lines 65-72)
```python
@pytest.fixture
def key_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    reference_key = mir_eval.io.load_key(ref_f)
    estimated_key = mir_eval.io.load_key(est_f)
```
Loads reference key annotations as ground truth labels. These annotations provide explicit standards for evaluating key detection outputs against predetermined correct answers.

Evidence 4: Key Label Format Validation
- File: `mir_eval/key.py`
- Code Reference: Explicit label validation (Lines 37-58)
```python
def validate_key(key):
    """Check that a key is well-formatted, e.g. in the form ``'C# major'``.
    The Key can be 'X' if it is not possible to categorize the Key and mode
    can be 'other' if it can't be categorized as major or minor.
    """
    if len(key.split()) != 2 and not (len(key.split()) and key.lower() == "x"):
        raise ValueError("'{}' is not in the form '(key) (mode)' " "or 'X'".format(key))
```
Validates reference label format for key annotations. This ensures explicit labels conform to expected formats before use as comparison standards.

Evidence 5: Segment Interval Labels
- File: `tests/test_segment.py`
- Code Reference: Reference intervals and labels (Lines 23-34)
```python
@pytest.fixture
def segment_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    # Load in an example segmentation annotation
    ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(ref_f)
    # Load in an example segmentation tracker output
    est_intervals, est_labels = mir_eval.io.load_labeled_intervals(est_f)
```
Loads reference intervals and labels as ground truth for segmentation evaluation. These labeled intervals serve as explicit standards for comparing model-generated segment boundaries.

Evidence 6: Chord Reference Annotations
- File: `tests/test_chord.py`
- Code Reference: Chord reference labels (Lines 25-35)
```python
@pytest.fixture
def chord_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    # Load in reference melody
    ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals(ref_f)
    # Load in estimated melody
    est_intervals, est_labels = mir_eval.io.load_labeled_intervals(est_f)
```
Loads chord reference labels from files providing ground truth chord progressions. These explicit annotations enable comparison of estimated chord sequences against predetermined correct labels.

Evidence 7: Transcription Pitch References
- File: `tests/test_transcription.py`
- Code Reference: Reference pitches (Lines 22-34)
```python
@pytest.fixture
def transcription_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    # Load in an example segmentation annotation
    ref_int, ref_pitch = mir_eval.io.load_valued_intervals(ref_f)
    # Load in estimated transcription
    est_int, est_pitch = mir_eval.io.load_valued_intervals(est_f)
```
Loads reference pitch annotations for transcription tasks. These valued intervals provide explicit ground truth pitch values for evaluating transcription accuracy.

Evidence 8: Beat Event Timestamps
- File: `tests/test_beat.py`
- Code Reference: Beat reference events (Lines 19-29)
```python
@pytest.fixture
def beat_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    reference_beats = mir_eval.io.load_events(ref_f)
    estimated_beats = mir_eval.io.load_events(est_f)
```
Loads reference beat event timestamps as ground truth for beat tracking evaluation. These explicit temporal annotations serve as comparison standards for estimated beat locations.

Evidence 9: Pattern Discovery References
- File: `tests/test_pattern.py`
- Code Reference: Pattern reference annotations (Lines 22-31)
```python
@pytest.fixture
def pattern_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    reference_patterns = mir_eval.io.load_patterns(ref_f)
    estimated_patterns = mir_eval.io.load_patterns(est_f)
```
Loads reference pattern annotations providing ground truth for pattern discovery tasks. These explicit pattern labels enable evaluation of discovered patterns against predetermined correct instances.

Evidence 10: Expected Score Validation
- File: `tests/test_tempo.py`
- Code Reference: Score comparison against expected values (Lines 105-110)
```python
def test_tempo_regression(tempo_data):
    ref_tempi, ref_weight, est_tempi, expected_scores = tempo_data
    
    scores = mir_eval.tempo.evaluate(ref_tempi, ref_weight, est_tempi)
    assert scores.keys() == expected_scores.keys()
    for metric in scores:
        assert np.allclose(scores[metric], expected_scores[metric], atol=A_TOL)
```
Compares computed scores against pre-computed expected scores stored in JSON files. These expected scores serve as explicit reference standards for validating metric computation correctness.