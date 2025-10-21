# Evidently AI - Stage 1 (CONFIGURE) Evaluation

## Summary
Evidently AI is a Python library for ML/LLM evaluation and monitoring with minimal declarative configuration. While it excels at data definition and metric specification, it lacks traditional "configuration" in the sense of external config files, model provider abstractions, or cost estimation. Configuration happens primarily through Python code with data definition objects and metric declarations.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Basic pandas/dataframe support with schema via `DataDefinition`, no versioning |
| S1F2: Model Configuration | 1 | LLM judge support exists but minimal provider abstraction, no resource control |
| S1F3: Prompt Configuration | 2 | Template system with variables exists for LLM evals, basic few-shot, no versioning |
| S1F4: Environment Setup | 3 | Clean pip install, Docker support, pinned dependencies, clear setup |
| S1F5: Security & Access | 1 | Basic env vars only, no RBAC/audit/vault integration |
| S1F6: Cost Estimation | 0 | No cost estimation or budget features |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 2/3

Dataset Source Support:
Evidently supports loading data from pandas DataFrames, which can be sourced from various origins (CSV, Parquet, databases via pandas). However, the framework itself doesn't provide direct connectors:

```python
# From examples/cookbook/metrics.ipynb
reference = pd.DataFrame(reference_data)
current = pd.DataFrame(current_data)

# Dataset creation from pandas
reference_dataset = Dataset.from_pandas(
    pd.DataFrame(reference_data),
    data_definition=data_definition,
)
```

Schema Definition:
Schema is defined through `DataDefinition` with column types and task specifications:

```python
# From examples/cookbook/metrics.ipynb
data_definition=DataDefinition(
    text_columns=["Question", "Answer"],
    numerical_columns=["Rating", "Predicted Rating"],
    categorical_columns=["Feedback", "Predicted Feedback"],
    regression=[Regression(target="Score", prediction="Predicted Score")]
)
```

This provides basic type definition but lacks constraints (min/max values, string length limits, etc.).

Split Strategies:
No built-in split functionality. Users must manually split data using pandas/sklearn:

```python
# From examples/cookbook/regression_preset.ipynb
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    housing_data.data, 
    housing_data.target, 
    test_size=0.4, 
    random_state=42
)
```

Versioning:
No dataset versioning system found in the codebase.

Evidence:
- ✅ Supports pandas DataFrames (1 source natively)
- ✅ Schema via `DataDefinition` (basic types only)
- ❌ No declarative split strategies
- ❌ No versioning system

---

### S1F2: Model and Backend Configuration
Rating: 1/3

Provider Support:
Limited provider abstraction. LLM judges support OpenAI, Anthropic via basic provider string:

```python
# From examples/cookbook/prompt_optimization_code_review_example.ipynb
judge = LLMEval(
    alias="Code Review Judge",
    provider="openai",
    model="gpt-4o-mini",
    column_name="Generated review",
    template=feedback_quality
)
```

```python
# From examples/cookbook/datagen.ipynb
# Switching providers
options = AnthropicOptions(api_key=anthropic_api_key)
twitter_generator = FewShotDatasetGenerator(
    provider="anthropic",
    model="claude-sonnet-4-0",
    options=options
)
```

Configuration Method:
Configuration happens in Python code, not external files. No YAML/JSON config support for models:

```python
# All configuration is code-based
judge = LLMEval(
    provider="openai",
    model="gpt-4o-mini",
    # No external config file reference
)
```

Authentication:
Only environment variables mentioned:

```python
# From examples/cookbook/datagen.ipynb
# os.environ["OPENAI_API_KEY"] = "..."
import os
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "<put your key in env or here>")
```

Resource Allocation:
No GPU/CPU specification, batch size, or resource control found in examples or documentation.

Evidence:
- ⚠️ 2 providers (OpenAI, Anthropic) via string
- ❌ No YAML/JSON config files
- ⚠️ Environment variables only for auth
- ❌ No resource allocation features

---

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 2/3

Parameter Definition:
LLM parameters can be set but examples show minimal usage:

```python
# From examples/cookbook/datagen.ipynb
# No temperature, top_p shown in examples
# Model selection only
model="gpt-4o-mini"
```

Template System:
Good templating system with variable substitution and Jinja2 support:

```python
# From examples/cookbook/datagen.ipynb
my_template = \"\"\"
    Please answer in style of Darth Vader

    {% super() %}
\"\"\"

pa_generator = RagDatasetGenerator(
    data,
    query_template=my_template,
    response_template=my_template,
)
```

Few-shot Support:
Few-shot examples supported:

```python
# From examples/cookbook/datagen.ipynb
twitter_generator = FewShotDatasetGenerator(
    kind='twitter posts',
    examples=[
        "CI/CD is as crucial in AI systems as in traditional software. #mlops #cicd",
        "Without test coverage for your data pipelines, you're flying blind.",
    ]
)
```

Prompt Versioning:
No built-in versioning, but can save/load templates:

```python
# From examples/cookbook/prompt_optimization_code_review_example.ipynb
new_judge.template.dump("my_template.yaml")
template = BaseLLMPromptTemplate.load("my_template.yaml")
```

Metric Configuration:
Metrics defined via Python objects:

```python
# From examples/cookbook/metrics.ipynb
report = Report([
    MinValue(column="Rating"),
    MaxValue(column="Rating"),
    MeanValue(column="Rating"),
])
```

Evidence:
- ⚠️ Limited parameter config (model selection mainly)
- ✅ Good templating with Jinja2 and variable substitution
- ✅ Few-shot support
- ⚠️ Save/load templates but no version tracking
- ✅ Metric configuration via Python API

---

### S1F4: Environment Setup and Dependency Management
Rating: 3/3

Dependency Specification:
Well-defined dependencies with multiple formats:

```python
# From setup.py
install_requires=[
    "pandas>=1.4.0,<3.0.0",
    "scikit-learn>=1.0.0",
    "numpy>=1.22.0,<3.0.0",
    # ... many more pinned versions
]
```

```
# From requirements.min.txt
evidently>=0.5.2,<0.6.0
numpy>=1.22.0,<3.0.0
pandas>=1.4.0,<3.0.0
# Specific versions
```

Containerization:
Official Docker images and Dockerfiles provided:

```dockerfile
# From docker/Dockerfile.service
FROM python:3.11-slim
# ... setup steps
```

```yaml
# From examples/llm_eval_grafana_dashboard/docker-compose.yml
services:
  db:
    image: postgres:15
  grafana:
    image: grafana/grafana:latest
```

Environment Automation:
Standard Python setup with pip:

```bash
# From README.md
pip install evidently
# or
conda install -c conda-forge evidently
```

```bash
# From examples/service/README.md
bash run_service.sh
# or
evidently ui
```

Hardware Configuration:
Not explicitly documented in configuration files, but Docker support allows infrastructure-as-code.

Evidence:
- ✅ Pinned dependencies in setup.py and requirements files
- ✅ Official Dockerfiles and Docker Compose examples
- ✅ Simple pip/conda install
- ⚠️ No explicit GPU/hardware config (relies on Docker/system)

---

### S1F5: Security and Access Control
Rating: 1/3

Credential Management:
Only environment variables shown:

```python
# From examples/service/docker_s3_tutorial.ipynb
docker run -d -p 8000:8000 \
  -e FSSPEC_S3_KEY="minioadmin" \
  -e FSSPEC_S3_SECRET="minioadmin" \
  -e FSSPEC_S3_ENDPOINT_URL="http://host.docker.internal:9000"
```

No vault integration or credential rotation mentioned.

Access Control:
No RBAC, user/group/role system found. The UI service example shows basic setup without access controls:

```python
# From examples/service/workspace_tutorial.ipynb
ws = Workspace.create("workspace")
project = ws.create_project("My Project")
# No user/permission specification
```

Audit Logging:
No audit logging features found in examples or documentation provided.

Enterprise Integration:
No SSO, LDAP, or compliance features mentioned.

Evidence:
- ⚠️ Environment variables only
- ❌ No RBAC or access control
- ❌ No audit logging
- ❌ No enterprise integration

---

### S1F6: Cost Estimation and Budget Planning
Rating: 0/3

Cost Modeling:
No cost estimation features found in any examples or documentation:

```python
# No cost estimation APIs found
# Examples run LLM calls without cost projection
await optimizer.arun(executor=judge, scorer="accuracy", dataset=dataset, repetitions=5)
# No cost output or budget warnings
```

Resource Projection:
No token counting or API call projection before execution.

Budget Tools:
No budget limits, cost breakdown, or optimization suggestions found.

Evidence:
- ❌ No cost estimation
- ❌ No resource projection
- ❌ No budget tools
- ❌ No cost optimization features

---

## Key Strengths

1. Clean Python API: Strong declarative API for metrics and data definitions
2. Good Templating: Jinja2-based prompt templates with variables
3. Excellent Setup: Simple installation, Docker support, pinned deps
4. Rich Metrics: 100+ built-in metrics for various ML/LLM tasks
5. Monitoring UI: Optional UI service for visualization

## Key Weaknesses

1. No Config Files: Everything is Python code, no YAML/JSON configs
2. Minimal Provider Abstraction: Limited LLM provider support
3. No Cost Features: Zero cost estimation or budget management
4. No Security Layer: Basic env vars only, no RBAC/audit
5. No Versioning: No dataset or prompt version tracking
6. Limited Resource Control: No GPU allocation, batch size optimization

## Use Case Fit

Good For:
- Python-first teams comfortable with code-based configuration
- Single-user or team environments without complex access needs
- Monitoring and evaluation workflows
- Teams with existing cost tracking infrastructure

Not Ideal For:
- Teams needing declarative YAML/JSON configuration
- Multi-tenant environments requiring RBAC
- Cost-sensitive projects needing budget controls
- Teams requiring credential rotation/vault integration
- Projects needing dataset/prompt versioning