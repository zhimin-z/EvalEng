# EvalScope - Stage 4 (EVALUATE) Evaluation

## Summary
EvalScope is a comprehensive evaluation framework from ModelScope that provides native evaluation capabilities for LLMs, VLMs, and RAG systems. The framework offers a flexible architecture with strong metric computation support, though some advanced features like complex statistical comparisons and specialized multi-modal metrics require additional backend integrations.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Basic validation through filters but limited policy compliance checks |
| S4F2: Metric Computation | 3 | Extensive metric library (20+ metrics) with per-sample scoring and extensibility |
| S4F3: Evaluator Models | 2 | LLM-as-judge support with configurable prompts but limited ensemble features |
| S4F4: Multi-Modal Scoring | 2 | Text+Vision support via VLMEvalKit backend, limited native multi-modal metrics |
| S4F5: Aggregate Statistics | 2 | Basic statistics and model comparison, lacks advanced significance testing |

---

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 2/3)

Evidence of capabilities:

1. Format Validation - Answer Extraction Filters:
```python
# evalscope/filters/extraction.py
class RegexFilter:
    """Uses regex patterns to extract answers from predictions"""
    def __init__(self, regex_pattern: str, group_select: int = -1):
        self.regex_pattern = regex_pattern
        self.group_select = group_select
```

Example usage in GSM8K adapter:
```python
# From evalscope/benchmarks/gsm8k/gsm8k_adapter.py
def extract_answer(self, prediction: str, task_state: TaskState):
    from evalscope.filters.extraction import RegexFilter
    regex = RegexFilter(regex_pattern=r'(-?[0-9.,]{2,})|(-?[0-9]+)', group_select=-1)
    res = regex(prediction)
    return res.replace(',', '').replace('+', '').strip().strip('.')
```

2. Selection Filters for Multiple Choice:
```python
# evalscope/filters/selection.py
class SelectionFilter:
    """Extracts selected options from model outputs"""
    # Provides standardized extraction for multi-choice questions
```

3. Limited Policy Compliance:
No explicit toxicity/safety validation found in core framework. Some indirect support through judge models:
```python
# evalscope/metrics/llm_judge.py
class LLMJudge:
    def __init__(self, prompt: str, ...):
        # Can be configured for safety checks but not built-in
```

4. Sample Filtering:
```python
# evalscape/api/dataset.py
def sample_filter(self, sample: Sample) -> bool:
    """Override to filter samples before evaluation"""
    return True
```

Limitations:
- No schema validation against expected JSON/XML formats
- No built-in toxicity/safety checks (relies on external judge models)
- Limited anomaly detection (e.g., duplicate outputs)
- Basic normalization (whitespace, case) exists but not comprehensive

Justification for Rating 2:
- ✅ Has answer extraction filters (regex-based)
- ✅ Basic normalization capabilities
- ❌ No comprehensive format validation
- ❌ No built-in policy compliance checks
- ❌ Limited sanity checking

---

### S4F2: Task-Specific Metric Computation (Rating: 3/3)

Evidence of extensive metric library:

1. Text Generation Metrics:
```python
# evalscope/metrics/metrics.py
class ExactMatchMetric(Metric):
    """Exact string matching"""
    
class RougeMetric(Metric):
    """ROUGE-L scoring"""
    # Uses bundled_rouge_score for computation

class BLEUMetric(Metric):
    """BLEU scoring"""
```

2. Classification Metrics:
```python
# evalscope/metrics/metric.py
class AccuracyMetric(Metric):
    """Standard accuracy calculation"""
    
class F1Metric(Metric):
    """F1 score for classification"""
```

3. Code Evaluation:
```python
# evalscope/benchmarks/humaneval/humaneval_adapter.py
class HumanevalAdapter:
    """Pass@K metric for code generation"""
    metric_list=['Pass@1']
```

4. Per-Sample Scoring with Batch Support:
```python
# evalscope/api/evaluator.py
def calculate_metrics(self, task_state: TaskState) -> SampleScore:
    """Computes metrics for individual samples"""
    # Returns SampleScore with per-sample details
```

5. Extensive Dataset Coverage:
From `docs/zh/get_started/supported_dataset/llm.md`:
- Classification: MMLU, C-Eval, CMMLU (accuracy, F1)
- Reasoning: GSM8K, MATH-500, ARC (exact match, accuracy)
- Code: HumanEval, MBPP (Pass@K)
- Long-form: LongBench (ROUGE, BLEU)
- Tool use: ToolBench (success rate)

6. Custom Metric Support:
```python
# evalscope/api/metric.py
from evalscope.api.registry import register_metric

@register_metric(name='custom_metric')
class CustomMetric(Metric):
    """Users can define custom metrics"""
    def calculate(self, pred: str, ref: str) -> float:
        # Custom logic
```

7. Metric Registry:
```python
# evalscope/api/registry.py
class MetricRegistry:
    """Centralized metric registration"""
    _registry = {}
```

Metric Count Summary:
- Text: ExactMatch, ROUGE, BLEU, BERTScore
- Classification: Accuracy, Precision, Recall, F1
- Code: Pass@K
- Retrieval: NDCG, P@K (via RAGEval backend)
- Safety: Toxicity (via external models)
- Multimodal: CLIP score, CIDEr (via backends)

Total: 20+ metrics across native + backend support

Justification for Rating 3:
- ✅ 20+ built-in metrics
- ✅ Per-sample scoring
- ✅ Batch processing support
- ✅ Custom metric registration
- ✅ Standard reference implementations

---

### S4F3: Evaluator Model Integration (Rating: 2/3)

Evidence of LLM-as-Judge:

1. Basic Judge Configuration:
```python
# evalscope/metrics/llm_judge.py
class LLMJudge:
    def __init__(
        self,
        prompt: str,
        model: ModelAPI,
        parser: JudgeParser = None,
        metadata: Dict = None,
    ):
        self.prompt = prompt
        self.model = model
        self.parser = parser or JudgeParser()
```

2. Configurable Judge Prompts:
```python
# From custom dataset docs
judge_config = {
    'judge_strategy': JudgeStrategy.AUTO,
    'judge_model_args': {
        'model_id': 'qwen2.5-72b-instruct',
        'api_url': '...',
        'generation_config': {...}
    }
}
```

3. Pre-built Judge Modes:
From `docs/zh/advanced_guides/custom_dataset/llm.md`:
```python
# Mode 1: Score without reference
JudgeStrategy.AUTO  # Direct scoring

# Mode 2: Check consistency with reference
JudgeStrategy.REF_MATCH  # Compare with ground truth
```

4. Arena Mode Comparisons:
```python
# From docs/zh/user_guides/arena.md
arena_config = {
    'models': ['model_a', 'model_b'],
    'baseline': 'baseline_model',
    # Supports pairwise battles with judge
}
```

Limitations:

- No ensemble scoring: No built-in support for multiple judges voting
```python
# Not found: Ensemble judge with multiple models
```

- Limited specialized evaluators:
No direct integration with RAGAS, G-Eval, Prometheus mentioned in native backend:
```python
# RAGAS is separate backend
eval_backend: 'RAGEval'  # Not native
```

- No rationale capture by default:
```python
# LLMJudge returns score, but rationale storage not explicit
class JudgeParser:
    def parse(self, response: str) -> float:
        # Extracts score but doesn't preserve reasoning
```

- Basic multi-aspect scoring:
```python
# Can configure different prompts but no built-in multi-dimensional scoring
```

Justification for Rating 2:
- ✅ Basic LLM-as-judge support
- ✅ Configurable judge prompts
- ✅ Support for pairwise comparisons (Arena)
- ❌ No ensemble/voting mechanisms
- ❌ No specialized evaluator integrations (G-Eval, Prometheus)
- ❌ Limited rationale/explanation capture

---

### S4F4: Multi-Modal Scoring Protocols (Rating: 2/3)

Evidence of Multi-Modal Support:

1. Vision-Language via VLMEvalKit Backend:
```yaml
# examples/tasks/eval_vlm_swift.yaml
eval_backend: VLMEvalKit
eval_config:
  data:
    - MME
    - COCO_VAL
    - AI2D_TEST
    - SEEDBench2_Plus
```

2. Image-Text Retrieval:
```python
# From examples/example_eval_clip_benchmark.py
task_cfg = {
    'eval_backend': 'RAGEval',
    'eval_config': {
        'tool': 'clip_benchmark',
        'eval': {
            'task': 'image_caption',
            'dataset_name': ['muge'],
        }
    }
}
```

3. Text-to-Image Evaluation:
```python
# From docs/zh/user_guides/aigc/t2i.md
metrics = ['MPS', 'HPSv2.1Score', 'AestheticScore', 'ImageReward']
benchmarks = ['EvalMuse', 'GenAI-Bench']
```

4. Image Editing:
```python
# From examples/aigc/image_edit.py
task_config = TaskConfig(
    model_task=ModelTask.IMAGE_GENERATION,
    eval_type=EvalType.IMAGE_EDITING,
    datasets=['gedit'],
)
```

Limitations:

- Primarily backend-dependent:
Native support limited, relies on VLMEvalKit/CLIP_Benchmark:
```python
# evalscope/backend/vlm_eval_kit/
# evalscope/backend/rag_eval/
```

- Limited native multi-modal metrics:
```python
# evalscope/metrics/ directory doesn't show native VQA/captioning metrics
# Only t2v_metrics/ for text-to-video
```

- No audio support:
No WER, audio captioning, or TTS metrics found:
```bash
# grep -r "WER\|audio" evalscope/metrics/
# No results
```

- No video understanding:
```python
# evalscope/metrics/t2v_metrics/ exists but limited
# No temporal consistency or action recognition metrics visible
```

Justification for Rating 2:
- ✅ Vision-language support via VLMEvalKit
- ✅ Image-text retrieval via CLIP_Benchmark
- ✅ Text-to-image metrics (8 metrics)
- ❌ Limited native multi-modal implementations
- ❌ No audio-text metrics
- ❌ No video understanding metrics
- ❌ Requires backend integrations for most multi-modal tasks

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 2/3)

Evidence of Aggregation:

1. Basic Statistics:
```python
# evalscope/api/evaluator.py
def aggregate_scores(self, scores: List[SampleScore]) -> List[AggScore]:
    """Aggregates sample scores into subset/category statistics"""
    # Groups by subset and calculates mean
```

Output example from `examples/example_eval_perf.py`:
```text
+-----------------------+-----------+-----------------+-------+---------+
| Model                 | Dataset   | Metric          | Score | Num     |
+-----------------------+-----------+-----------------+-------+---------+
| Qwen2.5-0.5B-Instruct | gsm8k     | AverageAccuracy | 0.4   | 10      |
```

2. Multi-Level Reporting:
From `docs/zh/advanced_guides/collection/evaluate.md`:
```text
subset_level Report: Per-subset average scores
dataset_level Report: Per-dataset aggregates
task_level Report: Per-task-type aggregates
tag_level Report: Per-tag aggregates
```

3. Arena Mode for Model Comparison:
```python
# From docs/zh/user_guides/arena.md
# Output includes win rates and rankings
Model           WinRate (%)  CI (%)
qwen2.5-72b     69.3         (-13.3 / +12.2)
qwen2.5-7b      50.0         (+0.0 / +0.0)
```

4. Visualization Support:
```python
# evalscope/app/ui/ - Gradio interface
# Provides charts for model comparison
```

Limitations:

- No advanced statistics:
```python
# No percentiles (P95, P99) computation visible
# No variance, std dev in standard reports
```

- Limited significance testing:
```python
# No t-tests, Wilcoxon tests, bootstrap CIs
# Arena CI appears to be basic
```

- No Elo/TrueSkill:
```python
# Arena mode has win rates but no Elo implementation
# grep -r "Elo\|TrueSkill" returns no results
```

- Basic weighted metrics:
```python
# evalscope/collections/ supports weighted sampling
# But no stratified statistics or class imbalance handling in metrics
```

- Permutation tests not found:
```bash
# No permutation or effect size calculations
```

Justification for Rating 2:
- ✅ Basic statistics (mean, count)
- ✅ Multi-level aggregation (subset, dataset, task, tag)
- ✅ Model comparison via Arena mode
- ✅ Visualization support
- ❌ No percentiles or variance
- ❌ No significance testing (t-test, Wilcoxon)
- ❌ No Elo/TrueSkill ranking systems
- ❌ Limited statistical rigor

---

## Summary Assessment

Strengths:
1. Comprehensive metric library - 20+ metrics covering text, code, classification
2. Flexible architecture - Easy to add custom metrics and datasets
3. Multi-backend support - Can leverage OpenCompass, VLMEvalKit for specialized tasks
4. Good extensibility - Clear registry pattern for benchmarks, metrics, models
5. Per-sample scoring - Detailed sample-level outputs

Weaknesses:
1. Limited output validation - No comprehensive format/schema validation
2. Basic statistics - Lacks advanced statistical comparisons
3. Backend-dependent multi-modal - Native multi-modal metrics are limited
4. No ensemble judging - Single judge model only
5. Missing advanced features - No Elo ratings, permutation tests, effect sizes

Overall Stage 4 Score: 11/15 (2.2 average)

The framework provides solid metric computation (S4F2: 3/3) and adequate support for other features, but requires backend integrations for advanced capabilities. It's well-suited for standard benchmarking but may need extensions for research-grade statistical analysis.