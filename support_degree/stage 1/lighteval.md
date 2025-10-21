# Lighteval (huggingface__lighteval) - Stage 1 (CONFIGURE) Evaluation

## Summary
Lighteval provides strong configuration capabilities with excellent multi-backend model support and comprehensive dataset handling through HuggingFace. The framework emphasizes declarative task definition through YAML/Python configs with good prompt templating. However, it lacks dedicated cost estimation features, schema validation APIs, and advanced security features like RBAC. The system excels at logical configuration of evaluations without requiring physical instantiation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Evidence: Supports HuggingFace datasets primarily through `hf_repo`, `hf_subset`, and `hf_avail_splits` parameters in task configs (see `examples/nanotron/custom_evaluation_tasks.py`). Also supports loading from local files. However, lacks explicit schema definition API, formal versioning system, or advanced split strategies beyond simple train/test splits. Dataset registration is logical (no loading required) through task config parameters like `hf_repo="lighteval/mmlu"`. Missing: declarative schema constraints, stratified splitting config, built-in dataset versioning. |
| S1F2: Model Configuration | 3 | Evidence: Excellent provider support with 10+ backends (transformers, vllm, sglang, TGI, inference endpoints, litellm, etc.) shown in `examples/model_configs/`. Clean YAML-based config API with examples like `transformers_model.yaml`, `vllm_model_config.yaml`, `sglang_model_config.yaml`. Supports authentication via env vars (`huggingface-cli login`). Resource allocation through parameters like `batch_size`, `tensor_parallel_size`, `gpu_memory_utilization` (in `vllm_model_config.yaml`). Can override configs at runtime. Covers all major LLM providers and local inference. |
| S1F3: Prompt Configuration | 3 | Evidence: Full templating system via Python functions. Variable substitution shown in `ZEROSHOT_QA_USER_PROMPT` in `examples/custom_tasks_templates/custom_yourbench_task.py` with `{question}` placeholders. Few-shot support through `few_shots_split` and `few_shots_select` parameters in `LightevalTaskConfig`. Prompt versioning possible through task versioning (`version=0` parameter). Metric configuration via `metrics=[Metrics.loglikelihood_acc]` in task configs. Template inheritance through Python class inheritance (see `CustomMMLUEvaluationTask` extending `LightevalTaskConfig`). Stop sequences configurable: `stop_sequence=["\n"]`. |
| S1F4: Environment Setup | 2 | Evidence: Uses `pyproject.toml` for dependency management with pinned versions. No official Docker images mentioned in README or docs. Setup via `pip install lighteval` with optional extras (`pip install -e .[dev]`). Hardware config through model parameters like `device: "cuda"` in YAML configs. Multi-GPU support via `tp_size`, `dp_size` in vllm/sglang configs. Missing: official Dockerfile, automated setup scripts (no `make setup`), Singularity support. Basic dependency management but lacks containerization and automation. |
| S1F5: Security & Access | 1 | Evidence: Basic credential management via `huggingface-cli login` (environment-based). Authentication for inference endpoints shown in `tgi_model.yaml` with `inference_server_auth: null` field. No evidence of: RBAC, audit logging, vault integration, SSO/LDAP support, or compliance certifications. The `endpoint_model.yaml` shows `endpoint_type: "protected"` but no detailed access control. Minimal security features beyond basic auth. |
| S1F6: Cost Estimation | 0 | Evidence: No cost estimation features found in codebase. No token counting before execution, no budget limits, no cost models for different providers. The generation parameters like `max_new_tokens: 256` in configs could theoretically be used for manual estimation, but framework provides no built-in cost calculation. Missing: pre-run cost estimation, budget tools, provider cost comparison, optimization suggestions. Would require external calculation entirely. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Strengths:
- Logical dataset registration without loading via `hf_repo` and `hf_subset` parameters
- HuggingFace Hub integration for 7000+ tasks (`examples/tasks/all_tasks.txt` shows extensive task coverage)
- Support for multiple splits: `hf_avail_splits=["train", "test", "validation"]`
- Few-shot selection strategies: `few_shots_select="random_sampling_from_train"` or `"sequential"`

Weaknesses:
- No declarative schema definition API (can't specify "text field, 1-500 chars, required")
- Split strategies limited to basic train/test/validation - no stratified splitting by field
- No formal versioning system (only manual `version=0` in task config)
- No support for databases, APIs, or cloud storage beyond HuggingFace

Code Evidence:
```python
# From examples/nanotron/custom_evaluation_tasks.py
LightevalTaskConfig(
    name="gsm8k",
    hf_repo="gsm8k",
    hf_subset="main",
    hf_avail_splits=["train", "test"],
    evaluation_splits=["test"],
    few_shots_split=None,
    few_shots_select="random_sampling_from_train",
)
```

### S1F2: Model and Backend Configuration
Strengths:
- 10+ backend providers with dedicated config examples
- Clean YAML-based configuration system
- Runtime parameter overrides supported
- Comprehensive generation parameters (temperature, top_p, etc.)
- Multi-GPU configuration (TP, DP, PP)

Code Evidence:
```yaml
# From examples/model_configs/vllm_model_config.yaml
model_parameters:
  model_name: "HuggingFaceTB/SmolLM2-1.7B-Instruct"
  tensor_parallel_size: 1
  data_parallel_size: 1
  gpu_memory_utilization: 0.6
  generation_parameters:
    temperature: 0.0
    top_p: 0.9
```

```yaml
# From examples/model_configs/sglang_model_config.yaml
model_parameters:
  tp_size: 1
  dp_size: 1
  mem_fraction_static: 0.8
  chunked_prefill_size: 4096
```

### S1F3: Evaluation Parameters and Prompt Configuration
Strengths:
- Full Python-based templating engine
- Variable substitution and few-shot example injection
- Prompt versioning through task versions
- Flexible metric configuration
- Stop sequence control

Code Evidence:
```python
# From examples/custom_tasks_templates/custom_yourbench_task.py
ZEROSHOT_QA_USER_PROMPT = """Answer the following question:

<question>
{question}
</question>

Enclose your full answer in <answer> XML tags."""

def yourbench_prompt(line, task_name: str = ""):
    return Doc(
        task_name=task_name,
        query=ZEROSHOT_QA_USER_PROMPT.format(question=line["question"]),
        choices=[line["ground_truth_answer"]],
        gold_index=0,
    )
```

Few-shot support:
```python
# From examples/nanotron/custom_evaluation_tasks.py
CustomMMLUEvaluationTask(
    name="mmlu:anatomy",
    few_shots_split="dev",
    few_shots_select="sequential",
)
```

### S1F4: Environment Setup and Dependency Management
Strengths:
- Modern `pyproject.toml` for dependency management
- Optional dependency groups for different backends
- Clear installation instructions

Weaknesses:
- No official Docker images
- No automated setup scripts
- Manual environment configuration required

Code Evidence:
```bash
# From README.md
pip install lighteval
# With extras:
pip install -e .[dev]
```

### S1F5: Security and Access Control
Strengths:
- Basic HuggingFace authentication
- Protected endpoint support

Weaknesses:
- No RBAC system
- No audit logging
- No vault integration
- No SSO/LDAP support
- No encryption at rest mentioned

Code Evidence:
```yaml
# From examples/model_configs/endpoint_model.yaml
model_parameters:
  endpoint_type: "protected"
```

```bash
# From README.md
huggingface-cli login
```

### S1F6: Cost Estimation and Budget Planning
Complete Absence:
- No cost estimation functionality in codebase
- No budget limit configuration
- No token counting pre-execution
- Manual calculation required for all costs

## Key Observations

### Green Flags:
1. Extensive example gallery: 100+ task examples in `examples/tasks/` directory
2. Rich model configuration: 10+ backend configs with detailed examples
3. Strong documentation: Comprehensive MDX docs in `docs/source/`
4. Tutorial notebooks: Custom task templates provided
5. Plugin system: Custom task and metric support

### Red Flags:
1. No cost estimation: Complete absence of budgeting features
2. Limited security: No RBAC, audit logs, or enterprise auth
3. No containerization: Missing Docker/Singularity support
4. Schema-less datasets: No validation or constraint definition

### Notable Design Choices:
1. Python-first configuration: Uses Python classes for task definition rather than pure YAML
2. HuggingFace-centric: Heavy reliance on HF Hub for datasets and models
3. Backend flexibility: Strong support for multiple inference backends
4. Declarative tasks: Logical task definition without data loading

## Recommendations for Improvement

1. Add cost estimation: Implement pre-run token counting and cost projection
2. Enhance security: Add RBAC, audit logging, and vault integration
3. Improve dataset handling: Add schema validation API and stratified splitting
4. Containerization: Provide official Docker images and Dockerfiles
5. Automated setup: Add setup scripts and make commands

## Conclusion

Lighteval excels at model and prompt configuration with excellent multi-backend support (10+ providers). The framework provides strong logical configuration capabilities through YAML and Python configs. However, it completely lacks cost estimation features and has minimal security controls beyond basic authentication. The dataset handling is functional but missing advanced features like schema validation and formal versioning. Overall, it's a solid evaluation framework for configuration but needs enhancement in cost management and security for enterprise use.