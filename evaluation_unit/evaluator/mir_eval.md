## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Weighted scoring algorithm for key detection
- File: `mir_eval/key.py`
- Function: `weighted_score()`
- Code Reference:
```python
def weighted_score(reference_key, estimated_key, allow_descending_fifths=False):
    """Compute a heuristic score which is weighted according to the
    relationship of the reference and estimated key, as follows:

    +------------------------------------------------------+-------+
    | Relationship                                         | Score |
    +------------------------------------------------------+-------+
    | Same key and mode                                    | 1.0   |
    +------------------------------------------------------+-------+
    | Estimated key is a perfect fifth above reference key | 0.5   |
    +------------------------------------------------------+-------+
    | Relative major/minor (same key signature)            | 0.3   |
    +------------------------------------------------------+-------+
    | Parallel major/minor (same key)                      | 0.2   |
    +------------------------------------------------------+-------+
    | Other                                                | 0.0   |
    +------------------------------------------------------+-------+
```
This implements a deterministic scoring algorithm for key detection based on musical theory relationships (perfect fifths, relative major/minor, parallel major/minor). The predefined scoring matrix ensures that all evaluations of key detection produce consistent, reproducible results based on established music theory principles, exemplifying the algorithmic evaluator category's goal of deterministic assessment.

Evidence 2: Precision, recall, and accuracy computation
- File: `mir_eval/multipitch.py`
- Functions: `compute_accuracy()`, `compute_err_score()`, `compute_num_true_positives()`
- Code Reference:
```python
def compute_accuracy(true_positives, n_ref, n_est):
    """Compute accuracy metrics.
    Returns
    -------
    precision : float
        ``sum(true_positives)/sum(n_est)``
    recall : float
        ``sum(true_positives)/sum(n_ref)``
    acc : float
        ``sum(true_positives)/sum(n_est + n_ref - true_positives)``
    """
    true_positive_sum = float(true_positives.sum())
    
    n_est_sum = n_est.sum()
    if n_est_sum > 0:
        precision = true_positive_sum / n_est.sum()
    else:
        precision = 0.0
    
    n_ref_sum = n_ref.sum()
    if n_ref_sum > 0:
        recall = true_positive_sum / n_ref.sum()
    else:
        recall = 0.0
```
These functions implement standard precision/recall/accuracy calculations and error scoring metrics using well-established statistical formulas. The mathematical definitions are fixed and deterministic, producing identical results for the same inputs across all runs, which fulfills the algorithmic evaluator's requirement for consistent and reproducible evaluation through established computational measures.

Evidence 3: Test framework for algorithmic metric validation
- File: `tests/test_beat.py`
- Code Reference:
```python
@pytest.fixture
def beat_data(request):
    ref_f, est_f, sco_f = request.param
    with open(sco_f) as f:
        expected_scores = json.load(f)
    reference_beats = mir_eval.io.load_events(ref_f)
    estimated_beats = mir_eval.io.load_events(est_f)
    return reference_beats, estimated_beats, expected_scores
```
Tests load reference data, estimated data, and expected scores from JSON files to compute algorithmic metrics. This testing infrastructure demonstrates the deterministic nature of the evaluation system, where pre-computed expected values can be reliably compared against runtime calculations, confirming that the metrics are algorithmic rather than learned or stochastic.

Evidence 4: Verification of deterministic metric computation
- File: `tests/test_beat.py`
- Code Reference:
```python
@pytest.mark.parametrize("beat_data", file_sets, indirect=True)
def test_beat_functions(beat_data):
    reference_beats, estimated_beats, expected_scores = beat_data

    # Compute scores
    scores = mir_eval.beat.evaluate(reference_beats, estimated_beats)
    # Compare them
    assert scores.keys() == expected_scores.keys()
    for metric in scores:
        assert np.allclose(scores[metric], expected_scores[metric], atol=A_TOL)
```
Tests verify that algorithmic metrics are correctly computed by comparing against pre-computed expected values using numerical tolerance checks. The ability to assert exact matches (within floating-point tolerance) between computed and expected scores confirms the deterministic and reproducible nature of these algorithmic evaluators, as they consistently produce the same results for identical inputs.

Evidence 5: Comprehensive coverage of MIR algorithmic metrics
- Files: Multiple test files across the repository
- Code Reference:
```
tests/test_tempo.py - Tempo detection metrics (F-measure, accuracy)
tests/test_melody.py - Pitch accuracy, voicing recall/precision
tests/test_chord.py - Chord recognition accuracy with various comparison functions
tests/test_segment.py - Segmentation precision/recall/F-measure
tests/test_onset.py - Onset detection F-measure
tests/test_transcription.py - Note transcription precision/recall
tests/test_pattern.py - Pattern discovery metrics (FPR)
tests/test_hierarchy.py - Hierarchical segmentation metrics
tests/test_separation.py - Source separation metrics (BSS eval)
tests/test_alignment.py - Alignment error metrics
```
The test files demonstrate evaluation of various MIR tasks using algorithmic metrics across diverse musical domains. Each test file implements deterministic mathematical functions and statistical metrics specific to its domain, collectively establishing that the entire harness operates exclusively through predefined computational measures rather than learned models or human judgment.

Evidence 6: Explicit documentation of algorithmic nature
- File: `README.rst`
- Code Reference:
```rst
mir_eval
========

Python library for computing common heuristic accuracy scores for various 
music/audio information retrieval/signal processing tasks.
```
The repository explicitly describes itself as computing "common heuristic accuracy scores," directly confirming its algorithmic nature. The use of "heuristic accuracy scores" indicates predefined computational formulas rather than learned or adaptive evaluation methods, aligning perfectly with the algorithmic evaluator definition of providing deterministic assessment through established computational measures.