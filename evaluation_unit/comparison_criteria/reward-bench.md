## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Preference Dataset Loading
- File: `tests/test_data.py`
- Code Reference: Dataset loading tests
```python
dataset = load_dataset("allenai/reward-bench", split="filtered")
dataset = load_dataset("allenai/pref-test-sets")
```
These datasets contain preference pairs with explicit labels indicating chosen and rejected responses. The ground truth preferences serve as static reference standards for evaluation.

Evidence 2: Preference Pair Structure
- File: `scripts/run_rm.py`
- Code Reference: Dataset loading with preference fields
```python
dataset, subsets = load_eval_dataset(
    core_set=not args.pref_sets,
    conv=conv,
    custom_dialogue_formatting=custom_dialogue,
    tokenizer=tokenizer,
    logger=logger,
    keep_columns=["text_chosen", "text_rejected", "id"],
)
```
The dataset contains explicit `text_chosen` and `text_rejected` fields representing ground truth preferences. These predetermined labels define which responses should be ranked higher for each instance.

Evidence 3: Binary Correctness Comparison
- File: `scripts/run_rm.py`
- Code Reference: Pairwise comparison evaluation
```python
# pairwise comparison list comprehension
results = [1 if chosen > rejected else 0 for chosen, rejected in zip(scores_chosen, scores_rejected)]
```
Compares model scores against the explicit preference labels. The evaluation checks whether models correctly assign higher scores to chosen responses than rejected responses based on ground truth labels.

Evidence 4: DPO Ground Truth Validation
- File: `scripts/run_dpo.py`
- Code Reference: Preference ranking verification
```python
[
    results.append(1) if chosen > rejected else results.append(0)
    for chosen, rejected in zip(scores_chosen_batch, scores_rejected_batch)
]
```
Similar evaluation pattern checking if model correctly ranks the explicitly labeled chosen response higher. Binary correctness is determined by comparison to predetermined preference labels.

Evidence 5: Dataset Column Specification
- File: `tests/test_data.py`
- Code Reference: Core set loading test
```python
def test_load_core_set_with_conv(self):
    dataset, _ = load_eval_dataset(
        core_set=True,
        conv=self.conv,
        custom_dialogue_formatting=False,
        tokenizer=None,
        keep_columns=["text_chosen", "text_rejected", "prompt"],
    )
```
Confirms the dataset structure includes explicit chosen/rejected labels for evaluation. These columns contain static ground truth annotations defining correct preference orderings.

Evidence 6: Best-of-N Ground Truth
- File: `scripts/run_v2.py`
- Code Reference: Dataset loading with correctness labels
```python
dataset, subsets, total_completions, num_correct = load_bon_dataset_v2(
    dataset=args.dataset,
    conv=conv,
    custom_dialogue_formatting=custom_dialogue,
    tokenizer=tokenizer,
    logger=logger,
)
```
The `num_correct` variable indicates ground truth labels for which completions are correct. These explicit correctness annotations serve as reference standards for Best-of-N evaluation.

Evidence 7: Subset Accuracy Calculation
- File: `scripts/run_rm.py`
- Code Reference: Ground truth comparison aggregation
```python
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    num_correct = sum(subset_dataset["results"])
    num_total = len(subset_dataset["results"])
    print(f"{subset}: {num_correct}/{num_total} ({num_correct/num_total})")
    results_grouped[subset] = num_correct / num_total
```
Calculates accuracy by comparing model predictions to ground truth labels across dataset subsets. The binary results indicate whether model rankings match explicit preference annotations.

Evidence 8: Weighted Score Aggregation
- File: `analysis/get_benchmark_results.py`
- Code Reference: Leaderboard score computation
```python
def get_average_over_rewardbench(
    df: pd.DataFrame,
    df_prefs: pd.DataFrame,
    model_type: str = None,
) -> pd.DataFrame:
    """Get average over a strict subset of reward models"""
    new_df = df.copy()
    for subset, sub_subsets in SUBSET_MAPPING.items():
        subset_cols = [col for col in new_df.columns if col in sub_subsets]
        sub_data = new_df[subset_cols].values
        sub_counts = [EXAMPLE_COUNTS[s] for s in subset_cols]
        new_df[subset] = np.average(sub_data, axis=1, weights=sub_counts)
```
Aggregates accuracy scores across subsets with known example counts. This weighted averaging confirms evaluation is based on comparison to explicit ground truth labels with predetermined correct answers for each preference pair.