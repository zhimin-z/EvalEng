# stanford-crfm/helm - Stage 1 (CONFIGURE) Evaluation

## Summary
HELM (Holistic Evaluation of Language Models) is a comprehensive evaluation framework with strong configuration capabilities focused on research reproducibility. It provides sophisticated dataset/scenario management, extensive model provider support, and programmatic configuration through Python APIs and YAML files. However, it lacks built-in cost estimation, GUI-based configuration, and enterprise security features like RBAC or credential vaulting.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | HELM supports multiple data sources (Hugging Face, CSV, JSON, APIs) with logical scenario definitions, but lacks declarative split strategies and formal versioning. Evidence: `docs/adding_new_scenarios.md` shows HF integration and manual split handling; no schema validation API found. |
| S1F2: Model Configuration | 3 | Excellent multi-provider support (15+ providers including OpenAI, Anthropic, HF, vLLM) with clean YAML-based configuration, secure credential management via files, and resource allocation options. Evidence: `docs/adding_new_models.md`, `src/helm/config/model_deployments.yaml`, `docs/credentials.md` show comprehensive provider support with deployment-specific configs. |
| S1F3: Prompt Configuration | 2 | Basic templating through Python string formatting and scenario-based prompt construction, but no built-in Jinja2 engine, limited few-shot configuration, and no formal prompt versioning system. Evidence: `src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py` shows manual prompt assembly; no template inheritance found. |
| S1F4: Environment Setup | 2 | Standard Python packaging with `pyproject.toml`, pinned dependencies in `requirements.txt`, and Docker support mentioned but no official images found. Setup requires manual steps. Evidence: `docs/installation.md` shows conda/virtualenv setup; `pyproject.toml` exists but no Dockerfile in repo structure. |
| S1F5: Security & Access | 1 | Basic credential management via plaintext config files (`credentials.conf`) with environment variable support. No RBAC, audit logging, vault integration, or SSO. Evidence: `docs/credentials.md` shows simple key-value credential storage; no access control documentation found. |
| S1F6: Cost Estimation | 1 | Token counting for dry runs exists but no cost modeling, budget limits, or provider pricing integration. Users must calculate costs manually. Evidence: `docs/benchmark.md` mentions `--dry-run` for token estimation but states "estimate" only; `scripts/estimate_cost.py` exists but not integrated into main workflow. |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (2/3)

Strengths:
- Multiple data sources supported: HuggingFace datasets (`load_dataset()`), local files (CSV, JSON, JSONL), GitHub raw files, and APIs
  ```python
  # From docs/adding_new_scenarios.md
  # Working with Hugging Face datasets
  # You can use `load_dataset()` to do so. It is recommended that you set the `cache_dir` 
  # parameter to a subdirectory within `output_path`.
  ```
  
- Scenario abstraction: Each dataset is wrapped in a `Scenario` class providing logical separation
  ```python
  # From src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py
  class MTSamplesReplicateScenario(Scenario):
      def get_instances(self, output_path: str) -> List[Instance]:
          # Downloads and processes data into Instance objects
  ```

- Lazy loading: Data is downloaded on-demand to `output_path`, not loaded upfront
  ```python
  # From docs/adding_new_scenarios.md - Downloading data to local disk
  # The `output_path` argument passed into the `get_instances()` method will contain 
  # a file path to a scenario-specific download folder
  ```

Weaknesses:
- No declarative schema API: Column types and constraints are implicit in Python code, not declared
  ```python
  # From src/helm/benchmark/scenarios/scenario.py - no validation schema
  @dataclass(frozen=True)
  class Instance:
      input: Input
      references: List[Reference]
      split: str  # No enum constraint enforcement at config level
  ```

- Manual split management: Splits are hardcoded as `TEST_SPLIT`, `TRAIN_SPLIT` constants, not declaratively configured
  ```python
  # From src/helm/benchmark/scenarios/mtsamples_procedures_scenario.py
  instances.append(
      Instance(
          input=Input(text=cleaned_text),
          references=[Reference(Output(text=reference_text), tags=[CORRECT_TAG])],
          split=TEST_SPLIT,  # Hardcoded, not configurable
      )
  )
  ```

- No formal versioning system: Dataset versions are managed via Git hashes in code, not through a versioning API
  ```python
  # From src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py
  GIT_HASH = "ebc104a4f96c5b7602242f301e081e9934a23344"  # Version baked into code
  ```

Rating: 2 points - Supports 3-4 sources with basic scenario abstraction but lacks declarative schemas and formal versioning.

---

### S1F2: Model and Backend Configuration (3/3)

Strengths:
- Extensive provider support (15+ providers): OpenAI, Anthropic, Cohere, AI21, HuggingFace, vLLM, Together, Mistral, Google, etc.
  ```yaml
  # From docs/credentials.md
  # Keys required for platforms:
  # - AI21: ai21ApiKey
  # - Aleph Alpha: AlephAlphaApiKey
  # - Anthropic: anthropicApiKey
  # - Cohere: cohereApiKey
  # - Google: googleProjectId, googleLocation
  # - GooseAI: gooseApiKey
  # - Mistral AI: mistralaiApiKey
  # - OpenAI: openaiApiKey, openApiOrgId
  ```

- Clean YAML configuration: Model deployments defined in structured YAML files
  ```yaml
  # From docs/adding_new_models.md - Hugging Face example
  model_deployments:
    - name: huggingface/pythia-70m
      model_name: eleutherai/pythia-70m
      tokenizer_name: EleutherAI/gpt-neox-20b
      max_sequence_length: 2048
      client_spec:
        class_name: "helm.clients.huggingface_client.HuggingFaceClient"
        args:
          pretrained_model_name_or_path: EleutherAI/pythia-70m
          revision: my_revision
          load_in_8bit: true
          device: cuda:0
  ```

- Secure credential management: Credentials stored in separate HOCON config files, never in code
  ```
  # From docs/credentials.md
  # You should create a `credentials.conf` file in your local configuration folder
  platformOneApiKey: sk-abcdefgh
  platformTneApiKey: sk-ijklmnop
  ```

- Resource allocation options: Device placement, quantization, multi-GPU support via `args`
  ```yaml
  # From docs/adding_new_models.md - Examples of common arguments
  # - Quantization: `load_in_8bit: true`
  # - Model precision: `torch_dtype: torch.float16`
  # - Model device: `device: cpu` or `device: cuda:0`
  # - Multi-GPU: `device_map: auto`
  ```

- Runtime overrides supported: Can specify models via CLI flags
  ```bash
  # From docs/huggingface_models.md
  helm-run \
      --run-entries boolq:model=stanford-crfm/BioMedLM \
      --enable-huggingface-models stanford-crfm/BioMedLM \
      --suite v1 \
      --max-eval-instances 10
  ```

Rating: 3 points - Full marks for 15+ providers, clean YAML API, secure auth via files, and resource control.

---

### S1F3: Evaluation Parameters and Prompt Configuration (2/3)

Strengths:
- Parameter specification: Temperature, top_p, max_tokens configurable via Request objects
  ```python
  # From demo.py
  request = Request(
      model="openai/gpt-4o-mini-2024-07-18",
      prompt="Life is like a box of",
      echo_prompt=True,
      temperature=0.3,
      max_tokens=50
  )
  ```

- Variable substitution: Basic string formatting with `{variable}` placeholders
  ```python
  # From src/helm/benchmark/annotation/mtsamples_replicate_annotator.py
  PROMPT_TEMPLATE = """You are a medical expert...
  <patient_information>
  {QUESTION}
  </patient_information>
  <response>
  {RESPONSE}
  </response>"""
  ```

- Few-shot support: Examples can be programmatically added to prompts
  ```python
  # From src/helm/proxy/example_queries.py
  def merge(examples, x):
      cur = self.description + "\n"
      for e in examples:
          cur += f"{rtrip(e[0])}\nAnswer: {e[1]}\n\n\n"
      cur += f"{rtrip(x)}\nAnswer: "
      return cur
  ```

Weaknesses:
- No templating engine: Uses Python string formatting, not Jinja2 or similar
  ```python
  # From src/helm/benchmark/scenarios/decodingtrust_adv_demonstration_scenario.py
  # Manual string concatenation instead of templates
  def merge(examples, x):
      cur = self.description + "\n"
      for e in examples:
          cur += f"{rtrip(e[0])}\nAnswer: {e[1]}\n\n\n"
      cur += f"{rtrip(x)}\nAnswer: "
      return cur
  ```

- No prompt versioning system: Prompts are hardcoded in Python code, no version tracking
  ```python
  # From src/helm/benchmark/annotation/mtsamples_procedures_annotator.py
  # Prompt defined as string constant, no versioning metadata
  PROMPT_TEMPLATE = """You are a medical expert..."""
  ```

- Limited role formatting: No built-in chat message roles, must be manually constructed
  ```yaml
  # No evidence of system/user/assistant role abstractions found in codebase
  ```

- No parameter validation: No checks against model capabilities at config time
  ```python
  # From demo.py - Request accepts any parameters, no validation shown
  request = Request(
      model="openai/gpt-4o-mini-2024-07-18",
      prompt="Life is like a box of",
      temperature=999  # Would not be caught at config time
  )
  ```

Rating: 2 points - Basic templating via string formatting and few-shot support exist, but no formal templating engine or versioning.

---

### S1F4: Environment Setup and Dependency Management (2/3)

Strengths:
- Multiple dependency specs: `pyproject.toml`, `requirements.txt`, `constraints.txt` all present
  ```
  # From repository structure
  ├── pyproject.toml
  ├── requirements.txt
  └── constraints.txt
  ```

- Optional dependencies marked: Extras like `[dev]`, `[heim]`, `[medhelm]`, `[vlm]` clearly defined
  ```bash
  # From docs/installation.md
  pip install crfm-helm  # Base install
  pip install "crfm-helm[vlm]"  # With VLM support
  pip install "crfm-helm[heim]"  # With text-to-image support
  ```

- Setup automation scripts: `install-dev.sh`, `install-heim-extras.sh`, `install-shelm-extras.sh`
  ```
  # From repository structure
  ├── install-dev.sh
  ├── install-heim-extras.sh
  └── install-shelm-extras.sh
  ```

- Virtual environment documentation: Clear instructions for conda and virtualenv
  ```bash
  # From docs/installation.md - Using Virtualenv
  python3 -m pip install virtualenv
  python3 -m virtualenv -p python3.10 helm-venv
  source helm-venv/bin/activate
  ```

Weaknesses:
- No official Docker images: Dockerfile not found in repository structure
  ```
  # Repository structure shows no Dockerfile at root or in subdirectories
  ```

- Dependencies not strictly pinned: `requirements.txt` likely uses ranges, not exact versions (not shown in excerpts)

- Manual CUDA setup: No automated hardware detection or compatibility checks
  ```bash
  # From docs/adding_new_models.md
  # User must manually specify: device: cuda:0
  # No startup validation mentioned
  ```

Rating: 2 points - Standard Python packaging with clear dependency management, but no containerization or automated setup validation.

---

### S1F5: Security and Access Control (1/3)

Strengths:
- Separate credential files: Credentials isolated in `credentials.conf`, not in code
  ```
  # From docs/credentials.md
  # Create a `credentials.conf` file in your local configuration folder
  {
      openaiApiKey: "...",
      ai21ApiKey: "..."
  }
  ```

- Environment variable support: Credentials can come from env vars (Google Cloud CLI integration)
  ```bash
  # From docs/credentials.md - Google setup
  gcloud auth application-default login
  gcloud auth application-default set-quota-project 123456789012
  ```

Weaknesses:
- Plaintext credential storage: No encryption at rest
  ```
  # From docs/credentials.md
  # Credentials stored as plain HOCON key-value pairs
  platformOneApiKey: sk-abcdefgh
  ```

- No access control: No RBAC, user/group/role system found
  ```
  # No documentation for access control in docs/credentials.md or elsewhere
  ```

- No audit logging: No mention of operation logging or tamper-proof logs
  ```
  # No audit logging documentation found in any docs
  ```

- No enterprise integration: No SSO, LDAP, vault integration
  ```
  # From docs/credentials.md - only basic API key management shown
  ```

Rating: 1 point - Basic env var credential management exists, but no access control or enterprise security features.

---

### S1F6: Cost Estimation and Budget Planning (1/3)

Strengths:
- Token counting for dry runs: Can estimate token usage without making requests
  ```bash
  # From docs/benchmark.md - Estimating Token Usage
  helm-run -r <RunSpec> --suite $SUITE --max-eval-instances <Number> --dry-run
  # Check output in benchmark_output/runs/$SUITE for token counts
  ```

- Estimation script exists: `scripts/estimate_cost.py` present in repository
  ```
  # From repository structure
  ├── scripts
  │   ├── estimate_cost.py
  │   └── estimate_cost_audio.py
  ```

Weaknesses:
- No cost modeling: Token counts don't translate to dollar amounts
  ```
  # From docs/benchmark.md
  # "sum indicates the estimated total number of tokens used"
  # No mention of cost calculation or pricing models
  ```

- Manual cost calculation required: Users must look up pricing externally
  ```
  # No documentation showing automated cost estimation or provider pricing integration
  ```

- No budget tools: No budget limits, cost-what-if analysis, or optimization suggestions
  ```
  # No budget-related flags or configuration options documented
  ```

- No provider cost comparison: Framework doesn't compare pricing across providers
  ```
  # No evidence of multi-provider cost comparison features
  ```

Rating: 1 point - Basic token counting exists but no cost modeling, budgeting, or optimization features.

---

## Evidence Summary

### Key Files Demonstrating Configuration Capabilities:

1. Dataset Configuration: `docs/adding_new_scenarios.md`, `src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py`
2. Model Configuration: `docs/adding_new_models.md`, `docs/credentials.md`, `docs/huggingface_models.md`
3. Prompt Configuration: `src/helm/benchmark/annotation/*_annotator.py`, `src/helm/proxy/example_queries.py`
4. Environment Setup: `docs/installation.md`, `pyproject.toml`, `install-*.sh` scripts
5. Security: `docs/credentials.md` (limited scope)
6. Cost Estimation: `docs/benchmark.md`, `scripts/estimate_cost.py`

### Overall Assessment:

HELM excels at model provider integration (S1F2: 3/3) with clean YAML configs and extensive provider support. It has adequate dataset/scenario management (S1F1: 2/3) with multiple source support but lacks declarative schemas. Prompt configuration (S1F3: 2/3) is basic but functional. Environment setup (S1F4: 2/3) is standard Python packaging without containerization. Security (S1F5: 1/3) and cost estimation (S1F6: 1/3) are minimal, lacking enterprise features and financial planning tools.

Total Score: 11/18 (61%)