## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Node Property Prediction Ground Truth
- File: `ogb/nodeproppred/evaluate.py`
- Code Reference: `_parse_and_check_input()` and `eval()` methods in `Evaluator` class
```python
def _parse_and_check_input(self, input_dict):
    if self.eval_metric == 'rocauc' or self.eval_metric == 'acc':
        if not 'y_true' in input_dict:
            raise RuntimeError('Missing key of y_true')
        if not 'y_pred' in input_dict:
            raise RuntimeError('Missing key of y_pred')

        y_true, y_pred = input_dict['y_true'], input_dict['y_pred']
```
```python
def _eval_acc(self, y_true, y_pred):
    acc_list = []
    for i in range(y_true.shape[1]):
        is_labeled = y_true[:,i] == y_true[:,i]
        correct = y_true[is_labeled,i] == y_pred[is_labeled,i]
        acc_list.append(float(np.sum(correct))/len(correct))
    return {'acc': sum(acc_list)/len(acc_list)}
```
The evaluator explicitly requires ground truth labels (`y_true`) to compare against model predictions (`y_pred`). Ground truth labels are loaded from preprocessed files and used for direct accuracy computation through comparison with predictions.

Evidence 2: Link Property Prediction Labels
- File: `ogb/linkproppred/evaluate.py`
- Code Reference: `_parse_and_check_input()` method
```python
def _parse_and_check_input(self, input_dict):
    if 'hits@' in self.eval_metric or 'rocauc' == self.eval_metric:
        if not 'y_pred_pos' in input_dict:
            raise RuntimeError('Missing key of y_pred_pos')
        if not 'y_pred_neg' in input_dict:
            raise RuntimeError('Missing key of y_pred_neg')

        y_pred_pos, y_pred_neg = input_dict['y_pred_pos'], input_dict['y_pred_neg']
```
```python
def _eval_rocauc(self, y_pred_pos, y_pred_neg, type_info):
    if type_info == 'torch':
        y_pred_pos_numpy = y_pred_pos.cpu().numpy()
        y_pred_neg_numpy = y_pred_neg.cpu().numpy()
    else:
        y_pred_pos_numpy = y_pred_pos
        y_pred_neg_numpy = y_pred_neg
    
    y_true = np.concatenate([np.ones(len(y_pred_pos_numpy)), np.zeros(len(y_pred_neg_numpy))]).astype(np.int32)
    y_pred = np.concatenate([y_pred_pos_numpy, y_pred_neg_numpy])

    rocauc = roc_auc_score(y_true, y_pred)
    return {'rocauc': rocauc}
```
Uses explicit ground truth labels distinguishing positive edges (actual links) from negative edges (non-links). These predetermined labels enable ROC-AUC computation through direct comparison of predictions against binary ground truth.

Evidence 3: Graph Property Prediction Ground Truth
- File: `ogb/graphproppred/evaluate.py`
- Code Reference: `_parse_and_check_input()` and evaluation methods
```python
def _parse_and_check_input(self, input_dict):
    if self.eval_metric == 'rocauc' or self.eval_metric == 'ap' or self.eval_metric == 'rmse' or self.eval_metric == 'acc':
        if not 'y_true' in input_dict:
            raise RuntimeError('Missing key of y_true')
        if not 'y_pred' in input_dict:
            raise RuntimeError('Missing key of y_pred')

        y_true, y_pred = input_dict['y_true'], input_dict['y_pred']
```
```python
elif self.eval_metric == 'F1':
    if not 'seq_ref' in input_dict:
        raise RuntimeError('Missing key of seq_ref')
    if not 'seq_pred' in input_dict:
        raise RuntimeError('Missing key of seq_pred')

    seq_ref, seq_pred = input_dict['seq_ref'], input_dict['seq_pred']
```
Graph-level evaluator requires explicit ground truth labels for each graph. For sequence-based tasks like code generation, it uses reference sequences (`seq_ref`) as predetermined correct answers for comparison.

Evidence 4: Dataset Label Loading
- File: `ogb/nodeproppred/dataset.py`
- Code Reference: `pre_process()` method
```python
if self.binary:
    self.graph = read_binary_graph_raw(raw_dir, add_inverse_edge = add_inverse_edge)[0]
    self.labels = np.load(osp.join(raw_dir, 'node-label.npz'))['node_label']
else:    
    self.graph = read_csv_graph_raw(raw_dir, add_inverse_edge = add_inverse_edge, additional_node_files = additional_node_files, additional_edge_files = additional_edge_files)[0]
    self.labels = pd.read_csv(osp.join(raw_dir, 'node-label.csv.gz'), compression='gzip', header = None).values
```
Dataset classes load ground truth labels from CSV or NPZ files. These static labels are stored in preprocessed files and serve as reference standards for all benchmark evaluations.

Evidence 5: Predefined Split Indices
- File: `ogb/nodeproppred/dataset.py`
- Code Reference: `get_idx_split()` method
```python
def get_idx_split(self, split_type = None):
    if split_type is None:
        split_type = self.meta_info['split']

    path = osp.join(self.root, 'split', split_type)

    train_idx = pd.read_csv(osp.join(path, 'train.csv.gz'), compression='gzip', header = None).values.T[0]
    valid_idx = pd.read_csv(osp.join(path, 'valid.csv.gz'), compression='gzip', header = None).values.T[0]
    test_idx = pd.read_csv(osp.join(path, 'test.csv.gz'), compression='gzip', header = None).values.T[0]

    return {'train': train_idx, 'valid': valid_idx, 'test': test_idx}
```
Provides predefined train/valid/test splits with corresponding ground truth labels. These fixed splits ensure consistent evaluation across different models using the same reference labels.

Evidence 6: Test Submission Format
- File: `examples/lsc/pcqm4m/test_inference_gnn.py`
- Code Reference: Test prediction saving (Lines 123-126)
```python
print('Predicting on test data...')
y_pred = test(model, device, test_loader)
print('Saving test submission file...')
evaluator.save_test_submission({'y_pred': y_pred}, args.save_test_dir, mode = 'test-whole')
```
The evaluator's `save_test_submission()` method expects predictions that will be compared against held-out ground truth labels. This demonstrates the evaluation framework's reliance on predetermined reference answers for assessment.