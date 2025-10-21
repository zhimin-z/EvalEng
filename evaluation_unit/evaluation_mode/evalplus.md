## Evaluation Mode Categories

[Dynamic Execution, Interactive Simulation]

## Detailed Analysis

### Dynamic Execution

Evidence 1: Code correctness evaluation through sandboxed execution
- File: `evalplus/evaluate.py`
- Function: `check_correctness()` and `untrusted_check()`
- Code Reference:
```python
def check_correctness(
    dataset: str,
    completion_id: int,
    problem: Dict[str, Any],
    solution: str,
    expected_output: Dict[str, List],
    base_only=False,
    fast_check=False,
    identifier=None,
    min_time_limit: float = DEFAULT_MIN_TIME_LIMIT,
    gt_time_limit_factor: float = DEFAULT_GT_TIME_LIMIT_FACTOR,
) -> Dict[str, Result]:
    ret = {
        "completion_id": completion_id,
        "task_id": problem["task_id"],
        "_identifier": identifier,
        "solution": solution,
    }
    ret["base"] = untrusted_check(
        dataset,
        solution,
        problem["base_input"],
        problem["entry_point"],
        expected=expected_output["base"],
        atol=problem["atol"],
        ref_time=expected_output["base_time"],
        fast_check=fast_check,
        min_time_limit=min_time_limit,
        gt_time_limit_factor=gt_time_limit_factor,
    )
```
The harness implements Dynamic Execution by running model-generated Python code in controlled sandboxed environments for correctness evaluation. This provides runtime execution of code solutions with configurable time limits and expected output validation, enabling direct functional correctness testing through actual execution rather than static analysis.

Evidence 2: Unsafe execution with resource constraints
- File: `evalplus/eval/__init__.py`
- Function: `unsafe_execute()`
- Code Reference:
```python
def unsafe_execute(
    dataset: str,
    entry_point: str,
    code: str,
    inputs,
    expected: List,
    time_limits,
    atol,
    fast_check,
    stat,  # Value
    details,  # Array
    progress,  # Value
):
    with create_tempdir():
        # These system calls are needed when cleaning up tempdir.
        import os
        import shutil

        rmtree = shutil.rmtree
        rmdir = os.rmdir
        chdir = os.chdir
        # Disable functionalities that can make destructive changes to the test.
        reliability_guard(maximum_memory_bytes=query_maximum_memory_bytes())
        exec_globals = {}
        try:
            with swallow_io():
                exec(code, exec_globals)
                fn = exec_globals[entry_point]

            for i, inp in enumerate(inputs):
                try:
                    with time_limit(time_limits[i]):
                        with swallow_io():
                            out = fn(*inp)
```
This function demonstrates actual execution of model-generated Python code with comprehensive safety mechanisms. The execution occurs within temporary directories with disabled destructive operations, memory limits via `reliability_guard()`, time constraints through `time_limit()`, and I/O isolation using `swallow_io()`. This multi-layered sandboxing approach enables safe Dynamic Execution while testing functional correctness across multiple test inputs.

Evidence 3: Performance profiling through execution
- File: `evalplus/evalperf.py`
- Function: `perf_worker()` for EvalPerf
- Code Reference:
```python
def perf_worker(
    task_id: str,
    ptask: Dict,  # EvalPerf data
    ret_dict: Dict,
    lazy_evaluation: bool,
    max_profile: int,
):
    rich.print(f"{task_id}: Started")
    start_time = time.time()

    ######################### Profiling Setup #########################
    n_reference = len(ptask["reference"])
    entry_point = ptask["entry_point"]
    pe_input = (
        mbpp_deserialize_inputs(task_id, ptask["pe_input"])[0]
        if task_id.startswith("Mbpp/")
        else ptask["pe_input"][0]
    )
    
    # ... profiling code execution ...
    sample_profiles = profile(
        solution,
        entry_point,
        [pe_input],
        timeout_second_per_test=PERF_EVAL_TIMEOUT_SECOND,
    )
```
EvalPerf extends Dynamic Execution to include performance profiling by executing code with instrumentation to measure CPU instruction counts and runtime characteristics. This goes beyond basic correctness testing to evaluate computational efficiency through actual execution, demonstrating how Dynamic Execution enables comprehensive behavioral assessment of generated code.

Evidence 4: Code coverage analysis through execution
- File: `tools/_experimental/evaluate_coverage.py`
- Function: `test_code_coverage()`
- Code Reference:
```python
def test_code_coverage(
    code: str, inputs: List[List[Any]], entry_point: str, mode="branch"
):
    def safety_test(code: str, inputs: List[List[Any]], entry_point: str):
        for input_list in inputs:
            code += f"{entry_point}({construct_inputs_sig(input_list)})\n"
        reliability_guard()
        try:
            with swallow_io():
                with time_limit(1):
                    exec(code, {})
```
The coverage testing functionality demonstrates Dynamic Execution for analyzing code quality metrics. By executing model-generated code with various inputs while monitoring branch/line coverage, the harness can assess the thoroughness of generated solutions. This execution-based analysis provides insights that static analysis alone cannot capture, validating the necessity of Dynamic Execution for comprehensive code evaluation.

---

### Interactive Simulation

Evidence 1: Multi-step correctness checking with profiling
- File: `evalplus/evalperf.py`
- Function: `perf_worker()` - Reference solution profiling
- Code Reference:
```python
def perf_worker(
    task_id: str,
    ptask: Dict,  # EvalPerf data
    ret_dict: Dict,
    lazy_evaluation: bool,
    max_profile: int,
):
    # ... setup ...
    
    ####################################################################
    ############### Lazily profile reference solutions #################
    ####################################################################
    cache_ref_num_inst = [None] * n_reference

    def get_avg_ref_profile(idx, check_order=True) -> Optional[Tuple]:
        nonlocal cache_ref_num_inst

        assert (
            idx < n_reference - 1
            and cache_ref_num_inst[idx + 1] is not None
            or idx == n_reference - 1
        ), f"Calling get_avg_ref_profile({idx}) before get_avg_ref_profile({idx+1}) is called, is not allowed! {n_reference = }"

        if cache_ref_num_inst[idx] is not None:
            return cache_ref_num_inst[idx], ptask["scores"][idx]

        evaluation_time = PERF_EVAL_TIMEOUT_SECOND
        ref_solution = ptask["reference"][idx]
        for _ in range(2):  # at most retry twice
            profiles = profile(
                ref_solution,
                entry_point,
                [pe_input],
                timeout_second_per_test=evaluation_time,
            )

            # Bad thing#1: timeout / failure happens
            if are_profiles_broken(profiles):
                print(f"{task_id}: [WARNING] Error in ref: {profiles}")
                rich.print(Syntax(ref_solution, "python"))
                print(f"{task_id}: Retrying w/ +10s timeout...")
                evaluation_time += 10
            else:
                break
```
EvalPerf implements Interactive Simulation through iterative profiling with feedback loops and state management. The system maintains persistent state across profiling iterations (via `cache_ref_num_inst`) and adapts its behavior based on execution results—when profiles fail or timeout, it automatically retries with extended timeouts (+10 seconds). This adaptive feedback mechanism demonstrates multi-step interaction where subsequent actions depend on previous execution outcomes, characteristic of Interactive Simulation rather than simple Dynamic Execution.

Evidence 2: Adaptive profiling with state evolution
- File: `evalplus/evalperf.py`
- Function: `perf_worker()` - Solution profiling loop
- Code Reference:
```python
    profile_cache = {}

    cur_profiled = 0
    for result in ret_dict["results"]:
        if cur_profiled >= max_profile:
            rich.print(f"{task_id}: Reached max_profile limit {max_profile}, stopped")
            break
        if not result["pass"]:
            continue

        solution = result["solution"]

        if solution in profile_cache:  # reuse cache
            sample_profiles = profile_cache[solution]
        else:
            sample_profiles = profile(
                solution,
                entry_point,
                [pe_input],
                timeout_second_per_test=PERF_EVAL_TIMEOUT_SECOND,
            )
            profile_cache[solution] = profile_cache  # store cache

        score = 0
        norm_score = 0
        result["matching_cluster_idx"] = -1  # -1 means even slower than the slowest ref
        # if the solution results in a timeout, score is 0
        if are_profiles_broken(sample_profiles):
            print(
                f"{task_id}: Tested solution error'ed out: {sample_profiles} ... regarded as 0 score"
            )
            rich.print(Syntax(solution, "python"))
        else:
            avg_sample_profile = result["_num_cpu_instructions"] = mean(sample_profiles)
            # Get profiles from fast to slow (back to front):
            for j in range(n_reference - 1, -1, -1):
                avg_ref_profile, ref_score = get_avg_ref_profile(j, check_order=False)
                if avg_sample_profile <= avg_ref_profile:
                    result["matching_cluster_idx"] = j
                    score = ref_score
                    norm_score = 100 * (j + 1) / n_reference
                    break

        result["dps"] = score
        result["dps_norm"] = norm_score
        result["profiled"] = True
        cur_profiled += 1
```
The profiling workflow demonstrates Interactive Simulation through state evolution and sequential decision-making across multiple evaluation steps. The system maintains a profile cache to avoid redundant computation, implements early stopping when reaching profiling limits, and makes adaptive decisions based on execution outcomes (skipping failed solutions, comparing performance against reference clusters). Each iteration's results influence subsequent evaluation steps, creating a feedback-driven evaluation process that adapts to model behavior—a hallmark of Interactive Simulation.

Evidence 3: Iterative input generation with feedback
- File: `evalplus/gen/type_mut.py`
- Class: `TypedMutGen`
- Code Reference:
```python
class TypedMutGen(MutateGen):
    def generate(self, num: int):
        start = time.time()
        num_generated = 1
        while len(self.new_inputs) < num and time.time() - start < self.timeout:
            if num_generated % 1000 == 0:
                print(
                    f"generated {num_generated} already with {len(self.new_inputs)} new inputs ... "
                )
            new_input = self.seed_selection()
            # Multi-step instead of single-step
            for _ in range(random.randint(1, MAX_MULTI_STEP_SIZE)):
                new_input = self.mutate(new_input)
            num_generated += 1
            if hash(str(new_input)) not in self.seed_hash:
                if trusted_check_exec(self.contract, [new_input], self.entry_point):
                    self.typed_fetch(new_input)
                    self.seed_pool.append(new_input)
                    self.new_inputs.append(new_input)
                self.seed_hash.add(hash(str(new_input)))
        return self.new_inputs[:num]
```
The mutation-based test input generation demonstrates Interactive Simulation through multi-step iterative processes with validation feedback. Each input undergoes multiple mutation steps (up to `MAX_MULTI_STEP_SIZE`) and is validated through execution (`trusted_check_exec`). Valid inputs are added to the seed pool, creating an evolving state where successful inputs influence future generation. This feedback loop—where execution results determine which inputs join the seed pool for subsequent mutations—exemplifies the state evolution and adaptation characteristic of Interactive Simulation.

Evidence 4: Iterative generation with ChatGPT feedback
- File: `evalplus/gen/chatgpt_gen.py`
- Class: `ChatGPTGen`
- Code Reference:
```python
class ChatGPTGen(BaseGen):
    def __init__(self, inputs: List, signature: str, contract_code: str, gd_code: str):
        super().__init__(inputs, signature, contract_code)
        self.gd_code = gd_code
        self.prompt_messages = [
            "Please generate complex inputs to test the function.",
            "Please generate corner case inputs to test the function.",
            "Please generate difficult inputs to test the function.",
        ]
        self.iteration = 20
        self.client = openai.Client()

    def generate(self, num: int):
        start = time.time()
        while len(self.new_inputs) < num and self.iteration >= 0:
            seeds = self.seed_selection()
            new_inputs = self.chatgpt_generate(seeds)
            for new_input in new_inputs:
                if hash(str(new_input)) not in self.seed_hash:
                    if trusted_check_exec(self.contract, [new_input], self.entry_point):
                        self.seed_pool.append(new_input)
                        self.seed_hash.add(hash(str(new_input)))
                        self.new_inputs.append(new_input)
            self.iteration -= 1
        return self.new_inputs[:num]
```
ChatGPT-based test generation exemplifies Interactive Simulation through multi-turn interaction with external agents and feedback-driven refinement. The system iteratively queries an LLM (up to 20 iterations) to generate test inputs, validates each through execution, and maintains evolving state (seed pool, seed hash). Valid inputs from previous iterations can influence subsequent generation through seed selection. This multi-agent, multi-turn process with validation feedback and state evolution represents a complex Interactive Simulation workflow that extends far beyond simple Dynamic Execution.