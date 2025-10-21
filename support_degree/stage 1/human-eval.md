# openai/human-eval - Stage 1 (CONFIGURE) Evaluation

## Summary
HumanEval is a minimal evaluation harness specifically designed for code generation tasks. It provides a fixed dataset and basic execution framework but lacks comprehensive configuration capabilities. The tool is intentionally simple, focusing on evaluating code completions against a single pre-defined dataset rather than providing a general-purpose evaluation framework with extensive configuration options.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No dataset configuration capability. The framework uses a single hardcoded dataset (`HumanEval.jsonl.gz`) with no support for registering alternative datasets, defining schemas, or configuring splits. The `read_problems()` function in `human_eval/data.py` only reads from a fixed location (`HUMAN_EVAL = os.path.join(ROOT, "..", "data", "HumanEval.jsonl.gz")`). While you can pass a `--problem_file` argument to the CLI, this is merely file path specification, not logical dataset configuration. No schema definition, versioning, or split strategies exist. |
| S1F2: Model Configuration | 0 | No model or backend configuration. The framework has no model abstraction layer. Users must generate completions externally using their own code (README states: "you just have to provide `generate_one_completion`"). The framework only accepts pre-generated completions in JSONL format (`{"task_id": "...", "completion": "..."}`). No provider support, authentication management, or resource allocation features exist. The tool is execution-only, not generation-aware. |
| S1F3: Prompt Configuration | 0 | No prompt configuration system. The prompts are embedded in the dataset file (`problem["prompt"]` in `execution.py`), and there is no templating engine, parameter configuration (temperature, top_p), or prompt versioning. The framework concatenates the fixed prompt with user-provided completion: `check_program = problem["prompt"] + completion + "\n" + problem["test"]` (`execution.py:33-38`). Users cannot configure or modify prompts without editing the dataset file directly. |
| S1F4: Environment Setup | 2 | Basic dependency management with manual setup. The repository provides standard Python packaging: `requirements.txt` (tqdm, fire, numpy), `setup.py` with proper package configuration, and clear installation instructions in README. However, dependencies are not pinned to specific versions, which could cause compatibility issues. No Docker container, conda environment file, or automated setup scripts provided. The README includes manual setup instructions using conda/pip. Hardware requirements are minimal (CPU-only by default), with no GPU/TPU configuration options. The security sandbox requirement is mentioned but not implemented (users must implement their own). |
| S1F5: Security & Access | 1 | Minimal security features, primarily warnings. The framework includes a `reliability_guard()` function (`execution.py:185-251`) that disables destructive operations (fork, kill, file removal, etc.) and limits system calls. However, the actual execution line is commented out by default with extensive warnings about sandboxing (`execution.py:47-52`). No credential management (as no models are configured), no RBAC, no audit logging, no enterprise integration. The security model relies entirely on users implementing their own sandbox, which the documentation explicitly recommends. |
| S1F6: Cost Estimation | 0 | No cost estimation capabilities. The framework has no cost modeling, budget tools, or resource projection features. Since it doesn't integrate with any model providers (users generate completions externally), there's no token counting, API call tracking, or cost estimation. The only resource consideration is the `timeout` parameter for code execution (default 3.0 seconds), which is a safety measure rather than a cost optimization feature. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (0 pts)

Evidence:
```python
# human_eval/data.py - Lines 9-10
ROOT = os.path.dirname(os.path.abspath(__file__))
HUMAN_EVAL = os.path.join(ROOT, "..", "data", "HumanEval.jsonl.gz")

# human_eval/data.py - Lines 13-14
def read_problems(evalset_file: str = HUMAN_EVAL) -> Dict[str, Dict]:
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)}
```

The framework only supports reading JSONL/JSONL.gz files. There's no abstraction for different data sources (CSV, databases, APIs, HuggingFace), no schema definition API, no split strategies, and no versioning system. The `--problem_file` CLI option is just a file path, not a logical dataset reference.

### S1F2: Model and Backend Configuration (0 pts)

Evidence from README:
```python
# README.md example showing external generation requirement
num_samples_per_task = 200
samples = [
    dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]
```

The comment states: "you just have to provide `generate_one_completion`" - meaning model interaction is entirely external. The framework has no concept of models, providers, or backends.

### S1F3: Prompt Configuration (0 pts)

Evidence:
```python
# human_eval/execution.py - Lines 33-38
check_program = (
    problem["prompt"]
    + completion
    + "\n"
    + problem["test"]
    + "\n"
    + f"check({problem['entry_point']})"
)
```

Prompts are static strings stored in the dataset. No templating, no variable substitution, no few-shot configuration, no versioning. Simple string concatenation is used.

### S1F4: Environment Setup (2 pts)

Evidence:
```python
# requirements.txt
tqdm
fire
numpy
```

```python
# setup.py - Lines 7-21
setup(
    name="human-eval",
    py_modules=["human-eval"],
    version="1.0",
    description="",
    author="OpenAI",
    packages=find_packages(),
    install_requires=[...],
    entry_points={
        "console_scripts": [
            "evaluate_functional_correctness = human_eval.evaluate_functional_correctness",
        ]
    }
)
```

Standard Python packaging with unpinned dependencies. README provides clear installation steps but no automation or containerization. Scores 2 points for having basic dependency management and installation instructions, but lacks advanced features like Docker, pinned versions, or hardware configuration.

### S1F5: Security & Access (1 pt)

Evidence:
```python
# human_eval/execution.py - Lines 47-52 (commented out by design)
# WARNING
# This program exists to execute untrusted model-generated code...
# Once you have read this disclaimer and taken appropriate precautions,
# uncomment the following line and proceed at your own risk:
exec(check_program, exec_globals)
```

```python
# human_eval/execution.py - Lines 185-251
def reliability_guard(maximum_memory_bytes: Optional[int] = None):
    """
    This disables various destructive functions...
    WARNING: This function is NOT a security sandbox.
    """
    # Disables os.kill, os.system, os.fork, etc.
    os.kill = None
    os.system = None
    # ... many more
```

The `reliability_guard()` provides basic protection by disabling dangerous functions, earning 1 point. However, no authentication, access control, audit logging, or enterprise features exist.

### S1F6: Cost Estimation (0 pts)

Evidence:
```python
# human_eval/evaluation.py - Lines 47-48
def evaluate_functional_correctness(
    sample_file: str,
    k: List[int] = [1, 10, 100],
    n_workers: int = 4,
    timeout: float = 3.0,  # Only resource parameter
    problem_file: str = HUMAN_EVAL,
):
```

The only resource-related parameter is `timeout` for code execution safety. No cost modeling, token counting, or budget features exist since the framework doesn't interact with model APIs.

## Key Observations

Strengths:
- Clean, minimal codebase focused on one task
- Well-documented installation process
- Standard Python packaging
- Basic security protections for code execution

Limitations:
- Not a general-purpose evaluation framework
- No configuration layer - everything is hardcoded or file-based
- No model integration - assumes external generation
- Single dataset support only
- No prompt engineering capabilities
- No cost tracking or resource management

Overall Stage 1 Score: 3/18 points

This tool is a dataset-specific evaluation harness rather than a configurable evaluation framework. It excels at its narrow purpose (evaluating code completions on HumanEval) but provides minimal configuration capabilities for the CONFIGURE stage.