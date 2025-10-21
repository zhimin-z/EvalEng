## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Label Tensor Storage
- File: `tensorflow_model_analysis/eval_metrics_graph/eval_metrics_graph.py`
- Code Reference: Label map attribute
```python
# OrderedDicts that map features, predictions, and labels keys to their
# tensors.
self._features_map = {}
self._predictions_map = {}
self._labels_map = {}
```
The `_labels_map` attribute stores label tensors that serve as ground truth for evaluation. These labels provide reference values for computing metrics by comparing against model predictions.

Evidence 2: Label Dictionary Retrieval
- File: `tensorflow_model_analysis/eval_metrics_graph/eval_metrics_graph.py`
- Code Reference: `get_features_predictions_labels_dicts()` method
```python
def get_features_predictions_labels_dicts(self):
    """Returns features, predictions, labels dictionaries (or values)."""
    # Returns tuple of (features, predictions, labels)
```
The method returns labels alongside predictions, demonstrating that labels are explicit reference values used throughout the evaluation pipeline for metric computation.

Evidence 3: Binary Classification Ground Truth
- File: `tensorflow_model_analysis/contrib/aggregates/binary_confusion_matrices_test.py`
- Code Reference: Test cases with explicit label values
```python
def testBinaryConfusionMatricesPerRow(self, ...):
    labels = (0, 0, 1, 1)  # Explicit ground truth labels
    predictions = (0, 0.5, 0.3, 0.9)
    # ... computation of confusion matrix based on labels vs predictions
```
Tests use explicit label values to validate confusion matrix computation. These predetermined ground truth labels are compared against predictions to compute true positives, false positives, true negatives, and false negatives.

Evidence 4: Slice Accessor Label Data
- File: `tensorflow_model_analysis/slicer/slice_accessor_test.py`
- Code Reference: Test data structure
```python
# Test data structure includes labels
'labels': make_features_dict({"ad_risk_score": [0]})
```
The test infrastructure includes label data as part of the evaluation data structure. These labels represent ground truth values used for computing metrics across data slices.

Evidence 5: Multi-Class Ground Truth
- File: Frontend tests in `tfma-multi-class-confusion-matrix-at-thresholds_test.js`
- Code Reference: Multi-class confusion matrix data
```javascript
const makeMultiClassData = () => {
  return {
    'matrices': [
      {
        'threshold': 0.2,
        'entries': [
          {'numWeightedExamples': 45},
          {'predictedClassId': 1, 'numWeightedExamples': 5},
          {'actualClassId': 1},  // Explicit actual/ground truth class
          {'actualClassId': 1, 'predictedClassId': 1, 'numWeightedExamples': 55}
        ],
      }
    ]
  };
};
```
Multi-class confusion matrix computation uses explicit `actualClassId` values representing ground truth classes. These are compared against `predictedClassId` to compute confusion matrix entries and classification metrics.

Evidence 6: Accuracy Metric Derivation
- File: Frontend tests in `tfma-accuracy-charts_test.js`
- Code Reference: Test data with derived metrics
```javascript
element.data = [
  {
    'precision': 0.75,
    'recall': 0.125,
    'threshold': Infinity,
    'truePositives': 3,  // Derived from comparing predictions to labels
    'trueNegatives': 4,
    'falsePositives': 2,
    'falseNegatives': 1,
  }
];
```
Test data includes true positives, true negatives, false positives, and false negatives derived from comparing predictions to ground truth labels. These metrics require explicit reference labels for computation of accuracy, precision, and recall.