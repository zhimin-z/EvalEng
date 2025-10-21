# Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text normalization and pattern matching
- File: `docs/quoted_spans_metric.md`
- Code Reference: Description of `citation_alignment_quoted_spans` metric
- Justification: This metric performs text normalization and pattern matching on model outputs without execution. It searches for quoted spans in model answers and checks if they appear verbatim in source documents through string comparison. The implementation normalizes text by collapsing whitespace and lower-casing, ignores spans shorter than three words by default, and outputs a score based on matching quoted spans to sources. This is purely syntactic analysis of text outputs without running any generated code.

Evidence 2: Statistical text comparison
- File: `docs/getstarted/rag_eval.md`
- Code Reference: `BleuScore` metric usage example
```python
from ragas.metrics import BleuScore
metric = BlueScore()
metric.single_turn_score(test_data)
```
BleuScore performs statistical text comparison between response and reference without execution of model-generated artifacts, only text similarity scoring. It is described as "A non-LLM metric" that operates on text structure.

Evidence 3: LLM-based criteria evaluation
- File: `docs/getstarted/rag_eval.md`
- Code Reference: `AspectCritic` metric with LLM-based evaluation
```python
from ragas.metrics import AspectCritic
metric = AspectCritic(name="summary_accuracy", llm=evaluator_llm, definition="Verify if the summary is accurate.")
await metric.single_turn_ascore(test_data)
```
This metric uses an LLM to evaluate responses against criteria without executing them. It evaluates text quality through inspection and judgment, returns binary pass/fail based on criteria evaluation, with no execution of generated content.

Evidence 4: Conversation completeness analysis
- File: `docs/howtos/applications/evaluating_multi_turn_conversations.md`
- Code Reference: Multiple AspectCritic implementations for conversation evaluation
```python
definition = "Return 1 if the AI completes all Human requests fully without any rerequests; otherwise, return 0."
aspect_critic = AspectCritic(name="forgetfulness_aspect_critic", definition=definition, llm=evaluator_llm)
```
Demonstrates various text-based evaluation criteria including conversation completeness through text analysis, tone consistency checks (Japanese vs Mexican politeness), and brand voice alignment validation through text inspection. All evaluations inspect message content without executing any code.

Evidence 5: Tool call pattern validation
- File: `docs/howtos/integrations/_langgraph_agent_evaluation.md`
- Code Reference: `ToolCallAccuracy` and `AgentGoalAccuracyWithReference` metrics
```python
from ragas.metrics import ToolCallAccuracy
tool_accuracy_scorer = ToolCallAccuracy()
await tool_accuracy_scorer.multi_turn_ascore(sample)
```
These metrics analyze agent interactions through comparison and validation. They compare actual tool calls against reference tool calls and validate if agent achieved stated goals through text inspection, with no execution of the tools themselves—only validation of call patterns through pattern matching and structural comparison.

Evidence 6: Agent interaction sequence validation
- File: `docs/howtos/integrations/swarm_agent_evaluation.md`
- Code Reference: Agent interaction evaluation with tool call validation
```python
sample = MultiTurnSample(
    user_input=shipment_update_ragas_trace,
    reference_tool_calls=[
        ToolCall(name="transfer_to_tracker_agent", args={}),
        ToolCall(name="track_order", args={"order_id": "3000"}),
        ToolCall(name="case_resolved", args={})
    ]
)
tool_accuracy_scorer = ToolCallAccuracy()
await tool_accuracy_scorer.multi_turn_ascore(sample)
```
Validates tool call sequences against expected patterns and checks goal achievement through comparison. No execution of actual customer service tools occurs, only analysis of interaction patterns.

Evidence 7: Custom text-based metric framework
- File: `docs/howtos/customizations/metrics/_write_your_own_metric.md`
- Code Reference: Custom hallucination metric implementation
```python
from ragas.metrics import AspectCritic, RubricsScore
hallucinations_binary = AspectCritic(
    name="hallucinations_binary",
    definition="Did the model hallucinate or add any information that was not present in the retrieved context?",
    llm=evaluator_llm
)
```
Shows framework for creating text-based evaluation metrics that evaluate factual consistency through text comparison. Rubric-based scoring analyzes response quality on 1-5 scale, with all metrics inspecting text outputs without execution.

Evidence 8: Prompt-based evaluation structure
- File: `docs/howtos/customizations/metrics/_modifying-prompts-metrics.md`
- Code Reference: Prompt modification for metrics
```python
from ragas.metrics._simple_criteria import SimpleCriteriaScoreWithReference
scorer = SimpleCriteriaScoreWithReference(name="random", definition="some definition")
prompts = scorer.get_prompts()
```
Demonstrates how metrics use prompts to analyze outputs. Metrics use structured prompts to evaluate text responses with evaluation based on matching criteria and examples, with no execution involved.

Evidence 9: JSON output validation
- File: `docs/howtos/applications/benchmark_llm.md`
- Code Reference: Discount calculation accuracy evaluation
```python
@discrete_metric(name="discount_accuracy", allowed_values=["correct", "incorrect"])
def discount_accuracy(prediction: str, expected_discount):
    parsed_json = json.loads(prediction)
    predicted_discount = parsed_json.get("discount_percentage")
    expected_discount_int = int(expected_discount)
    
    if predicted_discount == expected_discount_int:
        return MetricResult(value="correct", reason=f"Correctly calculated discount={expected_discount_int}%")
```
Evaluates model outputs through JSON parsing and comparison. Parses JSON output and compares values with no execution of discount calculation logic, only validation of final output through static comparison.

Evidence 10: Retrieval quality assessment
- File: `docs/howtos/applications/compare_embeddings.md`
- Code Reference: Context precision and recall metrics
```python
from ragas.metrics import context_precision, context_recall
metrics = [context_precision, context_recall]
result = evaluate(query_engine, metrics, test_questions, test_answers)
```
Evaluates retrieval quality through comparison metrics. Measures retrieval accuracy through statistical comparison with no execution of retrieved documents, only quality assessment and pattern matching between retrieved contexts and expected answers.