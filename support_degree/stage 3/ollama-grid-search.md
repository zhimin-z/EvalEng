# ollama-grid-search - Stage 3 (EXECUTE) Evaluation

## Summary
ollama-grid-search is a desktop application (Tauri-based) for evaluating LLM models through Ollama, focusing on parameter grid search and A/B testing. It has minimal execution orchestration capabilities, basic telemetry through the UI, no test-time optimizations beyond what Ollama provides, rudimentary failure handling, basic checkpointing via experiments, no distributed execution support, and no human evaluation features. It's designed as a single-user desktop tool rather than a scalable evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S3F1: Pipeline Orchestration | 1 | Sequential execution with manual orchestration. The app queues inference requests sequentially or with limited concurrency (max 5) through React Query. From `form-grid-params.tsx`: `concurrent_inferences: z.coerce.number().min(1).max(5)` and the config shows `concurrent_inferences: 1` as default. There's no DAG support, no conditional branching, and no protocol selection - just iterating over parameter combinations. The workflow in `docs/app-workflow.mermaid` shows a simple loop structure without sophisticated orchestration. |
| S3F2: Inference & Telemetry | 2 | Basic latency/throughput with some metadata. The app captures basic metrics from Ollama responses: `eval_duration`, `total_duration`, `eval_count`, `prompt_eval_count`, and calculates throughput. From `experiment-data-dialog.tsx`: shows "Eval Duration", "Total Duration", "Throughput (tokens/total_duration)". From `lib/index.ts`: `tokensPerSecond()`, `convertNanosecondsToTime()`, `formatInterval()` functions. However, no P50/P95/P99 percentiles, no real-time monitoring dashboard, no GPU utilization tracking, and no cost tracking beyond token counts. |
| S3F3: Test-Time Optimization | 0 | No optimization features. The application passes parameters to Ollama but implements no caching, batching, or optimization techniques itself. All requests go through Ollama's API with no prompt caching, no response caching, no dynamic batching, and no speculative decoding. The code shows no evidence of any test-time compute optimization - it's purely a parameter exploration tool. |
| S3F4: Failure Handling | 1 | Minimal error handling, manual intervention needed. There's a basic timeout setting (`request_timeout: 300` seconds in configs), and React Query provides automatic retries, but no exponential backoff configuration visible. From `form-grid-params.tsx`: users can manually "Stop Experiment" but this just cancels queries: `queryClient.cancelQueries({ queryKey: ["get_inference"] })`. No circuit breakers, no intelligent retry strategies, no fallback mechanisms. Errors appear to be handled at the UI level with basic alerts. |
| S3F5: Checkpointing | 1 | Minimal checkpoint support via experiment logs. Experiments are saved to a SQLite database with results as they complete (from `db.rs` migrations). However, there's no automatic resumption capability - users must manually re-run experiments. From `issue_with_form_params.md`: "Check why the experiment files seem to be keeping only one value for each param" suggests incomplete state persistence. No incremental evaluation beyond what's already completed and stored. The checkpoint is essentially just the final results, not mid-experiment state. |
| S3F6: Distributed Execution | 0 | Single-device only. This is a desktop application with no multi-GPU, multi-node, or cluster support. All execution happens on the local machine through the Ollama API. The concurrent_inferences setting (max 5) is just for HTTP request concurrency, not true distributed execution. No evidence of Ray, Dask, Slurm, or Kubernetes integration. No budget enforcement beyond the timeout setting. |
| S3F7: Human Evaluation | 0 | No human evaluation features. The app is purely for automated LLM inference and comparison. No crowdsourcing integration, no annotation interfaces, no quality control mechanisms, and no inter-rater agreement metrics. The "Prompt Archive" feature is for storing prompts, not for human annotation. Users can visually inspect results but there's no structured human evaluation workflow. |

## Stage 3 Total: 5/21 (23.8%)

## Key Strengths
1. Clean experiment logging: Results are persisted to SQLite with metadata, making them inspectable later
2. Basic telemetry: Captures essential timing metrics from Ollama (eval time, total time, throughput)
3. Parameter iteration: Effectively iterates over parameter combinations for grid search
4. UI-driven workflow: User-friendly interface for comparing results visually

## Key Weaknesses
1. No execution orchestration: Sequential processing with no DAG, dependencies, or conditional workflows
2. No optimization: Completely dependent on Ollama's performance; no caching, batching, or other optimizations
3. Limited resilience: Basic timeout and manual stop, but no sophisticated error handling or recovery
4. No distributed support: Desktop app with no scaling capabilities beyond local concurrency
5. No checkpointing for resumption: Can't resume interrupted experiments; must restart
6. No human evaluation: Purely automated evaluation with no annotation workflows

## Evidence-Based Observations

Concurrent Execution (Limited):
```typescript
// src/components/settings-dialog.tsx
concurrent_inferences: z.coerce.number().min(1).max(5),
// Defaults to 1, max 5 concurrent requests
```

Basic Telemetry:
```typescript
// src/components/experiment-data-dialog.tsx
<div className="font-mono text-gray-700 dark:text-gray-400">
  Eval Duration: {formatInterval(convertNanosecondsToTime(inf.result.eval_duration))}
</div>
<div className="font-mono text-gray-700 dark:text-gray-400">
  Throughput (tokens/total_duration): {tokensPerSecond(inf.result.total_duration, inf.result.eval_count)} tokens/s
</div>
```

Experiment Persistence:
```sql
-- src-tauri/migrations/20241124000000_create_experiment_table.sql
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created TEXT NOT NULL,
    contents TEXT NOT NULL,
    experiment_uuid TEXT UNIQUE NOT NULL
);
```

Simple Sequential Execution:
```typescript
// src/components/form-grid-params.tsx
function onSubmit(data: z.infer<typeof ParamsFormSchema>) {
  // Clear previous results (keep queries sequential)
  queryClient.removeQueries({ queryKey: ["get_inference"] });
  
  // Regenerate uuid for this experiment so all results are refreshed
  setFormValues({
    ...data,
    experiment_uuid: uuidv4(),
    // Convert form arrays to numeric arrays
  });
}
```

## Architectural Limitations

This tool is fundamentally a desktop GUI for Ollama parameter exploration, not an evaluation framework. It excels at its intended use case (manual parameter tuning and A/B testing for individuals) but lacks the infrastructure needed for production-scale evaluation pipelines. The Tauri + React architecture prioritizes user experience over execution scalability, and the reliance on Ollama means all actual inference optimization happens externally.