## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Reference Data Usage
- File: `examples/data_drift_grafana_dashboard/evidently_metrics_calculation.py`
- Code Reference: Reference dataset loading
```
reference_data = pd.read_parquet('data/reference.parquet')
# ...
reference_dataset = Dataset.from_pandas(reference_data, data_definition=data_definition)
run = report.run(reference_data=reference_dataset, current_data=current_dataset)
```
Evidently uses reference data as baseline labels for drift detection and performance comparison. The framework loads explicit reference datasets containing ground truth values for evaluating current model outputs.

---

### None

Evidence 1: LLM Text Descriptors
- File: `examples/llm_eval_grafana_dashboard/evidently_metrics_calculation.py`
- Code Reference: Text descriptors without reference
```
from evidently.descriptors import DeclineLLMEval, NegativityLLMEval, SentenceCount, Sentiment

descriptors = [
    NegativityLLMEval("response", alias="Negativity"),
    Sentiment("response", alias="Sentiment"),
    DeclineLLMEval("response", alias="Declines"),
    SentenceCount("response", alias="Sentence count")        
]
```
Computes intrinsic text properties including negativity scores, sentiment analysis, decline detection, and sentence counts without requiring external references. These metrics evaluate output quality through internal characteristics of the generated text.

Evidence 2: Missing Value Counts
- File: `examples/data_drift_grafana_dashboard/evidently_metrics_calculation.py`
- Code Reference: Data quality metrics
```
from evidently.metrics import ValueDrift, DriftedColumnsCount, MissingValueCount

report = Report(metrics = [
    ValueDrift(column='prediction'),
    DriftedColumnsCount(),
    MissingValueCount(column='prediction'),  # Intrinsic data quality metric
])
```
Computes missing value counts as an intrinsic data quality metric. This reference-free evaluation assesses data completeness without comparison to external standards, measuring inherent properties of the output dataset.