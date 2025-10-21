# OpenAI Evals - Stage 1 (CONFIGURE) Evaluation

## Summary
OpenAI Evals is a well-established framework for evaluating LLMs with strong dataset handling and model configuration capabilities. It excels at defining evaluation tasks but has minimal environment automation and limited security/cost features. Configuration is primarily code-based rather than declarative, which provides flexibility but requires more technical expertise.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Evidence: The framework supports multiple dataset sources (JSON, JSONL, HuggingFace) as shown in `evals/registry/data/` directories. However, dataset registration is implicit through file placement rather than a formal API. From `evals/data.py`: datasets are loaded via `get_jsonl` and `get_jsonls` functions without explicit schema definition. The registry system (`evals/registry.py`) provides basic versioning through YAML files but lacks advanced features like schema validation or computed splits. Example: Dataset files are simply placed in `evals/registry/data/<eval_name>/` with no declarative schema. |
| S1F2: Model Configuration | 2 | Evidence: Supports 3-4 providers (OpenAI models primarily, with some LangChain integration as seen in `evals/completion_fns/langchain_llm.py`). Configuration is through YAML registries (`evals/registry/completion_fns/`) and environment variables. From `evals/api.py`, authentication is via `OPENAI_API_KEY` environment variable. Example from docs: "After you obtain an API key, specify it using the `OPENAI_API_KEY` environment variable". Resource allocation is limited - no GPU specification in configs. The solver system provides some abstraction but model config is basic. |
| S1F3: Prompt Configuration | 2 | Evidence: Basic templating exists but varies by eval. Some evals use simple Python string formatting (e.g., `task_description.format(...)` in various elsuite evals), others have more structured approaches. From `evals/prompt/base.py`, there's minimal prompt infrastructure. Example from ballots eval: Prompts are in `prompts.py` files using basic Python strings with `.format()`. No unified templating engine like Jinja2. Versioning is manual through git rather than built-in. Few-shot support exists but must be manually implemented per eval. No centralized metric configuration - metrics are hardcoded in eval classes. |
| S1F4: Environment Setup | 2 | Evidence: Provides `pyproject.toml` with dependencies, but setup varies significantly by eval. From README: "pip install -e ." for basic setup, but many evals require additional steps. Example from hr_ml_agent_bench: Requires separate `requirements.txt` files per task and manual Docker setup. The multistep_web_tasks eval README notes: "The eval may require manual downloading of some docker images...mirrors are unreliable." No containerization by default (some evals provide Docker but not standardized). Hardware requirements are documented per-eval but not enforceable. |
| S1F5: Security & Access | 1 | Evidence: Security is minimal. Authentication is via environment variables only (`OPENAI_API_KEY`). From README: "Please be aware of the costs associated with using the API when running evals" but no built-in budget controls. From hr_ml_agent_bench README: "⚠️ Warning: This eval allows language models to run arbitrary code on your machine." No RBAC, no vault integration, no SSO. Optional Snowflake logging mentioned (`SNOWFLAKE_*` env vars) but no audit trail by default. The framework trusts the environment completely with no sandboxing unless manually implemented. |
| S1F6: Cost Estimation | 1 | Evidence: No built-in cost estimation. Token usage is tracked post-execution in logs (`evals/record.py` shows token counting), but no pre-run estimation. Example: Most eval READMEs include "Token Usage Estimates" sections with manually calculated ranges like "Below is a rough estimate of the total number of tokens consumed." No API for querying costs, no budget limits, no optimization suggestions. Users must manually calculate costs from token counts using external pricing information. The framework provides token counting but no cost modeling. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 2)

Strengths:
- Supports multiple formats: JSON, JSONL, CSV implicitly through Python loaders
- Registry system provides organization (`evals/registry/data/`)
- HuggingFace integration exists in some evals (e.g., `elsuite/imdb`)

Weaknesses:
- No formal dataset registration API - just file placement
- No schema definition capability - schemas are implicit from data structure
- Split strategies must be manually implemented per eval (no declarative splits)
- Versioning is via git/filenames, not a formal version tracking system

Evidence:
```python
# From evals/data.py - simple file loading, no schema
def get_jsonl(path: str) -> list[dict]:
    with open(path, "r") as f:
        return [json.loads(line) for line in f]
```

### S1F2: Model and Backend Configuration (Rating: 2)

Strengths:
- Clean YAML-based solver registry system
- Supports OpenAI models comprehensively
- Some extensibility through completion function protocol

Weaknesses:
- Limited provider support beyond OpenAI (3-4 providers max)
- Authentication only via environment variables (no vault integration)
- No resource allocation specification (GPU/CPU assignment)
- Validation is runtime, not configuration-time

Evidence:
```yaml
# From evals/registry/completion_fns/ - basic model config
gpt-4:
  class: evals.completion_fns.openai:OpenAICompletionFn
  args:
    model: gpt-4
```

### S1F3: Evaluation Parameters and Prompt Configuration (Rating: 2)

Strengths:
- Parameters can be set per-model in YAML configs
- Some evals have structured prompt systems

Weaknesses:
- No unified templating engine (each eval rolls its own)
- Prompt versioning is manual via git
- Few-shot support varies by eval, not framework-level
- No centralized metric configuration system

Evidence:
```python
# From elsuite/ballots/prompts.py - basic string formatting
TASK_DESCRIPTION = """
I have an important task for you...
{inputs}
"""
# No Jinja2, no inheritance, no composition system
```

### S1F4: Environment Setup and Dependency Management (Rating: 2)

Strengths:
- Provides `pyproject.toml` with core dependencies
- Some evals include Docker configurations
- Make commands for setup exist

Weaknesses:
- Inconsistent setup across evals (some require manual steps)
- Docker not standardized across framework
- Hardware requirements documented but not validated
- Multi-step setup for complex evals (hr_ml_agent_bench requires GPU, Docker, etc.)

Evidence:
From multistep_web_tasks README: "The eval may require manual downloading of some docker images. The webhosting mirrors are unreliable."

### S1F5: Security and Access Control (Rating: 1)

Strengths:
- Optional Snowflake logging integration
- Some evals include sandboxing warnings

Weaknesses:
- No RBAC, no user management
- Authentication only via environment variables
- No credential encryption or rotation
- No audit logging by default
- No enterprise integration (SSO, LDAP)
- Framework allows arbitrary code execution in some evals

Evidence:
From README: "specify it using the `OPENAI_API_KEY` environment variable"
From hr_ml_agent_bench: "⚠️ Warning: This eval allows language models to run arbitrary code"

### S1F6: Cost Estimation and Budget Planning (Rating: 1)

Strengths:
- Token counting in logs post-execution
- Many eval READMEs include token estimates

Weaknesses:
- No pre-run cost estimation
- No budget limit enforcement
- Token estimates are manually calculated and documented
- No cost optimization suggestions
- Users must look up pricing externally

Evidence:
Token usage is tracked in `evals/record.py` but only logged after execution. READMEs state: "Below is a rough estimate of the total number of tokens consumed" - all manual calculations.

## Key Observations

1. Code-First Philosophy: Configuration is primarily code-based rather than declarative, which gives flexibility but requires technical expertise
2. Eval-Specific Patterns: Many configuration aspects vary by eval rather than being framework-level features
3. Production Gaps: Minimal security, cost control, and enterprise features suggest focus on research rather than production use
4. Strong Core, Weak Periphery: Excellent at the core evaluation task but lacks supporting infrastructure for environment management and safety

## Overall Stage 1 Score: 10/18 (55.6%)

The framework demonstrates competent configuration capabilities for its primary use case (academic/research LLM evaluation) but lacks the comprehensive configuration features needed for production deployment, particularly in security, cost control, and environment automation.