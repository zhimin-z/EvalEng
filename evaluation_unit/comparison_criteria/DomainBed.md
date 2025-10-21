## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Dataset Label Structure
- File: `domainbed/datasets.py`
- Code Reference: MultipleDomainDataset and derived classes
```
class ColoredMNIST:
    # Returns TensorDataset(x, y) where
    y = labels.view(-1).long()  # line 238

class RotatedMNIST:
    # Returns TensorDataset(x, y) where
    y = labels.view(-1)  # line 254

class MultipleEnvironmentImageFolder:
    # Uses ImageFolder(path, transform=env_transform)
    # which automatically assigns class labels based on folder structure (line 299)
```
All dataset classes (ColoredMNIST, RotatedMNIST, VLCS, PACS, OfficeHome, TerraIncognita, DomainNet, WILDSCamelyon, WILDSFMoW, and Spawrious) load images paired with corresponding ground truth labels. These labels are explicit, predetermined class assignments that serve as the reference standard for evaluating model predictions on classification tasks across different domains.

Evidence 2: IID Accuracy Selection
- File: `domainbed/model_selection.py`
- Code Reference: IIDAccuracySelectionMethod._step_acc() method
```
def _step_acc(self, records):
    # Extracts validation accuracy (env{i}_out_acc)
    # and test accuracy (env{i}_in_acc) metrics
    # Lines 69-80
```
The IID accuracy selection method compares model predictions against explicit ground truth labels to compute accuracy metrics for each environment. The `env{i}_out_acc` and `env{i}_in_acc` values represent the proportion of predictions that match the predetermined labels, providing a direct measure of model performance against explicit references.

Evidence 3: Oracle Model Selection
- File: `domainbed/model_selection.py`
- Code Reference: OracleSelectionMethod.run_acc() method
```
def run_acc(self):
    # Selects models based on test_out_acc_key and test_in_acc_key
    # Lines 39-50
```
The oracle selection method chooses the best model checkpoint based on test accuracy metrics computed against ground truth labels. The `test_out_acc_key` and `test_in_acc_key` metrics measure how well model predictions match the explicit labels in held-out test environments, using these static references as the selection criterion.

Evidence 4: Ground Truth Results Reference File
- File: `domainbed/misc/test_sweep_results.txt`
- Code Reference: Expected accuracy values for validation
```
# Contains expected accuracy values like:
# "98.0 +/- 0.2", "64.2 +/- 0.8", etc.
# Used by domainbed/test/scripts/test_collect_results.py (lines 75-80)
```
This file stores manually-verified ground truth accuracy values that serve as references for validating the evaluation pipeline's correctness. The accuracy values are derived from comparing model predictions against explicit labels in benchmark datasets like VLCS. The test suite uses these predetermined accuracy values to ensure the results collection process produces outputs matching the expected ground truth performance.