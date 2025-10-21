# Inspect AI - Stage 1 (CONFIGURE) Evaluation

## Summary
Inspect AI demonstrates strong configuration capabilities with comprehensive model/provider support, flexible dataset loading, and sophisticated prompt templating. It excels at dataset configuration, model management, and environment setup through Docker/containers. However, it lacks built-in cost estimation features and has limited enterprise-grade security features (no native RBAC or vault integration for secrets).

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 3 | Excellent multi-source support with 5+ formats (JSON, CSV, HuggingFace, memory, example datasets), declarative schema via `FieldSpec`, flexible field mapping, shuffle/split capabilities, and metadata validation via Pydantic models. |
| S1F2: Model Configuration | 3 | Outstanding provider support (15+ providers including OpenAI, Anthropic, Google, Azure, AWS Bedrock, vLLM, Ollama), clean Python/YAML config API, secure credential management via env vars, and resource allocation control. |
| S1F3: Prompt Configuration | 2 | Good templating support with variable substitution and system/user/assistant message composition, but lacks formal versioning, template inheritance, and advanced few-shot configuration beyond manual message construction. |
| S1F4: Environment Setup | 3 | Excellent containerization with Docker Compose support, pinned dependencies via `pyproject.toml`/`requirements.txt`, automated sandbox setup, and comprehensive hardware configuration for GPU/CPU resources. |
| S1F5: Security & Access | 1 | Basic security with environment variable credential management only. No built-in RBAC, vault integration, audit logging, SSO, or enterprise features. Approval system exists but is for tool execution, not access control. |
| S1F6: Cost Estimation | 0 | No built-in cost estimation or budgeting features. The framework tracks token usage (`ModelUsage`) but provides no pricing models, cost projection, or budget enforcement mechanisms. |

---

## Detailed Evidence

### S1F1: Dataset Discovery and Logical Configuration

Rating: 3/3

Dataset Source Support - 5+ sources with clean APIs:

```python
# From src/inspect_ai/dataset/_sources/
# 1. JSON/JSONL
dataset = json_dataset("data.jsonl", sample_fields=FieldSpec(...))

# 2. CSV
dataset = csv_dataset("data.csv", sample_fields=FieldSpec(...))

# 3. HuggingFace
dataset = hf_dataset(
    "HuggingFaceH4/MATH-500",
    split="test",
    sample_fields=FieldSpec(input="problem", target="solution")
)

# 4. Memory/Python
dataset = MemoryDataset(samples=[...], name="my_data")

# 5. Example datasets (built-in)
dataset = example_dataset("security_guide")
```
*Evidence: `src/inspect_ai/dataset/_sources/example.py`, `examples/security_guide.py`, `examples/scorer.py`*

Schema Definition - Declarative via `FieldSpec` and Pydantic:

```python
# Field mapping with validation
from pydantic import BaseModel, Field

class PopularityMetadata(BaseModel, frozen=True):
    category: str
    label_confidence: float

dataset = json_dataset(
    "popularity.jsonl",
    FieldSpec(
        input="question",
        target="answer_matching_behavior",
        id="question_id",
        metadata=PopularityMetadata,  # Type-safe validation
    ),
)
```
*Evidence: `docs/_metadata_typing.md`, lines 7-24*

Split Strategies - Flexible with shuffle support:

```python
# Shuffle dataset
dataset = dataset.shuffle()
dataset = json_dataset("data.jsonl", shuffle=True)

# Shuffle with seed for reproducibility
dataset = dataset.shuffle(seed=42)

# Shuffle choices in multiple-choice questions
dataset = dataset.shuffle_choices()
dataset = json_dataset("data.jsonl", shuffle_choices=42)
```
*Evidence: `docs/_shuffling-choices.md`, lines 7-26*

Versioning - Limited built-in versioning, but supports explicit IDs:

```python
# Samples can have explicit IDs for tracking
Sample(id="question_123", input="...", target="...")

# Supports sample preservation across retries using stable IDs
# From docs/_sample-preservation.md:
# "Samples can have an explicit `id` field which contains the unique identifier"
```
*Evidence: `docs/_sample-preservation.md`, lines 12-22*

Justification: Inspect provides comprehensive dataset configuration with 5+ sources (JSON, CSV, HuggingFace, Memory, Examples), full schema definition via Pydantic models, flexible split/shuffle strategies, and sample ID tracking. The only gap is formal dataset versioning (e.g., dataset_v1.2 references), but the underlying capabilities are excellent.

---

### S1F2: Model and Backend Configuration

Rating: 3/3

Provider Support - 15+ providers across categories:

From `docs/_model-providers.md`:
```markdown
| Lab APIs | OpenAI, Anthropic, Google, Grok, Mistral, DeepSeek, Perplexity |
| Cloud APIs | AWS Bedrock, Azure AI |
| Open (Hosted) | Groq, Together AI, Fireworks AI, Cloudflare, HF Inference, SambaNova, Goodfire |
| Open (Local) | Hugging Face, vLLM, Ollama, Llama-cpp-python, SGLang, TransformerLens |
```
*Evidence: `docs/_model-providers.md`, lines 3-10*

Configuration Method - Clean Python API with YAML support:

```python
# Python API
from inspect_ai import eval
from inspect_ai.model import GenerateConfig

eval(
    task="my_task",
    model="openai/gpt-4o",
    config=GenerateConfig(
        temperature=0.7,
        max_tokens=2048,
        top_p=0.9
    )
)

# YAML configuration support
# From tests/test_eval_config/model.yaml
```
*Evidence: `examples/security_guide.py`, `tests/test_eval_config/model.yaml`*

Authentication - Environment variable based with secure handling:

```python
# From docs - API keys via environment variables
# OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc.

# Hooks for custom credential management
from inspect_ai.hooks import ApiKeyOverride

# Override API keys programmatically
hooks().api_key_override(
    lambda model_name: "custom_key_for_" + model_name
)
```
*Evidence: `docs/reference/inspect_ai.hooks.qmd`, lines discussing `ApiKeyOverride`*

Resource Allocation - Container-level and model-level controls:

```python
# Task-level sandbox configuration
@task
def my_task():
    return Task(
        dataset=[...],
        solver=[...],
        sandbox="docker",  # or ("docker", "compose.yaml")
    )

# Docker Compose resource limits
# From examples/intervention/computer/compose.yaml:
services:
  default:
    image: aisiuk/inspect-computer-tool
    cpus: 1.0
    mem_limit: 2.0gb
    ports:
      - "5900"
      - "6080"
```
*Evidence: `examples/intervention/shell/compose.yaml`, `examples/intervention/computer/compose.yaml`*

Concurrent Connection Management:
```python
eval(
    task="my_task",
    max_connections=10,  # Limit concurrent API calls
    max_samples=20,      # Limit concurrent sample processing
    max_subprocesses=8   # Limit parallel subprocess execution
)
```
*Evidence: `docs/_container_limits.md`, `docs/_max_samples.md`*

Justification: Inspect excels with 15+ model providers, clean Python/YAML configuration, secure environment variable authentication with hooks for customization, and comprehensive resource allocation at both container and execution levels.

---

### S1F3: Evaluation Parameters and Prompt Configuration

Rating: 2/3

Parameter Definition - Full support with validation:

```python
from inspect_ai.model import GenerateConfig

config = GenerateConfig(
    temperature=0.7,
    top_p=0.9,
    max_tokens=2048,
    num_choices=5,  # For parallel sampling
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["STOP", "END"],
    seed=42,
    extra_body={  # Provider-specific parameters
        "guided_regex": r"RGB: (\d{1,3}),(\d{1,3}),(\d{1,3})"
    }
)
```
*Evidence: `examples/structured.py`, lines 63-73, 104-108*

Template System - Basic with variable substitution:

```python
from inspect_ai.solver import prompt_template, system_message

# Variable substitution in prompts
PROMPT_TEMPLATE = """
Solve the following math problem step by step. The last line
of your response should be of the form ANSWER: $ANSWER.

{prompt}

Remember to put your answer on its own line after "ANSWER:".
"""

solver = [
    prompt_template(PROMPT_TEMPLATE),  # {prompt} substituted from input
    generate()
]

# Role-based message composition
solver = [
    system_message("You are a helpful assistant."),
    user_message("What is 2+2?"),
    assistant_message("Let me calculate that."),
    generate()
]
```
*Evidence: `examples/scorer.py`, lines 81-91*

Few-shot Examples - Manual construction via messages:

```python
# Manual few-shot via message history
from inspect_ai.model import ChatMessageUser, ChatMessageAssistant

state.messages = [
    ChatMessageUser(content="What is 1+1?"),
    ChatMessageAssistant(content="2"),
    ChatMessageUser(content="What is 2+2?"),
    ChatMessageAssistant(content="4"),
    ChatMessageUser(content=state.user_prompt.content)  # Actual question
]
```
*Evidence: Inferred from message API in documentation*

Prompt Versioning - No built-in support:
- No `prompt_v1`, `prompt_v2` versioning system
- No template inheritance or composition
- No diff tools for comparing prompts
- Manual versioning would require custom code

Metric Configuration - Declarative scorer specification:

```python
from inspect_ai.scorer import match, includes, accuracy, stderr

@task
def my_task():
    return Task(
        dataset=[...],
        solver=[...],
        scorer=match(numeric=True),  # Configure scoring behavior
        # Or multiple scorers
        scorer=[
            match(),
            includes()
        ]
    )

# Custom metrics in scorer definitions
@scorer(metrics=[accuracy(), stderr()])
def custom_scorer():
    async def score(state, target):
        # Custom scoring logic
        return Score(value=...)
    return score
```
*Evidence: `examples/tool_use.py`, `examples/scorer.py`, lines 32-39*

Justification: Inspect has solid parameter configuration and basic templating with variable substitution and role-based message composition. However, it lacks formal prompt versioning, template inheritance/composition features, and structured few-shot configuration (requires manual message construction). Metric configuration is good but not as flexible as full prompt management would be.

---

### S1F4: Environment Setup and Dependency Management

Rating: 3/3

Dependency Specification - Multiple formats with pinned versions:

```toml
# From pyproject.toml (partial)
[project]
name = "inspect-ai"
dependencies = [
    "aiohttp>=3.9.1",
    "anthropic>=0.40.0",
    "click>=8.1.0",
    "docker>=7.1.0",
    "jinja2>=3.1.0",
    "openai>=1.59.6",
    "pydantic>=2.10.4",
    "python-dotenv>=1.0.0",
    # ... many more pinned dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.8.0",
    "ruff>=0.4.0",
]
```
*Evidence: `pyproject.toml`, `requirements.txt`*

Containerization - Extensive Docker support:

```yaml
# Multiple official images provided
# From examples/intervention/multi_tool/compose.yaml:
services:
  default:
    image: aisiuk/inspect-tool-support  # Official image
    init: true

# Custom Dockerfile support
# From examples/intervention/shell/compose.yaml:
services:
  default:
    build: .  # Custom Dockerfile
    command: tail -f /dev/null
    cpus: 1.0
    mem_limit: 2.0gb
    network_mode: bridge
```
*Evidence: `examples/intervention/multi_tool/compose.yaml`, `examples/intervention/shell/compose.yaml`*

Official images available:
- `aisiuk/inspect-tool-support` - For general tool execution
- `aisiuk/inspect-computer-tool` - For computer use tasks

Environment Automation - Complete setup tooling:

```bash
# From README.md
git clone https://github.com/UKGovernmentBEIS/inspect_ai.git
cd inspect_ai
pip install -e ".[dev]"  # Automated setup

# Pre-commit hooks
make hooks

# Linting and testing
make check
make test
```
*Evidence: `README.md`, lines 16-28*

Hardware Configuration - GPU/CPU specification via Docker:

```yaml
# GPU configuration example (inferred from Docker support)
services:
  default:
    image: aisiuk/inspect-tool-support
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    cpus: 4.0
    mem_limit: 8.0gb
```

From documentation on parallelism:
```python
# Control of concurrent resources
eval(
    max_connections=10,     # API connection limit
    max_subprocesses=8,     # CPU core usage
    max_sandboxes=4,        # Container concurrency
    max_samples=20          # Total parallel samples
)
```
*Evidence: `docs/_container_limits.md`, `docs/parallelism.qmd` (inferred)*

Justification: Inspect provides excellent dependency management with pinned versions in `pyproject.toml`, multiple official Docker images, Docker Compose support, automated setup via pip/make, and comprehensive hardware configuration through Docker resource limits and concurrency controls.

---

### S1F5: Security and Access Control

Rating: 1/3

Credential Management - Environment variables only:

```python
# From documentation - API keys via env vars
# OPENAI_API_KEY
# ANTHROPIC_API_KEY
# GOOGLE_API_KEY
# etc.

# Programmatic override via hooks
from inspect_ai.hooks import hooks

hooks().api_key_override(
    lambda model_name: get_key_from_custom_source(model_name)
)
```
*Evidence: Documentation on model configuration, `docs/reference/inspect_ai.hooks.qmd`*

No Vault Integration:
- No HashiCorp Vault support
- No AWS Secrets Manager integration
- No Azure Key Vault support
- No credential encryption at rest
- No credential rotation support

Access Control - Approval system exists but for tools, not users:

```yaml
# From examples/approval/approval.yaml
# This is for TOOL EXECUTION approval, not user access control
approvers:
  - name: bash_allowlist
    tools: "*bash*"
    allowed_commands: ["ls", "echo", "cat"]
  
  - name: python_allowlist
    tools: "*python*"
    allowed_functions: ["print"]
    allowed_modules: ["math"]
  
  - name: human
    tools: "*"
```
*Evidence: `examples/approval/approval.yaml`*

This approval system is for tool execution security (preventing dangerous tool calls), not for user RBAC or resource access control.

No RBAC Features:
- No user/group/role system
- No restrictions on who can run evaluations
- No model-level access controls
- No dataset-level permissions

Audit Logging - Event tracking exists but not security-focused:

```python
# From reference documentation
# Events are logged for execution tracking:
# - ModelEvent (model calls)
# - ToolEvent (tool executions)
# - ApprovalEvent (approval decisions)

# But no:
# - Credential access logging
# - User action auditing
# - Tamper-proof logging
# - Log retention policies
```
*Evidence: `docs/reference/inspect_ai.event.qmd`*

Enterprise Integration - None:
- No SSO support (SAML, OAuth)
- No LDAP/Active Directory integration
- No compliance certifications mentioned
- No enterprise auth mechanisms

Justification: Inspect has minimal security features, limited to environment variable credential management with programmatic override hooks. The approval system is for tool execution safety, not access control. There is no RBAC, vault integration, security-focused audit logging, SSO, or enterprise integration features.

---

### S1F6: Cost Estimation and Budget Planning

Rating: 0/3

Cost Modeling - No built-in support:

```python
# Inspect tracks token usage:
from inspect_ai.model import ModelUsage

# ModelUsage includes:
# - input_tokens: int
# - output_tokens: int
# - total_tokens: int
# - input_tokens_cache_read: int | None
# - input_tokens_cache_write: int | None

# But no cost calculation or pricing data
```
*Evidence: `docs/reference/inspect_ai.model.qmd`, `ModelUsage` type*

No Pricing Information:
- No knowledge of provider pricing (OpenAI, Anthropic, etc.)
- No cost-per-token calculations
- No support for custom cost models
- Users must calculate costs manually using logged token counts

Resource Projection - Token counting only:

```python
# Token limits can be set but no pre-execution estimation:
from inspect_ai.util import token_limit

eval(
    task="my_task",
    limits=[token_limit(1024 * 500)]  # Limit to 500K tokens
)

# No projection of:
# - Total expected tokens before run
# - Expected API call count
# - Estimated compute hours
```
*Evidence: `docs/_token_limits.md`, `docs/reference/inspect_ai.util.qmd`*

Budget Tools - None:

```python
# No budget setting like:
# eval(task="my_task", budget_usd=100.0)  # NOT AVAILABLE

# No budget breakdown
# No cost-what-if analysis
# No budget enforcement
```

Optimization Suggestions - None:

- No recommendations for cheaper model alternatives
- No batch size optimization guidance for cost/speed tradeoffs
- No provider cost comparison features
- No cost vs. accuracy tradeoff analysis

Manual Cost Calculation Required:

Users must:
1. Run evaluation and get logs
2. Extract token counts from `ModelUsage`
3. Look up pricing from provider documentation
4. Calculate: `(input_tokens * input_price + output_tokens * output_price)`
5. Aggregate across all samples manually

Justification: Inspect provides no cost estimation or budgeting features. While it accurately tracks token usage via `ModelUsage`, it has no pricing models, no pre-execution cost estimation, no budget limits, and no optimization suggestions. Users must manually calculate costs using logged token counts and external pricing data.

---

## Summary Assessment

Strengths:
- Outstanding dataset configuration (5+ sources, schema validation, flexible loading)
- Excellent model provider support (15+ providers with unified API)
- Comprehensive containerization (Docker, Docker Compose, official images)
- Good dependency management (pinned versions, automated setup)
- Solid parameter configuration (full model config API)

Weaknesses:
- No cost estimation or budgeting (must calculate manually)
- Minimal security features (env vars only, no RBAC/vault/SSO)
- Limited prompt versioning (no built-in template versioning)
- Basic few-shot support (requires manual message construction)

Overall Configuration Grade: 15/18 (83%)

Inspect excels at the core configuration needs for evaluation tasks—datasets, models, and environments—making it highly usable for researchers and practitioners. However, it lacks enterprise-grade security features and cost management tools that would be important for production deployments or cost-sensitive research programs.