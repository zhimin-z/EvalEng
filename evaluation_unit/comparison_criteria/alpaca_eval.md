## Comparison Criteria Categories

[Comparative Baseline, None]

## Detailed Analysis

### Comparative Baseline

Evidence 1: Human preference annotations as comparison targets
- File: `src/alpaca_eval/analyze.py`
- Class/Function: `Analyzer.__init__()` and `Analyzer.agreement_of_annotations()`
- Code Reference:
```
def __init__(
    self,
    gold_crossannotations: Union[AnyPath, AnyData, Callable] = constants.ALPACAFARM_GOLD_CROSSANNOTATIONS,
    gold_annotations: Optional[Union[AnyPath, AnyData, Callable]] = constants.ALPACAFARM_GOLD_ANNOTATIONS,
    ...
):
    df_gold_crossannotations = utils.load_or_convert_to_dataframe(gold_crossannotations)
    self.df_gold_crossannotations = self._select_n_annotations(
        df_gold_crossannotations, n_annotators=self.n_annotators
    )
```
The harness loads human preference annotations (`gold_crossannotations`, `gold_annotations`) that contain pairwise preference judgments from multiple human annotators. These are used as baseline comparison targets to evaluate model outputs. The `preference` field in the data indicates which output humans preferred (1 or 2), serving as comparative baseline data.

Evidence 2: Reference model outputs for head-to-head comparison
- File: `src/alpaca_eval/annotators/pairwise_evaluator.py`
- Function: `PairwiseAnnotatorLocal.annotate_head2head()`
- Code Reference:
```
def annotate_head2head(
    self,
    outputs_1: Union[Sequence[dict[str, Any]], pd.DataFrame],
    outputs_2: Union[Sequence[dict[str, Any]], pd.DataFrame],
    ...
) -> list[dict[str, Any]]:
    """Head-to-head comparison between two sequence of outputs."""
```
This function enables direct comparison between outputs from two different models or between a model and a reference baseline. The outputs from one model/system serve as comparative baselines for evaluating the other.

---

### None

Evidence 1: Length-based intrinsic metrics
- File: `src/alpaca_eval/analyze.py`
- Function: `Analyzer.get_length_biases()`
- Code Reference:
```
def get_length_biases(
    self, annotations: Union[pd.DataFrame, str], significant_delta_length: int = 30
) -> dict[str, float]:
    """Estimate the biases for longer sentences."""
    df["best_output_length"] = df["best_output"].apply(len)
    df["worse_output_length"] = df["worse_output"].apply(len)
    df["one_is_longer"] = (
        df["best_output_length"] - df["worse_output_length"]
    ).abs() > significant_delta_length
```
This function computes intrinsic properties of model outputs (length) without comparing to external references. It measures whether the evaluator has a bias toward preferring longer outputs, which is a self-contained quality assessment.

Evidence 2: List formatting bias detection
- File: `src/alpaca_eval/analyze.py`
- Function: `Analyzer.get_list_biases()`
- Code Reference:
```
def get_list_biases(self, annotations: Union[pd.DataFrame, str]) -> dict[str, float]:
    """Estimate the biases for sentences with lists."""
    df["is_best_list"] = df["best_output"].apply(utils.contains_list)
    df["is_worse_list"] = df["worse_output"].apply(utils.contains_list)
```
This measures intrinsic formatting properties (presence of lists) in outputs without external references. It evaluates whether the annotator has inherent biases based on output structure alone.

Evidence 3: Time and cost efficiency metrics
- File: `src/alpaca_eval/analyze.py`
- Function: `get_metrics_evaluator()`
- Code Reference:
```
def get_metrics_evaluator(analyzer, df_crossannotations, evaluator_name=None):
    all_metrics["Price [$/1000 examples]"] = df_crossannotations["price_per_example"].mean() * 1000
    all_metrics["Time [seconds/1000 examples]"] = df_crossannotations["time_per_example"].mean() * 1000
```
These are reference-free efficiency metrics that measure the computational cost and latency of the evaluation process itself, independent of any external standards or baselines.

Evidence 4: Statistical variance and bias estimation
- File: `src/alpaca_eval/analyze.py`
- Functions: `Analyzer.estimate_variance()` and `Analyzer.estimate_bias()`
- Code Reference:
```
def estimate_variance(self, annotations: Union[pd.DataFrame, str]) -> float:
    """(over)Estimates the variance of the annotations by computing the 1 vs all agreement error."""
    agreement = self.agreement_of_annotations(
        annotations, annotations_2=None, n_majority_vote_1=1, n_majority_vote_2=None
    )
    return agreement["error"]
```
These functions compute intrinsic statistical properties of the annotations (variance, bias) through internal consistency checks, measuring agreement within the annotator's own predictions without requiring external references.