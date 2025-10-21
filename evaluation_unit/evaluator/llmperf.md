## Evaluator Categories

[Algorithmic, Custom]

## Detailed Analysis

### Algorithmic

Evidence 1: Numeric correctness validation through deterministic pattern matching
- File: `llm_correctness.py`
- Lines: 113-132
- Code Reference:
```python
commas_between_numbers_re = r"(\d+),(?=\d)"
# ... string manipulation and validation
re.findall(r"\d+", gen_text_commas_removed)
assert str(completed_request_config.metadata["rnd_number"]) in nums
```
This implements a correctness evaluation using rule-based, deterministic checks to verify if LLM-generated text contains the expected number in the correct format. The evaluation employs predefined algorithmic methods including regular expression pattern matching for comma detection, string manipulation for text cleaning, and assertion-based checking to validate outputs against expected numeric values. This represents a pure algorithmic evaluator that uses computational rules and logical operations to score model outputs on the correctness benchmark task, providing consistent and reproducible assessment through established string matching techniques.

Evidence 2: Statistical performance metric computation
- File: `token_benchmark_ray.py`
- Function: `metrics_summary()`
- Lines: 229-285
- Code Reference:
```python
# Quantile distributions (p25, p50, p75, p90, p95, p99)
# Statistical measures (mean, standard deviation, min, max)
# Error rates and throughput metrics
```
This function computes statistical metrics on collected performance data using pandas operations to calculate quantile distributions, statistical measures including mean and standard deviation, and performance indicators like error rates and throughput. These computations represent algorithmic, mathematical operations on model performance data that provide deterministic assessment through established statistical functions. The evaluator ensures consistent, reproducible evaluation by applying predefined computational measures to performance measurements.

Evidence 3: Standardized metric definitions
- File: `src/llmperf/common_metrics.py`
- Code Reference:
```python
# Metric constant definitions for latency, token counts, throughput, error rates
```
This file defines the standard algorithmic metrics used throughout the harness including latency measurements, token counts, throughput calculations, and error rates. These metric definitions establish predefined statistical functions that are consistently applied to model outputs across the evaluation framework, ensuring reproducible assessment through established computational measures that can be deterministically calculated from model performance data.

---

### Custom

Evidence 1: Domain-specific numeric conversion evaluation pipeline
- File: `llm_correctness.py`
- Function: `llm_correctness()` combined with validation logic
- Lines: 31-91, 113-132
- Code Reference:
```python
num2words.num2words(rnd_number)
prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."
# Custom validation logic with regex patterns and string matching
# Custom metrics: "mismatch_rate", "num_mismatched_requests"
```
This implements a custom evaluation pipeline specifically designed for numeric word-to-digit conversion tasks that extends beyond standard evaluator categories. The evaluator generates custom prompts with random numbers converted to words, creates domain-specific test cases for numeric conversion, implements specialized validation logic combining regex patterns with string matching, and tracks custom metrics like mismatch rate specific to this benchmark. This represents a custom evaluation mechanism addressing unique requirements for numeric conversion correctness testing that cannot be met by standard algorithmic evaluators alone, as it combines computational validation with specialized workflow logic tailored to this particular task domain.

Evidence 2: Specialized LLM performance benchmarking workflow
- File: `token_benchmark_ray.py`
- Function: `get_token_throughput_latencies()`
- Lines: 18-137
- Code Reference:
```python
randomly_sample_sonnet_lines_prompt()  # Shakespeare sonnets strategy
# Multiple evaluation dimensions: throughput, latency, token counts
# Custom token counting with LlamaTokenizer for cross-model consistency
# Multi-stage evaluation with concurrent request handling
```
This implements a custom evaluation workflow that combines multiple assessment dimensions through specialized mechanisms. The evaluator uses a unique prompting strategy sampling from Shakespeare sonnets rather than standard benchmarks, integrates multiple evaluation dimensions including throughput and latency measurements, implements custom token counting logic with LlamaTokenizer to ensure cross-model consistency, and creates a multi-stage evaluation pipeline with concurrent request handling. This represents a custom evaluation pipeline designed specifically for LLM performance benchmarking with non-standard approaches that address unique evaluation requirements by combining multiple measurement types into a unified specialized assessment framework.