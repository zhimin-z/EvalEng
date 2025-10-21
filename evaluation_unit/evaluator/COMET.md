## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Statistical correlation metrics
- File: `comet/models/metrics.py`
- Functions/Classes: `RegressionMetrics.compute()`, `WMTKendall.compute()`, `system_accuracy()`
- Code Reference:
```python
def compute(self) -> torch.Tensor:
    """Computes spearmans correlation coefficient."""
    try:
        preds = torch.cat(self.preds, dim=0)
        target = torch.cat(self.target, dim=0)
    except TypeError:
        preds = self.preds
        target = self.target
    kendall, _ = stats.kendalltau(preds.tolist(), target.tolist())
    spearman, _ = stats.spearmanr(preds.tolist(), target.tolist())
    pearson, _ = stats.pearsonr(preds.tolist(), target.tolist())
```
This code implements standard statistical correlation metrics (Kendall's tau, Spearman's rho, Pearson's r) which are algorithmic evaluators. These are deterministic mathematical functions that compute correlation between predicted and target scores using predefined statistical formulas to assess the quality of MT evaluation models. The metrics operate through fixed algorithmic procedures without learned parameters, making them purely algorithmic rather than ML-based evaluators.

Evidence 2: System accuracy metric
- File: `comet/models/metrics.py`
- Function: `system_accuracy()`
- Code Reference:
```python
def system_accuracy(y_hat: List[float], y: List[float], system: List[str]) -> float:
    """Implementation of system-level accuracy proposed in
        [To Ship not to Ship](https://aclanthology.org/2021.wmt-1.57/)
    """
    data = pd.DataFrame({"y_hat": y_hat, "y": y, "system": system})
    data = data.groupby("system").mean()
    pairs = list(combinations(data.index.tolist(), 2))
    
    tp = 0
    for system_a, system_b in pairs:
        human_delta = data.loc[system_a]["y"] - data.loc[system_b]["y"]
        model_delta = data.loc[system_a]["y_hat"] - data.loc[system_b]["y_hat"]
        if (human_delta >= 0) ^ (model_delta < 0):
            tp += 1
    
    accuracy = tp / len(pairs) if len(pairs) != 0 else 0
    return float(accuracy)
```
This implements a system-level accuracy metric using pairwise comparisons through rule-based algorithmic evaluation. It compares system rankings to determine accuracy through deterministic logic (comparing deltas and counting true positives) using only mathematical operations and conditional logic. The evaluation is entirely algorithmic with no learned components, relying solely on predefined rules for comparing human and model judgments.

Evidence 3: Matthews Correlation Coefficient
- File: `comet/models/metrics.py`
- Class: `MCCMetric`
- Code Reference:
```python
class MCCMetric(MulticlassMatthewsCorrCoef):
    def __init__(self, prefix: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.prefix = prefix

    def compute(self) -> torch.Tensor:
        """Computes matthews correlation coefficient."""
        mcc = super(MCCMetric, self).compute()
        return {self.prefix + "_mcc": mcc}
```
MCC (Matthews Correlation Coefficient) is a standard statistical metric for classification quality assessment. This is an algorithmic evaluator that uses a fixed mathematical formula to compute correlation coefficients, providing a deterministic measure of classification performance without any learned parameters or training data dependencies.

Evidence 4: Bootstrap resampling and statistical testing
- File: `comet/cli/compare.py`
- Functions: `bootstrap_resampling()`, `calculate_bootstrap()`, `pairwise_bootstrap()`
- Code Reference:
```python
def bootstrap_resampling(
    seg_scores: np.ndarray, sample_size: int, num_splits: int
) -> np.array:
    """Computes Bootstrap Resampling."""
    population_size = seg_scores.shape[1]
    subsample_ids = np.random.choice(
        population_size, size=(sample_size, num_splits), replace=True
    )
    subsamples = np.take(seg_scores, subsample_ids, axis=1)
    sys_scores = np.mean(subsamples, axis=1)
    return sys_scores
```
This implements bootstrap resampling for statistical significance testing, which is a classical algorithmic evaluation method. It uses established statistical procedures (resampling with replacement, t-tests, confidence interval computation) to compare MT systems through purely algorithmic means. The approach relies on statistical theory and deterministic sampling procedures rather than learned model parameters, making it a traditional algorithmic evaluator.

---

### ML-based

Evidence 1: Core COMET models using pretrained encoders
- Files: `comet/models/regression/regression_metric.py`, `comet/models/ranking/ranking_metric.py`, `comet/models/multitask/unified_metric.py`, `comet/models/multitask/xcomet_metric.py`
- Class: `RegressionMetric`
- Code Reference:
```python
class RegressionMetric(CometModel):
    """RegressionMetric:
    ...
    pretrained_model (str): Pretrained model from Hugging Face. Defaults to
        'xlm-roberta-large'.
    ...
    """
    def forward(
        self,
        src_input_ids: torch.tensor,
        src_attention_mask: torch.tensor,
        mt_input_ids: torch.tensor,
        mt_attention_mask: torch.tensor,
        ref_input_ids: torch.tensor,
        ref_attention_mask: torch.tensor,
        **kwargs
    ) -> Prediction:
        """Regression model forward method."""
        src_sentemb = self.get_sentence_embedding(src_input_ids, src_attention_mask)
        ref_sentemb = self.get_sentence_embedding(ref_input_ids, ref_attention_mask)
        mt_sentemb = self.get_sentence_embedding(mt_input_ids, mt_attention_mask)
        return self.estimate(src_sentemb, mt_sentemb, ref_sentemb)
```
These classes implement neural network models (XLM-RoBERTa, BERT-based architectures) that serve as learned evaluators for machine translation quality. They use pretrained language models with millions of learned parameters and neural network architectures to generate sentence embeddings and quality scores. The evaluation process involves forward passes through deep neural networks with learned representations, making them fundamentally ML-based evaluators that leverage patterns learned from training data rather than fixed algorithmic rules.

Evidence 2: Model loading and usage in CLI
- File: `comet/cli/score.py`
- Code Reference:
```python
def score_command() -> None:
    # ...
    if cfg.model.endswith(".ckpt") and os.path.exists(cfg.model):
        model_path = cfg.model
    else:
        model_path = download_model(cfg.model, saving_directory=cfg.model_storage_path)

    model = load_from_checkpoint(model_path)
    model.eval()
    model.half()
```
This code loads pretrained COMET models (neural networks) from checkpoints and uses them for evaluation in inference mode. The models are ML-based evaluators that predict quality scores through neural network inference using learned weights stored in checkpoint files. The `.half()` call indicates optimization for neural network inference, and the entire evaluation pipeline depends on learned model parameters rather than algorithmic computation.