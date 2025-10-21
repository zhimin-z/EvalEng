## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Accuracy computation through pairwise comparison
- File: `scripts/run_rm.py`
- Code Reference:
```python
# Line ~251-254: Pairwise comparison
results = [1 if chosen > rejected else 0 for chosen, rejected in zip(scores_chosen, scores_rejected)]

# Line ~311-315: Per-subset accuracy calculation
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    num_correct = sum(subset_dataset["results"])
    num_total = len(subset_dataset["results"])
    print(f"{subset}: {num_correct}/{num_total} ({num_correct/num_total})")
    results_grouped[subset] = num_correct / num_total
```
This demonstrates binary accuracy as a core algorithmic metric. The evaluation performs simple arithmetic comparisons (`chosen > rejected`) to determine correctness, then aggregates results per subset using deterministic mathematical operations. This is purely computational with no learned components—each comparison produces a binary outcome (1 or 0) based on predefined logic.

Evidence 2: Binary correctness evaluation in DPO context
- File: `scripts/run_dpo.py`
- Code Reference:
```python
# Line ~165-169: Binary comparison logic
[
    results.append(1) if chosen > rejected else results.append(0)
    for chosen, rejected in zip(scores_chosen_batch, scores_rejected_batch)
]

# Line ~186-190: Accuracy aggregation
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    num_correct = sum(subset_dataset["results"])
    num_total = len(subset_dataset["results"])
    print(f"{subset}: {num_correct}/{num_total} ({num_correct/num_total})")
```
The binary comparison logic applies the same deterministic evaluation approach in a different training context (DPO). The harness uses identical arithmetic comparison and aggregation patterns, reinforcing that the evaluation is algorithmic—relying on rule-based logic rather than learned representations or subjective judgment.

Evidence 3: Best-of-N scoring and accuracy computation
- File: `scripts/run_v2.py`
- Code Reference:
```python
# Line ~169-174: Pairwise scoring within batches
if isinstance(rewards[0], dict):
    scores_batch = [result["score"] for result in rewards]
else:
    scores_batch = rewards.float().cpu().numpy().tolist()

# Line ~194-206: Accuracy computation per subset
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    if subset.lower() == "ties":
        ties_subset_with_results, overall_score = process_single_model(subset_dataset)
        # ... special ties processing
        results_grouped[subset] = overall_score
    else:
        num_correct = sum(subset_dataset["results"])
        num_total = len(subset_dataset["results"])
        print(f"{subset}: {num_correct}/{num_total} ({num_correct/num_total})")
        results_grouped[subset] = num_correct / num_total
```
This extends the algorithmic evaluation to best-of-N scenarios while maintaining deterministic computation. The code extracts numeric scores and applies predefined mathematical operations (summation, division) to compute accuracy. Even special cases like "ties" processing follow rule-based logic rather than learned evaluation criteria.

Evidence 4: Win rate calculation from generative judgments
- File: `scripts/run_generative.py`
- Code Reference:
```python
# Line ~147-159: Binary win/loss determination from judgments
def process_shuffled(win, shuffle):
    if shuffle:
        winner_text = "B"
        loser_text = "A"
    else:
        winner_text = "A"
        loser_text = "B"
    
    if win == winner_text:
        return 1
    elif win == loser_text:
        return 0
    else:  # if "error"
        return 0.5  # effectively a tie

# Line ~247-251: Accuracy aggregation
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    num_correct = sum(subset_dataset["results"])
    num_total = len(subset_dataset["results"])
    results_grouped[subset] = num_correct / num_total
```
Win rate evaluation uses deterministic text matching to convert judge outputs into numeric scores. The logic is purely rule-based: string comparison against predefined values ("A", "B") maps to numeric outcomes (1, 0, 0.5). This demonstrates that even when using generative models as judges, the harness applies algorithmic processing to quantify results through predetermined rules.

Evidence 5: Weighted score calculation utility
- File: `rewardbench/utils.py`
- Function: `calculate_scores_per_section()`
- Code Reference:
```python
# scripts/run_rm.py, line ~318-320
if not args.pref_sets:
    results_leaderboard = calculate_scores_per_section(EXAMPLE_COUNTS, SUBSET_MAPPING, results_grouped)
    print(results_leaderboard)
```
The harness uses a centralized utility function to compute weighted scores across sections. This function applies predefined weights (example counts per subset) through standard statistical formulas, ensuring consistent and reproducible aggregation. The algorithmic nature is evident in the use of fixed constants and mathematical operations rather than learned weighting schemes.

Evidence 6: Weighted averaging across subsets and categories
- File: `analysis/get_benchmark_results.py`
- Code Reference:
```python
# Line ~74-77: Weighted average computation
def get_average_over_rewardbench(...):
    sub_data = new_df[subset_cols].values
    sub_counts = [EXAMPLE_COUNTS[s] for s in subset_cols]
    new_df[subset] = np.average(sub_data, axis=1, weights=sub_counts)

# Line ~93-96: Final weighted average across categories
final_data = new_df[data_cols].values
masked_data = np.ma.masked_array(final_data, np.isnan(final_data))
weights = [2, 2, 2, 2, 1]
average = np.ma.average(masked_data, axis=1, weights=weights)
```
The final aggregation demonstrates sophisticated algorithmic processing through weighted averaging. The code uses predefined weight vectors (both data-driven example counts and fixed category weights) and applies numpy's mathematical operations to compute final scores. This multi-level aggregation maintains the algorithmic characteristic: all computations are deterministic, reproducible, and based on established statistical formulas rather than learned or subjective criteria.