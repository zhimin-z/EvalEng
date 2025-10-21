# Quantus - Stage 1 (CONFIGURE) Evaluation

## Summary
Quantus is an XAI (Explainable AI) evaluation toolkit focused on evaluating neural network explanations across multiple metrics. While it excels at evaluation configuration, it lacks traditional evaluation framework configuration capabilities for datasets, models, and evaluation pipelines. Its configuration approach centers on metric instantiation with hyperparameters rather than declarative dataset/model registration.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No dataset abstraction exists. Users manually load data via numpy/torch/tf (see `tutorials/Tutorial_Getting_Started.ipynb`). No registration, schema, versioning, or split strategies. |
| S1F2: Model Configuration | 1 | Basic model wrapping via `ModelInterface` (`quantus/helpers/model/model_interface.py`) but no provider abstraction, multi-model configs, or resource allocation. Models passed directly to metrics. |
| S1F3: Prompt Configuration | 0 | Not applicable - this is an XAI evaluation framework, not an LLM evaluation framework. No prompt templates or parameter sweeps exist. |
| S1F4: Environment Setup | 2 | Has `pyproject.toml` with pinned dependencies and optional extras (`[torch]`, `[tensorflow]`, `[full]`). Docker not provided. Setup via `pip install quantus[torch]` works but requires manual framework selection. |
| S1F5: Security & Access | 0 | No credential management, RBAC, audit logging, or enterprise features. Pure Python library with no access controls. |
| S1F6: Cost Estimation | 0 | No cost estimation, budgeting, or resource projection capabilities. Framework focused on metric evaluation, not execution cost. |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (0/3)

Evidence:

From `tutorials/Tutorial_Getting_Started.ipynb`:
```python
# Load datasets and make loaders.
test_set = torchvision.datasets.MNIST(root='./sample_data', download=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=24)

# Load a batch of inputs and outputs to use for XAI evaluation.
x_batch, y_batch = iter(test_loader).next()
x_batch, y_batch = x_batch.cpu().numpy(), y_batch.cpu().numpy()
```

From `tutorials/Tutorial_Getting_Started_with_Tabular_Data.ipynb`:
```python
# Load datasets
df = pd.read_csv("assets/titanic3.csv")
# ... manual preprocessing ...
X = df_enc.drop(["survived"], axis=1).values
Y = df_enc["survived"].values
```

Analysis:
- No dataset abstraction: Users must manually load data using external libraries (torchvision, pandas, tensorflow_datasets)
- No registration system: Data passed directly as numpy arrays to metric `__call__()` methods
- No schema definition: Raw numpy arrays with implicit shapes
- No split strategies: Users manually create train/test splits via sklearn
- No versioning: No dataset version tracking exists

From `quantus/metrics/base.py` `__call__` signature:
```python
def __call__(
    self,
    model: Union[keras.Model, nn.Module, None],
    x_batch: np.ndarray,  # Raw numpy - no abstraction
    y_batch: np.ndarray,
    a_batch: Optional[np.ndarray],
    ...
)
```

Rating: 0 points - No dataset abstraction layer exists. Framework expects pre-loaded numpy arrays.

---

### S1F2: Model and Backend Configuration (1/3)

Evidence:

From `quantus/helpers/model/model_interface.py`:
```python
class ModelInterface(ABC):
    """Interface for model operations."""
    
    def __init__(
        self,
        model: Union["torch.nn.Module", "tf.keras.Model"],
        channel_first: bool = True,
        softmax: bool = False,
        model_predict_kwargs: Optional[Dict[str, Any]] = None,
        device: Optional[str] = None,
    ):
```

From `quantus/helpers/utils.py`:
```python
def get_wrapped_model(
    model: Union["torch.nn.Module", "tf.keras.Model"],
    channel_first: bool,
    softmax: bool,
    device: Optional[str],
    model_predict_kwargs: Optional[Dict[str, Any]],
) -> ModelInterface:
    """Wrap PyTorch or TensorFlow model."""
```

Analysis:
- Provider Support: Only PyTorch and TensorFlow supported via manual model passing
- No configuration files: Models configured via Python API only (no YAML/JSON)
- Authentication: Not applicable - local models only
- Resource allocation: Basic `device` parameter (`"cpu"` or `"cuda"`) but no GPU selection or batch size per model

From tutorial example:
```python
# User manually loads and passes model
model = LeNet()
model.load_state_dict(torch.load("tests/assets/mnist_model"))

# Then passes to metric directly
scores = metric(
    model=model,  # Direct model passing
    x_batch=x_batch,
    y_batch=y_batch,
    device=device,  # Simple device string
)
```

Positive aspects:
- Basic model interface abstraction exists
- Supports two major frameworks (PyTorch, TensorFlow)

Negative aspects:
- No declarative config (no YAML/JSON files)
- No multi-model orchestration
- No provider abstraction for APIs
- No resource management beyond simple device selection

Rating: 1 point - Basic model wrapping exists but lacks configuration infrastructure, multi-provider support, or resource management.

---

### S1F3: Evaluation Parameters and Prompt Configuration (0/3)

Evidence:

Quantus is an XAI evaluation framework, not an LLM evaluation framework. From `README.md`:
```markdown
Quantus is an eXplainable AI toolkit for responsible evaluation 
of neural network explanations.
```

The framework evaluates explanation methods (Saliency, GradCAM, etc.) on image/tabular data, not text generation or prompts.

From `quantus/metrics/base.py`:
```python
def __init__(
    self,
    abs: bool,  # Attribution parameters
    normalise: bool,
    normalise_func: Optional[Callable],
    aggregate_func: Callable,
    # No prompt-related parameters
):
```

Analysis:
- Not Applicable: This is an XAI evaluation library for computer vision/tabular models
- No LLM concepts (temperature, top_p, prompts, etc.)
- Evaluates explanation quality, not text generation

Rating: 0 points - Feature not applicable to this type of framework.

---

### S1F4: Environment Setup and Dependency Management (2/3)

Evidence:

From `pyproject.toml`:
```toml
[project]
name = "quantus"
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.19.5",
    "pandas>=1.5.3",
    "opencv-python>=4.5.5.62",
    # ... more pinned versions
]

[project.optional-dependencies]
torch = [
    "torch>=1.13.1; sys_platform != 'linux'",
    "torchvision>=0.15.1; sys_platform != 'linux'",
    "torch>=1.13.1, <2.0.0; sys_platform == 'linux' and python_version < '3.11'",
    # Platform-specific torch versions
]
tensorflow = [
    "tensorflow<2.16.0",
    "keras<3",
]
full = ["quantus[captum,tf-explain,zennit,transformers,torch]"]
```

From `README.md`:
```bash
# Clean installation options
pip install quantus  # Lightweight
pip install "quantus[torch]"  # With PyTorch
pip install "quantus[tensorflow]"  # With TensorFlow
pip install "quantus[full]"  # Everything
```

Analysis:

Positive aspects:
- Comprehensive `pyproject.toml` with pinned versions
- Platform-specific dependencies (Linux vs Mac/Windows for torch)
- Optional dependency groups for modularity
- Clear installation instructions in README

Negative aspects:
- No Docker/containerization provided
- No setup scripts or Makefile for environment creation
- No hardware requirements documentation beyond basic device selection
- Manual tox setup required for development

From `docs/source/getting_started/installation.md`:
```markdown
### Package requirements
python>=3.8.0
torch>=1.11.0
tensorflow>=2.5.0
```

Rating: 2 points - Good dependency specification with optional extras and platform handling, but lacks containerization and automated setup scripts.

---

### S1F5: Security and Access Control (0/3)

Evidence:

Searching the entire codebase reveals no security-related code:

From `quantus/metrics/base.py`:
```python
# No authentication, RBAC, or audit logging
def __call__(self, model, x_batch, y_batch, ...):
    # Direct execution, no access control
    scores = self.evaluate_batch(...)
```

From `quantus/__init__.py`:
```python
# Simple imports, no security layer
from quantus.metrics import *
from quantus.evaluation import evaluate
```

Analysis:
- No credential management: Pure Python library with no API keys or secrets
- No access control: No user/role system exists
- No audit logging: Only basic progress bars and warnings
- No enterprise features: No SSO, LDAP, or compliance features

This is expected for a Python library (not a service), but still represents absence of security features.

Rating: 0 points - No security features implemented. This is a local Python library with no access control mechanisms.

---

### S1F6: Cost Estimation and Budget Planning (0/3)

Evidence:

From `quantus/metrics/base.py`:
```python
def __call__(self, ...):
    # No cost estimation before evaluation
    batch_generator = self.generate_batches(data, batch_size)
    for data_batch in batch_generator:
        result = self.evaluate_batch(data_batch)
```

From tutorials (e.g., `Tutorial_Getting_Started.ipynb`):
```python
# User runs evaluation without cost estimates
scores = metric(
    model=model,
    x_batch=x_batch,  # No token counting
    y_batch=y_batch,
    # No budget limits or cost warnings
)
```

Analysis:
- No cost modeling: Framework doesn't track API costs or compute time
- No resource projection: No estimates before evaluation
- No budgeting tools: Cannot set spending limits
- No optimization suggestions: No cost-saving recommendations

This is expected since:
1. Framework evaluates local models (no API costs)
2. Focused on metric evaluation, not production deployment
3. Users run on their own hardware

Rating: 0 points - No cost estimation features. Framework designed for local research use, not production deployment with cost concerns.

---

## Key Observations

### What Quantus Does Well:
1. Metric Configuration: Rich API for configuring evaluation metrics with hyperparameters
2. Modular Dependencies: Smart optional dependencies via `[torch]`, `[tensorflow]`, `[full]`
3. Clear Documentation: Extensive tutorials and API docs
4. Extensibility: Well-designed base classes for custom metrics

### What Quantus Lacks for Traditional Evaluation:
1. Dataset Abstraction: No logical dataset registration or versioning
2. Declarative Config: Everything done via Python API, no YAML/JSON configs
3. Pipeline Orchestration: No evaluation pipeline configuration
4. Cost Management: No cost estimation or budgeting (not applicable for local use)
5. Access Control: No security features (expected for a library)

### Architectural Mismatch:
Quantus is fundamentally different from traditional evaluation frameworks:
- Quantus Focus: Evaluate explanation methods (Saliency, GradCAM) on pre-trained models
- Traditional Framework: Orchestrate model training/evaluation with dataset management
- Use Case: Research tool for XAI quality assessment vs. production ML pipelines

---

## Total Stage 1 Score: 3/18

Score Breakdown:
- S1F1 (Dataset): 0/3
- S1F2 (Models): 1/3  
- S1F3 (Prompts): 0/3
- S1F4 (Environment): 2/3
- S1F5 (Security): 0/3
- S1F6 (Cost): 0/3

Conclusion: Quantus is a specialized XAI evaluation library, not a general-purpose evaluation framework. It lacks traditional configuration capabilities (datasets, models, pipelines) but excels at its intended purpose: configurable metric-based evaluation of explanation methods. The low score reflects architectural mismatch with the evaluation criteria, not poor quality within its domain.