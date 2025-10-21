## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text Comparison and Metrics Computation
- File: `metrics/squad/compute_score.py`
- Functions: `normalize_answer()`, `f1_score()`, `exact_match_score()`, `compute_score()`
- Code Reference:
```python
def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    # ...
    return white_space_fix(remove_articles(remove_punc(lower(s))))

def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    # ... computes F1 based on token overlap
```
This module computes SQuAD metrics by comparing model predictions against reference answers through text normalization, token matching, and F1/exact match scoring. No code execution occurs—only string processing and comparison, demonstrating pure static analysis where outputs are directly examined without executing generated artifacts.

Evidence 2: Token Classification Evaluation
- File: `metrics/seqeval/seqeval.py`
- Class/Function: `Seqeval._compute()`
- Code Reference:
```python
def _compute(self, predictions, references, suffix: bool = False, ...):
    report = classification_report(
        y_true=references,
        y_pred=predictions,
        suffix=suffix,
        output_dict=True,
        # ...
    )
    # Processes classification report to extract metrics
```
Uses seqeval library to compute precision, recall, F1, and accuracy for sequence labeling tasks by comparing predicted and reference label sequences. This is pure static comparison without executing generated code, evaluating model outputs through direct examination of label sequences.

Evidence 3: BERTScore Metric
- File: `metrics/bertscore/bertscore.py`
- Class/Function: `BERTScore._compute()`
- Code Reference:
```python
def _compute(self, predictions, references, lang=None, model_type=None, ...):
    # Uses BERTScorer to compute precision, recall, F1
    (P, R, F) = self.cached_bertscorer.score(
        cands=predictions,
        refs=references,
        verbose=verbose,
        batch_size=batch_size,
    )
    return {"precision": P.tolist(), "recall": R.tolist(), "f1": F.tolist(), ...}
```
Computes semantic similarity between predictions and references using BERT embeddings and cosine similarity. While it uses a neural model for embeddings, it's analyzing model outputs through comparison, not executing generated artifacts. This represents static analysis with sophisticated comparison methods rather than dynamic execution.

Evidence 4: Character Error Rate (CER)
- File: `metrics/cer/test_cer.py`
- Class/Function: `TestCER.test_cer_case_sensitive()`
- Code Reference:
```python
def test_cer_case_sensitive(self):
    refs = ["White House"]
    preds = ["white house"]
    # S = 2, D = 0, I = 0, N = 11, CER = 2 / 11
    char_error_rate = cer.compute(predictions=preds, references=refs)
```
Tests for CER metric which computes edit distance between prediction and reference strings. This is purely text comparison without execution, exemplifying static analysis through direct string-level comparison of model outputs against references.

Evidence 5: POS Tagging Evaluation
- File: `metrics/poseval/poseval.py`
- Class/Function: `Poseval._compute()`
- Code Reference:
```python
def _compute(self, predictions, references, zero_division: Union[str, int] = "warn"):
    report = classification_report(
        y_true=[label for ref in references for label in ref],
        y_pred=[label for pred in predictions for label in pred],
        output_dict=True,
        zero_division=zero_division,
    )
    return report
```
Evaluates POS tagging by treating each token independently and computing classification metrics using scikit-learn's classification_report. Pure static comparison of labels without any execution, directly examining predicted labels against reference labels.

Evidence 6: Text Classification Evaluator
- File: `tests/test_evaluator.py`
- Class/Function: `TextClassificationEvaluator.compute()`
- Code Reference:
```python
def test_pipe_init(self):
    results = self.evaluator.compute(
        model_or_pipeline=self.pipe,
        data=self.data,
        input_column="text",
        label_column="label",
        label_mapping=self.label_mapping,
    )
    self.assertEqual(results["accuracy"], 1.0)
```
The evaluator compares model predictions (labels) against reference labels and computes metrics like accuracy, precision, recall, F1. The example shows it only performs label comparison through direct examination of classification outputs without executing any generated artifacts.

Evidence 7: Question Answering Evaluator
- File: `tests/test_evaluator.py`
- Class/Function: `QuestionAnsweringEvaluator.compute()`
- Code Reference:
```python
def test_pipe_init(self):
    results = self.evaluator.compute(
        model_or_pipeline=self.pipe,
        data=self.data,
    )
    self.assertEqual(results["exact_match"], 100.0)
    self.assertEqual(results["f1"], 100.0)
```
Compares predicted answers against reference answers using SQuAD metrics (exact match and F1). No execution of generated artifacts occurs—only static comparison of text answers to assess correctness through direct output examination.

Evidence 8: Image Classification Evaluator
- File: `tests/test_evaluator.py`
- Class/Function: `ImageClassificationEvaluator.compute()`
- Code Reference:
```python
def test_pipe_init(self):
    results = self.evaluator.compute(
        model_or_pipeline=self.pipe,
        data=self.data,
        label_mapping=self.label_mapping,
    )
    self.assertEqual(results["accuracy"], 0)
```
Evaluates image classification by comparing predicted labels with ground truth labels. Static comparison of classification outputs where model predictions are directly examined against references without executing generated code or artifacts.

Evidence 9: TREC Evaluation
- File: `metrics/trec_eval/trec_eval.py`
- Class/Function: `TRECEval._compute()`
- Code Reference:
```python
def _compute(self, references, predictions):
    # Creates TREC run and qrel objects
    trec_eval = TrecEval(trec_run, trec_qrel)
    
    # Computes various IR metrics through comparison
    result["map"] = trec_eval.get_map(depth=10000, per_query=False, trec_eval=True)
    result["bpref"] = trec_eval.get_bpref(depth=1000, per_query=False, trec_eval=True)
```
Computes information retrieval metrics (precision, recall, nDCG, AUPR) by comparing ranked document lists against relevance judgments. Pure static comparison that directly examines model-generated rankings without execution, assessing output quality through mathematical comparison.

Evidence 10: Brier Score
- File: `metrics/brier_score/brier_score.py`
- Class/Function: `BrierScore._compute()`
- Code Reference:
```python
def _compute(self, references, predictions, sample_weight=None, pos_label=1):
    brier_score = brier_score_loss(references, predictions, sample_weight=sample_weight, pos_label=pos_label)
    return {"brier_score": brier_score}
```
Computes Brier score for probability predictions by comparing predicted probabilities with true binary outcomes. Statistical comparison without execution, representing static analysis through direct mathematical evaluation of model output quality against ground truth.

Evidence 11: FrugalScore
- File: `metrics/frugalscore/frugalscore.py`
- Class/Function: `FRUGALSCORE._compute()`
- Code Reference:
```python
def _compute(self, predictions, references, batch_size=32, max_length=128, device=None):
    # Tokenizes and computes scores using a trained model
    predictions = trainer.predict(tokenized_datasets)
    return {"scores": list(predictions.predictions.squeeze(-1))}
```
Uses a distilled model to score text generation quality by computing similarity scores between predictions and references. While it uses a neural model internally, it's performing static comparison of text outputs—directly examining generated text against references without executing code artifacts.

Evidence 12: Documentation Confirmation
- File: `docs/source/types_of_evaluations.mdx`
- Code Reference:
```markdown
## Metrics
A metric measures the performance of a model on a given dataset. This is often based on an existing ground truth (i.e. a set of references)...

Examples of metrics include:
- [Accuracy](https://huggingface.co/metrics/accuracy)
- [Exact Match](https://huggingface.co/metrics/exact_match)
```
Describes three types of evaluations, with "Metrics" being the primary category that "measures the performance of a model on a given dataset" by comparing predictions to references. This documentation explicitly confirms the harness's focus on static analysis through direct comparison-based evaluation without artifact execution.