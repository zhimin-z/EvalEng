## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Mathematical Conversion Task Generation
- File: `llm_correctness.py`
- Code Reference: Task generation (Lines 65-68)
```python
rnd_number = random.randint(0, MAX_RANDOM_NUMBER)
rnd_num_words = num2words.num2words(rnd_number)
prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."
```
The harness generates mathematical conversion tasks with predetermined correct answers serving as ground truth labels. Random numbers are generated and their word representations are used as prompts, with the original numbers serving as explicit reference answers.

Evidence 2: Ground Truth Storage
- File: `llm_correctness.py`
- Code Reference: Metadata storage (Lines 75-76)
```python
request_config = RequestConfig(
    ...
    metadata={"rnd_number": rnd_number},
    ...
)
```
The random number (`rnd_number`) is stored as metadata in the request configuration, serving as the explicit label for validation. This predetermined correct answer is preserved for comparison against model outputs.

Evidence 3: Direct Answer Validation
- File: `llm_correctness.py`
- Code Reference: Result validation logic (Lines 105-117)
```python
if not metrics[common_metrics.ERROR_CODE]:
    try:
        commas_between_numbers_re = r"(\d+),(?=\d)"
        gen_text_commas_removed = re.sub(
            commas_between_numbers_re, r"\1", generated_text
        )
        nums = re.findall(r"\d+", gen_text_commas_removed)
        generated_text = gen_text_commas_removed.replace("\n", " ")
        
        assert str(completed_request_config.metadata["rnd_number"]) in nums
    except:
        num_mismatched_requests += 1
```
Validation compares model outputs directly against predetermined correct answers through assertion-based matching. The harness extracts numbers from generated text and verifies the presence of the expected ground truth value.

---

### None

Evidence 1: Performance Metric Definitions
- File: `src/llmperf/common_metrics.py`
- Code Reference: Metric definitions (Lines 1-18)
```python
INTER_TOKEN_LAT = "inter_token_latency_s"  # Inference efficiency
TTFT = "ttft_s"  # Time to first token
E2E_LAT = "end_to_end_latency_s"  # Total latency
REQ_OUTPUT_THROUGHPUT = "request_output_throughput_token_per_s"  # Throughput
```
Defines reference-free intrinsic quality metrics assessing model output properties without external references. These metrics measure performance characteristics like latency and throughput as inherent operational properties.

Evidence 2: Throughput and Latency Computation
- File: `token_benchmark_ray.py`
- Code Reference: `get_token_throughput_latencies()` function (Lines 97-105)
```python
request_metrics[common_metrics.INTER_TOKEN_LAT] /= request_metrics[common_metrics.NUM_OUTPUT_TOKENS]
request_metrics[common_metrics.NUM_OUTPUT_TOKENS] = num_output_tokens
request_metrics[common_metrics.NUM_TOTAL_TOKENS] = request_metrics[common_metrics.NUM_INPUT_TOKENS] + num_output_tokens
request_metrics[common_metrics.REQ_OUTPUT_THROUGHPUT] = num_output_tokens / request_metrics[common_metrics.E2E_LAT]
```
Computes metrics directly from request execution without any external comparison. These intrinsic measurements assess model performance through timing and token count properties independent of ground truth or baselines.

Evidence 3: Statistical Aggregation
- File: `token_benchmark_ray.py`
- Code Reference: `metrics_summary()` function (Lines 163-178)
```python
for key in [
    common_metrics.INTER_TOKEN_LAT,
    common_metrics.TTFT,
    common_metrics.E2E_LAT,
    common_metrics.REQ_OUTPUT_THROUGHPUT,
    common_metrics.NUM_INPUT_TOKENS,
    common_metrics.NUM_OUTPUT_TOKENS
]:
    ret[key] = {}
    series = pd.Series(list(flatten(df_without_errored_req[key]))).dropna()
    quantiles = series.quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99]).to_dict()
    ...
    ret[key]["mean"] = series.mean()
    ret[key]["min"] = series.min()
    ret[key]["max"] = series.max()
    ret[key]["stddev"] = series.std()
```
Computes self-contained statistical aggregations including quantiles, mean, standard deviation, and extrema. These intrinsic quality measures assess performance distribution characteristics without comparing to external standards.

Evidence 4: Error Rate Calculation
- File: `token_benchmark_ray.py`
- Code Reference: Error rate computation (Lines 180-190)
```python
error_codes = df[common_metrics.ERROR_CODE].dropna()
num_errors = len(error_codes)
ret[common_metrics.ERROR_RATE] = num_errors / len(metrics) if len(metrics) else 0
ret[common_metrics.NUM_ERRORS] = num_errors
```
Computes error rates as self-consistency measures without external references. These metrics assess operational reliability through intrinsic failure rate calculation independent of ground truth comparison.