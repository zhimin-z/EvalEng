## Evaluator Categories

[Environmental, Algorithmic]

## Detailed Analysis

### Environmental

Evidence 1: Core code execution validation function
- File: `bigcode_eval/tasks/custom_metrics/code_eval.py`
- Function: `check_correctness()`
- Code Reference:
```python
# Function imported from execute.py
check_correctness()
```
This harness executes model-generated code in sandboxed environments to validate correctness. The `check_correctness()` function runs generated code against test cases and returns execution results (pass/fail). This is environmental evaluation because it uses runtime execution feedback from actual program execution to assess model outputs on code generation tasks, rather than comparing against static references or using predefined algorithms.

Evidence 2: Code execution infrastructure
- File: `bigcode_eval/tasks/custom_metrics/execute.py`
- Code Reference:
```python
# Imported in code_eval.py
from execute import check_correctness
```
The `check_correctness` function executes code with timeouts, capturing stdout/stderr and exit codes. This environmental evaluation infrastructure validates generated code by running it in a controlled runtime environment, observing actual program behavior rather than static analysis. The use of execution-based validation makes this fundamentally environmental as it depends on dynamic runtime feedback.

Evidence 3: Comprehensive sandbox execution system
- File: `bigcode_eval/tasks/custom_metrics/beyond_eval.py`
- Class/Function: `Sandbox.unsafe_execute()` method
- Code Reference:
```python
# Lines 105-188
def unsafe_execute(self, script, timeout):
    # Executes code with safety restrictions
    # Measures runtime
    # Captures output
    # Evaluates correctness
```
This implements a comprehensive code execution sandbox that runs model-generated Python code against test cases. It executes code with safety restrictions, measures runtime, captures output, and evaluates correctness. The `eval_string_script()` patterns throughout the multiple_metrics subdirectory all execute generated code in their respective language runtimes. This is environmental because correctness is determined by actual execution behavior in a controlled environment, with real-time monitoring of resource usage, output, and termination conditions.

Evidence 4: Multi-language execution evaluators
- File: `bigcode_eval/tasks/custom_metrics/multiple_metrics/eval_*.py`
- Code Reference:
```python
# Multiple evaluator modules across files:
eval_python.py    # executes Python via subprocess
eval_java.py      # compiles with javac, runs with java
eval_cpp.py       # compiles with g++, executes binary
eval_rust.py      # compiles with rustc, runs executable
eval_go.py        # runs Go tests
eval_javascript.py # executes with node
# ... and additional language evaluators
```
Multiple evaluator modules for different programming languages all execute model-generated code and return execution status (OK/Exception/Timeout/SyntaxError). This is environmental evaluation because each language-specific module interacts with the actual runtime environment for that language (compilers, interpreters, virtual machines), validating code through real execution rather than static analysis. The diversity of language runtimes demonstrates the environmental nature—each requires actual interaction with language-specific toolchains and execution environments.

Evidence 5: HumanEval benchmark execution
- File: `bigcode_eval/tasks/humaneval.py`
- Function: `process_results()` method
- Code Reference:
```python
# Lines 75-82
def process_results(self, ...):
    return compute_code_eval(...)  # Executes against unit tests
```
Calls `compute_code_eval()` which executes generated code against unit tests. The execution results determine pass@k metrics for the HumanEval benchmark. This is environmental because the HumanEval benchmark fundamentally relies on executing generated functions against predefined test cases—correctness is determined by whether the code produces the expected outputs when actually run, not by static comparison to reference solutions.

Evidence 6: Multi-language HumanEval execution
- File: `bigcode_eval/tasks/humanevalpack.py`
- Function: `process_results()` method
- Code Reference:
```python
# Lines 531-565
def process_results(self, ...):
    code_metric.compute()  # Executes in multiple languages
```
Uses the `code_metric.compute()` function from the evaluate library to execute generated code in multiple programming languages (Python, C++, JavaScript, Java, Go, Rust) with language-specific compilation and runtime validation. This is environmental evaluation because it requires actual compilation and execution in each target language's runtime environment, validating that generated code not only has correct syntax but actually runs and produces correct outputs across diverse language ecosystems.

Evidence 7: Instruction-based code execution
- File: `bigcode_eval/tasks/instruct_humaneval.py`
- Function: `process_results()` method
- Code Reference:
```python
# Lines 64-70
def process_results(self, ...):
    compute_code_eval()  # Executes solutions against test cases
```
Executes generated code solutions against test cases using `compute_code_eval()` for instruction-based code generation tasks. This is environmental because it evaluates whether code generated from natural language instructions actually functions correctly when executed, testing the model's ability to translate instructions into working code through runtime validation rather than static analysis.

Evidence 8: Student-written prompt execution
- File: `bigcode_eval/tasks/studenteval.py`
- Function: `_run_assembled_program()` and `process_results()` methods
- Code Reference:
```python
# Lines 48-74 and 126-161
def _run_assembled_program(self, ...):
    # Executes in temporary files with timeout
    # Captures exit codes and output
    
def process_results(self, ...):
    # Determines correctness from execution results
```
Executes student-written prompts' generated code in temporary files with timeout controls, capturing exit codes and output to determine correctness. This is environmental evaluation because it validates code generated from student-authored prompts by actually running the programs, observing their behavior, and checking outputs against expected results—the evaluation depends entirely on runtime execution feedback rather than static correctness criteria.

---

### Algorithmic

Evidence 1: Statistical pass@k calculation
- File: `bigcode_eval/tasks/custom_metrics/code_eval.py`
- Function: `estimate_pass_at_k()`
- Code Reference:
```python
# Lines 157-170
def estimate_pass_at_k(n, c, k):
    # Calculates probability using combinatorial formulas
    # Returns pass@k metric
```
This implements a statistical metric (pass@k) that calculates the probability of at least k correct solutions from n samples using combinatorial formulas. This is algorithmic evaluation because it applies a predefined mathematical function to aggregate execution results into a standardized metric. While the underlying correctness data comes from environmental execution, the pass@k calculation itself is a fixed algorithmic transformation that doesn't depend on runtime behavior—it's a deterministic statistical formula.

Evidence 2: Efficiency and pass rate metrics
- File: `bigcode_eval/tasks/custom_metrics/beyond_eval.py`
- Function: `estimate_pass_at_k()` and `estimate_beyond_at_k()`
- Code Reference:
```python
# Lines 272-292
def estimate_pass_at_k(...):
    # Implements pass@k calculation
    
def estimate_beyond_at_k(...):
    # Measures computational efficiency using statistical formulas
```
These implement algorithmic metrics including pass@k calculation and the Beyond@k metric which measures computational efficiency using statistical formulas on runtime measurements. This is algorithmic because both metrics apply predetermined mathematical transformations to execution data. The Beyond@k metric specifically uses algorithmic formulas to score efficiency, transforming raw runtime measurements into normalized scores through fixed computational procedures rather than through environmental interaction.

Evidence 3: Combinatorial pass@k estimator
- File: `bigcode_eval/tasks/studenteval.py`
- Function: `_estimator()`
- Code Reference:
```python
# Lines 42-49
def _estimator(n, c, k):
    # Implements combinatorial calculation
    # Uses numpy mathematical operations
```
Implements a combinatorial calculation for pass@k estimation using numpy mathematical operations. This is algorithmic evaluation because it applies a predefined statistical formula to compute success probabilities from sample data. The function uses pure mathematical computation—combinatorial probability theory—to derive metrics from execution results, representing a fixed algorithmic transformation independent of any runtime environment.

Evidence 4: BLEU score evaluation
- File: Various task files (referenced in documentation)
- Tasks: `codexglue_code_to_text`, `conala`, `concode`
- Code Reference:
```python
# BLEU score evaluation (documented but not shown in excerpts)
```
The documentation mentions BLEU score evaluation for tasks like `codexglue_code_to_text`, `conala`, and `concode`. BLEU is a well-known algorithmic metric based on n-gram matching and precision calculations. This is algorithmic evaluation because BLEU applies a fixed mathematical formula that compares generated text against reference translations using n-gram overlap statistics—it's a predetermined scoring algorithm that operates on string comparisons without requiring any environmental interaction or code execution.