# Picovoice/speech-to-text-benchmark - Stage 4 (EVALUATE) Evaluation

## Summary
This is a specialized speech-to-text benchmarking framework, not a general-purpose LLM evaluation framework. It computes Word Error Rate (WER) and Punctuation Error Rate (PER) metrics for audio transcription models. While it has solid metric computation for its narrow domain (speech-to-text), it lacks most features expected of a general LLM evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Limited text normalization exists but no validation/policy checks. `normalizer.py` provides text normalization (removing symbols, handling diacritics, converting numbers) but no format validation, schema checking, or policy compliance features. No malformed output detection or sanity checks. |
| S4F2: Metric Computation | 1 | Only 2 metrics: WER and PER for speech-to-text (`metric.py` lines 13-15). No support for general text generation, classification, retrieval, or safety metrics. Per-sample scoring exists via `calculate()` method but extremely limited coverage. Not extensible beyond these two metrics. |
| S4F3: Evaluator Models | 0 | No LLM-as-judge, no evaluator model integration, no ensemble scoring. Framework only calls speech-to-text engines and compares against ground truth transcripts. `engine.py` contains STT engine wrappers, not evaluator models. |
| S4F4: Multi-Modal Scoring | 1 | Audio-only framework with WER metric (`metric.py` WordErrorRate class). No vision-language, video, or cross-modal capabilities. While it handles audio input, it only evaluates text output quality, not audio quality metrics like MOS or audio-specific features. |
| S4F5: Aggregate Statistics | 1 | Only basic mean calculation. `benchmark.py` lines 163-166 compute simple error rates: `error_rate = 100 * float(num_errors) / num_tokens`. `plot_results.py` generates bar charts of averages. No percentiles, confidence intervals, significance testing, or ranking systems. Results are aggregated manually in `results.py` as hardcoded dictionaries. |

## Detailed Analysis

### S4F1: Output Validation and Normalization (1 point)

Evidence:
- `normalizer.py` contains normalization logic but no validation:
  - Lines 39-67 (DefaultNormalizer): Removes diacritics, symbols, handles punctuation
  - Lines 103-145 (EnglishNormalizer): American spelling conversion, abbreviation handling, number-to-text
  - No checks for malformed outputs, empty transcripts, or anomalies

```python
# normalizer.py lines 92-98
def normalize(self, sentence: str, raise_error_on_invalid_sentence: bool = False) -> str:
    # Only raises error if explicitly requested and invalid characters found
    if raise_error_on_invalid_sentence:
        if not all(c in valid_characters + string.ascii_lowercase for c in sentence):
            raise RuntimeError()
```

Missing:
- No format validation (JSON, XML schemas)
- No policy compliance checks (toxicity, harmful content)
- No length constraints or sanity checks
- No handling of partial/truncated outputs

### S4F2: Task-Specific Metric Computation (1 point)

Evidence:
- Only 2 metrics defined in `metric.py`:
  - WordErrorRate (lines 26-34): Edit distance between transcripts
  - PunctuationErrorRate (lines 37-132): Punctuation-specific errors

```python
# metric.py lines 13-25
class Metrics(Enum):
    WER = "WER"
    PER = "PER"

@classmethod
def create(cls, x: Metrics):
    if x is Metrics.WER:
        return WordErrorRate()
    elif x is Metrics.PER:
        return PunctuationErrorRate()
```

Missing:
- No BLEU, ROUGE, METEOR, BERTScore for general text
- No classification metrics (accuracy, F1, AUC)
- No retrieval metrics (NDCG, MRR, MAP)
- No safety metrics (toxicity, bias)
- No extensibility mechanism for custom metrics

### S4F3: Evaluator Model Integration (0 points)

Evidence:
- `engine.py` contains only speech-to-text engines (Whisper, Amazon Transcribe, etc.)
- No evaluator models, LLM judges, or scoring models
- Framework compares transcripts to ground truth using edit distance only

```python
# benchmark.py lines 54-65
transcript = engine.transcribe(audio_path)
norm_transcript = normalizer.normalize(transcript)
# Direct comparison, no evaluator model
for metric_name, metric in metrics.items():
    num_errors, num_tokens = metric.calculate(
        prediction=transcribed_sentence, 
        reference=ref_sentence
    )
```

Missing:
- No LLM-as-judge functionality
- No pre-built judge prompts or configurable criteria
- No ensemble scoring or disagreement handling
- No rationale capture

### S4F4: Multi-Modal Scoring Protocols (1 point)

Evidence:
- Framework processes audio files but only evaluates text transcription quality
- `dataset.py` loads audio files (FLAC, WAV) but only for STT input
- No audio quality metrics, only text error rates

```python
# dataset.py lines 105-115
mp3_path = os.path.join(folder, "clips", row["path"])
flac_path = mp3_path.replace(".mp3", ".flac")
# Audio converted but only used as STT input
```

Missing:
- No image captioning metrics (CIDEr, SPICE)
- No VQA accuracy
- No text-to-image alignment (CLIP score)
- No TTS quality metrics (MOS)
- No cross-modal retrieval support

### S4F5: Aggregate Statistics and Cross-Model Comparison (1 point)

Evidence:
- Only basic mean calculation in `benchmark.py`:

```python
# benchmark.py lines 163-166
num_errors = sum(x.num_errors for x in metric_results)
num_tokens = sum(x.num_tokens for x in metric_results)
error_rate = 100 * float(num_errors) / num_tokens
```

- Results hardcoded in `results.py` as dictionaries (lines 11-642)
- `plot_results.py` generates simple bar charts of averages (lines 60-93)

```python
# plot_results.py lines 71-79
sorted_error_rates = sorted([
    (e, round(sum(w for w in engine_error_rate[e].values()) / 
              len(engine_error_rate[e]) + 1e-9, 1))
    for e in engine_error_rate.keys()
], key=lambda x: x[1])
```

Missing:
- No percentiles, standard deviation, variance
- No confidence intervals
- No statistical significance testing (t-test, Wilcoxon)
- No bootstrap or permutation tests
- No ranking systems (Elo, TrueSkill)
- No stratified statistics or sample weighting

## Strengths
1. Domain-specific implementation: Well-implemented for speech-to-text benchmarking
2. Per-sample scoring: Can compute WER/PER per audio file
3. Normalization: Robust text normalization for multiple languages
4. Parallel processing: Uses ProcessPoolExecutor for efficient batch processing

## Limitations
1. Not an LLM evaluation framework: Purpose-built for speech-to-text only
2. Minimal metric coverage: Only 2 metrics vs dozens needed for general LLM eval
3. No evaluator models: No LLM-as-judge or model-based scoring
4. Basic statistics only: No advanced statistical analysis or comparison features
5. No extensibility: Hard to add new metrics or domains

## Overall Assessment
This repository scores 4/15 for Stage 4 (EVALUATE). While it successfully benchmarks speech-to-text systems with appropriate metrics for that domain, it is fundamentally not designed as a general LLM evaluation framework. It lacks most features needed for comprehensive model evaluation (diverse metrics, evaluator models, advanced statistics, multi-modal support beyond audio→text). The framework would require a complete redesign to serve as a general-purpose LLM evaluation harness.