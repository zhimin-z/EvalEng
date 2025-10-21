## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Central evaluation interface with standard NLP metrics
- File: `promptbench/metrics/eval.py`
- Class: `Eval`
- Code Reference:
```python
compute_cls_accuracy()
compute_squad_v2_f1()
compute_bleu()
compute_math_accuracy()
compute_vqa_accuracy()
compute_cider()
```
The `Eval` class serves as the central evaluation interface for the repository, providing deterministic, rule-based scoring functions that compute performance using mathematical formulas. These methods implement standard NLP evaluation metrics including accuracy, F1, BLEU, and CIDEr scores. All computations are algorithmic and reproducible, with no ML model involvement.

Evidence 2: Token-level scoring with string normalization
- File: `promptbench/metrics/squad_v2/compute_score.py`
- Functions: `compute_exact()`, `compute_f1()`, `normalize_answer()`, `get_tokens()`
- Code Reference:
```python
def compute_exact()  # Exact match calculation
def compute_f1()  # F1 score calculation with precision/recall
def normalize_answer()  # String normalization for matching
def get_tokens()  # Tokenization for scoring
```
The SQuAD v2 evaluator uses token-level F1 scores computed through deterministic string matching algorithms. The implementation includes exact match calculation and F1 score computation based on precision and recall. String normalization and tokenization functions ensure consistent matching without any learned model components.

Evidence 3: Visual question answering with rule-based text processing
- File: `promptbench/metrics/vqa/eval_vqa.py`
- Class: `VQAEval`
- Code Reference:
```python
evaluate()  # Computes VQA accuracy
processPunctuation()  # Text normalization
processDigitArticle()  # Text normalization
```
The VQA evaluator computes accuracy through mathematical answer matching combined with rule-based text normalization. The `evaluate()` method applies deterministic normalization rules via `processPunctuation()` and `processDigitArticle()` functions to process text before computing accuracy scores. All processing follows predefined rules rather than learned patterns.

Evidence 4: N-gram overlap with TF-IDF weighting
- File: `promptbench/metrics/cider/cider_scorer.py`
- Class: `CiderScorer`
- Code Reference:
```python
compute_cider()  # Computes CIDEr metric using n-gram matching
compute_score()  # TF-IDF weighted cosine similarity
# Statistical functions for n-gram frequency analysis
```
The CIDEr scorer implements algorithmic evaluation using TF-IDF weighted n-gram overlap. It computes scores through statistical functions that analyze n-gram frequency and calculate TF-IDF weighted cosine similarity between candidate and reference texts. This is a purely mathematical approach with deterministic computations based on n-gram statistics, containing no ML models, environmental execution, human judgment, or custom hybrid approaches.