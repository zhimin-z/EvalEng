# Unbabel/COMET - Stage 4 (EVALUATE) Evaluation

## Summary
COMET is a specialized neural MT evaluation framework that focuses on computing quality scores using learned metrics. It has limited traditional metric computation capabilities and no built-in output validation or statistical comparison tools. The framework excels at training custom neural evaluators but lacks the comprehensive evaluation infrastructure expected from a general-purpose evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation features - framework assumes well-formed inputs |
| S4F2: Metric Computation | 1 | Single neural metric type (score 0-1), no traditional metrics library |
| S4F3: Evaluator Models | 3 | Excellent LLM-as-judge capabilities with multiple pre-trained models |
| S4F4: Multi-Modal Scoring | 0 | Text-only, no multi-modal support |
| S4F5: Aggregate Statistics | 1 | Basic mean/median only, no significance testing built-in |

---

## Detailed Feature Analysis

### S4F1: Output Validation and Normalization (0 pts)

Evidence: The framework has no output validation or normalization features. 

From `comet/models/base.py` (predict_step):
```python
def predict_step(
    self,
    batch: Dict[str, torch.Tensor],
    batch_idx: Optional[int] = None,
    dataloader_idx: Optional[int] = None,
) -> torch.Tensor:
    """Pytorch Lightning predict step."""
    model_outputs = Prediction(scores=self(batch).score)
    # No validation of outputs, just returns raw scores
    return model_outputs
```

From `comet/cli/score.py`:
```python
with open(cfg.sources(), encoding="utf-8") as fp:
    sources = [line.strip() for line in fp.readlines()]
# Simple strip(), no format validation or sanity checks
```

Missing capabilities:
1. No format validation (JSON, XML checking)
2. No schema validation
3. No policy compliance checks (toxicity, length constraints)
4. No sanity checks (duplicate detection, anomaly detection)
5. No normalization beyond basic `.strip()`

The framework expects clean text inputs and provides no tools for validating or normalizing model outputs.

### S4F2: Task-Specific Metric Computation (1 pt)

Evidence: COMET provides only neural evaluation metrics - no traditional metric library.

From `comet/models/base.py`:
```python
def predict(
    self,
    samples: List[Dict[str, str]],
    # ...
) -> Prediction:
    """Returns segment-level scores, system level score"""
    # Only returns neural model scores
    scores = torch.cat([pred["scores"] for pred in predictions], dim=0).tolist()
    output = Prediction(scores=scores, system_score=sum(scores) / len(scores))
    return output
```

From `README.md`:
```md
The model outputs scores ranging from 0 to 1, where 1 signifies a perfect translation.
```

Limitations:
1. No traditional metrics: No BLEU, ROUGE, METEOR, BERTScore, F1, etc.
2. Single metric type: Only provides neural quality scores (0-1 range)
3. No per-sample breakdown: Returns single score per sample, no multi-aspect scoring
4. Not extensible: Cannot easily add custom metrics beyond neural models

The framework is focused solely on neural evaluation metrics. While excellent for this purpose, it lacks a metric library for traditional NLP evaluation.

Partial credit (1 pt): Can compute per-sample scores and supports custom neural evaluators through training.

### S4F3: Evaluator Model Integration (3 pts)

Evidence: This is COMET's core strength - excellent evaluator model support.

From `MODELS.md` showing available evaluators:
```md
| Model | Description |
| Unbabel/wmt22-comet-da | Reference-based regression (XLM-R) |
| Unbabel/wmt22-cometkiwi-da | Reference-free (InfoXLM) |
| Unbabel/wmt23-cometkiwi-da-xl | 3.5B parameter QE model |
| Unbabel/wmt23-cometkiwi-da-xxl | 10.7B parameter QE model |
| Unbabel/XCOMET-XXL | Explainable with error spans |
```

From `comet/models/base.py` showing MC Dropout for uncertainty:
```python
def set_mc_dropout(self, value: int):
    """Sets Monte Carlo Dropout runs per sample."""
    self.mc_dropout = value

def predict_step(self, batch, batch_idx=None, dataloader_idx=None):
    model_outputs = Prediction(scores=self(batch).score)
    if self.mc_dropout:
        mcd_outputs = torch.stack(
            [self(batch).score for _ in range(self.mc_dropout)]
        )
        model_outputs["metadata"] = Prediction(
            mcd_scores=mcd_outputs.mean(dim=0),
            mcd_std=mcd_outputs.std(dim=0),  # Calibration mechanism
        )
    return model_outputs
```

From `comet/models/multitask/xcomet_metric.py` showing rationale capture:
```python
# XCOMET models output error spans with severity labels
output["metadata"] = Prediction(
    error_spans=[{
        'confidence': 0.416,
        'start': 13, 'end': 21,
        'severity': 'minor',  # MQM error categories
        'text': 'my food'
    }]
)
```

From `README.md` showing ensemble-like usage:
```md
# Different evaluators on same output:
model1 = load_from_checkpoint("Unbabel/wmt22-comet-da")
model2 = load_from_checkpoint("Unbabel/wmt22-cometkiwi-da")
# Can run multiple evaluators and aggregate results
```

Strengths:
1. Multiple evaluator types: Reference-based, reference-free, explainable
2. Pre-built judge models: 10+ pre-trained evaluators covering different sizes/capabilities
3. Rationale capture: XCOMET models provide error spans with severity labels
4. Calibration: MC Dropout for uncertainty estimation
5. Ensemble support: Can run multiple evaluators (though aggregation is manual)
6. Fine-tuned evaluators: Can train custom evaluators on domain-specific data

Rating: 3 pts - Comprehensive evaluator model support with multiple types, rationale capture, and calibration mechanisms.

### S4F4: Multi-Modal Scoring Protocols (0 pts)

Evidence: COMET is text-only with no multi-modal capabilities.

From `comet/encoders/base.py`:
```python
def prepare_sample(
    self,
    sample: List[str],  # Only accepts text strings
    word_level: bool = False,
    annotations: Optional[List[dict]] = None,
) -> Dict[str, torch.Tensor]:
    """Receives a list of strings and applies tokenization"""
    tokenizer_output = self.tokenizer(
        sample,  # Text-only input
        return_tensors="pt",
        padding=True,
        truncation=True,
    )
```

From `README.md` example usage:
```python
data = [
    {
        "src": "10 到 15 分钟可以送到吗",  # Text only
        "mt": "Can I receive my food in 10 to 15 minutes?",
        "ref": "Can it be delivered between 10 to 15 minutes?"
    }
]
model_output = model.predict(data, batch_size=8, gpus=1)
```

Missing capabilities:
1. No image captioning metrics (CIDEr, SPICE, CLIP score)
2. No VQA support
3. No audio/speech metrics (WER, MOS)
4. No video understanding
5. All encoders (XLM-R, BERT) are text-only

Rating: 0 pts - Text-only framework with no multi-modal support.

### S4F5: Aggregate Statistics and Cross-Model Comparison (1 pt)

Evidence: Very limited aggregation - only basic averaging.

From `comet/models/base.py`:
```python
def predict(self, samples, ...):
    scores = torch.cat([pred["scores"] for pred in predictions], dim=0).tolist()
    output = Prediction(
        scores=scores,
        system_score=sum(scores) / len(scores)  # Only mean
    )
    return output
```

From `comet/models/metrics.py` showing correlation metrics (for validation only):
```python
class RegressionMetrics(Metric):
    def compute(self) -> torch.Tensor:
        """Computes spearmans correlation coefficient."""
        kendall, _ = stats.kendalltau(preds.tolist(), target.tolist())
        spearman, _ = stats.spearmanr(preds.tolist(), target.tolist())
        pearson, _ = stats.pearsonr(preds.tolist(), target.tolist())
        # These are only used during training/validation
        # Not available in predict mode
        return {
            self.prefix + "_kendall": kendall,
            self.prefix + "_spearman": spearman,
            self.prefix + "_pearson": pearson,
        }
```

From `comet/cli/compare.py` showing comparison capability:
```bash
# compare.py exists but only does paired t-test and bootstrap
comet-compare -s src.de -t hyp1.en hyp2.en -r ref.en
# Uses external libraries, not well-integrated
```

From `comet/models/metrics.py` showing system-level accuracy:
```python
def system_accuracy(y_hat: List[float], y: List[float], system: List[str]) -> float:
    """System-level accuracy from 'To Ship not to Ship' paper"""
    data = pd.DataFrame({"y_hat": y_hat, "y": y, "system": system})
    data = data.groupby("system").mean()
    pairs = list(combinations(data.index.tolist(), 2))
    # Computes pairwise accuracy - basic comparison
```

Available features:
1. Basic statistics: Mean (system_score) only
2. Training metrics: Kendall, Spearman, Pearson (but only during training)
3. Simple comparison: `comet-compare` command for paired t-test
4. System-level grouping: Can group by system for pairwise accuracy

Missing features:
1. No median, std dev, variance, percentiles
2. No confidence intervals for predictions
3. No distribution analysis (histograms, outlier detection)
4. No significance testing built-in (compare.py is separate tool)
5. No ranking systems (Elo, TrueSkill)
6. No stratified statistics or weighted metrics

Rating: 1 pt - Provides mean aggregation and basic correlation metrics during training, but lacks comprehensive statistical analysis and comparison tools.

---

## Summary Assessment

Total Score: 5/15 points

Strengths:
- Excellent evaluator model integration (S4F3: 3 pts)
- Multiple pre-trained neural judges
- Error span detection with XCOMET
- MC Dropout for uncertainty
- Supports training custom evaluators

Critical Gaps:
- No output validation or normalization (S4F1: 0 pts)
- No traditional metrics library (S4F2: 1 pt)
- Text-only, no multi-modal support (S4F4: 0 pts)
- Minimal aggregation/statistics (S4F5: 1 pt)

Use Case:
COMET is a specialized neural MT evaluation tool, not a general-purpose evaluation framework. It excels at providing learned quality estimates but lacks the infrastructure for traditional metric computation, validation, and statistical analysis expected from comprehensive evaluation frameworks.