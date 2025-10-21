## Evaluator Categories

[Algorithmic, ML-based, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Basic statistical and mathematical metrics
- File: `lm_eval/api/metrics.py`
- Functions: Multiple algorithmic metric functions
- Code Reference:
```python
mean()
median()
nanmean()
perplexity()  # math.exp(-mean(items))
f1_score()  # sklearn F1 score
matthews_corrcoef()  # sklearn Matthews correlation
bleu()
chrf()
ter()  # sacrebleu library
exact_match_hf_evaluate()  # String matching with normalization
```
The harness uses predefined mathematical and statistical functions to evaluate model outputs deterministically. These include basic aggregations (mean, median), mathematical transformations (perplexity using exponential formula), machine translation metrics from established libraries (BLEU, CHRF, TER via sacrebleu), and sklearn-based scoring functions (F1, Matthews coefficient). All provide reproducible, rule-based computation without learned components.

Evidence 2: Text normalization and token-based scoring
- File: `lm_eval/tasks/longbench/metrics.py`
- Functions: Algorithmic scoring functions
- Code Reference:
```python
normalize_answer()  # Punctuation/article removal
count_score()  # Regex-based number extraction
retrieval_score()  # Regex pattern matching for paragraph IDs
rouge_score()  # ROUGE-L F1 calculation
f1_score()  # Token-level F1 using Counter objects
qa_f1_score()  # QA F1 with answer normalization
```
These functions implement deterministic text processing and scoring algorithms. They use rule-based normalization (removing punctuation, articles), regex pattern matching (for numbers and IDs), and token-level comparison (Counter-based F1). The ROUGE and QA F1 implementations follow established algorithmic procedures for computing overlap between predictions and references, ensuring consistent and reproducible evaluation.

Evidence 3: Standard machine translation metrics
- File: `lm_eval/tasks/wmt2016/metrics.py`
- Function: `agg_bleu()`
- Code Reference:
```python
def agg_bleu(items):
    bleu_fn = evaluate.load("bleu")
    predictions, references = zip(*items)
    return bleu_fn.compute(predictions=predictions, references=references)["bleu"]
```
This implementation loads the standard BLEU metric from the HuggingFace evaluate library, which implements the established bilingual evaluation understudy algorithm. BLEU is a deterministic metric based on n-gram precision with brevity penalty, computed through mathematical formulas without any learned parameters or probabilistic components.

Evidence 4: Domain-specific algorithmic metrics
- Files: Multiple task-specific metric files
  - `lm_eval/tasks/evalita_llm/metrics.py`
  - `lm_eval/tasks/aradice/*/metrics.py`
  - `lm_eval/tasks/japanese_leaderboard/ja_leaderboard_xlsum.py`
  - `lm_eval/tasks/qasper/metrics.py`
- Metrics: F1, precision, recall (sklearn), macro/micro/weighted F1, ROUGE2 with MeCab tokenization
The harness provides task-specific algorithmic implementations across diverse domains, all following deterministic computational procedures. The sklearn metrics (F1, precision, recall with various averaging strategies) use established classification evaluation formulas. The Japanese ROUGE2 with MeCab tokenization shows domain adaptation while maintaining algorithmic determinism through rule-based tokenization and n-gram overlap computation.

---

### ML-based

Evidence 1: Neural toxicity classification via external API
- File: `lm_eval/tasks/realtoxicityprompts/metric.py`
- Function: `toxicity_perspective_api()`
- Code Reference:
```python
def toxicity_perspective_api(
    doc, predictions, toxicity_threshold=0.5, total_retries=5, **kwargs
):
    """Toxicity Perspective API is a metric which uses Perspective API to score the toxicity of a generated sentence."""
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"
    # ... sends text to API for toxicity scoring
    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
```
This evaluator uses the Perspective API, which is a neural network-based toxicity classifier trained on large-scale human-annotated data. The evaluation process sends model-generated text to an external ML model that produces toxicity scores based on learned representations rather than rule-based computation. This represents ML-based evaluation where one trained model (Perspective API) judges the quality of outputs from another model being evaluated, capturing nuanced semantic properties that algorithmic approaches cannot assess.

---

### Environmental

Evidence 1: Symbolic mathematics execution environment
- File: `lm_eval/tasks/score/math/math_grader.py`
- Function: `math_equal()`
- Code Reference:
```python
def math_equal(
    prediction: Union[bool, float, str],
    reference: Union[float, str],
    include_percentage: bool = True,
    tolerance: float = 1e-4,
    timeout: float = 10.0,
) -> bool:
    """Exact match of math if and only if:
    1. numerical equal: both can convert to float and are equal
    2. symbolic equal: both can convert to sympy expression and are equal
    """
    from sympy.parsing.sympy_parser import parse_expr
    # ... evaluates mathematical expressions using sympy
```
The evaluator uses SymPy as a mathematical execution environment that parses, interprets, and evaluates symbolic mathematical expressions. Rather than performing simple string matching, it executes mathematical operations and symbolic simplification to determine semantic equivalence. The SymPy engine acts as an environment that validates whether generated expressions are mathematically correct through actual computation and algebraic manipulation, providing feedback based on mathematical rules and execution results.

Evidence 2: JSON schema validation environment
- File: `lm_eval/tasks/jsonschema_bench/metrics.py`
- Function: `schema_conform_with_format_checker()`
- Code Reference:
```python
def schema_conform_with_format_checker(
    instance: Dict[str, Any], schema: Dict[str, Any]
) -> bool:
    """Validate a JSON instance against a schema with enhanced format checking."""
    validator = Draft202012Validator(schema, format_checker=format_checker)
    try:
        validator.validate(instance)
    except ValidationError as e:
        raise ValidationError(e.message)
    return True
```
This evaluator uses the jsonschema library as an execution environment to validate model-generated JSON against formal specifications. The validator acts as an environmental system that interprets both the schema and the generated instance, checking structural conformance, type correctness, and format requirements. Success signals come from the validation environment's ability to execute the validation rules, making this an environmental evaluator that assesses quality through system-provided feedback rather than direct computation or learned models.