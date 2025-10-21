## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Comprehensive metric suite for multilingual evaluation
- File: `community_tasks/arabic_evals.py`
- Function: `Metrics.loglikelihood_acc()`, `Metrics.exact_match()`, `Metrics.rougeL`, `Metrics.bleu`, `Metrics.bleurt`, `Metrics.chrf`, `Metrics.ter`
- Code Reference:
```python
# Multiple algorithmic metrics used throughout the harness
Metrics.loglikelihood_acc()
Metrics.exact_match()
Metrics.rougeL
Metrics.bleu
Metrics.bleurt
Metrics.chrf
Metrics.ter
```
The harness extensively uses predefined algorithmic metrics as computational functions that score outputs based on mathematical formulas and string matching. These include log-likelihood accuracy metrics with normalization (LogProbCharNorm, LogProbTokenNorm, LogProbPMINorm), exact match scoring for comparing model outputs to gold answers, ROUGE metrics for summarization evaluation, BLEU/BLEURT/chrF/TER for translation tasks, and F1 scores for token overlap measurement. This demonstrates the algorithmic evaluator category's goal of ensuring consistent, reproducible evaluation through established computational measures.

Evidence 2: Character-normalized log-likelihood scoring
- File: `community_tasks/serbian_eval.py`
- Function: `Metrics.loglikelihood_acc(sample_params={"logprob_normalization": LogProbCharNorm()})`
- Code Reference:
```python
Metrics.loglikelihood_acc(sample_params={"logprob_normalization": LogProbCharNorm()})
```
Serbian evaluations employ algorithmic metrics with character-level normalization to compute accuracy scores based on log-likelihood comparisons. This provides deterministic assessment that is reproducible across different evaluation runs, exemplifying how algorithmic evaluators ensure consistent evaluation through predefined statistical functions.

Evidence 3: Token-normalized metrics for Filipino tasks
- File: `community_tasks/filipino_evals.py`
- Function: `LogLikelihoodAccMetric(normalization=LogProbTokenNorm())`, `Metrics.rougeL`, `Metrics.bleu`, `Metrics.bleurt`, `Metrics.chrf`, `Metrics.ter`
- Code Reference:
```python
LogLikelihoodAccMetric(normalization=LogProbTokenNorm())
Metrics.rougeL
Metrics.bleu
Metrics.bleurt
Metrics.chrf
Metrics.ter
```
Filipino tasks employ multiple algorithmic metrics including token-normalized log-likelihood accuracy and standard translation metrics. The combination of these predefined computational measures demonstrates how algorithmic evaluators provide reproducible assessments across different linguistic contexts using established mathematical formulas.

Evidence 4: Mathematical answer normalization
- File: `community_tasks/aimo_evals.py`
- Function: `Metrics.exact_match(sample_params={"normalize_gold": math_normalizer, "normalize_pred": math_normalizer})`
- Code Reference:
```python
Metrics.exact_match(sample_params={
    "normalize_gold": math_normalizer,
    "normalize_pred": math_normalizer
})
```
Mathematical evaluation uses exact match with specialized math normalization functions for comparing numerical answers. This algorithmic approach ensures deterministic assessment of mathematical reasoning tasks by applying predefined computational rules to standardize answer formats before comparison.

Evidence 5: Comprehensive metric documentation
- File: `docs/source/metric-list.mdx`
- Metrics: `loglikelihood_acc`, `loglikelihood_f1`, `mcc`, `word_perplexity`, `byte_perplexity`, `bits_per_byte`, `exact_match`, `f1_score`, `rouge`, `bleu`, `bert_score`, `faithfulness`, `extractiveness`, `copyright`
- Code Reference:
```markdown
- loglikelihood_acc
- loglikelihood_f1
- mcc (Matthew's correlation coefficient)
- word_perplexity, byte_perplexity, bits_per_byte
- exact_match, f1_score, rouge, bleu, bert_score
- faithfulness, extractiveness, copyright
```
Documentation confirms the harness provides extensive algorithmic metrics as predefined computational functions for various evaluation tasks. This comprehensive suite demonstrates the systematic approach to ensuring consistent, reproducible evaluation through established computational measures across diverse task types.

Evidence 6: Normalized exact matching for French tasks
- File: `community_tasks/french_evals.py`
- Function: `Metrics.exact_match(sample_params={"normalize_gold": math_normalizer, "normalize_pred": math_normalizer})`, `Metrics.loglikelihood_acc`
- Code Reference:
```python
Metrics.exact_match(sample_params={
    "normalize_gold": math_normalizer,
    "normalize_pred": math_normalizer
})
Metrics.loglikelihood_acc
```
French evaluations use exact match with mathematical normalization and log-likelihood accuracy metrics. These deterministic algorithmic functions provide reproducible assessment by applying consistent computational rules for answer comparison across evaluation runs.

Evidence 7: Log-likelihood accuracy for RAG evaluation
- File: `community_tasks/german_rag_evals.py`
- Function: `Metrics.loglikelihood_acc`
- Code Reference:
```python
Metrics.loglikelihood_acc
```
German RAG evaluations use log-likelihood accuracy for multiple-choice question evaluation. This algorithmic metric provides deterministic scoring based on statistical functions, ensuring consistent evaluation of retrieval-augmented generation performance.

---

### ML-based

Evidence 1: LLM-as-judge implementation for Arabic QA
- File: `community_tasks/arabic_evals.py`
- Class/Function: `JudgeMetricWrapper`, `JudgeLM`
- Code Reference:
```python
class JudgeMetricWrapper(Metric):
    """Wrapper class for LLM-based judge metric implementation."""
    
    def __init__(self, judge: JudgeLM):
        self.judge = judge
        # ...
    
    def compute(self, responses: list[str], formatted_docs: list[Doc], **kwargs) -> dict[str, float]:
        results = []
        for i, doc in enumerate(formatted_docs):
            question = doc.query
            gold = doc.choices[doc.gold_index] if doc.gold_index is not None else None
            answer = responses[i][0].result[0]
            
            score, _, _ = self.judge.evaluate_answer(question=question, answer=answer, options=None, gold=gold)
            results.append({self.metric_name: score})
        
        return results

judge = JudgeLM(
    model="Qwen/Qwen2.5-72B-Instruct",
    templates=judge_template,
    process_judge_response=process_judge_response,
    judge_backend="vllm",
)

wrapped_judge = JudgeMetricWrapper(judge)

alrage_qa_task = LightevalTaskConfig(
    name="alrage_qa",
    metrics=[wrapped_judge],
    # ...
)
```
This code implements an LLM-as-judge evaluator where the Qwen/Qwen2.5-72B-Instruct model serves as an evaluator for Arabic question-answering task outputs. The judge model provides scores from 0-10 for answer quality, which is then normalized. This exemplifies the ML-based evaluator category's goal of leveraging learned representations for nuanced assessment that captures semantic and contextual quality beyond what algorithmic metrics can measure.

Evidence 2: Multiple LLM judge implementations
- File: `docs/source/metric-list.mdx`
- Metrics: `llm_judge_gpt3p5`, `llm_judge_llama_3_405b`, `llm_judge_multi_turn_gpt3p5`, `llm_judge_multi_turn_llama_3_405b`
- Code Reference:
```markdown
## LLM-as-Judge
- llm_judge_gpt3p5: Can be used for any generative task, the model will be scored by a GPT3.5 model using the OpenAI API.
- llm_judge_llama_3_405b: Can be used for any generative task, the model will be scored by a Llama 3.405B model using the HuggingFace API.
- llm_judge_multi_turn_gpt3p5: Can be used for any generative task, the model will be scored by a GPT3.5 model using the OpenAI API. It is used for multiturn tasks like mt-bench.
- llm_judge_multi_turn_llama_3_405b: Can be used for any generative task, the model will be scored by a Llama 3.405B model using the HuggingFace API. It is used for multiturn tasks like mt-bench.
```
The documentation explicitly lists LLM-as-judge metrics that use large language models (GPT-3.5, Llama 3.405B) as evaluators to assess task outputs. These ML models provide learned evaluations of benchmark performance, demonstrating how the ML-based evaluator category leverages neural networks to capture nuanced semantic and contextual quality dimensions that are difficult for algorithmic metrics to assess.

Evidence 3: ML-based semantic and judge metrics reference
- File: `docs/source/package_reference/metrics.mdx`
- Classes: `BertScore`, `JudgeLLM`, `JudgeLLMMTBench`, `JudgeLLMMixEval`, `JudgeLM`
- Code Reference:
```markdown
### BertScore
[[autodoc]] metrics.metrics_sample.BertScore
### JudgeLLM
[[autodoc]] metrics.metrics_sample.JudgeLLM
### JudgeLLMMTBench
[[autodoc]] metrics.metrics_sample.JudgeLLMMTBench
### JudgeLLMMixEval
[[autodoc]] metrics.metrics_sample.JudgeLLMMixEval
### JudgeLM
[[autodoc]] metrics.utils.llm_as_judge.JudgeLM
```
The metrics reference includes BERTScore (which uses BERT embeddings for semantic similarity assessment) and multiple LLM judge implementations (JudgeLLM, JudgeLLMMTBench, JudgeLLMMixEval, JudgeLM). This confirms that ML models—both embedding-based models and generative language models—are used as evaluators in this harness, leveraging learned representations to capture semantic quality dimensions beyond surface-level string matching.

Evidence 4: Structured evaluation prompt for LLM judge
- File: `community_tasks/arabic_evals.py`
- Function: `judge_template()`
- Code Reference:
```python
def judge_template(question: str, answer: str, gold: str, options: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """
    Template for the Arabic judge prompt.
    System prompt translation: You are a neutral expert evaluator...
    """
    messages = [
        {
            "role": "system",
            "content": """أنت مقيّم محايد خبير باللغة العربية. يجب عليك:
1. تقييم دقة الإجابة مقارنة بالإجابة الصحيحة
2. التحقق من أن الإجابة مدعومة بالسياق المقدم
3. تقييم جودة وشمولية الإجابة

مهم جداً: يجب أن يكون ردك رقماً فقط من 0 إلى 10. لا تضف أي نص أو تفسير.""",
        },
        {
            "role": "user",
            "content": f"""السؤال: {question}
الإجابة المقدمة: {answer}
الإجابة الصحيحة: {gold}
أعط تقييماً من 0 إلى 10:...""",
        },
    ]
    return messages
```
This template demonstrates how the LLM judge is instructed to evaluate answers by comparing them to gold standards, assessing context support, and rating answer quality on a 0-10 scale. The structured prompt guides the ML model to perform nuanced assessment of answer accuracy, contextual grounding, and quality—demonstrating how ML-based evaluators leverage learned language understanding to capture complex quality dimensions that require semantic and contextual reasoning.