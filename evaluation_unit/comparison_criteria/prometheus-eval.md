## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, Comparative Baseline]

## Detailed Analysis

### Explicit Labels

Evidence 1: Benchmark Dataset Structure
- File: `eval/benchmark/data_loader.py`
- Code Reference: `EvalDataLoader` class
```python
class EvalDataLoader:
    ALLOWED_FILES = [
        "feedback_collection_ood_test.json",
        "feedback_collection_test.json",
        "preference_collection_ood_test.json",
        "flask_eval.json",
        "hhh_alignment_eval.json",
        "mt_bench_eval.json",
        "mt_bench_human_judgement_eval.json",
        "vicuna_eval.json",
        "autoj_pairwise.json",
        "alpaca_eval.json",
    ]
```
The repository loads benchmark datasets containing reference answers and gold labels for evaluation. These files contain predetermined correct answers serving as static reference targets for absolute grading (1-5 scores) and relative grading (A vs B comparisons).

Evidence 2: Score Comparison Against Labels
- File: `eval/utils.py`
- Code Reference: `calculate_results()` function
```python
def calculate_results(output_file_path, mode="a2a", skip_tie=False):
    # ...
    if "feedback_collection_ood_test" in data_name:
        gpt4_scores = [d["gpt4_score"] for d in data]
        prometheus_scores = [d["prometheus_score"][0] for d in data]
        correct_predictions = sum(
            1 for x, y in zip(prometheus_scores, gpt4_scores) if x == y
        )
        total_predictions = len(prometheus_scores)
        accuracy = correct_predictions / total_predictions
```
Explicitly compares model outputs against reference answers and ground truth labels. Computes accuracy by comparing predicted scores to gold standard scores, demonstrating explicit label-based evaluation.

Evidence 3: Reference Answer Extraction
- File: `eval/benchmark/data_loader.py`
- Code Reference: `_parse_records()` method
```python
def _parse_records(self):
    if self.data_name in ["flask_eval", "mt_bench_eval", "vicuna_eval", "feedback_collection_ood_test"]:
        for record in self.records:
            if isinstance(record, dict) and "instruction" in record:
                extracted_sections = extract_sections(record["instruction"])
                record.update(extracted_sections)  # Includes reference_answer
```
Extracts reference answers from dataset records. These reference answers are incorporated into the evaluation data as gold standards for comparing model outputs.

---

### Behavioral Specification

Evidence 1: Pairwise Performance Evaluation
- File: `eval/benchmark/autoj_utils/pairwise_eval.py`
- Code Reference: `evaluate_autoj_performance()` function
```python
def evaluate_autoj_performance(data: list, mode: str, skip_tie: bool = False):
    def preprocess_autoj_data(data: list, mode: str):
        labels = []
        preds = []
        do_one_func = do_one_abs if mode == "a2r" else do_one_rel
        for d in data:
            if skip_tie and d["label"] == 2:
                continue
            labels.append(d)
            preds.append(do_one_func(d))  # Executable validation function
        return labels, preds
```
Implements executable validation logic to check if model outputs meet specific behavioral criteria. Uses dynamic validator functions to verify correctness based on functional requirements rather than static comparison.

Evidence 2: Absolute Scoring Validation
- File: `eval/benchmark/autoj_utils/pairwise_eval.py`
- Code Reference: `do_one_abs()` function
```python
def do_one_abs(data):
    accepted_scores, rejected_scores = (
        data["prometheus_score"][0],
        data["prometheus_score"][1],
    )
    # Validation logic: checks if accepted > rejected
    if data["label"] != 2:
        for i in range(runs):
            if accepted_scores[i] is None or rejected_scores[i] is None:
                pass
            elif accepted_scores[i] > rejected_scores[i]:
                return data["label"]  # Validates correct behavior
                break
```
Dynamic validator checking if model outputs satisfy correctness criteria. Validates that accepted responses score higher than rejected ones, implementing programmatic behavioral specification rather than static label matching.

Evidence 3: Accuracy Computation Functions
- File: `eval/utils.py`
- Code Reference: `calculate_one_abs_acc()` function
```python
def calculate_one_abs_acc(data, acc_list: list):
    accepted_scores, rejected_scores = (
        data["prometheus_score"][0],
        data["prometheus_score"][1],
    )
    # Functional correctness validation
    if "tie" not in data.keys():
        for i in range(runs):
            if accepted_scores[i] > rejected_scores[i]:
                acc_list.append(1)  # Output passes validation
                break
```
Implements assertion-like checks for model output validation. These functions dynamically verify whether outputs satisfy specific behavioral criteria through programmatic correctness checks on benchmark tasks.

---

### Comparative Baseline

Evidence 1: Baseline Model Comparison
- File: `eval/utils.py`
- Code Reference: GPT-4 and human baseline comparison
```python
def calculate_results(output_file_path, mode="a2a", skip_tie=False):
    # ...
    if "flask" in output_file_path:
        human_scores = calculate_mean_scores("human_score")
        results["with Human"] = calculate_correlations(prometheus_scores, human_scores)
    
    gpt4_scores = calculate_mean_scores("gpt4_score")
    results["with GPT4"] = calculate_correlations(prometheus_scores, gpt4_scores)
```
Explicitly loads and compares against baseline model outputs from GPT-4 and human evaluators. Computes correlation metrics to assess relative performance against these comparative baselines.

Evidence 2: Correlation Metrics
- File: `eval/utils.py`
- Code Reference: `calculate_correlations()` function
```python
def calculate_correlations(scores1, scores2):
    pr, _ = pearsonr(scores1, scores2)  # Compare to baseline
    sr, _ = spearmanr(scores1, scores2)
    kt, _ = kendalltau(scores1, scores2)
    return {
        "Pearson": pr,
        "Kendall": kt,
        "Spearman": sr,
    }
```
Computes correlation metrics against baseline system outputs. These statistical measures assess agreement between model predictions and baseline judgments, enabling relative quality assessment.

Evidence 3: Baseline Judgment Loading
- File: `eval/benchmark/data_loader.py`
- Code Reference: Baseline output preservation
```python
# Data files contain baseline outputs like:
# - "gpt4_score": [scores from GPT-4]
# - "human_score": [scores from humans]
# - "chosen"/"rejected": human preference rankings
```
The data loader preserves baseline model and human outputs for comparative evaluation. These stored judgments serve as comparison standards for assessing model performance relative to established baselines.

Evidence 4: Transitivity Analysis
- File: `eval/transitivity.py`
- Code Reference: Cross-model comparison
```python
def add_response_score_A(row):
    return search_dict(row["orig_response_A"])  # Retrieves baseline score

def add_response_score_B(row):
    return search_dict(row["orig_response_B"])  # Retrieves baseline score
```
Implements transitivity checks by comparing model outputs against ground truth rankings. Retrieves baseline scores for cross-model comparison, enabling systematic assessment of relative performance through preference agreement metrics.