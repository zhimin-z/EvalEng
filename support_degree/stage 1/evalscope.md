# EvalScope (modelscope__evalscope) - Stage 1 (CONFIGURE) Evaluation

## Summary
EvalScope is a comprehensive evaluation framework from ModelScope that supports multiple model types (LLM, VLM, Embedding, AIGC) with a modular architecture. The framework provides strong configuration capabilities through Python APIs, YAML/JSON files, and CLI interfaces. However, it shows gaps in explicit dataset schema definition, cost estimation features, and enterprise-grade security controls.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Supports ModelScope hub + local paths with basic versioning; lacks explicit schema API and declarative split strategies |
| S1F2: Model Configuration | 3 | Excellent provider support (10+ backends), multiple config methods (Python/YAML/JSON/CLI), secure auth patterns |
| S1F3: Prompt Configuration | 2 | Basic templating with variable substitution and few-shot support; lacks versioning and advanced composition |
| S1F4: Environment Setup | 2 | Good dependency management with optional extras; lacks official containers and hardware validation |
| S1F5: Security & Access | 1 | Environment variable auth only; no RBAC, audit logging, or enterprise integrations |
| S1F6: Cost Estimation | 0 | No built-in cost modeling or budget features |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 2/3

Evidence:

1. Dataset Source Support (2-3 sources):
   - ModelScope hub integration: `dataset_id: 'modelscope/ai2_arc'` (examples/viz/20250117_154119/configs/task_config_8fafb3.yaml)
   - Local paths: `local_path: 'custom_eval/text/mcq'` (examples/example_eval_custom_llm_data.py)
   - Remote URLs via ModelScope API
   - Missing: Direct database, API endpoints, or cloud storage connectors

```python
# From examples/example_eval_custom_llm_data.py
task_cfg = TaskConfig(
    model='qwen/Qwen2-0.5B-Instruct',
    datasets=['general_mcq', 'general_qa'],
    dataset_args={
        'general_mcq': {
            'local_path': 'custom_eval/text/mcq',  # Local path support
            'subset_list': ['example']
        }
    }
)
```

2. Schema Definition (Implicit):
   - No explicit schema API found in codebase
   - Schema defined implicitly through `record_to_sample()` method in adapters
   - Example from docs/zh/advanced_guides/add_benchmark.md:

```python
def record_to_sample(self, record: Dict[str, Any]) -> Sample:
    """将原始数据记录转换为Sample对象"""
    return Sample(
        input=record['question'],
        target=record['answer'],
        choices=record['options'],  # Implicit type constraint
        subset_key=record['category'].lower(),
    )
```

3. Split Strategies (Manual):
   - Splits specified in BenchmarkMeta registration:

```python
# From docs/zh/advanced_guides/add_benchmark.md
@register_benchmark(
    BenchmarkMeta(
        train_split='train',
        eval_split='test',
        few_shot_num=4,
    )
)
```
   - No declarative split configuration (e.g., 70/20/10)
   - Splits computed during dataset loading, not lazily

4. Versioning (Basic):
   - Git-based versioning via `revision` parameter:

```python
# From examples/viz/20250117_154119/configs/task_config_8fafb3.yaml
model_args:
  revision: master  # Version control
```
   - No built-in dataset version tracking or comparison tools

Justification for 2/3:
- Supports 2-3 main sources (ModelScope, local, basic remote)
- No explicit schema API (relies on adapter code)
- Manual split specification without declarative strategies
- Basic version control via git revisions, not framework-managed

---

### S1F2: Model and Backend Configuration
Rating: 3/3

Evidence:

1. Provider Support (10+ providers):
   - Native backends: Local (transformers/vLLM), OpenAI-compatible APIs
   - Integrated frameworks: OpenCompass, VLMEvalKit, RAGAS, MTEB
   - Listed in README.md:

```text
- OpenAI API compatible endpoints
- Local models (ModelScope/HuggingFace)
- vLLM inference
- OpenCompass backend
- VLMEvalKit backend
- RAGEval (MTEB/CMTEB/RAGAS)
```

Example configuration:
```python
# From examples/example_eval_vlm_swift.py
task_cfg = {
    'eval_backend': 'VLMEvalKit',
    'eval_config': {
        'model': [{
            'type': 'internvl2-8b',
            'api_base': 'http://localhost:8801/v1/chat/completions',
            'key': 'EMPTY',
            'temperature': 0.0,
        }]
    }
}
```

2. Configuration Methods (Multiple):
   - Python API: `TaskConfig()` class
   - YAML: `examples/tasks/eval_native.yaml`
   - JSON: `examples/tasks/default_eval_swift_openai_api.json`
   - CLI: `evalscope eval --model X --datasets Y`

```python
# From evalscope/config.py (inferred structure)
task_cfg = TaskConfig(
    model='Qwen/Qwen2.5-0.5B-Instruct',
    datasets=['gsm8k', 'arc'],
    generation_config={'temperature': 0.7, 'max_tokens': 1024}
)
```

3. Authentication (Environment variables + API keys):
   - Supports `api_key` parameter in model configs
   - Environment variables: `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`

```python
# From examples/aigc/image_edit.py
judge_model_args={
    'model_id': 'qwen2.5-vl-72b-instruct',
    'api_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'api_key': env.get('DASHSCOPE_API_KEY'),  # Env var auth
}
```

4. Resource Allocation:
   - GPU/CPU specification via `device_map`:

```yaml
# From examples/viz/20250117_154119/configs/task_config_8fafb3.yaml
model_args:
  device: auto
  precision: torch.float16
  device_map: auto  # Resource allocation
```

Justification for 3/3:
- 10+ supported providers/backends
- Clean configuration API with multiple formats (Python/YAML/JSON/CLI)
- Secure authentication patterns (env vars + API keys)
- Resource control via device_map and precision settings

---

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 2/3

Evidence:

1. Parameter Definition (Validated):
   - Generation config with standard parameters:

```python
# From examples/example_qwen3_collection.py
generation_config={
    'max_tokens': 30000,
    'temperature': 0.6,
    'top_p': 0.95,
    'top_k': 20,
    'n': 1,
}
```
   - Parameter validation by model APIs (no framework-level validation shown)

2. Template System (Basic):
   - Variable substitution with `{variable}` syntax:

```python
# From docs/zh/advanced_guides/add_benchmark.md
PROMPT_TEMPLATE = """
Solve the following math problem step by step...

{question}

Remember to put your answer...
""".lstrip()
```

   - Few-shot support via `sample_to_fewshot()` method:

```python
def sample_to_fewshot(self, sample: Sample) -> str:
    return (
        f'{sample.input}\n\nReasoning:\n' + 
        f"{sample.metadata['reasoning']}\n\n" + 
        f'ANSWER: {sample.target}'
    )
```

   - Template formatting methods:
```python
# From docs/zh/advanced_guides/add_benchmark.md
def format_prompt_template(self, sample: Sample) -> str:
    """格式化基础提示模板"""
    # Uses prompt_template.format(question=sample.input)
    
def format_fewshot_template(self, fewshot: str, sample: Sample) -> str:
    """格式化包含few-shot的提示模板"""
    # Uses few_shot_prompt_template.format()
```

3. Prompt Versioning (Missing):
   - No explicit prompt versioning found
   - No template inheritance or diff tools

4. Metric Configuration (Declarative):
   - Metrics specified in BenchmarkMeta:

```python
# From docs/zh/advanced_guides/add_benchmark.md
@register_benchmark(
    BenchmarkMeta(
        metric_list=['acc'],  # Declarative metrics
    )
)
```

Justification for 2/3:
- Basic templating with variable substitution works well
- Few-shot support is functional but requires manual implementation
- No prompt versioning, inheritance, or diff tools
- Good metric configuration via declarative lists

---

### S1F4: Environment Setup and Dependency Management
Rating: 2/3

Evidence:

1. Dependency Specification (Multiple formats):
   - Found in repository structure: `requirements/` directory with multiple files
   - `pyproject.toml` for package metadata
   - `setup.py` for installation

```text
# From repository structure
requirements/
├── aigc.txt
├── app.txt
├── dev.txt
├── docs.txt
├── framework.txt
├── opencompass.txt
├── perf.txt
├── rag.txt
└── vlmeval.txt
```

   - Installation with optional dependencies:

```bash
# From README.md
pip install evalscope
pip install 'evalscope[perf]'
pip install 'evalscope[app]'
pip install 'evalscope[all]'
```

2. Containerization (Missing):
   - No Dockerfile found in repository
   - No official Docker images mentioned
   - No Singularity support

3. Environment Automation (Basic):
   - Pip installation: `pip install evalscope`
   - Source installation: `pip install -e .`
   - Makefile for development tasks

```makefile
# From Makefile (inferred)
docs:
    make docs
lint:
    make lint
```

4. Hardware Configuration (Partial):
   - GPU requirements in model_args:

```python
# From examples/aigc/image_edit.py
model_args={
    'precision': 'bfloat16',
    'device_map': 'cuda:2'  # GPU specification
}
```
   - No CUDA version specification
   - No compatibility checks on startup

Justification for 2/3:
- Good dependency management with optional extras
- Clear installation instructions
- Missing official containers
- Partial hardware configuration (GPU selection but no version checks)

---

### S1F5: Security and Access Control
Rating: 1/3

Evidence:

1. Credential Management (Environment variables only):
   - API keys via env vars:

```python
# From examples/aigc/image_edit.py
env = dotenv_values('.env')
api_key=env.get('DASHSCOPE_API_KEY')
```

   - Direct API key in config:

```python
# From examples/backend/rag/cross_encoder.py
'api_key': 'xxx',
```

   - No HashiCorp Vault, AWS Secrets Manager, or credential encryption

2. Access Control (None):
   - No RBAC system found
   - No user/group/role management
   - No resource access restrictions

3. Audit Logging (None):
   - Basic logging via `get_logger()`:

```python
# From evalscope/utils/logger.py (inferred usage)
from evalscope.utils.logger import get_logger
logger = get_logger()
logger.info('Starting evaluation...')
```

   - No sensitive operation logging
   - No tamper-proof logging or retention policies

4. Enterprise Integration (None):
   - No SSO support (SAML, OAuth)
   - No LDAP/Active Directory integration
   - No compliance certifications mentioned

Justification for 1/3:
- Environment variable auth is the only security feature
- No access control, audit logging, or enterprise integrations
- Suitable for individual/academic use but not enterprise deployments

---

### S1F6: Cost Estimation and Budget Planning
Rating: 0/3

Evidence:

1. Cost Modeling (Absent):
   - No cost estimation logic found in codebase
   - No API pricing data
   - No token counting before execution

2. Resource Projection (None):
   - No pre-execution token estimation
   - No API call projection
   - No compute hour estimation

3. Budget Tools (None):
   - No budget limit configuration
   - No cost breakdown by component
   - No cost-what-if analysis

4. Optimization Suggestions (None):
   - No cheaper alternative recommendations
   - No batch size optimization for cost/speed
   - No provider cost comparison

Note from stress testing:
The framework does track metrics during execution (TTFT, TPOP, throughput) but this is for performance benchmarking, not cost estimation.

```python
# From docs/zh/user_guides/stress_test/examples.md
# Output includes performance metrics but no cost data
Speed Benchmark Results:
+---------------+-----------------+----------------+
| Prompt Tokens | Speed(tokens/s) | GPU Memory(GB) |
+---------------+-----------------+----------------+
```

Justification for 0/3:
- No cost estimation, budgeting, or optimization features
- Framework focuses on evaluation quality, not cost management
- Users must calculate costs manually using external tools

---

## Key Strengths

1. Excellent Model Backend Support: 10+ providers/backends with unified configuration interface
2. Flexible Configuration: Multiple formats (Python/YAML/JSON/CLI) work seamlessly
3. Rich Evaluation Capabilities: Supports diverse model types (LLM, VLM, Embedding, AIGC)
4. Active Development: Recent commits show QwQ-32B, AIME25, and multimodal evaluation additions
5. Good Documentation: Comprehensive Chinese and English docs with examples

## Key Gaps

1. No Explicit Schema API: Dataset schemas defined in adapter code, not declaratively
2. Missing Cost Features: Zero support for cost estimation or budget planning
3. Limited Security: Environment variables only; no RBAC, audit logs, or enterprise features
4. No Official Containers: Installation requires manual environment setup
5. Basic Prompt Management: No versioning, inheritance, or diff tools for prompts

## Recommendations for Improvement

### High Priority
1. Add Cost Estimation: Implement pre-execution token counting and API cost projection
2. Schema API: Create declarative schema definition with validation rules
3. Official Docker Images: Provide pre-built containers for major configurations

### Medium Priority
4. Prompt Versioning: Add git-like versioning for prompt templates
5. Audit Logging: Implement sensitive operation tracking for compliance
6. Declarative Splits: Support 70/20/10 split definitions without manual code

### Low Priority
7. Enterprise Features: Add RBAC, SSO, and vault integrations for enterprise adoption
8. Hardware Validation: Check CUDA versions and compatibility on startup

---

## Final Assessment

Overall Stage 1 Score: 1.67/3.0 (10/18 points)

EvalScope demonstrates strong model and backend configuration capabilities (S1F2: 3/3), making it easy to evaluate diverse models across multiple providers. The framework's flexible configuration system works well for research and academic use cases.

However, the framework shows notable gaps in enterprise-grade features. The absence of cost estimation (S1F6: 0/3), limited security controls (S1F5: 1/3), and lack of explicit schema definitions (S1F1: 2/3) limit its suitability for production deployments where budget control, compliance, and access management are critical.

Best suited for: Academic research, model development teams, and evaluation experiments where cost tracking and enterprise security are not primary concerns.

Less suitable for: Production deployments requiring budget controls, enterprise compliance (SOC2/HIPAA), or multi-tenant access management.