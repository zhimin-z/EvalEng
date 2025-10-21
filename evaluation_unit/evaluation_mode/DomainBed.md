## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Results Comparison and Reporting
- File: `domainbed/lib/reporting.py`
- Function: `load_records()`
- Code Reference:
```python
def load_records(path):
    records = []
    for i, subdir in tqdm.tqdm(list(enumerate(os.listdir(path))):
        results_path = os.path.join(path, subdir, "results.jsonl")
        try:
            with open(results_path, "r") as f:
                for line in f:
                    records.append(json.loads(line[:-1]))
```
This function loads and parses evaluation results from JSON files without executing any model-generated artifacts. It reads pre-computed metrics (accuracy values) and organizes them for analysis, demonstrating pure static inspection of previously recorded outputs.

Evidence 2: Model Selection Through Metric Inspection
- File: `domainbed/model_selection.py`
- Class: `SelectionMethod` classes (`OracleSelectionMethod`, `IIDAccuracySelectionMethod`, `LeaveOneOutSelectionMethod`)
- Code Reference:
```python
class OracleSelectionMethod(SelectionMethod):
    @classmethod
    def run_acc(self, run_records):
        run_records = run_records.filter(lambda r:
            len(r['args']['test_envs']) == 1)
        test_env = run_records[0]['args']['test_envs'][0]
        test_out_acc_key = 'env{}_out_acc'.format(test_env)
        test_in_acc_key = 'env{}_in_acc'.format(test_env)
        chosen_record = run_records.sorted(lambda r: r['step'])[-1]
        return {
            'val_acc':  chosen_record[test_out_acc_key],
            'test_acc': chosen_record[test_in_acc_key]
        }
```
These classes analyze pre-computed accuracy metrics from model outputs to select the best hyperparameters. They inspect recorded validation and test accuracies without executing any code or running model inference, relying solely on static comparison of numerical values.

Evidence 3: Results Collection and Aggregation
- File: `domainbed/scripts/collect_results.py` (referenced in test files)
- File: `domainbed/test/scripts/test_collect_results.py`
- Function: `test_format_mean()`, `test_print_table_non_latex()`, `test_print_table_latex()`
- Code Reference:
```python
def test_format_mean(self):
    self.assertEqual(
        collect_results.format_mean([0.1, 0.2, 0.3], False)[2],
        '20.0 +/- 4.7')
```
These functions format and display evaluation metrics from completed training runs. They perform statistical analysis (mean, standard deviation) on accuracy values and generate formatted tables without executing any model artifacts, focusing purely on post-hoc analysis of stored results.

Evidence 4: Metric Comparison and Validation
- File: `domainbed/misc/test_sweep_results.txt`
- Code Reference:
```txt
-------- Dataset: VLCS, model selection method: training-domain validation set
Algorithm             C                     L                     S                     V                     Avg                  
ERM                   98.0 +/- 0.2          64.2 +/- 0.8          74.1 +/- 0.4          77.1 +/- 0.2          78.3
```
This file contains ground-truth results showing accuracy comparisons across different datasets and algorithms. The evaluation harness compares model outputs (accuracy values) against expected patterns without executing the models themselves, validating the correctness of static analysis procedures.

Evidence 5: Query-Based Result Filtering
- File: `domainbed/lib/query.py` (referenced in multiple files)
- File: `domainbed/test/lib/test_query.py`
- Function: Query operations for filtering and aggregating results
- Code Reference:
```python
def test_everything(self):
    people = Q([
        {'name': 'Bob', 'age': 40},
        {'name': 'Alice', 'age': 20},
        {'name': 'Bob', 'age': 10}
    ])
    self.assertEqual(people.select('name'), ['Bob', 'Alice', 'Bob'])
    self.assertEqual(people.argmax('age'), people[0])
```
The query system provides methods to filter, group, and analyze evaluation records based on their properties (accuracy, hyperparameters, etc.) through inspection rather than execution. This enables sophisticated analysis patterns while maintaining the static nature of the evaluation process.