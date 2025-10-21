# beir-cellar__beir - Stage 3 (EXECUTE) Evaluation

## Summary
BEIR is a heterogeneous benchmark for evaluating information retrieval models. It focuses on retrieval model evaluation rather than execution orchestration, with minimal infrastructure for pipeline management, failure handling, or resource optimization. The framework is designed for single-node evaluation with basic sequential execution.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 0 | No pipeline orchestration features. BEIR provides simple retrieval evaluation with sequential execution only. Examples show direct model instantiation and evaluation (`model = DRES(...)`, `retriever.retrieve(corpus, queries)`) without DAG support, conditional branching, or multi-protocol handling. Files: `examples/retrieval/evaluation/dense/evaluate_sbert.py` shows linear execution only. |
| S3F2: Inference & Telemetry | 1 | Minimal telemetry. Only basic time tracking exists (`start_time = time()`, `end_time = time()`). No latency percentiles, throughput metrics, memory tracking, or cost monitoring. Evidence from `examples/retrieval/evaluation/dense/evaluate_sbert.py` lines 91-94 shows manual timing without built-in telemetry. |
| S3F3: Test-Time Optimization | 1 | Limited optimization. Supports basic batching (`batch_size=128`) but no caching, dynamic batching, or advanced optimizations. FAISS indexes provide some optimization for dense retrieval (e.g., `evaluate_faiss_dense.py`), but this is external library functionality, not framework-level optimization. |
| S3F4: Failure Handling | 0 | No failure handling mechanisms. No retry logic, timeouts, circuit breakers, or error recovery. Code examples show no error handling patterns - just straightforward execution without resilience features. |
| S3F5: Checkpointing | 1 | Very limited checkpointing. Can save embeddings to disk (`retriever.encode_and_retrieve(..., encode_output_path="...")`) and results (`util.save_runfile()`, `util.save_results()`), but no automatic checkpointing, resume capabilities, or state persistence for interrupted runs. Evidence in `examples/retrieval/evaluation/dense/evaluate_huggingface_pkl_embs.py` lines 76-81. |
| S3F6: Distributed Execution | 1 | Single-node multi-GPU only. The framework supports parallel processing on one machine (`evaluate_sbert_multi_gpu.py` using `torch.distributed`), but no multi-node clustering, job scheduling, or budget enforcement. Evidence: `examples/retrieval/evaluation/dense/evaluate_sbert_multi_gpu.py` lines 24-26 shows `dist.init_process_group("nccl")` for local GPU parallelism only. |
| S3F7: Human Evaluation | 0 | No human evaluation features. No crowdsourcing integration, annotation interfaces, quality control, or agreement metrics. The framework is purely focused on automated IR metrics (NDCG, MAP, etc.). |

## Detailed Analysis

### S3F1: Pipeline Orchestration (0/3)
Evidence:
- All examples show sequential execution without orchestration
- From `examples/retrieval/evaluation/dense/evaluate_sbert.py`:
```python
# Lines 77-89
model = DRES(dense_model, batch_size=128, corpus_chunk_size=50000)
retriever = EvaluateRetrieval(model, score_function="cos_sim")
results = retriever.retrieve(corpus, queries)
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
```
This shows simple linear execution with no workflow management, task routing, or dependency handling.

### S3F2: Inference & Telemetry (1/3)
Evidence:
- Manual timing only, no built-in telemetry
- From `examples/retrieval/evaluation/dense/evaluate_sbert.py`:
```python
# Lines 91-94
start_time = time()
results = retriever.retrieve(corpus, queries)
end_time = time()
print(f"Time taken to retrieve: {end_time - start_time:.2f} seconds")
```
No framework-provided metrics for latency percentiles, throughput, memory, GPU utilization, or costs.

### S3F3: Test-Time Optimization (1/3)
Evidence:
- Basic batching support only
- From `examples/retrieval/evaluation/dense/evaluate_sbert.py`:
```python
# Line 68-73
model = DRES(
    dense_model,
    batch_size=128,
    corpus_chunk_size=50000,
)
```
- FAISS support exists but is external library functionality (`examples/retrieval/evaluation/dense/evaluate_faiss_dense.py`)
- No prompt caching, dynamic batching, or test-time optimization features

### S3F4: Failure Handling (0/3)
Evidence:
- No retry logic, timeouts, or error handling in any examples
- All code assumes successful execution without failure scenarios
- No circuit breaker patterns or graceful degradation

### S3F5: Checkpointing (1/3)
Evidence:
- Can save embeddings and results but no automatic checkpointing
- From `examples/retrieval/evaluation/dense/evaluate_huggingface_pkl_embs.py`:
```python
# Lines 76-81
start_time = time()
results = retriever.encode_and_retrieve(
    corpus=corpus,
    queries=queries,
    encode_output_path=embedding_dir,
    overwrite=False,  # Set to True if you want to overwrite existing embeddings
)
```
- Manual result saving: `util.save_runfile()`, `util.save_results()`
- No state persistence for resuming interrupted evaluations

### S3F6: Distributed Execution (1/3)
Evidence:
- Multi-GPU support on single node only
- From `examples/retrieval/evaluation/dense/evaluate_sbert_multi_gpu.py`:
```python
# Lines 24-28
dist.init_process_group("nccl")
device_id = int(os.getenv("LOCAL_RANK", 0))
torch.cuda.set_device(torch.cuda.device(device_id))
```
- No multi-node clustering, no Slurm/Kubernetes support, no budget enforcement
- Documentation explicitly states single-machine parallelism: `CUDA_VISIBLE_DEVICES=1,2,3,4 torchrun --nproc_per_node=4`

### S3F7: Human Evaluation (0/3)
Evidence:
- No human evaluation capabilities anywhere in the codebase
- Framework focuses exclusively on automated metrics (NDCG, MAP, Recall, Precision, MRR)
- No crowdsourcing, annotation UI, or inter-rater agreement features

## Key Strengths
1. Simple execution model: Easy to understand and use for basic retrieval evaluation
2. Multi-GPU support: Can parallelize on single machine with multiple GPUs
3. Result persistence: Can save embeddings and evaluation results

## Key Limitations
1. No orchestration: Cannot handle complex workflows or multi-stage pipelines
2. No resilience: No failure handling, retries, or recovery mechanisms
3. Minimal telemetry: Only manual timing, no comprehensive performance monitoring
4. Limited optimization: Basic batching only, no advanced test-time optimizations
5. Single-node only: No true distributed execution across clusters
6. No human evaluation: Purely automated metrics

## Overall Stage 3 Score: 4/21 (19%)

BEIR is designed as a simple evaluation benchmark, not an execution framework. It provides the bare minimum for running retrieval evaluations with basic multi-GPU support but lacks nearly all advanced execution features expected in modern ML evaluation frameworks.