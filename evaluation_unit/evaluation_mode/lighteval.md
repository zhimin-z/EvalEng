## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Multiple Choice Log-Likelihood Evaluation
- File: `community_tasks/arabic_evals.py`
- Function/Class: `arabic_mmlu_pfn()`, `CustomArabicMMLUTask`
- Code Reference:
```python
def arabic_mmlu_pfn(line, task_name: str = None):
    instruction = "السؤال التالي هو سؤال متعدد الإختيارات. اختر الإجابة الصحيحة:\n\n"
    # ...
    return Doc(
        task_name=task_name,
        query=query,
        choices=valid_keys_arabic,  # Return only valid choices (Arabic keys)
        gold_index=answer_index,  # Correct index in the valid Arabic keys
        instruction=instruction,
    )

class CustomArabicMMLUTask(LightevalTaskConfig):
    def __init__(self, name, hf_subset):
        super().__init__(
            # ...
            metrics=[Metrics.loglikelihood_acc(sample_params={"logprob_normalization": LogProbCharNorm()})],
            # ...
        )
```
This task evaluates models by computing log-likelihoods of different answer choices and selecting the one with the highest probability. The model output is not executed; instead, the probabilities are directly compared. This is a pure static analysis approach where model outputs (probability distributions) are inspected without execution.

Evidence 2: Format Validation and Text Comparison
- File: `community_tasks/filipino_evals.py`
- Function/Class: `get_mcq_prompt_function()`, multiple task configurations
- Code Reference:
```python
FILIPINO_BELEBELE_TASKS = [
    LightevalTaskConfig(
        name=f"belebele_{LangCodeLanguage.get(language).to_alpha3()}_{formulation.name.lower()}",
        prompt_function=get_mcq_prompt_function(
            iso_639_3_ind_to_iso_639_3_macro[LangCodeLanguage.get(language).to_alpha3()],
            lambda line: {
                "question": line["question"],
                "context": line["flores_passage"],
                "choices": [line[f"mc_answer{i}"] for i in range(1, 5)],
                "gold_idx": int(line["correct_answer_num"]) - 1,
            },
            formulation=formulation,
        ),
        metrics=[
            LogLikelihoodAccMetric(normalization=LogProbTokenNorm()),
            LogLikelihoodAccMetric(normalization=LogProbCharNorm()),
        ],
    )
]
```
These tasks use log-likelihood metrics to evaluate model outputs by comparing probability distributions over answer choices. The evaluation involves structural analysis of outputs (token-level and character-level normalization) without executing any generated code or artifacts.

Evidence 3: Exact Match and Math Normalization
- File: `community_tasks/french_evals.py`
- Function/Class: `prompt_bac_fr()`, `bac_fr_task`
- Code Reference:
```python
bac_fr_task = LightevalTaskConfig(
    name="bac-fr",
    suite=["community"],
    prompt_function=prompt_bac_fr,
    metrics=[
        Metrics.exact_match(sample_params={"normalize_gold": math_normalizer, "normalize_pred": math_normalizer}),
        Metrics.exact_match,
    ],
    stop_sequence=["\n"],
    version=0,
)
```
This task uses exact match metrics with normalization functions (like `math_normalizer`) to compare model outputs against gold answers. The evaluation involves string parsing and pattern matching without executing the generated text. This is pure static analysis of the model's textual outputs.

Evidence 4: Text Similarity and Matching
- File: `community_tasks/german_rag_evals.py`
- Function/Class: Multiple prompt functions and task configurations
- Code Reference:
```python
def prompt_fn_question_answer_match(line, task_name: str = None):
    instruction = "Beantwortet die Antwort wirklich die Frage? Antworte mit J für ja oder N für nein.\n\n"
    query_template = """\
Die Frage: {question}

Die Antwort: {answer}

Auswahl (J/N):"""
    # ...
    return Doc(
        task_name=task_name,
        instruction=instruction,
        query=query,
        choices=["J", "N"],
        gold_index=choices.index(line["target"]),
    )
```
The German RAG evaluation tasks use log-likelihood accuracy metrics to determine whether model outputs match expected patterns (like "J" or "N" for yes/no questions). The evaluation compares text outputs against reference answers through direct inspection, not execution.

Evidence 5: Metric Descriptions
- File: `docs/source/metric-list.mdx`
- Code Reference:
```markdown
## Automatic metrics for multiple-choice tasks
These metrics use log-likelihood of the different possible targets.
- `loglikelihood_acc`: Fraction of instances where the choice with the best logprob was correct
- `exact_match`: Fraction of instances where the prediction matches the gold
- `f1_score`: Average F1 score in terms of word overlap between the model output and gold
- `rouge`: Average ROUGE score based on n-gram overlap
- `bleu`: Corpus level BLEU score
```
The documentation clearly describes that the harness uses various static analysis metrics including log-likelihood comparison, exact match, F1 score, ROUGE, and BLEU. These metrics all involve inspecting model outputs through pattern matching, string comparison, and similarity scoring without executing the generated content.

Evidence 6: Math Expression Normalization
- File: `community_tasks/aimo_evals.py`
- Function/Class: `aimo_prompt()`, task configuration
- Code Reference:
```python
task = LightevalTaskConfig(
    name="aimo_progress_prize_1",
    prompt_function=aimo_prompt,
    metrics=[
        Metrics.exact_match(sample_params={"normalize_gold": math_normalizer, "normalize_pred": math_normalizer})
    ],
    generation_size=2048,
    stop_sequence=None,
)
```
This task evaluates mathematical reasoning by comparing model-generated answers to gold answers using `math_normalizer`. The normalization removes LaTeX formatting and normalizes mathematical expressions for comparison. This is static analysis - parsing and comparing text outputs without executing mathematical operations.

Evidence 7: Metric Class Documentation
- File: `docs/source/package_reference/metrics.mdx`
- Code Reference:
```markdown
### ExactMatches
[[autodoc]] metrics.metrics_sample.ExactMatches
### F1_score
[[autodoc]] metrics.metrics_sample.F1_score
### LoglikelihoodAcc
[[autodoc]] metrics.metrics_sample.LoglikelihoodAcc
### ROUGE
[[autodoc]] metrics.metrics_sample.ROUGE
### BertScore
[[autodoc]] metrics.metrics_sample.BertScore
### StringDistance
[[autodoc]] metrics.metrics_sample.StringDistance
```
The documentation references multiple static analysis metrics including exact matches, F1 scores, log-likelihood accuracy, ROUGE scores, BERTScore, and string distance metrics. All of these analyze model outputs through inspection and comparison without executing generated artifacts.

Evidence 8: Multiple Choice with Character Normalization
- File: `community_tasks/serbian_eval.py`
- Function/Class: `serbian_eval_prompt()`, multiple task configurations
- Code Reference:
```python
def serbian_eval_prompt(line: dict, task_name: Optional[str] = None) -> Doc:
    question = line["query"]
    choices = line["choices"]
    instruction = "Na osnovu sledećeg pitanja, izaberite tačanu opciju iz ponuđenih odgovora.\n"
    # ...
    return Doc(
        task_name=task_name,
        query=query,
        choices=choices,
        gold_index=gold_index,
        instruction=instruction,
    )

arc_easy = create_task_config(
    task_name="serbian_evals:arc_easy",
    metrics=[Metrics.loglikelihood_acc(sample_params={"logprob_normalization": LogProbCharNorm()})],
)
```
Serbian evaluation tasks use log-likelihood with character-level normalization to compare model outputs. The evaluation involves computing probabilities for different choices and selecting the highest one, which is pure static analysis of probability distributions.

Evidence 9: TUMLU Benchmark
- File: `community_tasks/turkic_evals.py`
- Function/Class: `tumlu_pfn()`, `CustomTUMLUTask`
- Code Reference:
```python
class CustomTUMLUTask(LightevalTaskConfig):
    def __init__(self, name, hf_subset):
        super().__init__(
            name=name,
            hf_subset=hf_subset,
            prompt_function=partial(tumlu_pfn, language=hf_subset),
            metrics=[Metrics.loglikelihood_acc(sample_params={"logprob_normalization": LogProbCharNorm()})],
            evaluation_splits=["test"],
            generation_size=-1,
            stop_sequence=None,
            version=0,
        )
```
The TUMLU tasks for Turkic languages use log-likelihood accuracy with character normalization. The evaluation compares probability distributions over answer choices without executing any code, making it a static analysis approach.

Evidence 10: Custom Metric Example
- File: `docs/source/adding-a-new-metric.mdx`
- Code Reference:
```python
def custom_metric(doc: Doc, model_response: ModelResponse) -> bool:
    response = model_response.text[0]
    return response == doc.choices[doc.gold_index]
```
The documentation shows that custom metrics directly inspect model responses by comparing text outputs to expected choices. This is a clear example of static analysis where the metric examines the generated text without executing it.