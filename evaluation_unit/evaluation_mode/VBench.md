## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: CLIP Score Computation
- File: `competitions/clip_score.py`
- Function: `clip_alignment()`, `compute_clip_score()`
- Code Reference:
```python
def clip_alignment(clip_model, video_dict, preprocess, device):
    sim = []
    for info in tqdm(video_dict):
        query = info["prompt"]
        text = clip.tokenize([query], truncate=True).to(device)
        text_feature = clip_model.encode_text(text)
        text_feature = F.normalize(text_feature, dim=-1)
        
        video_list = info["video_list"]
        for video_path in video_list:
            with torch.no_grad():
                images = read_frames_decord_by_fps(video_path, num_frames=8, sample="middle")
                images = image_transform(images)
                images = images.to(device)
                
                image_features = clip_model.encode_image(images)
                image_features = F.normalize(image_features, dim=-1, p=2)
                video_sim = image_features @ text_feature.T
                video_sim = np.mean(video_sim.cpu().tolist())
                sim.append(video_sim)
```
This implements static analysis by computing CLIP similarity scores between video frames and text prompts. The code extracts features from videos and text, then calculates cosine similarity without executing any model-generated code. It's purely feature comparison and scoring.

Evidence 2: Evaluation Metric Computation
- File: `VBench-2.0/vbench2/third_party/Instance_detector/swift/plugin/metric.py`
- Function: `compute_rouge_bleu()`, `compute_acc()`, `compute_acc_metrics()`
- Code Reference:
```python
def compute_rouge_bleu(preds: List[str], labels: List[str]):
    import jieba
    from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
    from rouge.rouge import Rouge
    score_dict = {key: MeanMetric() for key in ['rouge-1', 'rouge-2', 'rouge-l', 'bleu-4']}

    for pred, label in zip(preds, labels):
        hypothesis = list(jieba.cut(pred))
        reference = list(jieba.cut(label))
        if not hypothesis or not reference:
            continue
        rouge = Rouge()
        scores = rouge.get_scores(' '.join(hypothesis), ' '.join(reference))[0]
        for k, v in scores.items():
            score_dict[k].update(v['f'])
        bleu_score = sentence_bleu([list(label)], list(pred), smoothing_function=SmoothingFunction().method3)
        score_dict['bleu-4'].update(bleu_score)
```
These functions perform static analysis on model outputs by computing ROUGE, BLEU, and accuracy metrics through text comparison and pattern matching without executing any generated code.

Evidence 3: Evaluation Framework Integration
- File: `VBench-2.0/vbench2/third_party/Instance_detector/swift/llm/eval/eval.py`
- Class: `SwiftEval`
- Code Reference:
```python
def get_task_result(self, task_cfg: TaskConfig):
    run_task(task_cfg=task_cfg)
    reports = Summarizer.get_report_from_cfg(task_cfg=task_cfg)
    result = {}
    if task_cfg.eval_backend == EvalBackend.OPEN_COMPASS:
        for report in reports:
            if report[self.args.model_suffix] != '-':
                result[report['dataset']] = {report['metric']: report[self.args.model_suffix]}
```
The evaluation framework orchestrates static analysis evaluations across multiple backends (Native, OpenCompass, VLMEvalKit), comparing model outputs against reference answers using metrics.

Evidence 4: Custom Dataset Evaluation
- File: `VBench-2.0/vbench2/third_party/Instance_detector/docs/source_en/Instruction/Evaluation.md`
- Documentation describing static evaluation for custom datasets including multiple-choice questions (MCQ) evaluated by accuracy comparison, question-and-answer (QA) evaluated by ROUGE and BLEU metrics, format validation for CSV and JSONL files, and string matching and pattern checking without code execution.

Evidence 5: Report Generation
- File: `VBench-2.0/vbench2/third_party/Instance_detector/scripts/benchmark/generate_report.py`
- Function: `generate_sft_report()`, `generate_export_report()`
- Code Reference:
```python
def generate_sft_report(outputs: List[ModelOutput]):
    gsm8k_accs = []
    arc_accs = []
    ceval_accs = []
    for output in outputs:
        gsm8k_acc = None
        arc_acc = None
        ceval_acc = None
        for report in (output.reports or []):
            if report['name'] == 'gsm8k':
                gsm8k_acc = report['score']
            if report['name'] == 'arc':
                arc_acc = report['score']
```
These functions perform static analysis on evaluation results by comparing metrics, calculating statistics, and generating formatted reports.

---

### Dynamic Execution

Evidence 1: Anomaly Detection with Video Execution
- File: `VBench-2.0/vbench2/third_party/Instance_detector/swift/ui/llm_eval/eval.py` and `VBench-2.0/vbench2/third_party/Instance_detector/swift/ui/llm_eval/llm_eval.py`
- Class: `Eval`, `LLMEval`
- Function: `evaluate_model()`, `eval_model()`
- Code Reference:
```python
def eval_model(cls, *args):
    run_command, eval_args, log_file = cls.eval(*args)
    os.system(run_command)  # Executes the evaluation command
    time.sleep(2)
    return gr.update(open=True), EvalRuntime.refresh_tasks(log_file)
```
The evaluation system deploys models and executes inference tasks dynamically. The system can start model servers, run inference requests, and evaluate outputs - this involves executing model-generated responses.

Evidence 2: Model Deployment and API Execution
- File: `VBench-2.0/vbench2/third_party/Instance_detector/swift/llm/eval/eval.py`
- Class: `SwiftEval`
- Method: `run()`
- Code Reference:
```python
def run(self):
    args = self.args
    eval_report = {}
    deploy_context = nullcontext() if args.eval_url else run_deploy(args, return_url=True)
    with deploy_context as base_url:
        base_url = args.eval_url or base_url
        url = f"{base_url.rstrip('/')}/chat/completions"
        
        task_cfg = self.get_task_cfg(args.eval_dataset, args.eval_backend, url)
        result = self.get_task_result(task_cfg)
```
The evaluation harness deploys models as services and executes API calls to generate responses, which are then evaluated. This involves dynamic execution of model inference.

Evidence 3: Test Execution Framework
- File: `tests/eval/test_eval.py`, `tests/infer/test_infer.py`, `tests/deploy/test_dataset.py`
- Code Reference:
```python
def test_eval_native():
    from swift.llm import EvalArguments, eval_main
    eval_main(
        EvalArguments(
            model='Qwen/Qwen2.5-0.5B-Instruct',
            eval_dataset='arc',
            infer_backend=infer_backend,
            eval_backend='Native',
            eval_limit=10,
            eval_generation_config={
                'max_new_tokens': 128,
                'temperature': 0.1
            },
        ))
```
These test files execute model inference dynamically, running models on datasets and capturing outputs for evaluation.

Evidence 4: Video Processing and Execution
- File: `VBench-2.0/vbench2/third_party/Instance_detector/swift/ui/llm_eval/eval.py`
- Code Reference:
```python
def infer_lora(engine, request_config, infer_request: 'InferRequest'):
    resp_list = engine.infer([infer_request], request_config)
    response = resp_list[0].choices[0].message.content
    return response
```
The system processes and executes video inference tasks, including frame extraction and model prediction on video content.

Evidence 5: Dynamic Model Inference with Multiple Backends
- File: `tests/infer/test_infer.py`, `tests/deploy/test_logprobs.py`
- Code Reference:
```python
def test_infer(infer_backend):
    from swift.llm import RequestConfig
    from swift.plugin import InferStats
    engine, template, infer_requests = _prepare(infer_backend=infer_backend)
    request_config = RequestConfig(temperature=0)
    infer_stats = InferStats()

    response_list = engine.infer(
        infer_requests, template=template, request_config=request_config, metrics=[infer_stats])
```
These tests dynamically execute model inference across different backends (pt, vllm, lmdeploy) and evaluate the generated outputs.