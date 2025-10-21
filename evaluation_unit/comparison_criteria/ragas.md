## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, None, Custom]

## Detailed Analysis

### Explicit Labels

Evidence 1: RAG Reference Answers
- File: `docs/getstarted/rag_eval.md`
- Code Reference: Dataset structure showing expected outputs
```python
dataset = []
for query,reference in zip(sample_queries,expected_responses):
    dataset.append({
        "user_input":query,
        "retrieved_contexts":relevant_docs,
        "response":response,
        "reference":reference  # Explicit reference answer
    })
```
The evaluation dataset includes a `reference` field containing expected outputs. These predetermined correct answers serve as explicit ground truth for comparing model-generated responses.

Evidence 2: Expected Discount Values
- File: `docs/howtos/applications/benchmark_llm.md`
- Code Reference: `expected_discount` field in evaluation dataset
```markdown
| Customer Profile | Expected Discount | Description |
|------------------|-------------------|-------------|
| Martha is a 70-year-old retiree... | 15 | Senior only |
```
Evaluation datasets contain `expected_discount` values serving as explicit labels. These predetermined correct values provide static reference standards for validating model predictions.

Evidence 3: Agent Reference Labels
- File: `docs/howtos/integrations/_langgraph_agent_evaluation.md`
- Code Reference: `reference` parameter
```python
sample = MultiTurnSample(
    user_input=ragas_trace,
    reference="Price of 10 grams of silver",  # Explicit reference
)
```
The `AgentGoalAccuracyWithReference` metric explicitly uses reference labels as ground truth. These static reference answers provide comparison targets for evaluating agent outputs.

---

### Behavioral Specification

Evidence 1: Tool Call Validation
- File: `docs/howtos/integrations/_langgraph_agent_evaluation.md`
- Code Reference: `reference_tool_calls` with expected tool behavior
```python
sample = MultiTurnSample(
    user_input=ragas_trace,
    reference_tool_calls=[
        r.ToolCall(name="get_metal_price", args={"metal_name": "copper"})
    ],  # Behavioral specification of expected tool usage
)

tool_accuracy_scorer = ToolCallAccuracy()
await tool_accuracy_scorer.multi_turn_ascore(sample)
```
Validates functional correctness by checking whether the agent correctly identified and used the necessary tools with correct parameters. This executable specification verifies behavioral patterns in model outputs.

Evidence 2: Refusal Behavior Validation
- File: `docs/howtos/customizations/metrics/_write_your_own_metric_advanced.md`
- Code Reference: `RefusalPrompt` class for validation
```python
class RefusalPrompt(PydanticPrompt[RefusalInput, RefusalOutput]):
    instruction = "Given a user input and LLM response, output True if the request was refused by the LLM"
```
Implements executable specification validating whether the model's behavior (refusing requests) matches expected behavioral patterns. This dynamic validation mechanism assesses functional correctness beyond static comparison.

---

### None

Evidence 1: Aspect-Based Evaluation
- File: `docs/getstarted/evals.md`
- Code Reference: `AspectCritic` metric without reference
```python
test_data = {
    "user_input": "summarise given text\n...",
    "response": "The company experienced an 8% increase...",
    # No reference field needed
}
metric = AspectCritic(name="summary_accuracy", llm=evaluator_llm, 
                      definition="Verify if the summary is accurate.")
await metric.single_turn_ascore(test_data)
```
The `AspectCritic` metric evaluates quality based solely on the response itself without external references. This intrinsic assessment measures properties inherent to the output.

Evidence 2: Binary Pass/Fail Evaluation
- File: `docs/howtos/applications/evaluating_multi_turn_conversations.md`
- Code Reference: Binary evaluations without external references
```python
definition = "Return 1 if the AI completes all Human requests fully without any rerequests; otherwise, return 0."
aspect_critic = AspectCritic(
    name="forgetfulness_aspect_critic",
    definition=definition,  # Intrinsic property evaluation
    llm=evaluator_llm,
)
```
Binary metrics evaluate behavior without external references by assessing intrinsic properties like completeness and consistency. These reference-free measures assess quality through internal coherence.

Evidence 3: Citation Alignment Measurement
- File: `docs/quoted_spans_metric.md`
- Code Reference: `citation_alignment_quoted_spans` metric
```python
{
  "citation_alignment_quoted_spans": float,  # self-contained quality measure
  "matched": float,
  "total": float
}
```
Measures intrinsic properties of citation alignment without requiring external ground truth. This self-contained quality measure assesses internal consistency between claims and citations.

---

### Custom

Evidence 1: Composite Hallucination Metric
- File: `docs/howtos/customizations/metrics/_write_your_own_metric.md`
- Code Reference: Custom `HallucinationsMetric` combining multiple approaches
```python
@dataclass
class HallucinationsMetric(MetricWithLLM, SingleTurnMetric):
    def __post_init__(self):
        self.faithfulness_metric = Faithfulness(llm=self.llm)
    
    async def _single_turn_ascore(self, sample: SingleTurnSample, callbacks: Callbacks) -> float:
        faithfulness_score = await self.faithfulness_metric.single_turn_ascore(sample, callbacks)
        return 1 - faithfulness_score  # Custom combination logic
```
Creates composite metric combining multiple evaluation approaches with custom transformation logic. This hybrid system integrates faithfulness assessment with domain-specific scoring rules.

Evidence 2: Domain-Specific Discount Validation
- File: `docs/howtos/applications/benchmark_llm.md`
- Code Reference: `discount_accuracy` custom metric
```python
@discrete_metric(name="discount_accuracy", allowed_values=["correct", "incorrect"])
def discount_accuracy(prediction: str, expected_discount):
    """Check if the discount prediction is correct."""
    # Custom domain-specific validation logic
    parsed_json = json.loads(prediction)
    predicted_discount = parsed_json.get("discount_percentage")
    # ... custom comparison logic
```
Implements domain-specific custom metric with specialized validation logic for discount prediction. This tailored evaluation combines parsing, extraction, and custom comparison rules specific to the business domain.

Evidence 3: Multi-Turn Refusal Rate
- File: `docs/howtos/customizations/metrics/_write_your_own_metric_advanced.md`
- Code Reference: `RefusalRate` custom composite metric
```python
@dataclass
class RefusalRate(MetricWithLLM, MultiTurnMetric, SingleTurnMetric):
    # Custom metric combining LLM-based evaluation with statistical aggregation
    async def _multi_turn_ascore(self, sample, callbacks):
        # Custom logic for multi-turn evaluation
        scores = []
        for turn in grouped_messages:
            prompt_response = await self.refusal_prompt.generate(...)
            scores.append(prompt_response.refusal)
        return sum(scores)  # Custom aggregation
```
Multi-turn custom metric combining LLM-based evaluation with statistical aggregation. This hybrid approach integrates behavioral validation across conversation turns with specialized aggregation logic for computing overall refusal rates.