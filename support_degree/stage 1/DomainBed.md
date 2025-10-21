# DomainBed - Stage 1 (CONFIGURE) Evaluation

## Summary
DomainBed is a PyTorch-based benchmark suite for domain generalization research focused on computer vision tasks. It provides infrastructure for training and evaluating algorithms across multiple datasets, but it is not an LLM evaluation framework. The configuration capabilities are centered around computer vision model training (ResNets, CNNs) rather than LLM evaluation. This mismatch makes most Stage 1 features either not applicable or would require fundamental architectural changes to support LLM evaluation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset abstraction exists but only for image datasets. Datasets are hardcoded classes (VLCS, PACS, DomainNet) with no logical configuration layer. No support for text/LLM datasets, no schema definition, and splits are computed during dataset instantiation rather than configured declaratively. See `domainbed/datasets.py` lines 33-50 for the hardcoded DATASETS list and dataset classes that inherit from `MultipleDomainDataset`. |
| S1F2: Model Configuration | 0 | No support for LLM providers. Only supports computer vision models (ResNet, MNIST_CNN, WideResNet) hardcoded in `domainbed/networks.py`. No configuration system for LLM APIs, no provider abstraction, no authentication management for API services. The `hparams_registry.py` only defines hyperparameters for CV models (lr, weight_decay, resnet_dropout). |
| S1F3: Prompt Configuration | 0 | No prompt or template system exists. This is a computer vision framework without any text generation, prompting, or LLM-as-judge capabilities. No templating engine, no parameter configuration for language models, no few-shot support. |
| S1F4: Environment Setup | 2 | Basic dependency management via `requirements.txt` (`domainbed/requirements.txt` lists torch, torchvision, wilds, etc.) with pinned versions. No Docker support, no automated setup scripts, manual installation required. Multi-GPU support exists (`command_launchers.py` lines 33-54 with `multi_gpu_launcher`) but no containerization or hardware validation. |
| S1F5: Security & Access | 0 | No security features present. No credential management system, no RBAC, no audit logging, no enterprise integration. The framework assumes local execution with direct access to models and data. |
| S1F6: Cost Estimation | 0 | No cost estimation or budgeting features. Framework is designed for local/cluster training of computer vision models, not cloud API usage. No token counting, no API cost modeling, no budget limits. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 1)

Evidence:
- `domainbed/datasets.py` lines 10-38 show hardcoded dataset list:
```python
DATASETS = [
    "Debug28", "Debug224", "ColoredMNIST", "RotatedMNIST",
    "VLCS", "PACS", "OfficeHome", "TerraIncognita", "DomainNet",
    "SVIRO", "WILDSCamelyon", "WILDSFMoW",
    "SpawriousO2O_easy", "SpawriousO2O_medium", ...
]
```

- Datasets are Python classes, not configuration files. Example from `datasets.py` lines 380-386:
```python
class VLCS(MultipleEnvironmentImageFolder):
    CHECKPOINT_FREQ = 300
    ENVIRONMENTS = ["C", "L", "S", "V"]
    def __init__(self, root, test_envs, hparams):
        self.dir = os.path.join(root, "VLCS/")
        super().__init__(self.dir, test_envs, hparams['data_augmentation'], hparams)
```

Limitations:
- No schema definition API (line 44-50 show only `INPUT_SHAPE` and `ENVIRONMENTS` attributes)
- No version tracking system
- No declarative split configuration (splits determined by test_envs at runtime)
- Only supports image folders, not text datasets
- No support for JSON, CSV, HuggingFace datasets, databases, or APIs

### S1F2: Model Configuration (Rating: 0)

Evidence:
- `domainbed/networks.py` lines 145-179 show only CV models:
```python
def Featurizer(input_shape, hparams):
    """Auto-select an appropriate featurizer for the given input shape."""
    if len(input_shape) == 1:
        return MLP(input_shape[0], hparams["mlp_width"], hparams)
    elif input_shape[1:3] == (28, 28):
        return MNIST_CNN(input_shape)
    elif input_shape[1:3] == (224, 224):
        return ResNet(input_shape, hparams)
```

- `hparams_registry.py` lines 17-29 show hyperparameter definition:
```python
_hparam('resnet18', False, lambda r: False)
_hparam('resnet_dropout', 0., lambda r: r.choice([0., 0.1, 0.5]))
_hparam('freeze_bn', False, lambda r: False)
```

Why not applicable:
- No LLM provider support (OpenAI, Anthropic, HuggingFace inference)
- No API authentication mechanism
- No configuration for temperature, top_p, max_tokens
- Framework is hardwired for local PyTorch model training

### S1F3: Prompt Configuration (Rating: 0)

Evidence:
This feature is entirely absent. Searching the entire codebase reveals:
- No mention of "prompt", "template", or "few-shot" in any configuration files
- No templating engine (Jinja2, etc.)
- The `scripts/train.py` and `scripts/sweep.py` show only image model training pipelines

Why not applicable:
Computer vision frameworks don't use prompts. This is a fundamental architectural mismatch.

### S1F4: Environment Setup (Rating: 2)

Evidence:
- `domainbed/requirements.txt` shows pinned dependencies:
```txt
torch==1.12.1
torchvision==0.13.1
backpack-for-pytorch==1.3.0
numpy==1.22.4
```

- Multi-GPU support in `command_launchers.py` lines 33-54:
```python
def multi_gpu_launcher(commands):
    """Launch commands on the local machine, using all GPUs in parallel."""
    available_gpus = [x for x in os.environ['CUDA_VISIBLE_DEVICES'].split(',')]
    # ... GPU assignment logic
```

Limitations:
- No Dockerfile or container support
- No automated setup script (no `make setup` or `pip install -e .`)
- No conda environment file
- No hardware validation on startup
- Manual installation required

### S1F5: Security & Access Control (Rating: 0)

Evidence:
Complete absence of security features throughout the codebase:
- No credential management (`grep -r "vault\|secret\|password" * returns nothing relevant`)
- No RBAC system
- No audit logging
- No authentication layer

This is expected for a research codebase designed for single-user local/cluster execution.

### S1F6: Cost Estimation (Rating: 0)

Evidence:
- No cost-related code in any file
- `sweep.py` and `train.py` show no budget or cost tracking
- Framework designed for academic clusters with allocated compute, not pay-per-use APIs

Why not applicable:
This framework trains models locally/on clusters, not via paid APIs. Cost estimation is irrelevant for this use case.

## Critical Observations

1. Fundamental Architecture Mismatch: DomainBed is a domain generalization benchmark for computer vision, not an LLM evaluation framework. It would require a complete rewrite to support LLM evaluation.

2. No LLM Support: The entire framework is built around `torch.nn.Module`, image datasets, and ResNet/CNN architectures. There's no infrastructure for API calls, text processing, or language model evaluation.

3. Research Tool vs. Production Framework: This is designed for academic research with manual configuration and execution, not as a production-ready evaluation platform.

4. Configuration via Code: Most configuration happens through Python inheritance and method overrides rather than declarative config files, making it inflexible for the CONFIGURE stage requirements.

## Recommendation

DomainBed should not be evaluated as an LLM evaluation framework as it serves a completely different purpose. If forced to rate it for LLM evaluation:
- Total Score: 3/18 (only partial credit for basic dependency management and multi-GPU support)
- The framework would need fundamental architectural changes to support even basic LLM evaluation workflows

For actual LLM evaluation frameworks, consider tools like EleutherAI's lm-evaluation-harness, Anthropic's evals, or OpenAI's evals instead.