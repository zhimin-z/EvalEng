# Ragas - Stage 1 (CONFIGURE) Evaluation

## Summary
Ragas is an LLM evaluation framework focused on RAG systems with strong emphasis on metrics and testset generation. Configuration capabilities are primarily code-based with limited declarative configuration options. The framework excels at metric composition but lacks traditional evaluation harness features like dataset versioning, comprehensive provider configuration, and cost estimation. Configuration is scattered across multiple classes rather than centralized.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Basic CSV/JSONL loading exists but lacks schema definition, versioning, and split strategies. No declarative dataset configuration. |
| S1F2: Model Configuration | 2 | Supports multiple providers (OpenAI, Anthropic, HF, vLLM, etc.) via wrapper classes, but configuration is purely programmatic with no YAML/JSON config files. Authentication via env vars only. |
| S1F3: Prompt Configuration | 1 | Minimal templating - metrics use string prompts with basic variable substitution. No formal template system, versioning, or few-shot support at framework level. |
| S1F4: Environment Setup | 2 | Has `pyproject.toml` with dependencies, but no containerization, no automated setup scripts, and dependencies are not pinned to specific versions. |
| S1F5: Security & Access | 0 | Only supports environment variables for API keys. No vault integration, RBAC, audit logging, or enterprise features. |
| S1F6: Cost Estimation | 1 | Basic token counting exists in `src/ragas/cost.py` but no budget limits, pre-execution cost estimation, or optimization suggestions. |

---

## Detailed Feature Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 1/3

Evidence:

1. Dataset Source Support - Very limited:
```python
# src/ragas/dataset.py
class Dataset:
    def __init__(
        self,
        name: str,
        backend: str = "local/csv",
        data_model: Optional[Type[BaseModel]] = None,
        root_dir: str = ".",
        backend_kwargs,
    ):
```
- Only supports CSV/JSONL locally: `src/ragas/backends/local_csv.py`, `src/ragas/backends/local_jsonl.py`
- Google Drive backend exists but requires manual setup (`examples/gdrive_backend_example.py`)
- No built-in connectors for HuggingFace, databases, or cloud storage
- Data loading requires physical instantiation, not purely logical registration

2. Schema Definition - Missing:
```python
# No schema API found. Data models are optional Pydantic models:
dataset = Dataset(
    name="evaluation_results",
    data_model=EvaluationRecord,  # Optional Pydantic model
)
```
- No way to define column types, constraints, or validation rules at dataset level
- Schema validation only through optional Pydantic models passed by user

3. Split Strategies - Absent:
- No built-in train/test/validation splitting
- Examples show manual splitting:
```python
# examples/ragas_examples/text2sql/data_utils.py
train_df = df[df['split'] == 'train'].copy()  # Manual filtering
```

4. Versioning - None:
- No version tracking or history
- Dataset names are just strings with no version metadata

Justification: Framework provides basic data loading but lacks declarative configuration, schema definition, automated splits, and versioning. Configuration is minimal and imperative rather than logical/declarative.

---

### S1F2: Model and Backend Configuration
Rating: 2/3

Evidence:

1. Provider Support - Good variety:
```python
# src/ragas/llms/ contains wrappers for:
# - OpenAI (llama_index.py, langchain.py)
# - Anthropic (langchain.py)
# - Google (oci_genai.py mentions gemini)
# - HuggingFace (base.py)
# - vLLM (referenced in docs)
```
Example from `examples/oci_genai_example.py`:
```python
llm = oci_genai_factory(
    model_id=MODEL_ID,
    compartment_id=COMPARTMENT_ID,
    endpoint_id=ENDPOINT_ID
)
```

2. Configuration Method - Programmatic only:
```python
# All examples show Python API configuration:
from ragas.llms import LangchainLLMWrapper
llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
```
- No YAML/JSON configuration files found
- No CLI-based configuration
- Runtime overrides only through Python code

3. Authentication - Environment variables only:
```python
# examples/ragas_examples/text2sql/text2sql_agent.py
openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
```
- No vault integration
- No credential rotation
- Multi-region support depends on underlying provider SDK

4. Resource Allocation - Limited:
```python
# src/ragas/run_config.py shows basic execution config:
@dataclass
class RunConfig:
    max_workers: int = 16
    max_wait: int = 60
    timeout: t.Optional[int] = 60
```
- No GPU/CPU specification
- No validation before execution
- Basic concurrency control only

Justification: Supports multiple providers through wrapper classes but lacks centralized configuration files. Configuration is code-based with no declarative YAML/JSON support. Authentication limited to environment variables.

---

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 1/3

Evidence:

1. Parameter Definition - Basic:
```python
# src/ragas/run_config.py
@dataclass
class RunConfig:
    max_workers: int = 16
    max_wait: int = 60
    timeout: t.Optional[int] = 60
    max_retries: int = 10
    exception_handler: t.Optional[ExceptionHandler] = None
```
- Temperature, top_p controlled through underlying LLM wrappers, not framework-level
- No parameter sweeps at framework level

2. Template System - Minimal:
```python
# Metrics use basic string templates with variable substitution:
my_metric = DiscreteMetric(
    name="correctness",
    prompt="Check if the response contains {grading_notes}",
    allowed_values=["pass", "fail"],
)
```
From `examples/ragas_examples/prompt_evals/evals.py`:
```python
@discrete_metric(name="accuracy", allowed_values=["pass", "fail"])
def my_metric(prediction: str, actual: str):
    return MetricResult(value="pass") if prediction == actual else MetricResult(value="fail")
```
- No Jinja2 or advanced templating engine
- Variable substitution through f-strings, not formal templates
- Few-shot examples must be manually embedded in prompt strings

3. Prompt Versioning - Absent:
```python
# examples/iterate_prompt/ shows manual prompt file management:
# - promptv1.txt
# - promptv2_fewshot.txt
```
- No built-in versioning system
- No diff tools
- Manual file management only

4. Metric Configuration - Good but not configuration-file based:
```python
# Metrics defined in code, not config files:
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=llm
)
```

Justification: Basic string-based prompt templates with no formal templating engine, versioning, or declarative configuration. Metric specification is code-based rather than config-based.

---

### S1F4: Environment Setup and Dependency Management
Rating: 2/3

Evidence:

1. Dependency Specification - Present but not pinned:
```toml
# pyproject.toml
[project]
dependencies = [
    "numpy",
    "datasets",
    "tiktoken",
    "langchain",
    "langchain-core>=0.3.0",
    "langchain-openai",
    # ... more dependencies without version pins
]
```
- Has `pyproject.toml` with dependencies
- Not pinned to specific versions (except langchain-core>=0.3.0)
- Optional dependencies clearly marked:
```toml
[project.optional-dependencies]
all = [...]
```

2. Containerization - Absent:
- No Dockerfile in main repo
- Benchmark test has Dockerfile: `tests/benchmarks/Dockerfile` but not for production use
- No official Docker images mentioned

3. Environment Automation - Minimal:
```bash
# README.md shows basic pip install:
pip install ragas
# or from source:
pip install git+https://github.com/explodinggradients/ragas
```
- No setup scripts
- No virtual environment management
- Manual installation only

4. Hardware Configuration - Not documented:
- No CUDA version specifications
- No compatibility checks on startup
- Examples mention GPU but no framework-level configuration

Justification: Has dependency specification in `pyproject.toml` but lacks version pinning, containerization, and automated setup. Basic Python packaging only.

---

### S1F5: Security and Access Control
Rating: 0/3

Evidence:

1. Credential Management - Environment variables only:
```python
# All examples use env vars:
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
```
- No vault integration mentioned
- No encryption at rest
- No rotation support

2. Access Control - None:
- No RBAC mentioned
- No user/group/role system
- No access restrictions on experiments or models

3. Audit Logging - Analytics only, not security:
```python
# src/ragas/_analytics.py
# Basic usage analytics, not security audit logs
```
- Tracks usage for product improvement
- Not security-focused
- No tamper-proof logging

4. Enterprise Integration - None:
- No SSO support
- No LDAP/Active Directory
- No compliance certifications mentioned

Justification: Zero security features beyond basic environment variable authentication. No enterprise features, RBAC, or audit logging.

---

### S1F6: Cost Estimation and Budget Planning
Rating: 1/3

Evidence:

1. Cost Modeling - Basic token counting only:
```python
# src/ragas/cost.py
@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    model: str = ""

class CostCallbackHandler(BaseCallbackHandler):
    def on_llm_end(self, response: LLMResult, kwargs: t.Any):
        # Tracks token usage
```
- Tracks tokens but no cost calculation
- No pricing database
- No custom cost models

2. Resource Projection - Token counting only:
```python
# cost.py tracks tokens after execution, not before
token_usage_parser = get_token_usage_for_openai
```
- No pre-execution estimation
- No API call projection
- Reactive tracking, not predictive

3. Budget Tools - Absent:
- No budget limits
- No cost breakdown
- No what-if analysis

4. Optimization Suggestions - None:
- No cheaper model recommendations
- No batch size optimization
- No provider comparison

Justification: Only basic token counting exists for post-execution tracking. No cost estimation, budgeting, or optimization features.

---

## Key Observations

### Strengths:
1. Multi-provider support through wrapper classes (OpenAI, Anthropic, Google, HF)
2. Extensible metric system with decorator-based custom metrics
3. Good documentation with tutorials and examples
4. Experiment tracking via `@experiment()` decorator

### Critical Gaps:
1. No declarative configuration - everything is code-based
2. No dataset versioning or schema definition
3. No security features beyond env vars
4. No cost estimation or budgeting
5. No formal template system for prompts
6. No split strategies or dataset management

### Configuration Pattern:
Ragas follows an imperative, code-first approach rather than declarative configuration:
```python
# Typical Ragas workflow - all in code:
dataset = Dataset(name="test", backend="local/csv")
llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4"))
metric = DiscreteMetric(name="accuracy", prompt="...", allowed_values=["pass", "fail"])
result = evaluate(dataset, metrics=[metric], llm=llm)
```

No equivalent YAML/JSON configuration file approach exists.

---

## Stage 1 Total Score: 7/18 (38.9%)

The framework prioritizes execution over configuration, making it more suitable for researchers writing Python code than teams needing declarative, versioned, and budgeted evaluation pipelines. Configuration capabilities are functional but minimal, lacking enterprise-grade features expected in modern evaluation frameworks.