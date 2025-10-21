## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Metric Calculation and Comparison
- File: `evidently/legacy/report.py`
- Test Reference: `tests/report/test_report.py`
- Code Reference:
```python
class MockMetric(Metric[MockMetricResult]):
    def calculate(self, data: InputData) -> MockMetricResult:
        return MockMetricResult(value="a", series=pd.Series([0]), distribution=Distribution(x=[1, 1], y=[0, 0]))
```
The framework primarily calculates metrics by analyzing model outputs (predictions) against reference data without executing generated code. This test example demonstrates how metrics are evaluated through direct computation on input data, representing a core static analysis pattern where outputs are assessed without any execution of model-generated artifacts.

Evidence 2: Data Drift Detection
- File: `tests/calculations/test_data_drift.py`
- Function: `get_one_column_drift()`
- Code Reference:
```python
def test_get_one_column_drift_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    options: DataDriftOptions,
    column_type: ColumnType,
    expected_drift_detected: bool,
):
    result = get_one_column_drift(
        current_data=current_data,
        reference_data=reference_data,
        column_name=column_name,
        options=options,
        dataset_columns=dataset_columns,
        column_type=column_type,
        agg_data=False,
    )
```
The `get_one_column_drift()` function performs statistical analysis on data distributions without executing model code. It compares current versus reference data using statistical tests, analyzing the outputs directly to detect distributional shifts—a quintessential static analysis approach that requires no dynamic execution.

Evidence 3: Classification Performance Metrics
- File: `tests/calculations/test_classification_performance.py`
- Function: `calculate_metrics()`
- Code Reference:
```python
def test_calculate_metrics():
    prediction_probas = np.array([0.91, 0.82, 0.73, 0.64, 0.55, 0.46, 0.37, 0.28, 0.19, 0.0])
    target_values = [1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
    # Statistical analysis of predictions vs targets
    actual_result = calculate_metrics(column_mapping, confusion_matrix, target, prediction)
```
This evidence shows calculation of confusion matrices, accuracy, precision, and recall metrics without executing model code. The framework analyzes prediction probabilities and target values through statistical comparison, demonstrating static evaluation where model outputs are directly assessed against ground truth labels.

Evidence 4: Text Feature Analysis
- File: `tests/features/test_text_length_feature.py`, `tests/features/test_is_valid_json_feature.py`
- Function: `IsValidJSON.generate_feature()`
- Code Reference:
```python
@pytest.mark.parametrize(
    ("item", "expected"),
    [
        ('{"test": "abc"}', True),
        ("not json", False),
    ],
)
def test_is_valid_json_feature(item: str, expected: bool):
    feature_generator = IsValidJSON("column_1")
    result = feature_generator.generate_feature(data=data, ...)
```
The framework validates text properties like length, JSON validity, and SQL validity through parsing rather than execution. This JSON validation example illustrates how the system inspects output format correctness by parsing the structure without running any code, maintaining a purely analytical evaluation approach.

Evidence 5: Statistical Test Implementations
- File: `tests/calculations/stattests/test_get_stattest.py`
- Function: `get_stattest()`
- Code Reference:
```python
@pytest.mark.parametrize(
    "feature_type,stattest_name",
    [
        ("num", "anderson"),
        ("cat", "chisquare"),
        ("num", "ks"),
        ("num", "mannw"),
        # ... many statistical tests
    ],
)
def test_use_stattest_by_name(feature_type: str, stattest_name: str):
    assert get_stattest(pd.Series(), pd.Series(), feature_type, stattest_name)
```
The system applies statistical tests (Anderson-Darling, chi-square, Kolmogorov-Smirnov, Mann-Whitney, etc.) to compare distributions without any execution of generated artifacts. These tests perform only statistical comparison of data series, exemplifying static analysis through mathematical assessment rather than behavioral evaluation.

Evidence 6: Data Quality Metrics
- File: `tests/calculations/test_data_quality.py`
- Functions: `get_rows_count()`, `calculate_column_distribution()`
- Code Reference:
```python
def test_get_rows_count(dataset: pd.DataFrame, expected_rows: int) -> None:
    assert get_rows_count(dataset) == expected_rows

def test_calculate_column_distribution(dataset: pd.DataFrame, column_type: str, expected_distribution: list):
    assert calculate_column_distribution(dataset["test"], column_type=column_type) == expected_distribution
```
The framework analyzes data properties like missing values, distributions, and correlations through inspection-based analysis without execution. These functions examine structural and statistical properties of datasets directly, computing quality metrics through observation rather than dynamic testing.

Evidence 7: Recommendation System Metrics
- File: `tests/metrics/recsys/test_precision_top_k.py`, `tests/metrics/recsys/test_recall_top_k.py`
- Class: `PrecisionTopKMetric`
- Code Reference:
```python
def test_precision_value():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )
    metric = PrecisionTopKMetric(k=2)
    report.run(reference_data=None, current_data=current, ...)
```
The system calculates precision, recall, MRR, and other ranking metrics from predictions by analyzing ranking quality without executing recommendation algorithms. This demonstrates static evaluation of recommendation system outputs through mathematical computation of ranking-based metrics against target labels.