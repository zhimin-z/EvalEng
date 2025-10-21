# OpenAI Evals - Stage 2 (PREPARE) Evaluation

## Summary

OpenAI Evals is a comprehensive evaluation framework for LLMs with minimal built-in data preparation capabilities. The framework focuses on execution and evaluation logic rather than physical data preparation, preprocessing, or infrastructure building. While it has a registry system for datasets, most preparation features are either absent or require manual implementation by eval authors.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing utilities. Framework relies on manual data preparation in JSONL format with no built-in preprocessing pipelines, caching is basic, and splitting must be done manually before registration. |
| S2F2: Quality Assessment | 0 | No quality assessment tools present. No utilities for detecting label noise, computing demographic distributions, duplicate detection, or bias analysis. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features found in the codebase or documentation. |
| S2F4: Infrastructure Building | 1 | Minimal infrastructure support. Only one eval (multistep_web_tasks) uses complex infrastructure (WebArena docker containers), but this is eval-specific rather than framework-provided. |
| S2F5: Model Artifact Validation | 1 | Basic validation only. Framework validates API keys and model names but no checksum validation, version compatibility checks, or corruption detection for model artifacts. |
| S2F6: Evaluation Scenario Generation | 1 | Minimal generation capabilities. Some individual evals generate scenarios (e.g., function_deduction generates test cases), but no framework-level scenario generation utilities exist. |
| S2F7: Red-Teaming | 0 | No red-teaming framework or adversarial test generation capabilities. While some evals test specific adversarial scenarios, there's no general red-teaming infrastructure. |
| S2F8: Contamination Detection | 0 | No contamination detection features. Framework provides no utilities for comparing eval data against training corpora or detecting data leakage. |

## Detailed Feature Analysis

### S2F1: Data Preprocessing and Physical Partitioning (Rating: 1)

Evidence:

The framework has minimal preprocessing capabilities. From `evals/data.py`:

```python
def get_jsonl(path: str) -> list[dict]:
    """Read JSONL file from path and return as list of dicts"""
    with open(path, "r") as f:
        return [json.loads(line) for line in f]
```

The data loading is extremely basic - just reading JSONL files with no preprocessing, validation, or transformation capabilities.

From the README.md:
> "Please note that we are currently not accepting evals with custom code! While we ask you to not submit such evals at the moment, you can still submit model-graded evals with custom model-graded YAML files."

This indicates data must be prepared manually before being added to the registry. There's no evidence of:
- Built-in tokenization, normalization, or other text preprocessing
- Image or audio preprocessing pipelines
- Automated data splitting with stratification
- Preprocessing caching mechanisms
- Data versioning systems

The only "preprocessing" is manual preparation of JSONL files before registration in `evals/registry/data/`.

Rating Justification: Barely exists - users must prepare all data manually before using the framework.

### S2F2: Dataset Quality and Bias Assessment (Rating: 0)

Evidence:

No quality assessment utilities found in the codebase. Searching through the repository structure shows:
- No modules for label quality checking
- No demographic distribution analysis tools
- No duplicate detection utilities
- No bias detection frameworks

Individual evals may perform task-specific quality checks (e.g., `already_said_that` checks for format violations), but there are no framework-level quality assessment tools.

Rating Justification: Feature completely absent.

### S2F3: PII Detection and Anonymization (Rating: 0)

Evidence:

No PII detection capabilities found. From the documentation and code review:
- No mention of PII handling in any documentation
- No privacy-related modules in the codebase
- No anonymization utilities

The only privacy-related content is in individual eval descriptions noting they use public datasets, but no framework support for PII detection exists.

Rating Justification: Feature completely absent.

### S2F4: Task-Specific Infrastructure Building (Rating: 1)

Evidence:

Very limited infrastructure support, and what exists is eval-specific rather than framework-provided. From `evals/elsuite/multistep_web_tasks/README.md`:

```markdown
## Setup instructions ##
### NOTE: Important information for running this eval: ###
- The eval may require manual downloading of some docker images.
- Running the full eval requires downloading approximately 200GB of data.
```

This eval builds custom infrastructure using WebArena docker containers, but this is implemented within the specific eval, not as a reusable framework feature.

No evidence of:
- Framework-provided retrieval system builders (FAISS, ColBERT, BM25)
- Database setup utilities
- Index persistence and versioning
- Reusable infrastructure components

From `evals/base.py`, the framework provides only basic eval scaffolding with no infrastructure building capabilities.

Rating Justification: Minimal support - one eval has custom infrastructure, but no framework-level utilities exist.

### S2F5: Model Artifact Validation (Rating: 1)

Evidence:

Basic validation exists only for API connectivity. From `evals/api.py`:

```python
def check_api_key():
    """Validate that API key is set"""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set")
```

The framework validates:
- API key existence
- Model name validity (checks against OpenAI's model list)

No evidence of:
- Checksum validation for model weights
- Version compatibility checking
- Configuration schema validation
- Model corruption detection
- Integrity verification

Rating Justification: Minimal validation - only checks API credentials and model names.

### S2F6: Evaluation Scenario Generation (Rating: 1)

Evidence:

Minimal scenario generation, mostly within specific evals. From `evals/elsuite/function_deduction/README.md`:

> "The dataset are 100 int -> int functions of varying difficulty. Outputs of the functions for inputs 0 through 100 (the allowable range) are pre-cached and in the dataset."

This shows pre-generated scenarios rather than dynamic generation. Some generation exists in specific evals like `schelling_point`:

```python
# From schelling_point eval - generates permutations
def generate_permuted_samples(words, n_permutations):
    samples = []
    for _ in range(n_permutations):
        permuted = random.sample(words, len(words))
        samples.append(permuted)
    return samples
```

But there's no framework-level scenario generation system. No evidence of:
- Template instantiation with variables
- Parameter sweep generation
- Multi-turn dialogue generation utilities
- Reproducible scenario versioning

Rating Justification: Minimal - some evals generate variants, but no general framework support.

### S2F7: Red-Teaming and Adversarial Test Generation (Rating: 0)

Evidence:

No red-teaming framework exists. While some evals test adversarial capabilities (e.g., `make_me_say`, `make_me_pay`), these are specific task implementations, not a general red-teaming system.

From `evals/elsuite/make_me_pay/readme.md`:
> "This evaluation tests an AI system's ability to generate persuasive or manipulative text"

This is a single eval testing manipulation, not a red-teaming framework. No evidence of:
- Jailbreak attempt libraries
- Automated attack generation
- Prompt injection test generation
- Bias probing utilities
- Safety boundary testing frameworks

Rating Justification: Feature completely absent - no general red-teaming infrastructure.

### S2F8: Data Contamination Detection (Rating: 0)

Evidence:

No contamination detection capabilities found. From the codebase review:
- No modules for comparing eval data against training corpora
- No n-gram overlap detection
- No semantic similarity checking for contamination
- No fingerprinting systems

The framework assumes datasets are clean and doesn't provide contamination checking utilities.

Rating Justification: Feature completely absent.

## Key Strengths

1. Clear Data Format: Simple JSONL format makes manual data preparation straightforward
2. Extensive Example Library: 50+ diverse evals demonstrate various task types
3. Flexible Eval Design: Custom eval classes allow arbitrary evaluation logic
4. Registry System: Centralized registration of datasets, models, and evals

## Key Weaknesses

1. No Data Preprocessing: All preprocessing must be done manually before registration
2. No Quality Assurance: No tools for validating data quality, detecting biases, or finding duplicates
3. No Infrastructure Support: Users must build retrieval systems, databases, etc. from scratch
4. Manual Data Preparation: Framework expects fully prepared data in JSONL format
5. No Privacy Features: No PII detection or anonymization capabilities
6. No Contamination Checking: No utilities for detecting data leakage

## Overall Stage 2 Score

Total: 4/24 points

The framework scores very low on Stage 2 preparation capabilities. It's designed as an execution and evaluation framework, not a data preparation framework. Users are expected to:
- Manually prepare and clean all data
- Handle preprocessing in external scripts
- Build any necessary infrastructure themselves
- Perform quality checks outside the framework

This is an intentional design choice focused on eval execution rather than data preparation, but it means the framework provides minimal support for the physical preparation phase of evaluations.