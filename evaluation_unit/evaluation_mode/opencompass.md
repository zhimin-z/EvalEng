## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Text-based Evaluation Metrics
- Files: `docs/zh_cn/user_guides/metrics.md`, `docs/en/user_guides/metrics.md`
- Code References:
  - `ACCEvaluator` - Accuracy evaluation for classification/multiple choice
  - `EMEvaluator` - Exact match evaluation for Q&A tasks
  - `BleuEvaluator` - BLEU score for translation tasks
  - `RougeEvaluator` - ROUGE score for summarization tasks
  - Located in `opencompass/openicl/icl_evaluator`
These evaluators perform static analysis on model outputs by comparing them against reference answers through text matching, similarity scoring, and pattern matching. They inspect outputs without executing any generated code or artifacts.

Evidence 2: LLM-as-Judge Evaluation
- Files: 
  - `docs/zh_cn/advanced_guides/llm_judge.md`
  - `docs/en/advanced_guides/llm_judge.md`
  - `docs/zh_cn/advanced_guides/objective_judgelm_evaluation.md`
  - `docs/en/advanced_guides/objective_judgelm_evaluation.md`
- Code References:
  - `GenericLLMEvaluator` class
  - `LMEvaluator` evaluator type
  - Used in math evaluation: `eval_math_llm_judge.py`
The LLM-as-Judge mechanism uses language models to evaluate outputs through prompt-based comparison. It performs static analysis by having a judge model assess the semantic similarity and correctness of responses without executing them. The judge model outputs decisions like "[Yes]" or "[No]" based on text comparison.

Evidence 3: Subjective Evaluation
- Files: 
  - `docs/zh_cn/advanced_guides/subjective_evaluation.md`
  - `docs/en/advanced_guides/subjective_evaluation.md`
- Code References:
  - AlignBench scoring dataset
  - MTBench scoring dataset
  - Compare mode and Score mode evaluations
Subjective evaluation uses JudgeLLM to assess model outputs through text-based comparison and scoring, without executing the generated content. It's a form of static analysis where outputs are judged based on their textual properties.

---

### Dynamic Execution

Evidence 1: Code Execution for Humaneval
- Files: 
  - `docs/zh_cn/advanced_guides/code_eval.md`
  - `docs/en/advanced_guides/code_eval.md`
  - `docs/zh_cn/advanced_guides/code_eval_service.md`
  - `docs/en/advanced_guides/code_eval_service.md`
- Code References:
  - `HumanEvalEvaluator` - Executes generated code and calculates pass@k
  - `MBPPEvaluator` - Execution pass rate evaluation
  - Code evaluation service: `https://github.com/open-compass/code-evaluator`
  - Dataset configs: `configs/datasets/humaneval/humaneval_gen_8e312c.py`
The harness executes model-generated code in controlled environments (Docker containers) to verify correctness. The code evaluation service runs the generated programs, tests them against test cases, and returns execution results. This is clear dynamic execution of model artifacts.

Evidence 2: Multi-language Code Evaluation
- Files: `docs/zh_cn/advanced_guides/code_eval_service.md`
- Code References:
  - `HumanevalXDataset` - Multi-language code evaluation
  - Supported languages: Python, C++, Go, Java, JavaScript
  - `HumanevalXEvaluator` with execution backend
The system executes code in multiple programming languages within sandboxed environments. It compiles and runs generated programs to verify their correctness, which is dynamic execution of model outputs.

Evidence 3: DS1000 Dataset Evaluation
- Files: 
  - `docs/zh_cn/advanced_guides/code_eval_service.md`
  - `docs/en/advanced_guides/code_eval_service.md`
- Code References:
  - DS1000 dataset for Python algorithm libraries
  - Execution of SQL queries, scripts, and programs
  - Sandbox/container execution environment
The DS1000 evaluation involves executing model-generated Python code that uses various algorithm libraries (Pandas, Numpy, etc.). The generated code is run in controlled environments to validate functionality.