# lmms-eval (EvolvingLMMs-Lab__lmms-eval) - Stage 4 (EVALUATE) Evaluation

## Summary
lmms-eval is a comprehensive evaluation framework for Large Multimodal Models (LMMs) supporting text, image, video, and audio tasks. The framework demonstrates strong metric computation capabilities with extensive built-in metrics, good support for custom evaluations, and reasonable aggregation features. However, it lacks systematic output validation, has limited built-in evaluator model integration, and shows gaps in formal statistical comparison tools.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation features. The framework has basic answer extraction logic (e.g., `lmms_eval/tasks/screenspot/utils.py` contains regex-based answer parsing), but lacks comprehensive format validation, schema checking, or policy compliance features. Most validation is task-specific rather than systematic. Example from `lmms_eval/tasks/ifeval/`: uses external modules for instruction following but no built-in validation framework. |
| S4F2: Metric Computation | 3 | Extensive metric library with 100+ tasks and diverse metrics. The framework includes: text generation metrics (exact match, F1, CIDEr - see `lmms_eval/tasks/vdc/utils.py`), classification metrics (accuracy - widespread), retrieval metrics (IoU for bounding boxes in `lmms_eval/tasks/screenspot/utils.py`), vision-language metrics (various in OCRBench, ChartQA), per-sample scoring via `log_samples` flag, and custom metric support through task-specific `utils.py` files. Framework is extensible via `lmms_eval/api/metrics.py`. |
| S4F3: Evaluator Models | 2 | Basic LLM-as-judge support but limited integration. Found GPT-based evaluation in `lmms_eval/tasks/video_detail_description/` ("GPT-3.5 Evaluation"), and references to model-based scoring in VideoMathQA (`cot_step_evaluation.py` uses Qwen-3-4B). However, no built-in judge prompt library, no ensemble support, and minimal rationale capture beyond what individual tasks implement. The framework relies on external APIs (OpenAI, Anthropic via `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` in docs) rather than integrated evaluator infrastructure. |
| S4F4: Multi-Modal Scoring | 3 | Strong multi-modal support across image, video, and audio. Evidence includes: Image tasks (AI2D, ChartQA, DocVQA - see `docs/current_tasks.md`), Video metrics (temporal understanding in VideoMME, TemporalBench per `lmms_eval/tasks/README.md`), Audio evaluation (WER mentioned in `lmms_eval/tasks/README.md`, Step2, VoiceBench, WenetSpeech tasks), Cross-modal support (vision-language in numerous tasks). Framework handles modality-specific artifacts via `doc_to_visual`, `doc_to_messages` functions, and task-specific processors. Multi-modal artifact handling in `lmms_eval/api/instance.py`. |
| S4F5: Aggregate Statistics | 2 | Basic statistics with simple comparisons. The framework provides mean accuracy (standard across all tasks), per-task breakdown (evident in task configs like `lmms_eval/tasks/megabench/`), and result logging via wandb (`--wandb_args` in examples). However, lacks built-in: confidence intervals, significance testing, bootstrap methods, formal ranking systems beyond simple accuracy comparison. The `evaluator.py` in most tasks performs simple mean aggregation without distributional analysis. Some tasks like GSM8K have self-consistency variants (`gsm8k_cot_self_consistency`) but limited statistical rigor. |

## Detailed Evidence

### S4F1: Output Validation (Rating: 1)
Evidence of minimal validation:
- `lmms_eval/tasks/screenspot/utils.py`: Basic regex answer extraction but no schema validation
- `lmms_eval/tasks/ifeval/`: Uses external `langdetect` for language validation, not framework-level
- No systematic policy compliance checks found
- Answer extraction is ad-hoc per task (e.g., VideoMathQA uses post-processing script `cot_postprocess.py` externally)
- Missing: format validators, sanitization pipeline, anomaly detection

Supporting quote from docs:
> "Answer extraction logic: First looks for numbers within curly brackets: `{3}`, If not found, looks for standalone numbers and adds brackets" (lmms_eval/tasks/vlmsareblind/README.md)

This shows validation is basic pattern matching, not comprehensive validation.

### S4F2: Metric Computation (Rating: 3)
Evidence of extensive metrics:

1. Coverage: 100+ tasks listed in `docs/current_tasks.md` including:
   - Text: F1 score in WebSRC (`lmms_eval/tasks/websrc/README.md`)
   - Vision: IoU, ACC@IoU, CENTER ACC in ScreenSpot
   - Video: temporal metrics in TemporalBench
   - Audio: WER for speech recognition

2. Implementation Quality:
```python
# From lmms_eval/tasks/vdc/utils.py (example of metric implementation)
def vdc_doc_to_text(doc, model_specific_prompt_kwargs=None):
    # Task-specific metric preparation
    question = doc["question"]
    return question
```

3. Per-sample scoring: `--log_samples` flag throughout examples enables per-instance results

4. Extensibility: Each task has custom `utils.py` for metrics (e.g., `lmms_eval/tasks/lemonade/utils.py`, `lmms_eval/tasks/megabench/metrics/`)

Limitation: Some metrics require external evaluation (e.g., MEGA-Bench requires separate evaluator script)

### S4F3: Evaluator Models (Rating: 2)
Evidence of basic LLM-judge:

1. GPT-based evaluation:
```markdown
# From lmms_eval/tasks/video_detail_description/README.md
GPT-3.5 Evaluation: The answers are evaluated using a prompt we designed, 
which rates the responses based on the aforementioned dimensions with `gpt-3.5-turbo-0613`.
```

2. Limited integration:
- No built-in judge prompt library in framework
- Tasks implement their own evaluation (VideoMathQA uses Qwen-3-4B externally)
- Missing: ensemble scoring, rationale capture APIs, calibration

3. API dependencies:
```bash
# From docs/run_examples.md
export OPENAI_API_KEY="<YOUR_API_KEY>"
```

Gap: No framework-level evaluator model abstraction or pre-built judge infrastructure

### S4F4: Multi-Modal Scoring (Rating: 3)
Evidence of strong multi-modal support:

1. Image metrics: Multiple vision-language benchmarks
```markdown
# From lmms_eval/tasks/screenspot/README.md
REC/Grounding requires that a model outputs a bounding box for the target element in the image. 
The evaluation metrics are: IoU, ACC@IoIU, CENTER ACC
```

2. Video metrics:
```markdown
# From lmms_eval/tasks/lemonade/README.md
Questions are organized into three groups and six subcategories including Perception, 
Reasoning, Summarization, Session Properties, Physical Attributes, and Kinematics.
```

3. Audio metrics:
```markdown
# From README.md
The lmms-eval/v0.3.0 has been upgraded to support audio evaluations for audio models 
like Qwen2-Audio and Gemini-Audio across tasks such as AIR-Bench, Clotho-AQA, LibriSpeech
```

4. Cross-modal artifacts: Handled via `messages.extract_media()` in chat models

### S4F5: Aggregate Statistics (Rating: 2)
Evidence of basic statistics:

1. Mean/median: Standard across all tasks
```python
# Implicit in task evaluation - simple mean aggregation
# No explicit statistical module found
```

2. Per-task breakdown:
```json
// From lmms_eval/tasks/megabench/README.md example
{
    "model_summary": {
        "core": {
            "num_eval_tasks": 440,
            "num_eval_samples": 6531,
            "macro_mean_score": 0.21890499112354772
        }
    }
}
```

3. Limitations:
- No confidence intervals implementation found
- No significance testing (t-test, Wilcoxon) in codebase
- Self-consistency in GSM8K (`gsm8k_cot_self_consistency`) but not generalized
- Missing: bootstrap methods, effect size computation, ranking systems like Elo

Gap: No `lmms_eval/api/statistics.py` or similar module for advanced aggregation

## Key Strengths
1. Extensive task coverage: 100+ benchmarks across all modalities
2. Strong metric library: Comprehensive metrics for different task types
3. Multi-modal excellence: Best-in-class support for image/video/audio
4. Extensible design: Easy to add custom metrics per task

## Key Weaknesses
1. No systematic validation: Output validation is ad-hoc and task-specific
2. Limited evaluator integration: Basic LLM-judge without framework support
3. Weak statistical analysis: Simple mean/accuracy without rigorous comparison tools
4. External dependencies: Many advanced evaluations require external scripts

## Recommendations for Improvement
1. Add framework-level output validation module with schema checking
2. Create integrated evaluator model API with pre-built judge prompts
3. Implement statistical comparison toolkit (significance testing, confidence intervals)
4. Centralize metric computation to reduce task-specific duplication