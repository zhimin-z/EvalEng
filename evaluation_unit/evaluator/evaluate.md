# Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Built-in Algorithmic Metrics
- Files: `metrics/seqeval/seqeval.py`, `metrics/poseval/poseval.py`, `metrics/cer/test_cer.py`, `metrics/brier_score/brier_score.py`
- Code Reference:
```python
# metrics/seqeval/seqeval.py - Line 92-93
from seqeval.metrics import accuracy_score, classification_report

# metrics/poseval/poseval.py - Line 70-71
from sklearn.metrics import classification_report

# metrics/brier_score/brier_score.py - Line 31
from sklearn.metrics import brier_score_loss
```
The harness implements deterministic algorithmic metrics that rely on well-established mathematical formulas and statistical functions. The seqeval metric uses accuracy scores and classification reports for sequence labeling tasks, while poseval applies sklearn's classification report for part-of-speech tagging evaluation. The brier_score metric computes probabilistic calibration using sklearn's implementation. These are all rule-based, non-learned evaluators that compute scores through predefined algorithms without requiring neural network inference or trained model parameters.

Evidence 2: String Matching and Statistical Metrics
- Files: `metrics/squad/compute_score.py`, `metrics/squad_v2/compute_score.py`, `metrics/cuad/compute_score.py`
- Code Reference:
```python
# metrics/squad/compute_score.py - Lines 20-48
def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    # ...
    
def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    # ...
```
These functions implement token-level string matching algorithms for question answering evaluation. The normalize_answer function applies deterministic text preprocessing rules (lowercasing, removing articles, handling punctuation), while f1_score computes token overlap using set intersection operations. The exact_match_score function performs direct string comparison after normalization. All of these are purely algorithmic approaches that use regular expressions, string manipulation, and counting operations rather than learned representations, making them deterministic evaluators based on explicit matching rules.

Evidence 3: Information Retrieval Metrics
- Files: `metrics/trec_eval/trec_eval.py`
- Code Reference:
```python
# Lines 80-110
result["map"] = trec_eval.get_map(depth=10000, per_query=False, trec_eval=True)
result["bpref"] = trec_eval.get_bpref(depth=1000, per_query=False, trec_eval=True)
result["Rprec"] = trec_eval.get_rprec(depth=1000, per_query=False, trec_eval=True)
```
The TREC evaluation metrics compute standard information retrieval measures using algorithmic formulas. Mean Average Precision (MAP) calculates the average of precision values at relevant document positions, bpref (binary preference) measures ranking quality based on relevant versus non-relevant documents, and R-precision evaluates precision at the R-th position where R is the number of relevant documents. These are all deterministic mathematical computations based on ranking positions and relevance judgments, following established IR evaluation formulas without any machine learning components.

Evidence 4: Character and Token-Level Edit Distance
- Files: `metrics/cer/test_cer.py`
- Code Reference:
```python
# Lines 18-92
# S = 2, D = 0, I = 0, N = 11, CER = 2 / 11
char_error_rate = cer.compute(predictions=preds, references=refs)
```
Character Error Rate (CER) is computed using the Levenshtein distance algorithm, which calculates the minimum number of single-character edits (substitutions, deletions, insertions) required to transform the prediction into the reference. This is a classic dynamic programming algorithm that operates purely on character sequences using a well-defined mathematical formula: CER = (S + D + I) / N, where S is substitutions, D is deletions, I is insertions, and N is the total number of characters. The algorithm is completely deterministic and rule-based, requiring no learned parameters or model inference.

Evidence 5: Statistical Scoring Functions
- Files: `metrics/nist_mt/tests.py`
- Code Reference:
```python
# Lines 33-35
nist_score = nist.compute(
    predictions=[hypothesis_sent], references=[[reference_sent1, reference_sent2, reference_sent3]]
)
```
NIST MT score is an algorithmic metric for machine translation evaluation that extends BLEU by weighting n-gram matches based on their information gain. It computes n-gram precision statistics and applies arithmetic averaging with information-theoretic weighting, all based on predetermined mathematical formulas. The metric uses string matching to identify n-gram overlaps and statistical calculations to aggregate scores, making it a purely algorithmic approach that operates on surface-level text features without learned representations or neural network components.

---

### ML-based

Evidence 1: BERTScore - Transformer-based Evaluation
- Files: `metrics/bertscore/bertscore.py`
- Code Reference:
```python
# Lines 16-17, 96-100
import bert_score

self.cached_bertscorer = scorer(
    model_type=model_type,
    num_layers=num_layers,
    # ...
    device=device,
)

# Lines 112-117
(P, R, F) = self.cached_bertscorer.score(
    cands=predictions,
    refs=references,
    verbose=verbose,
    batch_size=batch_size,
)
```
BERTScore uses pre-trained BERT transformer models to compute contextual embeddings for both predictions and references, then measures similarity through cosine distance between token representations. This is fundamentally an ML-based evaluator because it relies on learned neural network parameters from BERT's pre-training on large text corpora. The model loads trained weights, performs forward passes through transformer layers to generate contextual representations, and uses these learned embeddings to assess semantic similarity. Unlike algorithmic metrics that use fixed rules, BERTScore's scoring depends entirely on the learned representations captured during BERT's training process.

Evidence 2: FrugalScore - Distilled ML Evaluation Model
- Files: `metrics/frugalscore/frugalscore.py`
- Code Reference:
```python
# Lines 57-59
self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# Lines 87-98
trainer = Trainer(self.model, training_args, tokenizer=self.tokenizer)
predictions = trainer.predict(tokenized_datasets)
return {"scores": list(predictions.predictions.squeeze(-1))}
```
FrugalScore is explicitly described as a "distillation approach that allows to learn a fixed, low cost version of any expensive NLG metric" (line 41), making it a trained ML model specifically designed for evaluation. It loads a fine-tuned sequence classification model that has been trained to predict quality scores, then uses this model's learned parameters to evaluate text generation outputs through inference. The use of AutoModelForSequenceClassification and the Trainer API demonstrates that this is a supervised learning approach where the model has been trained on labeled evaluation data to learn scoring patterns. This is a clear ML-based evaluator that uses learned weights rather than fixed algorithmic rules to assess output quality.