# JiWER - Stage 3 (EXECUTE) Evaluation

## Summary
JiWER is a specialized library for computing speech recognition error metrics (WER, CER, etc.), not a general evaluation framework. It lacks orchestration, telemetry, optimization, distributed execution, and human evaluation features entirely. It provides a simple API for calculating alignment and error rates between reference and hypothesis text pairs.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No orchestration features exist. The library processes single or batch reference/hypothesis pairs directly through function calls (`wer()`, `cer()`, etc.) without any workflow management, task routing, or dependency handling. See `src/jiwer/measures.py` - functions simply call `process_words()` or `process_characters()` directly. |
| S3F2: Inference & Telemetry | 0 | No telemetry, monitoring, or performance metrics. The library computes error rates but provides no latency tracking, throughput measurement, resource consumption monitoring, or cost tracking. Functions return only the error metrics themselves (see `src/jiwer/process.py` dataclasses `WordOutput` and `CharacterOutput` which contain only accuracy metrics). |
| S3F3: Test-Time Optimization | 0 | No optimization features. There is no caching, batching, or optimization techniques. The library uses RapidFuzz for fast edit distance computation but provides no user-facing optimization controls. See `src/jiwer/process.py:_word2int()` which processes each pair independently with no caching mechanism. |
| S3F4: Failure Handling | 0 | No failure handling, retry logic, or resilience features. Functions will raise Python exceptions on invalid input (see `src/jiwer/process.py:62-67` which raises `ValueError` for length mismatches) but provide no retry, timeout, or circuit breaker patterns. |
| S3F5: Checkpointing | 0 | No checkpointing or resumption capabilities. All computations are in-memory and must complete in a single run. There is no state persistence or incremental evaluation support anywhere in the codebase. |
| S3F6: Distributed Execution | 0 | No distributed execution support. The library is single-threaded Python with no multi-GPU, multi-node, or distributed processing capabilities. All computation happens in-process on a single machine (see `tests/test_speed.py` which shows benchmarks run synchronously). |
| S3F7: Human Evaluation | 0 | No human evaluation features. The library is purely algorithmic, computing WER/CER from existing reference/hypothesis pairs. There are no crowdsourcing integrations, annotation interfaces, or agreement metrics beyond what's computed from already-labeled data. |

## Detailed Analysis

### S3F1: Pipeline Orchestration (0 points)
Evidence: 
```python
# src/jiwer/measures.py:48-66
def wer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )
    return output.wer
```

The library provides only simple function calls that directly compute metrics. There is no:
- Task routing or pipeline definition
- DAG-based workflows
- Conditional branching
- Multiple evaluation protocols beyond transform composition

The `Compose` transform (see `src/jiwer/transforms.py:92-109`) chains data transformations but is not an execution orchestrator.

### S3F2: Inference & Telemetry (0 points)
Evidence:
```python
# src/jiwer/process.py:45-63
@dataclass
class WordOutput:
    references: List[List[str]]
    hypotheses: List[List[str]]
    alignments: List[List[AlignmentChunk]]
    wer: float
    mer: float
    wil: float
    wip: float
    hits: int
    substitutions: int
    insertions: int
    deletions: int
```

The output contains only error metrics - no timing, throughput, resource usage, or cost tracking. Speed tests exist (`tests/test_speed.py`) but only for benchmarking, not runtime telemetry.

### S3F3: Test-Time Optimization (0 points)
Evidence:
```python
# src/jiwer/process.py:228-245
def _word2int(reference: List[List[str]], hypothesis: List[List[str]]):
    word2int = defaultdict()
    word2int.default_factory = word2int.__len__
    ref_ints = [[word2int[word] for word in sentence] for sentence in reference]
    hyp_ints = [[word2int[word] for word in sentence] for sentence in hypothesis]
    return ref_ints, hyp_ints
```

While the library uses RapidFuzz (C++ backend) for performance, there are no user-configurable optimizations like:
- Prompt/response caching
- Dynamic batching
- Quantization or compilation options

Each call to `process_words()` recomputes everything from scratch.

### S3F4: Failure Handling (0 points)
Evidence:
```python
# src/jiwer/process.py:118-126
if len(ref_transformed) != len(hyp_transformed):
    raise ValueError(
        "After applying the transforms on the reference and hypothesis sentences, "
        f"their lengths must match. "
        f"Instead got {len(ref_transformed)} reference and "
        f"{len(hyp_transformed)} hypothesis sentences."
    )
```

Simple validation with immediate exception raising. No retry logic, exponential backoff, circuit breakers, or graceful degradation.

### S3F5: Checkpointing (0 points)
Evidence: No checkpoint-related code exists in the repository. The library is stateless - each function call is independent with no persistence mechanism. Even the CLI (`src/jiwer/cli.py`) reads files and computes results in one pass with no intermediate saves.

### S3F6: Distributed Execution (0 points)
Evidence:
```python
# tests/test_speed.py:4-10
def perform_computation(num_sentences):
    truth = ["this is a speed test" for _ in range(0, num_sentences)]
    hypo = ["this is not a speed test" for _ in range(0, num_sentences)]
    wer(truth, hypo)
```

All tests show synchronous, single-threaded execution. No mention of multi-GPU, multi-node, or distributed processing in any documentation or code. The `pyproject.toml` dependencies show only `rapidfuzz` and `click` - no distributed computing libraries.

### S3F7: Human Evaluation (0 points)
Evidence: The library computes metrics from already-labeled data pairs. From `docs/usage.md`:
```python
from jiwer import wer
reference = "hello world"
hypothesis = "hello duck"
error = wer(reference, hypothesis)
```

There are no features for collecting human annotations, integrating with crowdsourcing platforms, or managing rater agreements. The library assumes reference and hypothesis texts already exist.

## Conclusion

JiWER is fundamentally not an evaluation framework but a metrics computation library. It excels at its narrow purpose (computing WER/CER with good performance) but provides none of the execution infrastructure expected in Stage 3. It would be more accurate to consider JiWER as a component that could be used within an evaluation framework's scoring phase, rather than a framework itself.

Total Score: 0/21

The library receives 0 points across all Stage 3 features because it operates at a different abstraction level - it's a utility for computing specific metrics, not a system for orchestrating, monitoring, or managing evaluation runs.