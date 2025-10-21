## Evaluator Categories

[ML-based, Environmental, Algorithmic, Custom]

## Detailed Analysis

### ML-based

Evidence 1: LLM-based evaluation approach documentation
- File: `docs/getting_started/core_concepts/honest_harmless_helpful_evals.md`
- Code Reference:
```markdown
LLM-based evaluation and feedback function definitions
Evaluation criteria for LLM apps
```
The documentation establishes the framework for using LLM-based evaluation approaches, defining how large language models serve as judges for assessing application outputs. This sets the conceptual foundation for ML-based evaluation throughout the harness.

Evidence 2: OpenAI LLM as evaluator with chain-of-thought reasoning
- File: `src/agentic_evals.py`
- Code Reference (lines 17-19, 83-143):
```python
from trulens.providers.openai import OpenAI

provider = OpenAI(model_engine=os.environ.get("LLM_MODEL_NAME"))

context_rel_score, context_rel_reason = provider.context_relevance_with_cot_reasons(
    question=query,
    context=context_list,
)
```
The harness extensively uses LLM models (specifically OpenAI) as judges to evaluate model outputs. These are trained neural networks that provide scoring and reasoning for various quality metrics like relevance, groundedness, and answer relevance. The implementation employs chain-of-thought reasoning, allowing the evaluator to provide both numerical scores and explanatory reasoning for its assessments.

Evidence 3: Custom ML-based evaluators for specialized domains
- File: `src/agentic_evals.py`
- Class: `CustomChartEval`
- Code Reference (lines 153-200):
```python
class CustomChartEval(OpenAI):
    def chart_accuracy_with_cot_reasons(self, code: str, context: str) -> Tuple[float, Dict]:
    def chart_formatting_with_cot_reasons(self, code: str) -> Tuple[float, Dict]:
    def chart_relevance_with_cot_reasons(self, code: str, query: str, response: str) -> Tuple[float, Dict]:
```
Custom ML-based evaluators extend the OpenAI provider to create domain-specific assessment capabilities for chart evaluation. These specialized evaluators inherit the neural network-based judgment capabilities while adding tailored evaluation logic for visual data representation quality.

Evidence 4: Test infrastructure for ML-based feedback
- File: `tests/unit/test_otel_feedback.py`
- Code Reference (lines 11-18):
```python
def _mock_feedback_function_1(self, x: str) -> float:
```
The test infrastructure validates ML-based feedback functions, ensuring that the neural network evaluators can be properly integrated and tested within the harness. This demonstrates the systematic approach to verifying ML-based evaluation mechanisms.

---

### Environmental

Evidence 1: Inline evaluation during execution
- File: `docs/component_guides/runtime_evaluation/inline_evals.md`
- Code Reference:
```markdown
In-line evaluations allow you to assess and score agent behavior as it happens—directly within the execution flow
Real-time feedback from agent execution environment
```
The documentation describes how the harness evaluates model outputs based on real-time feedback from the execution environment. This enables assessment during actual runtime rather than post-hoc analysis, capturing environmental signals as they occur during agent operation.

Evidence 2: Vector store search results for retrieval quality
- File: `examples/expositional/use_cases/snowflake-ai-stack/src/retrieval.py`
- Function: `search()`
- Code Reference (lines 48-62):
```python
def search(self, query, k=5):
    """Perform a similarity search on the vector store using the query and return LangChain documents."""
    query_embedding = self.embeddings.embed_query(query)
    results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
```
The harness evaluates model outputs based on execution results from runtime environments, specifically vector stores that provide similarity search results. These are external system responses that validate model task performance in information retrieval scenarios, demonstrating environmental feedback as an evaluation signal.

Evidence 3: Runtime execution traces as evaluation input
- File: `src/agentic_evals.py`
- Code Reference (lines 83-91, 131-138):
```python
context_list = state.get("execution_trace")[state.get("current_step")][-1]["tool_calls"]
response = state.get("execution_trace")[state.get("current_step")][-1]["output"]
```
Evaluation uses runtime execution traces from the agent's environment, capturing tool call results and outputs directly from the execution flow. These environmental signals—including what tools were invoked and what they returned—provide concrete evidence of agent behavior and performance during actual system interaction.

---

### Algorithmic

Evidence 1: Exact match and numerical comparison functions
- File: `tests/test.py`
- Function: `assertJSONEqual()`
- Code Reference (lines 115-248):
```python
def assertJSONEqual(
    self,
    j1: serial_utils.JSON,
    j2: serial_utils.JSON,
    ...
    numeric_places: int = 7,
):
    if isinstance(j1, (int, float)):
        self.assertAlmostEqual(j1, j2, places=numeric_places, msg=ps)
```
The harness uses deterministic algorithmic functions for evaluation, including exact matching for structural equality and numerical tolerance comparisons for floating-point values. These are mathematical rules that provide reproducible, consistent assessment without any learned components.

Evidence 2: DataFrame comparison with tolerance-based matching
- File: `tests/util/df_comparison.py`
- Function: `compare_dfs_accounting_for_ids_and_timestamps()`
- Code Reference:
```python
compare_dfs_accounting_for_ids_and_timestamps(
    self,
    expected,
    actual,
    ignore_locators=ignore_locators,
    timestamp_tol=pd.Timedelta("0.02s"),
)
```
Structured data comparison using algorithmic tolerance thresholds for timestamps and identifier matching demonstrates deterministic evaluation logic. The function applies predefined rules to assess whether dataframes match within specified tolerances, providing systematic validation of tabular outputs.

Evidence 3: Regex-based pattern matching for score extraction
- File: `tests/unit/test_feedback_score_generation.py`
- Function: `test_re_0_10_rating()`
- Code Reference (lines 10-34):
```python
test_data = [
    ("The relevance score is 7.", 7),
    ("I rate this an 8 out of 10.", 8),
]

def test_re_0_10_rating(test_input, expected):
    result = feedback_generated.re_0_10_rating(test_input)
```
The harness employs regex-based pattern matching to extract numerical scores from text responses. This algorithmic approach uses deterministic string parsing rules rather than learned models, providing consistent and reproducible score extraction from evaluation outputs.

---

### Custom

Evidence 1: Domain-specific chart evaluation with custom rubrics
- File: `src/agentic_evals.py`
- Class: `CustomChartEval`
- Code Reference (lines 153-200):
```python
class CustomChartEval(OpenAI):
    def chart_accuracy_with_cot_reasons(self, code: str, context: str) -> Tuple[float, Dict]:
        system_prompt = f"""
        Use the following rubric to evaluate chart accuracy based on context:
        0: The chart does not reflect the data...
        3: The chart is completely accurate...
        """
```
The harness implements specialized evaluation mechanisms that extend standard ML-based evaluators with domain-specific logic for chart visualization assessment. By combining the neural network judgment capabilities of OpenAI models with carefully crafted rubrics for chart accuracy, formatting, and relevance, this creates a custom evaluator tailored to visual data representation quality.

Evidence 2: Trajectory evaluation combining execution analysis with LLM judgment
- File: `src/agentic_evals.py`
- Class: `CustomTrajEval`
- Code Reference (lines 212-235):
```python
class CustomTrajEval(OpenAI):
    def traj_execution_with_cot_reasons(self, trace) -> Tuple[float, Dict]:
        system_prompt = f"""
        Use the following rubric to evaluate the execution trace of the system:
        0: Agents made wrong or unnecessary calls...
        3: Agent handoffs were well-timed and logical...
        """
```
Custom trajectory evaluation represents a hybrid approach that combines execution trace analysis (environmental feedback) with LLM-based judgment (ML-based evaluation). This multi-stage evaluation assesses agent orchestration quality by examining the sequence of actions and decisions, demonstrating how custom evaluators can integrate multiple evaluation paradigms for complex assessment tasks.

Evidence 3: Hybrid evaluation with instrumentation and feedback functions
- File: `docs/component_guides/runtime_evaluation/inline_evals.md`
- Code Reference (lines 39-73):
```python
@inline_evaluation(f_context_relevance)
@instrument(
    span_type=SpanAttributes.SpanType.RETRIEVAL,
    attributes=lambda ret, exception, *args, **kwargs: {...}
)
def research_node(state: MessagesState):
```
The harness provides a custom pipeline that integrates runtime tracing with evaluation feedback functions. By combining instrumentation decorators (which capture environmental execution data) with inline evaluation decorators (which apply assessment functions), this creates a unified evaluation framework that simultaneously monitors and assesses agent behavior during execution.

Evidence 4: Custom evaluation pipeline with golden file comparison
- File: `tests/util/otel_test_case.py`
- Function: `_compare_events_to_golden_dataframe()`
- Code Reference (lines 49-83):
```python
def _compare_events_to_golden_dataframe(
    self,
    golden_filename: str,
    ignore_locators: Optional[List[str]] = None,
    regex_replacements: Optional[List[Tuple[str, str]]] = None,
):
```
Custom evaluation mechanisms that combine golden file comparison (algorithmic evaluation against reference outputs) with regex transformations (preprocessing for normalization) demonstrate specialized evaluation pipelines. This approach addresses unique testing requirements by chaining multiple evaluation techniques into a custom workflow that cannot be satisfied by any single standard evaluator category.