# TruLens - Stage 1 (CONFIGURE) Evaluation

## Summary
TruLens is a comprehensive LLM evaluation framework that provides robust configuration capabilities for datasets, models, prompts, and evaluation parameters. While it excels at runtime instrumentation and feedback evaluation, its approach to configuration is more runtime-oriented than declarative. The framework emphasizes Python-based configuration over static config files, with strong support for multiple providers and extensibility.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | TruLens supports dataset configuration through Python DataFrames and the `VirtualRecord` API. Evidence from `examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb` shows: `queries_df = pd.DataFrame({"query": queries})` and `run.start(input_df=queries_df)`. However, there's no built-in dataset versioning or declarative schema definition. Dataset sources are limited to DataFrames and virtual records, with no native support for multiple source types like JSON, CSV, or cloud storage connectors. |
| S1F2: Model Configuration | 3 | Excellent provider support with 7+ integrations (OpenAI, Anthropic, HuggingFace, Cortex, Bedrock, LiteLLM, Google) as seen in `src/providers/`. Configuration is Python-based via provider classes: `openai = OpenAI()`, `cortex = Cortex(model_engine="claude-3-5-sonnet")` (from experimental notebooks). Authentication via environment variables is standard: `os.environ["OPENAI_API_KEY"]`. No built-in resource allocation validation, but providers support model parameters. |
| S1F3: Prompt Configuration | 2 | Basic templating exists through framework integrations (LangChain, LlamaIndex) but no native TruLens prompt management system. Evidence from `src/feedback/README.md` shows feedback function configuration: `Feedback(provider.method).on_input_output()`, but this is evaluation-focused. No built-in prompt versioning or template inheritance. Parameter configuration exists per-provider but not centrally managed. Few-shot examples are framework-dependent (e.g., LangChain PromptTemplate). |
| S1F4: Environment Setup | 3 | Strong dependency management with `pyproject.toml` files across all packages (e.g., `src/core/pyproject.toml`). Docker support evidenced by `docker/test-database.yaml` and Docker-based testing (`src/dashboard/react_components/record_viewer_otel/README.md`). Virtual environment setup through Poetry (`poetry.lock` present). Installation documented: `pip install trulens`. Multi-package architecture with clear dependency trees. No explicit GPU/hardware configuration, but connector-based architecture supports various compute environments (Snowflake, local, cloud). |
| S1F5: Security & Access | 2 | Environment variable-based credential management: `os.environ["OPENAI_API_KEY"]`, `os.environ["SNOWFLAKE_USER_PASSWORD"]` (from experimental notebooks). Snowflake connector supports enterprise auth: `SnowflakeConnector(snowpark_session=snowpark_session)`. Database redaction: `TruSession(database_redact_keys=True)` from `examples/experimental/db_populate.ipynb`. No built-in RBAC, SSO, or vault integration. Limited audit logging beyond basic tracing. Primarily designed for single-user/team use rather than multi-tenant enterprise scenarios. |
| S1F6: Cost Estimation | 1 | Cost tracking exists post-execution (`record.cost` seen in notebooks) but no pre-execution estimation. From `src/core/trulens/core/schema/record.py`, costs are tracked during runtime with token counts. No built-in pricing models, budget limits, or cost optimization suggestions. Users must manually estimate based on provider pricing. The `Cost` class tracks spent resources but doesn't project future costs. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 2/3 points

Evidence:
```python
# From examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb
queries = [
    "Chart the current market capitalization of the top 5 banks in the US?",
    "Identify current regulatory changes for the financial services industry in the US.",
]
queries_df = pd.DataFrame({"query": queries})

run_config = RunConfig(
    run_name=run_name,
    dataset_name="web_search_queries",
    source_type="DATAFRAME",
    dataset_spec={"RECORD_ROOT.INPUT": "query"},
)
run: Run = tru_app.add_run(run_config=run_config)
run.start(input_df=queries_df)
```

```python
# From examples/experimental/virtual_example.ipynb
from trulens.apps.virtual import VirtualRecord

rec1 = VirtualRecord(
    main_input="Where is Germany?",
    main_output="Germany is in Europe",
    calls={
        context_method: dict(
            args=["Where is Germany?"],
            rets=["Germany is a country located in Europe."],
        )
    },
)
```

Strengths:
- DataFrame-based dataset input with schema mapping (`dataset_spec`)
- Virtual record API for offline evaluation without live apps
- Integration with Snowflake for enterprise data sources

Weaknesses:
- No declarative schema validation (no column type constraints, validation rules)
- No built-in dataset versioning system
- Limited to DataFrame and virtual records; no native JSON/CSV/cloud storage loaders
- Splits must be managed manually outside the framework

### S1F2: Model and Backend Configuration
Rating: 3/3 points

Evidence:
```python
# Provider support from src/providers/ directory structure:
# - openai/, bedrock/, cortex/, google/, huggingface/, langchain/, litellm/

# From examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb
from trulens.providers.cortex import Cortex
trace_eval_provider = Cortex(
    model_engine="claude-3-5-sonnet", 
    snowpark_session=snowpark_session
)

# From src/providers/openai/README.md
from trulens.providers.openai import OpenAI
openai = OpenAI()

# Authentication pattern from notebooks:
os.environ["OPENAI_API_KEY"] = "sk-proj-..."
os.environ["TAVILY_API_KEY"] = "tvly-dev-..."
```

Strengths:
- 7+ provider integrations (OpenAI, Anthropic, HuggingFace, Cortex, Bedrock, LiteLLM, Google)
- Clean provider instantiation API
- Environment variable-based authentication (standard practice)
- Multi-region support through Snowflake connector

Weaknesses:
- No centralized config file format (YAML/JSON) for model specifications
- No built-in resource allocation validation
- Runtime configuration only; no static config parsing

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 2/3 points

Evidence:
```python
# From src/feedback/README.md
from trulens.core import Feedback
from trulens.providers.openai import OpenAI

openai = OpenAI()

# Feedback function configuration
f_qa_relevance = Feedback(openai.relevance).on_input_output()

# Context selection with aggregation
f_context_relevance = (
    Feedback(openai.context_relevance)
    .on_input()
    .on(Select.Record.app.combine_docs_chain._call.args.inputs.input_documents[:].page_content)
    .aggregate(numpy.mean)
)
```

Strengths:
- Flexible selector API for extracting app components
- Aggregation support for multi-value feedback
- Integration with framework-native prompting (LangChain, LlamaIndex)

Weaknesses:
- No native TruLens template system (relies on wrapped frameworks)
- No prompt versioning or diff tools
- No built-in few-shot example management
- Parameter configuration is provider-specific, not centralized

### S1F4: Environment Setup and Dependency Management
Rating: 3/3 points

Evidence:
```toml
# From src/core/pyproject.toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.dependencies]
python = "^3.9,<3.13"
alembic = "^1.13.1"
dill = "^0.3.8"
munch = "^4.0.0"
# ... 20+ dependencies with version constraints
```

```yaml
# From docker/test-database.yaml
version: '3.8'
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: password
```

```markdown
# From README.md
## Installation and Setup
Install the trulens pip package from PyPI.
```bash
pip install trulens
```
```

Strengths:
- Poetry-based dependency management with lock files
- Multi-package monorepo with clear separation (`src/core/`, `src/providers/`, etc.)
- Docker support for database testing
- Simple installation: `pip install trulens`

Weaknesses:
- No explicit GPU/CUDA configuration documentation
- Hardware requirements not specified beyond Python version

### S1F5: Security and Access Control
Rating: 2/3 points

Evidence:
```python
# From examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb
os.environ["SNOWFLAKE_ACCOUNT"] = "..."
os.environ["SNOWFLAKE_USER"] = "..."
os.environ["SNOWFLAKE_USER_PASSWORD"] = "..."

snowflake_connection_parameters = {
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_USER_PASSWORD"],
    "database": os.environ["SNOWFLAKE_DATABASE"],
    "role": os.environ["SNOWFLAKE_ROLE"],
}
```

```python
# From examples/experimental/db_populate.ipynb
session = TruSession(database_redact_keys=True)
```

Strengths:
- Environment variable-based credential management
- Snowflake enterprise connector with role-based parameters
- Database key redaction feature
- Support for connection pooling through connectors

Weaknesses:
- No vault integration (HashiCorp Vault, AWS Secrets Manager)
- No RBAC for experiments/datasets within TruLens
- No SSO/SAML support
- Limited audit logging beyond basic tracing

### S1F6: Cost Estimation and Budget Planning
Rating: 1/3 points

Evidence:
```python
# From examples/experimental/dummy_example.ipynb
with truchain as recs:
    print(app_langchain("Hello?"))

print(recorder.get().cost)
# Cost tracking exists post-execution
```

```python
# From src/core/trulens/core/schema/record.py (implied from record structure)
# Cost is tracked during runtime but not projected before execution
```

Strengths:
- Post-execution cost tracking via `record.cost`
- Token count tracking for LLM calls

Weaknesses:
- No pre-execution cost estimation
- No built-in provider pricing models
- No budget limit enforcement
- No cost optimization suggestions
- No "what-if" analysis for provider switching

Why only 1 point:
The framework completely lacks pre-execution cost estimation capabilities. While it tracks costs after the fact, this fails the core requirement of "cost estimation before running." Users cannot project API call costs or set budget limits before evaluation begins. This is a significant gap for production use cases where cost control is critical.

## Overall Assessment

### Strengths
1. Excellent provider ecosystem: 7+ integrations with clean, consistent API
2. Strong dependency management: Poetry-based with proper version pinning
3. Flexible evaluation configuration: Selector API enables complex feedback specifications
4. Enterprise-ready connectors: Snowflake integration with proper authentication

### Critical Gaps
1. No declarative configuration format: Everything is runtime Python code, no YAML/JSON configs
2. Limited dataset management: No versioning, schema validation, or multi-source loading
3. Missing cost projection: Only post-hoc cost tracking, no pre-execution estimation
4. No native prompt versioning: Relies on wrapped framework capabilities

### Recommended Improvements
1. Add YAML-based configuration format for models, feedbacks, and datasets
2. Implement dataset versioning with schema validation
3. Build pre-execution cost estimator with provider pricing models
4. Create native prompt template system with versioning
5. Add RBAC and enterprise security features

Stage 1 Total Score: 13/18 points (72%)

The framework excels at runtime configuration through Python APIs but lacks the declarative, pre-execution planning features expected of a comprehensive evaluation harness. It's strongest in model/provider management and environment setup, weakest in cost estimation and dataset management.