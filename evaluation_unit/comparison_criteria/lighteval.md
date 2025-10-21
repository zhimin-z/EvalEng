## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification]

## Detailed Analysis

### Explicit Labels

Evidence 1: Arabic MMLU Gold Answers
- File: `community_tasks/arabic_evals.py`
- Code Reference: `arabic_mmlu_pfn()` function (Lines 84-110)
```python
# Find the correct index for the answer key in the Arabic version
answer_index = valid_keys_latin.index(line["Answer Key"])
```
- Code Reference: `CustomArabicMMLUTask` class (Lines 159-175)
- Code Reference: `arabic_mmlu_ht_pfn()` function (Lines 196-206)
```python
answer_index = int(line["answer"])
```
Task configurations extract correct answer indices from the "MBZUAI/ArabicMMLU" dataset. The `answer_index` variable stores predetermined correct responses serving as gold labels for benchmark evaluation.

Evidence 2: Serbian Multiple Choice Tasks
- File: `community_tasks/serbian_eval.py`
- Code Reference: `prompt_fn_oz_eval_task()` function (Lines 147-158)
```python
choices = ["A", "B", "C", "D", "E"]
return Doc(
    task_name=task_name,
    query=query,
    choices=choices,
    gold_index=choices.index(line["answer_str"]),
)
```
- Code Reference: `serbian_eval_prompt()` function (Lines 183-206)
```python
if task_name and "mmlu" in task_name:
    correct_answer = str(line["answer"])
    gold_index = next((i for i, choice in enumerate(choices) if correct_answer in choice), None)
else:
    gold_index = int(line["answer"])
```
Extracts gold answer indices from dataset labels. The `gold_index` field points to predetermined correct answers for computing accuracy metrics through comparison against static reference standards.

Evidence 3: Filipino Evaluation Gold Indices
- File: `community_tasks/filipino_evals.py`
- Code Reference: `arabic_mmlu_pfn()` for Balita NLP tasks (Lines 115-127)
```python
return Doc(
    task_name=task_name,
    query=query,
    choices=line["title_choices"],
    gold_index=line["title_choice_gold_idx"],
)
```
- Code Reference: Belebele tasks (Lines 144-157)
```python
"gold_idx": int(line["correct_answer_num"]) - 1,
```
Uses explicit gold indices from dataset for Balita NLP and Belebele tasks. These predetermined correct answer positions serve as ground truth labels for evaluation.

Evidence 4: French Evaluation Reference Answers
- File: `community_tasks/french_evals.py`
- Code Reference: `prompt_gpqa_fr()` function (Lines 54-76)
```python
gold_index = random.randint(0, 3)
choices = [line["Réponse incorrecte 1"], line["Réponse incorrecte 2"], line["Réponse incorrecte 3"]]
choices.insert(gold_index, line["Réponse correcte"])
```
- Code Reference: `prompt_bac_fr()` function (Lines 80-98)
```python
return Doc(
    task_name=task_name,
    query=prompt,
    choices=as_list(line["choix"]),
    gold_index=line["choix"].index(line["choix correct"]),
)
```
Tasks with predetermined answers from dataset. The correct answer is tracked through `gold_index` even when choices are shuffled, maintaining reference to explicit ground truth labels.

Evidence 5: AIMO Math Gold Answers
- File: `community_tasks/aimo_evals.py`
- Code Reference: `aimo_prompt()` function (Lines 39-47)
```python
return Doc(
    task_name=task_name,
    choices=[str(line["answer"])],
    gold_index=0,
    query=line["problem"],
)
```
Math tasks use predetermined answer from dataset. The `gold_index` consistently points to the static reference answer for accuracy computation.

Evidence 6: Turkic TUMLU Answer Keys
- File: `community_tasks/turkic_evals.py`
- Code Reference: `tumlu_pfn()` function (Lines 93-118)
```python
answer_index = valid_keys.index(line.get("answer"))
```
Extracts answer keys from TUMLU dataset. These explicit correct answers serve as gold standards for comparing model outputs in benchmark evaluation.

---

### Behavioral Specification

Evidence 1: Symbolic Prolog Verification
- File: `community_tasks/slr_bench_evals.py`
- Code Reference: Symbolic judge import (Lines 47-52)
```python
# Check for SWI-Prolog installation
if shutil.which("swipl") is None:
    raise ImportError(
        "SWI-Prolog (swipl) is not installed or not in PATH. "
    )
# Load the symbolic judge for evaluating Prolog programs
symbolic_judge = load("AIML-TUDA/VerifiableRewardsForScalableLogicalReasoning")
```
- Code Reference: `VerifiableRewardMetric` class (Lines 62-83)
```python
class VerifiableRewardMetric(SampleLevelComputation):
    def compute(self, doc, model_response, **kwargs):
        try:
            prediction = model_response.final_text[0]
            validation_program = doc.choices[0] if doc.choices else ""
            ref_format = [
                {
                    "validation_program": validation_program,
                    "evaluation_config": {"positive_predicate": "eastbound", "negative_predicate": "westbound"},
                }
            ]
            results = symbolic_judge.compute(predictions=[prediction], references=ref_format)
            return results["accuracy"]
```
Executes generated Prolog programs using SWI-Prolog to verify functional correctness against validation programs. This dynamic behavioral validation evaluates code through executable specifications rather than static answer matching.

Evidence 2: LLM-as-Judge Evaluation
- File: `community_tasks/arabic_evals.py`
- Code Reference: `JudgeMetricWrapper` class (Lines 691-731)
```python
class JudgeMetricWrapper(Metric):
    def compute(self, responses: list[str], formatted_docs: list[Doc], **kwargs) -> dict[str, float]:
        results = []
        for i, doc in enumerate(formatted_docs):
            question = doc.query
            gold = doc.choices[doc.gold_index] if doc.gold_index is not None else None
            answer = responses[i][0].result[0]
            score, _, _ = self.judge.evaluate_answer(question=question, answer=answer, options=None, gold=gold)
            results.append({self.metric_name: score})
        return results
```
- Code Reference: `judge_template()` function (Lines 811-847)
```python
def judge_template(question: str, answer: str, gold: str, options: Optional[List[str]] = None) -> List[Dict[str, str]]:
    messages = [
        {
            "role": "system",
            "content": """أنت مقيّم محايد خبير باللغة العربية. يجب عليك:
1. تقييم دقة الإجابة مقارنة بالإجابة الصحيحة
2. التحقق من أن الإجابة مدعومة بالسياق المقدم
3. تقييم جودة وشمولية الإجابة""",
        },
```
LLM-as-judge system programmatically evaluates answer quality through defined criteria including accuracy, context support, and comprehensiveness. The judge executes validation logic against model outputs using executable specifications for quality assessment on ALRAGE QA benchmark tasks.