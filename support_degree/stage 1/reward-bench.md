# RewardBench - Stage 1 (CONFIGURE) Evaluation

## Summary
RewardBench is a specialized evaluation framework for reward models and DPO-trained models. It provides limited configuration capabilities focused on model selection and inference parameters, primarily through YAML configs and CLI arguments. The framework is opinionated toward its specific use case (reward model evaluation) with minimal abstraction for datasets, environments, or cost estimation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Evidence: The framework has hardcoded dataset loading functions (`load_eval_dataset`, `load_bon_dataset`, `load_bon_dataset_v2` in `rewardbench/utils.py` - not shown but referenced). Dataset specification is minimal - only supports `--dataset` CLI arg (e.g., `scripts/run_v2.py` line 56). No schema definition, versioning, or declarative split strategies. Dataset format is implicitly determined by code logic rather than user configuration. Example: `parser.add_argument("--dataset", type=str, default="allenai/reward-bench-2")` shows basic HF path support only. |
| S1F2: Model Configuration | 2 | Evidence: Model configuration exists via `scripts/configs/eval_configs.yaml` with 100+ model entries. Config includes provider support (OpenAI, Anthropic, HF models), parameters like `batch_size`, `trust_remote_code`, `torch_dtype`, and `num_gpus`. Authentication is basic env vars only (`HF_TOKEN`, `ANTHROPIC_API_KEY`). Example from `eval_configs.yaml`: `openbmb/UltraRM-13b: {model: 'openbmb/UltraRM-13b', tokenizer: '...', chat_template: 'openbmb', batch_size: 8}`. Missing: validation, resource allocation beyond GPU count, multi-region support. Config override possible but limited to CLI args. |
| S1F3: Prompt Configuration | 1 | Evidence: No templating system for prompts. Chat templates hardcoded via fastchat (`get_conv_template`) in scripts like `run_rm.py` line 79: `conv = get_conv_template(chat_template)`. Parameter setting via CLI only (`--batch_size`, `--max_length`). No few-shot support, prompt versioning, or template inheritance. Generative models use hardcoded prompt formats in `rewardbench/generative.py` (not shown). Metric configuration is implicit - always computes accuracy, no custom metrics or threshold config. |
| S1F4: Environment Setup | 2 | Evidence: Basic dependency management exists. `setup.py` lines 37-61 shows pinned dependencies: `transformers==4.51.0`, `trl>=0.8.2`, etc. Dockerfile exists (line 31 of structure) for containerization. Setup via standard `pip install -e .` (README line 79). Optional extras for generative models (`pip install -e ".[generative]"` line 82). Missing: automated setup scripts, hardware compatibility checks, conda support. Dependencies are mix of pinned and unpinned. Docker image referenced but workflow unclear from provided files. |
| S1F5: Security & Access | 1 | Evidence: Basic env var credential management only. `run_dpo.py` lines 30-36 shows `HF_TOKEN = os.getenv("HF_TOKEN", None)` pattern. Beaker configs show secret references: `beaker_eval.yaml` line 16-22 has `{"name": "HF_TOKEN", "secret": "HF_TOKEN"}`. No RBAC, audit logging, encryption, SSO, or vault integration. All models/datasets accessible if token provided. No user/group system. Secrets passed as env vars in CI/CD (`submit_eval_jobs.py` line 34-37 shows secret mounting). |
| S1F6: Cost Estimation | 0 | Evidence: No cost estimation features exist. No token counting before execution, no budget limits, no pricing models, no optimization suggestions. Scripts run inference without cost projection. Batch size is manual (`--batch_size` arg), not optimized for cost. No warnings about expensive API calls. Example: `run_generative.py` calls API models without cost checks (lines not shown but implied by API usage). No cost tracking in outputs or logs. |

## Key Observations

### Strengths
1. Model configuration breadth: 100+ preconfigured models in `eval_configs.yaml` covering major providers
2. Basic containerization: Docker support with Beaker integration for AI2 infrastructure
3. Practical focus: Opinionated design works well for its specific use case

### Weaknesses
1. No dataset abstraction: Datasets are hardcoded function calls, no discovery or schema
2. Minimal prompt control: No templating system, everything hardcoded or via fastchat
3. No cost awareness: Framework cannot estimate or limit costs before execution
4. Limited security: Only env var secrets, no enterprise features
5. Environment setup manual: Requires users to handle dependencies without automation

### Architecture Pattern
RewardBench follows a script-based evaluation pattern rather than a configurable framework pattern. Each script (`run_rm.py`, `run_dpo.py`, `run_v2.py`) is a standalone evaluation pipeline with CLI args and YAML configs for model selection. This makes configuration simple but inflexible.

### Evidence of Limitations
- Dataset: `load_eval_dataset()` function (referenced but not shown) likely has hardcoded dataset URLs
- Prompts: `rewardbench/generative.py` (line 10 in imports) handles generative model prompts, but no template files visible
- Costs: No cost-related code in any script - straight to inference
- Schema: Dataset columns are hardcoded strings like `"text_chosen"`, `"text_rejected"` throughout

### Notable Configuration Gaps
1. No way to define custom evaluation metrics
2. No split strategies (train/val/test) - single dataset mode only  
3. No experiment tracking integration mentioned
4. No configuration validation before execution
5. No resource optimization (batch size is manual guess)

## Stage 1 Total: 7/18 points
The framework provides basic model configuration and dependency management but lacks sophisticated configuration capabilities for datasets, prompts, security, and cost control. It's designed for expert users who understand reward model evaluation, not for general-purpose configurable evaluation workflows.