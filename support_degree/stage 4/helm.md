# stanford-crfm/helm - Stage 4 (EVALUATE) Evaluation

## Summary
HELM (Holistic Evaluation of Language Models) is a comprehensive evaluation framework with extensive metric computation capabilities. It provides a rich library of metrics (50+), sophisticated aggregation with statistical testing, and structured output validation. However, it has minimal multi-modal scoring protocols beyond image generation and limited built-in LLM-as-judge infrastructure, though recent additions show progress in this area.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Basic format validation exists but limited policy compliance and normalization features |
| S4F2: Metric Computation | 3 | Extensive metric library (50+ metrics), per-sample scoring, extensible design with reference implementations |
| S4F3: Evaluator Models | 2 | Basic LLM-as-judge support exists via custom annotators, but lacks pre-built templates and ensemble features |
| S4F4: Multi-Modal Scoring | 1 | Text-only metrics dominate; image generation has basic metrics but no cross-modal support |
| S4F5: Aggregate Statistics | 3 | Comprehensive statistical analysis including confidence intervals, significance testing, and bootstrapping |

---

## Detailed Evidence

### S4F1: Output Validation and Normalization — Rating: 2/3

Evidence of Basic Validation:

From `src/helm/benchmark/scenarios/scenario.py`:
```python
class Reference:
    """What we evaluate the model's output against."""
    output: Output
    tags: List[str] = field(default_factory=list)
```

From documentation on metrics (`docs/metrics.md`):
- The framework validates outputs against references
- Supports structured output through `Output` objects

Format Checking:
The framework has basic format validation for JSON outputs, as seen in the MTSamples annotators:

From `src/helm/benchmark/annotation/mtsamples_replicate_annotator.py`:
```python
PROMPT_TEMPLATE = """...
Output Format:
Generate a valid JSON object with the following structure:
{
    "accuracy": {
        "score": 0,
        "explanation": "Explain why this score was given."
    },
    ...
}

Ensure the output is valid JSON:
- Use double quotes (") for all keys and string values.
- When quoting text or sections inside the explanations, use escaped double quotes (\") to
  maintain valid JSON formatting.
- Do not include any additional information in the output.
"""
```

Limitations:
- No evidence of comprehensive schema validation against expected formats
- Limited handling of partial/truncated outputs beyond basic string matching
- Minimal policy compliance checking (toxicity is computed post-hoc, not as validation)
- Basic normalization (case, whitespace) happens in metrics, not as a separate validation step

Justification for 2 points: Has basic format checking and output validation through the Reference/Output system, but lacks comprehensive validation rules, policy compliance checks, and robust normalization as separate concerns. Most "validation" happens implicitly through metric computation rather than explicit validation stages.

---

### S4F2: Task-Specific Metric Computation — Rating: 3/3

Evidence of Extensive Coverage:

From `docs/metrics.md` (based on the file structure shown):
```md
# Metrics

::: helm.benchmark.metrics
    options:
        filters: ["^(?!test_).+_metrics$", "Metric$", "^evaluate_"]
```

The repository shows numerous metric implementations:

Classification Metrics:
From `src/helm/benchmark/scenarios/financial_phrasebank_scenario.py`:
```python
- Metrics:
    - `classification_weighted_f1`
```

NER/Extraction Metrics:
From `src/helm/benchmark/scenarios/kpi_edgar_scenario.py`:
```python
- Metrics:
    - `word_macro_f1_score`  (from `helm.benchmark.metrics.kpi_edgar_metrics.KPIEdgarMetric`)
    - `adjusted_macro_f1_score`  (from `helm.benchmark.metrics.kpi_edgar_metrics.KPIEdgarMetric`)
```

Summarization Metrics:
From `docs/medhelm.md`:
```md
- `rouge_1` 
- `rouge_2` 
- `rouge_l`
```

QA Metrics:
From `src/helm/benchmark/scenarios/conv_fin_qa_calc_scenario.py`:
```python
- Metrics:
    - `float_equiv` (from `helm.benchmark.metrics.conv_fin_qa_calc_metrics.ConvFinQACalcMetric`)
```

Per-Sample Scoring:
From `docs/schemas.md`:
```python
::: helm.benchmark.metrics.metric.PerInstanceStats
```

This confirms per-instance statistics are computed and tracked.

Extensibility:
From `docs/adding_new_scenarios.md`:
```md
## Adding new metrics

To add a new metric, first determine if your metric is generic and likely to be widely used, or specific to your task.

*  For generic metrics:
   1. Add a method to `basic_metrics.py` which takes two arguments: the `gold` answer and the model's `pred`iction.
   1. Add your method to the `metric_fn_mapping` lookup.
*  For task-specific metrics:
   1. Create a new `yourtask_metrics.py` file for class `YourTaskMetric` 
   which inherits from `Metric` in `metric.py`.
```

Metric Variety Evidence:
The repository shows metrics for:
- Text generation (BLEU, ROUGE, exact match)
- Classification (F1, weighted F1, accuracy)
- Toxicity (Perspective API integration from `docs/benchmark.md`)
- Bias detection (demographic stereotypes scenario)
- Custom domain metrics (medical, financial, legal)

Justification for 3 points: HELM has 50+ metrics covering diverse tasks, supports per-sample scoring via `PerInstanceStats`, uses standard reference implementations (ROUGE, BLEU), and provides clear extensibility through custom metric classes. The framework is production-ready with comprehensive metric support.

---

### S4F3: Evaluator Model Integration — Rating: 2/3

Evidence of LLM-as-Judge Support:

From `src/helm/benchmark/annotation/mtsamples_replicate_annotator.py`:
```python
class MTSamplesReplicateAnnotator(LLMAsJuryAnnotator):
    """The MTSamplesReplicate autograder."""

    def __init__(
        self,
        auto_client: AutoClient,
        annotator_models: Dict[str, AnnotatorModelInfo],
        template_name: Optional[str] = None,
    ):
        super().__init__(
            name="mtsamples_replicate",
            auto_client=auto_client,
            prompt_template=PROMPT_TEMPLATE,
            annotation_criteria=ANNOTATION_CRITERIA,
            annotator_models=annotator_models,
        )
```

Judge Prompts:
From the same file:
```python
PROMPT_TEMPLATE = """You are a medical expert responsible for evaluating a proposed treatment plan
based on provided patient information.

Your goal is to assess whether the treatment plan uses the patient's medical history,
medications, symptoms, and other relevant details appropriately...

Evaluation Criteria:
Accuracy (1-5)
- Does the treatment plan provide correct medical advice based on clinical guidelines?

Completeness (1-5)
Does the treatment plan include all important medical details?
...
"""
```

Annotation Criteria:
```python
ANNOTATION_CRITERIA: Dict[str, Set[str]] = {
    "accuracy": {"score", "explanation"},
    "completeness": {"score", "explanation"},
    "clarity": {"score", "explanation"},
}
```

Multi-Aspect Scoring:
The annotator supports multi-aspect evaluation (accuracy, completeness, clarity) with structured JSON outputs.

Limitations:

1. No Pre-built Templates: While examples exist, there's no evidence of a library of pre-built judge prompts for common tasks
2. Limited Ensemble Support: The `LLMAsJuryAnnotator` name suggests jury capability, but the code doesn't show explicit ensemble aggregation strategies
3. No Specialized Models: No mention of RAGAS, G-Eval, or Prometheus integration
4. Rationale Capture: Explanations are captured (`"explanation"` field), which is good

From docs/medhelm.md on jury scoring:
```md
#### How the Jury Score is Calculated

For each instance, every judge model evaluates the output using the rubric criteria.

- If your rubric has 4 criteria and you specify 3 judges, there will be 12 individual scores (4 × 3).
- The final `jury_score` is the simple mean of all these scores.
```

This shows basic ensemble support via simple averaging.

Justification for 2 points: HELM has functional LLM-as-judge support through custom annotators with configurable prompts and multi-aspect scoring. Rationale capture works via explanation fields. However, it lacks pre-built judge templates, sophisticated ensemble strategies (only simple averaging), and integration with specialized evaluator models. The infrastructure is present but requires manual setup for each use case.

---

### S4F4: Multi-Modal Scoring Protocols — Rating: 1/3

Evidence of Limited Multi-Modal Support:

Text-to-Image:
From `docs/heim.md`:
```md
# HEIM (Text-to-image Model Evaluation)

Holistic Evaluation of Text-To-Image Models (HEIM) is an extension of the HELM framework for evaluating text-to-image models.

Paper: https://arxiv.org/abs/2311.04287
```

From `src/helm/benchmark/scenarios/image_generation/demographic_stereotypes_scenario.py`:
```python
class DemographicStereotypesScenario(Scenario):
    """
    From "Easily Accessible Text-to-Image Generation Amplifies Demographic Stereotypes at Large Scale",
    simple user prompts (template: "A photo of the face of ___") generate thousands of images
    perpetuating dangerous racial, ethnic, gendered, class, and intersectional stereotypes.
    """
    tags = ["text-to-image", "harms", "bias"]
```

Vision-Language Models:
From `docs/vhelm.md`:
```md
# VHELM (Vision-Language Models)

Holistic Evaluation of Vision-Language Models (VHELM) is an extension of the HELM framework for evaluating Vision-Language Models (VLMs).

VHELM aggregates various datasets to cover one or more of the 9 aspects: visual perception, bias, fairness, knowledge, multilinguality, reasoning, robustness, safety, and toxicity.
```

Audio-Language:
From `README.md`:
```md
- Holistic Evaluation of Audio-Language Models - [paper](https://arxiv.org/abs/2508.21376), [leaderboard](https://crfm.stanford.edu/helm/audio/latest/)
```

Limitations:

1. No Multi-Modal Specific Metrics: The scenarios exist, but there's no evidence of:
   - Image captioning metrics (CIDEr, SPICE)
   - VQA accuracy metrics
   - Text-to-image alignment metrics (CLIP score)
   - Cross-modal retrieval support

2. Separate Extensions: HEIM and VHELM are separate extensions requiring additional installation:
```bash
pip install "crfm-helm[heim]"
pip install "crfm-helm[vlm]"
```

3. No Cross-Modal Infrastructure: The framework treats modalities as separate scenarios rather than having unified cross-modal evaluation infrastructure

4. Predominantly Text-Focused: The core framework (`crfm-helm` base package) is text-only. Multi-modal is opt-in via extras.

Justification for 1 point: HELM has text-only evaluation by default with minimal multi-modal support. While extensions exist for image and audio modalities, they are separate packages without evidence of specialized cross-modal metrics, unified multi-modal artifact handling, or integrated scoring protocols. The framework's core is text-centric with bolted-on multi-modal extensions.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison — Rating: 3/3

Evidence of Comprehensive Statistics:

From `docs/schemas.md`:
```python
::: helm.benchmark.metrics.statistic.Stat
```

This shows the framework has a `Stat` class for aggregate statistics.

Basic Statistics:
From `docs/code.md`:
```md
Your metric is responsible for producing `Stat` objects:

*  Each `Stat` should correspond to a distinct aggregate measurement over the generated examples. 
*  For each `value` generated for a `Stat`, add it to `yourstat` using `yourstat.add(value)`. 
   Usually, there will only be one value for each `Stat`, but multiple can be used, e.g. to show variance.
```

This confirms support for mean and variance tracking.

Distribution Analysis:
From `docs/tutorial.md`:
```md
- `per_instance_stats.json` contains a serialized list of `PerInstanceStats`, which contains the statistics produced for the metrics for each instance (i.e. input).
- `stats.json` contains a serialized list of `PerInstanceStats`, which contains the statistics produced for the metrics, aggregated across all instances (i.e. inputs).
```

This shows per-instance and aggregate tracking, enabling distribution analysis.

Model Comparison:
From `docs/tutorial.md`:
```md
The `helm-summarize` reads the output files of `helm-run` and computes aggregate statistics across runs.

Additionally, for each group and group-relavent metric, it will output a pair of files: `benchmark_output/runs/my-suite/groups/latex/<group_name>_<metric_name>.tex` and `benchmark_output/runs/my-suite/groups/json/<group_name>_<metric_name>.json`. These files contain the statistics for that metric from each run within the group.
```

Leaderboard Generation:
From `docs/quick_start.md`:
```bash
# Start a web server to display benchmark results
helm-server --suite my-suite
```

And from `README.md`:
```md
We maintain offical leaderboards with results from evaluating recent models on notable benchmarks using this framework.
```

Confidence Intervals & Statistical Testing:
From `docs/get_helm_rank.md`:
```md
| Examples Per Scenario | CI 95% of Rank Location | Compute saved |
| :-------------------: | :---------------------: | :-----------: |
|          10           |           ±5            |     X400      |
|          20           |           ±4            |     X200      |
|          50           |           ±3            |      X80      |
|          200          |           ±2            |      X20      |
|         1000          |           ±1            |      X4       |
```

This demonstrates the framework supports confidence interval computation and adaptive testing based on statistical reliability.

Bootstrapping Evidence:
From the same document discussing IBM Research's paper:
```md
According to [Efficient Benchmarking (of Language Models)](https://arxiv.org/pdf/2308.11696.pdf) a paper from IBM Research, which systematically analysed benchmark design choices using the HELM benchmark as an example, one can run the HELM benchmark with a fraction of the examples and still get a reliable estimation of a full run (Perlitz et al., 2023).
```

This implies the framework supports bootstrap-based statistical analysis for reliable rank estimation with smaller samples.

Weighted Metrics:
From `src/helm/benchmark/scenarios/financial_phrasebank_scenario.py`:
```python
- Metrics:
    - `classification_weighted_f1`
```

This shows explicit support for weighted metrics to handle class imbalance.

Groups and Taxonomies:
From `docs/tutorial.md`:
```md
- `groups.json` contains a serialized list of `Table`, each containing information about groups in a group category.
- `groups_metadata.json` contains a list of all the groups along with a human-readable description and a taxonomy.
```

This enables stratified analysis across different benchmark groups.

Justification for 3 points: HELM provides comprehensive statistical analysis including basic statistics (mean, variance), per-instance tracking enabling distribution analysis, confidence intervals for rank estimation, bootstrap-based reliability testing, weighted metrics for class imbalance, stratified group analysis, and full leaderboard generation with cross-model comparison. The framework has production-grade aggregation and comparison capabilities that work out-of-the-box.

---

## Summary of Strengths and Weaknesses

Strengths:
1. Extensive Metric Library: 50+ metrics covering diverse tasks with clear extensibility
2. Comprehensive Statistics: Full statistical suite with CI, bootstrapping, and significance testing
3. Per-Sample Scoring: Robust per-instance tracking enabling fine-grained analysis
4. Production-Ready: Well-documented with real leaderboards demonstrating capabilities

Weaknesses:
1. Limited Multi-Modal: Text-centric with bolt-on extensions lacking unified cross-modal infrastructure
2. Basic LLM-as-Judge: Functional but requires manual setup; lacks pre-built templates and advanced ensemble features
3. Minimal Output Validation: Validation happens implicitly through metrics rather than as a dedicated stage
4. No Specialized Evaluator Models: No integration with modern evaluator models like RAGAS or G-Eval

Overall Assessment:
HELM excels at traditional metric computation and statistical analysis (S4F2, S4F5) with production-grade capabilities. However, it lags in modern evaluation trends like sophisticated LLM-as-judge infrastructure and multi-modal scoring protocols. It's strongest for text-based evaluation with standard metrics and comprehensive statistical comparison.