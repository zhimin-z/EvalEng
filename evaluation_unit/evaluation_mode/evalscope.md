## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Text Comparison and Format Validation
- File: `docs/zh/advanced_guides/add_benchmark.md` (and English equivalent)
- Code Reference:
```python
def calculate_metrics():
    ├── filter_prediction()
    │   └── extract_answer() [User Implementation]
    ├── match_score() / llm_match_score()
    └── Returns SampleScore
```
The framework performs static analysis on model outputs through multiple adapter implementations that show static output inspection. This is clear static analysis as it involves parsing and validating model output text without executing any generated code. The framework uses a pipeline approach where predictions are filtered, answers are extracted through pattern matching, and scores are calculated based on string comparison - all characteristic operations of static analysis that provide fast, low-infrastructure evaluation focused on output quality assessment.

---

Evidence 2: Answer Extraction Methods
- File: `docs/zh/advanced_guides/add_benchmark.md`
- Example: GSM8K adapter
- Code Reference:
```python
def extract_answer(self, prediction: str, task_state: TaskState):
    """从模型预测中提取答案"""
    from evalscope.filters.extraction import RegexFilter
    
    # 使用正则表达式提取数字答案
    regex = RegexFilter(regex_pattern=r'(-?[0-9.,]{2,})|(-?[0-9]+)', group_select=-1)
    res = regex(prediction)
    return res.replace(',', '').replace('+', '').strip().strip('.')
```
This exemplifies static analysis through direct examination of model outputs using regex pattern matching. The framework extracts numerical answers from text responses without executing any generated code, demonstrating the "direct examination of model outputs without executing generated artifacts" principle. This approach enables efficient answer extraction and validation purely through text parsing, supporting the static analysis goal of providing fast evaluation focused on output quality assessment.

---

Evidence 3: Multiple Choice Answer Extraction
- File: `docs/zh/advanced_guides/add_benchmark.md`
- Class: MultiChoiceAdapter
- Code Reference:
```python
class MultiChoiceAdapter(DefaultDataAdapter):
    # Built-in choice formatting and answer extraction logic
    # Supports single-choice and multiple-choice modes
```
The MultiChoiceAdapter provides standardized answer extraction logic for multiple-choice questions through text parsing and format validation. This represents static analysis as it examines the structure and content of model responses without executing any generated artifacts. The adapter validates answer formats (single or multiple choices) and extracts selections purely through pattern recognition, aligning with the static analysis definition of direct output examination for quality assessment.

---

Evidence 4: Metric Calculation Framework
- File: Referenced in documentation showing evaluation flow
- Code Reference:
```python
@dataclass
class Score:
    value: Dict[str, float]      # 各指标的得分 {"acc": 1.0, "f1": 0.8}
    extracted_prediction: str    # 提取的预测答案
    prediction: str              # 原始预测文本
```
The framework calculates metrics by comparing extracted predictions against target answers through string matching and similarity scoring. This metric calculation system operates entirely on static text comparisons without any execution of generated content, representing pure static analysis. The Score dataclass captures both raw and processed predictions alongside computed metrics, enabling comprehensive output quality assessment through direct examination rather than behavioral testing.

---

Evidence 5: Thinking Efficiency Evaluation
- File: `docs/zh/best_practice/think_eval.md`
- Code Reference:
```
- 模型推理token数（Reasoning Tokens）: 模型推理过程中reasoning content总数
- 首次正确token数（First Correct Tokens）: 从起始位置到第一个可以识别为正确答案位置的token数
- token效率（Token Efficiency）: $\hat{T}/T$
```
This evaluation approach analyzes model outputs by counting tokens, parsing reasoning chains, and calculating efficiency ratios - all forms of static inspection. The framework examines the structure and content of reasoning processes without executing any generated code or artifacts. By measuring token counts and identifying correctness positions through text analysis, this method provides fast, low-infrastructure evaluation of model reasoning efficiency, perfectly embodying the static analysis approach to output quality assessment.

---

### Dynamic Execution

Evidence 1: Code Generation Evaluation
- File: `docs/zh/best_practice/eval_qwq.md` and `docs/en/best_practice/eval_qwq.md`
- Dataset: LiveCodeBench
- Code Reference:
```python
datasets=['live_code_bench'],
dataset_args={
    'live_code_bench': {
        'extra_params': {
            'start_date': '2024-08-01',
            'end_date': '2025-02-28'
        },
        "filters": {"remove_until": "</think>"}
    }
},
```
Output:
```text
| Model   | Dataset         | Metric   | Subset         |   Num |   Score |
| qwq-32b | live_code_bench | Pass@1   | release_latest |   279 |  0.6237 |
```
LiveCodeBench exemplifies dynamic execution as models generate code that must be executed against test cases to verify correctness. The `Pass@1` metric specifically indicates functional correctness testing through actual code execution - the generated artifacts (code) are run in controlled environments to determine if they pass test cases. This represents the core principle of dynamic execution: testing functional correctness and behavioral adequacy through actual execution of model outputs rather than static inspection.

---

Evidence 2: VLMEvalKit Backend Support
- File: `docs/zh/user_guides/backend/vlmevalkit_backend.md`
- Multi-modal evaluation pipeline

The documentation demonstrates VLMEvalKit integration supporting various evaluation tasks. While many tasks involve static analysis (VQA, MCQ), the framework architecture includes execution capabilities for certain tasks. The multi-modal evaluation pipeline necessarily involves running model inference to generate outputs from image-text inputs, representing a form of dynamic execution where the model artifact itself is executed to produce results that are subsequently evaluated. This hybrid approach allows the framework to test functional correctness of multi-modal models through actual execution.

---

Evidence 3: CLIP Benchmark Evaluation
- File: `docs/zh/user_guides/backend/rageval_backend/clip_benchmark.md`
- Task: Image-Text Retrieval
- Code Reference:
```python
task_cfg = {
    "eval_config": {
        "tool": "clip_benchmark",
        "eval": {
            "models": [...],
            "dataset_name": ["muge", "flickr8k"],
            "task": "zeroshot_retrieval"
        }
    }
}
```
While CLIP evaluation involves embedding generation and similarity computation, the actual model inference pipeline requires executing the CLIP model's forward pass with image and text inputs. This constitutes dynamic execution of the model artifact itself - the framework runs the CLIP model in a controlled environment to generate embeddings, then tests the functional correctness of these embeddings for retrieval tasks. This goes beyond static analysis by actually executing the model architecture to produce outputs for evaluation.

---

Evidence 4: Text-to-Image Generation Evaluation
- File: `docs/zh/best_practice/t2i_eval.md`
- Code Reference:
```python
task_cfg = TaskConfig(
    model='HiDream-ai/HiDream-I1-Dev',
    model_task=ModelTask.IMAGE_GENERATION,
    generation_config={
        'height': 1024,
        'width': 1024,
        'num_inference_steps': 28,
    }
)
```
This demonstrates dynamic execution through running text-to-image generation models (FLUX, HiDream) in controlled environments to produce images. The generation process involves executing the diffusion model's inference pipeline - running generated or configured model code to create outputs that are subsequently analyzed. This exemplifies the dynamic execution goal of testing functional correctness: the framework verifies that the model can successfully execute its generation process and produce valid image artifacts from text prompts.

---

Evidence 5: Model Inference Execution
- File: Multiple best practice documents
- Code Reference:
```python
task_config = TaskConfig(
    api_url='http://0.0.0.0:8801/v1/chat/completions',
    model='DeepSeek-R1-Distill-Qwen-7B',
    eval_type='service',
    datasets=['math_500'],
    eval_batch_size=32,
    generation_config={
        'max_tokens': 20000,
        'temperature': 0.6,
    }
)
```
The framework executes model inference through API services (vLLM, ms-swift) or local execution, representing dynamic execution where the model artifact is run to generate outputs. For code generation tasks specifically, this involves two levels of dynamic execution: first executing the language model to generate code, then executing the generated code itself to test functional correctness. This dual execution pattern - running both the model and its generated artifacts - fully embodies the dynamic execution approach to testing functional correctness and behavioral adequacy through actual execution in controlled environments.