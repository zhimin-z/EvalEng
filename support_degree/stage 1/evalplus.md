# EvalPlus - Stage 1 (CONFIGURE) Evaluation

## Summary
EvalPlus is a code generation evaluation framework focused on HumanEval+ and MBPP+ benchmarks. It provides strong model configuration capabilities with support for multiple LLM backends, but has minimal dataset configuration features since it uses fixed benchmark datasets. The framework emphasizes execution-time configuration through CLI arguments rather than declarative configuration files.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset abstraction with hardcoded HumanEval/MBPP benchmarks; no schema definition or flexible split strategies |
| S1F2: Model Configuration | 3 | Excellent provider support (10+ backends), clean Python API, secure auth handling, and resource control |
| S1F3: Prompt Configuration | 2 | Basic templating via string formatting, parameter configuration exists, but no versioning or advanced templating |
| S1F4: Environment Setup | 2 | Good dependency management with requirements files and Docker, but manual setup required for some features |
| S1F5: Security & Access | 1 | Basic env var credential management only; no RBAC, audit logging, or enterprise features |
| S1F6: Cost Estimation | 0 | No cost estimation or budget planning capabilities |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 1/3

Dataset Source Support:
The framework only supports two fixed benchmark datasets:
```python
# evalplus/data/__init__.py
from evalplus.data.humaneval import get_human_eval_plus, get_human_eval_plus_hash
from evalplus.data.mbpp import get_mbpp_plus, get_mbpp_plus_hash
```

Users can override datasets via environment variables:
```python
# From docs/cli.md
HUMANEVAL_OVERRIDE_PATH="/path/to/HumanEvalPlus.jsonl.gz" evalplus.evaluate --dataset humaneval
MBPP_OVERRIDE_PATH="/path/to/MbppPlus.jsonl.gz" evalplus.evaluate --dataset mbpp
```

Evidence of limitations:
- Only 2 dataset sources (HumanEval, MBPP)
- No schema definition API - schemas are implicit in the code
- No declarative split strategies - datasets are used as-is
- Basic versioning through file paths only (`evalplus/evaluate.py:29-32`):
```python
problems = get_human_eval_plus(
    mini=mini, noextreme=noextreme, version=version
)
```

Justification for 1 point: Only supports 2 hardcoded datasets with environment variable override. No schema definition, no flexible splits, minimal versioning.

---

### S1F2: Model and Backend Configuration
Rating: 3/3

Provider Support - Exceptional:
The framework supports 10+ model providers (`evalplus/provider/__init__.py:7-8`):
```python
def make_model(
    model: str,
    backend: str,  # vllm, hf, openai, anthropic, google, bedrock, ollama, gptqmodel, hf_gaudi
    dataset: str,
    batch_size: int = 1,
    temperature: float = 0.0,
    ...
```

Supported backends:
1. `vllm` - vLLM inference engine
2. `hf` - HuggingFace Transformers
3. `hf_gaudi` - Intel Gaudi accelerators
4. `openai` - OpenAI API
5. `anthropic` - Anthropic API
6. `google` - Google Gemini
7. `bedrock` - AWS Bedrock
8. `ollama` - Ollama
9. `gptqmodel` - Quantized models

Configuration Method:
Clean Python API with CLI interface (`evalplus/codegen.py:106-136`):
```python
def run_codegen(
    model: str,
    dataset: str,
    root: str = "evalplus_results",
    bs: Optional[int] = None,
    n_samples: int = 1,
    temperature: float = 0.0,
    num_ctx: Optional[int] = None,
    backend: str = "vllm",
    base_url: str = None,
    tp: int = 1,  # tensor parallel
    ...
```

Authentication:
Secure handling via environment variables (`README.md:179-188`):
```bash
# OpenAI
export OPENAI_API_KEY="[YOUR_API_KEY]"
# Anthropic
export ANTHROPIC_API_KEY="[YOUR_API_KEY]"
# Google
export GOOGLE_API_KEY="[YOUR_API_KEY]"
# Bedrock
export BEDROCK_ROLE_ARN="[BEDROCK_ROLE_ARN]"
```

Resource Allocation:
Comprehensive GPU/CPU controls (`evalplus/provider/__init__.py:24-30`):
```python
# vllm only
tp=1,  # tensor parallel size
enable_prefix_caching=False,
enable_chunked_prefill=False,
# hf only
device_map=None,
attn_implementation="eager",
```

Justification for 3 points: Supports 9+ providers with clean configuration API, secure environment-based authentication, comprehensive resource control for GPU/CPU, and runtime parameter override capabilities.

---

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 2/3

Parameter Definition:
Parameters are configurable via CLI (`evalplus/codegen.py:106-136`):
```python
temperature: float = 0.0,
n_samples: int = 1,
bs: Optional[int] = None,  # batch size
max_new_tokens: int = 768,  # from provider/base.py
```

Validation exists (`evalplus/codegen.py:166-172`):
```python
if greedy and (temperature != 0 or bs != 1 or n_samples != 1):
    temperature = 0.0
    bs = 1
    n_samples = 1
    print("Greedy decoding ON (--greedy): setting bs=1, n_samples=1, temperature=0")
```

Template System:
Basic string-based templating (`evalplus/codegen.py:180-195`):
```python
instruction_prefix = "Please provide a self-contained Python script that solves the following problem in a markdown code block:"
response_prefix = "Below is a Python script with a self-contained function that solves the problem and passes corresponding tests:"

if evalperf_type == "perf-instruct":
    instruction_prefix = "Please provide an efficient and self-contained Python script..."
```

Prompt construction in `evalplus/provider/utility.py:30-43`:
```python
def make_raw_chat_prompt(
    prompt: str,
    instruction_prefix: str,
    response_prefix: str,
    tokenizer,
) -> str:
    messages = [
        {"role": "system", "content": instruction_prefix},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response_prefix},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
```

Limitations:
- No Jinja2 or advanced templating engine
- No prompt versioning system
- No few-shot example injection API
- Basic string formatting only

Metric Configuration:
Hardcoded metrics (`evalplus/evaluate.py:221-245`):
```python
# Calculate pass@k.
pass_at_k = {
    f"pass@{k}": estimate_pass_at_k(total, base_correct, k).mean()
    for k in [1, 10, 100]
    if total.min() >= k
}
```

Justification for 2 points: Has parameter configuration with validation and basic prompt templating via string formatting, but lacks advanced templating engine, versioning, few-shot support, and flexible metric configuration.

---

### S1F4: Environment Setup and Dependency Management
Rating: 2/3

Dependency Specification:
Multiple dependency files provided:
```python
# requirements.txt (evalplus/requirements.txt:1-29)
wget
appdirs
tempdir
multipledispatch
numpy
tqdm
termcolor
fire
rich
openai
tree_sitter>=0.22.0
transformers
# ... and more

# requirements-evalperf.txt
Pympler
cirron

# requirements-gaudi.txt
git+https://github.com/huggingface/optimum-habana.git
```

Proper package configuration (`setup.cfg:17-38`):
```python
[options]
packages = find:
python_requires = >=3.9
install_requires =
    wget>=3.2
    tempdir>=0.7.1
    # ... pinned versions
```

Containerization:
Official Docker image available (`README.md:76-81`):
```bash
docker run --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval \
           --samples /app/humaneval/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_0.0.jsonl
```

Dockerfile exists (`Dockerfile` mentioned in file structure).

Environment Automation:
Setup via pip (`README.md:53-54`):
```bash
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus"
```

Optional dependencies (`setup.cfg:50-52`):
```python
[options.extras_require]
perf = Pympler>=1.0.1
       cirron>=0.4
vllm = vllm>=0.5.1
```

Hardware Configuration:
GPU support detection (`evalplus/provider/hf.py:16-17`):
```python
self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Multi-GPU support via tensor parallelism (`evalplus/provider/__init__.py:28`):
```python
tp=1,  # tensor parallel size
```

Limitations:
- No automated setup script (make setup, etc.)
- Manual environment management required
- No conda environment specification
- Limited hardware requirement documentation

Justification for 2 points: Provides Docker containerization and pinned dependencies with optional extras, but requires manual setup and lacks automated environment configuration tools.

---

### S1F5: Security and Access Control
Rating: 1/3

Credential Management:
Only environment variables supported (`README.md:179-195`):
```bash
export OPENAI_API_KEY="[YOUR_API_KEY]"
export ANTHROPIC_API_KEY="[YOUR_API_KEY]"
export GOOGLE_API_KEY="[YOUR_API_KEY]"
export BEDROCK_ROLE_ARN="[BEDROCK_ROLE_ARN]"
```

Code usage (`evalplus/provider/openai.py` - imports openai which reads env vars):
```python
import openai
# OpenAI client automatically reads OPENAI_API_KEY from environment
```

Access Control:
No RBAC system found in codebase. No user/group/role management.

Audit Logging:
Basic logging exists but not for security (`evalplus/gen/util/ollama_request.py:9-10`):
```python
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
```

No audit trail for credential access or model usage.

Enterprise Integration:
No SSO, LDAP, or enterprise authentication features found.

Security Features:
Sandboxing for code execution (`evalplus/eval/__init__.py:91-96`):
```python
def query_maximum_memory_bytes() -> Optional[int]:
    maximum_memory_bytes = os.getenv(
        "EVALPLUS_MAX_MEMORY_BYTES", 4 * 1024 * 1024 * 1024
    )
    maximum_memory_bytes = min(int(maximum_memory_bytes), psutil.virtual_memory().total)
```

Basic resource limits (`evalplus/eval/utils.py:68-89`):
```python
def reliability_guard(maximum_memory_bytes: Optional[int] = None):
    if maximum_memory_bytes is not None:
        import resource
        resource.setrlimit(
            resource.RLIMIT_AS, (maximum_memory_bytes, maximum_memory_bytes)
        )
```

Justification for 1 point: Only supports environment variable-based credential management with basic execution sandboxing. No RBAC, audit logging, credential encryption, rotation, or enterprise integration features.

---

### S1F6: Cost Estimation and Budget Planning
Rating: 0/3

Cost Modeling:
No cost estimation logic found in the codebase. Searched for keywords like "cost", "price", "budget", "token_count" prediction but found none.

Resource Projection:
No token counting before execution. The framework only tracks execution after the fact.

Budget Tools:
No budget limiting, cost breakdown, or optimization suggestion features.

Evidence:
Examined `evalplus/evaluate.py`, `evalplus/codegen.py`, and `evalplus/config.py` - no cost-related configuration or estimation code exists.

The only resource-related configuration is execution timeouts and memory limits:
```python
# evalplus/config.py
DEFAULT_GT_TIME_LIMIT_FACTOR = 4.0
DEFAULT_MIN_TIME_LIMIT = 4.0
```

Justification for 0 points: Framework has no cost estimation, budgeting, or resource projection capabilities. It focuses purely on correctness and performance evaluation without financial considerations.

---

## Summary Assessment

Strengths:
- Outstanding model configuration (3/3): Supports 9+ backends with clean API and proper authentication
- Good environment setup (2/3): Docker support and proper dependency management

Weaknesses:
- Minimal dataset configuration (1/3): Fixed benchmarks only, no flexible data handling
- No cost features (0/3): Complete absence of cost estimation or budget planning
- Weak security (1/3): Only basic env var credentials, no enterprise features
- Basic prompt configuration (2/3): String-based templating without versioning

Overall Stage 1 Score: 9/18 (50%)

The framework excels at model provider integration but is designed specifically for fixed benchmark evaluation rather than general-purpose evaluation configuration. It prioritizes ease of use for specific benchmarks over configurability for diverse evaluation scenarios.