## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text comparison and statistical scoring methods
- File: `deepeval/scorer/scorer.py`
- Functions: `rouge_score()`, `sentence_bleu_score()`, `exact_match_score()`, `quasi_exact_match_score()`
- Code Reference:
```python
def exact_match_score():
    return 1 if prediction.strip() == target.strip() else 0
```
The scorer module implements multiple text-based evaluation methods that operate through direct string comparison and statistical analysis. The `rouge_score()` function calculates ROUGE scores by comparing target and prediction strings using statistical n-gram analysis, while `sentence_bleu_score()` computes BLEU scores through n-gram matching. The `exact_match_score()` performs direct string comparison, and `quasi_exact_match_score()` uses text normalization. These methods exemplify static analysis by examining output quality without executing any generated artifacts, providing fast evaluation focused on textual similarity and overlap.

Evidence 2: Semantic embedding-based analysis
- File: `deepeval/scorer/scorer.py`
- Functions: `bert_score()`, `answer_relevancy_score()`, `truth_identification_score()`
- Code Reference:
```python
def bert_score():
    # Uses BERTScore model to compare embeddings
def answer_relevancy_score():
    # Semantic similarity scoring using sentence transformers
```
These functions extend static analysis beyond surface-level text comparison to semantic understanding. The `bert_score()` method uses BERTScore models to compare text embeddings semantically, while `answer_relevancy_score()` employs sentence transformers for similarity scoring. The `truth_identification_score()` parses and compares lists from strings. All methods analyze text semantically without executing model outputs, demonstrating that static analysis can encompass both syntactic and semantic evaluation dimensions.

Evidence 3: LLM-based evaluation of test cases
- File: `deepeval/metrics/g_eval/g_eval.py`
- Class/Function: `GEval.measure()`, `GEval.a_measure()`, `GEval._evaluate()`
- Code Reference:
```python
def measure():
    # Evaluates test cases by analyzing model outputs against criteria
def _evaluate():
    # Constructs prompts to analyze test case content and generates scores/reasons
```
The `GEval` class processes `LLMTestCase` objects containing input, actual output, expected output, and context fields. The evaluation methods use an LLM to generate scores and reasoning based on predefined evaluation steps and criteria. The `_evaluate()` method constructs analytical prompts from test case content to produce scores and explanations. This demonstrates static analysis through LLM-powered assessment that examines output quality against criteria without executing generated artifacts.

Evidence 4: Conversational turn analysis
- File: `deepeval/metrics/conversational_g_eval/conversational_g_eval.py`
- Class/Function: `ConversationalGEval.measure()`, `ConversationalGEval.evaluate()`
- Code Reference:
```python
def evaluate():
    # Constructs prompts from test case content and generates scores
    self.score = float(g_score) / 10
```
The `ConversationalGEval` class extends static analysis to conversational contexts by analyzing conversation turns through LLM evaluation. The `measure()` and `a_measure()` methods process conversational test cases, while `evaluate()` constructs prompts from conversation content to generate normalized scores. This shows how static analysis adapts to sequential conversational data while maintaining the core principle of examining outputs without execution.

Evidence 5: Comparative output analysis
- File: `deepeval/metrics/arena_g_eval/arena_g_eval.py`
- Class/Function: `ArenaGEval.measure()`, `ArenaGEval._compare()`
- Code Reference:
```python
def _compare():
    # Formats test cases and determines winner through analysis
    # Returns winner determination without executing model-generated code
```
The `ArenaGEval` class implements head-to-head comparison of multiple model outputs through static analysis. The `measure()` and `a_measure()` methods compare outputs, while `_compare()` formats test cases and determines winners through analytical evaluation. The winner determination occurs purely through output inspection without executing any model-generated code, exemplifying comparative static analysis.

Evidence 6: MCP primitive usage validation
- File: `deepeval/metrics/mcp_use_metric/mcp_use_metric.py`
- Class/Function: `MCPUseMetric.measure()`, `MCPUseMetric._get_primitives_used_score()`, `MCPUseMetric._get_argument_correctness_score()`
- Code Reference:
```python
def measure():
    # Evaluates MCP (Model Context Protocol) primitive usage
def _get_primitives_used_score():
    # Inspects mcp_tools_called, mcp_resources_called, mcp_prompts_called
```
The `MCPUseMetric` class analyzes MCP primitive usage by inspecting tool, resource, and prompt calls without executing them. The scoring methods evaluate correctness of primitive selection and argument generation through validation logic. This demonstrates domain-specific static analysis that assesses whether model outputs correctly specify tool usage patterns without actually invoking those tools.

Evidence 7: Multimodal content analysis
- File: `deepeval/metrics/multimodal_metrics/multimodal_g_eval/multimodal_g_eval.py`
- Class/Function: `MultimodalGEval.measure()`, `MultimodalGEval._evaluate()`
- Code Reference:
```python
def measure():
    # Evaluates multimodal test cases (text + images)
def _evaluate():
    # Generates scores based on criteria without executing model outputs
```
The `MultimodalGEval` class extends static analysis to multimodal inputs by evaluating test cases containing both text and images. The evaluation methods construct test case representations and use LLM analysis to generate scores based on predefined criteria. This demonstrates that static analysis can handle diverse input modalities while maintaining the core principle of assessment without execution.

Evidence 8: Multi-turn MCP interaction analysis
- File: `deepeval/metrics/mcp/multi_turn_mcp_use_metric.py`
- Class/Function: `MultiTurnMCPUseMetric.measure()`, `MultiTurnMCPUseMetric._get_tool_accuracy_score()`, `MultiTurnMCPUseMetric._get_args_score()`
- Code Reference:
```python
def measure():
    # Evaluates multi-turn MCP interactions
def _get_tool_accuracy_score():
    # Analyzes tool usage across conversation turns
```
The `MultiTurnMCPUseMetric` class processes multi-turn interactions by analyzing tool usage patterns across conversation sequences. The scoring methods validate primitive usage through accuracy and argument correctness checks across unit interactions. This shows how static analysis scales to sequential interaction patterns while maintaining validation through inspection rather than execution.

Evidence 9: Test run aggregation and result presentation
- File: `deepeval/test_run/test_run.py`
- Functions: `display_results_table()`, `construct_metrics_scores()`, `calculate_test_passes_and_fails()`
- Code Reference:
```python
def display_results_table():
    # Formats and presents evaluation results
def construct_metrics_scores():
    # Constructs metrics scores from test case data
def calculate_test_passes_and_fails():
    # Analyzes test case success states
```
The test run management system aggregates results from static analysis metrics by constructing score summaries, calculating pass/fail counts, and formatting results for presentation. These orchestration functions analyze test case outcomes and metric scores without executing any model-generated artifacts. This demonstrates how static analysis extends to the evaluation framework level, providing infrastructure for result aggregation and reporting based on inspection-based assessment.