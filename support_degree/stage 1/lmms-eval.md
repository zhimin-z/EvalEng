# lmms-eval - Stage 1 (CONFIGURE) Evaluation

## Summary
lmms-eval is a comprehensive evaluation framework for Large Multimodal Models (LMMs) supporting image, video, and audio tasks. The framework demonstrates strong configuration capabilities for models and tasks, with good dataset management through HuggingFace integration. However, it lacks explicit logical configuration abstractions for datasets, has minimal security/access control features, and no built-in cost estimation capabilities. The framework is designed for research/evaluation rather than enterprise deployment.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Evidence: Datasets are loaded directly from HuggingFace without logical registration abstraction. In `lmms_eval/tasks/vstar_bench/utils.py`: datasets are loaded as `dataset = load_dataset("lmms-lab/vstar-bench", split="test")`. The `_default_template_yaml` files show configuration: `dataset_path: lmms-lab/vstar-bench` and `dataset_kwargs: {split: test}`. Gaps: No declarative schema definition, no version tracking API (relies on HF), no split strategy configuration (splits are hardcoded in YAML), no logical dataset registration before loading. Strengths: Supports multiple sources (HuggingFace, local paths via `video_base_dir`), straightforward loading. |
| S1F2: Model Configuration | 3 | Evidence: Excellent model configuration system. `examples/models/` directory contains 30+ model examples (qwen2_5_vl.sh, llava_onevision.sh, etc.). Models configured via CLI args: `--model qwen2_5_vl --model_args=pretrained=Qwen/Qwen2.5-VL-7B-Instruct,max_pixels=12845056,attn_implementation=flash_attention_2`. Supports 30+ providers (OpenAI, Anthropic, Claude, vLLM, SGLang, local models). Authentication via environment variables: `export OPENAI_API_KEY="<YOUR_API_KEY>"` (README.md). Resource allocation supported: `tensor_parallel_size=4, gpu_memory_utilization=0.85` (vllm_qwen2vl.sh). Clean Python API with model registration via `@register_model()` decorator (docs/model_guide.md). |
| S1F3: Prompt Configuration | 2 | Evidence: Task-level prompt configuration in YAML files. Example from `lmms_eval/tasks/vstar_bench/vstar_bench.yaml`: `post_prompt: "\nAnswer with the option's letter from the given choices directly."`, `generation_kwargs: {max_new_tokens: 16, temperature: 0, top_p: 1.0}`. Template system exists but basic - no Jinja2, limited variable substitution. Few-shot support exists: `num_fewshot: 0` in configs. Gaps: No prompt versioning, no template inheritance, no diff tools for prompts. Metric configuration exists in task YAMLs: `metric_list: [{metric: exact_match, aggregation: mean}]`. Templating is Python string formatting, not a dedicated engine. |
| S1F4: Environment Setup | 2 | Evidence: Dependencies specified in `pyproject.toml` with version constraints: `python = "^3.10"`, `torch = "^2.4.0"`, `transformers = "^4.46.0"`. Installation via pip/uv: `pip install -e .` or `uv sync` (README.md). Docker not officially provided (no Dockerfile in repo). Setup instructions in docs: `docs/run_examples.md` contains detailed model-specific setup. Conda/pip requirements scattered across examples. Gaps: No official Docker image, no automated setup script, dependencies spread across multiple files (miscs/llava_repr_requirements.txt, etc.), manual environment troubleshooting common (httpx, protobuf version issues mentioned in README). Hardware specs implicit (CUDA required, multi-GPU via accelerate). |
| S1F5: Security & Access | 1 | Evidence: Only environment variable-based credential management: `export OPENAI_API_KEY="<YOUR_API_KEY>"`, `export ANTHROPIC_API_KEY`, etc. (README.md). No RBAC, no audit logging, no access control system. Single-user oriented. Gaps: No vault integration, no credential encryption, no multi-user access control, no SSO, no enterprise security features. This is expected for an academic/research tool but limits enterprise use. Evidence from codebase shows direct API key usage without abstraction layers. |
| S1F6: Cost Estimation | 0 | Evidence: No cost estimation features found in codebase. No token counting before execution, no budget limits, no cost modeling. Batch size configuration exists (`--batch_size 1`) but not for cost optimization. Reasoning: Searched for "cost", "budget", "token_count", "price" in configs and code - no relevant features. Framework focuses on evaluation accuracy, not cost management. Users must manually calculate costs based on API usage. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (2/3)

Strengths:
- Multiple data sources supported: HuggingFace datasets (`load_dataset()`), local file paths (`video_base_dir`), cloud storage indirectly
- Over 100 task configurations demonstrate flexibility
- Clear YAML-based task configuration system

Evidence from codebase:
```yaml
# From lmms_eval/tasks/vstar_bench/_default_template_yaml
dataset_path: lmms-lab/vstar-bench
dataset_kwargs:
  split: test
  
# From lmms_eval/tasks/megabench/_default_template_yaml
dataset_path: TIGER-Lab/MEGA-Bench
```

```python
# From lmms_eval/tasks/vstar_bench/utils.py
dataset = load_dataset("lmms-lab/vstar-bench", split="test")
```

Gaps:
- No logical dataset registration: Datasets are loaded immediately, not registered as logical references first
- No schema API: Column types/constraints are implicit from HuggingFace dataset structure
- No split strategies: Splits hardcoded in YAML (`split: test`), no declarative 70/20/10 or stratified sampling
- Version tracking: Relies entirely on HuggingFace versioning, no framework-level version API
- No validation rules: No way to specify field constraints (e.g., "text field, 1-500 chars")

Rating justification: Works for 2-3 sources (HuggingFace, local files), basic config, but lacks logical abstraction layer and schema definition. Falls between 1pt and 2pt - choosing 2pt because multiple sources work well despite missing advanced features.

### S1F2: Model Configuration (3/3)

Strengths:
- Comprehensive provider support: 30+ models including OpenAI, Anthropic, Claude, vLLM, SGLang, HuggingFace models
- Clean CLI configuration with `--model` and `--model_args`
- Resource allocation controls (tensor parallelism, GPU memory)
- Secure environment variable-based authentication
- Model registration system via decorators

Evidence:
```bash
# From examples/models/qwen25vl.sh
accelerate launch --num_processes=8 --main_process_port=12346 -m lmms_eval \
    --model qwen2_5_vl \
    --model_args=pretrained=Qwen/Qwen2.5-VL-7B-Instruct,max_pixels=12845056,attn_implementation=flash_attention_2 \
    --tasks mme \
    --batch_size 1
```

```python
# From docs/model_guide.md
from lmms_eval.api.registry import register_model

@register_model("<name1>", "<name2>")
class MyCustomLM(LM):
    def __init__(self, pretrained: str, device: str = "cuda", kwargs):
        # Clean initialization pattern
```

```bash
# Authentication from README.md
export OPENAI_API_KEY="<YOUR_API_KEY>"
export ANTHROPIC_API_KEY="<YOUR_API_KEY>"
export HF_TOKEN="<YOUR_API_KEY>"
```

```bash
# Resource allocation from examples/models/vllm_qwen2vl.sh
python3 -m lmms_eval \
    --model vllm \
    --model_args model=Qwen/Qwen2-VL-7B-Instruct,tensor_parallel_size=4 \
    --batch_size 64
```

Why 3/3: 5+ providers, clean YAML/CLI config, secure env var auth, resource control, validation through model initialization. Meets all criteria for full points.

### S1F3: Prompt Configuration (2/3)

Strengths:
- Per-task prompt configuration in YAML files
- Generation parameter control (temperature, max_tokens, etc.)
- Post-prompt customization
- Few-shot support
- Metric configuration per task

Evidence:
```yaml
# From lmms_eval/tasks/vstar_bench/vstar_bench.yaml
post_prompt: "\nAnswer with the option's letter from the given choices directly."
generation_kwargs:
  max_new_tokens: 16
  temperature: 0
  top_p: 1.0
  num_beams: 1
  do_sample: false

# From lmms_eval/tasks/egoschema/egoschema.yaml
num_fewshot: 0
metric_list:
  - metric: exact_match
    aggregation: mean
    higher_is_better: true
```

```python
# Template usage from task files (basic string formatting)
def doc_to_text(self, doc):
    question = doc["question"]
    return f"Question: {question}\nAnswer with the option's letter."
```

Gaps:
- No advanced templating: String formatting only, not Jinja2 or similar
- No prompt versioning: Can't reference prompt_v1 vs prompt_v2
- No template inheritance: Each task defines prompts independently
- Limited variable substitution: Basic string interpolation, no complex logic
- No diff tools: Can't compare prompt versions systematically

Why 2/3: Basic templating with variable substitution, limited few-shot, no versioning. Between 1pt and 2pt - choosing 2pt because generation kwargs and metric config are well-designed despite templating limitations.

### S1F4: Environment Setup (2/3)

Strengths:
- Modern dependency management with pyproject.toml
- UV tool support for reproducible environments
- Comprehensive setup documentation
- Multi-GPU support via accelerate

Evidence:
```toml
# From pyproject.toml
[project]
requires-python = "^3.10"
dependencies = [
    "torch>=2.4.0",
    "transformers>=4.46.0",
    "accelerate",
    # ... 50+ dependencies with versions
]
```

```bash
# From README.md - Modern UV installation
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync  # Creates environment from uv.lock
uv run python -m lmms_eval --help
```

```markdown
# From docs/run_examples.md - Model-specific setup
# Install LLaVA dependencies
cd /path/to/LLaVA-NeXT
python3 -m pip install -e ".[train]"
python3 -m pip install flash-attn --no-build-isolation
```

Gaps:
- No official Docker image: No Dockerfile in repository root
- No automated setup script: Manual pip install steps required
- Scattered requirements: Multiple requirements files (llava_repr_requirements.txt, tinyllava_repr_requirements.txt)
- Common issues documented but not solved: README mentions httpx, protobuf version conflicts
- Hardware specs implicit: CUDA required but not validated on startup

```bash
# From README.md - Manual troubleshooting required
python3 -m pip install httpx==0.23.3
python3 -m pip install protobuf==3.20
python3 -m pip install numpy==1.26
```

Why 2/3: Requirements file with pinned deps, manual setup instructions, but lacks containerization and automated setup. Good for research use but not production-ready.

### S1F5: Security & Access Control (1/3)

Strengths:
- Environment variable-based credential management
- Separate API keys for different providers

Evidence:
```bash
# From README.md
export OPENAI_API_KEY="<YOUR_API_KEY>"
export HF_HOME="<Path to HF cache>" 
export HF_TOKEN="<YOUR_API_KEY>"
export ANTHROPIC_API_KEY="<YOUR_API_KEY>"
export DASHSCOPE_API_KEY="<YOUR_API_KEY>"
```

Gaps (nearly everything):
- No vault integration: No HashiCorp Vault, AWS Secrets Manager support
- No encryption at rest: Keys stored in plain environment variables
- No RBAC: No user/role/permission system
- No access control: Single-user tool, anyone with env access has full access
- No audit logging: No tracking of who ran what evaluations
- No SSO/LDAP: No enterprise authentication
- No compliance features: No SOC2, HIPAA considerations
- No credential rotation: Manual key updates only

Why 1/3: Only environment variables, no access control system. This is typical for academic/research frameworks but limits enterprise adoption. Barely meets minimum requirement for credential management.

### S1F6: Cost Estimation (0/3)

Complete absence of cost features:

Search evidence:
- Searched codebase for: "cost", "budget", "price", "token_count", "estimate" - no relevant results
- No cost modeling API
- No token counting before execution
- No budget limit configuration
- No provider pricing data
- No cost optimization suggestions

What exists instead:
```bash
# Batch size for throughput, not cost optimization
--batch_size 1
```

Why 0/3: No cost estimation features whatsoever. Framework designed for accuracy evaluation, not cost management. Users must manually track API costs.

## Key Observations

### Framework Strengths:
1. Excellent model configuration: 30+ providers, clean API, good resource control
2. Strong task ecosystem: 100+ benchmarks with consistent YAML configuration
3. Modern tooling: UV support, accelerate integration, comprehensive docs
4. Research-oriented: Perfect for academic evaluation and benchmarking

### Critical Gaps:
1. No logical dataset abstraction: Direct loading without registration layer
2. Basic templating: No Jinja2, versioning, or advanced prompt management
3. Minimal security: Environment variables only, no enterprise features
4. No cost management: Complete absence of budgeting/estimation tools
5. Setup complexity: Manual dependency management, no containerization

### Stage 1 Total: 10/18 points (55.6%)

Overall Assessment: lmms-eval excels at model configuration and has a solid task management system, but lacks enterprise-grade features like logical dataset configuration, advanced prompt management, security controls, and cost estimation. The framework is well-designed for its intended research/academic use case but would require significant enhancement for production or enterprise deployment.