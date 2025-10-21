## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Model output parsing and score extraction
- File: `eval/parser.py`
- Class/Function: `parse_output()`, `_parse_output_absolute()`, `_parse_output_relative()`
- Code Reference:
```python
def parse_output(outputs, mode: str):
    assert mode in [
        "absolute",
        "relative",
    ], "Invalid mode. Supported modes are: 'absolute' and 'relative'"

    if mode == "absolute":
        return _parse_output_absolute(outputs)

    if mode == "relative":
        return _parse_output_relative(outputs)
```
This evaluation harness performs static analysis of model-generated outputs by parsing and extracting scores from text responses without executing any code. The parser examines the textual structure of model outputs to extract evaluation results. The `_parse_output_absolute()` function uses regex pattern matching to extract scores (1-5) from model outputs, while `_parse_output_relative()` extracts comparative judgments (A or B) from text.

Evidence 2: Statistical correlation analysis
- File: `eval/utils.py`
- Function: `calculate_results()`
- Code Reference:
```python
def calculate_results(output_file_path, mode="a2a", skip_tie=False):
    def read_data_from_file():
        with open(output_file_path, "r") as file:
            return [json.loads(line) for line in file]

    def calculate_mean_scores(score_key):
        return [statistics.mean(d[score_key]) for d in data if d[score_key]]

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
This function performs statistical analysis on parsed model outputs, calculating correlation metrics and accuracy without executing any generated code. It analyzes the textual/numerical outputs from evaluation models, calculating correlations between Prometheus scores and reference scores (GPT-4 or human) through statistical comparison.

Evidence 3: Pairwise comparison validation
- File: `eval/benchmark/autoj_utils/pairwise_eval.py`
- Function: `evaluate_autoj_performance()`
- Code Reference:
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
            preds.append(do_one_func(d))
        return labels, preds
```
This function evaluates pairwise comparisons by analyzing the structure and content of model judgments without executing generated artifacts. It performs format validation and agreement calculation. The `do_one_rel()` function parses and validates relative grading outputs to ensure they contain only valid values ('A', 'B', 'TIE', or None).

---

### Dynamic Execution

Evidence 1: VLLM inference engine execution
- File: `eval/run_evaluate.py`
- Function: `batch_completions_with_retries()`
- Code Reference:
```python
def batch_completions_with_retries(
    model,
    inputs,
    params,
    batch_size,
    mode,
    parse_output,
    max_retries=5,
):
    batched_outputs = []

    batch_size = len(inputs)
    total_batches = len(inputs) // batch_size + (
        1 if len(inputs) % batch_size > 0 else 0
    )

    print("Processing initial batches...")
    for i in tqdm(
        range(0, len(inputs), batch_size), total=total_batches, desc="Initial Batches"
    ):
        batch_inputs = inputs[i : i + batch_size]
        batch_outputs = model.completions(batch_inputs, **params, use_tqdm=True)
        batched_outputs.extend(batch_outputs)
```
This function executes model-generated evaluation judgments through the VLLM inference engine. The harness runs the Prometheus evaluation model to generate scores and feedback for benchmark tasks, constituting dynamic execution of the evaluation model's inference process. The model execution generates evaluation outputs that are then parsed for feedback and scores.

Evidence 2: Prometheus evaluation model invocation
- File: `libs/prometheus-eval/prometheus_eval/judge.py`
- Class/Function: `PrometheusEval.absolute_grade()` and `relative_grade()`
- Code Reference:
```python
def absolute_grade(
    self,
    *,
    instructions: List[str],
    responses: List[str],
    rubric: List[str] | str,
    reference_answers: List[str] = None,
    params: Dict[str, Any] = {},
) -> Tuple[List[str], List[int]]:
    """
    Grades a batch of responses absolutely based on the provided instructions and responses.
    """
    
    # ... input preparation ...
    
    if self.is_async:
        feedbacks, scores = asyncio.run(
            async_batch_completions_with_retries(
                self.model,
                inputs,
                mode="absolute",
                params=params,
            )
        )
    else:
        feedbacks, scores = batch_completions_with_retries(
            self.model,
            inputs,
            mode="absolute",
            params=params,
        )

    return feedbacks, scores
```
These methods execute the Prometheus evaluation model to generate judgments on benchmark responses. The model is invoked to produce evaluation outputs dynamically based on input prompts, with support for both synchronous and asynchronous execution modes.

Evidence 3: BiGGen-Bench runtime model execution
- File: `BiGGen-Bench/run_response_eval.py`
- Function: `main()`
- Code Reference:
```python
def main(args):
    # ... setup code ...
    
    if is_prometheus:
        model = VLLM(eval_model_name, gpu_memory_utilization=0.9, max_model_len=8192)
        judge = PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)
    else:
        model = MockLLM(mode="absolute")
        judge = PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)

    feedbacks, scores = judge.absolute_grade(
        instructions=instructions,
        responses=responses,
        rubric=rubric,
        reference_answers=reference_answers,
    )
```
This script executes evaluation models (including Prometheus) to dynamically generate judgments on BiGGen-Bench benchmark responses. The model inference is performed at runtime using the VLLM engine, which executes the evaluation model to produce dynamic outputs that are subsequently analyzed.