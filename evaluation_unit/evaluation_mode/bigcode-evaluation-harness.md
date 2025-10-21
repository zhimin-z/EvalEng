# Evaluation Mode Categories

[Dynamic Execution, Static Analysis]

## Detailed Analysis

### Dynamic Execution

Evidence 1: Core code execution module with sandboxed environments
- File: `bigcode_eval/tasks/custom_metrics/code_eval.py`
- Function: `compute_code_eval()` and `check_correctness()`
- Code Reference:
```python
def compute_code_eval(predictions, references, k=[1, 10, 100], num_workers=4, timeout=3.0):
    """Returns the scores"""
    if os.getenv("HF_ALLOW_CODE_EVAL", 0) != "1":
        raise ValueError(_WARNING)
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        completion_id = Counter()
        n_samples = 0
        results = defaultdict(list)
        
        for task_id, (candidates, test_case) in enumerate(zip(predictions, references)):
            for candidate in candidates:
                test_program = candidate + "\n" + test_case
                args = (test_program, timeout, task_id, completion_id[task_id])
                future = executor.submit(check_correctness, *args)
```
This is the core code execution module that runs model-generated code in sandboxed environments. The `compute_code_eval()` function takes model predictions (generated code) and executes them against test cases to evaluate correctness. This clearly shows execution of model-generated code (`test_program`) with timeout controls and result capture.

Evidence 2: Main evaluator orchestration for code execution
- File: `bigcode_eval/evaluator.py`
- Function: `evaluate()`
- Code Reference:
```python
def evaluate(self, task_name, intermediate_generations=None):
    task = tasks.get_task(task_name, self.args)
    if task.requires_execution and not self.allow_code_execution:
        raise ValueError(_WARNING)
    
    # ...
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    if self.allow_code_execution and task.requires_execution:
        os.environ["HF_ALLOW_CODE_EVAL"] = "1"
    print("Evaluating generations...")
    results = task.process_results(generations, references)
```
The main evaluator orchestrates code execution by checking if tasks require execution and setting the appropriate environment variable. It controls the execution pipeline and ensures proper environment configuration before running generated code against test cases.

Evidence 3: HumanEval task execution for functional correctness
- File: `bigcode_eval/tasks/humaneval.py`
- Function: `GeneralHumanEval.process_results()`
- Code Reference:
```python
def process_results(self, generations, references):
    """Takes the list of LM generations and evaluates them against ground truth references,
    returning the metric for the generations.
    """
    results, _ = compute_code_eval(
        references=references,
        predictions=generations,
        k=self.k,
        num_workers=self.num_workers,
        timeout=self.timeout,
    )
    return results
```
HumanEval task explicitly executes generated Python code to verify functional correctness. It processes model generations by running them through the code evaluation pipeline with configurable parameters for parallel execution and timeout limits.

Evidence 4: Multi-language code execution with language-specific runtimes
- File: `bigcode_eval/tasks/humanevalpack.py`
- Function: `HumanEvalPackGenerative.process_results()`
- Code Reference:
```python
def process_results(self, generations, references):
    code_metric = load("Muennighoff/code_eval_octopack")
    timeout = LANGUAGE_TO_TIMEOUT[self.DATASET_NAME]
    num_workers = LANGUAGE_TO_NUM_WORKERS[self.DATASET_NAME]
    language = self.DATASET_NAME if self.DATASET_NAME != "js" else "javascript"
    
    # ... language-specific code preprocessing ...
    
    results, logs = code_metric.compute(
        references=references,
        predictions=generations,
        language=language,
        timeout=timeout,
        num_workers=num_workers,
    )
```
Executes model-generated code in multiple programming languages (Python, C++, JavaScript, Java, Go, Rust) using language-specific compilers and runtimes. This demonstrates the harness's capability to perform dynamic execution across diverse programming environments with appropriate tooling for each language.

Evidence 5: Sophisticated sandbox with resource limits and safety guards
- File: `bigcode_eval/tasks/custom_metrics/beyond_eval.py`
- Function: `Sandbox.unsafe_execute()`
- Code Reference:
```python
@staticmethod
def unsafe_execute(sample, result):
    with Sandbox.create_tempdir():
        # Disable functionalities that can make destructive changes to the test.
        Sandbox.reliability_guard()
        
        try:
            namespace = {}
            exec("import re", namespace)
            # ... more imports ...
            
            with Sandbox.swallow_io():
                with Sandbox.time_limit(sample['timeout']):
                    exec(sample['solution'], namespace)
                    exec(f"solution=Solution()", namespace)
                    # ... execute test cases ...
```
Implements a sophisticated sandbox for executing model-generated Python code with resource limits and safety guards. Evaluates both correctness and runtime efficiency by executing code within controlled environments that prevent destructive operations while measuring execution time and validating outputs.

Evidence 6: Language-specific evaluators with compilation and execution
- Files: `bigcode_eval/tasks/custom_metrics/multiple_metrics/eval_rust.py` (and similar files for Python, Java, C++, Go, JavaScript, PHP, Ruby, Scala, Swift, Julia, etc.)
- Code Reference:
```python
def eval_script(path: Path):
    basename = ".".join(str(path).split(".")[:-1])
    try:
        build = subprocess.run(
            ["rustc", path, "-o", basename], capture_output=True, timeout=15
        )
    except subprocess.TimeoutExpired as exc:
        return {"status": "Timeout", ...}
    
    if build.returncode != 0:
        status = "SyntaxError"
    else:
        try:
            output = subprocess.run([basename], capture_output=True, timeout=5)
            if output.returncode == 0:
                status = "OK"
```
Each evaluator compiles and/or executes model-generated code in its respective language. This example from Rust demonstrates the two-phase execution process: compilation verification followed by runtime execution, capturing both syntax correctness and functional behavior.

Evidence 7: Student-written prompt execution with test validation
- File: `bigcode_eval/tasks/studenteval.py`
- Function: `_run_assembled_program()`
- Code Reference:
```python
def _run_assembled_program(item):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
        f.write(item["program"])
        f.flush()
        try:
            result = subprocess.run(
                ["python3", f.name],
                timeout=EXECUTION_TIMEOUT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            exit_code = 1
```
Executes student-written prompts for code generation and validates against test assertions. The function creates temporary files containing generated programs and executes them in isolated processes with timeout protection and output suppression to validate functional correctness.

---

### Static Analysis

Evidence 1: String parsing and pattern matching for code extraction
- File: `bigcode_eval/tasks/humaneval.py`
- Function: `postprocess_generation()`
- Code Reference:
```python
def postprocess_generation(self, generation, idx):
    """Defines the postprocessing for a LM generation."""
    prompt = self.get_prompt(self.dataset["test"][idx])
    generation = generation[len(prompt) :]
    return prompt + self._stop_at_stop_token(generation, self.stop_words)
```
This method performs string parsing and pattern matching on model outputs to extract code snippets without executing them. It uses stop words to detect where generation should end, processing the textual structure of generated code through lexical analysis rather than runtime evaluation.

Evidence 2: Syntactic structure analysis for code truncation
- File: `bigcode_eval/tasks/humanevalpack.py`
- Function: `remove_last_block()` and `check_fn()`
- Code Reference:
```python
def check_fn(self, code):
    """Checks whether the generated code is finished."""
    if any([w in code for w in self.stop_words]): return True
    
    if self.DATASET_NAME == "python":
        for line in code.split("\n"):
            if len(line.strip()) > 0 and line[0] != ' ' and line[0] != '\t':
                return True
    else:
        open_brackets = 2 if self.DATASET_NAME == "java" else 1
        if code.count("{") + open_brackets == code.count("}"):
            return True
    return False
```
These methods analyze the structure of generated code syntactically to determine where to truncate it, checking for brackets and code blocks without execution. The function uses language-specific heuristics to identify code boundaries through pattern matching and indentation analysis.

Evidence 3: Static text processing for markdown code extraction
- File: `bigcode_eval/tasks/instruct_wizard_humaneval.py`
- Function: `clean_comp()`
- Code Reference:
```python
@staticmethod
def clean_comp(completion):
    if "```" in completion:
        def_line = completion.index("```")
        completion = completion[def_line:].strip()
        completion = completion.replace("```", "")
        try:
            next_line = completion.index("```")
            completion = completion[:next_line].strip()
        except:
            pass
    
    if '__name__ == "__main__"' in completion:
        next_line = completion.index('if __name__ == "__main__":')
        completion = completion[:next_line].strip()
```
Performs static text processing to extract code from markdown code blocks and remove boilerplate without executing. This demonstrates pure textual manipulation to clean and normalize generated outputs by identifying and removing common formatting patterns and test harness code.

Evidence 4: Diff format parsing without code execution
- File: `bigcode_eval/tasks/custom_metrics/diff_eval.py`
- Function: `parse_diff_content()` and `split_diff()`
- Code Reference:
```python
def parse_diff_content(
    hunk: str, separate_lines=False, reject_invalid=False
) -> Optional[tuple]:
    """Parse a diff content to turn it into (before_diff, after_diff) 
    based on '+', '-' at the beginning of each line."""
    hunk = hunk.split("\n")
    before_diff, after_diff = [], []
    for line in hunk:
        if not line:
            continue
        if line[0] == "-" or line[0] == " ":
            before_diff.append(line[1:])
        if line[0] == "+" or line[0] == " ":
            after_diff.append(line[1:])
```
Parses diff format outputs without executing any code, analyzing structure and syntax of diffs. The function performs lexical analysis of unified diff format by categorizing lines based on prefix markers, extracting semantic information from the textual representation.

Evidence 5: Pattern matching for stop token detection
- File: `bigcode_eval/base.py` (implied from task structure)
- Function: `_stop_at_stop_token()`
Pattern matching method that examines generated text to find stop tokens without execution. This function is referenced throughout tasks for truncating generations at stop words, using string matching algorithms to identify boundaries in generated content.

Evidence 6: Format validation and structure checking
- Files: `bigcode_eval/tasks/instruct_humaneval.py`, `bigcode_eval/tasks/humanevalpack.py`
- Code Reference:
```python
def postprocess_generation(self, generation, idx):
    """Defines the postprocessing for a LM generation."""
    example = self.get_dataset()[idx]
    prompt, function_name = example["context"], example["entry_point"]
    
    sep_index = generation.find("```")
    if sep_index == -1:
        pass
    else:
        if (generation[sep_index + len("```") : sep_index + len("```")]
            == "python"):
            generation = generation[sep_index + len("```") :]
```
Tasks validate output structure, check for code blocks, parse function signatures, and verify format compliance without executing code. This demonstrates static analysis techniques for ensuring generated outputs conform to expected formats through pattern matching and structural validation.