# Giskard - Stage 1 (CONFIGURE) Evaluation

## Summary
Giskard is an open-source testing framework for ML models (tabular, NLP, LLM, vision) with a focus on automated vulnerability detection and test generation. The framework demonstrates solid configuration capabilities across dataset handling, model integration, and LLM evaluation, but lacks comprehensive cost estimation, security features, and advanced environment management tooling found in production-grade evaluation platforms.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Evidence: Multiple source support exists but with limitations. From `giskard/datasets/base/__init__.py`, datasets can be created from pandas DataFrames with schema definition via `cat_columns`, `column_types`. From examples in `docs/integrations/mlflow/mlflow-llm-example.ipynb`, data loading from PDFs via PyPDFLoader is shown. However, there's no declarative dataset registry system - users must manually load data. Split strategies are manual (users must pre-split data before wrapping). No built-in versioning system for datasets. Code snippet from Dataset class shows basic wrapping: `Dataset(df=df, target="Survived", cat_columns=['Pclass', 'Sex', "SibSp", "Parch", "Embarked"])`. Missing: declarative source connectors, automated split strategies, version tracking API. |
| S1F2: Model Configuration | 2 | Evidence: Good provider support (5+ frameworks) but basic configuration. From `giskard/models/` directory, supports sklearn, pytorch, tensorflow, catboost, huggingface, langchain. Configuration via Python API only: `Model(model=model, model_type="classification")`. From `giskard/llm/client/` shows OpenAI/Mistral/Claude client support. Authentication via environment variables only (`OPENAI_API_KEY` in examples). No YAML/JSON config files, no resource allocation specifications, no validation before execution. Code example from README: `giskard_model = giskard.Model(model=model_predict, model_type="text_generation", name="Climate Change QA", description="...", feature_names=["question"])`. Missing: declarative config files, resource specs, pre-execution validation. |
| S1F3: Prompt Configuration | 2 | Evidence: Basic templating exists for LLM use cases but limited versioning. From `docs/reference/notebooks/LLM_QA_IPCC.ipynb`, shows prompt templates: `PROMPT_TEMPLATE = """You are the Climate Assistant...\nContext:\n{context}\n\nQuestion:\n{question}"""` with `PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["question", "context"])`. No built-in few-shot support, no prompt versioning system, no parameter sweeps. Metric configuration exists via `giskard/scanner/` detectors but not declaratively configured. Missing: Jinja2 templating engine, prompt versioning API, few-shot injection system, parameter sweep configuration. |
| S1F4: Environment Setup | 2 | Evidence: Standard Python packaging but minimal automation. From `pyproject.toml`: Uses PDM with dependencies specified. No official Docker images provided (checked repository structure). `docs/open_source/installation_library/index.md` shows basic pip install: `pip install "giskard[llm]" -U`. From `docs/community/contribution_guidelines/dev-environment.md`: Manual setup with PDM: `pdm install`. Dependencies pinned in `pdm.lock` but no container support. Missing: Official Dockerfiles, automated setup scripts, hardware requirement specifications, compatibility checks. Only supports Python 3.9-3.11 explicitly. |
| S1F5: Security & Access | 1 | Evidence: Minimal security features. From examples, credentials managed via environment variables only: `os.environ['OPENAI_API_KEY'] = "sk-XXX"` in `docs/integrations/mlflow/mlflow-llm-example.ipynb`. No RBAC system found in codebase. No audit logging for model access. From `giskard/utils/analytics_collector.py`: Basic analytics but not security-focused logging. Code snippet shows basic env var usage only. Missing: Vault integration, RBAC, audit logs, SSO support, encryption at rest, enterprise security features. This is an open-source library focused on testing, not a multi-user platform. |
| S1F6: Cost Estimation | 1 | Evidence: No cost estimation capabilities found. Searched `giskard/` directory for cost/budget/pricing features - none exist. From `giskard/llm/client/`, clients call APIs but don't track costs. No token counting before execution, no budget limits, no cost modeling. The scanner in `giskard/scanner/` runs tests but provides no cost estimates. Missing: Cost estimation API, token counting, budget limits, provider pricing knowledge, optimization suggestions. This feature is completely absent from the framework. |

## Key Strengths

1. Strong Model Integration: Excellent support for diverse model types (sklearn, pytorch, tensorflow, huggingface, langchain) with clear wrapper patterns in `giskard/models/` directory.

2. LLM Focus: Dedicated LLM evaluation capabilities with prompt templates, RAG support (see `giskard/rag/`), and vulnerability scanning specifically for LLMs (hallucination, prompt injection detection).

3. Vulnerability Detection: Core strength in automated scanning (`giskard/scanner/`) with issue detection across multiple categories (performance bias, robustness, security).

4. Good Documentation: Extensive tutorials (40+ notebooks in `docs/reference/notebooks/`) covering tabular, NLP, LLM, RAG, and vision use cases with concrete examples.

## Critical Gaps

1. No Cost Management: Complete absence of cost estimation, budget controls, or token counting features essential for production LLM evaluation.

2. Limited Security: Environment variable-only authentication, no RBAC, no enterprise security features. Not suitable for multi-user production environments.

3. Manual Configuration: No declarative config files (YAML/JSON), everything requires Python code. No configuration validation before execution.

4. Basic Environment Setup: No containerization support, no hardware specifications, minimal automation for reproducibility.

5. Primitive Dataset Management: No dataset versioning, no declarative source connectors, manual split management, no metadata tracking beyond basic column types.

6. No Prompt Versioning: While prompt templates exist, there's no versioning system for tracking prompt iterations or comparing versions.

## Evidence of Configuration Philosophy

From `README.md`: "Install the latest version of Giskard from PyPi using pip: `pip install "giskard[llm]" -U`"

The framework focuses on code-first configuration rather than declarative approaches. Users wrap models/datasets in Python:

```python
# From README.md
giskard_model = giskard.Model(
    model=model_predict,
    model_type="text_generation",
    name="Climate Change Question Answering",
    description="This model answers any question about climate change based on IPCC reports",
    feature_names=["question"],
)
```

This approach works well for data scientists doing exploratory testing but lacks the production-readiness of frameworks with declarative configuration, environment automation, and enterprise security.

## Recommendations for Improvement

1. Add Cost Estimation Module: Create `giskard/cost/` with token counting and budget tracking before execution.
2. Implement Configuration Files: Support YAML/JSON configs for models, datasets, and scan parameters.
3. Build Dataset Registry: Add versioning, declarative source connectors, and automated split strategies.
4. Enhance Security: Add basic RBAC and secure credential management (at minimum, credential file encryption).
5. Provide Docker Support: Create official Docker images with pinned dependencies.
6. Add Prompt Versioning: Create prompt registry with version tracking and diff capabilities.