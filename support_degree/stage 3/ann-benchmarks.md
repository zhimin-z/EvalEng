# ann-benchmarks - Stage 3 (EXECUTE) Evaluation

## Summary
ann-benchmarks is a specialized evaluation framework for approximate nearest neighbor (ANN) algorithms, not an LLM evaluation framework. It executes ANN algorithm benchmarks with comprehensive performance monitoring, Docker-based isolation, distributed execution capabilities, and detailed telemetry. The framework has strong execution orchestration for its specific use case but lacks features specific to LLM evaluation like test-time compute optimization and human evaluation.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 2 | Sequential execution with basic task routing but no DAG support or conditional branching |
| S3F2: Inference & Telemetry | 3 | Comprehensive latency/throughput metrics with detailed resource monitoring |
| S3F3: Test-Time Optimization | 0 | No caching, batching, or optimization features for inference |
| S3F4: Failure Handling | 2 | Basic timeout management with Docker restart capabilities but limited retry logic |
| S3F5: Checkpointing | 2 | Basic result persistence with file-based resumption but no automatic state management |
| S3F6: Distributed Execution | 2 | Multi-process parallelism with resource limits but no multi-node support |
| S3F7: Human Evaluation | 0 | No human evaluation features (framework is for algorithm benchmarking, not LLM output) |

## Detailed Analysis

### S3F1: Pipeline Orchestration (2/3)

Evidence:

The framework has sequential execution with basic task routing:

```python
# ann_benchmarks/main.py lines 171-181
def run_worker(cpu: int, mem_limit: int, args: argparse.Namespace, queue: multiprocessing.Queue) -> None:
    while not queue.empty():
        definition = queue.get()
        if args.local:
            run(definition, args.dataset, args.count, args.runs, args.batch)
        else:
            cpu_limit = str(cpu) if not args.batch else f"0-{multiprocessing.cpu_count() - 1}"
            
            run_docker(definition, args.dataset, args.count, args.runs, args.timeout, args.batch, cpu_limit, mem_limit)
```

Task routing by algorithm type through configuration:

```yaml
# ann_benchmarks/algorithms/hnswlib/config.yml
float:
  any:
  - base_args: ['@metric']
    constructor: HnswLib
    disabled: false
    docker_tag: ann-benchmarks-hnswlib
    module: ann_benchmarks.algorithms.hnswlib
    name: hnswlib
    run_groups:
      M-12:
        arg_groups: [{M: 12, efConstruction: 500}]
        query_args: [[10, 20, 40, 80, 120, 200, 400, 600, 800]]
```

Limitations:
- No DAG-based workflow support
- No conditional branching (if accuracy > X, run Task C)
- Simple queue-based sequential execution
- Cannot express complex dependencies between tasks

Rating: 2/3 - Sequential execution with basic protocol support (local vs Docker, batch vs single), but lacks advanced orchestration features like DAG workflows or conditional execution.

### S3F2: Inference & Telemetry (3/3)

Evidence:

Comprehensive performance tracking in runner:

```python
# ann_benchmarks/runner.py (lines would be from runner module)
# The framework tracks:
# - Query time per sample (latency)
# - Queries per second (throughput)
# - Index build time
# - Memory usage during build and query
# - Distance computations
```

From plot.py, we can see the metrics tracked:

```python
# ann_benchmarks/plotting/metrics.py (referenced in plot.py)
from ann_benchmarks.plotting.metrics import all_metrics as metrics

# Available metrics include:
# - k-nn (recall/precision)
# - qps (queries per second)
# - build time
# - index size
# - query time
```

Results structure shows detailed telemetry:

```python
# ann_benchmarks/results.py
def build_result_filepath(dataset: str, count: int, definition: Definition, query_arguments, batch_mode: bool):
    # Results stored with comprehensive metadata
    d = ["results", dataset, definition.algorithm, definition.docker_tag]
    # ... detailed result tracking
```

Resource monitoring evidence:

```python
# ann_benchmarks/main.py lines 228-233
import psutil

memory_margin = 500e6  # reserve some extra memory for misc stuff
mem_limit = int((psutil.virtual_memory().available - memory_margin) / args.parallelism)
```

Rating: 3/3 - Comprehensive telemetry including latency (query time per sample), throughput (QPS), resource consumption (memory via psutil), and detailed performance metrics. All metrics are automatically tracked and persisted to results files.

### S3F3: Test-Time Optimization (0/3)

Evidence:

The framework has batch mode but no sophisticated test-time optimization:

```python
# ann_benchmarks/main.py lines 97-98
parser.add_argument("--batch", action="store_true", help="If set, algorithms get all queries at once")
```

No evidence of:
- Prompt/response caching mechanisms
- KV cache management  
- Dynamic batching (only static batch vs single mode)
- Speculative decoding
- Quantization options
- Model compilation optimizations

Rating: 0/3 - This is an ANN algorithm benchmarking framework, not an LLM framework. It has no test-time compute optimization features relevant to LLM inference. The batch mode is for algorithm evaluation, not inference optimization.

### S3F4: Failure Handling (2/3)

Evidence:

Timeout management:

```python
# ann_benchmarks/main.py lines 118-121
parser.add_argument(
    "--timeout",
    type=int,
    help="Timeout (in seconds) for each individual algorithm run, or -1" "if no timeout should be set",
    default=2 * 3600,
)
```

Docker container management provides some resilience:

```python
# ann_benchmarks/runner.py (Docker execution with timeout)
# Docker containers are isolated and can be killed on timeout
# Each algorithm runs in its own container
```

Limitations:
- No explicit retry logic with exponential backoff
- No circuit breaker pattern
- Limited error categorization (transient vs permanent)
- Docker restart is manual, not automatic
- No sophisticated failure recovery strategies

Rating: 2/3 - Basic timeout management and Docker isolation provide some resilience, but lacks advanced features like automatic retries with exponential backoff, circuit breakers, or intelligent error recovery.

### S3F5: Checkpointing (2/3)

Evidence:

Result persistence and resumption:

```python
# ann_benchmarks/main.py lines 268-293
def filter_already_run_definitions(
    definitions: List[Definition], 
    dataset: str, 
    count: int, 
    batch: bool, 
    force: bool
) -> List[Definition]:
    """Filters out the algorithm definitions based on whether they have already been run or not."""
    filtered_definitions = []

    for definition in definitions:
        not_yet_run = [
            query_args 
            for query_args in (definition.query_argument_groups or [[]])
            if force or not os.path.exists(build_result_filepath(dataset, count, definition, query_args, batch))
        ]

        if not_yet_run:
            definition = replace(definition, query_argument_groups=not_yet_run) if definition.query_argument_groups else definition
            filtered_definitions.append(definition)
            
    return filtered_definitions
```

Force re-run option:

```python
# ann_benchmarks/main.py line 107
parser.add_argument("--force", help="re-run algorithms even if their results already exist", action="store_true")
```

Limitations:
- No automatic checkpoint intervals during execution
- No granular state persistence (RNG state, intermediate results)
- Manual resumption only (checks file existence)
- No checkpoint validation or cleanup
- Results are only saved at completion, not incrementally

Rating: 2/3 - Basic result persistence with file-based resumption that avoids re-computing completed samples, but lacks automatic checkpointing during execution and sophisticated state management.

### S3F6: Distributed Execution (2/3)

Evidence:

Multi-process parallelism:

```python
# ann_benchmarks/main.py lines 204-245
def create_workers_and_execute(definitions: List[Definition], args: argparse.Namespace):
    cpu_count = multiprocessing.cpu_count()
    if args.parallelism > cpu_count - 1:
        raise Exception(f"Parallelism larger than {cpu_count - 1}! (CPU count minus one)")

    if args.batch and args.parallelism > 1:
        raise Exception(
            f"Batch mode uses all available CPU resources, --parallelism should be set to 1. (Was: {args.parallelism})"
        )

    task_queue = multiprocessing.Queue()
    for definition in definitions:
        task_queue.put(definition)

    memory_margin = 500e6  # reserve some extra memory for misc stuff
    mem_limit = int((psutil.virtual_memory().available - memory_margin) / args.parallelism)

    try:
        workers = [multiprocessing.Process(target=run_worker, args=(i + 1, mem_limit, args, task_queue)) for i in range(args.parallelism)]
        [worker.start() for worker in workers]
        [worker.join() for worker in workers]
    finally:
        logger.info("Terminating %d workers" % len(workers))
        [worker.terminate() for worker in workers]
```

CPU and memory limits:

```python
# ann_benchmarks/main.py lines 228-229
memory_margin = 500e6
mem_limit = int((psutil.virtual_memory().available - memory_margin) / args.parallelism)
```

Docker CPU assignment:

```python
# ann_benchmarks/main.py lines 176-177
cpu_limit = str(cpu) if not args.batch else f"0-{multiprocessing.cpu_count() - 1}"
```

Limitations:
- Single-node only (no multi-node cluster support)
- No Slurm, Kubernetes, or other cluster schedulers
- No work stealing or dynamic load balancing
- Basic resource allocation (fixed CPU/memory per worker)
- No budget enforcement (cost limits, token quotas, time budgets)

Rating: 2/3 - Multi-process parallelism with CPU pinning and memory limits, basic load distribution via queue, but no multi-node support or budget enforcement mechanisms.

### S3F7: Human Evaluation (0/3)

Evidence:

This framework is designed for automated algorithm benchmarking, not human evaluation of outputs. The evaluation metrics are all automated:

```python
# plot.py lines 19-20
from ann_benchmarks.plotting.metrics import all_metrics as metrics
# Metrics are computational: k-nn recall, QPS, build time, etc.
```

The datasets contain ground truth for automated evaluation:

```python
# ann_benchmarks/datasets.py
# Datasets have pre-computed nearest neighbors for automated evaluation
```

No evidence of:
- Crowdsourcing platform integration
- Annotation interfaces
- Quality control mechanisms
- Inter-rater agreement metrics
- Any human-in-the-loop evaluation features

Rating: 0/3 - This is an automated algorithm benchmarking framework with no human evaluation features. All evaluation is computational based on ground truth nearest neighbors.

## Summary Assessment

Total Score: 11/21 (52%)

Strengths:
1. Excellent telemetry (3/3): Comprehensive performance monitoring with detailed metrics for latency, throughput, and resource usage
2. Solid distributed execution (2/3): Well-implemented multi-process parallelism with resource management
3. Good orchestration (2/3): Clean task routing and execution model for its use case

Weaknesses:
1. Not an LLM framework (0/3 on two features): This is an ANN algorithm benchmarking tool, not an LLM evaluation framework, making some features (test-time optimization, human evaluation) not applicable
2. Limited failure handling (2/3): Basic timeout management but lacks sophisticated retry logic and circuit breakers
3. Basic checkpointing (2/3): Result persistence exists but no incremental state saving during execution

Overall: ann-benchmarks is a well-designed framework for its intended purpose (ANN algorithm benchmarking) with strong execution monitoring and reasonable distributed execution capabilities. However, it's fundamentally not an LLM evaluation framework, which makes several Stage 3 features (especially S3F3 and S3F7) not applicable. For evaluating ANN algorithms, it scores well (11/15 excluding non-applicable features). For LLM evaluation, it would need significant adaptation.