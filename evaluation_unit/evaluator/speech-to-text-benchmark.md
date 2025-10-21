## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Word Error Rate and Punctuation Error Rate metric implementations
- File: `metric.py`
- Class: `WordErrorRate` class and `PunctuationErrorRate` class
- Code Reference:
```python
class WordErrorRate(Metric):
    def calculate(self, prediction: str, reference: str) -> Tuple[int, int]:
        pred_tokens = prediction.split()
        ref_tokens = reference.split()
        
        error_count = editdistance.eval(ref_tokens, pred_tokens)
        token_count = len(ref_tokens)
        
        return error_count, token_count
```
```python
class PunctuationErrorRate(Metric):
    @staticmethod
    def _compute_dp_matrix(reference: Sequence[str], prediction: Sequence[str]) -> NDArray:
        m, n = len(reference), len(prediction)
        dp = np.zeros((m + 1, n + 1), dtype=int)
        # ... dynamic programming implementation
```
This repository exclusively uses algorithmic metrics to evaluate speech-to-text engine outputs. The primary evaluators are Word Error Rate (WER) and Punctuation Error Rate (PER). WER is implemented in the `WordErrorRate` class, which calculates edit distance between predicted and reference word sequences using a deterministic, rule-based metric. PER is implemented in the `PunctuationErrorRate` class, which uses dynamic programming and backtracking to align punctuation between reference and prediction, providing a deterministic algorithmic approach based on mathematical formulas.

Evidence 2: Benchmark execution with algorithmic metric application
- File: `benchmark.py`
- Code Reference:
```python
metrics = {m: Metric.create(m) for m in metric_names}
results = {m: {"num_errors": 0, "num_tokens": 0} for m in metric_names}

for metric_name, metric in metrics.items():
    num_errors, num_tokens = metric.calculate(prediction=transcribed_sentence, reference=ref_sentence)
    results[metric_name]["num_errors"] += num_errors
    results[metric_name]["num_tokens"] += num_tokens
```
The benchmark applies these algorithmic metrics to evaluate model outputs on speech-to-text benchmarks. This demonstrates the practical application of deterministic evaluation functions that provide consistent, reproducible assessment through established computational measures.

Evidence 3: Latency measurement using algorithmic timing
- File: `benchmark_latency.py`
- Function: `compute_latencies()`
- Code Reference:
```python
def compute_latencies(...) -> Sequence[float]:
    latencies = []
    # ...
    for (send_time, receive_time), (ref_word, transcribed_word) in zip(aligned_timings, aligned_words):
        if ref_word != transcribed_word:
            continue
        latencies.append(receive_time - send_time)
    return latencies
```
This computes word emission latency through simple arithmetic operations on timestamps, providing another example of deterministic algorithmic evaluation that ensures reproducible performance assessment.

Evidence 4: Text normalization algorithms for preprocessing
- File: `normalizer.py`
- Class: `EnglishNormalizer`
- Code Reference:
```python
class EnglishNormalizer(Normalizer):
    def normalize(self, sentence: str, raise_error_on_invalid_sentence: bool = False) -> str:
        # ... algorithmic text transformations
        sentence = " ".join(num2txt(x) for x in sentence.split())
        # ... more rule-based transformations
```
While these are preprocessing functions, they support the algorithmic evaluation pipeline by applying rule-based text transformations that standardize inputs before evaluation, ensuring consistent and reproducible metric calculation.