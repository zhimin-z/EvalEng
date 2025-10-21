## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Metrics Comparison and Validation
- File: `tensorflow_model_analysis/eval_metrics_graph/eval_metrics_graph.py`
- Functions: `get_metric_values()`, `metrics_reset_update_get()`, `metrics_reset_update_get_list()`
- Code Reference:
```python
def get_metric_values(self) -> Dict[str, Any]:
    """Retrieve metric values."""
    with self._lock:
        return self._get_metric_values()

def _get_metric_values(self) -> Dict[str, Any]:
    # Lock should be acquired before calling this function.
    metric_values = self._session.run(fetches=self._metric_value_ops)
    return dict(zip(self._metric_names, metric_values))
```
The evaluation harness performs static analysis of model-generated metrics by computing metric values, comparing them against expected values, and validating their format without executing any model-generated code. The `get_metric_values()` method extracts computed metric values from TensorFlow operations, while `metrics_reset_update_get()` processes features, predictions, and labels to update and retrieve metric variables. These operations analyze the structure and values of model outputs through inspection and mathematical computation.

Evidence 2: Slice Key Validation and Pattern Matching
- File: `tensorflow_model_analysis/slicer/slicer_lib.py` (referenced in tests)
- Functions: `get_slices_for_features_dicts()`, `is_slice_applicable()`, `slice_key_matches_slice_specs()`
- Test File: `tensorflow_model_analysis/slicer/slicer_test.py`
- Code Reference:
```python
# From slicer_test.py
def testIsSliceApplicable(self):
    test_cases = [
        (
            "applicable",
            ["column1"],
            [("column3", "value3"), ("column4", "value4")],
            (("column1", "value1"), ("column3", "value3"), ("column4", "value4")),
            True,
        ),
        # ... more test cases validating slice applicability
    ]
```
The slicer component performs static analysis by validating slice keys against specifications, matching patterns in feature dictionaries, and checking if slices meet specified criteria. Tests show validation of slice keys like `(("gender", "f"),)` and pattern matching for features without executing any generated artifacts.

Evidence 3: Binary Confusion Matrix Analysis
- File: `tensorflow_model_analysis/contrib/aggregates/binary_confusion_matrices_test.py`
- Functions: `BinaryConfusionMatrices.add_input()`, confusion matrix computation
- Code Reference:
```python
def testBinaryConfusionMatricesPerRow(
    self,
    thresholds,
    example_ids_count,
    example_weights,
    example_ids,
    expected_result,
):
    labels = (0, 0, 1, 1)
    predictions = (0, 0.5, 0.3, 0.9)

    confusion_matrix = binary_confusion_matrices.BinaryConfusionMatrices(
        thresholds=thresholds,
        example_ids_count=example_ids_count,
    )
    accumulator = confusion_matrix.create_accumulator()
    for label, prediction, example_weight, example_id in zip(
        labels, predictions, example_weights, example_ids
    ):
        accumulator = confusion_matrix.add_input(
            accumulator=accumulator,
            labels=[label],
            predictions=[prediction],
            example_weights=[example_weight] if example_weight else None,
            example_id=example_id,
        )
    self.assertDictEqual(accumulator, expected_result)
```
The confusion matrices are computed by analyzing predictions against labels through statistical aggregation. The test shows analysis of thresholds, true/false positives/negatives without executing model-generated code, only analyzing the model's output values.

Evidence 4: Frontend Visualization Data Processing
- Files: `tensorflow_model_analysis/frontend/tfma-metrics-histogram/tfma-metrics-histogram.js`, `tensorflow_model_analysis/frontend/lib/cell-renderer_test.js`
- Functions: `prepareHistogram_()`, `renderValue()`, `extractFloatValue()`
- Code Reference:
```javascript
// From tfma-metrics-histogram.js
prepareHistogram_(data, numBuckets, rangeMin, rangeMax) {
    const dataSeriesList = data.getSeriesList();
    const metricRange = data.getColumnRange(this.metric);

    // Add the data column labels to the first row of dataTableArray.
    const header = [this.metric, XLabel.UNWEIGHTED, XLabel.WEIGHTED];
    const dataTableArray = [header];

    if (numBuckets <= 0 || rangeMin > rangeMax || metricRange.min > rangeMax ||
        metricRange.max < rangeMin || !dataSeriesList.length) {
      // Histogram range is empty - Return empty flag.
      return {
        dataTableArray: [header],
        hAxisTicks: [],
        highlightedBuckets: [],
        isEmpty: true
      };
    }
    // ... continues with static analysis of metric data
}
```
The frontend components perform static analysis of metric data to prepare visualizations. The `prepareHistogram_()` function analyzes metric distributions without execution, and `renderValue()` validates and formats metric values for display through inspection and pattern matching.

Evidence 5: Metrics Validation and Format Checking
- File: `tensorflow_model_analysis/frontend/lib/cell-renderer_test.js`
- Functions: `testRenderValueWithBoundedValue()`, `testRenderValueWithMultiClassConfusionMatrix()`
- Code Reference:
```javascript
testRenderValueWithBoundedValue: function() {
    const value = 1;
    const boundedValue = makeBoundedValueObject(value, 2, 3);
    const cell = CellRenderer.renderValue(boundedValue);
    assertEquals(value, cell.v);
    assertEquals(
        '<tfma-bounded-value value=1 lower-bound=2 upper-bound=3>' +
            '</tfma-bounded-value>',
        cell.f);
},
```
Tests demonstrate validation of metric value formats including bounded values, confusion matrices, and array values. The renderer checks structure and format of metric outputs through inspection without executing any generated code.