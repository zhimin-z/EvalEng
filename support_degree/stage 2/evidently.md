# Evidently - Stage 2 (PREPARE) Evaluation

## Summary
Evidently is an ML/LLM observability and testing framework focused on evaluation and monitoring, not a traditional evaluation harness. It has no data preparation infrastructure - users must bring preprocessed data. The framework provides tools for computing metrics on existing datasets but lacks features for dataset preprocessing, splitting, quality assessment, PII detection, infrastructure building, scenario generation, red-teaming, and contamination detection. It's designed as a post-processing evaluation tool, not a comprehensive data preparation pipeline.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No preprocessing capabilities. Users must provide clean, ready-to-use DataFrames. From `examples/cookbook/metrics.ipynb`: data is already in final form with `pd.DataFrame(reference_data)`. No utilities for tokenization, normalization, or format conversion. The `Dataset.from_pandas()` method only wraps existing data with metadata. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment tools. Framework provides metrics for model output evaluation (drift, performance) but not for assessing dataset label quality, demographics, duplicates, or bias in training data. `metrics.ipynb` shows only model prediction metrics like `Accuracy()`, `Precision()`, not data quality checks. |
| S2F3: PII Detection | 1 | Minimal PII handling for guardrails only. From `examples/cookbook/guardrails.ipynb`: `PIICheck()` exists but is a runtime validator for model outputs, not a preprocessing tool. No anonymization, no audit trails, no batch PII scanning of datasets. Example: `PIICheck().validate("My address is Some city")` - validates individual strings, not datasets. |
| S2F4: Infrastructure Building | 0 | No infrastructure building. No support for FAISS, ColBERT, BM25, Elasticsearch, or database setup. The framework assumes all data and retrieval systems are already built. From repository structure: no modules for index building, only metric calculation on predictions. |
| S2F5: Model Artifact Validation | 0 | No model validation features. Framework doesn't download, validate, or manage models. From examples: users bring their own trained models (e.g., `model.fit(X_train, y_train)` in `regression_preset.ipynb`). No checksum validation, version checks, or integrity verification. |
| S2F6: Scenario Generation | 1 | Very limited synthetic data generation. From `examples/cookbook/datagen.ipynb`: `FewShotDatasetGenerator` and `RagDatasetGenerator` exist for LLM prompt testing but are experimental ("future" module path: `src/evidently/future/`). Basic templating only, no multi-turn dialogues or edge cases. Example: `FewShotDatasetGenerator(kind='twitter posts', count=2)` - simple generation, not evaluation scenarios. |
| S2F7: Red-Teaming | 0 | No red-teaming capabilities. Framework evaluates model outputs but doesn't generate adversarial inputs. From `guardrails.ipynb`: guards validate outputs but don't create attacks. No jailbreak generation, prompt injection tests, or safety boundary probing. |
| S2F8: Contamination Detection | 0 | No contamination detection. Framework compares current vs reference data for drift (e.g., `ValueDrift()` in `metrics.ipynb`) but cannot compare eval data against training corpora for overlap. No n-gram matching, semantic similarity for contamination, or mitigation tools. |

---

## Detailed Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning (0/3)

Evidence of absence:

1. No data loading utilities: From `examples/cookbook/metrics.ipynb`:
```python
reference_data = {
    "Question": ["How can I manage stress effectively?", ...],
    "Answer": ["Manage stress by practicing...", ...],
    "Rating": [5, 4, 0, 1, 0]
}
reference = pd.DataFrame(reference_data)
```
Users manually create DataFrames - no loaders for common formats.

2. No preprocessing pipelines: From `src/evidently/__init__.py` imports, core classes are `Report`, `Dataset`, `DataDefinition` - no preprocessing modules. The `Dataset` class is a wrapper:
```python
# From metrics.ipynb
current_dataset = Dataset.from_pandas(
    pd.DataFrame(current_data),
    data_definition=data_definition
)
```
Just metadata annotation, no transformation.

3. No splitting functionality: Examples show pre-split data:
```python
# From regression_preset.ipynb
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    housing_data.data, housing_data.target, test_size=0.4, random_state=42
)
```
Users must use sklearn or manual splitting.

4. No caching: No evidence of data caching mechanisms in documentation or code structure.

Rating: 0 - Would require building entire preprocessing layer from scratch.

---

### S2F2: Dataset Quality and Bias Assessment (0/3)

Evidence of absence:

From `examples/cookbook/metrics.ipynb`, all quality checks are for model outputs, not datasets:
```python
quality_report = Report([
    MinValue(column="Rating"),          # Column stats, not label quality
    MaxValue(column="Rating"),
    CategoryCount(column="Feedback"),   # Distribution, not bias detection
    UniqueValueCount(column="Feedback"),
    MissingValueCount(column="Feedback")
])
```

These metrics check data completeness, not:
- Label noise/inconsistencies
- Inter-annotator agreement
- Demographic distributions in training data
- Duplicate detection (framework has `DuplicatedRowCount` but it's for monitoring data drift, not cleaning)

From `src/evidently/metrics/__init__.py`, available metrics are for drift and model performance, not dataset quality assessment:
```python
from evidently.metrics import DriftedColumnsCount
from evidently.metrics import ValueDrift
from evidently.metrics import F1Score, Accuracy
```

Rating: 0 - No tools for assessing dataset quality before model training.

---

### S2F3: PII Detection and Anonymization (1/3)

Limited guardrail functionality only:

From `examples/cookbook/guardrails.ipynb`:
```python
from evidently.guardrails import PIICheck

@guard(PIICheck())
def process_with_pii(input: str) -> str:
    return input

process_with_pii("My address is Some city")  # Runtime validation
```

What exists:
- Basic PII detection for individual strings (addresses, SSNs mentioned in guard examples)
- Runtime validation only

What's missing:
- No batch processing of datasets
- No anonymization strategies (redaction, pseudonymization)
- No audit trails or compliance reporting
- Cannot be used for preprocessing datasets

From repository structure, `src/evidently/guardrails/` exists but is focused on inference-time checks, not data preparation.

Rating: 1 - Minimal PII features, not suitable for dataset preprocessing.

---

### S2F4: Task-Specific Infrastructure Building (0/3)

Complete absence:

Repository structure shows no infrastructure modules:
```
src/evidently/
├── metrics/          # Evaluation metrics
├── tests/            # Test conditions
├── ui/               # Visualization
├── presets/          # Metric bundles
└── [no infrastructure/]
```

From `README.md`:
> "An open-source framework to evaluate, test, and monitor ML and LLM-powered systems."

Framework assumes infrastructure exists. From `examples/cookbook/recsys_metrics.ipynb`:
```python
# Users must pre-build recommendation infrastructure
recommendations_df = pd.DataFrame(recommendations)  # Already computed
interactions_df = pd.DataFrame(interactions)        # Already exists
```

No tools for:
- Building FAISS/ColBERT indices
- Database setup
- Multi-agent environments
- Artifact versioning

Rating: 0 - Not in scope for this framework.

---

### S2F5: Model Artifact Validation (0/3)

Evidence from examples:

From `examples/cookbook/regression_preset.ipynb`:
```python
model = linear_model.Ridge(random_state=42)
model.fit(X_train, y_train)
preds_train = model.predict(X_train)
```

Users bring their own models - no validation. Framework only evaluates predictions.

From `README.md`:
> "Works with tabular and text data... Supports evals for predictive and generative tasks"

Focus is on prediction evaluation, not model management. No evidence of:
- Model download utilities
- Checksum validation
- Version compatibility checks
- Configuration validation

Rating: 0 - Framework doesn't interact with model files/artifacts.

---

### S2F6: Evaluation Scenario Generation (1/3)

Limited experimental features:

From `examples/cookbook/datagen.ipynb`:
```python
from evidently.llm.datagen import FewShotDatasetGenerator

twitter_generator = FewShotDatasetGenerator(
    kind='twitter posts',
    count=2,
    user=UserProfile(role="ML engineer", ...),
    examples=["CI/CD is crucial...", ...]
)
twitter_generator.generate()
```

What exists (in `src/evidently/future/`):
- `FewShotDatasetGenerator` for simple text generation
- `RagDatasetGenerator` for question/answer from knowledge base
- Basic prompt templating

What's missing:
- No multi-turn dialogue generation (examples show single-turn only)
- No edge case generation (boundary conditions, adversarial inputs)
- No combinatorial scenario generation
- Limited to LLM text generation, not evaluation scenarios

From module path `src/evidently/future/`, this is experimental, not production-ready.

Rating: 1 - Minimal generation, experimental, not for evaluation scenarios.

---

### S2F7: Red-Teaming and Adversarial Test Generation (0/3)

No red-teaming capabilities:

From `examples/cookbook/guardrails.ipynb`:
```python
from evidently.guardrails import ToxicityCheck, NegativityCheck

@guard([ToxicityCheck(), NegativityCheck()])
def process_with_toxicity_and_negativity(input: str) -> str:
    return input
```

Guards validate outputs but don't generate adversarial inputs.

Framework provides:
- Output validation (toxicity, PII, negativity)
- Custom validators via `PythonFunction`

Framework lacks:
- Jailbreak attempt libraries
- Prompt injection generators
- Bias probing datasets
- Attack taxonomies

From repository structure, no `adversarial/` or `redteam/` modules exist.

Rating: 0 - No red-teaming features.

---

### S2F8: Data Contamination Detection (0/3)

Drift detection only, not contamination:

From `examples/cookbook/metrics.ipynb`:
```python
drift_report = Report([
    DriftedColumnsCount(cat_stattest="psi", num_stattest="wasserstein"),
    ValueDrift(column="Feedback", method="psi", threshold=0.05)
])
drift_snapshot = drift_report.run(current, reference)
```

This compares current vs reference distributions for model monitoring, not:
- Eval data vs training corpus comparison
- N-gram overlap detection
- Semantic similarity for contamination
- Mitigation recommendations

Framework assumes data sources are separate - no tools to verify.

Rating: 0 - Not designed for contamination detection.

---

## Key Observations

### Framework Scope Mismatch
Evidently is an evaluation and monitoring framework, not a data preparation harness. From `README.md`:
> "100+ built-in metrics from data drift detection to LLM judges"

It operates after data preparation:
1. User preprocesses data → 2. User trains model → 3. Evidently evaluates outputs

### What Evidently Does Well (Out of Scope for Stage 2)
From examples and docs:
- Stage 3 (EXECUTE): Comprehensive metrics library (`F1Score`, `Accuracy`, `NDCG`, etc.)
- Stage 6 (MONITOR): Drift detection, A/B testing, UI dashboard
- LLM Evaluation: Text descriptors, semantic similarity, LLM-as-judge

### Architecture Confirms No Preparation Features
From `src/evidently/` structure:
```
evidently/
├── metrics/          # Evaluation metrics (Stage 3)
├── tests/            # Pass/fail conditions (Stage 3)
├── ui/               # Dashboard (Stage 6)
├── presets/          # Metric bundles
├── guardrails/       # Runtime validators (Stage 3)
└── [NO preprocessing, splitting, or infrastructure modules]
```

### Documentation Transparency
Documentation is clear about scope. From tutorials:
- Users must provide `pd.DataFrame` with clean data
- No "data preparation" or "preprocessing" sections in docs
- Examples show sklearn for train/test split

---

## Conclusion

Stage 2 Score: 2/24 (8%)

Evidently is not suitable for Stage 2 (PREPARE) tasks. It's designed as a post-processing evaluation tool that assumes:
- Data is already clean and split
- Infrastructure (indices, databases) is already built  
- Models are already trained
- Evaluation scenarios are manually created

The framework excels at computing metrics on prepared data, not preparing data. Users would need to build an entire data preparation pipeline separately (using pandas, sklearn, custom scripts) before using Evidently.

For evaluation harness purposes, Evidently should be assessed primarily on Stage 3 (EXECUTE) and Stage 6 (MONITOR) capabilities, where it has substantial functionality.