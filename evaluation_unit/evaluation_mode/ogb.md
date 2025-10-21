## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Node property prediction evaluation through direct metric computation
- File: `ogb/nodeproppred/evaluate.py`
- Class/Function: `Evaluator` class with methods `_eval_rocauc()`, `_eval_acc()`
- Code Reference:
```python
def _eval_rocauc(self, y_true, y_pred):
    '''
        compute ROC-AUC and AP score averaged across tasks
    '''
    rocauc_list = []
    for i in range(y_true.shape[1]):
        if np.sum(y_true[:,i] == 1) > 0 and np.sum(y_true[:,i] == 0) > 0:
            is_labeled = y_true[:,i] == y_true[:,i]
            rocauc_list.append(roc_auc_score(y_true[is_labeled,i], y_pred[is_labeled,i]))
    return {'rocauc': sum(rocauc_list)/len(rocauc_list)}
```
The evaluator validates and processes model predictions without executing them (lines 60-95 in `_parse_and_check_input()`). The `eval()` method (lines 97-118) calls metric computation functions. `_eval_rocauc()` (lines 159-175) computes ROC-AUC scores by comparing predicted scores against true labels, while `_eval_acc()` (lines 177-183) calculates accuracy by comparing predicted class labels to true labels. This represents pure static analysis: numerical predictions are validated for format/shape, then compared against ground truth labels through mathematical operations without executing any generated artifacts.

Evidence 2: Link property prediction through ranking and statistical metrics
- File: `ogb/linkproppred/evaluate.py`
- Class/Function: `Evaluator` class with methods `_eval_hits()`, `_eval_mrr()`, `_eval_rocauc()`
- Code Reference:
```python
def _eval_hits(self, y_pred_pos, y_pred_neg, type_info):
    if len(y_pred_neg) < self.K:
        return {'hits@{}'.format(self.K): 1.}
    if type_info == 'torch':
        kth_score_in_negative_edges = torch.topk(y_pred_neg, self.K)[0][-1]
        hitsK = float(torch.sum(y_pred_pos > kth_score_in_negative_edges).cpu()) / len(y_pred_pos)
    else:
        kth_score_in_negative_edges = np.sort(y_pred_neg)[-self.K]
        hitsK = float(np.sum(y_pred_pos > kth_score_in_negative_edges)) / len(y_pred_pos)
    return {'hits@{}'.format(self.K): hitsK}
```
The evaluator validates prediction tensors/arrays (lines 78-153 in `_parse_and_check_input()`). `_eval_hits()` (lines 197-213) computes Hits@K metric by ranking predictions, `_eval_mrr()` (lines 215-244) calculates Mean Reciprocal Rank, and `_eval_rocauc()` (lines 246-260) computes ROC-AUC score. The evaluation analyzes model-generated predictions through ranking operations and statistical comparison without executing code or artifacts, following the pattern of validating inputs, comparing predictions to ground truth, and computing metrics purely through mathematical operations.

Evidence 3: Graph property prediction with diverse metric computation
- File: `ogb/graphproppred/evaluate.py`
- Class/Function: `Evaluator` class with methods `_eval_rocauc()`, `_eval_ap()`, `_eval_rmse()`, `_eval_acc()`, `_eval_F1()`
- Code Reference:
```python
def _eval_F1(self, seq_ref, seq_pred):
    precision_list = []
    recall_list = []
    f1_list = []
    for l, p in zip(seq_ref, seq_pred):
        label = set(l)
        prediction = set(p)
        true_positive = len(label.intersection(prediction))
        false_positive = len(prediction - label)
        false_negative = len(label - prediction)
        # ... computation of precision, recall, F1
    return {'precision': np.average(precision_list),
            'recall': np.average(recall_list),
            'F1': np.average(f1_list)}
```
The evaluator validates prediction formats (lines 49-94 in `_parse_and_check_input()`) and provides multiple metric computation methods: `_eval_rocauc()` (lines 149-165) computes ROC-AUC averaged across tasks, `_eval_ap()` (lines 168-185) computes Average Precision, `_eval_rmse()` (lines 187-196) calculates Root Mean Square Error, `_eval_acc()` (lines 198-205) computes accuracy scores, and `_eval_F1()` (lines 207-241) calculates F1 score using set operations on sequences. This provides standardized static analysis evaluation for graph-level classification and regression tasks, examining numerical outputs through comparison with reference labels and computing performance metrics without dynamic execution, interactive simulation, or custom hybrid evaluation patterns.