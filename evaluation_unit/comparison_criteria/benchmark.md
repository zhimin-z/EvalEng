## Comparison Criteria Categories

[None]

## Detailed Analysis

### None

Evidence 1: Latency Measurement
- File: `torchbenchmark/util/experiment/metrics.py`
- Code Reference: get_latencies() function
```
def get_latencies(func, device: str, nwarmup=WARMUP_ROUNDS, num_iter=BENCHMARK_ITERS) -> List[float]:
    "Run one step of the model, and return the latency in milliseconds."
    # Warm-up `nwarmup` rounds
    for _i in range(nwarmup):
        func()
    result_summary = []
    for _i in range(num_iter):
        if device == "cuda":
            torch.cuda.synchronize()
            t0 = time.time_ns()
            func()
            torch.cuda.synchronize()
            t1 = time.time_ns()
        else:
            t0 = time.time_ns()
            func()
            t1 = time.time_ns()
        result_summary.append((t1 - t0) / NANOSECONDS_PER_MILLISECONDS)
    return result_summary
```
This function measures execution time by capturing timestamps before and after model execution. Latency is computed purely from timing measurements without any comparison to expected outputs, reference implementations, or ground truth labels. The metric evaluates performance efficiency as an intrinsic property of the model.

Evidence 2: Memory Profiling
- File: `torchbenchmark/util/experiment/metrics.py`
- Code Reference: get_peak_memory() function
```
def get_peak_memory(func, device: str, num_iter=MEMPROF_ITER, export_metrics_file="", 
                    metrics_needed=[], metrics_gpu_backend="torch", cpu_monitored_pid=None) -> Tuple[Optional[float], Optional[str], Optional[float]]:
    "Run one step of the model, and return the peak memory in MB."
    # ...
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
    for _ in range(num_iter):
        work_func()
    if device == "cuda":
        device_id = torch.cuda.current_device()
        gpu_peak_mem = torch.cuda.max_memory_allocated() / 10**9
    total = psutil.virtual_memory().total
    percentage = psutil.Process(os.getpid()).memory_percent()
    cpu_peak_mem = percentage * total / 10**9
```
Memory profiling tracks GPU and CPU memory usage during model execution using system monitoring APIs. Peak memory is measured directly from hardware resource utilization without comparing to reference memory profiles or expected memory footprints. This evaluates resource efficiency as an intrinsic characteristic of the model implementation.

Evidence 3: Model Metrics Collection
- File: `torchbenchmark/util/experiment/metrics.py`
- Code Reference: TorchBenchModelMetrics dataclass
```
@dataclasses.dataclass
class TorchBenchModelMetrics:
    latencies: List[float]
    throughputs: List[float]
    cpu_peak_mem: Optional[float]
    gpu_peak_mem: Optional[float]
    ttfb: Optional[float]  # time-to-first-batch
    pt2_compilation_time: Optional[float]
    pt2_graph_breaks: Optional[float]
    model_flops: Optional[float]
```
The metrics dataclass defines intrinsic performance and efficiency measures collected during model execution. All metrics (latency, throughput, memory usage, compilation time, FLOPS) are computed from direct observation of model behavior without requiring external references, baseline comparisons, or ground truth validation.

Evidence 4: FLOPS Computation
- File: `torchbenchmark/util/experiment/metrics.py`
- Code Reference: get_model_flops() function
```
def get_model_flops(model_config: TorchBenchModelConfig) -> float:
    "Run one step of the eager model, and return the model total flops."
    # ...
    from torch.utils.flop_counter import FlopCounterMode
    flop_counter = FlopCounterMode()
    
    with flop_counter:
        work_func()
    total_flops = sum([v for _, v in flop_counter.flop_counts["Global"].items()])
```
FLOPS measurement uses PyTorch's internal FlopCounterMode to count floating-point operations during model execution. This computational efficiency metric is derived entirely from analyzing the model's operation graph without comparing to reference implementations or expected operation counts. The harness measures what the model actually does, not how well it matches external specifications.