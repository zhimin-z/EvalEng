## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text Comparison and Pattern Matching
- File: `lm_eval/tasks/longbench/metrics.py`
- Functions: `normalize_answer()`, `normalize_zh_answer()`, `count_score()`, `retrieval_score()`, `classification_score()`
- Code Reference:
```python
def normalize_answer(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    # ... string manipulation only
```
These functions perform text normalization, pattern matching, and string comparison on model outputs without executing any code. They use regex patterns, string operations, and fuzzy matching to evaluate model-generated responses against references.

Evidence 2: F1 Score and Statistical Metrics
- File: `lm_eval/tasks/evalita_llm/metrics.py`
- Functions: `macro_f1_score()`, `micro_f1_score()`, `weighted_f1_score()`
- Code Reference:
```python
def macro_f1_score(items):
    unzipped_list = list(zip(*items))
    golds = unzipped_list[0]
    preds = unzipped_list[1]
    fscore = f1_score(golds, preds, average="macro")
    return fscore
```
These functions compute F1 scores by comparing predicted labels with reference labels using sklearn metrics. No execution of model-generated code occurs—only statistical analysis of classification results.

Evidence 3: JSON Schema Validation
- File: `lm_eval/tasks/jsonschema_bench/metrics.py`
- Functions: `is_json_schema_valid()`, `schema_conform_with_format_checker()`, `json_validity()`
- Code Reference:
```python
def json_validity(references: list[str], predictions: list[str]) -> bool:
    prediction = predictions[0]
    try:
        json.loads(prediction.strip().strip("```").strip("json").strip())
    except json.JSONDecodeError:
        return False
    return True
```
These functions validate JSON structure and schema conformance by parsing and inspecting the structure of model outputs without executing any code within them.

Evidence 4: Mathematical Expression Comparison
- File: `lm_eval/tasks/score/math/math_grader.py`
- Functions: `normalize_answer_string()`, `math_equal()`, `extract_answer()`
- Code Reference:
```python
def normalize_answer_string(expr: str) -> str:
    """Normalize answer expressions."""
    # String manipulation and regex operations
    expr = _remove_left_and_right(expr)
    expr = _process_and_or_inside_text(expr)
    expr = _remove_right_units(expr)
    # ... more string operations
    return expr
```
These functions normalize and compare mathematical expressions symbolically using sympy parsing. While sympy evaluates symbolic expressions, this is mathematical simplification/comparison, not execution of arbitrary model-generated code.

Evidence 5: BLEU, ROUGE, and Translation Metrics
- File: `lm_eval/api/metrics.py`
- Functions: `bleu()`, `chrf()`, `ter()`, aggregation functions
- Code Reference:
```python
@register_aggregation("bleu")
def bleu(items):
    refs = list(zip(*items))[0]
    preds = list(zip(*items))[1]
    refs, preds = _sacreformat(refs, preds)
    return sacrebleu.corpus_bleu(preds, refs).score
```
These metrics use sacrebleu library to compute corpus-level translation quality scores by comparing model outputs with references through n-gram matching and statistical measures.

Evidence 6: Exact Match and String Similarity
- File: `lm_eval/api/metrics.py`
- Functions: `exact_match_hf_evaluate()`, `f1_abstractive()` (in `lm_eval/tasks/qasper/metrics.py`)
- Code Reference:
```python
def exact_match_hf_evaluate(predictions, references, regexes_to_ignore=None, ...):
    if regexes_to_ignore is not None:
        for s in regexes_to_ignore:
            predictions = np.array([re.sub(s, "", x) for x in predictions])
    # ... string comparison logic
    score_list = predictions == references
    return {"exact_match": np.mean(score_list)}
```
These functions perform exact string matching and token-level F1 calculation through string normalization and comparison operations.

Evidence 7: Perplexity and Statistical Aggregations
- File: `lm_eval/api/metrics.py`
- Functions: `perplexity()`, `weighted_perplexity()`, `bits_per_byte()`, `bootstrap_stderr()`
- Code Reference:
```python
@register_aggregation("perplexity")
def perplexity(items):
    return math.exp(-mean(items))
```
These functions perform statistical aggregations on loglikelihood scores from the model without executing any generated content.

Evidence 8: Toxicity Scoring via API
- File: `lm_eval/tasks/realtoxicityprompts/metric.py`
- Function: `toxicity_perspective_api()`
- Code Reference:
```python
def toxicity_perspective_api(doc, predictions, toxicity_threshold=0.5, ...):
    data = {
        "comment": {"text": pred},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    # Makes API call for static analysis
    req_response = s.post(url, json=data, headers=headers)
```
This function sends model-generated text to Perspective API for toxicity scoring. The API performs static analysis of text content for toxicity attributes without executing the text as code.

Evidence 9: Core Evaluation Pipeline
- File: `lm_eval/evaluator.py`
- Functions: `evaluate()`, `simple_evaluate()`
- Code Reference:
```python
# From evaluator.py, lines ~568-640
for filter_key in task.instances[0].filtered_resps.keys():
    for doc_id, doc in doc_iterator:
        metrics = task.process_results(
            doc, [req.filtered_resps[filter_key] for req in requests]
        )
        # Metrics are computed through static analysis of filtered responses
```
The main evaluation pipeline processes model outputs through metric functions that perform static analysis. The code shows how responses are collected and passed through static analysis metrics.

Evidence 10: Aggregation and Bootstrap Statistics
- File: `lm_eval/evaluator_utils.py`
- Class: `TaskOutput`
- Method: `calculate_aggregate_metric()`
- Code Reference:
```python
def calculate_aggregate_metric(self, bootstrap_iters=100000) -> None:
    for (metric, filter_key), items in self.sample_metrics.items():
        try:
            agg_fn = self.task.aggregation()[metric]
        except KeyError:
            agg_fn = mean
        metric_key = f"{metric},{filter_key}"
        self.agg_metrics[metric_key] = agg_fn(items)
```
This method aggregates sample-level metrics using statistical functions without executing any model-generated artifacts.