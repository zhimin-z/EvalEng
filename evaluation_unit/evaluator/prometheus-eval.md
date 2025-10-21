## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Statistical Correlation Metrics
- File: `eval/utils.py`
- Functions: `calculate_correlations()`, `calculate_results()`
- Code Reference:
```python
def calculate_correlations(scores1, scores2):
    pr, _ = pearsonr(scores1, scores2)
    sr, _ = spearmanr(scores1, scores2)
    kt, _ = kendalltau(scores1, scores2)
    return {
        "Pearson": pr,
        "Kendall": kt,
        "Spearman": sr,
    }
```
The harness uses statistical correlation functions (Pearson, Spearman, Kendall's Tau) to evaluate the performance of LLM judges by comparing their scores against reference scores (GPT-4 scores, human scores). These are deterministic mathematical functions that compute similarity between score distributions, providing reproducible assessment through established computational measures.

Evidence 2: Accuracy Calculations
- File: `eval/utils.py`
- Functions: `calculate_one_abs_acc()`, `calculate_one_rel_acc()`
- Code Reference:
```python
def calculate_one_abs_acc(data, acc_list: list):
    accepted_scores, rejected_scores = (
        data["prometheus_score"][0],
        data["prometheus_score"][1],
    )
    # ... comparison logic
    for i in range(runs):
        if accepted_scores[i] is None or rejected_scores[i] is None:
            pass
        elif accepted_scores[i] > rejected_scores[i]:
            acc_list.append(1)
            break
```
The harness computes accuracy metrics by comparing model predictions against ground truth labels using rule-based logic (comparing scores, counting matches). This is a deterministic algorithmic evaluation that ensures consistent, reproducible results through predefined computational procedures.

Evidence 3: Consistency Measurement (Krippendorff's Alpha)
- File: `eval/consistency.py`
- Code Reference:
```python
alpha_ordinal = krippendorff.alpha(
    reliability_data=rate_data, level_of_measurement="ordinal"
)
result_val = alpha_ordinal
```
The harness calculates inter-rater reliability using Krippendorff's alpha, a statistical measure of agreement. This is a predefined algorithmic metric that provides deterministic assessment of annotation consistency through established statistical functions.

Evidence 4: Agreement and Consistency Metrics
- File: `eval/benchmark/autoj_utils/pairwise_eval.py`
- Functions: `check_res()`, `group_wise_collect()`
- Code Reference:
```python
def check_res(gt_label, pred_label, pred_label_exchange):
    correct = [0, 0]
    agree = 0
    both_correct = 0
    if gt_label == pred_label:
        correct[0] = 1
    # ... more comparison logic
    return correct, agree, both_correct
```
The evaluation calculates agreement rates and consistency scores through rule-based comparisons between predicted and ground truth labels. These are algorithmic evaluations based on exact matching and statistical aggregation, ensuring reproducible evaluation through deterministic computational measures.

Evidence 5: Pattern Matching for Output Parsing
- File: `eval/parser.py`
- Functions: `_parse_output_absolute()`, `_parse_output_relative()`
- Code Reference:
```python
pattern = r"""(?:\[RESULT\]|Score|\[SCORE\]|\[RESULT\]:|Score:|score:|Result:|\[Result\]|score of)\s*(?:\(\s*|\[\s*|)\s*(\d+)"""
matches = re.search(pattern, output, re.IGNORECASE | re.VERBOSE)
```
The harness uses regular expressions to parse and extract scores from model outputs. This is a rule-based, algorithmic approach to processing evaluation results that provides deterministic and reproducible score extraction through predefined pattern matching logic.

---

### ML-based

Evidence 1: Prometheus Model as Evaluator
- File: `eval/run_evaluate.py`
- Code Reference:
```python
from src.llms.vllm_utils import VLLM

model = VLLM(model_name, num_gpus=num_gpus, cache_dir=cache_dir)

feedbacks, scores = collect_and_zip_feedbacks_and_scores(
    model,
    inputs,
    records,
    params,
    parse_output,
    batch_size=1024,
    runs=1 if mode != "a2a" else 3,
    mode=mode,
)
```
The harness uses Prometheus models (LLMs) to evaluate other language models' outputs on benchmark tasks. The models generate feedback and scores for responses, acting as learned evaluators rather than rule-based metrics. This leverages learned representations for nuanced assessment that captures semantic and contextual quality beyond what deterministic metrics can measure.

Evidence 2: LLM-as-Judge Library Integration
- File: `libs/prometheus-eval/prometheus_eval/judge.py`
- Class: `PrometheusEval`
- Code Reference:
```python
class PrometheusEval:
    def __init__(
        self,
        model,
        absolute_grade_template: str = ABSOLUTE_PROMPT_WO_REF,
        relative_grade_template: str = RELATIVE_PROMPT_WO_REF,
    ):
        # ... model validation
        self.model = model
```
The PrometheusEval class wraps ML models (VLLM, LiteLLM) to perform evaluation. The models are trained language models that assess quality through inference, not predefined rules. This ML-based approach enables nuanced assessment of semantic and contextual quality dimensions that algorithmic methods cannot reliably capture.

Evidence 3: Multiple ML Model Support
- File: `libs/prometheus-eval/prometheus_eval/judge.py`
- Code Reference:
```python
if hasattr(model, "validate_vllm"):
    from .vllm import VLLM
elif hasattr(model, "validate_litellm"):
    from .litellm import AsyncLiteLLM, LiteLLM
```
The harness supports multiple ML model backends (VLLM for local inference, LiteLLM for API-based models like GPT-4) as evaluators. These are neural network-based models that generate evaluations through learned parameters, providing flexible ML-based assessment across different model architectures and deployment scenarios.

Evidence 4: Model Inference for Grading
- File: `BiGGen-Bench/run_response_eval.py`
- Code Reference:
```python
if is_prometheus:
    model = VLLM(eval_model_name, gpu_memory_utilization=0.9, max_model_len=8192)
    judge = PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)
else:
    model = AsyncLiteLLM(eval_model_name, batch_size=100, requests_per_minute=100)
    judge = PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)

feedbacks, scores = judge.absolute_grade(
    instructions=instructions,
    responses=responses,
    rubric=rubric,
    reference_answers=reference_answers,
)
```
The BiGGen-Bench evaluation uses ML models (Prometheus or other LLMs) to perform absolute grading on benchmark tasks. The models generate feedback and assign scores based on learned representations, not algorithmic rules. This demonstrates ML-based evaluators leveraging neural networks to assess quality through contextual understanding rather than predefined computational measures.

Evidence 5: Model-Specific Evaluation Templates
- File: `libs/prometheus-eval/test_absolute.py`
- Code Reference:
```python
model = VLLM(model="prometheus-eval/prometheus-7b-v2.0")
judge = PrometheusEval(
    model=model,
    absolute_grade_template=ABSOLUTE_PROMPT,
)

feedback, score = judge.single_absolute_grade(
    instruction=instruction,
    response=response,
    rubric=score_rubric,
    reference_answer=reference_answer
)
```
The test demonstrates using Prometheus-7B-v2.0 (a trained language model) as an evaluator. The model processes prompts with instructions and rubrics to generate evaluations, showing ML-based assessment of benchmark task outputs. This exemplifies how machine learning models serve as evaluators by leveraging learned representations to provide nuanced quality assessment that captures semantic and contextual dimensions.