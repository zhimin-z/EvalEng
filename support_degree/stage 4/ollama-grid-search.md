# ollama-grid-search - Stage 4 (EVALUATE) Evaluation

## Summary
Ollama Grid Search is a desktop application for evaluating LLMs through grid search and A/B testing. It focuses on generating multiple inference outputs across parameter combinations but provides minimal metric computation capabilities. The tool is primarily designed for manual/visual inspection of results rather than automated evaluation with metrics, scoring protocols, or statistical analysis.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No output validation or normalization features present |
| S4F2: Metric Computation | 0 | No metric library or automated scoring capabilities |
| S4F3: Evaluator Models | 0 | No LLM-as-judge or evaluator model integration |
| S4F4: Multi-Modal Scoring | 0 | Text-only, no multi-modal evaluation support |
| S4F5: Aggregate Statistics | 1 | Basic throughput metrics only, no comparison or statistical testing |

---

## Detailed Analysis

### S4F1: Output Validation and Normalization (0/3)

Evidence:

The application generates inference outputs but performs no validation, policy checks, or normalization:

1. No Format Validation: From `src-tauri/src/commands/inference_commands.rs` (lines 91-134), the inference command directly returns the raw response from Ollama without any validation:

```rust
let result = ollama
    .generate(params.to_request(Some(stream)))
    .await
    .map_err(|e| Error::StringError(e.to_string()))?;
```

2. No Policy Compliance: No checks for harmful content, toxicity, or policy violations anywhere in the codebase.

3. No Sanity Checks: Results are stored directly without logical consistency checks or anomaly detection (from `src-tauri/src/commands/experiment_commands.rs`, lines 61-90):

```rust
let new_inference = Inference {
    parameters: inference_parameters,
    result: inference_result,
};
```

4. No Normalization: The UI components display responses verbatim with no standardization (from `src/components/results/grid-result-item.tsx`, lines 126-135):

```tsx
<div className="whitespace-pre-wrap break-words text-cyan-600 dark:text-cyan-600">
  {data.result.response}
</div>
```

Rating Justification: The tool performs no validation or normalization of any kind. It's designed for human inspection of raw outputs.

---

### S4F2: Task-Specific Metric Computation (0/3)

Evidence:

The application has zero metric computation capabilities:

1. No Metrics Library: Search through the entire codebase reveals no BLEU, ROUGE, accuracy, F1, or any other evaluation metrics.

2. Only Basic Throughput: From `src/lib/index.ts` (lines 58-64), the only "metric" computed is tokens per second:

```typescript
export function tokensPerSecond(
  total_duration: number,
  eval_count: number,
): string {
  const time_taken_sec = convertNanosecondsToTime(total_duration);
  return (eval_count / time_taken_sec).toFixed(2);
}
```

3. No Per-Sample Scoring: Results are stored with metadata but no scores (from `src/Interfaces/index.ts`, lines 29-36):

```typescript
export interface IInferenceResult {
  response: string;
  created_at: string;
  eval_count: number;
  eval_duration: number;
  prompt_eval_count: number;
  prompt_eval_duration: number;
  total_duration: number;
}
```

4. No Extensibility: No mechanism to add custom metrics or integrate external evaluation libraries.

Rating Justification: The tool is explicitly designed for visual comparison rather than automated metric computation. From `README.md` (lines 21-24):

> "allowing you to iterate over their combinations and to visually inspect the results."

---

### S4F3: Evaluator Model Integration (0/3)

Evidence:

No evaluator model or LLM-as-judge functionality exists:

1. No Judge Prompts: The application only generates responses from target models, never uses LLMs for evaluation.

2. No Specialized Evaluators: No integration with RAGAS, G-Eval, Prometheus, or any evaluation-specific models.

3. No Ensemble Scoring: Results are independent; no mechanism to have multiple evaluators score the same output.

4. No Rationale Capture: From `src/Interfaces/index.ts` (lines 39-54), the inference structure only captures generation parameters and metadata, no evaluation reasoning:

```typescript
export interface IInference {
  parameters: IInferenceParameters;
  result: IInferenceResult;
}
```

Rating Justification: The tool is focused on generation, not evaluation. No judge or evaluator model capabilities.

---

### S4F4: Multi-Modal Scoring Protocols (0/3)

Evidence:

The application is text-only with no multi-modal support:

1. Text-Only Models: From `src-tauri/Cargo.toml` (line 24), uses `ollama-rs` which supports text generation only:

```toml
ollama-rs = { version = "0.2.0", default-features = false, features = ["rustls"] }
```

2. No Vision/Audio Metrics: No image captioning, VQA, WER, or any multi-modal evaluation metrics in the codebase.

3. Text-Only Interface: From `src/components/results/grid-result-item.tsx` (lines 126-135), results display only text responses:

```tsx
<div className="whitespace-pre-wrap break-words text-cyan-600 dark:text-cyan-600">
  {data.result.response}
</div>
```

4. No Multi-Modal Artifacts: The database schema (from `src-tauri/migrations/`) stores only text prompts and responses.

Rating Justification: Pure text-only tool with no multi-modal evaluation capabilities.

---

### S4F5: Aggregate Statistics and Cross-Model Comparison (1/3)

Evidence:

Very limited statistics, primarily throughput metrics:

1. Basic Throughput Only: From `src/lib/index.ts` (lines 58-64), only tokens/second is computed:

```typescript
export function tokensPerSecond(
  total_duration: number,
  eval_count: number,
): string {
  const time_taken_sec = convertNanosecondsToTime(total_duration);
  return (eval_count / time_taken_sec).toFixed(2);
}
```

2. No Distribution Analysis: Results are displayed individually with no histograms, percentiles, or outlier detection.

3. No Model Comparison: From `src/components/results/grid-results-pane.tsx` (lines 50-72), results are listed sequentially without comparative statistics:

```tsx
{allInferenceQueries.map(({ data }, i) => (
  <GridResultItem
    key={i}
    data={data}
    idx={i}
    hideModelNames={config.hide_model_names}
  />
))}
```

4. No Statistical Testing: No t-tests, Wilcoxon tests, confidence intervals, or significance testing.

5. No Ranking Systems: No Elo ratings, TrueSkill, or leaderboards.

6. Minimal Metadata Display: From `src/components/results/inference-metadata.tsx` (lines 35-97), shows duration and token counts but no statistical aggregations:

```tsx
<div>Eval Count: {data.result.eval_count} tokens</div>
<div>
  Eval Duration:{" "}
  {formatInterval(convertNanosecondsToTime(data.result.eval_duration))}
</div>
<div>
  Total Duration:{" "}
  {formatInterval(convertNanosecondsToTime(data.result.total_duration))}
</div>
<div>
  Throughput (tokens/total_duration):{" "}
  {tokensPerSecond(data.result.total_duration, data.result.eval_count)}{" "}
  tokens/s
</div>
```

Rating Justification: Only basic throughput metrics are computed. No aggregation beyond displaying individual results, no comparative statistics, and no significance testing. The tool requires manual comparison by users.

---

## Key Observations

### Strengths
- Clear focus on generation across parameter combinations
- Good experiment tracking with database storage
- User-friendly interface for visual inspection
- Effective A/B testing support for manual evaluation

### Limitations for Evaluation
1. No Automated Metrics: Completely absent - no BLEU, ROUGE, accuracy, or any standard metrics
2. No Validation: Raw outputs stored without any quality checks
3. Manual Comparison Only: Users must visually compare results themselves
4. No Statistical Analysis: No significance testing or comparative statistics
5. Text-Only: No multi-modal evaluation support

### Use Case Alignment
This tool is designed for:
- Parameter exploration (grid search)
- Visual/manual quality assessment
- Experiment logging and reproducibility

It is not designed for:
- Automated evaluation with metrics
- Statistical comparison of models
- Policy compliance checking
- Multi-modal assessment

### Architecture Note
From the workflow diagram (`docs/app-workflow.mermaid`) and code structure, the application architecture is:
```
React Frontend → Tauri Commands → Ollama API
                              → SQLite Database
```

All evaluation logic would need to be built from scratch, as the current focus is purely on orchestrating generation and storing results.

---

## Overall Stage 4 Score: 1/15

The application provides minimal evaluation capabilities, earning only 1 point for basic throughput metrics. It's fundamentally a generation orchestration tool rather than an evaluation framework, designed for manual inspection rather than automated assessment.