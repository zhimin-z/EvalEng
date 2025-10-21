## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, Comparative Baseline, None, Custom]

## Detailed Analysis

### Explicit Labels

Evidence 1: Task Document Processing
- File: `lmms_eval/evaluator.py`
- Code Reference: Ground truth processing
```python
for doc_id, doc in doc_iterator:
    requests = instances_by_doc_id[doc_id]
    metrics = task.process_results(doc, [req.filtered_resps[filter_key] for req in requests])
    if log_samples:
        target = task.doc_to_target(doc)
        saved_doc = {}
        for key, value in doc.items():
```
Tasks load documents with ground truth answers via `doc_to_target`, and model outputs are compared against these predetermined correct answers through the `process_results` method. This establishes explicit reference targets as the primary evaluation mechanism.

Evidence 2: Metric Aggregation Structure
- File: `lmms_eval/evaluator_utils.py`
- Code Reference: TaskOutput class
```python
for (metric, filter_key), items in self.sample_metrics.items():
    if metric in self.task.aggregation():
        agg_fn = self.task.aggregation()[metric]
        metric_key = f"{metric},{filter_key}"
```
The metric aggregation system processes evaluation results against reference answers stored in task documents. Model predictions are systematically compared to explicit labels through aggregation functions that accumulate correctness assessments.

---

### Behavioral Specification

Evidence 1: Structured Response Validation
- File: `tools/live_bench/live_bench/data_generator/score_getter.py`
- Code Reference: Prompt formatting (Lines 112-130)
```python
def _format_prompt(self, question: str, answer: str, images: List[Image.Image]):
    prompt = [{"role": "system", "content": self.prompt}]
    messages = []
    for image in images:
        messages.append(format_gpt4v_images(image))
    messages.append({"type": "text", "text": f"Question: {question}\nQuestioner's Answer: {answer}"})
    messages.append({"type": "text", "text": 'You should format you answer into json format like this: {"reason": "some reason", "score": 10}'})
```
Implements validation functions for generated responses with structured format requirements. The system validates behavioral correctness through executable specifications defining expected output structure and content format.

Evidence 2: Executable Metric Validators
- File: `lmms_eval/tasks/megabench/evaluator.py`
- Code Reference: Metric type validation
```python
elif metric == MetricType.SYMBOLIC_PLANNING_TEST or metric == MetricType.PROGRAM_JUDGE:
    query["scores"]["field"][field] = metric.match(
        response_obj.get(field),
        eval_context,
    )
elif metric == MetricType.CONSTRAINED_GENERATION:
    score, eval_info = metric.match(response_obj, eval_context)
```
Uses metric types like `SYMBOLIC_PLANNING_TEST` and `PROGRAM_JUDGE` that execute validation logic on model outputs. These behavioral specifications verify functional correctness through dynamic evaluation rather than static comparison.

Evidence 3: Multi-Modal Evaluation Specifications
- File: `docs/lmms-eval-0.3.md`
- Code Reference: Evaluation method documentation
```md
a. Accuracy: Used for tasks with definitive ground truth answers
b. WER: Applied to some Audio Speech Recognition (ASR) tasks.
c. GPT-4 Eval: Applied to open-ended responses.
```
Documents behavioral specifications including executable validators for different task types. The GPT-4 evaluation represents functional correctness checking through model-based judgment of response quality.

---

### Comparative Baseline

Evidence 1: Quality Assessment Scoring
- File: `tools/live_bench/live_bench/data_generator/score_prompt.md`
- Code Reference: Comparative evaluation prompt
```md
Based on the multi-round Q&A regarding the image, please evaluate each question and answer from the multi-round Q&A based on the image for their authenticity (whether the information can be directly obtained from the image or reasonably inferred) and logical coherence. For each Q&A pair, provide a rating from 1 to 10...
```
Evaluates model outputs relative to expected response quality standards through comparative assessment. The prompt establishes baseline criteria for authenticity and coherence against which responses are judged.

Evidence 2: Version Compatibility Baseline
- File: `docs/lmms-eval-0.4.md`
- Code Reference: Backward compatibility comparison table
```md
| Models (v0.3/v0.4) | AI2D | ChartQA | DocVQA-Val | MME Perception | MME Cognition |
|---|---|---|---|---|---|
| LLaVA-OneVision-7B | 81.35/81.35 | 80.0/80.0 | 87.1/87.1 | 1578.64/1578.64 |
```
Compares new harness version outputs against previous version results as baseline. This validates consistency by using prior system outputs as comparative reference standards.

Evidence 3: Reproducibility Validation
- File: `docs/lmms-eval-0.5.md`
- Code Reference: Reproducibility validation table
```md
| Model | Task | lmms-eval | Reported | Δ | Status |
|-------|------|----------|-----------|-----|--------|
| Qwen-2.5-7B-Instruct | MedQA | 53.89 | 54.28 | -0.39 | ✓ |
```
Compares lmms-eval scores against officially reported results from other systems. Uses external baseline scores as comparison targets to validate evaluation accuracy and consistency.

---

### None

Evidence 1: Throughput Performance Metrics
- File: `docs/throughput_metrics.md`
- Code Reference: Core timing metrics
```md
### Core Timing Metrics
- E2E (End-to-End Latency): Total time from request submission to response completion (in seconds)
- TTFT (Time to First Token): Time from request submission until the first token is generated
- TPOT (Time Per Output Token): Average time to generate each output token after the first
- Speed (Inference Speed): Token generation rate calculated as 1/TPOT
```
Documents intrinsic performance metrics measuring computational efficiency without external references. These timing measurements assess system characteristics independent of ground truth or baseline comparisons.

Evidence 2: Token Throughput Calculation
- File: `lmms_eval/models/model_utils/gen_metrics.py`
- Code Reference: Intrinsic throughput measurement
```python
def calculate_token_throughput(token_count: int, duration: float) -> float:
    """
    Calculate the token throughput.
    """
    if duration <= 0:
        return 0.0
    return token_count / duration
```
Computes token generation rate as intrinsic efficiency measure. This reference-free metric evaluates processing speed without requiring comparison to external standards.

Evidence 3: Statistical Confidence Metrics
- File: `lmms_eval/evaluator_utils.py`
- Code Reference: Bootstrap error calculation
```python
stderr_fn = stderr_for_metric(
    metric=agg_fn,
    bootstrap_iters=min(bootstrap_iters, 100) if metric in ["bleu", "chrf", "ter"] else bootstrap_iters,
)
```
Calculates bootstrap standard error as self-contained statistical measure. This intrinsic metric assesses result stability through resampling without external reference requirements.

---

### Custom

Evidence 1: Multi-Stage Field Evaluation
- File: `lmms_eval/tasks/megabench/evaluator.py`
- Code Reference: Hybrid evaluation pipeline
```python
# 2) Evaluate each field
for fld, fld_metric_name in field_score_functions.items():
    metric = self._build_metric(fld_metric_name, score_config)
    if isinstance(metric, VLMJudgeScore):
        has_vlm_metric = True
    self._evaluate_field(task_name, metric, fld, response_obj, correct_answer, query)

# Evaluate global auxiliary metrics (if any)
for fld, fld_metric_name in global_aux_metrics.items():
    metric = self._build_metric(fld_metric_name, score_config)
```
Implements complex evaluation pipeline with field-specific metrics and global auxiliary metrics. This hybrid approach combines multiple evaluation criteria types through specialized multi-stage processing tailored for MEGA-Bench requirements.

Evidence 2: Configurable Judge Framework
- File: `docs/lmms-eval-0.4.md`
- Code Reference: LLM-as-judge protocol
```md
A standardized protocol for using language models as judges to evaluate other model outputs:
Supported Judge Types:
- General: Open-ended evaluation with custom prompts
- Binary: Yes/No or 0/1 judgments  
- Score: Numerical scoring within a defined range
- Comparative: Compare two model responses
```
Provides specialized comparison framework with configurable judge types combining behavioral specification with comparative baseline evaluation. This custom system integrates multiple assessment dimensions through flexible judge configurations designed for diverse evaluation scenarios.