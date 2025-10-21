# Unbabel/COMET - Stage 8 (MONITOR) Evaluation

## Summary
COMET is a machine translation evaluation framework focused on training and using neural metrics to evaluate MT quality. It is NOT a monitoring/continuous improvement framework for LLM systems in production. COMET is designed for offline evaluation of translation quality using pre-trained metrics or training new metrics. It lacks production monitoring, drift detection, online evaluation, feedback loops, and automated improvement features entirely.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities exist. Framework is for offline MT evaluation only. |
| S8F2: Online Evaluation | 0 | No online/streaming evaluation. Only batch prediction via `predict()` method exists. |
| S8F3: Feedback Integration | 0 | No feedback loop mechanisms. Only supports static dataset evaluation. |
| S8F4: Improvement Planning | 0 | No automated recommendations or improvement planning features. |

## Detailed Analysis

### S8F1: Production Drift Monitoring (0/3 points)

Evidence of absence:

COMET is fundamentally an offline evaluation framework for machine translation quality assessment, not a production monitoring system.

From `comet/models/base.py` (lines 333-403), the `predict()` method shows this is batch-oriented:

```python
def predict(
    self,
    samples: List[Dict[str, str]],
    batch_size: int = 16,
    gpus: int = 1,
    devices: Union[List[int], str, int] = None,
    mc_dropout: int = 0,
    progress_bar: bool = True,
    accelerator: str = "auto",
    num_workers: int = None,
    length_batching: bool = True,
) -> Prediction:
    """Method that receives a list of samples (dictionaries with translations,
    sources and/or references) and returns segment-level scores, system level score
    and any other metadata outputed by COMET models.
```

This is a batch prediction function that processes complete datasets offline, not a streaming/monitoring function.

From `comet/cli/score.py` (lines 1-244), the scoring CLI shows it processes static files:

```python
parser.add_argument("-s", "--sources", type=Path_fr)
parser.add_argument("-t", "--translations", type=Path_fr, nargs="+")
parser.add_argument("-r", "--references", type=Path_fr)
```

No drift monitoring features:
- No statistical tests (KS test, chi-square, MMD)
- No drift score computation over time
- No per-feature drift analysis
- No performance degradation tracking
- No behavioral monitoring for production edge cases
- No alerting mechanisms whatsoever
- No logging infrastructure integration
- No streaming data support for continuous monitoring

The entire codebase focuses on evaluating translation quality given source/hypothesis/reference triplets, not monitoring production systems.

Rating: 0 points - Completely absent. COMET is not a production monitoring framework.

---

### S8F2: Online and Streaming Evaluation (0/3 points)

Evidence of batch-only processing:

From `comet/models/base.py` (lines 333-403), all prediction happens via the `predict()` method which requires complete sample lists:

```python
def predict(
    self,
    samples: List[Dict[str, str]],  # Complete list required
    batch_size: int = 16,
    ...
) -> Prediction:
```

The DataLoader usage in `comet/models/base.py` (lines 380-387) shows batch processing:

```python
dataloader = DataLoader(
    dataset=samples,
    batch_size=batch_size,
    sampler=sampler,
    collate_fn=self.prepare_for_inference,
    num_workers=num_workers,
    multiprocessing_context="fork" if torch.backends.mps.is_available() else None,
)
```

No A/B testing capabilities:

The CLI in `comet/cli/compare.py` exists but only compares multiple systems offline, not in production:

```python
def compare_command() -> None:
    parser = ArgumentParser(description="Command for comparing multiple MT systems.")
```

This compares static system outputs, not live A/B tests with traffic splitting.

No shadow deployment:

There is no mechanism to:
- Run candidate models alongside production models
- Perform side-by-side comparisons in real-time
- Ensure zero production impact during evaluation

No automated rollback:

The framework has no concept of:
- Deployment versioning
- Metric-based rollback triggers
- Automatic fallback mechanisms
- Production deployment states

No online metrics:
- No real-time metric computation
- No time-windowed aggregation
- No anomaly detection on live data

The `comet/models/metrics.py` file (lines 1-134) defines correlation metrics (Kendall, Spearman, Pearson) computed after batch prediction:

```python
class RegressionMetrics(Metric):
    def compute(self) -> torch.Tensor:
        """Computes spearmans correlation coefficient."""
        preds = torch.cat(self.preds, dim=0)
        target = torch.cat(self.target, dim=0)
        kendall, _ = stats.kendalltau(preds.tolist(), target.tolist())
        spearman, _ = stats.spearmanr(preds.tolist(), target.tolist())
```

These are offline correlation computations with human judgments, not online monitoring metrics.

Rating: 0 points - No online or streaming evaluation capabilities exist.

---

### S8F3: Feedback Loop Integration (0/3 points)

Evidence of static dataset approach:

Training in COMET uses static CSV files specified in config. From `configs/models/regression_model.yaml`:

```yaml
regression_metric:
  init_args:
    train_data: 
      - data/1720-da.csv
    validation_data: 
      - data/wmt-ende-newstest2021.csv
      - data/wmt-enru-newstest2021.csv
      - data/wmt-zhen-newstest2021.csv
```

From `comet/models/base.py` (lines 244-271), data loading is file-based:

```python
def setup(self, stage: str) -> None:
    """Data preparation function called before training by Lightning.
    stage (str): either 'fit', 'validate', 'test', or 'predict'
    """
    if stage in (None, "fit"):
        train_dataset = self.read_training_data(self.hparams.train_data[0])
        self.validation_sets = [
            self.read_validation_data(d) for d in self.hparams.validation_data
        ]
```

No production log parsing:

There is no mechanism to:
- Parse production logs
- Collect user feedback from deployed systems
- Ingest operational metrics from live environments
- Process real-time feedback vs batch ingestion

No failure mining:

The framework doesn't:
- Extract failure cases from production
- Automatically incorporate production failures into eval datasets
- Prioritize failures based on production frequency/severity

No metric updates based on production:

The metrics defined in `comet/models/metrics.py` are static correlation computations. There's no mechanism to:
- Update evaluation metrics based on production correlation
- Add new metrics based on production issues
- Validate metrics against production performance

No closed-loop automation:

There are no features for:
- Automatic re-evaluation triggers based on feedback accumulation
- Feedback accumulation thresholds
- Integration with retraining pipelines based on production data

The training command in `comet/cli/train.py` requires manual execution:

```python
def train_command() -> None:
    """CLI command to train COMET models."""
    parser = LightningArgumentParser(...)
```

This is a manual training process, not an automated feedback-driven retraining loop.

Rating: 0 points - No feedback loop integration exists.

---

### S8F4: Iteration Planning and Improvement Recommendations (0/3 points)

Evidence of manual analysis requirements:

The framework outputs scores and error spans (for XCOMET models) but provides no automated analysis. From `comet/cli/score.py` (lines 186-210):

```python
for i in range(len(data[files[0]])):  # loop over (src, ref)
    for j in range(len(files)):  # loop of system
        data[files[j]][i]["COMET"] = seg_scores[j][i]
        if errors and errors[j] and errors[j][i]:
            data[files[j]][i]["errors"] = errors[j][i]
            
        if not cfg.only_system:
            print(
                "{}\tSegment {}\tscore: {:.4f}".format(
                    files[j], i, seg_scores[j][i]
                )
            )

for j in range(len(files)):
    print("{}\tscore: {:.4f}".format(files[j], sys_scores[j]))
```

This simply outputs scores and detected error spans. Users must manually analyze these results.

No root cause analysis:

The framework doesn't:
- Identify performance bottlenecks automatically
- Perform error pattern analysis beyond error span detection
- Provide causal analysis tools

While XCOMET models detect error spans with severity labels (`comet/models/utils.py`, lines 48-54):

```python
class LabelSet:
    """Taken from: https://github.com/LightTag/sequence-labeling-with-transformers/"""
    def __init__(self, labels: List[str] = ["minor", "major", "critical"]):
        self.labels_to_id = {}
        self.ids_to_label = {}
```

This is just error detection, not root cause analysis of why errors occur or what to do about them.

No hyperparameter recommendations:

There are no features for:
- Sensitivity analysis of hyperparameters
- Suggested search spaces based on performance
- Expected impact estimates of hyperparameter changes

Hyperparameters are manually specified in config files like `configs/models/regression_model.yaml`:

```yaml
regression_metric:
  init_args:
    encoder_learning_rate: 1.0e-06
    learning_rate: 1.5e-05
    layerwise_decay: 0.95
```

No prompt optimization:

COMET evaluates translation quality; it doesn't work with prompts. The concept of "prompt optimization" doesn't apply to this framework.

No dataset expansion recommendations:

The framework doesn't:
- Identify underrepresented scenarios in the evaluation data
- Prioritize data collection needs
- Perform gap analysis to suggest missing test cases

No roadmap generation:

There are no features for:
- Structured experiment plans
- Prioritized improvement lists
- Impact vs effort estimates

Users must manually interpret scores and plan improvements.

Rating: 0 points - No automated improvement recommendations or planning features.

---

## Overall Assessment

Total Score: 0/12 points

COMET is fundamentally not a monitoring or continuous improvement framework. It is a specialized tool for:

1. Training neural MT evaluation metrics using static datasets with human judgments (Direct Assessments, MQM annotations)
2. Evaluating translation quality offline by scoring MT system outputs against references

The framework excels at its intended purpose (offline MT quality evaluation) but has zero capabilities for:
- Production monitoring
- Drift detection
- Online/streaming evaluation
- A/B testing in production
- Feedback loop integration
- Automated improvement recommendations

This is confirmed throughout the documentation:

From `README.md`:
> "COMET is an open-source framework for MT evaluation that can be used for two purposes:
> * To evaluate MT systems with our currently available high-performing metrics
> * To train and develop new metrics."

From `docs/source/running.rst`:
> "After installing COMET you can score you MT outputs with the following command:
> comet score -s sources.txt -h hypothesis.txt -r references.txt"

The entire design philosophy is batch evaluation of static datasets, not continuous monitoring of production systems.

Recommendation: If production monitoring, drift detection, online evaluation, or automated improvement for LLM/MT systems is required, a completely different framework would be needed. COMET should only be considered for its intended use case: offline evaluation and metric training for machine translation.