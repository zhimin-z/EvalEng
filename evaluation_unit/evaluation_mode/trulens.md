## Evaluation Mode Categories

[Static Analysis, Dynamic Execution, Interactive Simulation, Custom]

## Detailed Analysis

### Static Analysis

Evidence 1: Feedback functions for evaluating LLM outputs
- File: `docs/getting_started/core_concepts/honest_harmless_helpful_evals.md`
- Code Reference:
```markdown
"At its most basic level, the AI applications should give accurate information... It should have access to retrieve and reliably use the information needed to answer questions"
```
Documents "honest" evaluations including context relevance and groundedness checking, "harmless" evaluations for safety/toxicity checking, and "helpful" evaluations for response quality.

Evidence 2: Research evaluation without execution
- File: `src/agentic_evals.py`
- Function: `research_eval_node()` (lines 31-93)
- Code Reference:
```python
def research_eval_node(state) -> Command[Literal["orchestrator"]]:
    query = state.get("user_query")
    context_list = state.get("execution_trace")[state.get("current_step")][-1]["tool_calls"]
    response = state.get("execution_trace")[state.get("current_step")][-1]["output"]
    
    provider = OpenAI(model_engine=os.environ.get("LLM_MODEL_NAME"))
    
    with st.spinner("Evaluating research..."):
        context_rel_score, context_rel_reason = provider.context_relevance_with_cot_reasons(
                question=query,
                context=context_list,
            )
        grounded_score, grounded_reason = provider.groundedness_measure_with_cot_reasons(
            source=" ".join(context_list),
            statement=response
        )
        answer_score, answer_reason = provider.relevance_with_cot_reasons(prompt=query, response=response)
```
Evaluates context relevance, groundedness, and answer relevance by analyzing model outputs. Does not execute generated code, only examines text content.

Evidence 3: Custom chart evaluation with rubrics
- File: `src/agentic_evals.py`
- Class: `CustomChartEval` (lines 116-154)
- Code Reference:
```python
class CustomChartEval(OpenAI):
    def chart_accuracy_with_cot_reasons(self, code: str, context: str) -> Tuple[float, Dict]:
        system_prompt = f"""
        Use the following rubric to evaluate chart accuracy based on context:
        0: The chart does not reflect the data, plots incorrect values/relationships, or plots hypothetical data.
        1: The chart has significant errors (e.g., wrong labels, major mismatches in data) but shows some partial attempt.
        2: The chart is mostly correct with minor, non-critical errors.
        3: The chart is completely accurate: correct data, correct relationships, correct calculations.
        """
```
Evaluates chart code accuracy and formatting through static analysis using rubrics to score code quality without execution.

---

### Dynamic Execution

Evidence 1: Test configuration for executing Python test suites
- File: `conftest.py`
- Code Reference:
```python
def pytest_addoption(parser):
    parser.addoption(
        "--skip_basic_tests",
        action="store_true",
        default=False,
        help="Skip tests not marked optional/snowflake",
    )
```
However, this is harness infrastructure testing, not benchmark evaluation.

Evidence 2: Notebook execution for testing
- File: `tests/legacy/test_trulens_eval_notebooks.py`
- Class: `PatchesPreprocessor`
- Code Reference:
```python
class PatchesPreprocessor(ExecutePreprocessor):
    """Execute a notebook but make patches to the source before doing so."""
    
    def preprocess_cell(self, cell, resources, index, **kwargs):
        first_line = cell["source"].split("\n")[0]
        print(f"  Executing cell {index}: {first_line}.")
```
Executes notebook cells containing model-generated code and validates that notebooks run successfully.

Evidence 3: Chart code execution
- File: `examples/expositional/use_cases/snowflake-ai-stack-agentic-eval/src/agentic_evals.py`
- Function: `chart_eval_node()`
- Code Reference:
```python
def chart_eval_node(state) -> Command[Literal["orchestrator"]]:
    context = state.get("execution_trace")[state.get("current_step")-1][-2]["output"]
    code = state.get("execution_trace")[state.get("current_step")][-1]["code"]
```
Evaluates generated chart code (though execution details not shown in snippet) and tests that code compiles and runs correctly.

---

### Interactive Simulation

Evidence 1: In-line evaluations during agent execution
- File: `docs/component_guides/runtime_evaluation/inline_evals.md`
- Code Reference:
```python
@inline_evaluation(f_context_relevance)
@instrument(
    span_type=SpanAttributes.SpanType.RETRIEVAL,
    attributes=lambda ret, exception, *args, **kwargs: {
        SpanAttributes.RETRIEVAL.QUERY_TEXT: args[0]["messages"][-1].content,
        SpanAttributes.RETRIEVAL.RETRIEVED_CONTEXTS: [...]
    },
)
def research_node(state: MessagesState) -> Command[Literal["chart_generator", END]]:
    result = research_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "chart_generator")
```
Evaluates agent behavior during multi-step execution and modifies agent state based on evaluation results. By adding the evaluation results to the agent's state, the agent can then use evaluation results to guide execution steps.

Evidence 2: State-based evaluation with feedback loops
- File: `src/agentic_evals.py`
- Function: `research_eval_node()` (lines 31-93)
- Code Reference:
```python
def research_eval_node(state) -> Command[Literal["orchestrator"]]:
    # ... evaluation logic ...
    
    eval_entry = {
        "step": state.get("current_step"),
        "agent": "research_eval",
        "metrics": parsed_eval,
    }
    
    return Command(
        update={
            "messages": [eval_msg],
            "execution_trace": append_to_step_trace(state, state.get("current_step"), eval_entry)
        },
        goto=goto
    )
```
Multi-turn evaluation with persistent state evolution, feedback incorporated into agent decision-making, and sequential evaluation across multiple agent steps.

Evidence 3: Tests for interactive evaluation
- File: `tests/unit/test_otel_inline_evaluations.py`
- Code Reference:
```python
def _create_and_invoke_simple_app(self, emit_spans: bool) -> pd.DataFrame:
    feedback_func = Feedback(simple_feedback).on({
        "text": Selector(span_attribute="test_output")
    })
    
    @inline_evaluation(feedback_func, emit_spans=emit_spans)
    @instrument(...)
    def simple_node(state: MessagesState) -> MessagesState:
        state["messages"].append(AIMessage("Sachiboy"))
        return state
```
Validates interactive simulation with state modification and tests feedback loop integration.

---

### Custom

Evidence 1: Domain-specific chart evaluation pipeline
- File: `src/agentic_evals.py`
- Class: `CustomChartEval` (lines 116-200)
- Code Reference:
```python
class CustomChartEval(OpenAI):
    def chart_accuracy_with_cot_reasons(self, code: str, context: str) -> Tuple[float, Dict]:
        # Custom rubric for chart accuracy
        
    def chart_formatting_with_cot_reasons(self, code: str) -> Tuple[float, Dict]:
        # Custom rubric for chart formatting
        
    def chart_relevance_with_cot_reasons(self, code: str, query: str, response: str) -> Tuple[float, Dict]:
        # Custom rubric for chart relevance
```
Specialized evaluation for chart generation tasks that combines multiple evaluation dimensions (accuracy, formatting, relevance) with domain-specific scoring rubrics.

Evidence 2: Trajectory evaluation
- File: `src/agentic_evals.py`
- Class: `CustomTrajEval` (lines 238-260)
- Code Reference:
```python
class CustomTrajEval(OpenAI):
    def traj_execution_with_cot_reasons(self, trace) -> Tuple[float, Dict]:
        system_prompt = f"""
        Use the following rubric to evaluate the execution trace of the system:
        0: Agents made wrong or unnecessary calls...
        1: Several unnecessary or misordered agent/tool use...
        2: Some minor inefficiencies or unclear transitions...
        3: Agent handoffs were well-timed and logical...
        """
```
Custom evaluation of multi-agent execution trajectories representing a novel approach combining multiple interaction types.

Evidence 3: "Honest, Harmless, Helpful" framework
- File: `docs/getting_started/core_concepts/honest_harmless_helpful_evals.md`
- Code Reference:
```markdown
"TruLens adapts 'honest, harmless, helpful' as desirable criteria for LLM apps from Anthropic"
```
Custom evaluation philosophy adapted from Anthropic, representing a hybrid approach combining multiple evaluation categories.