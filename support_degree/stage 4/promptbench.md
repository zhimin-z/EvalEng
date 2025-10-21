# PromptBench - Stage 4 (EVALUATE) Evaluation

## Summary
PromptBench is a comprehensive evaluation framework for Large Language Models focused on prompt robustness and adversarial testing. It provides basic metric computation capabilities with standardized interfaces but lacks advanced validation, aggregation, and comparison features expected of a mature evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation present. Basic projection functions defined but no systematic validation framework |
| S4F2: Metric Computation | 2 | Core metrics implemented but limited coverage. Per-sample scoring absent in most cases |
| S4F3: Evaluator Models | 1 | LLM-as-judge capabilities exist but no dedicated evaluation-specific features |
| S4F4: Multi-Modal Scoring | 2 | Multi-modal support exists but limited metric coverage |
| S4F5: Aggregate Statistics | 1 | Basic aggregation only, no statistical testing or advanced comparisons |

---

## Detailed Analysis

### S4F1: Output Validation and Normalization (1/3)

Evidence of minimal validation:

1. Basic projection functions in examples (`examples/basic.ipynb`):
```python
def proj_func(pred):
    mapping = {
        "positive": 1,
        "negative": 0
    }
    return mapping.get(pred, -1)
```
- Simple mapping but no schema validation
- Returns -1 for unknown values (basic error handling)

2. Output processing utilities (`promptbench/utils/dataprocess.py` - referenced in docs):
```python
# From docs/examples/basic.md
pred = pb.OutputProcess.cls(raw_pred, proj_func)
```
- Single output processing function
- No format validation mentioned
- No policy compliance checks

3. DyVal processing (docs/examples/dyval.md):
```python
# dyval preds are processed differently, please refer to the source code
pred = process_dyval_preds(raw_pred)
```
- Task-specific processing exists
- No documentation of validation rules

Missing features:
- No malformed JSON/XML detection mentioned
- No schema validation framework
- No policy compliance checks (harmful content, etc.)
- No anomaly detection
- Limited normalization capabilities

Rating justification: While basic projection functions exist, there's no comprehensive validation framework. The system relies on manual projection function definition per task, which is error-prone and doesn't scale.

---

### S4F2: Task-Specific Metric Computation (2/3)

Evidence of metric coverage:

1. Supported datasets (README.md):
```python
SUPPORTED_DATASETS = [
    'cola', 'sst2', 'qqp', 'mnli', 'qnli', 'wnli', 'rte', 'mrpc',  # Classification
    'mmlu', 'squad_v2',  # QA
    'un_multi', 'iwslt',  # Translation
    'math', 'gsm8k',  # Math reasoning
    'bool_logic', 'valid_parentheses',  # Logical reasoning
    'vqav2', 'nocaps', 'mmmu'  # Multi-modal
]
```

2. Evaluation functions (docs/examples/basic.md):
```python
# Classification accuracy
score = pb.Eval.compute_cls_accuracy(preds, labels)
```

3. DyVal evaluation (docs/examples/dyval.md):
```python
score[order] = dyval_evaluate(dataset.dataset_type, preds, answers)
```

4. Metric library reference (promptbench/metrics/):
```
promptbench/metrics/
├── bleu/
├── cider/
├── squad_v2/
├── vqa/
└── eval.py
```

Missing features:
- No per-sample score storage documented
- Limited metric composition
- No explicit documentation of all available metrics
- No custom metric definition examples beyond projection functions

Rating justification: The framework supports multiple task types with appropriate metrics (classification, QA, translation). However, the documentation doesn't clearly enumerate all metrics, and per-sample scoring isn't prominently featured. The modular metric structure is present but not fully documented.

---

### S4F3: Evaluator Model Integration (1/3)

Evidence of LLM support:

1. Model loading (docs/examples/basic.md):
```python
model = pb.LLMModel(model='google/flan-t5-large', max_new_tokens=10, temperature=0.0001)
```

2. Supported models (README.md):
```python
SUPPORTED_MODELS = [
    'google/flan-t5-large', 'llama2-7b', 'llama2-7b-chat',
    'phi-1.5', 'phi-2', 'gpt-3.5-turbo', 'gpt-4',
    'vicuna-7b', 'vicuna-13b', 'gemini-pro'
]
```

3. MPA agents (examples/mpa.ipynb):
```python
paraphraser = LLMModel("gpt-4-turbo", max_new_tokens=1000, temperature=0.7)
evaluator = LLMModel("gpt-4-turbo", max_new_tokens=1000, temperature=0)

paraphrase_question_agent = ParaphraserAgent(paraphraser, prompt, input_process, output_process)
evaluate_question_agent = EvaluatorAgent(evaluator, prompt, input_process, output_process)
```

Missing features:
- No pre-built judge prompts for general evaluation
- No multi-aspect scoring frameworks
- No ensemble scoring mechanisms
- No rationale capture documented
- No evaluation-specific features beyond basic model calls

Rating justification: While the framework can call LLMs and has agent-based evaluation in MPA, it lacks dedicated evaluation features like pre-built judge prompts, multi-aspect scoring, or rationale capture. The MPA module shows promise but is focused on paraphrasing rather than general evaluation.

---

### S4F4: Multi-Modal Scoring Protocols (2/3)

Evidence of multi-modal support:

1. Multi-modal datasets (README.md):
```python
Multi-modal datasets:
- VQAv2
- NoCaps
- MMMU
- MathVista
- AI2D
- ChartQA
- ScienceQA
```

2. Multi-modal models (docs/examples/multimodal.md):
```python
SUPPORTED_MODELS_VLM = [
    'Salesforce/blip2-opt-2.7b',
    'llava-hf/llava-1.5-7b-hf',
    'gemini-pro-vision',
    'gpt-4-vision-preview',
    'Qwen/Qwen-VL-Chat',
    'internlm/internlm-xcomposer2-vl-7b'
]
```

3. Multi-modal evaluation (docs/examples/multimodal.md):
```python
model = pb.VLMModel(model='llava-hf/llava-1.5-7b-hf', max_new_tokens=2048)
input_images = data['images']
raw_pred = model(input_images, input_text)
pred = pb.OutputProcess.pattern_split(raw_pred, 'ANSWER:')
score = pb.Eval.compute_cls_accuracy(preds, labels)
```

4. Metric directories (file structure):
```
promptbench/metrics/
├── vqa/
├── cider/
```

Missing features:
- No explicit image captioning metrics (CIDEr, SPICE) documented
- No CLIP score for image-text alignment
- No audio-text metrics
- No video understanding metrics
- Limited cross-modal metric documentation

Rating justification: The framework supports multiple vision-language models and datasets with appropriate evaluation. However, the metric coverage for multi-modal tasks isn't well-documented, and specialized metrics like CLIP score or image captioning metrics aren't explicitly mentioned in the documentation.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (1/3)

Evidence of aggregation:

1. Basic accuracy computation (docs/examples/basic.md):
```python
score = pb.Eval.compute_cls_accuracy(preds, labels)
print(f"{score:.3f}, {prompt}")
```

2. PromptEval results (examples/efficient_multi_prompt_eval.ipynb):
```python
result = efficient_eval(model, prompt_list, dataset, proj_func, budget=1200)
# Output includes:
{
    'full_performances': array([...]),
    'quantiles': {'5': 0.887, '25': 0.914, '50': 0.921, '75': 0.929, '95': 0.940},
    'average': 0.916,
    'std_dev': 0.024
}
```

3. Visualization (examples/efficient_multi_prompt_eval.ipynb):
```python
result = efficient_eval(model, prompt_list, dataset, proj_func, 
                        visualize=True)  # generates combined_result.png
```

Missing features:
- No pairwise significance testing
- No bootstrap confidence intervals
- No permutation tests
- No effect size computation
- No Elo/TrueSkill rankings
- No model comparison utilities
- No stratified statistics

Rating justification: The framework provides basic mean accuracy and the PromptEval module adds quantiles and standard deviation. However, there's no statistical testing, model comparison framework, or advanced aggregation. The efficient_eval function shows promise with quantile analysis and visualization, but lacks rigorous statistical comparison capabilities.

---

## Key Strengths

1. Diverse dataset support: 28+ datasets across multiple domains
2. Multi-modal capabilities: Vision-language models and datasets
3. Efficient evaluation: PromptEval module for sampling-based evaluation
4. Adversarial testing: Comprehensive prompt attack framework
5. Dynamic evaluation: DyVal for contamination mitigation

## Key Limitations

1. Minimal validation framework: No systematic output validation
2. Limited metric documentation: Metrics exist but aren't well-enumerated
3. No statistical testing: Lacks significance tests for comparisons
4. Basic aggregation: Only mean/std/quantiles, no advanced statistics
5. No per-sample analysis: Metrics are primarily aggregate-level
6. Limited evaluator features: No pre-built judge prompts or ensemble scoring

## Recommendations

1. Add validation layer: Implement systematic output validation with schema checking
2. Document metrics: Create comprehensive metric catalog with examples
3. Implement statistical testing: Add t-tests, bootstrap CI, permutation tests
4. Per-sample scoring: Enable detailed per-sample metric storage and analysis
5. Enhance evaluator framework: Add pre-built judge prompts and multi-aspect scoring
6. Model comparison: Implement pairwise comparison with significance testing