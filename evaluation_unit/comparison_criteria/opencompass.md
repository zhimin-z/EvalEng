## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, Comparative Baseline, None, Custom]

## Detailed Analysis

### Explicit Labels

Evidence 1: Dataset Configuration with Reference Answers
- File: `opencompass/datasets/`
- Code Reference: `govrepcrs_eval_cfg` configuration
```python
govrepcrs_eval_cfg = dict(
    evaluator=dict(type=BleuEvaluator),
    pred_role='BOT',
    pred_postprocessor=dict(type=general_cn_postprocess),
    dataset_postprocessor=dict(type=general_cn_postprocess))
```
Dataset files contain explicit reference answers and standard evaluation configurations. The evaluator compares model predictions against predetermined correct answers using metrics like BLEU.

Evidence 2: Reference Answer Column Specification
- File: `docs/zh_cn/user_guides/metrics.md`
- Code Reference: Dataset reading configuration
```python
govrepcrs_reader_cfg = dict(
    input_columns=['prompt'], 
    output_column='answer'  # Reference answer column
)
```
Dataset reading configuration specifies `output_column='answer'` as the reference answer column, providing explicit ground truth labels for evaluation.

Evidence 3: Standard Evaluation Metrics
- File: `docs/en/user_guides/metrics.md`
- Code Reference: Metric descriptions
```
- ACCEvaluator: "Common in classification tasks... Accuracy is usually used as the evaluation standard"
- EMEvaluator: "Common in Q&A and reading comprehension tasks... Matching rate is usually used"
- Datasets with explicit labels: MMLU, CEval, ARC, CLUE_CMRC, CLUE_DRCD, DROP, etc.
```
Evaluators like ACCEvaluator, EMEvaluator, BleuEvaluator, and RougeEvaluator compare predictions against predetermined correct answers from datasets, implementing explicit label-based evaluation.

Evidence 4: ChemBench Accuracy Metrics
- File: `examples/eval_chembench.py`
- Code Reference: Accuracy results
```
ChemBench_Name_Conversion... accuracy... 45.43
```
Shows accuracy metrics computed against standard answers, demonstrating explicit label comparison for benchmark evaluation.

---

### Behavioral Specification

Evidence 1: Code Evaluation Configuration
- File: `docs/zh_cn/advanced_guides/code_eval.md`
- Code Reference: HumanEval evaluator setup
```python
from opencompass.datasets import HumanevalXDataset, HumanevalXEvaluator

humanevalx_eval_cfg_dict = {
    lang : dict(
        evaluator=dict(
            type=HumanevalXEvaluator,
            language=lang,
            ip_address="localhost",
            port=5000),
        pred_role='BOT')
}
```
Configures code evaluation with executable test cases through HumanEval evaluator, implementing behavioral specification for code generation tasks.

Evidence 2: Code Execution Environment
- File: `docs/en/advanced_guides/code_eval_service.md`
- Code Reference: Evaluation service description
```
"To complete the LLM code capability evaluation, we need to build a separate evaluation environment"
"Common in code generation tasks... Execution pass rate and `pass@k` are usually used as the evaluation standard"
```
Uses `HumanEvalEvaluator` and `MBPPEvaluator` with execution pass rates, validating functional correctness through test suite execution rather than static comparison.

Evidence 3: Docker-Based Test Execution
- File: `docs/zh_cn/advanced_guides/code_eval_service.md`
- Code Reference: Docker execution command
```shell
docker run -it -p 5000:5000 code-eval-{your-dataset}:latest python server.py
```
Provides isolated execution environment for running generated code against tests. This implements behavioral validation by executing model outputs against predefined test cases to verify functional correctness.

Evidence 4: Pass@k Metric Implementation
- File: `docs/zh_cn/advanced_guides/code_eval.md`
- Code Reference: Test suite execution
Mentions `humaneval_postprocess` and pass@k metrics where code is executed against test cases to validate functional correctness, implementing executable specification for behavioral assessment.

---

### Comparative Baseline

Evidence 1: Pairwise Comparison Mode
- File: `docs/zh_cn/advanced_guides/subjective_evaluation.md`
- Code Reference: Compare mode description
```
"Compare模式：将模型的回答进行两两比较，以计算对战其胜率"
(Compare mode: pairwise comparison to calculate win rate)
"AlpacaEvalv2 英文Compare数据集"
"ArenaHard 英文Compare数据集"
```
Implements pairwise comparison framework where model responses are compared to calculate win rates, following Chatbot Arena methodology for relative performance assessment.

Evidence 2: Model Comparison Framework
- File: `docs/en/advanced_guides/subjective_evaluation.md`
- Code Reference: Comparative evaluation
```
"Compare Mode: comparing model responses pairwise to calculate their win rate"
```
Establishes comparative baseline evaluation through pairwise model comparison, enabling relative quality assessment against baseline systems.

Evidence 3: Contamination Reference Sets
- File: `docs/zh_cn/advanced_guides/contamination_eval.md`
- Code Reference: Reference model configuration
```python
from .datasets.gsm8k_contamination.gsm8k_contamination_ppl_ecdd22 import gsm8k_datasets  
# includes training, test, and reference sets
```
Uses reference model perplexities for comparison in contamination detection, with "参考集" (reference set) serving as comparative baseline.

Evidence 4: Multi-Model Performance Comparison
- File: `docs/zh_cn/advanced_guides/longeval.md`
- Code Reference: Model comparison results
```
"GPT-4 和 GPT-3.5-turbo-16k在长文本任务中仍然占据领先地位"
Performance tables comparing: XGen-7B-8k, Vicuna-7b-v1.5-16k, LongChat-7b-v1.5-32k, ChatGLM2-6B-32k
```
Compares different models' performance on long-context tasks, establishing baseline comparisons through relative rankings and competitive evaluation.

---

### None

Evidence 1: Perplexity Measurement
- File: `docs/en/user_guides/metrics.md`
- Code Reference: Intrinsic metric reference
```
Reference to perplexity measurement: "average_ppl"
```
Perplexity measurement evaluates intrinsic model properties without external references, providing self-contained quality assessment.

Evidence 2: Contamination Perplexity Assessment
- File: `docs/zh_cn/advanced_guides/contamination_eval.md`
- Code Reference: Perplexity results
```text
dataset          version    metric       mode       internlm-7b-hf
---------------  ---------  -----------  -------  ----------------
gsm8k-train-ppl  0b8e46     average_ppl  unknown              1.5
```
Perplexity calculation without external references measures intrinsic data fit, used for contamination detection through internal consistency assessment.

Evidence 3: Inference Efficiency Metrics
- File: `docs/en/advanced_guides/evaluation_lmdeploy.md`
- Code Reference: Performance measurements
References to inference acceleration and latency measurements in performance discussions, providing intrinsic operational metrics without comparison to external standards.

---

### Custom

Evidence 1: LLM-as-Judge Framework
- File: `docs/zh_cn/advanced_guides/objective_judgelm_evaluation.md`
- Code Reference: Judge configuration
```python
eval_cfg = dict(
    evaluator=dict(
        type=LMEvaluator,
        pred_postprocessor=dict(type=math_judement_preprocess),
        prompt_template=dict(
            type=PromptTemplate,
            template=dict(round=[
                dict(role='HUMAN', prompt=eng_obj_prompt),
            ]),
        ),
    ),
    pred_role="BOT",
)
```
Uses another LLM to evaluate outputs, combining comparative baseline evaluation with behavioral specification through specialized judgment pipelines.

Evidence 2: Generic LLM Judge Configuration
- File: `docs/en/advanced_guides/llm_judge.md`
- Code Reference: Generic evaluator setup
```python
eval_cfg = dict(
    evaluator=dict(
        type=GenericLLMEvaluator,
        prompt_template=dict(...),
        dataset_cfg=dict(...),
        judge_cfg=YOUR_JUDGE_MODEL_CONFIG,
        dict_postprocessor=dict(type=generic_llmjudge_postprocess),
    ),
)
```
Implements configurable LLM-based evaluation with custom prompts and judge models, creating specialized hybrid evaluation pipelines.

Evidence 3: Cascade Evaluator Hybrid
- File: `docs/en/advanced_guides/llm_judge.md`
- Code Reference: Cascade configuration
```python
cascade_evaluator = dict(
    type=CascadeEvaluator,
    llm_evaluator=llm_judge_evaluator,
    rule_evaluator=rule_evaluator,
    parallel=False
)
```
Combines rule-based and LLM-based evaluation in multi-stage pipeline, creating custom hybrid approach that integrates explicit rules with model-based judgment.

Evidence 4: Circular Evaluation Strategy
- File: `docs/en/advanced_guides/circular_eval.md`
- Code Reference: Circular dataset configuration
```python
class CircularCEvalDataset(CEvalDataset, metaclass=CircularDatasetMeta):
    dataset_class = CEvalDataset
    default_circular_splits = ['val', 'test']
    default_option_keys = ['A', 'B', 'C', 'D']
```
Custom augmentation strategy with shuffled options implementing hybrid evaluation combining multiple passes, extending standard explicit label evaluation with specialized robustness testing.

Evidence 5: Multi-Stage NeedleBench Evaluation
- File: `docs/zh_cn/advanced_guides/needleinahaystack_eval.md`
- Code Reference: Multi-tier task structure
```
- Single-Needle, Multi-Needle, Multi-Needle Reasoning tasks
- Ancestral Trace Challenge with complex logic chains
- Domain-specific evaluation for long-context tasks
```
Domain-specific evaluation pipeline with multiple complexity tiers, creating specialized framework for long-context assessment through progressive difficulty stages.

Evidence 6: Subjective Evaluation with Custom Rubrics
- File: `docs/zh_cn/advanced_guides/subjective_evaluation.md`
- Code Reference: Specialized scoring systems
```
- Custom evaluation templates for different capabilities
- AlignBench, MTBench with specialized scoring rubrics
- Multi-stage evaluation pipelines
```
Implements custom multi-stage evaluation pipelines with specialized scoring rubrics for subjective assessment, combining comparative baseline with domain-specific criteria through configurable templates.