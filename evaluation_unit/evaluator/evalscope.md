## Evaluator Categories

[Algorithmic, ML-based, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Predefined metric implementations
- File: `docs/zh/advanced_guides/add_benchmark.md`
- Code Reference:
```python
metric_list=['acc']  # Accuracy metric
match_score() / llm_match_score()  # Score matching functions
RegexFilter  # Answer extraction using regex patterns
```
The framework implements predefined statistical metrics including accuracy calculations, score matching functions, and regex-based answer extraction. These deterministic functions compute scores based on mathematical formulas (accuracy = correct/total) and string matching algorithms. The `RegexFilter` class uses pattern matching to extract structured answers from model outputs, representing a rule-based algorithmic approach to evaluation. BLEU and ROUGE metrics mentioned in the documentation further demonstrate algorithmic scoring based on n-gram overlap calculations.

Evidence 2: Retrieval and classification metrics
- File: `docs/zh/user_guides/backend/rageval_backend/clip_benchmark.md`
- Code Reference:
```
recall@k  # Recall metric for retrieval tasks
acc@k     # Accuracy metric for classification tasks
```
The system employs algorithmic metrics for zero-shot retrieval tasks using recall@k (measuring the proportion of relevant items found in top-k results) and zero-shot classification tasks using acc@k (measuring top-k accuracy). These are deterministic calculations following established information retrieval formulas: recall@k = |relevant ∩ retrieved@k| / |relevant|. The mathematical foundation of these metrics makes them purely algorithmic evaluators without learned parameters.

Evidence 3: Image quality scoring functions
- File: `docs/zh/best_practice/t2i_eval.md`
- Code Reference:
```
Models: MPS[1], HPSv2.1Score[2]
Metrics: 图像真实性、文本-图像对齐度
```
The framework uses mathematical scoring functions for assessing image quality dimensions including realism and text-image alignment. While some models like MPS and HPSv2.1Score may incorporate learned components, the evaluation metrics themselves are computed through deterministic mathematical formulas that aggregate multiple quality indicators into final scores, representing the algorithmic evaluation layer.

---

### ML-based

Evidence 1: LLM-as-judge deployment
- File: `docs/zh/best_practice/think_eval.md`
- Code Reference:
```python
judge_config = dict(
    api_key='EMPTY',
    base_url='http://0.0.0.0:8801/v1',
    model_name='Qwen2.5-72B-Instruct',
)
```
The framework deploys Qwen2.5-72B-Instruct as a judge model to detect the earliest position of correct answers in reasoning processes, following ProcessBench's methodology. This represents a trained neural network evaluator that uses learned language understanding capabilities to assess correctness and reasoning quality. The model acts as an automated judge, replacing human annotators by leveraging its pre-trained knowledge to evaluate model outputs through inference rather than algorithmic rules.

Evidence 2: Conditional judge model evaluation
- File: `docs/zh/user_guides/backend/vlmevalkit_backend.md`
- Code Reference:
```yaml
LOCAL_LLM: qwen2-7b-instruct  # 裁判员模型的 model_id
```
The system implements a hybrid evaluation approach where an LLM judge model (qwen2-7b-instruct) is conditionally deployed for evaluation. When the judge model is unavailable, the framework falls back to post-processing with exact matching, demonstrating that the ML-based evaluator provides more sophisticated assessment capabilities. The judge model uses learned representations to evaluate outputs beyond simple string matching, enabling nuanced judgment of response quality.

Evidence 3: Multimodal ML evaluation models
- File: `docs/zh/best_practice/t2i_eval.md`
- Code Reference:
```
FGA-BLIP2  # 自动化评分模型
MPS, HPSv2.1Score  # Image evaluation models
Qwen3-235B-A22B  # Report generation model
```
The evaluation pipeline employs multiple trained ML models: FGA-BLIP2 as the primary automated scoring model for text-to-image tasks, MPS and HPSv2.1Score for assessing image quality dimensions, and Qwen3-235B-A22B for generating intelligent evaluation reports. These are neural networks trained on specific tasks that use learned features to evaluate outputs, representing sophisticated ML-based evaluators that go beyond deterministic metrics.

Evidence 4: Embedding-based similarity evaluation
- File: `docs/zh/user_guides/backend/rageval_backend/clip_benchmark.md`
- Model: `AI-ModelScope/chinese-clip-vit-large-patch14-336px`
CLIP models serve as evaluators for multimodal tasks by computing learned embeddings for both images and text, then measuring similarity in the shared embedding space. This evaluation approach relies entirely on the model's pre-trained representations rather than hand-crafted features or algorithmic rules. The neural network has learned semantic correspondences between modalities during training, enabling it to assess alignment quality through embedding similarity.

---

### Environmental

Evidence 1: Speed benchmarking through service execution
- File: `docs/en/user_guides/stress_test/speed_benchmark.md`
- Code Reference:
```
API endpoint: /v1/completions
Metric: 速度测试（模型在单个请求下的标准速度）
```
The framework performs speed benchmarking by executing actual API calls to deployed model services and measuring response times. This environmental evaluation depends on real system behavior including network latency, server load, and model inference time. The evaluation is not simulated but relies on actual execution in the deployment environment, measuring performance characteristics that only manifest during live system interaction.

Evidence 2: Inference execution with system hooks
- File: `docs/zh/advanced_guides/add_benchmark.md`
- Code Reference:
```python
run_inference()
├── _on_inference_start() [钩子方法]
├── _on_inference() [钩子方法]
└── _on_inference_end() [钩子方法]
```
The evaluation framework includes hook methods that capture environmental feedback during model inference execution. These hooks enable monitoring of system state, resource usage, and execution flow during actual model inference. The framework receives real-time feedback from the inference environment including completion status, errors, and timing information. This represents environmental evaluation where the execution context itself provides validation signals beyond just output correctness.

Evidence 3: Code execution validation
- File: `docs/zh/best_practice/eval_qwq.md`
- Code Reference:
```
LiveCodeBench evaluation
Metric: Pass@1
```
The framework uses LiveCodeBench to evaluate code generation capabilities by executing model-generated code in an actual runtime environment and measuring successful execution with the Pass@1 metric. This environmental evaluator runs code through compilers/interpreters, captures execution results including runtime errors and output correctness, and provides binary pass/fail feedback based on test case execution. The evaluation fundamentally depends on environmental execution rather than static code analysis or learned assessment.