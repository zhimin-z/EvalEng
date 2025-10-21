## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text-based preference annotation without execution
- File: `src/alpaca_eval/annotators/pairwise_evaluator.py`
- Classes/Functions: `PairwiseAnnotator`, `SinglePairwiseAnnotator`, `annotate_pairs()`, `annotate_head2head()`
- Code Reference:
```python
def annotate_pairs(...):
    # Processes examples containing "output_1" and "output_2" keys
    # Returns "preference" values (1, 1.5, or 2)
    pass

def annotate_head2head(
    self,
    outputs_1: Union[Sequence[dict[str, Any]], pd.DataFrame],
    outputs_2: Union[Sequence[dict[str, Any]], pd.DataFrame],
    ...
) -> list[dict[str, Any]]:
    """Head-to-head comparison between two sequence of outputs."""
```
The core evaluation mechanism in AlpacaEval compares model-generated text outputs through LLM-based preference judgments. The system takes two text outputs (`output_1` and `output_2`) and determines which is preferred without executing any code. The annotations are purely textual comparisons: the `annotate_pairs()` method processes examples containing `"output_1"` and `"output_2"` keys, returns `"preference"` values (1, 1.5, or 2) indicating which output is preferred, and no execution of model outputs occurs - only textual inspection and comparison.

Evidence 2: Preference scoring and agreement metrics
- File: `src/alpaca_eval/analyze.py`
- Classes/Functions: `Analyzer` class, `agreement_of_annotations()`, `get_length_biases()`, `get_list_biases()`
- Code Reference:
```python
def agreement_of_annotations(...):
    # Compares preference labels between annotators using scoring rules
    pass

def get_length_biases(
    self, annotations: Union[pd.DataFrame, str], significant_delta_length: int = 30
) -> dict[str, float]:
    """Estimate the biases for longer sentences."""
    df["best_output_length"] = df["best_output"].apply(len)
    df["worse_output_length"] = df["worse_output"].apply(len)
    pass

def get_list_biases(self, annotations: Union[pd.DataFrame, str]) -> dict[str, float]:
    """Estimate the biases for sentences with lists."""
    df["is_best_list"] = df["best_output"].apply(utils.contains_list)
    df["is_worse_list"] = df["worse_output"].apply(utils.contains_list)
```
The analysis module performs static inspection of annotations: `agreement_of_annotations()` compares preference labels between annotators using scoring rules (zero_one, absolute, squared), `get_length_biases()` analyzes text length patterns in preferences by comparing string lengths, `get_list_biases()` detects list formatting patterns using `utils.contains_list()` which performs regex/pattern matching, and all operations involve parsing and comparing text properties without execution.

Evidence 3: Regex-based completion parsing
- File: `src/alpaca_eval/annotators/pairwise_evaluator.py`
- Parameter: `fn_completion_parser`
- Code Reference:
```python
fn_completion_parser: Optional[Union[Callable, str]] = "regex_parser"
```
The evaluator uses regex parsing to extract preferences from LLM completions. This is a form of pattern matching on text outputs to extract structured information (the preference label), demonstrating that the system analyzes textual patterns rather than executing code.

Evidence 4: Output format validation and structure checking
- File: `src/alpaca_eval/evaluators_configs/alpaca_eval_gpt4/alpaca_eval.txt` (and other evaluator configs)
- Content: Prompts requesting structured outputs
- Code Reference:
```
Your response must be a valid Python dictionary
```
The evaluation prompts explicitly request structured outputs (Python dictionaries, JSON) which are then parsed and validated. The system checks output structure and format without executing the content: prompts request "Your response must be a valid Python dictionary" and the framework parses these structured responses to extract preference information through static inspection.

Evidence 5: Test suite for annotation agreement
- File: `tests/test_analyze.py`
- Functions: `test_agreement_of_annotations()`, `test_get_length_biases()`, `test_get_list_biases()`
- Code Reference:
```python
def test_agreement_of_annotations():
    # Creates mock DataFrames with preference labels
    # Computes agreement scores by comparing label values
    pass

def test_get_length_biases():
    # Analyzes length biases through text property inspection
    pass

def test_get_list_biases():
    # Tests list formatting bias detection
    pass
```
Tests demonstrate the static analysis nature of evaluation: they create mock DataFrames with preference labels, compute agreement scores by comparing label values, analyze length and list formatting biases through text property inspection, and demonstrate that no execution of any generated code or artifacts occurs.

Evidence 6: Correlation and bias analysis
- File: `src/alpaca_eval/analyze.py`
- Functions: `estimate_correlations()`, `estimate_bias()`, `estimate_variance()`
- Code Reference:
```python
def estimate_correlations():
    # Computes Spearman and Pearson correlations between win rates
    pass

def estimate_bias():
    # Analyzes bias in annotations
    pass

def estimate_variance():
    # Estimates variance of annotations
    pass
```
These methods perform statistical analysis on annotation data: `estimate_correlations()` computes Spearman and Pearson correlations between win rates, operations involve aggregating preference scores and computing metrics, and all analysis is on collected annotations, not on executing model outputs.

Evidence 7: Win rate computation
- File: `src/alpaca_eval/analyze.py`
- Function: Win rate aggregation
- Code Reference:
```python
leaderboard_1 = (
    annotations_1.groupby(groupby)[self.annotation_key]
    .aggregate(self.scoring_rule.generalized_win_rate)
    .rename("win_rate_1")
)
```
Win rates are computed by aggregating preference annotations through grouping and scoring rules. This is pure statistical analysis of annotation data without any execution, demonstrating that the evaluation framework operates entirely on static comparison of text outputs and computed preference metrics.