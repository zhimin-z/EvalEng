## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text comparison and error calculation
- File: `metric.py`
- Class/Function: `WordErrorRate.calculate()`, `PunctuationErrorRate.calculate()`
- Code Reference:
```python
def calculate(self, prediction: str, reference: str) -> Tuple[int, int]:
    pred_tokens = prediction.split()
    ref_tokens = reference.split()
    
    error_count = editdistance.eval(ref_tokens, pred_tokens)
    token_count = len(ref_tokens)
    
    return error_count, token_count
```
The harness performs static analysis of speech-to-text model outputs by comparing predicted transcriptions against reference transcripts without executing any generated artifacts. The Word Error Rate calculation performs direct text comparison using edit distance without executing any code. The Punctuation Error Rate calculation uses dynamic programming and backtracking to align predicted and reference punctuation marks, calculating insertion/deletion/substitution errors through purely syntactic analysis of text structure.

Evidence 2: Text normalization and validation
- File: `normalizer.py`
- Class/Function: `EnglishNormalizer.normalize()`, `DefaultNormalizer._remove_symbols_and_diacritics()`
- Code Reference:
```python
if raise_error_on_invalid_sentence:
    valid_characters = " '" + self._punctuation_set if self._keep_punctuation else " '"
    if not all(c in valid_characters + string.ascii_lowercase for c in sentence):
        raise RuntimeError()
```
The normalizers perform format validation and structural transformation on model outputs. Text structure validation checks the syntactic structure of transcribed text against valid character sets. The normalizers apply regex patterns and character replacements to standardize output format, including punctuation removal, number-to-word conversion, and abbreviation normalization (lines 185-246).

Evidence 3: Main evaluation workflow
- File: `benchmark.py`
- Function: `process()`
- Code Reference:
```python
transcript = engine.transcribe(audio_path)
norm_transcript = normalizer.normalize(transcript)

ref_sentence = ref_transcript.strip("\n ").lower()
transcribed_sentence = norm_transcript.strip("\n ").lower()

# Text comparison for American English
if language == Languages.EN:
    ref_sentence = EnglishNormalizer.to_american(...)
    transcribed_sentence = EnglishNormalizer.to_american(...)

# Calculate metrics using string comparison
for metric_name, metric in metrics.items():
    num_errors, num_tokens = metric.calculate(
        prediction=transcribed_sentence, 
        reference=ref_sentence
    )
```
The main benchmarking process demonstrates pure static analysis through a workflow of loading model transcriptions, normalizing them, and comparing them with reference transcripts. The process loads text outputs, normalizes format, and computes error metrics through string comparison without any code execution.

Evidence 4: Alignment analysis
- File: `benchmark_latency.py`
- Class/Function: `Aligner.align_words()`, `Aligner.align_timings()`
- Code Reference:
```python
def align_words(self, ref_words: Sequence[str], pred_words: Sequence[str], ...):
    dp = self._compute_edit_distance_matrix(ref_words, pred_words)
    # ... backtracking to find optimal alignment ...
    all_alignments = backtrack(len(ref_words), len(pred_words))
    best_alignment = max(all_alignments, key=lambda x: x[1])[0]
    return best_alignment
```
The latency benchmark includes an alignment component that performs syntactic analysis of word sequences. This computes optimal word-level alignments using edit distance and dynamic programming backtracking without executing any model-generated code.

Evidence 5: Results visualization
- File: `plot_results.py`
- Function: `_plot_error_rate()`, `_plot_cpu()`, `_plot_latency()`
The plotting module reads pre-computed metrics and visualizes them. While this is post-processing of benchmark results rather than evaluation itself, it demonstrates that the harness's output is static metric data (error rates, latency values) that gets analyzed and visualized without any code execution.