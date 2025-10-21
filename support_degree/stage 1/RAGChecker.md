# RAGChecker - Stage 1 (CONFIGURE) Evaluation

## Summary
RAGChecker is a diagnostic evaluation framework for RAG systems that operates primarily at runtime rather than through explicit configuration. It lacks traditional dataset/model configuration abstractions and instead requires users to provide pre-formatted evaluation data with RAG outputs already generated. The framework focuses on claim-level checking rather than upfront configuration management.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Basic JSON input format only, no dataset abstraction, no versioning, no schema API |
| S1F2: Model Configuration | 1 | Minimal configuration via CLI args, only supports LLM provider names, no resource allocation |
| S1F3: Prompt Configuration | 1 | Hardcoded prompts with no templating system, no versioning, limited parameter control |
| S1F4: Environment Setup | 2 | Basic pyproject.toml with dependencies, no containerization, minimal automation |
| S1F5: Security & Access | 0 | No credential management beyond env vars, no access control, no audit logging |
| S1F6: Cost Estimation | 0 | No cost estimation or budgeting features |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration

Rating: 1/3

Evidence:

1. Dataset Source Support: Only supports JSON input format
   - From `ragchecker/cli.py`:
     ```python
     parser.add_argument(
         "--input_path", type=str, required=True,
         help="Input path to the json file."
     )
     ```
   - From `ragchecker/container.py`:
     ```python
     @dataclass_json
     @dataclass
     class RAGResults:
         results: List[RAGResult] = field(default_factory=list)
     ```
   - No support for CSV, databases, APIs, or cloud storage
   - Single source type: local JSON files only

2. Schema Definition: No schema API
   - From `ragchecker/container.py`:
     ```python
     @dataclass
     class RAGResult:
         query_id: str
         query: str
         gt_answer: str
         response: str
         retrieved_context: List[RetrievedDoc] | None = None
     ```
   - Schema is hardcoded in dataclass definition
   - No validation rules or constraints definable by users
   - No way to specify field types or requirements declaratively

3. Split Strategies: Not applicable
   - Framework expects pre-split, pre-evaluated RAG outputs
   - No dataset splitting functionality
   - From `examples/checking_inputs.json`: Data must include pre-generated `response` and `retrieved_context`

4. Versioning: No versioning support
   - No version tracking for datasets
   - No version history or comparison tools
   - No ability to reference different dataset versions

Conclusion: The framework provides minimal dataset abstraction. Users must manually format data into a specific JSON structure with RAG outputs already generated. There's no dataset discovery, schema definition API, split strategies, or versioning capabilities.

---

### S1F2: Model and Backend Configuration

Rating: 1/3

Evidence:

1. Provider Support: Limited to LiteLLM-compatible providers
   - From `ragchecker/cli.py`:
     ```python
     parser.add_argument(
         '--extractor_name', type=str, default="bedrock/meta.llama3-70b-instruct-v1:0",
         help="Model used for extracting claims."
     )
     parser.add_argument(
         '--checker_name', type=str, default="bedrock/meta.llama3-70b-instruct-v1:0",
         help="Model used for checking whether the claims are factual."
     )
     ```
   - Only supports providers via LiteLLM (OpenAI, Bedrock, etc.)
   - From `tutorial/ragchecker_tutorial_en.md`:
     > "RAGChecker employ [litellm](https://docs.litellm.ai/) for invoking the LLMs"
   - Same configuration for both extractor and checker models

2. Configuration Method: CLI arguments or Python API
   - From `ragchecker/evaluator.py`:
     ```python
     def __init__(
         self,
         extractor_name="bedrock/meta.llama3-70b-instruct-v1:0",
         checker_name="bedrock/meta.llama3-70b-instruct-v1:0",
         extractor_max_new_tokens=1000,
         batch_size_extractor=32,
         batch_size_checker=32,
         ...
     ):
     ```
   - No YAML/JSON config file support
   - All configuration via constructor parameters or CLI

3. Authentication: Environment variables only
   - From `ragchecker/evaluator.py`:
     ```python
     if openai_api_key:
         os.environ['OPENAI_API_KEY'] = openai_api_key
     ```
   - No vault integration or credential rotation
   - Relies on LiteLLM's authentication mechanisms

4. Resource Allocation: Batch size only
   - From `ragchecker/cli.py`:
     ```python
     parser.add_argument(
         "--batch_size_extractor", type=int, default=32,
         help="Batch size for extractor."
     )
     parser.add_argument(
         "--batch_size_checker", type=int, default=32,
         help="Batch size for checker."
     )
     ```
   - No GPU/CPU specification
   - No memory or compute resource control
   - No validation before execution

Conclusion: Very basic model configuration via CLI arguments or Python API. Supports 2-3 model roles (extractor, checker) through LiteLLM integration. No sophisticated configuration management, resource allocation, or authentication beyond environment variables.

---

### S1F3: Evaluation Parameters and Prompt Configuration

Rating: 1/3

Evidence:

1. Parameter Definition: Minimal parameter control
   - From `ragchecker/evaluator.py`:
     ```python
     extractor_max_new_tokens=1000,
     batch_size_extractor=32,
     batch_size_checker=32,
     ```
   - Only `max_tokens` configurable for generation
   - No temperature, top_p, or other sampling parameters exposed
   - No parameter sweeps supported

2. Template System: No templating - hardcoded prompts
   - Prompts are embedded in RefChecker library (dependency)
   - From `ragchecker/evaluator.py`:
     ```python
     self.extractor = LLMExtractor(
         model=extractor_name, 
         batch_size=batch_size_extractor,
         api_base=extractor_api_base
     )
     ```
   - No way to customize prompts without modifying source code
   - No variable substitution or template inheritance
   - No Jinja2 or similar templating support

3. Prompt Versioning: None
   - Prompts are hardcoded in RefChecker dependency
   - No version tracking or comparison tools
   - No ability to A/B test different prompts

4. Metric Configuration: Via CLI argument
   - From `ragchecker/cli.py`:
     ```python
     parser.add_argument(
         '--metrics', type=str, nargs='+', default=[all_metrics],
         help='Metrics to evaluate the results.'
     )
     ```
   - From `ragchecker/metrics.py`:
     ```python
     METRIC_GROUP_MAP = {
         overall_metrics: [precision, recall, f1],
         retriever_metrics: [claim_recall, context_precision],
         generator_metrics: [...],
         all_metrics: [...]
     }
     ```
   - Can select metric groups but no custom metric definitions
   - No success criteria thresholds in config

Conclusion: Extremely limited prompt and parameter configuration. Prompts are hardcoded with no templating system. Only basic parameters like batch size and max tokens are configurable. No prompt versioning or sophisticated metric configuration beyond selection.

---

### S1F4: Environment Setup and Dependency Management

Rating: 2/3

Evidence:

1. Dependency Specification: Uses Poetry with pyproject.toml
   - From `pyproject.toml`:
     ```toml
     [tool.poetry]
     name = "ragchecker"
     version = "0.1.9"
     
     [tool.poetry.dependencies]
     python = "^3.9"
     refchecker = "^0.2"
     loguru = "^0.7"
     dataclasses-json = "^0.6"
     ```
   - Dependencies specified but not pinned to exact versions (using `^`)
   - Clear dependency declaration
   - No optional dependencies marked

2. Containerization: None provided
   - No Dockerfile in repository
   - No official Docker images mentioned
   - From README search: No container-related documentation

3. Environment Automation: Basic pip install
   - From `README.md`:
     ```bash
     pip install ragchecker
     python -m spacy download en_core_web_sm
     ```
   - Simple installation process
   - No setup scripts or Makefile
   - Manual spaCy model download required

4. Hardware Configuration: No explicit support
   - No CUDA version specification
   - No GPU requirements documented
   - From code: Relies on underlying libraries (litellm) for hardware handling
   - No compatibility checks on startup

Conclusion: Basic dependency management via Poetry. Simple installation process but no containerization, automated setup scripts, or hardware configuration management. Dependencies use semantic versioning ranges rather than pinned versions.

---

### S1F5: Security and Access Control

Rating: 0/3

Evidence:

1. Credential Management: Environment variables only
   - From `ragchecker/evaluator.py`:
     ```python
     if openai_api_key:
         os.environ['OPENAI_API_KEY'] = openai_api_key
     ```
   - No vault integration (HashiCorp Vault, AWS Secrets Manager)
   - No credential encryption
   - No rotation support
   - Relies entirely on LiteLLM's credential handling

2. Access Control: None
   - No RBAC system
   - No user/group/role management
   - No restrictions on who can run evaluations
   - Open execution model

3. Audit Logging: Basic logging only
   - From `ragchecker/evaluator.py`:
     ```python
     from loguru import logger
     logger.info(f"Extracting claims for {extract_type} of {len(results)} RAG results.")
     ```
   - Basic operational logging with loguru
   - No sensitive operation logging
   - No tamper-proof logging
   - No retention policies

4. Enterprise Integration: None
   - No SSO support (SAML, OAuth)
   - No LDAP/Active Directory integration
   - No compliance certifications mentioned
   - No enterprise features documented

Conclusion: No security features beyond basic environment variable credential passing. No access control, audit logging, or enterprise integration capabilities. This is a research tool without production security considerations.

---

### S1F6: Cost Estimation and Budget Planning

Rating: 0/3

Evidence:

1. Cost Modeling: None
   - No cost estimation before running
   - No pricing knowledge for different providers
   - No cost model support for local inference
   - Search through codebase: No cost-related functions

2. Resource Projection: None
   - No token count estimation before execution
   - No API call projection
   - No compute hour estimation
   - Framework provides intermediate results but no pre-execution estimates

3. Budget Tools: None
   - No budget limits settable
   - No cost breakdown by component
   - No cost-what-if analysis
   - No budget management features

4. Optimization Suggestions: None
   - No recommendations for cheaper alternatives
   - No batch size optimization for cost/speed tradeoff
   - No provider cost comparison
   - Focus is on evaluation quality, not cost

Conclusion: Complete absence of cost estimation and budgeting features. The framework focuses on evaluation quality and doesn't provide any cost management capabilities. Users must manually track costs through their LLM provider dashboards.

---

## Overall Assessment

Total Score: 5/18 (27.8%)

RAGChecker is primarily a runtime evaluation tool rather than a configuration-driven framework. It operates on the principle that users have already:
1. Built their RAG system
2. Generated responses and retrieved contexts
3. Formatted results into the expected JSON structure

The framework then performs claim-level checking on these pre-generated outputs. This design philosophy means:

Strengths:
- Simple, focused API for a specific evaluation task
- Clear Python/CLI interface for basic operations
- Reasonable dependency management with Poetry

Weaknesses:
- No dataset abstraction or discovery mechanisms
- Minimal model configuration capabilities
- Hardcoded prompts with no customization
- No security, access control, or cost management features
- Requires significant manual preparation of input data
- No configuration file support (YAML/JSON)

Use Case Fit:
RAGChecker is suitable for researchers and developers who:
- Have existing RAG systems generating outputs
- Want to perform detailed claim-level diagnostics
- Are comfortable with programmatic configuration
- Don't need production-grade security or cost management

It is not suitable for:
- End-to-end RAG evaluation pipelines
- Organizations requiring configuration management at scale
- Production environments needing security and cost controls
- Teams wanting dataset versioning and management

The low configuration score reflects that RAGChecker is designed as a specialized diagnostic tool rather than a comprehensive evaluation platform with rich configuration capabilities.