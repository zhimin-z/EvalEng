## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Target Reference in Evaluation Loop
- File: `lm_eval/evaluator.py`
- Code Reference: Ground truth labels in evaluation loop (Lines 633-656)
```python
for doc_id, doc in doc_iterator:
    # ...
    metrics = task.process_results(
        doc, [req.filtered_resps[filter_key] for req in requests]
    )
    if log_samples:
        target = task.doc_to_target(doc)
        example = {
            "doc_id": doc_id_true,
            "doc": doc,
            "target": target,  # Gold standard target
            # ...
        }
```
The evaluation process compares model predictions against reference answers stored in documents. The `target` field contains gold standard answers extracted from benchmark datasets for comparison.

Evidence 2: Ground Truth Answer Matching
- File: `lm_eval/tasks/longbench/metrics.py`
- Code Reference: `get_count_score()` function
```python
def get_count_score(doc: dict, results: list[str], **kwargs):
    output = 0.0
    prediction = results[0].strip()
    for ground_truth in doc["answers"]:  # Explicit gold answers
        score = count_score(prediction, ground_truth)
        output = max(score, output)
    return {"count_score": output}
```
Functions expect ground truth answers from `doc["answers"]`, comparing predictions against multiple explicit reference answers to compute maximum match scores.

Evidence 3: Math Problem Reference Answers
- File: `lm_eval/tasks/score/math/math_grader.py`
- Code Reference: `math_equal()` function (Line 282)
```python
def math_equal(
    prediction: Union[bool, float, str],
    reference: Union[float, str],  # Reference answer
    include_percentage: bool = True,
    tolerance: float = 1e-4,
    timeout: float = 10.0,
) -> bool:
```
Compares predictions against reference answers for math problems. The reference parameter contains gold standard solutions used as comparison targets for numerical and symbolic equality.

Evidence 4: QA Gold Standard Answers
- File: `lm_eval/tasks/qasper/metrics.py`
- Code Reference: `f1_abstractive()` function
```python
def f1_abstractive(predictions, references):
    """
    Taken from the official evaluation script for v1.1 of the SQuAD dataset.
    """
    prediction_tokens = normalize_answer(predictions[0]).split()
    references_tokens = normalize_answer(references[0]).split()  # Gold reference
```
Computes F1 scores by comparing prediction tokens against reference answer tokens. The references contain explicit gold standard answers from the dataset for token-level comparison.

Evidence 5: Translation Reference Texts
- File: `lm_eval/tasks/wmt2016/metrics.py`
- Code Reference: `agg_bleu()` function
```python
def agg_bleu(items):
    bleu_fn = evaluate.load("bleu")
    predictions, references = zip(*items)  # Reference translations
    return bleu_fn.compute(predictions=predictions, references=references)["bleu"]
```
Uses reference translations loaded from benchmark datasets to compute BLEU scores. The references provide explicit ground truth translations for quality assessment against model-generated translations.

---

### Behavioral Specification

Evidence 1: Mathematical Correctness Validation
- File: `lm_eval/tasks/score/math/math_grader.py`
- Code Reference: Executable verification functions (Lines 282-403)
```python
def math_equal(
    prediction: Union[bool, float, str],
    reference: Union[float, str],
    include_percentage: bool = True,
    tolerance: float = 1e-4,
    timeout: float = 10.0,
) -> bool:
    """
    Exact match of math if and only if:
    1. numerical equal: both can convert to float and are equal
    2. symbolic equal: both can convert to sympy expression and are equal
    """
```
Implements executable verification through numerical and symbolic computation. Validates mathematical correctness beyond string matching by evaluating equivalence through computational methods.

Evidence 2: Symbolic Equality Checking
- File: `lm_eval/tasks/score/math/math_grader.py`
- Code Reference: `symbolic_equal()` function (Line 446)
```python
def symbolic_equal(a, b, tolerance, timeout=10.0):
    import sympy
    # ... executable verification logic
    if sympy.simplify(a - b) == 0:
        return True
```
Uses symbolic computation to verify mathematical equivalence dynamically. This executable specification validates functional correctness through algebraic simplification rather than static comparison.

Evidence 3: JSON Schema Validation
- File: `lm_eval/tasks/jsonschema_bench/metrics.py`
- Code Reference: Schema conformance checker (Lines 46-71)
```python
def schema_conform_with_format_checker(
    instance: Dict[str, Any], schema: Dict[str, Any]
) -> bool:
    """
    Validate a JSON instance against a schema with enhanced format checking.
    """
    if not is_json_schema_valid(schema):
        raise ValidationError("The JSON schema is invalid.")
    validator = Draft202012Validator(schema, format_checker=format_checker)
    try:
        validator.validate(instance)  # Executable validation
    except ValidationError as e:
        raise ValidationError(e.message)
    return True
```
Executes schema conformance validation through dynamic checking. The validator provides executable specification for verifying structural and format correctness of JSON outputs.

Evidence 4: Schema Compliance Verification
- File: `lm_eval/tasks/jsonschema_bench/metrics.py`
- Code Reference: `schema_compliance()` function (Lines 74-97)
```python
def schema_compliance(references: list[str], predictions: list[str]) -> bool:
    # ... parses and validates JSON against schema
    schema_conform = schema_conform_with_format_checker(json_obj, json_schema)
    return schema_conform
```
Validates JSON objects against schema specifications through executable parsing and validation logic. This behavioral specification ensures outputs conform to structural requirements dynamically.

Evidence 5: Code Similarity Validation
- File: `lm_eval/tasks/longbench/metrics.py`
- Code Reference: `code_sim_score()` function (Lines 96-106)
```python
def code_sim_score(prediction: str, ground_truth: str, **kwargs):
    all_lines = prediction.lstrip("\n").split("\n")
    prediction = ""
    for line in all_lines:
        if ("`" not in line) and ("#" not in line) and ("//" not in line):
            prediction = line
            break
    return fuzz.ratio(prediction, ground_truth) / 100  # Behavioral check
```
Analyzes code structure through fuzzy matching after filtering non-code elements. This behavioral validation assesses structural similarity beyond exact string comparison.

---

### None

Evidence 1: Perplexity Calculations
- File: `lm_eval/api/metrics.py`
- Code Reference: Self-contained perplexity calculation (Lines 35-45)
```python
@register_aggregation("perplexity")
def perplexity(items):
    return math.exp(-mean(items))

@register_aggregation("weighted_perplexity")
def weighted_perplexity(items):
    return math.exp(-weighted_mean(items))

@register_aggregation("bits_per_byte")
def bits_per_byte(items):
    return -weighted_mean(items) / math.log(2)
```
Computes perplexity as intrinsic quality measure from log-likelihoods without external references. These metrics evaluate model uncertainty based solely on internal probability distributions.

Evidence 2: Perplexity Metric Registration
- File: `lm_eval/api/metrics.py`
- Code Reference: Reference-free metrics (Lines 198-220)
```python
@register_metric(
    metric="perplexity",
    higher_is_better=False,
    output_type="loglikelihood",
    aggregation="perplexity",
)
def perplexity_fn(items):  # This is a passthrough function
    return items

@register_metric(
    metric="word_perplexity",
    higher_is_better=False,
    output_type="loglikelihood_rolling",
    aggregation="weighted_perplexity",
)
def word_perplexity_fn(items):
    return items
```
Registers reference-free perplexity metrics that assess model outputs based on intrinsic log-likelihood properties without comparing to ground truth or baselines.

Evidence 3: Toxicity Scoring
- File: `lm_eval/tasks/realtoxicityprompts/metric.py`
- Code Reference: Intrinsic toxicity assessment (Lines 13-84)
```python
def toxicity_perspective_api(
    doc, predictions, toxicity_threshold=0.5, total_retries=5, **kwargs
):
    """Toxicity Perspective API is a metric which uses Perspective API to score 
    the toxicity of a generated sentence.
    """
    # ... scores toxicity without reference to ground truth
    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
```
Assesses content toxicity as intrinsic property using Perspective API. This reference-free metric evaluates output safety characteristics without comparing to external standards.

Evidence 4: JSON Validity Checking
- File: `lm_eval/tasks/jsonschema_bench/metrics.py`
- Code Reference: Structural validation (Lines 99-107)
```python
def json_validity(references: list[str], predictions: list[str]) -> bool:
    """Check if output is valid JSON"""
    prediction = predictions[0]
    try:
        json.loads(prediction.strip().strip("```").strip("json").strip())
    except json.JSONDecodeError:
        return False
    return True
```
Validates JSON structural correctness without references through parsing. This intrinsic metric checks format validity independent of content correctness or ground truth comparison.

Evidence 5: Bootstrap Error Calculations
- File: `lm_eval/evaluator_utils.py`
- Code Reference: Self-consistency measures (Lines 93-120)
```python
def calculate_aggregate_metric(self, bootstrap_iters=100000) -> None:
    for (metric, filter_key), items in self.sample_metrics.items():
        # ...
        self.agg_metrics[metric_key] = agg_fn(items)
        # ... stderr calculation without external reference
        self.agg_metrics[f"{metric}_stderr,{filter_key}"] = (
            stderr_fn(items) if (stderr_fn and len(items) > 1) else "N/A"
        )
```
Computes bootstrap standard errors as intrinsic variance measures. These self-consistency metrics assess result stability through resampling without requiring external reference standards.