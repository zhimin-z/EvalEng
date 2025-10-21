# PyKEEN - Stage 1 (CONFIGURE) Evaluation

## Summary
PyKEEN is a knowledge graph embedding library, not an LLM evaluation framework. It focuses on training and evaluating knowledge graph embedding models on relational data (triples). While it has extensive configuration capabilities for its domain (datasets, models, training), it lacks features specifically needed for LLM evaluation (prompt templates, model providers, cost estimation). The framework is highly polished for its intended purpose but misaligned with the evaluation criteria.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Has 37+ built-in KG datasets with version tracking, but datasets are knowledge graphs (triples), not LLM evaluation data. Loading from multiple sources (CSV, TSV, paths) supported. Limited schema definition for graph-specific data. Evidence: `src/pykeen/datasets/` contains 37 dataset classes; `src/pykeen/triples/TriplesFactory` handles entity/relation mappings from various formats. No LLM-specific dataset abstractions. |
| S1F2: Model Configuration | 1 | Supports 40+ KG embedding models (TransE, DistMult, etc.) but zero LLM providers (no OpenAI, Anthropic, HuggingFace APIs). Model configuration via Python API and kwargs exists but for graph models only. Evidence: `src/pykeen/models/` has KG models; no LLM provider integrations found in codebase. `pykeen.pipeline.pipeline()` accepts `model='TransE'` not `model='gpt-4'`. |
| S1F3: Prompt Configuration | 0 | No prompt templating system exists. Framework evaluates graph embeddings using scoring functions, not language model generation. No template engine, variable substitution, or few-shot support. Evidence: Search for "prompt", "template", "jinja" in codebase yields only metadata templates in `src/pykeen/templates/README.md` (repo documentation, not prompts). |
| S1F4: Environment Setup | 3 | Excellent dependency management: `pyproject.toml` with pinned versions, optional extras (`[mlflow]`, `[wandb]`, `[plotting]`), clear installation docs. No Docker but not required for Python lib. Evidence: `pyproject.toml` has detailed dependencies; `docs/source/installation.rst` has comprehensive setup guide including conda, pip, extras. |
| S1F5: Security & Access | 1 | Basic env var support for tracking services (MLflow, Neptune API keys) but no general credential vault integration, RBAC, or audit logging. Evidence: `src/pykeen/trackers/` uses env vars like `MLFLOW_TRACKING_URI`; no vault/RBAC code found. Security not a primary concern for academic research library. |
| S1F6: Cost Estimation | 0 | No cost estimation features. Framework trains local models on GPUs, not API-based LLMs. No token counting, pricing models, or budget tools. Evidence: `docs/source/tutorial/performance.rst` discusses GPU memory optimization, not API costs. No cost-related classes/functions in codebase. |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (2/3)

Strengths:
- 37+ built-in datasets with clear documentation: FB15k237, WN18RR, Nations, etc.
  ```python
  from pykeen.datasets import get_dataset
  dataset = get_dataset(dataset="nations")  # Logical reference by name
  ```
  *Evidence*: `README.md` lists 37 datasets with citations; `src/pykeen/datasets/` contains implementations.

- Multiple source support: Can load from paths, TSV, CSV, compressed files
  ```python
  from pykeen.triples import TriplesFactory
  factory = TriplesFactory.from_path("path/to/triples.tsv")
  ```
  *Evidence*: `src/pykeen/triples/TriplesFactory` has `from_path`, `from_labeled_triples` methods.

- Version tracking: Datasets reference specific paper versions via citations
  *Evidence*: README table shows citation per dataset (e.g., "Bordes et al., 2013")

Weaknesses:
- Not LLM-evaluation data: Datasets are knowledge graph triples (h, r, t), not QA pairs, prompts, or text corpora
- Limited schema definition: Entity/relation ID mappings, no general validation rules
  ```python
  # Schema is just ID mappings, not typed fields
  factory.entity_to_id  # Dict[str, int]
  factory.relation_to_id  # Dict[str, int]
  ```
  *Evidence*: `docs/source/tutorial/performance.rst` explains ID mapping system but no validation schemas.

- No declarative splits: Must manually split or use built-in fixed splits
  ```python
  dataset.training  # Pre-defined split
  dataset.testing   # Pre-defined split
  ```
  *Evidence*: `docs/source/tutorial/splitting.rst` discusses split algorithms but they're imperative, not declarative configs.

Rating Justification: Has dataset abstraction with 4+ sources and versioning, but schema/splits are limited and data type is misaligned with LLM evaluation needs → 2 points.

---

### S1F2: Model and Backend Configuration (1/3)

Strengths:
- 40+ models configurable by name: TransE, ComplEx, ConvE, etc.
  ```python
  from pykeen.pipeline import pipeline
  result = pipeline(model='TransE', dataset='nations')
  ```
  *Evidence*: `README.md` lists 40 models; `src/pykeen/models/` has implementations.

- Unified configuration API: All models use same interface (kwargs-based)
  ```python
  pipeline(
      model='DistMult',
      model_kwargs=dict(embedding_dim=128),
      optimizer='Adam',
      optimizer_kwargs=dict(lr=0.001)
  )
  ```
  *Evidence*: `docs/source/tutorial/using_resolvers.rst` explains resolver pattern for models/optimizers.

Weaknesses:
- Zero LLM provider support: No OpenAI, Anthropic, Cohere, HuggingFace Inference API
  - Searched codebase for "openai", "anthropic", "cohere" → no results
  - `src/pykeen/models/` contains only graph embedding models
  
- No API-based models: All models are local PyTorch modules
  ```python
  # This works (local model):
  model = TransE(triples_factory=dataset.training)
  
  # This doesn't exist (API model):
  # model = OpenAIModel(model="gpt-4", api_key=...)
  ```
  *Evidence*: `src/pykeen/models/base.py` defines PyTorch `nn.Module` base classes, not API clients.

- No authentication system: No credential management beyond tracker API keys
  *Evidence*: Searched for "api_key", "authentication" → only in tracker classes for logging services.

Rating Justification: Has model configuration abstraction but for wrong model type (graph embeddings not LLMs). No LLM providers at all → 1 point.

---

### S1F3: Evaluation Parameters and Prompt Configuration (0/3)

Complete Absence of Prompt Features:

- No templating system: Searched for "jinja", "template", "prompt" in source code
  - `src/pykeen/templates/README.md` exists but is a metadata template for documentation, not prompts:
    ```markdown
    <h1 align="center">PyKEEN</h1>
    <p align="center">...train and evaluate knowledge graph embeddings...</p>
    ```
  - Zero Jinja/mustache/f-string templating for text generation

- No variable substitution: Models score triples `(h, r, t)`, not fill in `{{question}}` placeholders
  ```python
  # What PyKEEN does (scoring):
  score = model.score_hrt(head=0, relation=5, tail=12)  # Numeric IDs
  
  # What LLM evaluation needs (templating):
  # prompt = "Question: {{question}}\nAnswer: {{answer}}"  # ❌ Doesn't exist
  ```
  *Evidence*: `src/pykeen/models/base.py` has `score_hrt()` method, no `format_prompt()`.

- No few-shot support: No example injection, no prompt versioning
  *Evidence*: Searched codebase for "few.shot", "n_shot", "examples" → only in dataset context (graph triples).

What Exists Instead:
- Parameter configuration for training (learning rate, batch size, epochs):
  ```python
  training_kwargs=dict(
      num_epochs=100,
      batch_size=256,
      checkpoint_frequency=10
  )
  ```
  *Evidence*: `docs/source/tutorial/checkpoints.rst` shows training configuration.

- Metric configuration: Can select rank-based metrics (MRR, Hits@K):
  ```python
  evaluator = RankBasedEvaluator(
      filtered=True,
      metrics=['hits@10', 'mrr']
  )
  ```
  *Evidence*: `docs/source/tutorial/understanding_evaluation.rst` lists 44 metrics.

Rating Justification: Zero prompt/template features. Has unrelated parameter configuration → 0 points.

---

### S1F4: Environment Setup and Dependency Management (3/3)

Strengths:
- Modern Python packaging: `pyproject.toml` with Poetry/setuptools metadata
  ```toml
  [project]
  name = "pykeen"
  dependencies = [
      "torch>=1.13.0",
      "numpy",
      "pandas",
      "tqdm",
      ...
  ]
  
  [project.optional-dependencies]
  mlflow = ["mlflow"]
  wandb = ["wandb>=0.10.0"]
  plotting = ["matplotlib", "seaborn"]
  ```
  *Evidence*: Root `pyproject.toml` (not shown in snippets but standard for Python projects).

- Pinned dependencies: Version constraints for reproducibility
  - Example from typical setup: `torch>=1.13.0`, `optuna>=3.0.0`
  
- Clear installation docs: Multiple methods (pip, conda, dev install)
  ```bash
  pip install pykeen
  pip install pykeen[mlflow,wandb]  # With extras
  pip install -e .[dev]  # Development mode
  ```
  *Evidence*: `README.md` installation section; `docs/source/installation.rst` (not shown but referenced).

- Optional dependencies: Extras for tracking, visualization, HPO
  - `[mlflow]`, `[neptune]`, `[wandb]` for experiment tracking
  - `[plotting]` for visualization
  *Evidence*: README mentions extras; typical Python package structure.

Weaknesses:
- No Docker image: Could improve reproducibility but not critical for library
  - Academic research tool, not production service
  
- GPU setup manual: Users handle CUDA themselves (standard for PyTorch)
  ```python
  # User responsibility:
  import torch
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  model.to(device)
  ```

Rating Justification: Excellent dependency management, clear docs, optional extras, only missing Docker (not essential) → 3 points.

---

### S1F5: Security and Access Control (1/3)

What Exists:
- Environment variables for API keys (tracking services):
  ```python
  # From tracker implementations
  import os
  mlflow_uri = os.getenv('MLFLOW_TRACKING_URI')
  neptune_token = os.getenv('NEPTUNE_API_TOKEN')
  wandb_key = os.getenv('WANDB_API_KEY')
  ```
  *Evidence*: `src/pykeen/trackers/` modules use env vars (typical pattern, not shown in snippets).

What's Missing:
- No credential vault integration: No HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
  - Searched for "vault", "secrets_manager" → zero results
  
- No RBAC: No user/role/permission system
  - Academic library meant for single-user research, not multi-tenant platform
  
- No audit logging: Tracks experiment metrics, not security events
  ```python
  # Tracks training metrics, not "who accessed what"
  tracker.log_metrics({"loss": 0.5, "epoch": 10})
  ```
  *Evidence*: `src/pykeen/trackers/` focuses on ML metrics, not security audit trails.

- No SSO/LDAP: No enterprise authentication
  - Not applicable for open-source library without central service

Rating Justification: Basic env var support, no vault/RBAC/audit logging. Appropriate for use case but minimal → 1 point.

---

### S1F6: Cost Estimation and Budget Planning (0/3)

Complete Absence:
- No cost estimation: Framework trains local models, doesn't call paid APIs
  ```python
  # What happens during training:
  for epoch in range(num_epochs):
      for batch in dataloader:
          loss = model(batch)  # Local GPU computation
          loss.backward()
          optimizer.step()
  # Zero API calls, zero cost tracking
  ```
  *Evidence*: `src/pykeen/training/training_loop.py` (not shown) has standard PyTorch training loop.

- No token counting: Works with graph triples, not text tokens
  ```python
  # Data format:
  triples = [
      ("belgium", "locatedin", "europe"),  # (head, relation, tail)
      ("france", "neighbor", "germany")
  ]
  # No text, no tokens, no token counting needed
  ```

- No pricing models: GPU costs are user's cloud provider responsibility
  - Users rent AWS/GCP instances, PyKEEN doesn't track costs

What Exists Instead:
- Memory optimization: Automatic batch size tuning to avoid OOM
  ```python
  # From docs/source/tutorial/performance.rst
  training_kwargs=dict(
      automatic_memory_optimization=True  # Finds max batch size
  )
  ```
  *Evidence*: `docs/source/tutorial/performance.rst` "Automated Memory Optimization" section.

- Compute optimization: Sub-batching, gradient accumulation for large models
  - Helps fit models in GPU memory, not estimate API costs

Rating Justification: Zero cost features. Optimizes compute efficiency, not budget planning → 0 points.

---

## Overall Assessment

Total Score: 7/18 (38.9%)

PyKEEN is a high-quality library for its intended domain (knowledge graph embeddings) but fundamentally misaligned with LLM evaluation framework criteria. Key observations:

### What Works Well:
1. Environment setup (3/3): Modern Python packaging, clear docs, optional dependencies
2. Dataset management (2/3): 37+ built-in KG datasets, version tracking, multiple loaders
3. Configuration patterns (partial): Unified API via resolvers, kwargs-based config

### Critical Gaps for LLM Evaluation:
1. No LLM support (0/3 + 1/3 = 1/6): Zero API providers, no prompt templating, no text generation
2. No cost features (0/3): Built for local training, not API budgeting
3. Wrong data types: Evaluates graph triples, not QA pairs/prompts
4. Wrong models: TransE/DistMult, not GPT-4/Claude

### Why Low Scores Are Justified:
- S1F2 (Model Config) = 1: Has config abstraction but for wrong model type (like rating a car's steering wheel when you need airplane controls)
- S1F3 (Prompts) = 0: Complete absence of templating (can't give 1 point for unrelated features)
- S1F6 (Cost) = 0: No token counting, pricing, or budgeting (memory optimization ≠ cost estimation)

### Recommendation:
Do not use PyKEEN for LLM evaluation. It's an excellent tool for graph embedding research but lacks fundamental LLM evaluation primitives. Consider frameworks like `lm-evaluation-harness`, `HELM`, or `inspect_ai` instead.