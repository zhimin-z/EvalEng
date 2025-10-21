# openai/human-eval - Stage 4 (EVALUATE) Evaluation

## Summary
HumanEval is a minimalist evaluation harness specifically designed for code generation tasks. It focuses exclusively on functional correctness testing through code execution and provides a single specialized metric (pass@k). The framework is purpose-built and lacks general-purpose evaluation features like multi-modal support, LLM-as-judge capabilities, or comprehensive statistical analysis tools.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation exists. The framework expects completions in a specific JSONL format with `task_id` and `completion` fields (`README.md` lines 29-30), but there's no schema validation or format checking code visible. The only validation is implicit through execution failures - if code is malformed, it will fail during `exec()` (`execution.py` line 53). No policy compliance checks, sanity checks, or normalization features exist. The framework assumes inputs are already properly formatted. |
| S4F2: Metric Computation | 1 | Extremely limited metric library with only one specialized metric: pass@k for code functional correctness (`evaluation.py` lines 7-23, 75-77). The `estimate_pass_at_k` function implements the unbiased estimator described in the Codex paper. While this metric is well-implemented with per-sample scoring (`evaluation.py` lines 53-57 store individual results), there are no text generation metrics (BLEU, ROUGE), classification metrics, retrieval metrics, or safety metrics. No extensibility mechanism for custom metrics exists - users would need to fork the codebase. |
| S4F3: Evaluator Models | 0 | No evaluator model integration whatsoever. The framework relies purely on functional correctness testing through code execution (`execution.py` lines 42-53). There are no LLM-as-judge features, no pre-built judge prompts, no support for specialized evaluator models like RAGAS or G-Eval, and no capability to use models for evaluation. This is by design - the framework evaluates code by running test cases, not through model-based evaluation. |
| S4F4: Multi-Modal Scoring | 0 | Completely text-only (specifically code-only) framework. No support for vision-language, audio-text, video understanding, or any modality beyond text/code. The entire framework operates on string completions that are executed as Python code (`execution.py` line 53: `exec(check_program, exec_globals)`). No infrastructure for handling images, audio, video, or cross-modal evaluation exists. |
| S4F5: Aggregate Statistics | 1 | Very basic aggregation capabilities. The framework computes mean pass@k across all problems (`evaluation.py` line 76: `.mean()`), and internally tracks total samples and correct samples per problem (`evaluation.py` lines 70-74). However, there are no standard statistical measures (median, std dev, percentiles, confidence intervals), no distribution analysis, no significance testing for model comparison, no ranking systems, and no weighted metrics. The output is simply a dictionary with pass@k values for requested k values (`evaluation.py` lines 75-77). Per-sample results are saved to a JSONL file (`evaluation.py` lines 79-87), but no statistical analysis is performed on them. |

## Detailed Evidence

### S4F1: Output Validation and Normalization
Evidence from README.md (lines 27-32):
```markdown
After following the above instructions to enable execution, generate samples
and save them in the following JSON Lines (jsonl) format, where each sample is
formatted into a single line like so:
```
{"task_id": "Corresponding HumanEval task ID", "completion": "Completion only without the prompt"}
```
```

Evidence from evaluation.py (line 54):
```python
for sample in tqdm.tqdm(stream_jsonl(sample_file)):
    task_id = sample["task_id"]
    completion = sample["completion"]
```
The code assumes these fields exist without validation. No try-catch for missing fields or format errors.

### S4F2: Task-Specific Metric Computation
Evidence from evaluation.py (lines 7-23):
```python
def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
```

This is the only metric in the entire codebase. No other metrics are available.

### S4F3: Evaluator Model Integration
Evidence from execution.py (lines 42-53):
```python
check_program = (
    problem["prompt"]
    + completion
    + "\n"
    + problem["test"]
    + "\n"
    + f"check({problem['entry_point']})"
)

try:
    exec_globals = {}
    with swallow_io():
        with time_limit(timeout):
            exec(check_program, exec_globals)
```

Evaluation is purely through code execution, not model-based evaluation. No model integration exists.

### S4F4: Multi-Modal Scoring Protocols
The entire codebase operates on text/code strings. No image, audio, or video handling capabilities exist. All files (`execution.py`, `evaluation.py`, `data.py`) only process text/code data.

### S4F5: Aggregate Statistics and Cross-Model Comparison
Evidence from evaluation.py (lines 70-77):
```python
# Calculate pass@k.
total, correct = [], []
for result in results.values():
    result.sort()
    passed = [r[1]["passed"] for r in result]
    total.append(len(passed))
    correct.append(sum(passed))
total = np.array(total)
correct = np.array(correct)

ks = k
pass_at_k = {f"pass@{k}": estimate_pass_at_k(total, correct, k).mean()
             for k in ks if (total >= k).all()}
```

Only computes mean pass@k. No other statistics, no confidence intervals, no significance testing, no distribution analysis. The output is just a simple dictionary like `{'pass@1': 0.5, 'pass@10': 0.7}`.

## Overall Assessment

HumanEval is an extremely focused, single-purpose evaluation tool. It excels at what it's designed for (functional correctness testing of code) but provides almost none of the general evaluation framework features assessed in Stage 4. It's more of a specialized benchmark runner than a comprehensive evaluation framework. For code generation evaluation through execution, it works well, but it lacks extensibility, rich metrics, statistical analysis, and modern evaluation features like LLM-as-judge. Organizations needing a full-featured evaluation framework would find this too limited, but researchers specifically evaluating code generation functional correctness would find it adequate for that narrow use case.