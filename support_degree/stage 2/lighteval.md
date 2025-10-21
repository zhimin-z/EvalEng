# Lighteval - Stage 2 (PREPARE) Evaluation

## Summary
Lighteval is a lightweight LLM evaluation framework that focuses primarily on runtime evaluation rather than extensive data preparation infrastructure. It assumes datasets are already well-formatted on the Hugging Face Hub and provides minimal preprocessing, quality assessment, or infrastructure building capabilities. Most Stage 2 features are either absent or require manual implementation by users.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing utilities, mostly manual splitting required. Lighteval loads datasets directly from HF Hub with basic caching but lacks preprocessing pipelines. Evidence: `src/lighteval/tasks/lighteval_task.py` shows tasks only define `hf_repo`, `hf_subset`, and `evaluation_splits` - no preprocessing config. The `prompt_function` in tasks does formatting but not true preprocessing. Example from `examples/custom_tasks_templates/custom_yourbench_task.py` shows prompts are formatted at request time, not pre-processed. No stratified splitting, no version control for splits. |
| S2F2: Quality Assessment | 0 | No quality assessment features. Searched entire codebase - no label quality checks, demographic analysis, duplicate detection, or bias detection utilities. Tasks assume clean, ready-to-use datasets from HF Hub. No tools for detecting label noise, inter-annotator agreement, or outlier detection. |
| S2F3: PII Detection | 0 | No PII handling. No PII detection, anonymization, or privacy features found in codebase. The framework assumes datasets are already cleaned and compliant. No regex patterns, NER models, or audit trail for PII. |
| S2F4: Infrastructure Building | 0 | No infrastructure utilities. No support for building FAISS/ColBERT indices, database setup, or retrieval systems. The framework evaluates pre-trained models on existing datasets without building task-specific infrastructure. No index building, persistence, or artifact management features. |
| S2F5: Model Validation | 1 | Minimal validation, mostly manual. Basic model loading from HF Hub with revision pinning (e.g., `examples/model_configs/transformers_model.yaml` shows `revision: "57aa3c6599c53705406c648e7acca7e11dc45ea3"`), but no cryptographic checksum validation, version compatibility checks beyond what transformers provides, or corruption detection. Models are loaded via standard transformers/vllm APIs without additional integrity verification. |
| S2F6: Scenario Generation | 1 | Minimal generation, mostly static prompts. Prompt functions in tasks (e.g., `examples/nanotron/custom_evaluation_tasks.py`) create prompts from dataset lines but don't generate variations, multi-turn dialogues, or edge cases. The `prompt_function` parameter allows templating but not systematic variation generation. Few-shot examples are selected (`few_shots_select="random_sampling_from_train"`) but not parameterically generated. No reproducible scenario versioning. |
| S2F7: Red-Teaming | 0 | No red-teaming features. No jailbreak attempts, prompt injection tests, bias probing, or safety boundary testing. The framework is designed for standard benchmark evaluation, not adversarial testing. No attack libraries or adversarial generation capabilities found. |
| S2F8: Contamination Detection | 0 | No contamination features. No tools to compare eval data against training corpora, no n-gram overlap detection, no semantic similarity checks for contamination. The framework assumes users have already ensured train/test separation. |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (1 pt)

Evidence of minimal capabilities:

1. Basic dataset loading from HF Hub with caching:
```python
# From src/lighteval/tasks/lighteval_task.py
class LightevalTaskConfig:
    def __init__(
        self,
        name: str,
        prompt_function: Callable,
        hf_repo: str,
        hf_subset: str = "default",
        hf_avail_splits: list[str] | None = None,
        evaluation_splits: list[str] | None = None,
        # ...
    ):
```
Tasks specify which HF dataset and splits to use, but don't define preprocessing steps.

2. No preprocessing pipelines:
The framework loads raw datasets and applies prompt formatting at runtime. Example from `examples/nanotron/custom_evaluation_tasks.py`:
```python
def hellaswag_prompt(line, task_name: str = None):
    def preprocess(text):
        """Comes from AiHarness"""
        text = text.replace(" [title]", ". ")
        text = re.sub("\\[.*?\\]", "", text)
        text = text.replace("  ", " ")
        return text
    
    ctx = f"{line['ctx_a']} {line['ctx_b'].capitalize()} "
    return Doc(
        task_name=task_name,
        query=preprocess(line["activity_label"] + ": " + ctx),
        choices=[" " + preprocess(ending) for ending in line["endings"]],
        gold_index=int(line["label"]) if line["label"] != "" else -1,
    )
```
This is runtime formatting, not preprocessing with caching or versioning.

3. No physical splitting utilities:
Tasks reference pre-existing HF Hub splits. From `examples/custom_tasks_templates/custom_yourbench_task.py`:
```python
yourbench = LightevalTaskConfig(
    name="HF_TASK_NAME",
    hf_avail_splits=["train"],
    evaluation_splits=["train"],
    few_shots_split=None,
    # ...
)
```
No code to create stratified splits, save them to disk, or version them.

Rating: 1 pt - Minimal preprocessing, manual splitting required, basic HF caching only.

---

### S2F2: Dataset Quality and Bias Assessment (0 pts)

Evidence of absence:

Searched entire codebase for quality assessment terms:
- No "label_quality", "inter_annotator", "outlier_detection"
- No demographic analysis tools
- No duplicate detection (exact or fuzzy)
- No bias detection capabilities

The framework assumes datasets from HF Hub are already clean and balanced. No utilities provided for quality checks.

Rating: 0 pts - No quality assessment features.

---

### S2F3: PII Detection and Anonymization (0 pts)

Evidence of absence:

No PII-related code found. The framework focuses on model evaluation, not data sanitization. Users are expected to use pre-cleaned datasets.

Rating: 0 pts - No PII handling.

---

### S2F4: Task-Specific Infrastructure Building (0 pts)

Evidence of absence:

No retrieval system building, no database setup, no index creation. The framework evaluates models on existing datasets without building auxiliary infrastructure.

Example from `examples/custom_tasks_tests.py` shows tasks are defined by pointing to existing HF datasets:
```python
gsm8k_test = LightevalTaskConfig(
    name="gsm8k",
    hf_repo="gsm8k",
    hf_subset="main",
    # ...
)
```
No infrastructure building step before evaluation.

Rating: 0 pts - No infrastructure utilities.

---

### S2F5: Model Artifact Validation (1 pt)

Evidence of minimal validation:

1. Model loading with revision pinning:
From `examples/model_configs/transformers_model.yaml`:
```yaml
model_parameters:
  model_name: "HuggingFaceTB/SmolLM2-1.7B-Instruct"
  revision: "57aa3c6599c53705406c648e7acca7e11dc45ea3"
```
This ensures specific model versions, but no cryptographic validation.

2. No integrity checks:
Models are loaded via standard libraries (transformers, vllm) without additional checksum verification or corruption detection:
```python
# From examples/custom_models/local_mt_model.py
self._model = SeamlessM4Tv2ForTextToText.from_pretrained(config.model)
```
Relies on HF Hub's built-in validation, no extra checks.

Rating: 1 pt - Minimal validation via revision pinning, no cryptographic or integrity checks.

---

### S2F6: Evaluation Scenario Generation (1 pt)

Evidence of minimal generation:

1. Template-based prompting:
From `examples/nanotron/custom_evaluation_tasks.py`:
```python
def mmlu_prompt(line, task_name: str = None):
    topic = line["subject"]
    prompt = f"The following are questions about {topic.replace('_', ' ')}.\nQuestion: "
    prompt += line["question"] + "\nAnswer:"
    
    return Doc(
        task_name=task_name,
        query=prompt,
        choices=[f" {c}" for c in line["choices"]],
        gold_index=line["answer"],
    )
```
This creates prompts from dataset lines but doesn't generate variations or edge cases.

2. Few-shot sampling:
```python
# From examples/nanotron/custom_evaluation_tasks.py
CustomMMLUEvaluationTask(
    few_shots_split="dev",
    few_shots_select="sequential",
    # ...
)
```
Samples few-shots from a split but doesn't generate new scenarios.

Rating: 1 pt - Basic templating, no systematic variation generation or multi-turn support.

---

### S2F7: Red-Teaming and Adversarial Test Generation (0 pts)

Evidence of absence:

No adversarial testing capabilities. The framework focuses on standard benchmarks like MMLU, GSM8K, HellaSwag. No jailbreak attempts, prompt injection tests, or safety probes found in codebase.

Rating: 0 pts - No red-teaming features.

---

### S2F8: Data Contamination Detection (0 pts)

Evidence of absence:

No contamination detection tools. The framework assumes proper train/test separation in datasets. No n-gram overlap or semantic similarity checks.

Rating: 0 pts - No contamination features.

---

## Key Observations

### Strengths
1. Simple task definition via `LightevalTaskConfig` makes it easy to point to existing HF datasets
2. Flexible prompt functions allow custom formatting at request time
3. Multiple backend support (transformers, vllm, sglang) for efficient evaluation
4. Custom metric support through extension system

### Limitations for Stage 2
1. No data preparation layer - assumes datasets are ready-to-use
2. No quality assurance tools - relies on dataset curators
3. No infrastructure building - evaluates existing models on existing data
4. Minimal validation - basic model loading without integrity checks
5. No adversarial testing - standard benchmarks only
6. No contamination checks - assumes clean train/test splits

### Design Philosophy
Lighteval is designed as a lightweight evaluation harness, not a comprehensive data preparation framework. It excels at:
- Running evaluations quickly across multiple backends
- Defining custom tasks with minimal boilerplate
- Saving detailed results for analysis

But it intentionally omits heavy data preprocessing, assuming users work with well-curated HF datasets.

---

## Final Checklist
- [x] All 8 features rated (S2F1 through S2F8)
- [x] Every rating has evidence (code snippets, file paths)
- [x] Justifications are concise (2-4 sentences max)
- [x] Consistent rating standards across features

---

## Total Stage 2 Score: 3/24 (12.5%)

Lighteval scores very low on Stage 2 because it's fundamentally a runtime evaluation framework rather than a data preparation system. It assumes datasets arrive clean, split, and ready-to-use from the Hugging Face Hub. For users needing extensive data preprocessing, quality checks, or infrastructure building, they would need to handle those steps externally before using Lighteval for evaluation.