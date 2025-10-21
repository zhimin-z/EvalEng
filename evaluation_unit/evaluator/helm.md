## Evaluator Categories

[Algorithmic, ML-based, Environmental, Human]

## Detailed Analysis

### Algorithmic

Evidence 1: Algorithmic metric implementations in core metrics directory
- File: `src/helm/benchmark/metrics/` directory
- Additional Documentation: `docs/metrics.md`
- Code Reference:
```python
# Documentation filters for metrics
"^(?!test_).+_metrics$", "Metric$", "^evaluate_"
```
The metrics directory contains numerous algorithmic metric implementations that are documented with specific regex patterns to identify metric classes and evaluation functions. These implementations provide the foundation for deterministic, rule-based scoring of model outputs using predefined mathematical formulas.

Evidence 2: Token counting verification in window services
- File: `src/helm/benchmark/window_services/test_gpt2_window_service.py`
- Code Reference:
```python
assert self.window_service.get_num_tokens(TEST_PROMPT) == 51
```
This test demonstrates exact algorithmic token counting, where the window service uses a deterministic tokenization algorithm to count tokens. The exact match assertion (== 51) confirms this is a precise, reproducible algorithmic computation rather than a learned or probabilistic evaluation.

Evidence 3: ROUGE and BERTScore metric configuration
- File: `src/helm/benchmark/run_specs/medhelm/benchmark_config.py`
- Code Reference:
```python
SUMMARIZATION_METRICS = {
    "rouge_1",
    "rouge_2", 
    "rouge_l",
    "BERTScore-P",
    "BERTScore-R",
    "BERTScore-F",
}
```
The harness defines standard algorithmic metrics for summarization tasks. ROUGE metrics use n-gram overlap statistics, while BERTScore uses embedding similarity. These are deterministic computational functions that apply predefined algorithms (statistical overlap and cosine similarity) to score outputs mathematically without requiring human judgment or model inference.

Evidence 4: Classification and NER algorithmic metrics
- File: `docs/enterprise_benchmark.md`
- Code Reference:
```markdown
- `exact_match` for CTI to MITRE benchmark
- `classification_weighted_f1` for financial phrasebank
- `rouge_1`, `rouge_2`, `rouge_l` for summarization tasks
- `word_macro_f1_score` and `adjusted_macro_f1_score` for KPI EDGAR NER
```
The enterprise benchmark documentation specifies multiple algorithmic metrics across different task types. Exact match uses string comparison, F1-score variants use precision/recall calculations, and ROUGE uses n-gram statistics. These are all rule-based computational formulas that produce deterministic scores based on mathematical definitions.

---

### ML-based

Evidence 1: GPT-4o and Llama as safety judges
- File: `src/helm/benchmark/annotation/model_as_judge.py`
- Function: `score_with_reasoning_with_gpt_and_llama()`
- Code Reference:
```python
def score_with_reasoning_with_gpt_and_llama(
    auto_client: AutoClient,
    annotator_prompt: str,
) -> Dict[str, Optional[Union[str, float]]]:
    """EXPERIMENTAL: DO NOT USE IN PRODUCTION
    
    Score using GPT-4o and Llama 3.1 for safety scenarios in HELM Safety."""
    SHORT_NAME_TO_MODEL_INFO: Dict[str, AnnotatorModelInfo] = {
        "gpt": AnnotatorModelInfo(model_name="openai/gpt-4o-2024-05-13", ...),
        "llama": AnnotatorModelInfo(
            model_name="meta/llama-3.1-405b-instruct-turbo", ...),
    }
```
This function implements ML-based evaluation by using large language models (GPT-4o and Llama 3.1) as judges. These models have learned parameters from pre-training and generate evaluative scores through inference. Unlike algorithmic metrics that apply fixed formulas, these ML models use their learned representations to assess output quality, making them neural network-based evaluators rather than rule-based ones.

Evidence 2: Flexible LLM jury annotation framework
- File: `src/helm/benchmark/annotation/model_as_judge.py`
- Class: `LLMAsJuryAnnotator`
- Code Reference:
```python
class LLMAsJuryAnnotator(Annotator):
    """
    A flexible LLM-based annotator that can be configured for different annotation scenarios.
    
    This annotator supports:
    - Custom prompt templates
    - Multiple evaluation models
    - Configurable evaluation criteria
    """
```
The LLMAsJuryAnnotator class provides a configurable framework for using language models as evaluators. This architecture allows multiple LLMs to serve as judges with customizable prompts and criteria. The flexibility in model selection and prompt engineering demonstrates that these are ML-based evaluators that leverage learned model capabilities rather than executing predefined algorithmic rules.

Evidence 3: Safety-focused model-as-judge implementation
- File: `src/helm/benchmark/annotation/simple_safety_tests_annotator.py`
- Class: `SimpleSafetyTestsAnnotator`
- Code Reference:
```python
class SimpleSafetyTestsAnnotator(Annotator):
    """Autograder for SimpleSafetyTests scenario that uses model as judge to rate harmfulness of output."""
```
This annotator uses a language model to evaluate the harmfulness of outputs for safety testing. The model-as-judge approach is necessary here because safety assessment requires nuanced understanding of content that cannot be captured by algorithmic rules. The ML model's learned knowledge about harmful content enables it to provide more sophisticated safety ratings than pattern-matching algorithms could achieve.

Evidence 4: Jury metric configuration system
- File: `src/helm/benchmark/run_specs/medhelm/benchmark_config.py`
- Code Reference:
```python
@dataclass(frozen=True)
class JuryMetricConfig(MetricConfig):
    """Configuration for jury-based metrics with multiple judges"""
    prompt_file: str
    judges: List[AnnotatorModelInfo]
```
The jury metric configuration defines a structured system for using multiple ML models as judges. This multi-model jury approach aggregates evaluations from different language models, treating each as an independent evaluator. The configuration specifies which models serve as judges and what prompts guide their evaluation, establishing an ML-based evaluation framework distinct from algorithmic scoring.

---

### Environmental

Evidence 1: HEIM human evaluation data processing
- File: `scripts/heim_human_eval.py`
- Function: `generate_heim_human_eval_dataset()`
- Code Reference:
```python
def generate_heim_human_eval_dataset(raw_human_eval_results_path: str):
    """
    Given a human eval results folder from HEIM, generates a dataset that can be used to evaluate VLMs.
    """
    # Reads CSV files with human annotations
    for csv_file_name in os.listdir(question_folder_path):
        if not csv_file_name.startswith("Batch"):
            continue
        with open(csv_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in tqdm(reader):
                # Extract answers from annotation system
                answer_key: str = QUESTION_TYPE_TO_ANSWER_KEY[question_type].format(choice=choice)
                answer = row[answer_key]
```
This script processes evaluation results from an external annotation system (HEIM). The "Batch" CSV files indicate data from an external platform where annotations were collected. By ingesting these external results and formatting them for the harness, the system demonstrates environmental evaluation—leveraging feedback from systems outside the core harness infrastructure to assess model performance on benchmark tasks.

Evidence 2: External difficulty dataset integration
- File: `docs/reeval.md`
- Code Reference:
```python
# load difficulty
difficulty_dataset = load_dataset("stair-lab/reeval-difficulty", split=split_name)
prompt_to_difficulty: dict[str, float] = {row["request.prompt"]: row["z"] for row in difficulty_dataset}
```
The harness loads difficulty ratings from an external HuggingFace dataset (stair-lab/reeval-difficulty) to incorporate pre-computed difficulty scores into the evaluation process. These difficulty ratings come from an external source and are used to adapt or contextualize benchmark evaluation. This represents environmental evaluation because the harness consumes evaluation metadata produced by external systems rather than computing everything internally.

Evidence 3: Scenario-to-metric mapping from external benchmarks
- File: `src/helm/benchmark/reeval_runner.py`
- Code Reference:
```python
scenario_to_metric_name = {
    "air_bench_2024": "air_score",
    "babi_qa": "quasi_exact_match",
    # ... maps scenarios to their evaluation criteria
}
```
The REEval runner maps external benchmark scenarios to their designated evaluation metrics. These scenarios (like air_bench_2024) are external benchmarks with their own evaluation protocols. The harness integrates with these external evaluation frameworks by adopting their specified metrics, demonstrating environmental evaluation through alignment with externally-defined assessment standards for benchmark tasks.

---

### Human

Evidence 1: Multi-aspect human judgment questions for image generation
- File: `scripts/heim_human_eval.py`
- Code Reference:
```python
QUESTION_TYPE_TO_INFOS = {
    "alignment": {
        "instruction": "Please answer the question below about the following image and description.",
        "question": "How well does the image match the description?",
        "choices": {
            0: "Does not match at all",
            1: "Has significant discrepancies",
            2: "Has several minor discrepancies",
            3: "Has a few minor discrepancies",
            4: "Matches exactly",
        },
    },
    "aesthetics": {...},
    "originality": {...},
    # Human judgment questions for image generation
}
```
The harness defines structured questions for human annotators to evaluate vision-language model outputs across multiple quality dimensions. These questions (alignment, aesthetics, originality) require human judgment because they assess subjective qualities that cannot be reliably measured algorithmically. The ordinal scale (0-4) captures gradations of human perception, making this a direct human evaluation system for benchmark task assessment.

Evidence 2: Human annotation aggregation and scoring
- File: `scripts/heim_human_eval.py`
- Code Reference:
```python
examples[image_url]["human_annotations"].append(correct_answer)
# Later computes mean score
example["mean_score"] = statistics.fmean(example["human_annotations"])
```
The harness collects multiple human annotations per example and aggregates them by computing mean scores. This multi-annotator approach treats human judgments as the primary evaluation signal, using statistical aggregation to create reliable ground truth scores from individual human ratings. The averaging process demonstrates that human evaluation is central to the benchmark assessment, not merely supplementary validation.