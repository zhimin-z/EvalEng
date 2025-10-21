## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Direct Assessment Scores
- Files: 
  - `comet/models/regression/regression_metric.py` (lines 106-120)
  - `comet/models/multitask/unified_metric.py` (lines 341-355)

```
# From regression_metric.py
def read_training_data(self, path: str) -> List[dict]:
    """Method that reads the training data (a csv file) and returns a list of
    samples.

    Returns:
        List[dict]: List with input samples in the form of a dict
    """
    df = pd.read_csv(path)
    df = df[["src", "mt", "ref", "score"]]
    df["src"] = df["src"].astype(str)
    df["mt"] = df["mt"].astype(str)
    df["ref"] = df["ref"].astype(str)
    df["score"] = df["score"].astype("float16")  # Explicit label: quality score
    return df.to_dict("records")
```
The COMET framework loads ground truth quality assessment scores from CSV files. These scores (e.g., Direct Assessment scores from WMT) serve as explicit reference labels for evaluating model outputs. The `score` field represents predetermined correct quality ratings that models are trained to predict.

Evidence 2: Reference Translations
- Files: 
  - `comet/cli/score.py` (lines 87-94)
  - `comet/models/regression/regression_metric.py` (lines 153-170)

```
# From score.py
if cfg.references is not None:
    with open(cfg.references(), encoding="utf-8") as fp:
        references = [line.strip() for line in fp.readlines()]
    data = {
        "src": [sources for _ in translations],
        "mt": translations,
        "ref": [references for _ in translations],  # Explicit reference labels
    }
```
Reference translations are loaded as explicit labels for benchmarking translation quality. These are gold standard human translations used as comparison targets for evaluating machine translation outputs.

Evidence 3: Human Preference Rankings (DARR Data)
- Files: 
  - `comet/models/ranking/ranking_metric.py` (lines 94-108)

```
# From ranking_metric.py
def read_training_data(self, path: str) -> List[dict]:
    """Method that reads the validation data (a csv file) and returns a list of
    samples.

    Returns:
        List[dict]: List with input samples in the form of a dict
    """
    df = pd.read_csv(path)
    df = df[["src", "pos", "neg", "ref"]]  # pos/neg are ranked translations
    df["src"] = df["src"].astype(str)
    df["pos"] = df["pos"].astype(str)
    df["neg"] = df["neg"].astype(str)
    df["ref"] = df["ref"].astype(str)
    return df.to_dict("records")
```
The ranking metric loads Direct Assessment Relative Ranks (DARR) data where translations are explicitly labeled as "positive" (better quality) and "negative" (worse quality). These are explicit comparative labels derived from human judgments.

Evidence 4: Error Annotations (MQM Labels)
- Files: 
  - `comet/models/multitask/unified_metric.py` (lines 653-654)

```
# From unified_metric.py
for span in error_spans:
    sentence_output.append(
        {
            "text": self.encoder.tokenizer.decode(span["tokens"]),
            "confidence": torch.concat(span["confidence"]).mean().item(),
            "severity": span["severity"],
            "start": span["offset"][0],
            "end": span["offset"][1],
        }
    )
decoded_output.append(sentence_output)
```
Error annotations with severity labels (minor, major, critical) based on MQM typology are loaded as explicit labels for training and evaluation. These annotations mark specific error spans with predetermined severity classifications.

Evidence 5: System-Level Scores
- Files: 
  - `comet/models/metrics.py` (lines 35-77)
  - `comet/cli/compare.py` (lines 124-148)

```
# From metrics.py
def system_accuracy(y_hat: List[float], y: List[float], system: List[str]) -> float:
    """Implementation of system-level accuracy proposed in
        [To Ship not to Ship](https://aclanthology.org/2021.wmt-1.57/)

    Args:
        y_hat (List[int]): List of metric scores
        y (List[int]): List of ground truth scores  # Explicit labels
        system (List[str]): List with the systems that produced a given translation.

    Return:
        Float: System-level accuracy.
    """
    try:
        data = pd.DataFrame({"y_hat": y_hat, "y": y, "system": system})
    except ValueError:
        raise Exception(...)
```
Ground truth system-level scores (`y`) are used as explicit labels to compute system-level accuracy metrics. These represent predetermined quality assessments for entire MT systems.