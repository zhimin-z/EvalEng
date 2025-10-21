## Evaluation Mode Categories

[Dynamic Execution]

## Detailed Analysis

### Dynamic Execution

Evidence 1: Core correctness checking mechanism
- File: `human_eval/execution.py`
- Function: `check_correctness()`
- Code Reference:
```python
def check_correctness(
    problem: Dict, completion: str, timeout: float, completion_id: Optional[int] = None
) -> Dict:
    """
    Evaluates the functional correctness of a completion by running the test
    suite provided in the problem.
    """
    manager = multiprocessing.Manager()
    result = manager.list()

    p = multiprocessing.Process(target=unsafe_execute, args=(problem, completion, timeout, result))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.kill()
```
This function executes model-generated code completions in a controlled environment. It spawns a separate process to run the `unsafe_execute` function with timeout protection, which is a clear indicator of dynamic execution of model outputs.

Evidence 2: Direct code execution implementation
- File: `human_eval/execution.py`
- Function: `unsafe_execute()`
- Code Reference:
```python
def unsafe_execute(problem: Dict, completion: str, timeout: float, result):
    # ... setup code ...
    
    check_program = (
        problem["prompt"]
        + completion
        + "\n"
        + problem["test"]
        + "\n"
        + f"check({problem['entry_point']})"
    )

    try:
        exec_globals = {}
        with swallow_io():
            with time_limit(timeout):
                # Model-generated code execution happens here
                exec(check_program, exec_globals)
        result.append("passed")
    except TimeoutException:
        result.append("timed out")
    except BaseException as e:
        result.append(f"failed: {e}")
```
This function constructs a complete Python program by combining the problem prompt, the model-generated completion, and test cases, then executes it using Python's `exec()` function. This is the core dynamic execution component where model-generated code artifacts are actually run. The execution results are captured (passed/timed out/failed) to evaluate functional correctness.

Evidence 3: Orchestration of parallel execution
- File: `human_eval/evaluation.py`
- Function: `evaluate_functional_correctness()`
- Code Reference:
```python
def evaluate_functional_correctness(
    sample_file: str,
    k: List[int] = [1, 10, 100],
    n_workers: int = 4,
    timeout: float = 3.0,
    problem_file: str = HUMAN_EVAL,
):
    """
    Evaluates the functional correctness of generated samples...
    """
    problems = read_problems(problem_file)

    # Check the generated samples against test suites.
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        completion_id = Counter()
        n_samples = 0
        results = defaultdict(list)

        print("Reading samples...")
        for sample in tqdm.tqdm(stream_jsonl(sample_file)):
            task_id = sample["task_id"]
            completion = sample["completion"]
            args = (problems[task_id], completion, timeout, completion_id[task_id])
            future = executor.submit(check_correctness, *args)
            futures.append(future)
```
This function orchestrates the dynamic execution process by submitting model-generated code completions to a thread pool executor that calls `check_correctness()`. It manages parallel execution of multiple code samples with timeout constraints, collects execution results, and computes pass@k metrics based on whether the executed code passed the test suites.

Evidence 4: Safety infrastructure for code execution
- File: `human_eval/execution.py`
- Function: `reliability_guard()`
- Code Reference:
```python
def reliability_guard(maximum_memory_bytes: Optional[int] = None):
    """
    This disables various destructive functions and prevents the generated code
    from interfering with the test (e.g. fork bomb, killing other processes,
    removing filesystem files, etc.)
    
    WARNING
    This function is NOT a security sandbox...
    """
    # Sets memory limits
    if maximum_memory_bytes is not None:
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (maximum_memory_bytes, maximum_memory_bytes))
    
    # Disables dangerous functions
    os.kill = None
    os.system = None
    shutil.rmtree = None
    subprocess.Popen = None
    # ... etc
```
This function implements safety guards specifically designed for executing untrusted model-generated code. It disables dangerous system calls and sets resource limits, which is infrastructure specifically needed for dynamic execution environments. The existence of these protective measures confirms that the harness executes model outputs in a controlled but live execution environment.

Evidence 5: Explicit documentation of execution model
- File: `README.md`
- Code Reference:
```markdown
**This program exists to run untrusted model-generated code. Users are strongly
encouraged not to do so outside of a robust security sandbox. The [execution
call](https://github.com/openai/human-eval/blob/master/human_eval/execution.py#L48-L58)
in `execution.py` is deliberately commented out to ensure users read this
disclaimer before running code in a potentially unsafe manner.**
```
The documentation explicitly states that this harness runs "untrusted model-generated code" and warns about security implications. This confirms the primary interaction mode is dynamic execution of model outputs, not static analysis or other evaluation methods.