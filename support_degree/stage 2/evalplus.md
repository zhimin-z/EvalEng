# EvalPlus - Stage 2 (PREPARE) Evaluation

## Summary
EvalPlus is a code generation evaluation framework focused on Python correctness testing (HumanEval+, MBPP+) and efficiency evaluation (EvalPerf). The framework has minimal data preparation capabilities, focusing primarily on code generation and execution rather than dataset preprocessing, quality assessment, or infrastructure building. Most Stage 2 features are absent or minimal.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing exists. The framework loads pre-built datasets from HuggingFace without preprocessing pipelines. From `evalplus/data/__init__.py`: `load_dataset("evalplus/evalperf", split="test")` shows direct loading. The only "preprocessing" is deserialization via `mbpp_deserialize_inputs()` in `evalplus/data/mbpp.py` for MBPP-specific input formats. No tokenization, normalization, caching, or versioned splitting—datasets are consumed as-is. |
| S2F2: Quality Assessment | 0 | No quality assessment tools. The codebase contains no functionality for label quality checks, demographic analysis, duplicate detection, or bias assessment. File `evalplus/syncheck.py` only performs syntax checking of generated code, not dataset quality. The framework assumes pre-curated datasets from HuggingFace. |
| S2F3: PII Detection | 0 | No PII detection or anonymization. Grep for "pii", "privacy", "anonymize" returns no results. The framework focuses on code generation benchmarks which are already public datasets (HumanEval, MBPP), with no handling of sensitive data. |
| S2F4: Infrastructure Building | 0 | No infrastructure building capabilities. The framework doesn't support building retrieval systems, databases, or specialized environments. From `evalplus/evaluate.py`, it only executes code against pre-defined test inputs using `untrusted_check()`. No FAISS, BM25, vector databases, or similar infrastructure mentioned anywhere in the codebase. |
| S2F5: Model Artifact Validation | 1 | Minimal validation exists. The framework validates dataset hashes (e.g., `get_human_eval_plus_hash()` in `evalplus/data/humaneval.py`) to ensure dataset integrity. From `evalplus/evaluate.py`: checks for expected outputs via `get_groundtruth(problems, dataset_hash, [])`. However, no checksum validation for downloaded models, no version compatibility checks for model artifacts, and no corruption detection beyond basic execution failures. |
| S2F6: Scenario Generation | 1 | Minimal generation capabilities. The `evalplus/inputgen.py` file generates test inputs using ChatGPT and mutation-based approaches: `ChatGPTGen` for LLM-based generation and `TypedMutGen` for type-aware mutations. However, this is limited to single-function test input generation—no prompt variations, multi-turn dialogues, or edge case generators for evaluation scenarios. From `evalplus/gen/chatgpt_gen.py`: generates inputs but not evaluation prompts or scenarios. |
| S2F7: Red-Teaming | 0 | No red-teaming features. The framework focuses on functional correctness of code generation, not safety testing. No jailbreak attempts, prompt injection tests, bias probing, or adversarial generation. The `evalplus/sanitize.py` file sanitizes LLM outputs but doesn't generate adversarial inputs. |
| S2F8: Contamination Detection | 0 | No contamination detection. While the framework is concerned with evaluation integrity (mentions "noextreme" flag to filter extreme cases), there's no implementation for detecting training data contamination. No n-gram overlap analysis, semantic similarity checks, or comparison against training corpora. The focus is on adding more tests to existing benchmarks, not detecting contamination. |

## Key Observations

### Strengths
1. Dataset versioning: Uses dataset hashes for reproducibility (`get_human_eval_plus_hash()`)
2. Basic input generation: Implements mutation-based and LLM-based test input generation
3. Minimal validation: Checks expected outputs against ground truth with caching

### Limitations
1. No preprocessing pipelines: Datasets consumed directly from HuggingFace without transformation
2. No quality assessment: Assumes pre-curated, high-quality datasets
3. No infrastructure: Purely code execution framework, no retrieval/database support
4. No security features: No PII detection, red-teaming, or contamination checks
5. Limited scenario generation: Only generates test inputs, not evaluation scenarios

### Evidence of Missing Features

No data preprocessing (`evalplus/data/__init__.py`):
```python
def get_evalperf_data():
    dataset = load_dataset("evalplus/evalperf", split="test").to_list()
    # Direct loading, no preprocessing
```

No quality assessment (grep results show zero matches for quality-related terms)

No infrastructure building (`evalplus/evaluate.py` shows only code execution):
```python
def check_correctness(...):
    ret["base"] = untrusted_check(
        dataset, solution, problem["base_input"], ...
    )
```

Limited scenario generation (`evalplus/inputgen.py`):
```python
# Only generates test inputs, not evaluation scenarios
def input_generation(args, problems):
    for problem in problems.values():
        input_gen = ChatGPTGen(...).generate(args.chatgpt_len)
```

This framework is purpose-built for code generation evaluation with pre-existing benchmarks, not general-purpose evaluation with extensive data preparation needs.