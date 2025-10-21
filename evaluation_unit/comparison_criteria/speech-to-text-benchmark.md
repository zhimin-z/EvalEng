## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: CommonVoice Dataset Transcripts
- File: `dataset.py`
- Code Reference: `CommonVoiceDataset.__init__()` (Lines 107-130)
```python
with open(os.path.join(folder, "test.tsv")) as f:
    reader: csv.DictReader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        # ... process audio
        transcript = normalizer.normalize(row["sentence"], raise_error_on_invalid_sentence=True)
        self._data.append((flac_path, transcript))
```
Loads audio paths paired with reference transcripts from `test.tsv`. The normalized transcripts serve as ground truth labels for evaluating speech-to-text model outputs.

Evidence 2: LibriSpeech Reference Loading
- File: `dataset.py`
- Code Reference: `LibriSpeechTestCleanDataset.__init__()` (Lines 148-165)
```python
with open(os.path.join(chapter_folder, f"{speaker_id}-{chapter_id}.trans.txt"), "r") as f:
    transcripts = dict(x.split(" ", maxsplit=1) for x in f.readlines())
```
Loads reference transcripts from `.trans.txt` files, creating explicit ground truth labels paired with audio samples for benchmark evaluation.

Evidence 3: Multi-Dataset Ground Truth
- File: `dataset.py`
- Code Reference: Multiple dataset classes (Lines 187-401)
- `TEDLIUMDataset.__init__()`: Loads reference transcripts from `.stm` caption files
- `MLSDataset.__init__()`: Loads reference transcripts from `transcripts.txt`
- `VoxPopuliDataset.__init__()`: Loads reference transcripts from `asr_test.tsv`
- `FleursDataset.__init__()`: Loads reference transcripts from `test.tsv`

Each dataset class loads audio files paired with their correct transcriptions, providing static reference labels across multiple benchmark datasets for objective speech recognition assessment.

Evidence 4: Reference-Based Evaluation
- File: `benchmark.py`
- Code Reference: `process()` function (Lines 41-75)
```python
for index in indices:
    audio_path, ref_transcript = dataset.get(index)
    transcript = engine.transcribe(audio_path)
    norm_transcript = normalizer.normalize(transcript)
    
    ref_sentence = ref_transcript.strip("\n ").lower()
    transcribed_sentence = norm_transcript.strip("\n ").lower()
    
    # Calculate metrics by comparing prediction to reference
    for metric_name, metric in metrics.items():
        num_errors, num_tokens = metric.calculate(prediction=transcribed_sentence, reference=ref_sentence)
```
Compares model outputs against reference transcripts loaded from datasets. The evaluation explicitly uses ground truth labels to calculate error metrics by comparing predictions to reference sentences.

Evidence 5: Word Error Rate Calculation
- File: `metric.py`
- Code Reference: `WordErrorRate.calculate()` (Lines 32-38)
```python
def calculate(self, prediction: str, reference: str) -> Tuple[int, int]:
    pred_tokens = prediction.split()
    ref_tokens = reference.split()
    error_count = editdistance.eval(ref_tokens, pred_tokens)
    token_count = len(ref_tokens)
    return error_count, token_count
```
Directly compares predicted tokens to reference tokens using edit distance. This metric explicitly requires reference labels to compute error rates by measuring differences from ground truth.

Evidence 6: Punctuation Error Rate
- File: `metric.py`
- Code Reference: `PunctuationErrorRate.calculate()` (Lines 95-108)
Compares predicted punctuation to reference punctuation, using explicit ground truth labels to evaluate punctuation accuracy in transcriptions.

---

### None

Evidence 1: Real-Time Factor Computation
- File: `benchmark.py`
- Code Reference: RTF calculation (Lines 172-174)
```python
rtf = sum(x.process_sec for x in results) / sum(x.audio_sec for x in results)
```
RTF is calculated from processing time and audio duration without external references. This intrinsic metric measures computational efficiency by comparing processing speed to audio length.

Evidence 2: Engine Performance Tracking
- File: `engine.py`
- Code Reference: Base Engine class (Lines 50-56)
```python
def audio_sec(self) -> float:
    raise NotImplementedError()

def process_sec(self) -> float:
    raise NotImplementedError()
```
- Code Reference: Whisper implementation (Lines 895-901)
```python
start_sec = time.time()
res = self._model.transcribe(path, language=self._language_code)["text"]
self._proc_sec += time.time() - start_sec
```
Abstract methods and implementations track intrinsic performance metrics like audio duration and processing time. These reference-free measures assess engine efficiency without comparing to external standards.

Evidence 3: Word Emission Latency
- File: `benchmark_latency.py`
- Code Reference: `compute_latencies()` function (Lines 104-137)
```python
def compute_latencies(engine_name: Engines, engine_params: Dict[str, Any], 
                     language: Languages, examples: Sequence[Example]) -> Sequence[float]:
    # ...
    for example in examples:
        transcribed_words, receive_timings, send_timings = engine.measure_word_latency(audio_path, alignments)
        # ...
        for (send_time, receive_time), (ref_word, transcribed_word) in zip(aligned_timings, aligned_words):
            if ref_word != transcribed_word:
                continue
            latencies.append(receive_time - send_time)  # Intrinsic timing measure
```
Computes latency based on timing differences without external references. This intrinsic metric measures responsiveness by calculating time delays between speaking and transcription emission.

Evidence 4: Efficiency Metrics Storage
- File: `results.py`
- Code Reference: RTF dictionary (Lines 1-12)
```python
RTF = {
    Engines.PICOVOICE_LEOPARD: {
        Datasets.TED_LIUM: 0.042,
    },
    # ...
}
```
- Code Reference: Latency dictionary (Lines 14-26)
```python
LATENCIES = {
    Engines.AZURE_SPEECH_TO_TEXT_REAL_TIME: {
        Datasets.LIBRI_SPEECH_TEST_CLEAN: 530,
    },
    # ...
}
```
Stores reference-free computational efficiency and latency metrics. These dictionaries capture intrinsic performance properties (processing speed, responsiveness) without requiring comparison to ground truth or baseline standards.