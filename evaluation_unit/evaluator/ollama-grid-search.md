## Evaluator Categories

[Human, Algorithmic]

## Detailed Analysis

### Human

Evidence 1: Visual inspection and manual comparison workflow
- File: `README.md`
- Code Reference:
```
"This project automates the process of selecting the best models, prompts, or inference 
parameters for a given use-case, allowing you to iterate over their combinations and to 
visually inspect the results."
```
While ollama-grid-search is not a traditional evaluation harness since it does not automatically score or judge model outputs, it serves as an evaluation mechanism by enabling human evaluators to systematically compare models through prompting techniques. The tool facilitates visual inspection by humans rather than providing automated evaluation, making the human the primary evaluator who assesses quality and selects the best configurations based on their judgment.

Evidence 2: A/B testing for manual comparison
- File: `README.md`
- Code Reference:
```
"A/B Testing: Similarly, you can perform A/B tests by selecting different models 
and compare results for the same prompt/parameter combination"
```
The tool explicitly supports manual human comparison through A/B testing workflows. This enables model developers to systematically evaluate different models or configurations by presenting results side-by-side for human judgment, confirming that humans serve as the evaluators who determine which outputs are superior.

---

### Algorithmic

Evidence 1: Token throughput calculation
- File: `src/lib/index.ts`
- Function: `tokensPerSecond()`
- Code Reference:
```typescript
export function tokensPerSecond(interval: number, tokens: number): number {
  const seconds = interval / 1e9;
  const tokensPerSecond = tokens / seconds;
  return parseFloat(tokensPerSecond.toFixed(2));
}
```
The harness implements algorithmic evaluators through deterministic performance metrics. This function computes token generation throughput as a reproducible, quantitative measure that helps developers assess model efficiency. While not evaluating output quality, these algorithmic metrics provide objective performance measurements that complement human evaluation.

Evidence 2: Performance metrics in response interface
- File: `src/Interfaces/index.ts`
- Interface: `IResponsePayload`
- Code Reference:
```typescript
export interface IResponsePayload {
  model: string;
  created_at: string;
  response: string;  // Raw response text only
  done: boolean;
  context: number[];
  total_duration: number;
  prompt_eval_count: number;
  prompt_eval_duration: number;
  eval_count: number;  // Token count, not evaluation score
  eval_duration: number;
}
```
The interface captures multiple algorithmic performance metrics including duration, token counts, and evaluation timing. These deterministic measurements provide quantitative data about model performance characteristics (speed, throughput) that can be compared across different configurations without subjective judgment.

Evidence 3: Query functions for metric retrieval
- File: `src/components/queries/index.ts`
- Functions: `get_inference()`, `get_experiments()`
- Code Reference:
```typescript
// Functions available:
- get_inference() - Retrieves inference results
- get_models() - Lists available models
- get_all_prompts() - Retrieves prompts
- get_ollama_version() - Gets version info
- get_experiments() - Retrieves past experiments
```
These query functions retrieve and organize performance data from experiments, enabling systematic collection of algorithmic metrics across multiple model runs. The functions support reproducible measurement by providing consistent access to quantitative performance data without performing any quality assessment of the outputs themselves.