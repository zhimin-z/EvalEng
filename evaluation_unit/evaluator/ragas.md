## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Quoted spans citation alignment metric
- File: `docs/quoted_spans_metric.md`
- Metric Name: `citation_alignment_quoted_spans`
- Code Reference:
```python
# Metric measures fraction of quoted spans appearing verbatim in sources
# Implementation normalizes text by collapsing whitespace and lowercasing
# Performs string matching to count matched vs total quoted spans
```
This metric measures the fraction of quoted spans in a model's answer that appear verbatim in retrieved sources. The implementation normalizes text by collapsing whitespace and lowercasing, then performs string matching to count matched vs total quoted spans. This is a deterministic, rule-based algorithmic metric that uses string matching algorithms without ML models.

Evidence 2: Context precision and recall metrics
- File: `docs/howtos/applications/compare_embeddings.md`
- Metrics: `context_precision`, `context_recall`
- Code Reference:
```python
from ragas.metrics import (context_precision, context_recall)
```
These metrics evaluate retriever performance through mathematical calculations of precision and recall scores - classic algorithmic metrics for information retrieval evaluation.

Evidence 3: BLEU score for text similarity
- File: `docs/getstarted/evals.md`
- Metric: `BleuScore`
- Code Reference:
```python
from ragas.metrics import BleuScore
metric = BleuScore()
test_data = SingleTurnSample(**test_data)
metric.single_turn_score(test_data)
# Output: 0.137
```
BLEU is a well-established algorithmic metric that uses n-gram matching and precision calculations. It's explicitly mentioned as a "non-LLM metric" in the documentation and produces deterministic scores based on string overlap between response and reference.

Evidence 4: Discount accuracy verification
- File: `docs/howtos/applications/benchmark_llm.md`
- Metric: `discount_accuracy`
- Code Reference:
```python
@discrete_metric(name="discount_accuracy", allowed_values=["correct", "incorrect"])
def discount_accuracy(prediction: str, expected_discount):
    parsed_json = json.loads(prediction)
    predicted_discount = parsed_json.get("discount_percentage")
    expected_discount_int = int(expected_discount)
    
    if predicted_discount == expected_discount_int:
        return MetricResult(value="correct", reason=...)
    else:
        return MetricResult(value="incorrect", reason=...)
```
This is a deterministic comparison metric that parses JSON and performs exact numeric matching between predicted and expected discount values - pure algorithmic evaluation without ML models.

---

### ML-based

Evidence 1: Aspect-based critique evaluation
- File: `docs/getstarted/evals.md`
- Metric: `AspectCritic`
- Code Reference:
```python
from ragas.metrics import AspectCritic
metric = AspectCritic(name="summary_accuracy", llm=evaluator_llm, definition="Verify if the summary is accurate.")
await metric.single_turn_ascore(test_data)
```
AspectCritic is explicitly an LLM-based metric that uses a language model (`evaluator_llm`) to evaluate model outputs. It returns binary pass/fail based on LLM judgment against a definition criterion.

Evidence 2: RAG evaluation with LLM judges
- File: `docs/getstarted/rag_eval.md`
- Metrics: `LLMContextRecall`, `Faithfulness`, `FactualCorrectness`
- Code Reference:
```python
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
result = evaluate(dataset=evaluation_dataset, 
                 metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
                 llm=evaluator_llm)
```
These metrics use LLMs as evaluators/judges. The documentation explicitly mentions using an "evaluator LLM" for evaluation, and the metrics require an LLM parameter to function.

Evidence 3: Multi-turn conversation assessment
- File: `docs/howtos/applications/evaluating_multi_turn_conversations.md`
- Metrics: `AspectCritic`, `SimpleCriteriaScore`
- Code Reference:
```python
from ragas.metrics import AspectCritic, SimpleCriteriaScore
aspect_critic = AspectCritic(
    name="forgetfulness_aspect_critic",
    definition="Return 1 if the AI completes all Human requests...",
    llm=evaluator_llm,
)
```
These metrics explicitly use LLMs (`llm=evaluator_llm`) to evaluate conversation quality based on custom definitions. The LLM acts as a judge to assess whether conversations meet specified criteria.

Evidence 4: Rubric-based scoring
- File: `docs/howtos/customizations/metrics/_write_your_own_metric.md`
- Metric Base Class: `RubricsScore`
- Code Reference:
```python
from ragas.metrics import RubricsScore
hallucinations_rubric = RubricsScore(
    name="hallucinations_rubric", 
    llm=evaluator_llm, 
    rubrics=rubric
)
```
RubricsScore uses an LLM to evaluate outputs against provided rubrics (scoring criteria from 1-5). The LLM interprets the rubric and assigns scores based on its learned understanding.

Evidence 5: Custom refusal rate metric
- File: `docs/howtos/customizations/metrics/_write_your_own_metric_advanced.md`
- Metric: Custom `RefusalRate` with LLM-based prompt
- Code Reference:
```python
class RefusalRate(MetricWithLLM, MultiTurnMetric, SingleTurnMetric):
    refusal_prompt: PydanticPrompt = RefusalPrompt()
    async def _single_turn_ascore(self, sample, callbacks):
        prompt_response = await self.refusal_prompt.generate(
            data=prompt_input, llm=self.llm
        )
        return int(prompt_response.refusal)
```
This custom metric explicitly inherits from `MetricWithLLM` and uses an LLM to generate binary refusal judgments. The metric architecture demonstrates how LLMs serve as learned evaluators for custom criteria.

Evidence 6: Agent performance evaluation
- File: `docs/howtos/integrations/_langgraph_agent_evaluation.md`
- Metrics: `ToolCallAccuracy`, `AgentGoalAccuracyWithReference`
- Code Reference:
```python
from ragas.metrics import ToolCallAccuracy, AgentGoalAccuracyWithReference
tool_accuracy_scorer = ToolCallAccuracy()
scorer = AgentGoalAccuracyWithReference()
scorer.llm = evaluator_llm
```
AgentGoalAccuracyWithReference explicitly requires an LLM to evaluate whether agent goals are achieved. The documentation shows LLM assignment (`scorer.llm = evaluator_llm`), indicating ML-based evaluation.

Evidence 7: Customizable prompt-based metrics
- File: `docs/howtos/customizations/metrics/_modifying-prompts-metrics.md`
- Metric Class: `SimpleCriteriaScoreWithReference`
- Code Reference:
```python
from ragas.metrics._simple_criteria import SimpleCriteriaScoreWithReference
scorer = SimpleCriteriaScoreWithReference(name="random", definition="some definition")
# Shows prompts used by LLM for evaluation
scorer.get_prompts()
```
This documentation explicitly discusses modifying prompts used by LLM-based metrics, showing that the evaluation framework uses LLMs with customizable prompts to score outputs. The ability to modify instructions and few-shot examples confirms these are ML-based evaluators using learned models.