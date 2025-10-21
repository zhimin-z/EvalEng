# COMET - Stage 1 (CONFIGURE) Evaluation

## Summary
COMET is a neural framework for machine translation evaluation, not a general-purpose evaluation framework. It's designed specifically for evaluating MT systems using learned metrics. While it has configuration capabilities for its specific domain, it lacks the broad dataset/model configuration features expected of a general evaluation framework. Configuration is primarily focused on training evaluation metrics rather than configuring diverse evaluation scenarios.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited to CSV format with fixed schema for MT data; no abstraction layer |
| S1F2: Model Configuration | 2 | Supports multiple encoder models but limited to specific architecture; basic YAML config |
| S1F3: Prompt Configuration | 0 | No prompt configuration - not applicable for this metric-based framework |
| S1F4: Environment Setup | 2 | Poetry-based dependencies with pinned versions; basic Docker support mentioned but not provided |
| S1F5: Security & Access | 1 | Basic environment variable auth only; no RBAC or advanced security |
| S1F6: Cost Estimation | 0 | No cost estimation or budgeting features |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration
Rating: 1/3

Evidence:

1. Dataset Format: Only CSV with fixed schema
```python
# From docs/source/training.md
"""
To train your metric we expect your data to be a csv with the following columns:
- `src`: The source segment.
- `mt`: The machine translation hypothesis.
- `ref`: The reference segment.
- `score`: The human judgment score.
"""
```

2. No Dataset Abstraction: Direct file loading without registry
```python
# From comet/models/base.py, lines 394-400
def train_dataloader(self) -> DataLoader:
    """Method that loads the train dataloader."""
    data_path = self.hparams.train_data[
        self.current_epoch % len(self.hparams.train_data)
    ]
    train_dataset = self.read_training_data(data_path)
    logger.info(f"Loading {data_path}.")
```

3. Configuration Example: Simple path specification
```yaml
# From configs/models/regression_model.yaml
train_data: 
  - data/1720-da.csv
validation_data: 
  - data/wmt-ende-newstest2021.csv
  - data/wmt-enru-newstest2021.csv
  - data/wmt-zhen-newstest2021.csv
```

Limitations:
- No support for multiple data sources (HuggingFace, databases, APIs)
- No schema definition API
- No declarative split strategies
- No versioning support
- Must implement `read_training_data()` manually for each model type

### S1F2: Model and Backend Configuration
Rating: 2/3

Evidence:

1. Encoder Support: Multiple encoder models supported
```python
# From comet/encoders/__init__.py
str2encoder = {
    "BERT": BERTEncoder,
    "XLM-RoBERTa": XLMREncoder,
    "MiniLM": MiniLMEncoder,
    "XLM-RoBERTa-XL": XLMRXLEncoder,
    "RemBERT": RemBERTEncoder,
}
```

2. YAML Configuration: Clean config structure
```yaml
# From configs/models/regression_model.yaml
regression_metric:
  class_path: comet.models.RegressionMetric
  init_args:
    encoder_model: XLM-RoBERTa
    pretrained_model: xlm-roberta-large
    optimizer: AdamW
    encoder_learning_rate: 1.0e-06
    learning_rate: 1.5e-05
    batch_size: 16
```

3. Model Loading: Supports local and HuggingFace Hub
```python
# From comet/models/__init__.py, lines 48-64
def download_model(
    model: str,
    saving_directory: Union[str, Path, None] = None,
    local_files_only: bool = False,
) -> str:
    try:
        model_path = snapshot_download(
            repo_id=model, cache_dir=saving_directory, local_files_only=local_files_only
        )
    except Exception:
        try:
            checkpoint_path = download_model_legacy(model, saving_directory)
        except Exception:
            raise KeyError(f"Model '{model}' not supported by COMET.")
```

Limitations:
- Limited to specific encoder architectures (no arbitrary model support)
- No resource allocation configuration (GPU/CPU assignment)
- Authentication only via environment variables
- No multi-provider support (only HuggingFace-style models)

### S1F3: Evaluation Parameters and Prompt Configuration
Rating: 0/3

Evidence:

This framework is designed for metric evaluation, not prompt-based LLM evaluation. There is no prompt configuration system because COMET doesn't use prompts - it uses learned neural metrics.

```python
# From comet/models/base.py
# Models take structured input (src, mt, ref) not prompts
def prepare_sample(
    self,
    sample: List[dict],
    stage: str = "fit",
    *args,
    kwargs,
):
    """This method will be called by dataloaders to prepared data to input to the
    model.
    
    Args:
        sample (List[dict]): Batch of train/val/test samples.
    """
```

Justification:
- No templating system
- No prompt versioning
- No few-shot configuration
- Not applicable to this framework's purpose

### S1F4: Environment Setup and Dependency Management
Rating: 2/3

Evidence:

1. Dependency Management: Poetry with pinned versions
```toml
# From pyproject.toml
[tool.poetry.dependencies]
python = "^3.8.0"
sentencepiece = "^0.2.0"
pandas = ">=1.4.1"
transformers = "^4.17"
pytorch-lightning = "^2.0.0"
torch = ">=1.6.0"
numpy = "^1.20.0"
```

2. Installation Instructions: Simple pip install
```markdown
# From README.md
pip install --upgrade pip
pip install unbabel-comet
```

3. Development Setup: Clear instructions
```bash
# From README.md
git clone https://github.com/Unbabel/COMET
cd COMET
pip install poetry
poetry install
```

Limitations:
- No official Dockerfile provided (only referenced)
- No automated setup scripts
- Limited hardware configuration documentation
- No conda environment file

### S1F5: Security and Access Control
Rating: 1/3

Evidence:

1. Basic Auth: Only environment variables and HuggingFace login
```markdown
# From README.md
Note: To use some COMET models such as `Unbabel/wmt22-cometkiwi-da` you must 
acknowledge it's license on Hugging Face Hub and log-in into hugging face hub.
```

2. No RBAC: No access control system visible in codebase

3. No Audit Logging: Standard Python logging only
```python
# From comet/__init__.py
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
```

Limitations:
- No credential encryption
- No vault integration
- No role-based access control
- No audit trails
- No enterprise authentication (SSO, SAML)

### S1F6: Cost Estimation and Budget Planning
Rating: 0/3

Evidence:

No cost estimation features found in the codebase. The framework focuses on metric computation, not API-based LLM calls that would incur costs.

```python
# From comet/cli/score.py
# Scoring is local computation, no cost estimation
def score_command() -> None:
    parser = ArgumentParser(description="Command for scoring MT systems.")
    parser.add_argument("-s", "--sources", type=Path_fr)
    parser.add_argument("-t", "--translations", type=Path_fr, nargs="+")
    parser.add_argument("-r", "--references", type=Path_fr)
    # No cost-related arguments
```

Justification:
- No token counting
- No budget limits
- No cost modeling
- Not applicable for this type of framework

## Key Observations

### Strengths:
1. Clear Model Configuration: YAML-based configuration for training metrics
2. Multiple Encoder Support: Supports various transformer models
3. Good Dependency Management: Poetry with pinned versions
4. Model Hub Integration: Clean HuggingFace Hub integration

### Weaknesses:
1. Not a General Evaluation Framework: Designed specifically for MT evaluation metrics
2. Limited Dataset Abstraction: Only CSV with fixed schema
3. No Security Features: Basic authentication only
4. No Cost Management: Not applicable to this framework
5. Missing Containerization: No Dockerfile provided despite documentation references

### Architecture Mismatch:
This framework is fundamentally different from the evaluation frameworks the rubric was designed for (like HELM, lm-evaluation-harness). COMET trains and applies learned metrics for MT evaluation, rather than configuring diverse evaluation scenarios with prompts and multiple data sources.

## Overall Stage 1 Score: 6/18 (33%)

The low score reflects that COMET is not designed as a general-purpose evaluation framework. It's a specialized tool for MT evaluation using neural metrics. The rubric criteria assume a framework that:
- Configures diverse evaluation scenarios
- Supports multiple data sources and formats
- Uses prompt-based evaluation
- Manages API costs

COMET does none of these because it serves a different purpose: training and applying learned metrics for translation quality assessment.