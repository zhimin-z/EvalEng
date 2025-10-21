## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: ROC-AUC and accuracy metrics for node property prediction
- File: `ogb/nodeproppred/evaluate.py`
- Classes/Functions: `Evaluator` class with methods `_eval_rocauc()`, `_eval_acc()`
- Code Reference:
```python
def _eval_rocauc(self, y_true, y_pred):
    '''
        compute ROC-AUC and AP score averaged across tasks
    '''
    rocauc_list = []
    for i in range(y_true.shape[1]):
        #AUC is only defined when there is at least one positive data.
        if np.sum(y_true[:,i] == 1) > 0 and np.sum(y_true[:,i] == 0) > 0:
            is_labeled = y_true[:,i] == y_true[:,i]
            rocauc_list.append(roc_auc_score(y_true[is_labeled,i], y_pred[is_labeled,i]))
    return {'rocauc': sum(rocauc_list)/len(rocauc_list)}

def _eval_acc(self, y_true, y_pred):
    acc_list = []
    for i in range(y_true.shape[1]):
        is_labeled = y_true[:,i] == y_true[:,i]
        correct = y_true[is_labeled,i] == y_pred[is_labeled,i]
        acc_list.append(float(np.sum(correct))/len(correct))
    return {'acc': sum(acc_list)/len(acc_list)}
```
This evaluator computes ROC-AUC scores using `sklearn.metrics.roc_auc_score` and accuracy through exact match comparison. These are deterministic, algorithmic metrics for node property prediction tasks.

Evidence 2: Ranking metrics for link prediction
- File: `ogb/linkproppred/evaluate.py`
- Classes/Functions: `Evaluator` class with methods `_eval_hits()`, `_eval_mrr()`, `_eval_rocauc()`
- Code Reference:
```python
def _eval_hits(self, y_pred_pos, y_pred_neg, type_info):
    '''
        compute Hits@K
    '''
    if type_info == 'torch':
        kth_score_in_negative_edges = torch.topk(y_pred_neg, self.K)[0][-1]
        hitsK = float(torch.sum(y_pred_pos > kth_score_in_negative_edges).cpu()) / len(y_pred_pos)
    else:
        kth_score_in_negative_edges = np.sort(y_pred_neg)[-self.K]
        hitsK = float(np.sum(y_pred_pos > kth_score_in_negative_edges)) / len(y_pred_pos)
    return {'hits@{}'.format(self.K): hitsK}

def _eval_mrr(self, y_pred_pos, y_pred_neg, type_info):
    '''
        compute mrr
    '''
    if type_info == 'torch':
        optimistic_rank = (y_pred_neg > y_pred_pos).sum(dim=1)
        pessimistic_rank = (y_pred_neg >= y_pred_pos).sum(dim=1)
        ranking_list = 0.5 * (optimistic_rank + pessimistic_rank) + 1
        mrr_list = 1./ranking_list.to(torch.float)
        return {'mrr_list': mrr_list, ...}
```
This evaluator implements ranking-based metrics (Hits@K, MRR) and ROC-AUC for link prediction. These are mathematical formulas applied to predicted scores, representing algorithmic evaluation.

Evidence 3: Multiple statistical metrics for graph property prediction
- File: `ogb/graphproppred/evaluate.py`
- Classes/Functions: `Evaluator` class with methods `_eval_rocauc()`, `_eval_ap()`, `_eval_rmse()`, `_eval_acc()`, `_eval_F1()`
- Code Reference:
```python
def _eval_rocauc(self, y_true, y_pred):
    '''
        compute ROC-AUC averaged across tasks
    '''
    rocauc_list = []
    for i in range(y_true.shape[1]):
        if np.sum(y_true[:,i] == 1) > 0 and np.sum(y_true[:,i] == 0) > 0:
            is_labeled = y_true[:,i] == y_true[:,i]
            rocauc_list.append(roc_auc_score(y_true[is_labeled,i], y_pred[is_labeled,i]))
    return {'rocauc': sum(rocauc_list)/len(rocauc_list)}

def _eval_rmse(self, y_true, y_pred):
    '''
        compute RMSE score averaged across tasks
    '''
    rmse_list = []
    for i in range(y_true.shape[1]):
        is_labeled = y_true[:,i] == y_true[:,i]
        rmse_list.append(np.sqrt(((y_true[is_labeled,i] - y_pred[is_labeled,i])**2).mean()))
    return {'rmse': sum(rmse_list)/len(rmse_list)}

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
        # ... precision/recall/F1 calculation
    return {'F1': np.average(f1_list)}
```
This evaluator implements multiple algorithmic metrics for graph property prediction including ROC-AUC, Average Precision (from sklearn), RMSE, accuracy, and F1 score. All are deterministic statistical/mathematical functions.

Evidence 4: Knowledge graph embedding score functions
- Files: `examples/lsc/wikikg90m/dgl-ke-ogb-lsc/python/dglke/models/pytorch/score_fun.py`, `examples/lsc/wikikg90m/dgl-ke-ogb-lsc/python/dglke/models/mxnet/score_fun.py`
- Code Reference:
```python
# TransE score function
def edge_func(self, edges):
    head = edges.src['emb']
    tail = edges.dst['emb']
    rel = edges.data['emb']
    score = head + rel - tail
    return {'score': self.gamma - th.norm(score, p=self.dist_ord, dim=-1)}

# DistMult score function
def edge_func(self, edges):
    head = edges.src['emb']
    tail = edges.dst['emb']
    rel = edges.data['emb']
    score = head * rel * tail
    return {'score': th.sum(score, dim=-1)}
```
These are algorithmic scoring functions for knowledge graph embeddings (TransE, DistMult, ComplEx, RotatE, etc.). They compute scores using mathematical formulas (distance metrics, dot products) for evaluating link prediction in knowledge graphs.