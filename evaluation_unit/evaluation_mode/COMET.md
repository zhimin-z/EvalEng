## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Correlation Metrics Computation
- File: `comet/models/metrics.py`
- Class/Function: `RegressionMetrics.compute()`
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
    report = {
        self.prefix + "_kendall": kendall,
        self.prefix + "_spearman": spearman,
        self.prefix + "_pearson": pearson,
    }
```
The `RegressionMetrics` class computes statistical correlation metrics (Kendall, Spearman, Pearson) by comparing model predictions against reference scores without executing any generated code. This code performs statistical analysis on model outputs by computing correlation coefficients between predictions and targets. It's purely analytical - comparing numerical scores without executing any model-generated artifacts. This exemplifies Static Analysis through direct examination of model outputs focused on fast, low-infrastructure quality assessment.

Evidence 2: System Accuracy Calculation
- File: `comet/models/metrics.py`
- Function: `system_accuracy()`
- Code Reference:
```python
def system_accuracy(y_hat: List[float], y: List[float], system: List[str]) -> float:
    """Implementation of system-level accuracy proposed in
        [To Ship not to Ship](https://aclanthology.org/2021.wmt-1.57/)
    ...
    """
    try:
        data = pd.DataFrame({"y_hat": y_hat, "y": y, "system": system})
    except ValueError:
        raise Exception(...)
    
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
The `system_accuracy` function analyzes translation quality scores at the system level through pairwise comparisons. This function performs structural analysis on model outputs by grouping scores by system and computing accuracy through pairwise comparisons. It's analyzing the format and relationships of outputs without executing any code. This demonstrates Static Analysis by providing direct examination of output quality through statistical comparison without requiring execution infrastructure.

Evidence 3: Error Span Decoding
- File: `comet/models/multitask/unified_metric.py`
- Function: `decode()`
- Code Reference:
```python
def decode(
    self,
    subword_probs: torch.Tensor,
    input_ids: torch.Tensor,
    mt_offsets: torch.Tensor,
) -> List[Dict]:
    """Decode error spans from subwords.
    ...
    """
    decoded_output = []
    for i in range(len(mt_offsets)):
        seq_len = len(mt_offsets[i])
        error_spans, in_span, span = [], False, {}
        for token_id, probs, token_offset in zip(
            input_ids[i, :seq_len], subword_probs[i][:seq_len], mt_offsets[i]
        ):
            if self.decoding_threshold:
                if torch.sum(probs[1:]) > self.decoding_threshold:
                    probability, label_value = torch.topk(probs[1:], 1)
                    label_value += 1  # offset from removing label 0
                else:
                    probability, label_value = torch.topk(probs[0], 1)
            else:
                probability, label_value = torch.topk(probs, 1)
            
            label = self.label_encoder.ids_to_label.get(label_value)
            # Label set: O I-minor I-major
            # Begin of annotation span
            if label.startswith("I") and not in_span:
                in_span = True
                span["tokens"] = [token_id,]
                span["severity"] = label.split("-")[1]
                span["offset"] = list(token_offset)
                span["confidence"] = [probability,]
```
The `decode` method extracts and structures error annotations from model predictions. This method performs pattern matching and structure validation on model outputs to identify error spans. It parses the probability distributions and token sequences to extract structured annotations without executing any generated content. This illustrates Static Analysis through direct examination of model outputs, parsing their structure for quality assessment without dynamic execution.

Evidence 4: Translation Scoring and JSON Export
- File: `comet/cli/score.py`
- Function: `score_command()`
- Code Reference:
```python
def score_command() -> None:
    # ... setup code ...
    
    outputs = model.predict(
        samples=data,
        batch_size=cfg.batch_size,
        gpus=cfg.gpus,
        progress_bar=(not cfg.quiet),
        accelerator="auto",
        num_workers=cfg.num_workers,
        length_batching=(not cfg.disable_length_batching),
    )
    seg_scores = outputs.scores
    if "metadata" in outputs and "error_spans" in outputs.metadata:
        errors = outputs.metadata.error_spans
    else:
        errors = []
    
    # ... processing code ...
    
    for i in range(len(data[files[0]])):  # loop over (src, ref)
        for j in range(len(files)):  # loop of system
            data[files[j]][i]["COMET"] = seg_scores[j][i]
            if errors and errors[j] and errors[j][i]:
                data[files[j]][i]["errors"] = errors[j][i]
    
    if cfg.to_json != "":
        with open(cfg.to_json, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
```
The `score_command` function evaluates translations and exports results in JSON format. This command scores translations and validates their JSON structure by extracting scores and error metadata. It performs format validation and similarity scoring between outputs and references without executing any generated code. This represents Static Analysis by directly examining and structuring model outputs for quality assessment with minimal infrastructure requirements.

Evidence 5: Statistical Significance Testing
- File: `comet/cli/compare.py`
- Function: `calculate_bootstrap()`
- Code Reference:
```python
def calculate_bootstrap(
    x_sys_scores: np.ndarray, y_sys_scores: np.ndarray, x_name: Path_fr, y_name: Path_fr
) -> Statistical_test_info:
    """Calculate bootstrap score, wins and ties for a system pair."""
    num_splits = x_sys_scores.shape[0]
    delta = x_sys_scores - y_sys_scores
    ties = np.absolute(delta)
    ties = float(len(ties[ties < EPS]))
    x_wins = float(len(delta[delta >= EPS]))
    y_wins = float(len(delta[delta <= -EPS]))
    return {
        "x_name": x_name,
        "y_name": y_name,
        "bootstrap_resampling": {
            "x-mean": float(np.mean(x_sys_scores)),
            "y-mean": float(np.mean(y_sys_scores)),
            "ties (%)": ties / num_splits,
            "x_wins (%)": x_wins / num_splits,
            "y_wins (%)": y_wins / num_splits,
        },
    }
```
The `compare_command` function compares multiple MT systems using statistical tests. This function performs statistical analysis on translation quality scores through bootstrap resampling and paired t-tests. It analyzes the numerical outputs to determine statistical significance without executing any generated artifacts. This demonstrates Static Analysis through direct statistical comparison of outputs, providing fast quality assessment without execution requirements.

Evidence 6: Score Validation Tests
- File: `tests/unit/test_models_predict.py`
- Class/Function: `TestUnifiedMetricPredict.test_predict()`
- Code Reference:
```python
class TestUnifiedMetricPredict(unittest.TestCase):
    def test_predict(self):
        model_output = self.model.predict(TEST_SAMPLES, batch_size=12, gpus=self.gpus)
        assert "error_spans" in model_output.metadata
        assert "src_scores" in model_output.metadata
        assert "ref_scores" in model_output.metadata
        assert "unified_scores" in model_output.metadata
        
        expected_scores = np.array(
            [model_output.metadata.src_scores, model_output.metadata.ref_scores, model_output.metadata.unified_scores]
        ).mean(axis=0)
        
        # Assert for almost equal Arrays or Numbers
        np.testing.assert_almost_equal(expected_scores, np.array(model_output.scores), decimal=5)
        np.testing.assert_almost_equal(model_output.system_score, expected_scores.mean(), 5)
```
The test suite validates model predictions against expected outputs. These tests validate the structure and format of model outputs by checking for required fields and comparing numerical values. They perform static validation of prediction outputs without executing any generated code. This exemplifies Static Analysis by directly examining output structure and quality through assertions, enabling fast validation without dynamic execution infrastructure.