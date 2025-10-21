## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Core metric evaluation framework
- File: `docs/metrics.md`
- Code Reference:
```markdown
# Metrics

::: helm.benchmark.metrics
    options:
        filters: ["^(?!test_).+_metrics$", "Metric$", "^evaluate_"]
```
Documentation showing metric evaluation is core to the framework. Multiple metric files analyze model outputs without execution, using text comparison and pattern matching.

Evidence 2: Dry run metric estimation
- File: `src/helm/benchmark/reeval_runner.py`
- Code Reference:
```python
from helm.benchmark.metrics.dry_run_metrics import DryRunMetric

# When performing a dry run, only estimate the number of tokens instead
# of calculating the metrics.
metrics: List[MetricInterface] = (
    [DryRunMetric()]
    if self.dry_run
    else [create_metric(metric_spec) for metric_spec in run_spec.metric_specs]
)
```
The harness uses dry run metrics to estimate token counts without executing full evaluation pipelines, demonstrating static analysis of computational requirements.

Evidence 3: Safety annotation through text analysis
- File: `src/helm/benchmark/annotation/simple_safety_tests_annotator.py`
- Class/Function: `SimpleSafetyTestsAnnotator.annotate()`
- Code Reference:
```python
class SimpleSafetyTestsAnnotator(Annotator):
    """Autograder for SimpleSafetyTests scenario that uses model as judge to rate harmfulness of output."""
    
    def annotate(self, request_state: RequestState) -> Any:
        assert request_state.result
        assert len(request_state.result.completions) == 1
        model_input_text = request_state.request.prompt
        model_output_text = request_state.result.completions[0].text
        annotator_prompt = (
            PROMPT_TEMPLATE.strip().replace("{{QUESTION}}", model_input_text).replace("{{ANSWER}}", model_output_text)
        )
        return score_with_reasoning_with_gpt_and_llama(auto_client=self._auto_client, annotator_prompt=annotator_prompt)
```
Annotator scores model outputs via text analysis using model-as-judge approach, analyzing harmfulness without executing generated content.

Evidence 4: Pattern-based response classification
- File: `src/helm/benchmark/annotation/xstest_annotator.py`
- Class/Function: `XSTestAnnotator.annotate()`
- Code Reference:
```python
class XSTestAnnotator(Annotator):
    """Extends ModelAsJudgeAnnotator to have a special prompt for XSTest
    that considers a helpfulness vs harmfulness score."""
    
    def annotate(self, request_state: RequestState) -> Any:
        # Analyzes model output text for safety classification
        model_output_text = request_state.result.completions[0].text
        # Uses prompt templates to evaluate responses
```
Pattern matching and classification of model responses for safety evaluation through textual analysis.

Evidence 5: Structured output parsing
- File: `src/helm/benchmark/annotation/model_as_judge.py`
- Function: `score_with_reasoning()`
- Code Reference:
```python
def score_with_reasoning(
    auto_client: AutoClient,
    annotator_prompt: str,
    annotator_model: str,
    annotator_model_deployment: str,
) -> ScoreAndReasoning:
    # Makes request to judge model
    annotator_response = auto_client.make_request(annotator_request)
    annotator_response_text = annotator_response.completions[0].text
    
    # Parses structured output from judge (no execution)
    reasoning_match = re.search(
        r"<\s*reasoning\s*>(.*?)<\/?\s*reasoning\s*>", annotator_response_text, re.DOTALL | re.IGNORECASE
    )
    score_match = re.search(r"<\s*score\s*>(.*?)<\/?\s*score\s*>", annotator_response_text, re.DOTALL | re.IGNORECASE)
```
Model-as-judge evaluation extracts scoring and reasoning through regex pattern matching on text outputs, demonstrating format validation without execution.

Evidence 6: Token counting and text validation
- File: `src/helm/benchmark/window_services/test_gpt2_window_service.py`
- Code Reference:
```python
def test_tokenize_and_count(self):
    assert self.window_service.get_num_tokens(TEST_PROMPT) == 51

def test_fits_within_context_window(self):
    # Should fit in the context window
    assert self.window_service.fits_within_context_window(TEST_PROMPT, 1025 - 51)
```
Window services perform syntactic analysis including token counting, text tokenization, and context window validation without executing model outputs.

---

### Dynamic Execution

Evidence 1: Dry-run execution mode
- File: `docs/benchmark.md`
- Code Reference:
```bash
## Dry Runs

The `helm-run` provides several flags that can be used to test that the configuration and scenario are working correctly without actually sending requests to the model

    # Create the instances and the requests, but don't send requests to the model
    helm-run --conf src/helm/benchmark/presentation/run_entries_small.conf --max-eval-instances 10  --suite v1 --dry-run
```
Documents dry-run execution mode for testing configuration and scenarios, demonstrating controlled execution environments for validation.

Evidence 2: Adaptive testing execution
- File: `src/helm/benchmark/reeval_runner.py`
- Class/Function: `REEvalRunner`
- Code Reference:
```python
class REEvalRunner(Runner):
    """
    This runner implements the basic (non-amortized) method described in the paper
    `Reliable and Efficient Amortized Model-Based Evaluation`. This approach, which is
    also known as Computerized Adaptive Testing (CAT) within the framework of Item Response
    Theory (IRT), leverages adaptive testing to evaluate model performance.
    """
    
    # Execute the request
    single_scenario_state: ScenarioState = ScenarioState(
        adapter_spec=run_spec.adapter_spec,
        request_states=[selected_item],
        annotator_specs=run_spec.annotators,
    )
    
    # Execute (fill up results)
    single_scenario_state = self.executor.execute(single_scenario_state)
```
Implements adaptive testing that executes model requests in controlled manner, dynamically selecting and running evaluation items based on performance.

Evidence 3: Instance preprocessing with unique IDs
- File: `src/helm/benchmark/data_preprocessor.py`
- Code Reference:
```python
def test_data_preprocessor():
    # Test that each Instance is given a unique ID and is preserved through data augmentation
    data_preprocessor = DataPreprocessor(DataAugmenterSpec())
    scenario: Scenario = create_scenario(get_simple1_spec().scenario_spec)
    instances = with_instance_ids(scenario.get_instances(output_path=""))
    instances: List[Instance] = data_preprocessor.preprocess(instances)
```
Preprocesses evaluation instances with unique identification and data augmentation, supporting controlled execution tracking.

Evidence 4: External resource acquisition
- File: `scripts/heim_human_eval.py`
- Function: `download_image_if_not_exists()`
- Code Reference:
```python
def download_image_if_not_exists(image_url: str, local_image_path: str) -> None:
    if os.path.exists(local_image_path):
        return
    
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"Image URL {image_url} returned status code {response.status_code}.")
    with open(local_image_path, "wb") as f:
        f.write(response.content)
```
Downloads and processes external resources (images) for evaluation, demonstrating dynamic resource acquisition during execution.

Evidence 5: Multi-step execution pipeline
- File: `src/helm/benchmark/runner.py`
- Code Reference:
```python
# Execute the requests in an reeval manner
assert run_spec.adapter_spec.reeval_parameters is not None
model_ability: float = run_spec.adapter_spec.reeval_parameters.model_ability or 0.0

# Execute (fill up results)
single_scenario_state = self.executor.execute(single_scenario_state)

# Annotate (post-process the results)
single_scenario_state = self.annotator_executor.execute(single_scenario_state)
```
Core execution pipeline manages request state, executes model API calls, and coordinates post-processing with annotators.

Evidence 6: Adaptive evaluation workflow
- File: `docs/reeval.md`
- Code Reference:
```bash
# Reliable and Efficient Amortized Model-based Evaluation

python3 -m helm.benchmark.reeval_run --conf-paths $RUN_ENTRIES_CONF_PATH --num-train-trials $NUM_TRAIN_TRIALS --priority $PRIORITY --suite $SUITE_NAME --models-to-run $MODELS_TO_RUN --model-ability $MODEL_ABILITY --max-eval-instances $MAX_EVAL_INSTANCES
```
Documents execution workflow for adaptive evaluation with configurable parameters for model testing and instance selection.