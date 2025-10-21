# Quantus - Stage 2 (PREPARE) Evaluation

## Summary
Quantus is an evaluation framework for XAI (explainable AI) methods, focused on evaluating explanations rather than preparing evaluation data. It assumes users provide pre-trained models, data, and explanations. The framework has minimal data preparation capabilities and no infrastructure for building evaluation artifacts.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing - only shape normalization and channel ordering (`quantus/metrics/base.py:390-392`). No data loading, caching, splitting, or versioning capabilities. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment tools. Framework evaluates explanations, not data quality or bias detection. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features present in codebase. |
| S2F4: Infrastructure Building | 0 | No infrastructure building utilities. Framework expects pre-trained models and pre-computed data/explanations. |
| S2F5: Model Validation | 0 | No model artifact validation. Users must provide valid models; framework only wraps them (`quantus/helpers/utils.py` contains `get_wrapped_model` but no validation). |
| S2F6: Scenario Generation | 0 | No scenario generation capabilities. Framework evaluates existing explanations, not generates evaluation scenarios. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial test generation features. |
| S2F8: Contamination Detection | 0 | No data contamination detection capabilities. |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (1 point)

Evidence of minimal preprocessing:

From `quantus/metrics/base.py:390-392`:
```python
# Reshape input batch to channel first order:
if not isinstance(channel_first, bool):  # None is not a boolean instance.
    channel_first = utils.infer_channel_first(x_batch)
x_batch = utils.make_channel_first(x_batch, channel_first)
```

From `quantus/helpers/utils.py`, the preprocessing is limited to:
- Channel ordering normalization
- Shape inference
- Attribution expansion

What's missing:
- No data loading from configs
- No caching mechanisms
- No data splitting functionality
- No preprocessing pipelines for text/images/audio
- No validation of data quality

Tutorial evidence (`tutorials/Tutorial_Getting_Started.ipynb`):
Users must load and preprocess data themselves:
```python
# Load datasets and make loaders.
test_set = torchvision.datasets.MNIST(root='./sample_data', download=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=24)
x_batch, y_batch = next(iter(test_loader))
```

### S2F2: Dataset Quality and Bias Assessment (0 points)

Evidence of absence:
- No quality assessment metrics in `quantus/metrics/` directory
- Framework focuses exclusively on explanation evaluation (6 categories: faithfulness, robustness, localisation, complexity, randomisation, axiomatic)
- Documentation (`README.md:75-135`) lists only XAI evaluation metrics, no data quality tools

### S2F3: PII Detection and Anonymization (0 points)

Evidence of absence:
- Searched codebase for PII-related functionality - none found
- No privacy-related modules in `quantus/helpers/` or `quantus/functions/`
- No mention of PII in documentation or tutorials

### S2F4: Task-Specific Infrastructure Building (0 points)

Evidence of absence:
- No retrieval systems (FAISS, BM25, etc.)
- No database setup utilities
- No specialized environment builders
- Framework expects ready-to-use models

From `tutorials/Tutorial_Getting_Started.ipynb`:
```python
# Load a pre-trained LeNet classification model (architecture at quantus/helpers/models).
model = LeNet()
model.load_state_dict(torch.load("tests/assets/mnist_model"))
```

Users must handle all infrastructure themselves.

### S2F5: Model Artifact Validation (0 points)

Evidence of minimal validation:

From `quantus/helpers/utils.py` (model wrapping only):
```python
def get_wrapped_model(
    model: Union[keras.Model, nn.Module, ModelInterface],
    channel_first: bool,
    softmax: bool,
    device: Optional[str],
    model_predict_kwargs: Optional[Dict[str, Any]],
) -> ModelInterface:
```

This only wraps models for API consistency, performs no:
- Checksum validation
- Version compatibility checks
- Configuration validation
- Corruption detection

### S2F6: Evaluation Scenario Generation (0 points)

Evidence of absence:
- No prompt variation or scenario generation
- Framework evaluates existing explanations
- Users provide static test cases

From `quantus/metrics/base.py:144-190`, the `__call__` method expects pre-provided data:
```python
def __call__(
    self,
    model: Union[keras.Model, nn.Module, None],
    x_batch: np.ndarray,
    y_batch: np.ndarray,
    a_batch: Optional[np.ndarray],  # Pre-computed explanations
    ...
)
```

### S2F7: Red-Teaming and Adversarial Test Generation (0 points)

Evidence of absence:
- No adversarial generation in codebase
- Robustness metrics evaluate sensitivity to perturbations but don't generate adversarial examples
- From `quantus/metrics/robustness/`, metrics measure robustness but don't create attacks

### S2F8: Data Contamination Detection (0 points)

Evidence of absence:
- No contamination detection functionality
- No training corpus comparison tools
- Framework is evaluation-focused, not data-centric

## Key Observations

### Framework Purpose
Quantus is designed for evaluating explanations, not preparing evaluation data. From `README.md:15`:
```markdown
A toolkit to evaluate neural network explanations
```

### User Responsibilities
Users must provide:
1. Pre-trained models
2. Preprocessed datasets
3. Pre-computed or generate-on-demand explanations

From `docs/source/getting_started/getting_started_example.md:30-54`:
```python
# Load a pre-trained LeNet classification model (architecture at quantus/helpers/models).
model = LeNet()
model.load_state_dict(torch.load("tests/assets/mnist_model"))

# Load datasets and make loaders.
test_set = torchvision.datasets.MNIST(root='./sample_data', download=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=24)
```

### What Quantus Does Well
- Explanation evaluation: 30+ metrics across 6 categories
- Framework flexibility: Supports PyTorch, TensorFlow
- Integration: Works with Captum, tf-explain, Zennit

From `quantus/__init__.py:11-17`:
```python
# Expose quantus.evaluate to the user.
from quantus.evaluation import evaluate

# Expose quantus.explain to the user.
from quantus.functions.explanation_func import explain
```

### Architecture Gap
The framework focuses on Stage 3 (EXECUTE) and beyond, assuming Stage 2 (PREPARE) is handled externally. From `quantus/metrics/base.py`, the core flow is:
1. Accept pre-prepared data
2. Apply minimal normalization
3. Evaluate explanations
4. Aggregate results

## Conclusion

Quantus scores 1/24 points in Stage 2 (PREPARE) because:
- It's not designed for data preparation
- It assumes users handle data loading, preprocessing, splitting, and quality assurance
- The only preparation functionality is minimal shape/channel normalization for API consistency
- All infrastructure, validation, and scenario generation are user responsibilities

This low score doesn't reflect poor quality—rather, it indicates Quantus operates at a different stage of the evaluation pipeline, focusing on explanation evaluation rather than evaluation preparation.