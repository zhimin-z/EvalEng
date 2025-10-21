## Evaluation Mode Categories

[Dynamic Execution, Static Analysis]

## Detailed Analysis

### Dynamic Execution

Evidence 1: Model execution in training mode
- File: `test_bench.py`
- Function: `TestBenchNetwork.test_train()`
- Code Reference:
```python
def test_train(self, model_path, device, benchmark):
    task.make_model_instance(test="train", device=device)
    benchmark(task.invoke)  # Executes the model
```
This evaluation harness executes PyTorch models in training mode to measure their performance characteristics. The `test_train()` function creates a model instance configured for training and invokes it through a benchmark wrapper, allowing the harness to capture execution metrics during actual model training operations.

Evidence 2: Model execution in evaluation mode
- File: `test_bench.py`
- Function: `TestBenchNetwork.test_eval()`
- Code Reference:
```python
def test_eval(self, model_path, device, benchmark, pytestconfig):
    task.make_model_instance(test="eval", device=device)
    benchmark(task.invoke)  # Executes the model
```
Similar to training mode, the harness executes models in evaluation mode to benchmark inference performance. This demonstrates the framework's ability to dynamically run models in different operational states and capture their runtime behavior.

Evidence 3: Training function invocation
- File: `test.py`
- Function: `train_fn()`
- Code Reference:
```python
def train_fn(self):
    task.make_model_instance(test="train", device=device, batch_size=batch_size)
    task.invoke()  # Executes model training
```
The `train_fn()` orchestrates model training execution by instantiating the model with specific configurations and invoking its training routine. This provides direct evidence of dynamic execution where the model's generated artifacts (computational graphs, forward/backward passes) are actually run.

Evidence 4: Evaluation function invocation
- File: `test.py`
- Function: `eval_fn()`
- Code Reference:
```python
def eval_fn(self):
    task.make_model_instance(test="eval", device=device, batch_size=batch_size)
    task.invoke()  # Executes model evaluation
```
The evaluation function demonstrates controlled execution of inference workloads, allowing the harness to measure model behavior during prediction tasks. This complements training execution by covering the full lifecycle of model operations.

Evidence 5: Latency measurement through execution
- File: `torchbenchmark/util/experiment/metrics.py`
- Function: `get_latencies()`
- Code Reference:
```python
def get_latencies(func, device: str, nwarmup=WARMUP_ROUNDS, num_iter=BENCHMARK_ITERS):
    for _i in range(nwarmup):
        func()  # Warmup execution
    for _i in range(num_iter):
        torch.cuda.synchronize()
        t0 = time.time_ns()
        func()  # Actual model execution
        torch.cuda.synchronize()
        t1 = time.time_ns()
```
This function measures execution latency by repeatedly running the model and timing each invocation. The use of warmup rounds and synchronization barriers demonstrates sophisticated dynamic execution that captures realistic runtime performance, going beyond simple output inspection to measure temporal characteristics of actual execution.

Evidence 6: Memory profiling during execution
- File: `torchbenchmark/util/experiment/metrics.py`
- Function: `get_peak_memory()`
- Code Reference:
```python
def get_peak_memory(func, device: str, num_iter=MEMPROF_ITER, ...):
    def work_func():
        if device == "cuda":
            torch.cuda.synchronize()
            func()  # Execute model
            torch.cuda.synchronize()
```
The harness executes models while monitoring memory consumption, capturing peak memory usage during actual runtime. This requires dynamic execution to observe memory allocation patterns that only emerge when models process data and maintain intermediate activations.

Evidence 7: FLOPS calculation through execution
- File: `torchbenchmark/util/experiment/metrics.py`
- Function: `get_model_flops()`
- Code Reference:
```python
def get_model_flops(model_config: TorchBenchModelConfig) -> float:
    from torch.utils.flop_counter import FlopCounterMode
    flop_counter = FlopCounterMode()
    with flop_counter:
        work_func()  # Execute model to count FLOPs
```
Computing FLOPS (floating point operations per second) requires executing the model under instrumentation to count operations. The harness runs the model within a profiling context that tracks computational operations, demonstrating dynamic execution as a prerequisite for measuring computational efficiency.

Evidence 8: Benchmark orchestration
- File: `run_benchmark.py`
- Function: `run()`
The `run_benchmark.py` script orchestrates the entire benchmarking process, coordinating model execution across different configurations, devices, and batch sizes. This top-level control demonstrates that dynamic execution is the primary mode of operation for the harness, with all measurements deriving from actual model runs in controlled environments.

---

### Static Analysis

Evidence 1: Device placement verification
- File: `test.py`
- Function: `check_device_fn()`
- Code Reference:
```python
def check_device_fn(self):
    task = ModelTask(model_name, timeout=TIMEOUT)
    task.make_model_instance(test="eval", device=device)
    task.check_device()  # Validates device placement without executing
```
The harness includes validation logic that inspects whether model components are correctly placed on target devices (CPU/GPU) without running full execution cycles. This static check verifies configuration correctness by examining model properties and tensor locations, providing quick sanity checks before expensive benchmarking operations.

Evidence 2: Accuracy attribute inspection
- File: `torchbenchmark/util/experiment/metrics.py`
- Function: `get_model_accuracy()`
- Code Reference:
```python
def get_model_accuracy(model_config: TorchBenchModelConfig, ...):
    accuracy_model_config = copy.deepcopy(model_config)
    if not "--accuracy" in accuracy_model_config.extra_args:
        accuracy_model_config.extra_args = ["--accuracy"] + accuracy_model_config.extra_args
    model = load_model(accuracy_model_config)
    accuracy = model.accuracy  # Checks model accuracy attribute
```
The harness retrieves pre-computed accuracy values by inspecting model attributes rather than running full validation cycles. This demonstrates static analysis where the evaluation focuses on examining existing properties and metadata without executing the model on test datasets.

Evidence 3: Output structure validation
- File: `test.py`
- Function: `eval_fn()` with output checking
- Code Reference:
```python
def eval_fn(self):
    task.invoke()
    task.check_details_eval(device=device, md=metadata)
    task.check_eval_output()  # Validates output format/structure
```
After minimal execution, the harness validates that model outputs conform to expected formats and structures. The `check_eval_output()` function performs static inspection of output tensors to ensure they have correct shapes, data types, and value ranges, which is primarily an inspection task rather than performance profiling.

Evidence 4: Metadata and attribute validation
- File: `test.py`
- Function: `example_fn()` with accuracy assertion
- Code Reference:
```python
def example_fn(self):
    accuracy = task.get_model_attribute("accuracy")
    assert (accuracy == "pass" or 
            accuracy == "eager_1st_run_OOM" or 
            accuracy == "eager_2nd_run_OOM"), 
            f"Expected accuracy pass, get {accuracy}"
```
The harness performs static validation of model metadata by retrieving attributes and checking them against expected values. This operation inspects model properties without profiling execution performance, serving as a correctness check that complements the dynamic execution metrics.