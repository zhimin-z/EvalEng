## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: SQuAD Score Computation
- File: `metrics/squad/compute_score.py`
- Code Reference: `compute_score()` function
```
ground_truths = list(map(lambda x: x["text"], qa["answers"]))
prediction = predictions[qa["id"]]
exact_match += metric_max_over_ground_truths(exact_match_score, prediction, ground_truths)
```
This metric computes exact match and F1 scores by comparing model predictions against reference answers stored in the dataset. The ground truth answers are explicitly loaded from the dataset structure with fields like `qa["answers"]` containing gold standard text spans.

Evidence 2: SQuAD v2 Raw Scores
- File: `metrics/squad_v2/compute_score.py`
- Code Reference: `get_raw_scores()` function
```
gold_answers = [t for t in qa["answers"]["text"] if normalize_answer(t)]
if not gold_answers:
    gold_answers = [""]  # For unanswerable questions
```
Computes scores against explicit reference answers stored in `qa["answers"]["text"]` as gold standard labels. Handles unanswerable questions by providing empty string references, maintaining explicit ground truth comparison.

Evidence 3: ReCoRD Evaluation
- File: `metrics/super_glue/record_evaluation.py`
- Code Reference: `evaluate()` function
```
ground_truths = list(map(lambda x: x["text"], qa["answers"]))
prediction = predictions[qa["id"]]
```
Evaluates predictions against explicit ground truth answers from the ReCoRD dataset. The reference answers are loaded from `qa["answers"]` for direct comparison with model predictions.

Evidence 4: CUAD Score Computation
- File: `metrics/cuad/compute_score.py`
- Code Reference: `compute_score()` function
```
ground_truths = list(map(lambda x: x["text"], qa["answers"]))
```
Computes precision, recall, and F1 by comparing predictions to ground truth labels stored in the dataset, providing explicit reference-based evaluation metrics.

Evidence 5: Sequence Evaluation
- File: `metrics/seqeval/seqeval.py`
- Code Reference: `Seqeval._compute()` method
```
report = classification_report(
    y_true=references,
    y_pred=predictions,
    ...
)
```
Uses explicit label sequences as references for token classification evaluation. The `references` parameter contains ground truth label sequences for classification reporting.

Evidence 6: BERTScore Reference Comparison
- File: `metrics/bertscore/bertscore.py`
- Code Reference: `BERTScore._compute()` method
```
if isinstance(references[0], str):
    references = [[ref] for ref in references]
```
Compares predictions against reference sentences. The `references` parameter contains explicit reference text for evaluation, converted to list format for consistent processing.

Evidence 7: Evaluator Documentation
- File: `docs/source/base_evaluator.mdx`
- Code Reference: Documentation examples
```
label_column="label"
```
Documentation shows evaluators using datasets with explicit labels, where `label_column` parameter indicates ground truth labels are present in the dataset structure.

---

### Behavioral Specification

Evidence 1: Code Execution Evaluation
- File: `metrics/code_eval/code_eval.py`
- Code Reference: `CodeEval._compute()` method
```
for task_id, (candidates, test_case) in enumerate(zip(predictions, references)):
    for candidate in candidates:
        test_program = candidate + "\n" + test_case
        args = (test_program, timeout, task_id, completion_id[task_id])
        future = executor.submit(check_correctness, *args)
```
Executes test cases against model-generated code to verify functional correctness. The test cases are executable specifications that validate whether generated code behaves correctly through dynamic execution.

Evidence 2: Correctness Checking
- File: `metrics/code_eval/execute.py` (referenced)
- Code Reference: `check_correctness` function
The `check_correctness` function executes code against test cases, providing behavioral validation of model outputs through runtime verification rather than static comparison.

Evidence 3: Mathematical Problem Solving
- File: `additional-tests-requirements.txt`
- Code Reference: Dependencies
```
git+https://github.com/hendrycks/math.git
```
The inclusion of MATH benchmark dependency suggests support for executable test cases in mathematical problem solving, where solutions are validated through behavioral correctness rather than text matching.

---

### None

Evidence 1: Probabilistic Calibration
- File: `metrics/brier_score/brier_score.py`
- Code Reference: `BrierScore._compute()` method
```
brier_score = brier_score_loss(references, predictions, sample_weight=sample_weight, pos_label=pos_label)
```
Brier score is fundamentally a calibration metric that measures the quality of probabilistic predictions. While it uses references for calculation, it evaluates intrinsic properties of probability estimates rather than requiring specific reference outputs.

Evidence 2: Reference-Free Measurements
- File: `docs/source/types_of_evaluations.mdx`
- Code Reference: Measurements section
```
"In the case of model predictions, it can help to calculate the average [perplexity](https://huggingface.co/metrics/perplexity) of model predictions using different models such as [GPT-2](https://huggingface.co/gpt2) and [BERT](https://huggingface.co/bert-base-uncased), which can indicate the quality of generated text when no reference is available."
```
Documentation explicitly describes measurements as reference-free evaluations that provide insights without external references, such as perplexity and word length for assessing text quality.