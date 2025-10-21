## Evaluator Categories

[Algorithmic, Human, ML-based, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Performance measurement metrics
- File: Performance monitoring throughout the system
- Code Reference:
```javascript
tokensPerSecond
```
The harness provides algorithmic performance metrics such as tokens-per-second measurements that deterministically quantify model inference speed. These metrics use mathematical formulas to compute throughput rates based on token count and elapsed time, providing reproducible and objective performance assessments without requiring external judgment or comparison baselines.

Evidence 2: Basic accuracy and statistical evaluators
- File: `docs/en/user_guides/metrics.md` and `docs/zh_cn/user_guides/metrics.md`
- Code Reference:
```
| `ACCEvaluator`        | Accuracy             | `first_capital_postprocess`  | agieval, ARC, bbh, mmlu, ceval, commonsenseqa, crowspairs, hellaswag |
| `EMEvaluator`         | Match Rate           | None, dataset-specific       | drop, CLUE_CMRC, CLUE_DRCD                                           |
| `BleuEvaluator`       | BLEU                 | None, `flores`               | flores, iwslt2017, summscreen, govrepcrs                             |
| `RougeEvaluator`      | ROUGE                | None, dataset-specific       | truthfulqa, Xsum, XLSum                                              |
```
The documentation explicitly lists algorithmic evaluators including accuracy (ACCEvaluator), exact match (EMEvaluator), BLEU scores (BleuEvaluator), and ROUGE scores (RougeEvaluator). These are deterministic, rule-based metrics using mathematical formulas and string matching algorithms that provide consistent, reproducible evaluation through established computational measures.

Evidence 3: Code execution metrics
- File: `docs/en/user_guides/metrics.md`
- Code Reference:
```
| `HumanEvalEvaluator`  | pass@k               | `humaneval_postprocess`      | humaneval_postprocess                                                |
| `MBPPEvaluator`       | Execution Pass Rate  | None                         | mbpp                                                                 |
```
Code evaluation using pass@k and execution pass rates are algorithmic metrics that compute statistical measures based on test execution results. These evaluators apply predefined statistical functions to determine the probability that generated code passes test cases, providing deterministic assessment of code generation quality.

Evidence 4: Statistical evaluators
- File: `docs/zh_cn/user_guides/metrics.md`
- Code Reference:
```
| `MATHEvaluator`       | Accuracy             | `math_postprocess`           | math                                                                 |
| `MccEvaluator`        | Matthews Correlation | None                         | --                                                                   |
| `AUCROCEvaluator`     | AUC-ROC              | None                         | jigsawmultilingual, civilcomments                                    |
```
These evaluators compute statistical metrics including Matthews Correlation Coefficient and AUC-ROC, which are deterministic mathematical functions. They provide quantitative assessment through established statistical formulas that ensure consistent evaluation across different runs and datasets.

Evidence 5: Configuration example
- File: `docs/zh_cn/user_guides/metrics.md`
- Code Reference:
```
govrepcrs_eval_cfg = dict(
    evaluator=dict(type=BleuEvaluator),            # Use the common translator evaluator BleuEvaluator
    pred_role='BOT',                               
    pred_postprocessor=dict(type=general_cn_postprocess),      
    dataset_postprocessor=dict(type=general_cn_postprocess))
```
This configuration demonstrates how algorithmic evaluators like BleuEvaluator are integrated into the evaluation pipeline. The setup shows the systematic use of predefined metrics with preprocessing steps, ensuring reproducible assessment through established computational measures.

---

### Human

Evidence 1: Manual model comparison mechanism
- Justification: ollama-grid-search is not a traditional evaluation harness since it does not automatically evaluate model outputs in its workflow. However, it qualifies as an evaluation harness because it provides systematic mechanisms that enable model developers to compare different models using various prompting techniques. In this framework, humans serve as the evaluators who make qualitative judgments about model performance across different parameter configurations and prompt variations. The harness facilitates structured human assessment by organizing model outputs for side-by-side comparison, capturing the subjective quality dimensions that automated methods cannot reliably assess. This human-in-the-loop evaluation approach addresses the goal of capturing preferences and subjective quality through expert judgment rather than algorithmic scoring.

---

### ML-based

Evidence 1: LLM-as-judge for subjective evaluation
- File: `docs/zh_cn/advanced_guides/subjective_evaluation.md`
- Code Reference:
```
为了探究模型的主观能力，我们采用了JudgeLLM作为人类评估者的替代品（[LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)）。
```
The harness explicitly supports using LLMs (like GPT-4) as judge models to evaluate subjective capabilities of other models, implementing the LLM-as-a-Judge paradigm. This approach leverages learned representations from large language models to provide nuanced assessment that captures semantic and contextual quality dimensions beyond what rule-based methods can measure, serving as a scalable alternative to human evaluation.

Evidence 2: Generic LLM evaluator
- File: `docs/en/advanced_guides/llm_judge.md`
- Code Reference:
```
eval_cfg = dict(
    evaluator=dict(
        type=GenericLLMEvaluator,  # Using LLM as evaluator
        prompt_template=dict(...),
        judge_cfg=YOUR_JUDGE_MODEL_CONFIG,  # Configuration for the judge model
        dict_postprocessor=dict(type=generic_llmjudge_postprocess),
    ),
)
```
GenericLLMEvaluator is a dedicated component for using ML models (specifically LLMs) to evaluate benchmark task outputs. The judge model performs inference to assess correctness and quality by processing both the task input and model output through a learned neural network. This ML-based approach enables evaluation of open-ended generation tasks where outputs may be semantically correct but lexically different from reference answers.

Evidence 3: LLM judge for objective evaluation
- File: `docs/zh_cn/advanced_guides/objective_judgelm_evaluation.md`
- Code Reference:
```
d['eval_cfg']= dict(
    evaluator=dict(
        type=LMEvaluator,
        pred_postprocessor=dict(type=math_judement_preprocess),
        prompt_template=dict(...),
    ),
    pred_role="BOT",
)
```
LMEvaluator uses language models to judge the equivalence of mathematical expressions, demonstrating ML-based evaluation for objective tasks where rule-based methods are insufficient. The evaluator leverages the model's learned mathematical reasoning capabilities to determine semantic equivalence between expressions that may be syntactically different, showcasing how ML-based evaluators can handle complex reasoning tasks.

Evidence 4: Environment variable configuration for judge models
- File: `docs/en/advanced_guides/llm_judge.md`
- Code Reference:
```bash
export OC_JUDGE_MODEL=Qwen/Qwen2.5-32B-Instruct
export OC_JUDGE_API_KEY=sk-1234
export OC_JUDGE_API_BASE=http://172.30.56.1:4000/v1
```
The harness provides infrastructure for configuring ML-based judge models via environment variables, indicating systematic support for ML-based evaluation. This configuration mechanism allows users to specify which trained models serve as evaluators, supporting both local and API-based judge models to leverage learned representations for assessment.

Evidence 5: Cascade evaluator with ML component
- File: `docs/en/advanced_guides/llm_judge.md`
- Code Reference:
```
cascade_evaluator = dict(
    type=CascadeEvaluator,
    llm_evaluator=llm_judge_evaluator,
    rule_evaluator=rule_evaluator,
    parallel=False
)
```
CascadeEvaluator combines rule-based and ML-based (LLM) evaluation in a hierarchical structure, where the LLM evaluator is used to re-assess samples that rule-based methods cannot confidently evaluate. This hybrid evaluation demonstrates how ML-based evaluators complement algorithmic approaches by handling edge cases and ambiguous outputs that require learned semantic understanding.

---

### Environmental

Evidence 1: Code execution environment
- File: `docs/zh_cn/advanced_guides/code_eval_service.md`
- Code Reference:
```
为了完成LLM代码能力评测，我们需要搭建一套独立的评测环境，避免在开发环境执行错误代码从而造成不可避免的损失。目前 OpenCompass 使用的代码评测服务可参考[code-evaluator](https://github.com/open-compass/code-evaluator)项目。
```
The harness uses an isolated execution environment (Docker-based code-evaluator service) to run model-generated code and capture execution results for benchmarks like HumanEval and MBPP. This environmental evaluation approach assesses performance through direct interaction with a sandboxed runtime system, where success signals come from actual code execution rather than pattern matching or learned representations.

Evidence 2: Code evaluator service configuration
- File: `docs/en/advanced_guides/code_eval_service.md`
- Code Reference:
```
humanevalx_eval_cfg_dict = {
    lang : dict(
            evaluator=dict(
                type=HumanevalXEvaluator,
                language=lang,
                ip_address="localhost",    # code_eval_server ip_address
                port=5000),               # code evaluation service
            pred_role='BOT')
    for lang in ['python', 'cpp', 'go', 'java', 'js']
}
```
HumanevalXEvaluator connects to an external execution service that runs model-generated code in a sandboxed environment and returns pass/fail results. This is environmental evaluation of code generation tasks where the environment (execution runtime) provides success signals by attempting to execute the code against test cases and returning whether the execution succeeded or failed.

Evidence 3: Docker service for code execution
- File: `docs/en/advanced_guides/code_eval_service.md`
- Code Reference:
```shell
docker run -it -p 5000:5000 code-eval-{your-dataset}:latest python server.py
curl -X POST -F 'file=@./examples/humanevalx/python.json' -F 'dataset=humanevalx/python' localhost:5000/evaluate
```
The harness launches a Docker container that acts as an execution environment for evaluating model-generated code. The service endpoint receives code and returns execution results (pass@k metrics), demonstrating system-provided feedback where the Docker environment serves as the ground truth for code correctness through actual runtime behavior.

Evidence 4: Multiple language execution support
- File: `docs/zh_cn/advanced_guides/code_eval.md`
- Code Reference:
```
目前支持的语言有`python`, `cpp`, `go`, `java`, `js`。
```
The code evaluation infrastructure supports multiple programming languages, requiring separate execution environments for each language to validate model-generated code. Each language runtime serves as a distinct environmental evaluator that provides language-specific success signals based on compilation success, runtime behavior, and test case outcomes.

Evidence 5: Pass@k evaluation via execution
- File: `docs/en/advanced_guides/code_eval.md`
- Code Reference:
```
mbpp_datasets[0]['eval_cfg']['evaluator']['type'] = MBPPPassKEvaluator
```
MBPPPassKEvaluator and pass@k metrics rely on executing model-generated code multiple times in an environment and checking if the code passes test cases. This is environmental evaluation where assessment comes from direct interaction with the execution environment rather than static analysis, with success determined by whether the code produces correct outputs when run against test inputs in the target system.