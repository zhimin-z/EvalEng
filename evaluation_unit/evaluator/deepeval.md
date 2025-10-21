## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Exact and quasi-exact matching functions
- File: `deepeval/scorer/scorer.py`
- Functions: `exact_match_score()`, `quasi_exact_match_score()`, `quasi_contains_score()`
- Code Reference:
```python
@classmethod
def exact_match_score(cls, target: str, prediction: str) -> int:
    """Metrics that calculates whether two sequences matches exactly or not."""
    if not prediction:
        return 0
    return 1 if prediction.strip() == target.strip() else 0
```
These functions implement deterministic string matching algorithms that compare predictions against targets using rule-based logic. The exact match performs binary comparison after whitespace normalization, while quasi-exact variants apply text normalization before matching. These are pure algorithmic evaluators that require no machine learning inference and produce consistent, reproducible results based solely on string operations.

Evidence 2: Statistical NLP metrics (ROUGE and BLEU)
- File: `deepeval/scorer/scorer.py`
- Functions: `rouge_score()`, `sentence_bleu_score()`
- Code Reference:
```python
@classmethod
def rouge_score(cls, target: str, prediction: str, score_type: str) -> float:
    """Calculates the Rouge score for a given target and prediction."""
    from rouge_score import rouge_scorer
    scorer = rouge_scorer.RougeScorer([score_type], use_stemmer=True)
    scores = scorer.score(target, prediction)
    return scores[score_type].fmeasure
```
These methods compute well-established algorithmic metrics for text generation quality. ROUGE measures n-gram overlap for summarization evaluation, while BLEU calculates precision-based scores for translation quality. Both use mathematical formulas and statistical computations (stemming, n-gram counting, precision/recall calculations) without requiring neural network inference, making them deterministic algorithmic evaluators.

Evidence 3: BERTScore and pass@k computational metrics
- File: `deepeval/scorer/scorer.py`
- Functions: `bert_score()`, `pass_at_k()`
- Code Reference:
```python
@classmethod
def bert_score(cls, target: str, prediction: str) -> float:
    """Calculates BERTScore using pretrained embeddings."""
    from bert_score import score
    P, R, F1 = score([prediction], [target], lang="en")
    return F1.item()

@classmethod
def pass_at_k(cls, n: int, c: int, k: int) -> float:
    """Mathematical formula for pass@k metric."""
    # Implementation of combinatorial formula
```
While BERTScore uses pretrained embeddings, it applies them through algorithmic similarity computations (cosine similarity between fixed embeddings) rather than performing new model inference. The pass@k function implements a pure mathematical formula for code generation evaluation. Both represent algorithmic approaches: BERTScore uses static embeddings in deterministic calculations, and pass@k applies combinatorial mathematics, distinguishing them from adaptive ML-based evaluators.

---

### ML-based

Evidence 1: GEval LLM-based evaluation framework
- File: `deepeval/metrics/g_eval/g_eval.py`
- Class: `GEval`
- Code Reference:
```python
async def _a_evaluate(self, test_case: LLMTestCase, _additional_context: Optional[str] = None) -> Tuple[Union[int, float], str]:
    prompt = self.evaluation_template.generate_evaluation_results(
        evaluation_steps=number_evaluation_steps(self.evaluation_steps),
        test_case_content=test_case_content,
        parameters=g_eval_params_str,
        rubric=rubric_str,
        score_range=self.score_range,
        _additional_context=_additional_context,
    )
    res, cost = await self.model.a_generate_raw_response(prompt, top_logprobs=self.top_logprobs)
    data = trimAndLoadJson(res.choices[0].message.content, self)
    return data["score"], data["reason"]
```
This class implements an ML-based evaluator that uses a language model to generate evaluation scores dynamically. The evaluator constructs prompts with evaluation criteria and test case content, then invokes `model.a_generate_raw_response()` to perform neural network inference. The LLM acts as a learned judge that interprets context, applies evaluation rubrics, and produces scores with reasoning. This requires active model inference for each evaluation, distinguishing it from static algorithmic approaches.

Evidence 2: Arena-style comparative evaluation with LLMs
- File: `deepeval/metrics/arena_g_eval/arena_g_eval.py`
- Class: `ArenaGEval`
- Code Reference:
```python
def _compare(self, test_case: ArenaTestCase) -> Tuple[str, str, Dict[str, str]]:
    prompt = ArenaGEvalTemplate.generate_arena_winner(
        evaluation_steps=number_evaluation_steps(self.evaluation_steps),
        test_case_contents=formatted_test_case,
        parameters=g_eval_params_str,
    )
    if self.using_native_model:
        res, cost = self.model.generate(prompt, schema=Winner)
        return res.winner, res.reason, dummy_to_real_names
```
This evaluator uses an LLM to perform head-to-head comparisons between multiple model outputs, determining a winner through neural inference. The model processes evaluation steps and test case contents to make comparative judgments, leveraging learned reasoning capabilities. This represents ML-based evaluation where the scoring mechanism itself is a trained neural network that must perform inference to generate comparative assessments, rather than applying predetermined formulas.

Evidence 3: Conversational and MCP protocol evaluation
- File: `deepeval/metrics/conversational_g_eval/conversational_g_eval.py`, `deepeval/metrics/mcp_use_metric/mcp_use_metric.py`
- Classes: `ConversationalGEval`, `MCPUseMetric`
- Code Reference:
```python
def _get_primitives_used_score(self, test_case: LLMTestCase, available_primitives: str, primitives_used: str) -> MCPPrimitivesScore:
    prompt = MCPUseMetricTemplate.get_primitive_correctness_prompt(
        test_case, available_primitives, primitives_used
    )
    if self.using_native_model:
        res, cost = self.model.generate(prompt, schema=MCPPrimitivesScore)
        return res
```
These specialized evaluators use LLM inference to assess complex conversational quality and protocol usage correctness. They generate prompts tailored to specific evaluation contexts (multi-turn conversations, API primitive usage) and invoke model generation to produce structured scores. The evaluation logic resides in the trained neural network's weights rather than in explicit algorithms, requiring model inference to interpret context and apply learned evaluation criteria.

Evidence 4: Specialized neural scoring models
- File: `deepeval/scorer/scorer.py`
- Functions: `faithfulness_score()`, `hallucination_score()`, `neural_toxic_score()`, `answer_relevancy_score()`, `neural_bias_score()`
- Code Reference:
```python
@classmethod
def hallucination_score(cls, source: str, prediction: str, model: Optional[str] = None) -> float:
    """Calculate the hallucination score using Vectara Hallucination Evaluation Model."""
    from deepeval.models.hallucination_model import HallucinationModel
    scorer = HallucinationModel(model_name=model)
    return scorer.model.predict([source, prediction])

@classmethod
def answer_relevancy_score(cls, predictions: Union[str, List[str]], target: str, model_type: Optional[str] = None, model_name: Optional[str] = None) -> float:
    """Calculates the Answer relevancy score."""
    from deepeval.models.answer_relevancy_model import AnswerRelevancyModel, CrossEncoderAnswerRelevancyModel
    answer_relevancy_model = AnswerRelevancyModel(model_name=model_name)
    query_embedding = answer_relevancy_model(target)
    document_embedding = answer_relevancy_model(docs)
    scores = util.dot_score(query_embedding, document_embedding)[0].cpu().tolist()
    return scores[0]
```
These functions invoke specialized trained neural networks (SummaCZS, Vectara HEM, Detoxify, sentence transformers, UnBiasedModel) to evaluate specific quality dimensions. Each model has learned patterns through training on relevant datasets and performs neural inference to generate scores. For example, the hallucination scorer uses a trained model to detect inconsistencies between source and prediction, while answer relevancy employs transformer embeddings and semantic similarity. These are ML-based evaluators because they depend on trained model weights and neural computation rather than algorithmic rules.

Evidence 5: Multimodal LLM evaluation
- File: `deepeval/metrics/multimodal_metrics/multimodal_g_eval/multimodal_g_eval.py`
- Class: `MultimodalGEval`
- Code Reference:
```python
def _evaluate(self, test_case: MultimodalTestCase) -> Tuple[Union[int, float], str]:
    # Constructs multimodal prompt with images and text
    res = self.model.generate(prompt)
    return res.score, res.reason
```
This evaluator extends ML-based evaluation to multimodal inputs, using models capable of processing both text and images. The model performs inference across modalities to generate evaluation scores, leveraging learned cross-modal representations. This represents advanced ML-based evaluation where the neural network must integrate information from multiple input types, requiring sophisticated model inference beyond what algorithmic approaches can provide.