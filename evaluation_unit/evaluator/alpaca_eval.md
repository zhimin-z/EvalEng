## Evaluator Categories

[ML-based, Human]

## Detailed Analysis

### ML-based

Evidence 1: GPT-4 evaluation prompt templates
- File: `src/alpaca_eval/evaluators_configs/alpaca_eval_gpt4/alpaca_eval.txt`
- Code Reference:
```
Prompt templates for GPT-4 evaluation
```
This configuration file contains prompt templates that instruct GPT-4 on how to evaluate and compare model outputs, establishing it as an ML-based judge in the evaluation framework.

Evidence 2: GPT-4 Turbo function calling template
- File: `src/alpaca_eval/evaluators_configs/alpaca_eval_gpt4_turbo_fn/alpaca_eval_fn.txt`
- Code Reference:
```
GPT-4 Turbo function calling template
```
This template enables GPT-4 Turbo to perform structured evaluation using function calling capabilities, providing a more programmatic approach to ML-based evaluation.

Evidence 3: Llama3 70B model evaluation template
- File: `src/alpaca_eval/evaluators_configs/alpaca_eval_llama3_70b_fn/alpaca_eval_fn.txt`
- Code Reference:
```
Llama3 70B model evaluation template
```
This configuration demonstrates the framework's support for open-source LLM judges, extending beyond proprietary models to include Llama3-70B as an evaluator.

Evidence 4: GPT-4 Turbo classification-based evaluation
- File: `src/alpaca_eval/evaluators_configs/alpaca_eval_clf_gpt4_turbo/alpaca_eval_clf.txt`
- Code Reference:
```
GPT-4 Turbo classification-based evaluation
```
This template implements a classification approach to evaluation, where GPT-4 Turbo categorizes and scores outputs rather than using open-ended generation.

Evidence 5: Pairwise evaluation orchestration classes
- File: `src/alpaca_eval/annotators/pairwise_evaluator.py`
- Class/Function: `PairwiseAnnotator` and `SinglePairwiseAnnotator`
- Code Reference:
```python
# Classes that handle LLM-based evaluation
class PairwiseAnnotator:
    # Coordinates multiple LLM judges
    
class SinglePairwiseAnnotator:
    # Handles individual LLM evaluation instances
```
This repository implements an LLM-as-judge evaluation framework where these classes coordinate the use of large language models (GPT-4, GPT-4 Turbo, Llama3-70B, Claude) to evaluate and rank model outputs. The evaluator configuration files contain prompt templates that instruct these ML models to assess response quality by comparing pairs of outputs. The `PairwiseAnnotator` classes orchestrate these LLM judges to generate preference annotations, calling the models via APIs (OpenAI, Anthropic, etc., as evidenced by `src/alpaca_eval/decoders/`) to score benchmark task outputs, establishing them as ML-based evaluators.

---

### Human

Evidence 1: Human preference annotations as gold standard
- File: `src/alpaca_eval/analyze.py`
- Class/Function: `Analyzer.__init__()`
- Code Reference:
```python
def __init__(
    self,
    gold_crossannotations: Union[AnyPath, AnyData, Callable] = constants.ALPACAFARM_GOLD_CROSSANNOTATIONS,
    gold_annotations: Optional[Union[AnyPath, AnyData, Callable]] = constants.ALPACAFARM_GOLD_ANNOTATIONS,
    ...
):
```
The `Analyzer` class loads human cross-annotations and annotations as gold standard references for evaluation. These parameters point to datasets containing human preference judgments that serve as ground truth for measuring automated evaluator quality.

Evidence 2: Gold annotation constants
- File: `src/alpaca_eval/constants.py`
- Code Reference:
```python
ALPACAFARM_GOLD_CROSSANNOTATIONS
ALPACAFARM_GOLD_ANNOTATIONS
```
These constants reference the canonical human annotation datasets used throughout the framework, establishing centralized access to human evaluation data.

Evidence 3: Human annotation data structure
- File: `tests/test_analyze.py`
- Code Reference:
```python
RECORDS = {
    "preference": ...,  # 1 or 2 indicating which output humans preferred
    "annotator_index": ...,  # Identifying different human annotators
    "time_per_example": ...,
    "price_per_example": ...
}
```
Test data reveals the structure of human annotations, including preference labels (1 or 2 indicating which output humans preferred), annotator identifiers to track different human judges, and metadata about annotation time and cost. This structure supports multi-annotator analysis and agreement calculations.

Evidence 4: Human-model agreement comparison
- File: `src/alpaca_eval/analyze.py`
- Function: `Analyzer.agreement_of_annotations()`
- Code Reference:
```python
def agreement_of_annotations(self, annotations, ...):
    # Compares model annotations against human gold standard
```
The repository uses human annotations as the gold standard for evaluation quality. This method measures agreement between automated evaluator judgments and human preferences, computing metrics like "Human agreement" (as seen in the `get_metrics_evaluator()` function) to assess how well ML-based evaluators align with human judgment. This comparison framework establishes human evaluation as a core evaluator category in the harness, serving as the ultimate benchmark for validating automated evaluation approaches.