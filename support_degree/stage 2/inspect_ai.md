# Inspect AI - Stage 2 (PREPARE) Evaluation

## Summary

Inspect AI is primarily an execution framework for LLM evaluations, not a data preparation tool. It provides strong capabilities for loading and configuring datasets at runtime, but offers minimal infrastructure for physical data preprocessing, quality assessment, or adversarial test generation. The framework excels at task orchestration and execution but delegates most preparation concerns to external tools or manual processes.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Basic loading with field mapping only, no preprocessing pipelines or caching |
| S2F2: Quality Assessment | 0 | No built-in quality, bias, or duplicate detection tools |
| S2F3: PII Detection | 0 | No PII detection or anonymization features |
| S2F4: Infrastructure Building | 2 | Strong sandbox/tool infrastructure for evaluation, but no retrieval systems or databases |
| S2F5: Model Validation | 1 | Basic model loading validation, no checksums or integrity verification |
| S2F6: Scenario Generation | 1 | Template instantiation only via prompt_template, no multi-turn generation or edge case tools |
| S2F7: Red-Teaming | 0 | No red-teaming framework or adversarial test generation |
| S2F8: Contamination Detection | 0 | No contamination detection capabilities |

---

## Detailed Feature Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning - Rating: 1

Evidence:

The framework provides basic dataset loading from CSV, JSON, and Hugging Face sources with field mapping capabilities:

```python
# From src/inspect_ai/dataset/_sources/example.py
def example_dataset(
    name: str,
    sample_fields: FieldSpec | RecordToSample | None = None,
) -> Dataset:
    """Read a dataset from inspect_ai package examples."""
```

```python
# From examples/popularity.py
dataset = example_dataset(
    name="popularity",
    sample_fields=FieldSpec(
        input="question",
        target="answer_matching_behavior",
        metadata=["label_confidence"],
    ),
)
```

Limitations:

1. No Preprocessing Pipelines: The `FieldSpec` only maps field names - there's no tokenization, normalization, or transformation support:

```python
# From docs reference - only field mapping, no preprocessing
class FieldSpec:
    input: str
    target: str | list[str]
    id: str | None
    metadata: list[str] | BaseModel | None
```

2. No Physical Splitting: Datasets are loaded into memory with a simple shuffle method, but there's no functionality to create actual train/val/test files:

```python
# From docs/_shuffling-choices.md
dataset = dataset.shuffle_choices(seed=42)
# OR
dataset = json_dataset("data.jsonl", shuffle_choices=42)
```

This is just in-memory shuffling of choices, not creating physical splits.

3. No Validation or Caching: The dataset loading code shows no checksum verification, format validation, or caching of preprocessed data. Files are simply loaded each time.

4. No Versioning: The `EvalDataset` structure tracks location but not versions:

```python
# From reference docs
class EvalDataset:
    name: str | None
    location: str | None
    # No version field
```

The framework expects you to bring already-preprocessed data and only handles runtime field mapping.

---

### S2F2: Dataset Quality and Bias Assessment - Rating: 0

Evidence:

Extensive search through the codebase reveals no quality assessment tools:

- No label quality checking, outlier detection, or inter-annotator agreement metrics
- No demographic analysis or bias detection functionality
- No duplicate detection capabilities
- The `Sample` class is purely for storing data, not analyzing it

```python
# From reference docs - Sample is just a data container
class Sample:
    input: str | list[ChatMessage]
    target: str | list[str] | None
    id: str | int | None
    metadata: dict[str, Any]
    files: dict[str, str] | None
    setup: str | None
```

The only metadata tracking is user-provided fields - no automated quality metrics are computed or stored.

Conclusion: Users must perform all quality assessment externally before loading data into Inspect.

---

### S2F3: PII Detection and Anonymization - Rating: 0

Evidence:

No PII detection or anonymization features exist in the codebase:

- Searching through all documentation and examples yields no mentions of PII, privacy, GDPR, or anonymization
- The sandbox environment provides isolation for execution safety, but not data privacy:

```python
# From docs/sandboxing.qmd - focuses on code execution isolation
@task
def bash():
    return Task(
        dataset=[...],
        sandbox="docker",  # For execution safety, not data privacy
        ...
    )
```

- No pre-processing hooks for PII scanning before data is used in prompts

Users must handle PII detection and redaction in their data pipelines before using Inspect.

---

### S2F4: Task-Specific Infrastructure Building - Rating: 2

Evidence:

Inspect provides strong infrastructure for evaluation execution but not for data preparation:

What EXISTS (evaluation infrastructure):

1. Sandbox Environments - Robust Docker-based sandboxes for tool execution:

```python
# From docs/sandboxing.qmd
@task
def my_task():
    return Task(
        solver=[use_tools([bash(), python()])],
        sandbox=("docker", "compose.yaml")
    )
```

2. Tool Infrastructure - Extensive tooling support:

```python
# From docs/tools-standard.qmd
tools = [
    bash_session(),
    text_editor(),
    web_browser(),
    computer(),
    web_search()
]
```

3. Agent Frameworks - Agent orchestration with state management:

```python
# From examples/intervention/intervention.py
@solver
def intervention_agent(mode: Mode) -> Solver:
    return chain(
        system_message(SHELL_PROMPT),
        user_prompt(),
        use_tools([bash(), python()]),
        agent_loop(),
    )
```

What's MISSING (data preparation infrastructure):

1. No Retrieval Systems: No FAISS, ColBERT, BM25, or vector database builders
2. No Database Setup: No schema creation, data ingestion, or query interfaces
3. No Index Building: Can't build search indices for knowledge-intensive tasks

The `web_search` tool exists but uses external providers (OpenAI, Tavily, etc.):

```python
# From examples/biology_qa.py - uses external search APIs
web_search(
    providers={
        "grok": {"max_search_results": 10},
        "openai": openai_options,
        "tavily": tavily_options,
    }
)
```

Why Rating is 2 not 3:

- Excellent execution infrastructure (sandboxes, tools, agents)
- But zero data preparation infrastructure (no retrieval/database builders)
- The framework assumes you bring your own indexed data or use external services

---

### S2F5: Model Artifact Validation - Rating: 1

Evidence:

Basic validation exists but is minimal:

1. Model Loading Checks - Basic connection and format validation:

```python
# From docs/models.qmd
model = get_model("openai/gpt-4o")
# Will fail if credentials invalid or model unavailable
```

2. No Checksum Verification: No SHA256 or cryptographic validation of model weights
3. No Version Compatibility: Models are referenced by provider/name strings with no version pinning:

```python
# From examples - version is in the string, not validated
"openai/gpt-4o-mini"
"anthropic/claude-3-5-haiku-latest"  # "latest" is not validated
```

4. No Configuration Validation: The `GenerateConfig` class has type checking but no schema validation:

```python
# From reference docs
class GenerateConfig:
    temperature: float | None = None
    max_tokens: int | None = None
    # No validation ranges or schema enforcement beyond types
```

5. No Corruption Detection: Models are accessed via APIs - no local weight validation

The framework trusts model providers to serve correct models and only validates basic connectivity/authentication.

---

### S2F6: Evaluation Scenario Generation - Rating: 1

Evidence:

Minimal generation capabilities - only template instantiation:

1. Template Support - Basic variable substitution:

```python
# From docs/solvers.qmd
prompt_template("What is the capital of {country}?")
```

2. No Parameter Sweeps: No built-in way to generate N variations or combinatorial prompts

3. No Multi-Turn Generation: The framework supports multi-turn execution but not generation:

```python
# From examples - messages are manually constructed, not generated
Sample(
    input=[
        {"role": "user", "content": "Question 1"},
        {"role": "assistant", "content": "Answer 1"},
        {"role": "user", "content": "Question 2"},
    ]
)
```

4. No Edge Case Generators: No boundary condition, adversarial input, or stress test generators

5. Reproducibility via Seeds: Shuffling supports seeds but this is just for ordering:

```python
# From docs/_shuffling-choices.md
dataset = dataset.shuffle_choices(seed=42)
```

What you'd need to do manually:

```python
# User must write their own generation logic
samples = []
for temp in [0.0, 0.5, 1.0]:
    for prompt_variant in variations:
        samples.append(Sample(input=prompt_variant, metadata={"temp": temp}))
```

The framework provides no helpers for systematic scenario generation.

---

### S2F7: Red-Teaming and Adversarial Test Generation - Rating: 0

Evidence:

No red-teaming framework exists:

1. No Jailbreak Library: Searching codebase for "jailbreak", "red team", "adversarial" yields no results
2. No Attack Generation: No prompt injection, context smuggling, or bias probing tools
3. No Safety Testing: No built-in safety boundary testing

The closest feature is the approval system which can review tool calls, but this is for runtime control, not test generation:

```python
# From examples/approval/approval.py - runtime approval, not test generation
@task
def approval_demo() -> Task:
    return Task(
        solver=react(...),
        approval="approval.yaml"  # Reviews actions, doesn't generate attacks
    )
```

What's missing:

- No pre-built adversarial prompt libraries
- No automated jailbreak attempt generation
- No bias probe generation across demographic dimensions
- No attack taxonomy or categorization

Users must manually create adversarial test cases or use external tools.

---

### S2F8: Data Contamination Detection - Rating: 0

Evidence:

No contamination detection capabilities:

1. No Training Corpus Comparison: Framework has no concept of training data
2. No N-gram Overlap Detection: No text comparison utilities
3. No Semantic Similarity: While models can compute embeddings, there's no built-in contamination checker

The evaluation logs track what was evaluated but have no contamination metadata:

```python
# From reference docs - EvalLog has no contamination fields
class EvalLog:
    status: str
    eval_id: str
    results: EvalResults
    samples: list[EvalSample]
    # No contamination_score or similar field
```

Why this matters:

Inspect evaluates models but provides no tools to detect if evaluation data leaked into training, which is critical for benchmark validity.

---

## Key Observations

### Strengths
1. Strong execution infrastructure - excellent sandboxing, tool support, and agent frameworks
2. Flexible dataset loading - supports multiple formats with field mapping
3. Production-ready evaluation - robust logging, error handling, and parallelism

### Critical Gaps
1. Zero data preparation tools - no preprocessing pipelines, quality checks, or validation
2. No adversarial testing - no red-teaming or safety probe generation
3. No contamination detection - no way to verify benchmark integrity
4. Manual scenario generation - users must write all variation/edge case logic

### Design Philosophy
Inspect is designed as an evaluation execution engine, not a data preparation framework. It expects:
- Pre-processed, validated datasets
- Externally-generated adversarial tests
- Manual quality assurance before evaluation
- External retrieval systems and databases

This is a valid design choice but means users need complementary tools for Stage 2 preparation work.