# AutoRAG - Stage 1 (CONFIGURE) Evaluation

## Summary
AutoRAG is a RAG pipeline optimization framework that provides strong configuration capabilities through YAML files, with comprehensive dataset management, embedding/LLM model configuration, and project structure management. It excels at declarative configuration but has limited built-in cost estimation and enterprise security features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Supports multiple sources (parquet, HuggingFace datasets) with schema definition via columns, but lacks advanced versioning and declarative split strategies |
| S1F2: Model Configuration | 3 | Excellent support for 5+ providers (OpenAI, HuggingFace, Ollama, Bedrock, OpenAILike) with clean YAML/Python API and flexible authentication |
| S1F3: Prompt Configuration | 2 | Basic templating with variable substitution (f-string), limited few-shot support, no built-in versioning system |
| S1F4: Environment Setup | 2 | Good dependency management with Docker support, but manual setup required for some features (parsing, Korean/Japanese support) |
| S1F5: Security & Access | 1 | Basic environment variable support for API keys, no RBAC, audit logging, or enterprise integrations |
| S1F6: Cost Estimation | 0 | No built-in cost estimation or budget planning features |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 2/3

Evidence:

1. Dataset Source Support (2-3 sources):
   - Parquet files (primary format): `docs/source/data_creation/data_format.md`
   ```python
   corpus_df = pd.read_parquet('path/to/corpus.parquet')
   qa_df = pd.read_parquet('path/to/qa.parquet')
   ```
   - HuggingFace datasets: `README.md` mentions "You can check out sample datasets at huggingface"
   - CSV support for raw data: `tests/resources/sample_contents_nqa.csv`
   
2. Schema Definition (Basic):
   From `docs/source/data_creation/data_format.md`:
   ```
   QA Dataset columns:
   - qid (string): Unique identifier
   - query (string): User's question
   - retrieval_gt (2D list): Ground truth document IDs
   - generation_gt (list): Ground truth answers
   
   Corpus Dataset columns:
   - doc_id (string): Unique identifier
   - contents (string): Actual contents
   - metadata (dict): Including last_modified_datetime
   ```
   
   Schema is implicit from data structure rather than explicit API. No validation rules shown beyond type expectations.

3. Split Strategies (Manual):
   From `docs/source/tutorial.md`:
   ```
   Don't forget to split train and test dataset.
   It is common mistake to not split dataset, but it will occur overfitting issue.
   We highly recommend you to optimize RAG pipeline with train dataset, and evaluate whole pipeline with test dataset later.
   ```
   No declarative split configuration - users must manually split data.

4. Versioning (Limited):
   From `docs/source/data_creation/data_format.md`:
   ```python
   # metadata includes last_modified_datetime
   metadata = {
       'last_modified_datetime': datetime.now()
   }
   ```
   Basic timestamp tracking in metadata, but no version control system or queryable history.

Justification: Supports 2-3 sources (parquet, HuggingFace, CSV) with defined schema via required columns. No declarative split strategies or comprehensive versioning system. Users must manually manage data splits and versions.

---

### S1F2: Model and Backend Configuration
Rating: 3/3

Evidence:

1. Provider Support (5+ providers):
   From `docs/source/local_model.md`:
   ```yaml
   | LLM Model Type | llm parameter | Description |
   |:--------------:|:-------------:|-------------|
   | OpenAI         | openai        | For OpenAI models (GPT-3.5, GPT-4) |
   | OpenAILike     | openailike    | For models with OpenAI-compatible APIs (e.g., Mistral, Claude) |
   | Ollama         | ollama        | For locally running Ollama models |
   | Bedrock        | bedrock       | For AWS Bedrock models |
   ```
   
   Also supports HuggingFace models:
   ```yaml
   - module_type: llama_index_llm
     llm: huggingface
     model_name: mistralai/Mistral-7B-Instruct-v0.2
   ```

2. Configuration Method (YAML + Python API):
   From `docs/source/optimization/custom_config.md`:
   ```yaml
   nodes:
     - node_type: generator
       modules:
         - module_type: llama_index_llm
           llm: openailike
           model: mistralai/Mistral-7B-Instruct-v0.2
           api_base: your_api_base
           api_key: your_api_key
           temperature: 0.7
   ```
   
   Python API from `docs/source/local_model.md`:
   ```python
   import autorag
   from llama_index.core.llms.mock import MockLLM
   autorag.generator_models['mockllm'] = MockLLM
   ```

3. Authentication (Flexible):
   From `docs/source/troubleshooting.md`:
   ```bash
   # Environment variables
   export OPENAI_API_KEY=your_api_key
   
   # .env file support
   pip install python-dotenv
   ```
   
   Direct API key in YAML:
   ```yaml
   - module_type: llama_index_llm
     llm: openai
     model: gpt-3.5-turbo
     api_key: your_api_key
   ```

4. Resource Allocation:
   From `docs/source/optimization/custom_config.md`:
   ```yaml
   modules:
     - module_type: llama_index_llm
       llm: openai
       model: gpt-3.5-turbo-16k
       batch: 4  # Batch size control
   ```
   
   GPU configuration from `docs/source/local_model.md`:
   ```yaml
   - module_type: llama_index_llm
     llm: huggingface
     device_map: "auto"
     model_kwargs:
       torch_dtype: "float16"
   ```

Justification: Excellent support for 5+ providers with clean YAML configuration, Python API for custom models, flexible authentication (env vars, .env, direct YAML), and resource allocation controls (batch size, device_map). Meets all criteria for full score.

---

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 2/3

Evidence:

1. Parameter Definition (Good):
   From `docs/source/local_model.md`:
   ```yaml
   modules:
     - module_type: llama_index_llm
       llm: openai
       model: gpt-3.5-turbo-16k
       temperature: [0.5, 1.0, 1.5]  # Parameter sweep support
       max_tokens: 512
   ```
   
   From `docs/source/optimization/custom_config.md`:
   ```yaml
   # Tuple support for ranges
   - module_type: hybrid_rrf
     weight_range: (4,80)
   ```

2. Template System (Basic f-string):
   From `docs/source/nodes/prompt_maker/fstring.md`:
   ```yaml
   - module_type: fstring
     prompt: "Read the passages and answer the given question. \n Question: {query} \n Passage: {retrieved_contents} \n Answer : "
   ```
   
   Limited to f-string variable substitution. No Jinja2 or advanced templating.

3. Prompt Versioning (None):
   No evidence of built-in prompt versioning system. From `docs/source/optimization/folder_structure.md`, only trial-level versioning exists:
   ```json
   {
       "trial_name": "0",
       "start_time": "2024-09-30 01:43:30"
   }
   ```

4. Metric Configuration (Good):
   From `docs/source/optimization/custom_config.md`:
   ```yaml
   strategy:
     metrics: [bleu, meteor, rouge]
     speed_threshold: 10
     strategy: mean  # or rank, normalize_mean
   ```
   
   From `docs/source/evaluate_metrics/generation.md`:
   ```yaml
   metrics:
     - metric_name: sem_score
       embedding_model: openai_embed_3_small
     - metric_name: bleu
   ```

Justification: Good parameter definition with sweep support and metric configuration. Basic templating limited to f-string with variable substitution (no Jinja2, no few-shot injection built-in). No prompt versioning system. Caps at 2 points.

---

### S1F4: Environment Setup and Dependency Management
Rating: 2/3

Evidence:

1. Dependency Specification (Good):
   From `autorag/pyproject.toml`:
   ```toml
   [project]
   dependencies = [
       "llama-index>=0.11.0",
       "pandas>=2.1.4",
       ...
   ]
   
   [project.optional-dependencies]
   gpu = ["torch", "transformers"]
   parse = ["pdfminer.six", "tesseract"]
   ko = ["konlpy"]
   ja = ["fugashi"]
   ```
   
   Clear dependency groups, but not fully pinned versions.

2. Containerization (Docker provided):
   From `README.md` and `docs/source/install.md`:
   ```dockerfile
   # Dockerfile.base, Dockerfile.gpu available
   docker build --target production -t autorag:prod .
   ```
   
   Pre-built images: `autoraghq/autorag:api`, `autoraghq/autorag:gpu`

3. Environment Automation (Manual with guides):
   From `docs/source/install.md`:
   ```bash
   pip install AutoRAG
   # For GPU
   pip install "AutoRAG[gpu]"
   # For parsing
   pip install "AutoRAG[parse]"
   ```
   
   Requires manual installation of system dependencies:
   ```
   For parsing you need to install some local packages like libmagic, tesseract, and poppler.
   The installation method depends upon your OS.
   ```

4. Hardware Configuration (Basic docs):
   From `docs/source/install.md`:
   ```bash
   docker run --gpus all \  # GPU support
     -v $(pwd)/projects:/usr/src/app/projects \
     autoraghq/autorag:gpu evaluate
   ```
   
   No comprehensive hardware specs or compatibility checks on startup.

Justification: Good dependency management with optional groups and Docker support. However, requires manual system dependency installation (tesseract, poppler) and lacks automated setup scripts. Hardware configuration documented but not automated. Solid 2/3.

---

### S1F5: Security and Access Control
Rating: 1/3

Evidence:

1. Credential Management (Basic env vars only):
   From `docs/source/install.md`:
   ```bash
   export OPENAI_API_KEY="sk-...your-api-key..."
   ```
   
   From `docs/source/troubleshooting.md`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
   
   No vault integration, no credential rotation, no encryption at rest.

2. Access Control (None):
   No evidence of RBAC, user/group/role system, or access restrictions in documentation or configuration files.

3. Audit Logging (None):
   No security-focused audit logging mentioned. Only trial history tracking:
   ```json
   // projects/tutorial_1/trial.json
   {
       "trial_name": "0",
       "start_time": "2024-09-30 01:43:30"
   }
   ```

4. Enterprise Integration (None):
   No SSO, LDAP, or compliance features mentioned in documentation.

Justification: Only basic environment variable support for API keys. No RBAC, audit logging, vault integration, or enterprise features. Minimal security configuration capabilities.

---

### S1F6: Cost Estimation and Budget Planning
Rating: 0/3

Evidence:

No cost estimation features found in:
- Configuration files (`autorag/sample_config/`)
- Documentation (`docs/source/`)
- CLI interface (`autorag/cli.py`)

From `docs/source/troubleshooting.md`, only batch size adjustment for rate limiting:
```yaml
modules:
  - module_type: llama_index_llm
    llm: openai
    model: gpt-3.5-turbo-16k
    batch: 4  # For avoiding rate limits
```

Justification: No cost modeling, token estimation, budget limits, or optimization suggestions. Framework focuses on performance optimization without cost considerations.

---

## Overall Assessment

Strengths:
1. Excellent Model Configuration (S1F2): Best-in-class support for multiple LLM/embedding providers with clean YAML and Python APIs
2. Good Dataset Management (S1F1): Clear schema definitions and multiple source support
3. Flexible Parameter Configuration: Supports parameter sweeps and metric configuration

Weaknesses:
1. No Cost Features (S1F6): Complete absence of cost estimation or budget management
2. Limited Security (S1F5): Only basic env var authentication, no enterprise features
3. Basic Templating (S1F3): F-string only, no advanced templating or versioning

Best For: Research teams and developers who need rapid RAG pipeline experimentation with multiple model providers, prioritizing performance optimization over cost control and enterprise security.

Not Suitable For: Enterprise deployments requiring cost controls, RBAC, audit trails, or compliance certifications.